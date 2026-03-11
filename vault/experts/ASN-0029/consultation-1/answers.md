# Revision Consultation — ASN-0029

**Review:** review-1.md
**Date:** 2026-03-11 08:58

## Summary

8 REVISE items analyzed: 6 internal, 2 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 3: D10 "standard operations" is undefined

**Category:** NELSON
**Reason:** The qualifier "standard operations" reflects a design choice about whether publication permanence is absolute or admits exceptions. Nelson's intent regarding withdrawal conditions determines whether D10 should be unconditional or scoped.

**Nelson question:** Is the permanence of publication absolute — once published, always published with no mechanism for reversal — or did you intend withdrawal to be possible under specific conditions, and if so, what distinguishes a withdrawal from a standard operation?

**Nelson's Answer:**

# Publication Permanence: Difficult, Not Absolute

No, permanence is not absolute. I designed withdrawal to be **possible but deliberately difficult**, because the difficulty itself serves a purpose. Let me explain the architecture of this decision.

## The Default: Stay Published

The starting principle is clear:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The phrase "except by lengthy due process" is doing critical work. This is not "never" — it is "not easily." The distinction matters enormously.

## Why Withdrawal Must Be Hard

The reason is structural, not philosophical. When you publish, other people create links to your content — links that **they own**, at **their addresses**. Those links are their property. If you withdraw your document, you break their property.

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

This is the key insight: your document is not just yours anymore once published. It has become part of a web of dependencies. Others have built on it, linked to it, quoted from it. Their work depends on yours remaining accessible.

## The Mechanisms

I specified several distinct mechanisms, each for different circumstances:

### 1. Supersession (the normal path)

The preferred approach is not withdrawal but **supersession** — publish a new version and declare the old one superseded. The old version remains accessible (preserving others' links), but readers are directed to the new version through a supersession link.

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version." [LM 4/52-4/53]

This is how corrections work. You don't erase your mistake — you publish the correction and let the system guide readers to it.

### 2. Lengthy Due Process (actual withdrawal)

The publication contract provides for withdrawal, but with deliberate friction. The contractual terms require one year's notice and a fee. NEED_RAW: [5/19-5/21] for the exact withdrawal provisions in the publication contract.

### 3. Peremptory Challenge (for anonymous defamation)

For anonymous publication ("John Doe publication"), I specified a specific removal mechanism:

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge." [LM 2/60]

This is the one case where someone other than the owner can trigger removal — because the owner (being anonymous) "won't hang around to defend their acts." For identified publishers, peremptory challenge does not apply; removal requires negotiation or court order.

### 4. Privashing (the escape hatch)

For authors who want universal accessibility but also want the right to withdraw freely, I provided an explicit alternative to formal publication:

> "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution." [LM 2/48]

Privashing gives you the reach of publication without the permanence obligation. The tradeoff: no royalties, and anyone who linked to your privashed document has no recourse if you pull it.

## What Distinguishes Withdrawal from Standard Operations

Standard operations — INSERT, DELETE, REARRANGE, COPY — modify a document's V-space arrangement. They change what the document looks like now, but nothing is destroyed in I-space. Previous versions remain accessible. These are routine and unrestricted (for the owner).

Withdrawal is categorically different. It is the removal of a **published** document from public accessibility. This is not an editing operation — it is a **contractual** operation that affects other participants in the network. That is why it requires due process rather than a command.

The distinction maps to the three-structure design:

> "a rational conceptual structure, plus a technical structure which makes it possible, and a contractual structure which makes it possible for people to use it confidently." [LM 4/4]

Editing is technical. Withdrawal is contractual.

## The Deeper Reason

I had Fahrenheit 451 in mind, and the Ministry of Truth:

> "A reference article, say, in an encyclopedia can be changed simply by storing another one in its place—and poof! history is changed." [LM 3/21]

If withdrawal were easy, the system would enable exactly the kind of historical revision I designed it to prevent. Making withdrawal difficult is not a bug — it is a deliberate defense against the erasure of the record. The friction is the feature.

But making withdrawal **impossible** would be tyrannical in the other direction — forcing people to stand behind statements forever, with no recourse. So the system provides mechanisms, but makes them proportional to the social consequences: supersession is easy, full withdrawal is hard, and the intermediate option (privashing) lets cautious authors avoid the permanence obligation entirely.

### Issue 8: No concrete example verifying postconditions

**Category:** GREGORY
**Reason:** Constructing a worked example for D12/D13 requires confidence in how version addresses are actually allocated — particularly whether the sub-document tumbler field increments by 1 and what the concrete address looks like when versioning across accounts. Gregory's implementation knowledge anchors the example in real allocation behavior.

**Gregory question:** When CREATENEWVERSION is called on an own-account document (e.g., `1.0.1.0.3`), what concrete tumbler address does the version receive — is it `1.0.1.0.3.1` for the first version, `1.0.1.0.3.2` for the second, and does the sub-document field always start at 1?

**Gregory's Answer:**

## KB Synthesis

Yes — for an owned document, the version address is always a child of the source document's address, starting at `.1` for the first version and incrementing monotonically.

**Address structure:**

For source document `1.0.1.0.3`:
- First version → `1.0.1.0.3.1`
- Second version → `1.0.1.0.3.2`
- Third version → `1.0.1.0.3.3`
- Version of a version → `1.0.1.0.3.1.1` (grandchild)

**The allocation mechanism** [SS-ADDRESS-ALLOC, SS-VERSION-ADDRESS Finding 0068]:

`docreatenewversion` calls `findisatoinsertnonmolecule` with `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)`, which sets `depth=1`. The algorithm:

1. Computes `upperbound = tumblerincrement(source_doc, depth-1=0, 1)` → the next sibling of the source doc (`1.0.1.0.4` in your example)
2. Calls `findpreviousisagr` to find the highest existing address below that upper bound
3. Applies a containment check — verifies the found address is actually under the source document
4. If no child exists: allocates first child as `source_doc.1` → `1.0.1.0.3.1`
5. If child exists: truncates to the child's length and increments → `1.0.1.0.3.2`, etc.

The sub-document (version child) field always starts at `1`, not `0`. There is no `.0.` boundary crossing between the document and its version addresses — `depth=1` means a single component is appended with no zero separator. Compare this to document-under-account allocation where `depth=2` produces the `.0.` separator (e.g., `1.0.1` → `1.0.1.0.1`) [SS-ADDRESS-SPACE Finding 0021].

**Unlimited depth** [SS-VERSION-ADDRESS Finding 0068]:

The nesting is unbounded:
```
1.0.1.0.3              (doc)
├── 1.0.1.0.3.1        (version 1)
│   └── 1.0.1.0.3.1.1  (version of version 1)
└── 1.0.1.0.3.2        (version 2)
```

**Ownership matters** [SS-VERSION-ADDRESS Finding 0068]:

This child-of-source allocation only applies when `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)` is true (the requesting user owns the document). If a different user versions `1.0.1.0.3`, their version is allocated under their own account instead — the address encodes ownership, not universal version lineage.

**Monotonicity guarantee** [INV-MONOTONIC Finding 0068]:

Version addresses within a document's child namespace are strictly monotonically increasing. Deleting a version does not free its address — the granfilade retains all allocated addresses permanently, so subsequent versions always allocate higher numbers, never reusing a prior version's address.

---

## Code Exploration

---

## Answer: CREATENEWVERSION Address Allocation for Own-Account Documents

### Short answer

For a document at `1.0.1.0.3`:
- First version → `1.0.1.0.3.1`
- Second version → `1.0.1.0.3.2`
- Nth version → `1.0.1.0.3.N`

The appended component always starts at **1**, never 0.

---

### Code trace

**Step 1 — entry point: `fns.c:289-300`**

```c
void createnewversion(typetask *taskptr)
{
  typeisa originaldocisa, newdocisa;
  ...
  if (   getcreatenewversion (taskptr, &originaldocisa)
      && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
      putcreatenewversion (taskptr, &newdocisa);
```

Note: `isaptr` and `wheretoputit` are **both** `originaldocisa`.

---

**Step 2 — own-account branch: `do1.c:260-299`**

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    /* ECH 7-13 introduced test for ownership to do right thing ... */
    if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
        makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);  // own-account path
    } else {
        makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  // foreign-doc path
    }
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) return FALSE;
    ...
}
```

For an own-account document: `tumbleraccounteq` and `isthisusersdocument` are both true → **`makehint(DOCUMENT, DOCUMENT, ...)`** is called with `hintisa = 1.0.1.0.3`.

---

**Step 3 — `makehint`: `do2.c:78-84`**

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;   // DOCUMENT
    hintptr->subtype = typebelow;     // DOCUMENT
    hintptr->atomtype = typeofatom;   // 0
    movetumbler (isaptr, &hintptr->hintisa);  // hintisa = 1.0.1.0.3
}
```

---

**Step 4 — routing: `granf2.c:130-156`**

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        findisatoinsertmolecule(...);
    } else {
        findisatoinsertnonmolecule(...);  // DOCUMENT is not ATOM → goes here
    }
    tumblerjustify(isaptr);
    return TRUE;
}
```

---

**Step 5 — the address arithmetic: `granf2.c:203-242`**

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
    // DOCUMENT == DOCUMENT → depth = 1

    hintlength = tumblerlength(&hintptr->hintisa);
    // hintisa = 1.0.1.0.3 → hintlength = 5

    tumblerincrement(&hintptr->hintisa, depth-1, 1, &upperbound);
    // depth-1 = 0 → upperbound = 1.0.1.0.4

    findpreviousisagr(fullcrumptr, &upperbound, &lowerbound);
    // finds highest ISA below 1.0.1.0.4

    // Check if lowerbound is under hintisa
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        // Nothing under this hint yet — first child
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
        // depth=1 → appends .1 → 1.0.1.0.3.1
    } else {
        tumblertruncate(&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
        // if lowerbound has 5 components (= hintlength): increment at depth=1 → appends .1
        // if lowerbound has 6 components (>hintlength): increment at 0 → increments last digit
    }
}
```

Walking through each case for `hintisa = 1.0.1.0.3`:

| State of granfilade | `lowerbound` found | computation | result |
|---|---|---|---|
| No versions yet | `1.0.1.0.3` (5 digits, = hintisa) | `tumblertruncate(1.0.1.0.3, 6)` → `1.0.1.0.3`; `tumblerlength==5==hintlength` → `tumblerincrement(_, depth=1, 1)` → append `.1` | **`1.0.1.0.3.1`** |
| Version `.1` exists | `1.0.1.0.3.1` (6 digits) | `tumblertruncate(1.0.1.0.3.1, 6)` → `1.0.1.0.3.1`; `tumblerlength==6≠hintlength` → `tumblerincrement(_, 0, 1)` → increment last digit | **`1.0.1.0.3.2`** |
| Versions `.1` and `.2` exist | `1.0.1.0.3.2` | same as above, last digit → **`1.0.1.0.3.3`** |

The `tumblerincrement` at `depth=1, bint=1` (`tumble.c:599-623`) finds the last non-zero mantissa index and writes `bint=1` at `idx+rightshift=idx+1` — this is what appends the new `.1` component.

---

### Confirmed by golden tests

The golden file `golden/versions/version_address_allocation.json` records the actual backend output:

```json
{ "op": "create_document", "label": "doc1",    "result": "1.1.0.1.0.1"   },
{ "op": "create_version",  "from": "doc1",     "result": "1.1.0.1.0.1.1" },  // first version
{ "op": "create_version",  "from": "doc1",     "result": "1.1.0.1.0.1.2" },  // second version
{ "op": "create_version",  "from": "doc2",     "result": "1.1.0.1.0.2.1" },  // first version of other doc
{ "op": "create_version",  "from": "version1", "result": "1.1.0.1.0.1.1.1"}  // versioning a version
```

And `golden/versions/multiple_versions_same_source.json` confirms:

```json
{ "op": "create_version", "from": "source", "result": "1.1.0.1.0.1.1" },
{ "op": "create_version", "from": "source", "result": "1.1.0.1.0.1.2" }
```

---

### Summary

| Question | Answer |
|---|---|
| Address of first version of `1.0.1.0.3`? | `1.0.1.0.3.1` |
| Address of second version? | `1.0.1.0.3.2` |
| Address of Nth version? | `1.0.1.0.3.N` |
| Does the sub-document component start at 1? | **Yes**, always. `tumblerincrement(hintisa, depth=1, bint=1)` writes 1 as the new last component — never 0. |
| Are versions siblings of each other (not nested)? | Yes — all versions of `1.0.1.0.3` are at `1.0.1.0.3.K` for K=1,2,3... They are siblings at depth 6. |
| Can a version itself be versioned? | Yes, same code path. `1.0.1.0.3.1` → `1.0.1.0.3.1.1`, `1.0.1.0.3.1.2`, etc. |

The key mechanism is `depth = 1` (from `supertype == subtype == DOCUMENT`, `granf2.c:209`) and the monotonically-incrementing last component under the document's own subtree. The first-ever child always receives the value `1` because `tumblerincrement` writes `bint=1` at one position right of the document's last digit (`tumble.c:621`).
