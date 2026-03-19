# Revision Consultation — ASN-0029

**Review:** review-6.md
**Date:** 2026-03-11 12:19

## Summary

3 REVISE items analyzed: 2 internal, 1 consulted (0 nelson, 1 gregory)

## Consultation Results

### Issue 1: D7 — `home(a) ∈ Σ.D` not established

**Category:** GREGORY
**Reason:** The missing link is whether INSERT on document `d` allocates I-addresses under `d`'s tumbler prefix. This is an I-space allocation discipline question answerable from the udanax-green implementation.

**Gregory question:** When INSERT allocates fresh I-addresses for document `d`, are those addresses always allocated under `d`'s tumbler prefix (i.e., `d ≼ fresh`), or can they fall elsewhere in the I-space?

**Gregory's Answer:**

## KB Synthesis

Fresh I-addresses for text content are **not** allocated under `d`'s own tumbler prefix. The allocation is document-scoped but falls in a separate address namespace — the permascroll — not under `d`'s orgl address.

## What the allocation mechanism does

From [SS-ADDRESS-SPACE] Finding 0061: allocation is stateless query-and-increment — `findpreviousisagr` finds the current maximum I-address within a bounded subrange, then increments by 1. No session-local counter, no global counter.

From [SS-ADDRESS-SPACE] Finding 0065 and [SS-ADDRESS-SPACE] Finding 0077: the upper bound is derived from `d`'s ISA via `tumblerincrement(&hintisa, depth, atomtype+1, &upperbound)`. This scopes the search to content allocated **for** document `d`, but not necessarily **under** `d`.

## Two separate address namespaces

The granfilade contains both document/orgl addresses and permascroll content addresses in distinct tumbler ranges [SS-ADDRESS-SPACE] Finding 0077:

- Document addresses (orgls, versions, link orgls): under `d`'s own prefix, e.g. `1.1.0.1.0.1`, `1.1.0.1.0.1.1` (version), `1.1.0.1.0.1.0.2.1` (link)  
- Content I-addresses (permascroll atoms): in a separate range, e.g. `2.1.0.1.0.1.3.1` through `2.1.0.1.0.1.3.10` for ten inserts into document `d`

[SS-ADDRESS-SPACE] Finding 0033 shows empirically: a document at `1.1.0.1.0.1` has text I-addresses allocated as `2.1.0.1.0.1.3.1`, `2.1.0.1.0.1.3.2`, etc. The `2.1` node prefix is the permascroll node — distinct from the document's `1.1` orgl-store prefix.

From [SS-CONTENT-IDENTITY] Finding 0009: "Permascroll I-addresses (e.g., `2.1.0.5.0.123`) dereference to character bytes in the global immutable permascroll" — confirming this is a separate node.

## The relationship that does hold

`d ≼ fresh` in the strict prefix sense is **false**: document `d = 1.1.0.1.0.1` does not prefix content address `2.1.0.1.0.1.3.1`.

What holds instead: `d`'s account and document components are **embedded** in the content address as middle segments under the permascroll node. The allocation is bounded to content "belonging to" `d` — same account/doc components — but lives under a different top-level node.

[SS-ADDRESS-SPACE] Finding 0077 summarizes this explicitly: "allocation is a family of independent functions partitioned by tumbler range: `next_doc_addr(granf, parent) = max_child(granf, parent) + 1` and `next_content_addr(granf, doc) = max_content(granf, doc) + 1`. Both query the same granfilade tree but search **different subtrees**."

---

## Code Exploration

---

## Answer

**Yes — fresh I-addresses are always allocated under `d`'s tumbler prefix.** The guarantee is structural, baked into `findisatoinsertmolecule`, and depends on three interlocking mechanisms. Here is the full trace.

---

### Call chain

```
insert (fns.c:84)
  → doinsert (do1.c:87)
      → makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)  [do1.c:117]
      → inserttextingranf (granf1.c:44)
          → inserttextgr (granf2.c:83)
              → findisatoinsertgr (granf2.c:130)
                  → findisatoinsertmolecule (granf2.c:158)
```

---

### Step 1 — `makehint` stamps `d` into the hint

`do2.c:78-84`:
```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;   // DOCUMENT = 3
    hintptr->subtype   = typebelow;   // ATOM     = 4
    hintptr->atomtype  = typeofatom;  // TEXTATOM = 1
    movetumbler(isaptr, &hintptr->hintisa);   // hintisa = docisa
}
```

Called as `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` at `do1.c:117`. The document's tumbler address is copied verbatim into `hint.hintisa`.

---

### Step 2 — guard: `d` must exist before any address is minted

`findisatoinsertgr` at `granf2.c:130-156`:
```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr(fullcrumptr, &hintptr->hintisa)) {
        fprintf(stderr, "nothing at hintisa for atom\n");
        return (FALSE);               // <-- hard stop
    }
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);
}
tumblerjustify(isaptr);
return (TRUE);
```

If `d` itself is not present in the granfilade, the function returns `FALSE` immediately. No I-address is allocated at all.

---

### Step 3 — computing the address in `findisatoinsertmolecule`

`granf2.c:158-181`:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typeisa upperbound, lowerbound;

    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    //  rightshift=2, bint=TEXTATOM+1=2
    //  → upperbound = docisa.0.0.2  (two zero levels appended, then +2)

    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    //  lowerbound = last ISA in granfilade that is < docisa.0.0.2

    if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {
        //  CASE 1: lowerbound is docisa itself (no text allocated yet)
        tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);  // → docisa.0.0.1
        tumblerincrement(isaptr, 1, 1, isaptr);                        // → docisa.0.0.1.0.1
    } else if (hintptr->atomtype == TEXTATOM) {
        //  CASE 2: lowerbound is a previous text atom under docisa
        tumblerincrement(&lowerbound, 0, 1, isaptr);                   // → lowerbound + 1
    }
}
```

#### How `tumblerincrement` works (`tumble.c:599-622`)

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    //  idx = position of last non-zero digit

    cptr->mantissa[idx + rightshift] += bint;
    //  places bint exactly rightshift positions AFTER the last digit
    tumblerjustify(cptr);
}
```

So `tumblerincrement(docisa, 2, 2, &upperbound)` with docisa's last non-zero at index `n` sets `mantissa[n+2] += 2`. In tumbler notation: **`docisa.0.0.2`** — a proper sub-address of docisa.

---

### Step 4 — why `lowerbound` is always inside docisa's subtree

`findpreviousisagr` (`granf2.c:256-278`) walks the granfilade tree, accumulating offsets of left siblings, to find the last leaf-entry whose start address is ≤ `upperbound`. At the bottom level, `findlastisaincbcgr` (`granf2.c:280-284`) adjusts for text nodes by adding `textlength − 1` to the leaf's base address.

The invariant: because `isaexistsgr` (Step 2) confirmed `d` exists in the granfilade at exactly `docisa`, `findpreviousisagr` with `upperbound = docisa.0.0.2` will return **at minimum** `docisa` itself. It cannot return anything less than `docisa` because `docisa` is already in the tree and is closer to `upperbound` than anything before it.

Therefore `lowerbound ∈ [docisa, docisa.0.0.2)`. That half-open interval is entirely within docisa's tumbler subtree.

---

### Step 5 — both arithmetic cases stay inside the subtree

| Situation | `tumblerlength` check | Arithmetic | Result |
|---|---|---|---|
| First text insert ever | `len(docisa) == len(lowerbound)` → lowerbound IS docisa | `docisa.0.0.1`, then `.0.1` | `docisa.0.0.1.0.1` ✓ |
| Subsequent insert | lengths differ → lowerbound is a sub-address of docisa | `lowerbound + 1` at depth 0 | still under docisa ✓ |

Both results are unambiguously prefixed by docisa.

---

### Step 6 — sequential characters within one INSERT

After the starting ISA `lsa` is fixed, `inserttextgr` at `granf2.c:100` advances it for each text segment:

```c
tumblerincrement(&lsa, 0, textset->length, &lsa);
//  rightshift=0: adds length to lsa's last digit
//  stays in the same leaf-sequence under docisa
```

Each character in the inserted text gets address `lsa + k` (depth-0 increment) for `k = 0, 1, ..., total_length − 1`. All of these share the `docisa.0.0.X.0.*` prefix.

---

### Summary

INSERT allocates fresh I-addresses through this chain:

1. **`makehint`** (`do1.c:117`) stamps `docisa` into the hint.
2. **`isaexistsgr`** (`granf2.c:136`) guarantees `d` is in the granfilade before any address is produced.
3. **`findisatoinsertmolecule`** (`granf2.c:158`) bounds its search to `[docisa, docisa.0.0.2)` — the latter being the strict delimiter for TEXTATOM space under `d`.
4. The `lowerbound` returned by `findpreviousisagr` is necessarily in that interval (docisa anchors the floor), so both arithmetic paths produce an address that starts with `docisa` as a prefix.
5. Subsequent character addresses advance by depth-0 increments (`tumblerincrement(lsa, 0, length, lsa)`) which never exit the leaf-sequence.

**Fresh I-addresses are always of the form `docisa.0.0.X.0.Y…` — they fall strictly under `d`'s tumbler prefix, never elsewhere in I-space.**
