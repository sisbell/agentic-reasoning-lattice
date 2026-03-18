## Question 13 [gregory]

> When `isanextensionnd` detects that a COPY's I-addresses are contiguous with an existing POOM entry in the target document, it coalesces them into a single crum — does this silent merging ever cause problems for `retrievedocvspanset` or `compare_versions`, where the system might need to distinguish separately-copied spans that happened to be I-address-adjacent?

## KB Synthesis

No, the silent coalescing never causes problems for either operation. Here's why:

**`isanextensionnd` only coalesces when both conditions hold:**

From `[ST-VCOPY]` (Finding 0046): extension requires (1) same `homedoc` (I-address origin document) AND (2) contiguous in both V and I dimensions. The `homedoc` field records which document originally allocated the I-addresses — not which document the content was copied *from* most recently.

This guard prevents the problematic case. If you copy "AB" from source S1 and then "CD" from source S2, even if those I-addresses happen to be numerically adjacent and the V-positions are contiguous, they have different homedoc values and are never merged. Cross-provenance spans stay separate.

**For `retrievedocvspanset`:**

Coalescing of adjacent same-homedoc content is not an information loss — it is the explicitly intended behavior. `[INV-VSPAN-CONSOLIDATION]` states this directly: "the span representation returned by retrieve_vspanset is always maximally consolidated — adjacent spans with consecutive V-positions are merged." This is an invariant, not a side effect. Two separately-copied but I-address-contiguous spans from the same source *are* the same logical block of content; consolidating them is semantically correct.

**For `compare_versions`:**

From `[SS-COMPARE-VERSIONS]` (Finding 0015) and `[INT-SPORGL-VERSION-COMPARE]`, the operation works via I-address intersection: V-spans are converted to I-spans via sporgls, then intersected. Crum structure is invisible to this path — the I-address range produced by one coalesced crum is identical to the union of two separate crums covering the same range. The comparison result is the same either way.

**The one scenario that might look suspicious:**

If document T copies "AB" (i1–i2) from S at V 1.1, then separately copies "CDE" (i3–i5) from S at V 1.3, and these are I-address-contiguous and V-address-contiguous, coalescing produces one crum [V 1.1, V 1.6) → [i1, i5]. `compare_versions(T, S)` finds one large shared span. This is correct — T genuinely shares that entire contiguous I-address range with S. There is nothing to distinguish about the assembly history; Xanadu's content identity model (`[INV-CONTENT-IMMUTABILITY]`) concerns *which* I-addresses are present, not *how many operations* placed them there.

The `homedoc` guard is the key: it ensures that only content of genuinely identical provenance ever gets coalesced, making the merge semantically lossless for both retrieval and comparison purposes.

---

## Code Exploration

Now I have everything needed for a complete, sourced answer.

---

## Answer: `isanextensionnd` Coalescing and Its Effects on `retrievedocvspanset` and `compare_versions`

### The Coalescing Mechanism

`isanextensionnd` [insertnd.c:301–309] fires inside `insertcbcnd` [insertnd.c:242–275] during POOM insertion. When it returns TRUE, the new span is silently absorbed into the existing crum by extending its width rather than creating a new node:

```c
// insertnd.c:250-258
if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
    dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
    ivemodified (ptr);
    setwispupwards (father,1);
    ...
    return(FALSE);
}
```

The coalesce condition is:

```c
// insertnd.c:301-309
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions must hold simultaneously:

**Condition 1 — Same `homedoc`.** The source document of the new insertion must match the existing crum's `c2dinfo.homedoc`.

**Condition 2 — 2D adjacency in BOTH I and V.** The key is `dspsize(POOM)`. From [wisp.h:26–27]:

```c
#define DSPSIZEPM 2
#define dspsize(A) ((A)==GRAN?DSPSIZEGR:((A)==SPAN?DSPSIZESP:DSPSIZEPM))
```

`DSPSIZEPM = 2`, so `lockeq` [wisp.c:261–266] compares **both** `dsas[I]` and `dsas[V]` of the reach vs. the new origin. Coalescing only fires when the existing crum ends at exactly the same point in BOTH I-space AND V-space as the new insertion begins.

---

### Why the 2D Adjacency Condition Is the Load-Bearing Safety Invariant

Each POOM bottom crum created by `insertpm` [orglinks.c:75–134] has equal I-width and V-width. `insertpm` sets them together:

```c
// orglinks.c:115-117
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

This encodes a **stride-1** linear mapping between I-space and V-space inside every crum. A crum with absolute grasp (I=i₁, V=v₁) and width w represents the bijection: V-position v₁+k ↔ I-position i₁+k for k ∈ [0, w).

When `isanextensionnd` fires on two crums A and B:
- Crum A: V=[v₁, v₁+w₁), I=[i₁, i₁+w₁)
- Crum B: V=[v₁+w₁, v₁+w₁+w₂), I=[i₁+w₁, i₁+w₁+w₂)

The 2D adjacency condition guarantees A's reach equals B's origin in **both** dimensions. After coalescing to V=[v₁, v₁+w₁+w₂), I=[i₁, i₁+w₁+w₂):

- For any k < w₁: V↔I via merged crum = i₁+k = same as A alone ✓
- For any k ≥ w₁: V↔I via merged crum = i₁+k = i₁+w₁+(k-w₁) = same as B alone ✓

The linear formula **remains continuous and correct** across the join point because the 2D adjacency requirement is exactly the condition that makes this true.

---

### Effect on `retrievedocvspanset`

`doretrievedocvspanset` [do1.c:322–336] calls `retrievevspansetpm` [orglinks.c:173–221], which reads **only the POOM root's top-level summary**:

```c
// orglinks.c:184-190
if (is1story (&ccptr->cwid.dsas[V])) {
    vspan.itemid = VSPANID;
    movetumbler (&ccptr->cdsp.dsas[V], &vspan.stream);
    movetumbler (&ccptr->cwid.dsas[V], &vspan.width);
    ...
}
```

Internal tree structure — whether a range is stored as one merged crum or two separate crums — is completely invisible here. The root's `cwid` summary reflects the same total V-coverage either way.

**Verdict: coalescing is irrelevant to `retrievedocvspanset`.**

---

### Effect on `compare_versions`

`doshowrelationof2versions` [do1.c:428–449] follows this pipeline:

```
filter_specset_to_text_subspace
  → specset2ispanset [do2.c:14–46]
    → vspanset2ispanset [orglinks.c:397–402]
      → permute [orglinks.c:404–422]
        → span2spanset [orglinks.c:425–454]
          → retrieverestricted [retrie.c:56–85]
            → findcbcinarea2d [retrie.c:229–268]
              → makecontextfromcbc [context.c:151–174]
              → incontextlistnd [context.c:75–111]
          → context2span [context.c:176–212]
```

`findcbcinarea2d` walks the POOM tree to bottom crums that intersect the query V-range, then `context2span` clips each crum to the queried sub-range:

```c
// context.c:191-203
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement (&grasp.dsas[idx2], 0,
                      (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
                      &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement (&reach.dsas[idx2], 0,
                      -tumblerintdiff(&reach.dsas[idx1], &upperbound),
                      &reach.dsas[idx2]);
}
```

This is linear arithmetic. For a merged crum spanning V=[v₁, v₁+w₁+w₂), I=[i₁, i₁+w₁+w₂), a query for V=[v₁+w₁, v₁+w₁+w₂) clips:
- Bottom: `grasp.dsas[I]` advances by `w₁` → yields i₁+w₁
- Top: no clip needed
- Result: I=[i₁+w₁, i₁+w₁+w₂)

This is **identical** to what two separate crums would produce. The merged crum cannot be distinguished from the pair.

**Verdict: coalescing is transparent to `compare_versions`.**

---

### The One Real Information Loss — and Why It Doesn't Matter

After coalescing, the merged crum retains `c2dinfo.homedoc` (source document identity) but loses track of the **source V-positions** of the two contributing spans. The `type2dbottomcruminfo` struct [crum.h:107–110] holds only `homedoc`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

If you copy source V=[1,3) and then source V=[10,13) from the same document into a target consecutively — and the underlying I-addresses happen to be contiguous — the resulting POOM cannot distinguish "these came from two non-contiguous source locations."

But **`compare_versions` doesn't need to distinguish this**. Its job is to find common I-addresses between two versions. The I-coverage of the merged crum is correct. The back-mapping from I-addresses to source V-positions is performed by querying the **source document's** POOM (via `ispan2vspanset` on the source orgl in `restrictvspecsetovercommonispans` [correspond.c:52–80]), which was never modified during the copy. The source POOM correctly records whether those I-addresses came from V=[1,3) and V=[10,13) as separate non-contiguous regions.

The target POOM's coalesced crum records only that I=[100,106) occupies V=[1,6) in the target — which is correct. The source structure is preserved in the source document.

---

### Conditions Under Which Problems WOULD Arise

There is one hypothetical edge that would be unsafe: if two crums from **different** V→I linear offsets ended up satisfying the `isanextensionnd` condition. But this is ruled out by the 2D check. To satisfy `lockeq(..., dspsize(POOM))` [insertnd.c:308, wisp.h:26]:

> Both the I-reach and the V-reach of the existing crum must equal the I-origin and V-origin of the new insertion.

Combined with the stride-1 invariant from `insertpm`, this condition is the **unique** relationship that makes the two crums representable as a single contiguous parallelogram. Any configuration that would produce incorrect `context2span` output necessarily fails this 2D check and is never coalesced.

---

### Summary Table

| Caller | How it uses POOM | Affected by coalescing? |
|--------|-----------------|------------------------|
| `retrievedocvspanset` → `retrievevspansetpm` | Reads root `cwid.dsas[V]` only | **No** — invisible |
| `compare_versions` → `findcbcinarea2d` | Walks to bottom crums | **No** — `context2span` linear clipping handles merged crums correctly |
| `context2span` clipping logic | Linear I↔V arithmetic | **No** — 2D adjacency condition preserves linear stride-1 map |

The silent merging is safe by construction. `isanextensionnd`'s 2D adjacency gate (`dspsize(POOM) = 2` in `lockeq`) is precisely calibrated to admit only merges that preserve the linear V↔I bijection that the rest of the system assumes.
