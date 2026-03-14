## Question 12 [gregory]

> I-addresses encode a document-level prefix (e.g., `1.1.0.1.0.1.0.1.x`) — does the system ever use this prefix to look up the originating document for a piece of content, or is the hierarchy purely a namespace partitioning convention with no runtime semantic role?

## KB Synthesis

The prefix has active runtime semantic roles — it is not purely a namespace convention — but those roles are confined to allocation time. At retrieval time, a separate index handles document attribution.

## Allocation-time use (active runtime semantics)

During INSERT and MAKELINK, the document ISA is used to compute an upper bound that scopes the `findpreviousisagr` tree search:

- For text: `tumblerincrement(&hintptr->hintisa, 2, atomtype + 1, &upperbound)` bounds the search to the document's content subspace [SS-ADDRESS-SPACE Finding 0065, SS-ADDRESS-ALLOC Finding 0065]
- For links: `upperbound = docISA.2.3` bounds search to the document's link subspace [SS-ADDRESS-ALLOC Finding 0065]
- For documents/versions: `upperbound = tumblerincrement(hintisa, depth-1, 1)` bounds to the parent's child range [SS-ADDRESS-ALLOC Finding 0021]

After finding the candidate address, `tumblertruncate` + `tumblereq` explicitly verify the found address is actually contained under the target parent — this check was added to fix Bug 0013, which showed cross-account allocation when the containment check was missing [PRE-ADDRESS-ALLOC, SS-TUMBLER-CONTAINMENT].

So the document prefix is semantically load-bearing during allocation: the system *derives which I-address range to search* from the document ISA.

## Retrieval-time: prefix NOT parsed

When you have an I-address and need to know which document it came from, the system does **not** parse the prefix. Instead, it uses two separately maintained data structures:

1. **DOCISPAN index** (spanfilade type 4): `insertspanf(..., DOCISPAN)` explicitly records the I-address → document mapping at insert time. `find_documents` queries this index [SS-DOCISPAN, Finding 0036, 0047].

2. **Sporgl `sporgladdress` field**: explicitly stores the source document ISA in the sporgl struct, not derived from the I-address [SS-SPORGL Finding 0013].

3. **POOM crum `homedoc` field**: `isanextensionnd()` reads an explicit `homedoc` stored in the crum, not inferred from the I-address [INV-IADDR-PROVENANCE Finding 0046].

## Summary

| Use | Prefix hierarchy used? | Mechanism |
|-----|----------------------|-----------|
| Allocating next I-address | **Yes** — bounds the search range | `tumblerincrement` on document ISA |
| Verifying allocation stays in-bounds | **Yes** — containment check | `tumblertruncate` + `tumblereq` |
| Looking up originating document | **No** | DOCISPAN index (spanfilade) |
| Provenance in POOM crums | **No** | Explicit `homedoc` field |
| Provenance in sporgls | **No** | Explicit `sporgladdress` field |

The hierarchy is a genuine structural invariant with runtime enforcement during allocation, but once an I-address is allocated, its document of origin is tracked through separately maintained indices rather than by parsing the address itself.

---

## Code Exploration

I now have everything needed for a complete answer. Here it is:

---

## I-Address Prefix: Runtime Semantic Role in udanax-green

**Short answer: The I-address document prefix is not a passive namespace partition. It is the primary lookup key into the granfilade, drives BERT access control, and constrains content allocation — but it does NOT walk the prefix hierarchy at retrieval time to identify "the originating document." That identity must be supplied by the caller.**

---

### 1. The Granfilade Is Indexed by I-Address — Document Lookup via Prefix

The global `granf` structure is a 1D enfilade indexed on the WIDTH dimension using I-addresses as keys. Every document in the system has a leaf node in this tree at its exact I-address, holding its orgl (permutation matrix).

The path is:

`findorgl()` [`granf1.c:17`] → `fetchorglgr()` [`granf2.c:22`] → `retrievecrums()` [`retrie.c:15`] → `findcbcseqcrum()` [`retrie.c:167`]

`findcbcseqcrum` descends the granfilade tree by comparing `address` against each crum's WIDTH span, until it reaches the leaf whose totaloffset equals the requested I-address:

```c
// granf2.c:34-40
if ((context = retrievecrums ((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
    return NULL;
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);  // exact match required
}
```

The I-address prefix thus directly encodes _where in the granfilade tree_ the document's orgl lives. A document at `1.1.0.1.0.1.0.1.x` is found by traversing the WIDTH dimension of the granfilade to that exact position. This is structural, not symbolic.

---

### 2. V↔I Translation Requires Fetching the Document's Orgl First

`specset2ispanset()` [`do2.c:14–46`] shows the critical runtime flow when a retrieve operation arrives with a V-spec (document ISA + V-span set):

```c
// do2.c:34-36
findorgl(taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
    && (ispansetptr = vspanset2ispanset(taskptr, docorgl, ...))
```

The document's I-address (`docisa`) is passed to `findorgl`, which traverses the granfilade to retrieve the orgl. That orgl is then passed to `permute()` [`orglinks.c:404`] to perform the V→I conversion via `span2spanset()`. Without the I-address lookup, there is no orgl, and the V→I mapping is impossible. The I-address prefix is the indirection handle for all document content operations.

---

### 3. BERT Access Control Uses the Exact I-Address

`findorgl()` first calls `checkforopen()` [`bert.c:52`] before touching the granfilade:

```c
// granf1.c:22
if ((temp = checkforopen(isaptr, type, user)) <= 0) { ... return FALSE; }
```

`checkforopen` computes `hashoftumbler(tp)` [`bert.c:234`] — a weighted sum of all mantissa digits and `exp` — and searches `berttable[hash]` for an exact `tumblereq()` match on the full I-address. The BERT table stores one entry per `(connection, documentid)` pair. Access is enforced at the exact I-address level; no prefix walking occurs here.

Account-level ownership is checked via `isthisusersdocument()`, which internally uses `tumbleraccounteq()` [`tumble.c:38`]. That function walks the mantissa comparing until the account tumbler terminates (two consecutive zeros), returning TRUE if the document I-address shares the account prefix at all non-zero positions. This is the one place where a prefix relationship is semantically used — to determine whether an unopened document is "owned" by the current user's account and can be read without an explicit open.

---

### 4. Address Allocation Validates Prefix Membership

`findisatoinsertnonmolecule()` [`granf2.c:203–241`] allocates new I-addresses for new documents/accounts. It:

1. Calls `findpreviousisagr()` to find the highest existing ISA below an upper bound
2. Verifies the found address is actually under `hintptr->hintisa` by truncating and comparing:

```c
// granf2.c:231-232
tumblertruncate(&lowerbound, hintlength, &truncated);
lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
```

3. If the lowerbound is from a different prefix subtree, treats it as absent and generates the first child as `hintisa.0.1`

The prefix is thus a structural constraint on where new identities may be allocated — all content under a document must share that document's I-address prefix.

---

### 5. The `homedoc` Field and `crumqualifies2d` — Dead Code

`crumqualifies2d()` [`retrie.c:270–279`] contains a `homedoc` comparison that _looks_ like it would filter orgl crums by their originating document:

```c
if ((crumptr->height == 0) && infoptr &&
    !tumblereq(&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

However, this is dead code. The only caller that could pass a non-NULL `infoptr` is `retrieverestricted()` [`retrie.c:56`], but `span2spanset()` calls it with `(typeisa*)NULL` at [`orglinks.c:435`]. More definitively, `findcbcinarea2d()` — which receives `infoptr` and passes it to `crumqualifies2d` — contains an explicit guard:

```c
// retrie.c:244-250
if(infoptr){
    fprintf(stderr,"not NULL infoptr versions mumble ... shouldent happen till we try something fancier\n");
    gerror("findcbcinarea2d");
}
```

Both DISTRIBUTION and non-DISTRIBUTION builds call `gerror()` if `infoptr` is non-null. The `homedoc` check was intended future functionality (the comment dates to `11/27/84`) but was never activated.

---

### Summary

| Mechanism | Role of I-address prefix | Active? |
|---|---|---|
| `fetchorglgr` / granfilade lookup | Primary index — prefix encodes tree position of document's orgl | **Yes** |
| `checkforopen` / BERT table | Exact I-address match for per-connection access control | **Yes** |
| `tumbleraccounteq` / ownership | Prefix comparison to determine if document is under user's account | **Yes** |
| `findisatoinsertnonmolecule` | Prefix validates that new ISAs stay within the parent hierarchy | **Yes** |
| `crumqualifies2d` / `homedoc` | Content-level document membership filtering at retrieval | **Dead — never activated** |

The hierarchy is not a pure namespace convention. The prefix is the granfilade's physical index structure, meaning a document at `1.1.0.1.0.1.0.1.x` is found by traversing the WIDTH dimension of the tree to that location. However, the system does **not** dynamically "walk the prefix" to discover which document owns a piece of content at retrieval time — that document identity must be supplied by the caller as an explicit `docisa` argument. The prefix tells you _where_ to look; it does not tell you _what_ to look for without being provided as a query parameter.
