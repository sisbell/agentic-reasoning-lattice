## Question 17 [evidence]

> When the compared specsets cover only sub-ranges of each document rather than full extents, is the correspondence computation restricted before the POOM walk (via retrieverestricted-style bounded traversal) or computed over full documents and filtered afterward?

## KB Synthesis

The KB does not contain direct source-level evidence from `correspond.c`'s internals about this specific question, but the mechanism can be inferred with high confidence from the V→I conversion pipeline that `compare_versions` must use.

## The Restriction Mechanism

The POOM walk is **bounded pre-walk**, not a full-document traversal with post-filter.

The conversion chain documented in the KB is:

`vspanset2ispanset` → `permute()` → `span2spanset()` → `retrieverestricted()`

This is the same path used by link following, endset retrieval, and transclusion. Critically, `retrieverestricted()` at `retrie.c:56-85` takes an address range as a parameter and performs **bounded B-tree traversal** — it descends only into subtrees whose grasp/reach intervals overlap the specified span [SS-POOM-MULTIMAP, SS-VSPAN-TO-SPORGL].

Specifically, `permute()` at `orglinks.c:404-422` "iterates restriction spanset, calls `span2spanset()` per span" [SS-POOM-MULTIMAP]. Each input V-span from the specset becomes a separate bounded traversal of the POOM. Nodes outside the specified V-range are never visited.

## What the KB Says About compare_versions Specifically

[PRE-COMPARE-VERSIONS] (Finding 0015) describes the algorithm:
1. Retrieve V-spans from both documents
2. Filter to text subspace only (missing in current implementation)
3. Convert V-spans to I-spans
4. Find common I-addresses
5. Map back to V-spans

Step 3 uses `vspanset2ispanset`, which performs bounded traversal per input V-span. When the caller provides a sub-range specset, those sub-range spans are passed directly to step 3, and the POOM walk is restricted to those ranges.

[ST-SPECSET-COMPARE] (Finding 0003) confirms the observable result: "Content outside the SpecSet boundaries is excluded from comparison results. This means compare is not a whole-document operation — it respects the SpecSet as a filter on which content participates."

## One Caveat

[PRE-COMPARE-VERSIONS] also notes that the *current buggy implementation* calls "retrieve V-spans from both documents" (step 1 gets the full vspanset via `retrieve_vspanset`), which is why link spans trigger Bug 0009. This step 1 is only relevant when `correspond.c` internally retrieves document extents itself rather than receiving caller-provided specsets. If the caller provides explicit sub-range specsets, step 1 is bypassed — the sub-range V-spans go directly into step 3's bounded traversal.

## Summary

The restriction is **pre-walk via bounded traversal** through `retrieverestricted`. Whether the input is the full document extent or a sub-range specset, the POOM walk is parameterized by the input V-spans — there is no post-filter step that walks more than needed. The `retrieverestricted`-style bounded traversal is a fundamental property of the V→I conversion pipeline shared across all operations including `compare_versions` [SS-VSPAN-TO-SPORGL, SS-POOM-MULTIMAP, INT-SPORGL-VERSION-COMPARE].

---

## Code Exploration

I now have everything needed for a complete, citation-backed answer.

---

## Answer

The correspondence computation is **restricted before the POOM walk**, not filtered afterward. The restriction is injected as a bounded traversal argument into `retrieverestricted` — exactly the same mechanism as for any other restricted retrieval. However, there is also a second, post-conversion restriction pass at the I-span level. Here is the precise execution trace.

---

### The call chain

```
showrelationof2versions [fns.c:250]
  └─ doshowrelationof2versions [do1.c:428]
       ├─ specset2ispanset (×2) [do2.c:14]
       │    └─ vspanset2ispanset [orglinks.c:397]
       │         └─ permute [orglinks.c:404]
       │              └─ span2spanset [orglinks.c:425]
       │                   └─ retrieverestricted ← RESTRICTION INJECTED HERE [orglinks.c:435]
       │                        └─ retrieveinarea [retrie.c:87]
       │                             └─ findcbcinarea2d [retrie.c:229]
       │                                  └─ crumqualifies2d (guards each node) [retrie.c:270]
       ├─ intersectspansets [correspond.c:145]
       └─ ispansetandspecsets2spanpairset [do2.c:185]
            ├─ restrictspecsetsaccordingtoispans [correspond.c:18]
            │    └─ restrictvspecsetovercommonispans [correspond.c:52]
            │         └─ ispan2vspanset [orglinks.c:389]
            │              └─ permute → span2spanset → retrieverestricted (again, bounded)
            └─ makespanpairset [correspond.c:267]
                 └─ makespanpairsforispan (linear zipper, no tree walk) [correspond.c:290]
```

---

### Phase 1: V→I conversion — POOM walk is bounded by the sub-range span

`specset2ispanset` [do2.c:14–46] walks the incoming specset. For each `VSPECID` item it calls `vspanset2ispanset` with the document's vspanset exactly as supplied by the caller — not inflated to the full document extent. That function delegates immediately to `permute` [orglinks.c:397–401]:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
  typespanset *permute();
  return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` [orglinks.c:404–422] iterates one span at a time over the input `restrictionspanset`:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
}
```

Each individual span in the specset's vspanset is passed, one at a time, to `span2spanset`. Inside `span2spanset` [orglinks.c:425–454], the restriction span is passed directly as `span1ptr` to `retrieverestricted`:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
```
— `orglinks.c:435`

`retrieverestricted` [retrie.c:56–85] unpacks the span into a `(span1start, span1end)` half-open interval. `span2ptr` is `NULL`, so `span2start` and `span2end` are zeroed:

```c
if (span1ptr) {
    movetumbler (&span1ptr->stream, &span1start);
    tumbleradd (&span1start, &span1ptr->width, &span1end);
} else {
    tumblerclear (&span1start);
    tumblerclear (&span1end);
}
if (span2ptr) { ... } else {
    tumblerclear (&span2start);
    tumblerclear (&span2end);
}
```

The call reaches `findcbcinarea2d` [retrie.c:229–268], which calls `crumqualifies2d` at every internal and leaf node:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                           span2start, span2end, index2, ...)) {
        continue;
    }
```
— `retrie.c:252–255`

`crumqualifies2d` [retrie.c:270–305] applies the restriction test for dimension 1 (the V-axis, the restriction span):

```c
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if ( endcmp <= ONMYLEFTBORDER) { return(FALSE); }
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if ( startcmp > THRUME ) { return (FALSE); }
```
— `retrie.c:282–290`

Any node whose V-extent lies entirely outside `[span1start, span1end)` is pruned without descent. **The POOM walk is bounded to the sub-range at every level of the tree.** No full-document traversal occurs.

For the second dimension (`span2`, the I-axis here), `span2end` is zero, so `iszerotumbler(span2end)` is TRUE and that check short-circuits to `TOMYRIGHT` [retrie.c:292], meaning the I-axis is unbounded — every I-extent qualifies, which is correct because we want all I-addresses reachable from the given V-span.

---

### Phase 2: I-span intersection — post-conversion but still pre-final-walk

After both specsets are converted to ispansets, `doshowrelationof2versions` [do1.c:443–448] computes:

```c
specset2ispanset(taskptr, version1, &version1ispans, READBERT)
&& specset2ispanset(taskptr, version2, &version2ispans, READBERT)
&& intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
&& ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
```

`intersectspansets` [correspond.c:145–189] uses `spanintersection` [correspond.c:210–265] to find only the I-addresses common to both versions. This is a **pure span arithmetic pass** — no tree walk.

`ispansetandspecsets2spanpairset` [do2.c:185–207] then calls:

```c
restrictspecsetsaccordingtoispans(taskptr, ispanset, &specset1, &specset2);
makespanpairset(taskptr, ispanset, specset1, specset2, pairsetptr);
```

`restrictspecsetsaccordingtoispans` [correspond.c:18–50] calls `restrictvspecsetovercommonispans` [correspond.c:52–90] for each specset, which for each `(ispan, specset)` pair calls `ispan2vspanset` → `permute` → `span2spanset` → `retrieverestricted` **again** — now with each common I-span as the restriction, bounding the POOM walk to only nodes whose I-extent overlaps that span. `removespansnotinoriginal` [correspond.c:92–135] then further clips the result to the intersection with the caller's original V-span ranges.

`makespanpairsforispan` [correspond.c:290–349] is a **linear zipper** walk over the already-restricted span lists — it never touches the POOM tree at all.

---

### Summary

The correspondence computation uses **restriction before the POOM walk** via the `retrieverestricted`-style bounded-traversal mechanism, not compute-everything-then-filter:

| Stage | Mechanism | Where bounded |
|---|---|---|
| V→I conversion (`specset2ispanset`) | `retrieverestricted` with `span1ptr = V-span` | `crumqualifies2d` prunes at every node [retrie.c:253–255] |
| I-span intersection | span arithmetic only | No tree walk |
| Re-restriction by common I-spans (`restrictvspecsetovercommonispans`) | `retrieverestricted` with `span1ptr = I-span` | Same `crumqualifies2d` path |
| Final pairing (`makespanpairsforispan`) | linear list zipper | No tree walk |

The key invariant is in `span2spanset` [orglinks.c:435]: **the restriction span is passed directly as `span1ptr`**, so `crumqualifies2d` tests each crum's extent against that span boundary before descending. A sub-range specset therefore causes a sub-range POOM traversal — narrower input spans mean fewer nodes qualify and fewer subtrees are entered. Full-document traversal with post-hoc filtering never occurs.
