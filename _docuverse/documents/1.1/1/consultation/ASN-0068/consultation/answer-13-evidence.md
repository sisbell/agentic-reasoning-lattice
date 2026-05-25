## Question 13 [evidence]

> When a single I-address span is mapped to multiple V-positions in one document (self-transclusion), does `compare_versions` emit a separate correspondence pair for each V-position, producing an N×M cross-product against the other document's mappings?

## KB Synthesis

## Self-Transclusion and `compare_versions` Cross-Product Behavior

The KB does not contain a direct finding for this exact combination, but the relevant mechanisms can be synthesized:

### What the mechanisms predict

**The POOM is a genuine multimap.** `ispan2vspanset(poom, i)` returns a *set* of VSpans — every V-position mapping to that I-address. When document A has I-range R at V-positions v1 and v2 (via self-transclusion), the I→V step yields `{v1, v2}` for A. [SS-POOM-MULTIMAP]

**`correspond.c` assumes 1:1.** The implementation's nested loop "assumes each ispan matches at most one vspec" — this assumption is stated explicitly as the cause of the link-subspace crash. [EC-COMPARE-VERSIONS-LINK-CRASH]

**The inverse operation (`ispan2vspanset`) is the shared path.** Both link endset retrieval and `compare_versions` I→V conversion go through `permute` → `span2spanset` → `retrieverestricted`, which accumulates all contexts. [SS-POOM-MULTIMAP, INT-SPORGL-VERSION-COMPARE]

### The structural tension

If document A has N V-positions for I-range R and document B has M V-positions for R, the theoretically correct result would be N×M correspondence pairs. The set-returning nature of `ispan2vspanset` would deliver that input to `correspond.c`. However, the 1:1 assumption in `correspond.c`'s loop means the code was not designed to consume and emit that cross-product correctly — it likely processes only the first result from each side.

### What cannot be answered from the KB

Whether the outcome is:
- Silent truncation to a 1×1 pair (one V-position from each side)
- A crash (as with the link subspace case)
- Incorrect pairing

is not documented by any finding. The KB has no scenario directly testing `compare_versions` against a document containing internal self-transclusion. The self-comparison case [EC-SELF-COMPARISON] documents the trivial reflexive case (same document, no internal duplication) and returns a single full-span pair — but that does not address the multimap scenario.

### Summary

The POOM multimap would supply N×M I-span pairs to `correspond.c`, but `correspond.c`'s 1:1 structural assumption means the N×M cross-product is almost certainly **not** what is emitted. The exact failure mode (truncation, crash, or wrong pairing) is not answerable from the KB. [SS-POOM-MULTIMAP, EC-COMPARE-VERSIONS-LINK-CRASH, EC-SELF-TRANSCLUSION, SS-COMPARE-VERSIONS]

---

## Code Exploration

I now have complete information to answer the question definitively. Here is the full answer.

---

## Answer: Self-Transclusion in `compare_versions` — Does It Produce an N×M Cross-Product?

**No.** `compare_versions` does not produce an N×M cross-product. The intermediate I-span intersection is N×M, but the downstream span-pairing is sequential (1:1), not a cross-product. In the untested full-document case, the code produces sequential pairs until one specset is exhausted, then crashes.

---

## Complete Call Chain

### Entry: `doshowrelationof2versions` — `do1.c:428-449`

```c
bool doshowrelationof2versions(typetask *taskptr, typespecset version1, typespecset version2, typespanpairset *relation)
{
  typeispanset version1ispans = NULL;
  typeispanset version2ispans = NULL;
  typeispanset commonispans = NULL;

    filter_specset_to_text_subspace(taskptr, version1);
    filter_specset_to_text_subspace(taskptr, version2);

    return
        specset2ispanset(taskptr, version1, &version1ispans, READBERT)
      &&    specset2ispanset(taskptr, version2, &version2ispans, READBERT)
      &&    intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
      &&    ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
    ;
}
```

Three distinct phases: (1) V→I for each doc, (2) I-span intersection, (3) build span pairs.

---

### Phase 1: V→I Conversion — how self-transclusion creates duplicate I-spans

**`specset2ispanset`** `do2.c:14-46` loops over vspecs and calls:

**`vspanset2ispanset`** `orglinks.c:397-402`:
```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

**`permute`** `orglinks.c:404-422` iterates over input V-spans:
```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
}
```

**`span2spanset`** `orglinks.c:425-454` is where the key behavior emerges:
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`retrieverestricted` performs a 2D enfilade search (`findcbcinarea2d` `retrie.c:229-268`) that traverses ALL crums whose V-extent intersects the query span and collects them into a context list via `incontextlistnd` `context.c:75-111`, which "always adds new entries" (Finding 0039 confirmed this).

**`context2span`** `context.c:176-212` then extracts the target-dimension span from each context by computing the proportional offset between the restriction bounds and the crum's grasp/reach.

**The consequence for self-transclusion:** If Document A has I-span I-X appearing at V1 and V2 (two PM crums: `(V=V1, I=I-X)` and `(V=V2, I=I-X)`), and the query specset covers the full document V-span:

- `retrieverestricted` finds **both crums**
- The `for (c = context ...)` loop runs twice
- `context2span` extracts I-X **from each crum separately**
- `onitemlist` appends both to the ispanset (no deduplication)

**Result: `version1ispans = [I-X, I-X]`** — two identical entries.

---

### Phase 2: I-span Intersection — the N×M step

**`intersectspansets`** `correspond.c:177-182`:
```c
for (; set1; set1 = set1->next) {
    for (p = set2; p; p = p->next) {
        if (comparespans (taskptr, set1, p, set3, spantype))
            set3 = &(*set3)->next;
    }
}
```

This is an explicit **nested loop**: every entry in set1 is tested against every entry in set2. With `version1ispans = [I-X, I-X]` (N=2) and `version2ispans = [I-X]` (M=1):

- Outer iteration 1 (I-X): Inner p=I-X → intersection I-X → added
- Outer iteration 2 (I-X): Inner p=I-X → intersection I-X → added again

**`commonispans = [I-X, I-X]`** — N×M = 2 entries.

---

### Phase 3: Building Pairs — sequential, NOT cross-product

**`ispansetandspecsets2spanpairset`** `do2.c:185-207` calls:
1. `restrictspecsetsaccordingtoispans` — filters specsets to only V-spans with common I-spans
2. `makespanpairset` — builds the actual output pairs

**`restrictspecsetsaccordingtoispans`** `correspond.c:18-50` calls `restrictvspecsetovercommonispans` `correspond.c:52-90`:

```c
*newspecsetptr = NULL;
for (; ispanset; ispanset = ispanset->next) {      // outer: each common I-span
    for (; specset; specset = ...) {                // inner: remaining vspecs (NOT RESET!)
        if(ispan2vspanset(taskptr,versionorgl,ispanset,&docvspanset)){
            s1 = new vspec with docvspanset;
            ...
        }
    }
}
```

**Critical:** the inner loop does not reset per outer iteration. For the N×M `commonispans`:
- First I-X: processes all vspecs; `ispan2vspanset(A_orgl, I-X)` returns `[V1, V2]`; creates `{A, [V1, V2]}`; specset exhausted
- Second I-X: specset is NULL → nothing added

After `removespansnotinoriginal` `correspond.c:92-135` further intersects with the original specset:
- `specset1 = [{A, [V1, V2]}]` (total V-width = 2w)
- `specset2 = [{B, [W1]}]` (total V-width = w)

**`makespanpairset`** `correspond.c:267-288`:
```c
for (; ispanset; ispanset = ispanset->next) {    // loops N×M = 2 times
    movetumbler (&ispanset->width, &iwidth);
    makespanpairsforispan (taskptr, &iwidth, &specset1, &specset2, &pairset);
    *pairsetptr = pairset;
    pairsetptr = &pairset->nextspanpair;
}
```

**First iteration** (iwidth = w):

`makespanpairsforispan` `correspond.c:290-349`:
```c
spec1 = (typevspec *)*specset1ptr;   // {A, [V1, V2]}
span1 = spec1->vspanset;              // V1
spec2 = (typevspec *)*specset2ptr;   // {B, [W1]}
span2 = spec2->vspanset;              // W1
while (span1 && span2 && tumblercmp (iwidth, &sum) == GREATER) {
    // width(V1) == width(W1) == w: EQUAL case
    *pairsetptr = makespanpair(..., &span1->stream, ..., &span2->stream, &span1->width);
    // sum = w; loop exits (sum == iwidth)
```

Pair `(A.V1, B.W1, w)` produced. W1 consumed → `*specset2ptr = NULL`. V2 remains in spec1.

**Second iteration** (iwidth = w, `*specset2ptr = NULL`):

```c
spec2 = (typevspec *)*specset2ptr;   // NULL
span2 = spec2->vspanset;              // ← NULL POINTER DEREFERENCE → CRASH
```

There is no NULL guard before this dereference `correspond.c:306`.

---

## Structural Summary

| Step | Location | What happens |
|------|----------|-------------|
| V→I conversion | `orglinks.c:425-454` | Each PM crum generates one I-span entry; self-transclusion generates duplicate I-spans |
| I-span intersection | `correspond.c:177-182` | Explicit N×M nested loop → commonispans has N×M entries |
| V-span restriction | `correspond.c:52-90` | Inner specset loop NOT reset; only first I-span in commonispans produces vspec output |
| Pair building | `correspond.c:290-349` | Sequential 1:1 matching, NOT cross-product; consumes specsets destructively |
| Crash condition | `correspond.c:304-306` | NULL dereference when specset2 exhausted but commonispans loop has entries remaining |

---

## Why the Existing Tests Pass

**All current `compare_versions` tests use narrow specsets.** For example, `internal_transclusion_identity` passes:
- `spec1 = [{D, [1.10, width=0.4]}]` — covers only the *first* V-occurrence
- `spec2 = [{D, [1.19, width=0.4]}]` — covers only the *second* V-occurrence

Each narrow V-span maps to I-X via exactly ONE crum, so:
- `version1ispans = [I-X]` (N=1)
- `version2ispans = [I-X]` (M=1)
- `commonispans = [I-X]` (N×M = 1)
- `makespanpairset` loops once → one pair `(1.10, 1.19)` — matches golden output

The untested scenario — specsets wide enough to cover *both* V-positions of the same I-span — would trigger the crash on the second `makespanpairset` iteration.

---

## Answer to the Question

**No, `compare_versions` does not produce an N×M cross-product output.**

- The intermediate `intersectspansets` step at `correspond.c:177-182` IS a nested loop and creates N×M entries in `commonispans`
- But `makespanpairsforispan` at `correspond.c:290-349` does **sequential 1:1 matching**: V1 with W1, V2 with W2 — never (V1,W1), (V1,W2), (V2,W1), (V2,W2)
- When N ≠ M, the code **crashes** with a NULL dereference at `correspond.c:306` after producing min(N,M) sequential pairs
- When N = M > 1, the code still crashes after N pairs because `commonispans` has N² remaining iterations against exhausted specsets

The algorithm is designed for the non-self-transclusion case (N=M=1 per I-span within a given specset). Self-transclusion with a wide specset is an untested and broken edge case.
