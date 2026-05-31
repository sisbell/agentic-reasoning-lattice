## Question 2 [evidence]

> Does udanax-green fix a per-document link V-position depth at first link insertion and retain that depth across states where the link subspace is emptied and later repopulated, and is content-subspace depth treated the same or differently?

## KB Synthesis

The KB addresses pieces of this but does not have a single finding that covers the full repopulation cycle. Here is what is directly supportable, and where inference is required.

---

**Link V-position at first insertion**

[SS-LINK-SUBSPACE] (Finding 0052) states that `findnextlinkvsa` hardcodes the first link position at `2.1` by incrementing tumbler coordinates: first to `2.0`, then to `2.1`. Subsequent links are placed at `vspanreach` — the current end of the document's V-extent. This means the starting position is derived from current POOM state, not a fixed document-level counter.

**After emptying the link subspace via DELETEVSPAN**

[SS-THREE-LAYER-MODEL] (Finding 0040) confirms that `DELETEVSPAN(2.x)` removes only the POOM entry; the link orgl in I-space and the spanfilade entries are untouched. If all link POOM entries are removed, the link subspace in the POOM is empty. Since `findnextlinkvsa` uses `vspanreach` for subsequent links, and since an empty link subspace would reset `vspanreach` to the 2.x origin, a new link would again be placed at `2.1`. The KB does not have a direct golden test confirming this repopulation behavior — this is inferred from the `vspanreach` mechanism.

**POOM tree depth (enfilade height) does not reset**

This is the key asymmetry. [SS-ENFILADE-TREE] (Finding 0058) and [INV-ENFILADE-MINIMALITY] are unambiguous: `levelpull` is disabled (returns 0 immediately). Tree height can only increase via `levelpush`. After deleting all link content, [ST-DELETE] (Finding 0058) states:

> `delete_all(doc) ⟹ dom(poom(doc)) = ∅ ∧ enf.height(doc) = enf.height_before(doc)`

The POOM tree retains whatever height it reached when links were present. Repopulating the link subspace inserts into this taller-than-minimal tree structure. The two "empty" states — never-filled (height=1, one zero-width bottom node) versus emptied-after-growth (height H, empty intermediate nodes, no bottom nodes) — are structurally non-equivalent [EC-EMPTY-DOC].

**Content subspace treated the same at the structural level**

[FC-SUBSPACE] (Findings 0054, 0055) confirms the two subspaces are independent shift domains, but at the POOM level they share the same disabled-levelpull invariant. Text subspace POOM height is equally monotonically non-decreasing. The distinction is:

- **V-positions** for text content would restart at `1.1` after emptying the text subspace (same logic as links resetting to `2.1`)
- **I-addresses** for text content are globally monotonically increasing and never reuse [INV-MONOTONIC], [INV-NO-IADDR-REUSE] — deleting text from V-space does not free the I-addresses in the granfilade, so the next INSERT allocates above the previous maximum

This I-address monotonicity has no direct parallel for link V-positions: link V-positions are POOM locations, not granfilade I-addresses, so they can in principle reset when the subspace empties. Links do allocate I-addresses for their orgls [SS-ADDRESS-ALLOC] (Finding 0065), and those I-addresses are also monotonically increasing and never reused.

---

**Summary**

| Property | Link subspace (2.x) | Text subspace (1.x) |
|---|---|---|
| First V-position after emptying | Resets to 2.1 (inferred from `findnextlinkvsa`) | Resets to 1.1 (same logic) |
| POOM tree height after emptying | Retained (levelpull disabled) | Retained (same) |
| I-address counter after emptying | Monotonically continues (link orgl I-addrs) | Monotonically continues |

The KB does not have direct experimental evidence for the repopulation V-position scenario. The enfilade height retention is established fact [SS-ENFILADE-TREE], [INV-ENFILADE-MINIMALITY]. The two subspaces are treated structurally identically by the POOM machinery — no asymmetry is documented.

---

## Code Exploration

I now have all the code I need. Here is the full answer, with source citations.

---

## Does udanax-green fix a per-document link V-position depth at first link insertion, and retain it?

### Short answer

No per-document fixation occurs. The link subspace V-position depth is **globally hardcoded as 2** (two-digit tumblers, e.g., `2.1`, `2.2`, …) in `findnextlinkvsa`. After the link subspace is emptied, the algorithm always restores the same starting position. The content subspace uses the same depth (2) but a different first digit.

---

### 1. How link V-positions are determined: `findnextlinkvsa`

Every call to `docreatelink` (do1.c:195) or `domakelink` (do1.c:169) calls `findnextlinkvsa` to place the link's ISA reference into the document's POOM:

```c
// do1.c:184
&& findnextlinkvsa (taskptr, docisaptr, &linkvsa)
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)
```

The function itself (do2.c:151-167):

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);   // firstlink = 2
    tumblerincrement (&firstlink, 1, 1, &firstlink);   // firstlink = 2.1  (depth-2)

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);   // reach < 2.1 → place at 2.1
    else
        movetumbler (&vspanreach, vsaptr);  // reach ≥ 2.1 → place at vspanreach
    return (TRUE);
}
```

`tumblerincrement(zero, rightshift=0, value=2)` produces `{exp=0, mantissa=[2,0,…]}` — a depth-1 tumbler (one significant digit). The second call adds a second digit, yielding `{exp=0, mantissa=[2,1,0,…]}` — depth-2 (two significant digits; `tumblerlength` = `nstories - exp` = 2 − 0 = 2, tumble.c:259-261).

This `firstlink = 2.1` is built from scratch on every call. **There is no per-document stored value.** The depth-2 structure comes entirely from the hardcoded construction of `2.1`.

---

### 2. Why subsequent links also stay at depth 2

When `insertpm` (orglinks.c:75) places the link into the document's POOM:

```c
// orglinks.c:115
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

For `vsaptr = 2.1` (depth=2): `shift = 1`. The V-width of the link crum is set at depth 1, i.e., one second-digit unit (0.1 in Xanadu notation). The root crum's `cwid.dsas[V]` grows by this amount.

After adding a link at 2.1, `vspanreach = stream + width` stays a depth-2 tumbler (e.g., `2.2`). Each subsequent link also gets a depth-2 position. The depth never grows unless the accumulated second-digit value exceeds what a single `tdigit` (UINT) can hold — not a practical concern.

---

### 3. Behaviour after the link subspace is cleared

`deletevspanpm` (orglinks.c:145-152) removes link crums from the document's POOM:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

After this, the root crum's `cwid.dsas[V]` shrinks to reflect only remaining content. `doretrievedocvspan` reads this root crum (orglinks.c:165-172, which reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the root directly). If all links are deleted and only text remains at 1.x, then `vspanreach` is some value below `2.0`.

The next `findnextlinkvsa` call: `tumblercmp(vspanreach, 2.1) == LESS` → `vsaptr = firstlink = 2.1`.

**The link subspace restarts at 2.1, depth 2, every time.** This looks like retention, but it is not — there is no saved state. It is the same unconditional hardcoded logic running on a document whose V-reach has dropped below 2.1.

---

### 4. Link endpoint V-positions within each link's own orgl

`setlinkvsas` (do2.c:169-183) places from/to/three at fixed positions within the link's own POOM:

```c
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // 1
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);  // 1.1 (depth-2)

tumblerincrement (tovsaptr, 0, 2, tovsaptr);      // 2
tumblerincrement (tovsaptr, 1, 1, tovsaptr);       // 2.1 (depth-2)

tumblerincrement (threevsaptr, 0, 3, threevsaptr); // 3
tumblerincrement (threevsaptr, 1, 1, threevsaptr); // 3.1 (depth-2)
```

These are called unconditionally; all link endpoint slots always live at `1.1`, `2.1`, `3.1` — depth-2, hardcoded per-endpoint, not per-document or per-link.

---

### 5. Content subspace: same depth, different first digit

Text insertion (`doinsert`, do1.c:87) takes the V-address from the caller:

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = inserttextingranf(...) && docopy (taskptr, docisaptr, vsaptr, ...);
```

The caller passes `Address(1, 1)` → V=1.1 (depth-2). For the `appendpm` path (orglinks.c:17-27), `findvsatoappend` also produces 1.1:

```c
// orglinks.c:42-43 (empty-doc branch)
tumblerincrement (vsaptr, 0, 1, vsaptr);  // 1
tumblerincrement (vsaptr, 1, 1, vsaptr);  // 1.1 (depth-2)
```

The text subspace also uses depth-2 positions. The structural distinction is purely the first digit:

| Subspace | First digit | Range | Example |
|---|---|---|---|
| Text content | 1 | [1.1, 2.0) | 1.1, 1.2, … |
| Link references in doc | 2 | [2.1, …) | 2.1, 2.2, … |
| Link endpoints (within link orgl) | 1, 2, 3 | fixed | 1.1, 2.1, 3.1 |

The threshold `linkspacevstart = 2` (orglinks.c:37) defines where text stops and links begin in the document's POOM; `findvsatoappend` never places text at or above V=2.

---

### Summary

| Question | Answer | Key code |
|---|---|---|
| Is depth fixed per-document at first link insertion? | No — no per-document storage; the constant `2.1` is rebuilt from scratch each call | do2.c:156-158 |
| Is it retained after the link subspace is emptied? | The algorithm always returns to `2.1` after clearing, not because state is retained but because `firstlink = 2.1` is unconditional | do2.c:162-165 |
| Content subspace treated same or differently? | Same depth (2); different first digit (1 vs 2); text depth is caller-set, link depth is system-set | do2.c:169-183; orglinks.c:42-43 |

The link endpoint slots within each link's own orgl (`1.1`, `2.1`, `3.1`) are also fixed-depth-2 constants, identical across all links in all documents.
