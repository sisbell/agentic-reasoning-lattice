## Question 6 [evidence]

> Does udanax-green enforce that every node address descends from a single root (e.g., via a single global granfilade), or do independent node-allocation trees occur in the implementation?

## KB Synthesis

The implementation uses a **single global granfilade** as the one allocation tree for all node addresses. Independent allocation trees do not occur.

**Single-root enforcement**

[SS-ADDRESS-SPACE] Finding 0021 is explicit: *"The entire granf (global address enfilade) is a single flat tree; the allocation algorithm enforces hierarchical structure by bounding searches to the parent's address range."* Accounts, documents, versions, link orgls, and content I-addresses all live in this one tree.

**How hierarchy is simulated without separate trees**

Rather than separate subtrees per account or document, `findisatoinsertnonmolecule` enforces containment by computing an upper bound (`tumblerincrement(parent, depth-1, 1)`) and restricting `findpreviousisagr` to that range [SS-ADDRESS-ALLOC]. Allocation for documents under account `1.1.0.2` searches only within that account's tumbler prefix — but still inside the same global granfilade.

**Two global enfilades, not more**

[SS-DUAL-ENFILADE] Finding 0012 confirms the system has exactly two global enfilades: `granf` (all content and document structure) and `spanf` (link index). Both are created once at startup via `createenf()` and stored at fixed locations in `enf.enf` [SS-UNIFIED-STORAGE].

**Per-document POOMs are not independent allocation trees**

Each document has its own POOM (V→I mapping enfilade) [SS-POOM-MUTABILITY], but these are stored as orgls *within* the granfilade, not as independent root trees. They store V-to-I mappings for one document; address allocation still runs through the single global granfilade.

**Finding 0077 confirms shared allocation**

[SS-ADDRESS-SPACE] Finding 0077: *"Both [document address allocation and content I-address allocation] query the same granfilade tree but search different subtrees."* There is no per-partition counter or separate tree — all allocation is stateless query-and-increment against the single global granfilade.

**Summary:** One global granfilade, one global spanfilade. The address hierarchy (node → account → document → element) is enforced algorithmically by bounding searches, not by splitting into separate trees.

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## Does udanax-green enforce a single global granfilade root?

**Yes, unconditionally.** The implementation enforces a single global granfilade root at the C language level, with no mechanism to create or reference a second one.

---

### 1. One global variable, declared once

`corediskout.c:21`:
```c
typegranf granf;
typespanf spanf;
```

This is the only definition of `granf` in the entire codebase. It is exported via `xanadu.h:14`:
```c
extern typegranf granf;
```

Every translation unit that uses node addresses imports this single pointer.

---

### 2. Initialized exactly once at startup

`entexit.c:41–46` (`initmagicktricks`, called from `bed.c:95`):
```c
if (initenffile()) {
    initkluge ((typecuc**)&granf, (typecuc**)&spanf);   // restore from disk
} else {
    granf = (typegranf) createenf (GRAN);                // create fresh
    spanf = (typespanf) createenf (SPAN);
}
```

Both branches produce exactly one `granf` for the lifetime of the backend process. There is no subsequent call to `createenf(GRAN)` anywhere else in the codebase.

`initkluge` (`corediskin.c:18–41`) recovers `granf` from a fixed disk location (`GRANFDISKLOCATION`), reading a single serialized tree root. `createenf(GRAN)` creates a fresh empty granfilade. Either way, one tree, one root.

---

### 3. Every allocation and lookup passes the same `granf`

All operations that touch node addresses pass the global `granf` literal — no caller supplies an alternative:

| Operation | Code citation |
|---|---|
| Create new document | `createorglingranf(taskptr, granf, &hint, isaptr)` — `do1.c:240` |
| Create node or account | `createorglingranf(taskptr, granf, &hint, &isa)` — `do1.c:252` |
| Create new version | `createorglingranf(taskptr, granf, &hint, newisaptr)` — `do1.c:277` |
| Create link | `createorglingranf(taskptr, granf, &hint, linkisaptr)` — `do1.c:182, 209` |
| Insert text (allocates ispan address) | `inserttextingranf(taskptr, granf, &hint, textset, &ispanset)` — `do1.c:118` |
| Rearrange / copy / delete | `findorgl(taskptr, granf, docisaptr, &docorgl, ...)` — `do1.c:40, 55, 75, 164` |
| Retrieve | `findorgl(taskptr, granf, &specset->docisa, &docorgl, ...)` — `do2.c:35` |
| V↔I conversion | `findorgl(taskptr, granf, docisaptr, &orglptr, ...)` — `orglinks.c:23` |
| Link end-set operations | `findorgl(taskptr, granf, ...)` — `sporgl.c:44, 77, 152` |

---

### 4. Address allocation is strictly hierarchical within that single tree

`findisatoinsertgr` (`granf2.c:130–156`) dispatches to two sub-routines based on `hintptr->subtype`:

- `findisatoinsertmolecule` (`granf2.c:158`) — for ATOM types (text content, links): allocates an address *under* the document's tumbler, formatted as `docisa.2.atomtype+1`.
- `findisatoinsertnonmolecule` (`granf2.c:203`) — for DOCUMENT/ACCOUNT/NODE types: finds the highest existing key under `hintptr->hintisa` and increments it, producing strictly nested addresses.

The `typehint` for each operation (`do2.c:78–84`, called as `makehint(...)` throughout `do1.c`) is always rooted in either:
- `taskptr->account` (the per-connection account tumbler, e.g. `1.1.0.1`), or
- a document address derived from that account.

All resulting tumbler keys live in a strict hierarchy: `NODE > ACCOUNT > DOCUMENT > ATOM`, all as leaf keys in the one global granfilade.

---

### 5. `createenf(POOM)` does NOT create independent trees

`granf2.c:120`:
```c
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
```

This is called in `createorglgr`, which stores a per-document version orgl as a **value** inside the granfilade, keyed by the document's tumbler. These POOM-type orgls are not address spaces; they are the POOM (Permutation of Ordered Memory) structure for an individual document's content. They are fetched via `fetchorglgr` (`granf2.c:22`), which searches inside `granf` for the key and extracts the stored orgl pointer. They cannot be reached without going through `granf`.

---

### Conclusion

udanax-green enforces a single universal granfilade root (`granf`, `corediskout.c:21`) with no mechanism to create or reference a second one. Every node address — account, document, link, text atom — is allocated as a key within this one tree via `findisatoinsertgr`/`createorglgr`, and every lookup uses `findorgl(taskptr, granf, ...)`. Independent node-allocation trees do not occur in the implementation.
