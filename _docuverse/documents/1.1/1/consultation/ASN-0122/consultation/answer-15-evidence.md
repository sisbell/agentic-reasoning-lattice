## Question 15 [evidence]

> If document A contains the same I-addresses at two different V-positions (self-transclusion) and document B contains them once, does SHOWRELATIONOF2VERSIONS return two correspondence pairs (one per V-occurrence in A), and via what mechanism — does incontextlistnd enumerate all V-positions per shared I-span?

## KB Synthesis

## Answer

**Yes, two correspondence pairs are returned — one per V-occurrence in A.** Both the V→I conversion path and (if needed) the I→V path participate via `incontextlistnd`. Here is the full mechanism.

---

### Step 1: V→I conversion produces two sporgls for document A

`vspanset2sporglset` calls `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted`, querying the POOM by its V-dimension.

Document A's POOM is a multimap [SS-POOM-MULTIMAP]. It holds **two separate crums** pointing to the same I-address range `i₁..i₄`:
- Crum₁: V 1.10..1.13 → I i₁..i₄
- Crum₂: V 1.19..1.22 → I i₁..i₄

When `findcbcinarea2d` queries the V-dimension range covering A's full content, it traverses all siblings at each B-tree level and recurses into all qualifying subtrees, accumulating every matching leaf node [SS-POOM-MULTIMAP]:

> "The accumulation function `incontextlistnd()` inserts each found context into a sorted linked list, never replacing existing entries."

Both crums fall within the V-range query. `incontextlistnd` accumulates both. The result is **two distinct contexts**, both carrying I-address `i₁..i₄` but at different V-positions. `vspanset2sporglset` therefore produces:
- Sporgl₁: (origin=i₁, width=0.4, doc=A) ← from V 1.10
- Sporgl₂: (origin=i₁, width=0.4, doc=A) ← from V 1.19

Document B produces one sporgl:
- Sporgl₃: (origin=i₁, width=0.4, doc=B) ← from B's single V-occurrence

[INT-SPORGL-VERSION-COMPARE] confirms: "Both documents' content is converted to sporgls, then intersection is computed by I-address (the `sporglorigin` field)."

---

### Step 2: I-space intersection yields two matches

`correspond.c`'s nested loop compares each sporgl from A against each sporgl from B by `sporglorigin`:

- Sporgl₁ ∩ Sporgl₃: `i₁..i₄ ∩ i₁..i₄ ≠ ∅` → **match → pair 1**
- Sporgl₂ ∩ Sporgl₃: `i₁..i₄ ∩ i₁..i₄ ≠ ∅` → **match → pair 2**

[SS-COMPARE-VERSIONS]: "The operation produces a list of ordered pairs of V-spans — one from each document — where the paired spans reference the same permascroll I-address range."

Each pair is reported with the V-position embedded in the sporgl, yielding:
```
Pair 1: (A: V 1.10 for 0.4,  B: V <B's position> for 0.4)
Pair 2: (A: V 1.19 for 0.4,  B: V <B's position> for 0.4)
```

---

### The I→V direction confirms the same result

If `ispan2vspanset` is invoked for A on the shared I-span (e.g., during a follow-up query), it queries A's POOM by the I-dimension. `findcbcinarea2d` again traverses all qualifying subtrees and `incontextlistnd` accumulates all matching contexts [SS-POOM-MULTIMAP]:

> `ispan2vspanset(poom, i_B) = { VSpan(1.10, 0.4), VSpan(1.19, 0.4) }`

[INV-RETRIEVAL-V-SORTED] confirms the result list is V-sorted regardless of tree structure.

---

### Limiting condition

This only works cleanly for the text subspace. If A or B contains links, `correspond.c` crashes [EC-COMPARE-VERSIONS-LINK-CRASH] because the link ISAs in the 2.x subspace are not permascroll addresses and the nested-loop logic breaks. The self-transclusion scenario is safe precisely because all I-addresses involved are permascroll addresses in the 1.x subspace [PRE-COMPARE-VERSIONS].

---

## Code Exploration

I have now traced the complete execution path. Here is the full answer.

---

## SHOWRELATIONOF2VERSIONS and Self-Transclusion

**Short answer: No — only ONE correspondence pair is returned, not two. `incontextlistnd` does enumerate both V-positions (the mechanism works correctly), but the pairing stage in `makespanpairsforispan` is bounded by the I-space width budget, which is exhausted after the first match.**

---

## Full Execution Trace

### 1. Entry Point: `doshowrelationof2versions` [`do1.c:428`]

```c
bool doshowrelationof2versions(typetask *taskptr, typespecset version1, typespecset version2, typespanpairset *relation)
{
    ...
    return
        specset2ispanset(taskptr, version1, &version1ispans, READBERT)
      &&    specset2ispanset(taskptr, version2, &version2ispans, READBERT)
      &&    intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
      &&    ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
    ;
}
```

**Step 1 — V→I conversion for doc A.** `specset2ispanset` at [`do2.c:14`] calls `vspanset2ispanset` → `permute` → `span2spanset` for A's V-span (which covers both V1 and V2). The POOM for A has two crums: one for (V1→I1) and one for (V2→I1). When `vspanset2ispanset` runs, both crums contribute to the I-output. The result `version1ispans` contains the I-span I1 of width W.

**Step 2 — V→I for doc B.** Same path; B's POOM has one crum (VB→I1). `version2ispans` = I1 of width W.

**Step 3 — Intersection.** `intersectspansets` at [`correspond.c:145`] finds the overlap: the single I-span I1, width W. I-space has only one copy of I1 regardless of how many V-positions reference it.

**Step 4 — Pair generation.** `ispansetandspecsets2spanpairset` at [`do2.c:185`]:

```c
restrictspecsetsaccordingtoispans(taskptr, ispanset, &specset1, &specset2);
makespanpairset (taskptr, ispanset, specset1, specset2, pairsetptr);
```

---

### 2. The `incontextlistnd` mechanism inside `restrictvspecsetovercommonispans`

`restrictspecsetsaccordingtoispans` at [`correspond.c:18`] calls `restrictvspecsetovercommonispans`, which calls `ispan2vspanset(taskptr, orgl_A, ispanset, &docvspanset)`. This is the path where `incontextlistnd` acts.

Call chain: `ispan2vspanset` [`orglinks.c:389`] → `permute` [`orglinks.c:404`] → `span2spanset` [`orglinks.c:425`]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
//                                              ↑ I                ↑ V
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`retrieverestricted` at [`retrie.c:56`] → `retrieveinarea` → `findcbcinarea2d` at [`retrie.c:229`]:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, ...)) {
        continue;
    }
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);   // ← index1 = I
    }
}
```

Doc A's POOM has **two leaf crums** that both satisfy `crumqualifies2d` for the I-span I1: one crum records (V1, I1) and the other records (V2, I1). `findcbcinarea2d` visits both siblings during its `getrightbro` traversal. For each, it calls `incontextlistnd`.

**`incontextlistnd` at [`context.c:75`] inserts each context into a sorted linked list keyed on `index1 = I`.** The sort key `grasp.dsas[I]` is the context's I-address left boundary. Both crums share I1.start, so both enter the list (the second is inserted at the beginning, per the `< THRUME` case at [`context.c:90`], but both are present). The function never replaces — it always appends or inserts:

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    prologuecontextnd (c, &grasp, (typedsp*)NULL);   // extracts c's I-coordinate
    ...                                               // linked-list insertion sort
}
```

Back in `span2spanset` at [`orglinks.c:439`], the loop over both contexts calls `context2span` for each with `targindex = V`, extracting the V-span. The result is a V-span list: **[V1(width W), V2(width W)]**.

**So yes, `incontextlistnd` does enumerate all V-positions** — the two-element context list faithfully represents both occurrences of I1 in doc A. `ispan2vspanset` for doc A returns [V1, V2].

---

### 3. Why only ONE pair is returned: `makespanpairsforispan`

After `restrictspecsetsaccordingtoispans` completes, the input to `makespanpairset` at [`correspond.c:267`] is:

```
commonispans:  [I1, width=W]   (a single I-span)
specset1 (A):  docisa=A, vspanset=[V1(W), V2(W)]
specset2 (B):  docisa=B, vspanset=[VB(W)]
```

`makespanpairset` at [`correspond.c:278`]:
```c
for (; ispanset; ispanset = ispanset->next) {
    movetumbler (&ispanset->width, &iwidth);          // iwidth = W
    makespanpairsforispan (taskptr, &iwidth, &specset1, &specset2, &pairset);
    ...
}
```

`iwidth = W` — the width of the common I-span, drawn directly from `ispanset->width` at [`correspond.c:279`]. This is a **budget** of how much I-content can be paired.

Inside `makespanpairsforispan` at [`correspond.c:308`]:

```c
while (span1 && span2 && tumblercmp (iwidth, &sum) == GREATER) {
    cmp = tumblercmp (&span1->width, &span2->width);
    switch (cmp) {
      case EQUAL:
        *pairsetptr = makespanpair(taskptr, &spec1->docisa, &span1->stream,
                                             &spec2->docisa, &span2->stream, &span1->width);
        tumbleradd (&sum, &span1->width, &sum);    // sum += W → sum = W
        span2 = span2->next;                        // span2 = NULL (B exhausted)
        span1 = span1->next;                        // span1 = V2
        break;
        ...
    }
    pairsetptr = &(*pairsetptr)->nextspanpair;
}
// Loop exit check: span2 == NULL → exit
```

**Iteration 1 (and only):**
- `span1 = V1(W)`, `span2 = VB(W)`, `sum = 0`, `iwidth = W`
- `W == W` → EQUAL branch
- Emits pair: **(A, V1.start) ↔ (B, VB.start), width W**
- `sum += W` → `sum = W = iwidth` → `iwidth > sum` is now FALSE
- `span2 = NULL` (B only had VB)
- `span1 = V2` (second occurrence in A, with width W)
- **Loop condition: `span2 == NULL` → exit immediately**

V2 — the second V-occurrence of I1 in doc A — was correctly accumulated by `incontextlistnd`, was correctly returned by `ispan2vspanset`, and is present in specset1's vspanset. But `makespanpairsforispan` exits before ever reaching it because:

1. The I-budget `iwidth = W` (common I-span width) is exhausted after the first pairing.
2. `span2` (B's V-span list) is simultaneously exhausted, providing a second exit condition.

**Result: one pair, `(A:V1 ↔ B:VB)`.**

---

## Mechanism Summary

| Stage | Function | Behavior |
|---|---|---|
| I→V for doc A | `findcbcinarea2d` [`retrie.c:252`] | Visits **all** qualifying POOM leaf crums for I1 |
| Context accumulation | `incontextlistnd` [`context.c:75`] | Inserts each context into sorted list; never replaces — both V1 and V2 context nodes are present |
| V-span extraction | `span2spanset` loop [`orglinks.c:439`] | Converts every context to a V-span; returns **[V1, V2]** |
| Restriction | `restrictvspecsetovercommonispans` [`correspond.c:52`] | Builds specset1 for A with `vspanset=[V1(W), V2(W)]` |
| Pairing | `makespanpairsforispan` [`correspond.c:308`] | Bounded by `iwidth = W` (I-span width); exhausted after pairing V1↔VB; **V2 orphaned** |

**The invariant**: `iwidth` encodes a measure of shared I-content, not shared V-content. The same I-address can appear at N V-positions in a document, but it still occupies only W bytes of I-space. `makespanpairsforispan` treats I-width as the pairing budget: once W bytes of correspondences are accounted for, the loop terminates, regardless of how many V-positions remain in the specset.

`incontextlistnd` is faithful — it enumerates all V-occurrences. The truncation happens exclusively in the pairing algorithm at `correspond.c:308`, which is controlled by `iwidth`, not by the V-span count.

---

**Empirical confirmation**: The golden test `internal/internal_transclusion_identity.json` confirms the one-pair result for the intra-document case (comparing `[1.10, +0.4]` vs `[1.19, +0.4]`, both referencing the same I-span, returns one pair). The cross-document scenario follows the identical code path through `makespanpairsforispan` and produces the same one-pair result by the same mechanism.
