## Question 2 [evidence]

> In udanax-green, do content positions (subspace `s_C`) and link positions (subspace `s_L`) ever have different tumbler depths within one document, or are both subspaces always at the same depth?

## KB Synthesis

Both subspaces share the same V-address tumbler depth, but their internal POOM displacement representations diverge in exponent — and that divergence is load-bearing.

## V-Address Depth: Same

Every concrete example in the KB places text and link V-addresses at the same 2-digit depth:

- Text subspace: `1.1`, `1.2`, `1.3` … (mantissa [1, n], exp=0)
- Link subspace: `2.1`, `2.2` … (mantissa [2, n], exp=0)
- Type-endpoint subspace: `3.1` … (mantissa [3, n], exp=0)

[SS-TWO-BLADE-KNIFE] (Finding 0054) confirms this uniformity — `findaddressofsecondcutforinsert` computes a second blade at `(N+1).1` for any subspace N, which only makes sense if all subspaces are at the same digit depth. [SS-POOM-BOTTOM-CRUM] (Finding 0076) states explicitly that "V-addresses use 2 tumbler digits (e.g., `0.5`, `1.1`)".

## POOM Displacement Exponents: Different

[FC-SUBSPACE] (Finding 0055) reveals a critical internal asymmetry. In the POOM tree, the two subspaces' relative displacement fields (`cdsp.dsas[V]`) use **different exponents**:

> "Text crums within the deletion's subspace have displacements at exp=-1 (same level as the width), while link crums at exp=0 are unaffected."

Concrete example from Finding 0055:
```
Text crum: V-displacement 0.4  (exp = -1)
Link crum: V-displacement 2.1  (exp =  0)
Deletion width: 0.3            (exp = -1)

strongsub(0.4, 0.3) → exponents match → subtraction proceeds → 0.1
strongsub(2.1, 0.3) → exp(-1) < exp(0) → strongsub returns 2.1 unchanged
```

This exponent difference is not a deliberate depth distinction — it is an **arithmetic consequence** of how relative displacements are computed in the POOM tree (absolute positions minus parent grasp). Text positions accumulate at the sub-unit scale (exp=-1); link positions sit at a higher scale (exp=0). As [INT-DELETE-SUBSPACE-ASYMMETRY] (Finding 0055) notes, DELETE's subspace isolation is an **incidental arithmetic guard** (exponent mismatch in `strongsub`), not a structural guard like INSERT's two-blade knife.

## Summary

| Level | Text (1.x) | Link (2.x) | Same? |
|-------|-----------|-----------|-------|
| Absolute V-address digit count | 2 | 2 | **Yes** |
| POOM displacement exponent | exp = -1 | exp = 0 | **No** |

The two subspaces are at identical tumbler depth in the user-visible address space. Within the POOM tree's internal displacement representation they operate at different scales — a distinction the implementation relies on for DELETE's subspace isolation, but one that is accidental rather than specified. [EC-DEEPLY-ORPHANED-LINK] (Finding 0055) notes this protection is fragile: if `strongsub` were extended to handle cross-exponent arithmetic, DELETE would lose subspace isolation while INSERT (which uses the deliberate two-blade knife) would remain safe.

---

## Code Exploration

I now have all the information needed for a comprehensive answer.

---

## Answer: s_C and s_L Always Have the Same Tumbler Depth

**Short answer:** Both subspaces are always assigned as **2-story (depth-2) tumblers** within one document. The subspaces are distinguished only by the value of the first mantissa digit, never by depth.

---

### What "Depth" Means in This Code

There is no `depth` field in the tumbler struct. Depth is computed from two functions:

**`nstories`** [`tumble.c:249-257`]:
```c
INT nstories(tumbler *tumblerptr)
{
  INT i;
    for (i = NPLACES; i > 0 && tumblerptr->mantissa[--i] == 0;);
    return (i + 1);
}
```
Scans from the end of `mantissa[NPLACES=16]` to find the last non-zero slot; returns `index + 1`. A tumbler `{exp=0, mantissa=[1,5,0,...]}` = `1.5` has `nstories=2`.

**`tumblerlength`** [`tumble.c:259-262`]:
```c
INT tumblerlength(tumbler *tumblerptr)
{
    return (nstories (tumblerptr) - tumblerptr->exp);
}
```
Adjusts for the exponent field. When `exp=0`, `tumblerlength == nstories`. When `exp=-1` (fractional tumblers like `0.k`), `tumblerlength = nstories + 1`.

---

### How s_C Positions Are Assigned

`findvsatoappend` [`orglinks.c:29-49`] determines where to insert text content:

```c
int findvsatoappend(typecorecrum *ptr, tumbler *vsaptr)
{
  tumbler linkspacevstart;
    tumblerclear(&linkspacevstart);
    tumblerincrement(&linkspacevstart, 0, 2, &linkspacevstart);  // = {exp=0, mantissa=[2,...]} = "2"
    prologuend(ptr, &offset, &grasp, &reach);
    if (
       iszerolock((tumbler*)&ptr->cwid, widsize(POOM))
    || (tumblercmp(&grasp.dsas[V], &linkspacevstart) != LESS)) {
        tumblerincrement(vsaptr, 0, 1, vsaptr);  // vsaptr = {exp=0, mantissa=[1,...]}
        tumblerincrement(vsaptr, 1, 1, vsaptr);  // vsaptr = {exp=0, mantissa=[1,1,...]} = "1.1"
    } else if (tumblercmp(&reach.dsas[V], &linkspacevstart) == LESS) {
        movetumbler(&reach.dsas[V], vsaptr);     // next pos after existing text, always 1.n form
    } else {
        findnextaddressinvspace(ptr, &grasp, &linkspacevstart, vsaptr); // navigates before V=2
    }
}
```

First insert → `vsaptr = 1.1` = `{exp=0, mantissa=[1,1,0,...]}`. Subsequent inserts extend `1.n` where n increments. All are **depth 2** (`nstories=2`, `tumblerlength=2`).

The V-crum width is then computed in `insertpm` [`orglinks.c:115-117`]:
```c
shift = tumblerlength(vsaptr) - 1;    // = 2-1 = 1
inc = tumblerintdiff(&lwidth, &zero);
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);
```
Since `aptr` is zero and `rightshift=1`: `crumwidth.dsas[V] = {exp=-1, mantissa=[inc,...]}` = `0.inc`. This is 1-story (`nstories=1`), but `tumblerlength = 1-(-1) = 2` — also depth 2.

---

### How s_L Positions Are Assigned

`findnextlinkvsa` [`do2.c:151-167`] places each link crum in the owning document's V-space:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
    tumblerclear(&firstlink);
    tumblerincrement(&firstlink, 0, 2, &firstlink);  // {exp=0, mantissa=[2,...]} = "2"
    tumblerincrement(&firstlink, 1, 1, &firstlink);  // {exp=0, mantissa=[2,1,...]} = "2.1"

    (void) doretrievedocvspan(taskptr, docisaptr, &vspan);
    tumbleradd(&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp(&vspanreach, &firstlink) == LESS)
        movetumbler(&firstlink, vsaptr);  // first link goes at 2.1
    else
        movetumbler(&vspanreach, vsaptr); // subsequent links extend 2.n
    return (TRUE);
}
```

First link → `vsaptr = 2.1` = `{exp=0, mantissa=[2,1,0,...]}`. Subsequent links go at `2.2`, `2.3`, etc. All are **depth 2** (`nstories=2`, `tumblerlength=2`). The V-width is computed identically via `insertpm` — also depth 2.

`setlinkvsas` [`do2.c:169-183`] sets the endset positions _within_ the link's own POOM:
```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear(fromvsaptr);
    tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);  // 1
    tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);  // 1.1  ← depth 2
    tumblerclear(tovsaptr);
    tumblerincrement(tovsaptr, 0, 2, tovsaptr);      // 2
    tumblerincrement(tovsaptr, 1, 1, tovsaptr);      // 2.1  ← depth 2
    if (threevsaptr) {
        tumblerincrement(threevsaptr, 0, 3, threevsaptr);  // 3
        tumblerincrement(threevsaptr, 1, 1, threevsaptr);  // 3.1 ← depth 2
    }
    return (TRUE);
}
```
All three endsets within the link's own V-space are also depth-2 tumblers.

---

### Side-by-Side Comparison

| Subspace | POOM V-address | `nstories` | `exp` | `tumblerlength` |
|----------|---------------|------------|-------|-----------------|
| s_C (text) | `{exp=0, mantissa=[1,n,...]}` = `1.n` | 2 | 0 | 2 |
| s_L (link) | `{exp=0, mantissa=[2,n,...]}` = `2.n` | 2 | 0 | 2 |
| Both (width) | `{exp=-1, mantissa=[k,...]}` = `0.k` | 1 | -1 | 2 |

**The depths are always equal — 2 for both position and width tumblers.**

---

### The Separator and Why It Isn't a Depth Boundary

The link subspace starts at V=`2` (not at a deeper address). This boundary is defined in `findvsatoappend` [`orglinks.c:37`]:
```c
tumblerincrement(&linkspacevstart, 0, 2, &linkspacevstart);  // linkspacevstart = {mantissa=[2,...]} = "2"
```
Text lives at V < 2, links at V ≥ 2. This is a **value boundary** (first-digit 1 vs first-digit 2), not a depth boundary.

The `is1story` check in `retrievevspansetpm` [`orglinks.c:184`]:
```c
if (is1story(&ccptr->cwid.dsas[V])) { /* if it is just text return that */
```
is testing whether the **root crum's total V-width** has only one non-zero digit. For text-only documents, cwid = `{exp=-1, mantissa=[n,...]}` = `0.n` (1-story). For mixed documents, cwid = `{exp=0, mantissa=[n,m,...]}` = `n.m` (2-story), where `mantissa[0]=n` encodes text extent and `mantissa[1]=m` encodes link count. This is a diagnostic on the combined cwid — not evidence that the two subspaces use different depths.

---

### Observed Golden Test Confirmation

`golden/content/insert_text.json` (text-only) — returned span:
```json
{"start": "1.1", "width": "0.13"}
```
→ text at V=`1.1` (depth 2), width `0.13` (2 digits).

`golden/documents/retrieve_vspan_with_links.json` (text + link):
```json
{"start": "0", "width": "0.1"},   // link span
{"start": "1", "width": "1"}      // text span
```
The peculiar `start: "0"` is an artifact of `retrievevspansetpm`'s hack: it zeroes `mantissa[1]` of the cwid and calls `tumblerjustify` rather than reading actual V-addresses. The underlying POOM crums for both subspaces are still at `1.n` (text) and `2.n` (link) — both depth-2.

`golden/links/create_link.json` — content spans used to specify link endpoints:
```json
{"start": "1.22", "width": "0.9"}   // source in s_C
{"start": "1.1",  "width": "0.23"}  // target in s_C
```
All explicit content addresses seen by the client are depth-2 (`1.n`).

---

### Conclusion

**s_C and s_L positions are always the same tumbler depth within one document.** Both use depth-2 (`tumblerlength=2`) V-address tumblers, of the form `1.n` for content and `2.n` for links. The separation between subspaces is encoded entirely in the value of the first mantissa digit — `1` for content, `2` for links — with no change in depth structure. There is no code path in `findvsatoappend`, `findnextlinkvsa`, `setlinkvsas`, or `insertpm` that would ever produce s_C and s_L crums at different depths.
