## Question 1 [evidence]

> In udanax-green, do region-transposition / arrangement-permutation operations operate only on the text subspace, or are they invoked on link or other depth-2 subspaces — and if the latter, how does the implementation handle sparse / tombstoned V-position ranges?

## KB Synthesis

REARRANGE is **not restricted to the text subspace**. The implementation is subspace-blind, and the KB contains direct evidence of cross-subspace invocation and its consequences.

---

## Subspace Handling

`rearrangend()` in `edit.c:78-160` applies a pure tumbler displacement to every POOM crum whose V-position falls in the affected regions. The offset computation in `makeoffsetsfor3or4cuts()` derives displacements from cut-point geometry alone — no digit-0 (subspace) inspection occurs. `sortknives()` normalizes the cut sequence to ascending order but does not validate subspace membership [PRE-REARRANGE, Finding 0056].

Concretely, if cuts span the boundary between subspace 1.x and 2.x, content in section 1 is displaced by `diff[1] = cut2 - cut1`, which can carry a 1.x V-position into the 2.x range [EC-REARRANGE-CROSS-SUBSPACE]:

```
Pivot [1.1, 1.4, 2.5]:
  diff[1] = 2.5 - 1.4 = 1.1
  Content at V:1.1–1.3 lands at V:2.2–2.4 (link subspace)
```

`retrieve_contents` at 2.x then returns text bytes — the content discipline (`INV-SUBSPACE-CONVENTION`) is violated. The backend returns no error [EC-REARRANGE-CROSS-SUBSPACE, Finding 0051].

This contrasts with INSERT and DELETE. INSERT uses a deliberate two-blade knife where `blade[1]` is computed as `(N+1).1` — the next subspace boundary — structurally preventing shifts from crossing subspace boundaries [FC-SUBSPACE, SS-TWO-BLADE-KNIFE, Finding 0054]. DELETE achieves cross-subspace safety accidentally via `strongsub`'s exponent guard [FC-SUBSPACE, Finding 0055]. REARRANGE has **neither mechanism** [INT-DELETE-SUBSPACE-ASYMMETRY].

---

## Sparse / Tombstoned Ranges

There are no tombstones. DELETE frees bottom crums via `disown` + `subtreefree` [ST-DELETE, Finding 0064]. A deleted V-position range has **no POOM entries** — it is genuinely absent, not marked absent.

REARRANGE's per-crum iteration therefore handles sparse ranges implicitly: `rearrangecutsectionnd` classifies each existing crum into a section (0–4) and applies `tumbleradd` [ST-REARRANGE, Finding 0056]. A gap in V-space simply produces no crums to classify — the loop body is never executed for that range. This is confirmed directly by [EC-REARRANGE-EMPTY-REGION]: an empty region `[cutN, cutN+1)` contributes to offset arithmetic for other sections but moves nothing, because there are no spans to iterate over.

---

## Summary

| Aspect | Behavior |
|--------|----------|
| Subspace restriction | None — cuts can span 1.x/2.x/3.x boundaries |
| Cross-subspace moves | Accepted silently; violates `INV-SUBSPACE-CONVENTION` |
| Sparse regions | Implicitly skipped — no crums, no iterations |
| Tombstones | Do not exist; DELETE physically frees crums |
| Guard mechanism | None (unlike INSERT's knife or DELETE's `strongsub`) |

---

## Code Exploration

Now I have enough to answer comprehensively. Let me trace the full call chain.

---

## Region-Transposition / Permutation Operations in udanax-green

### 1. The Call Chain for `rearrange`

The FEBE `rearrange` request enters at `fns.c:159`:

```c
void rearrange(typetask *taskptr)
{
    (void) getrearrange (taskptr, &docisa, &cutseq);
    putrearrange (taskptr);
    if (!dorearrange (taskptr, &docisa, &cutseq))
        ...
}
```

This calls `dorearrange` (do1.c:34–43):

```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    typeorgl docorgl;
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    /*&& TRUE*/ /* ht stuff */  );
}
```

`findorgl` looks up the document's orgl (POOM) in the `granf` granfilade. Then `rearrangepm` (orglinks.c:137–142) is called:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

This passes the full `docorgl` POOM and `index=V` into `rearrangend` with **no subspace filtering whatsoever**.

---

### 2. `rearrangend` Operates on the Entire POOM V-Axis

`rearrangend` (edit.c:78–160) processes all crums in the target POOM:

```c
int rearrangend(typecuc *fullcrumptr, typecutseq *cutseqptr, INT index)
{
    // ...
    knives.dimension = index;  // index == V
    // ...
    makecutsnd (fullcrumptr, &knives);
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
    prologuend ((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
    for (ptr = (typecuc*)findleftson(father); ptr; ptr = (typecuc *)findrightbro(...)) {
        i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
        switch (i) {
          case 0: case 4:  // never move
            break;
          case 1: case 2: case 3:  // shift
            tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
            ivemodified((typecorecrum*)ptr);
            break;
        }
    }
    // ...
}
```

The loop at edit.c:113 walks **all** children, regardless of their V-address. Every crum in the POOM — text or link — is classified and potentially displaced.

---

### 3. V-Space Layout: Text Subspace vs Link Subspace

The document POOM contains two kinds of content:

**Text crums** (V ∈ [1.x, 2.0)): placed by `insertpm` during `insert` and `copy` operations, with the first V-address being approximately 1.1.

**Link reference crums** (V ≥ 2.x): placed by `docreatelink` (do1.c:195–221) which calls `findnextlinkvsa` (do2.c:151–167):

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);
    tumblerincrement (&firstlink, 1, 1, &firstlink);
    // firstlink = 2.1

    doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);
    else
        movetumbler (&vspanreach, vsaptr);
    return (TRUE);
}
```

Link references are placed at V ≥ 2.1. The link's ISA (I-address) is what actually gets stored at these V-positions (via `docopy` of the `ispanset` produced by `tumbler2spanset`).

This is also confirmed by `findvsatoappend` (orglinks.c:29–49):

```c
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);
// linkspacevstart = 2.0
if (tumblercmp (&reach.dsas[V], &linkspacevstart) == LESS) {
    movetumbler (&reach.dsas[V], vsaptr);  // no links in doc
} else {
    findnextaddressinvspace(ptr, &grasp, &linkspacevstart, vsaptr);
}
```

The subspace boundary in V-space is at **2.0** (mantissa[0]=2): text below it, link references at or above it.

---

### 4. De Facto Protection for Link Crums — But No Explicit Guard

When cuts are specified within the text subspace (all cut positions < 2.0), the link crums at V ≥ 2.x are classified by `rearrangecutsectionnd` (edit.c:191–204):

```c
INT rearrangecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    for (i = knives->nblades -1; i >= 0 ; --i) {
        cmp = whereoncrum (ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME) {
            return (-1);          // crum straddles cut — error
        } else if (cmp <= ONMYLEFTBORDER) {
            return (i+1);         // crum starts at or after this cut
        }
    }
    return (0);  // crum is left of all cuts
}
```

For a link crum at V = 2.x and cuts all at V < 2.0: `whereoncrum` of cut address (< 2.0) relative to link crum (≥ 2.x) returns `TOMYRIGHT` — the crum is entirely to the left of the cut. The `cmp <= ONMYLEFTBORDER` test fails for all iterations, so the function returns **0**.

Section 0 in `rearrangend` (edit.c:122) maps to:
```c
case 0: case 4:  /* these never move */
    break;
```

**Link crums therefore survive a text-subspace rearrange unmodified.** But this is purely a numerical consequence of the tumbler ordering — there is no guard clause, no subspace check, and no assertion. If cuts extend into V ≥ 2.x, link crums will be displaced just like text crums.

The classifiers `istextcrum` / `islinkcrum` (orglinks.c:246–260) exist but are **not used** in the rearrange path. They appear only in `maxtextwid`, which is called by `retrievevspansetpm` (orglinks.c:173–221) for reporting the document's V-span:

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){
        return TRUE;
    }
    return FALSE;
}
```

---

### 5. Depth-2 Subspaces (Link Document POOMs)

A link document's POOM uses depth-2 V-addresses for its endpoints, established by `setlinkvsas` (do2.c:169–183):

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);  // from = 1.1
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);      // to = 2.1
    if (threevsaptr) {
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);  // three = 3.1
    }
    return (TRUE);
}
```

If `rearrange` is called with a link document's ISA as target, `findorgl` retrieves the link's POOM and `rearrangend` operates on its depth-2 V-addresses (1.1, 2.1, 3.1). There is no check in `dorearrange` or `rearrangepm` distinguishing document ISAs from link ISAs. The link's internal endpoint layout would be corrupted if the cut positions land in range.

---

### 6. Sparse / Tombstoned V-Ranges

**There are no tombstones in the POOM.** Deletion (`deletend`, edit.c:31–76) physically removes crums via:

```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);
    break;
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

Crums in the deleted range are freed; crums after it have their V-displacement shifted down by `width`. No sentinel or tombstone crum is left behind.

When `rearrangend` is called with cuts that fall in a sparse/deleted region:

1. `makecutsnd` tries to split crums at cut positions. If no crum spans a cut (gap), no split occurs — it silently succeeds.
2. `newfindintersectionnd` finds the subtree father for the cut region.
3. The loop through children classifies crums by which inter-cut section they fall in. Crums on either side of the gap are classified by their actual V-addresses vs the cut positions. The gap itself has no representation to classify.
4. Offsets (`diff[1]`, `diff[2]`, `diff[3]` from `makeoffsetsfor3or4cuts`, edit.c:164–184) are applied to matching crums regardless. The result is crums displaced into or away from the gap region, potentially producing a non-contiguous V-address layout.

No validation of cut positions exists. `acceptablevsa` (do2.c:110–113) is a stub:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

And there is no analogous cut-position validation before calling `rearrangend`.

---

### Summary

| Question | Answer | Key Evidence |
|---|---|---|
| Does rearrange operate only on text subspace? | **No** — operates on the full POOM V-axis | `rearrangepm` calls `rearrangend(..., V)` without filtering — orglinks.c:139 |
| Are link crums protected? | **De facto only** — section 0 = no movement when cuts < 2.0 | `rearrangecutsectionnd` returns 0 for crums left of all cuts — edit.c:191–204 |
| Is there an explicit guard? | **No** | No subspace check in `rearrangepm`, `dorearrange`, or `rearrangend` |
| Can link-subspace (V ≥ 2.x) crums be rearranged? | **Yes**, if cuts extend into that range | Same rearrange logic applies uniformly |
| Are link POOMs (depth-2 V-addresses) at risk? | **Yes**, if rearrange targets a link ISA | No ISA type check in `dorearrange` |
| How are tombstoned/sparse ranges handled? | **Silently** — no crums to split, adjacent crums shifted per diff offsets | `deletend` frees crums physically; `acceptablevsa` is a stub returning TRUE — do2.c:110–113 |
| Does the ht/spanfilade get updated on rearrange? | **No** — commented out | `/*&& TRUE*/ /* ht stuff */` in `dorearrange` — do1.c:42 |

The `permute` function (orglinks.c:404–422) — called by `vspanset2ispanset` / `ispan2vspanset` — is **coordinate mapping** (V↔I), not arrangement transposition. It too has no subspace filtering; it will map V-spans in link space (≥ 2.x) to I-addresses just as readily as text spans. The only point where subspace filtering is explicitly applied is `doshowrelationof2versions` (do1.c:428–449), which calls `filter_specset_to_text_subspace` (do1.c:414–426) before comparison — a later semantic fix documented as Bug 015/Finding 015.
