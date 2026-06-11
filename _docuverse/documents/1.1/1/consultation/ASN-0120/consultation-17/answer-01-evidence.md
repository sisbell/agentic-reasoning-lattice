## Question 1 [evidence]

> When CREATELINK's `vspanset2sporglset`/`permute` emits sporgls, is each sporgl's I-span always confined to currently-allocated istream addresses, or can a stored span's width extend past the allocated content into the istream's unallocated frontier (e.g., by merging across or rounding up to crum boundaries)?

## KB Synthesis

Each sporgl's I-span is confined to currently-allocated I-stream addresses. There is no mechanism by which the width can bleed into the unallocated frontier or round up to crum boundaries. Here is why, synthesized across the relevant KB entries.

---

## The Conversion Chain

From [ST-LINK-CREATE] (Finding 0037) and [SS-VSPAN-TO-SPORGL] (Finding 0013), the chain for CREATELINK is:

```
V-span
  → vspanset2ispanset / permute
    → span2spanset
      → retrieverestricted  (finds POOM crums overlapping the query V-range)
    → one I-span per contiguous I-address region
  → one sporgl per I-span
```

Each step is bounded by what the POOM actually contains.

---

## Why I-Spans Cannot Extend Past Allocated Addresses

**1. Crums represent exactly-allocated content.**

From [SS-POOM-BOTTOM-CRUM] (Finding 0076), each bottom crum carries `(V-origin, V-width, I-origin, I-width)`. The I-width is a re-encoded form of the I-span width from allocation — not a rounded or padded value. From [INV-WIDTH-VALUE-EQUIVALENCE] (Finding 0076): `value(crum.width.dsas[V]) == value(crum.width.dsas[I])`. Both sides encode the same integer, which is exactly the byte count inserted.

**2. I-address allocation is exact and byte-granular.**

From [INV-SINGLE-CHAR-GRANULARITY] (Finding 0034): "The granularity of all address operations is the single byte … each byte position receives exactly one I-space address." From [SS-ADDRESS-SPACE] (Finding 0033): `inserttextingranf` increments by `textset->length` — the allocation is byte-exact, no padding or rounding occurs.

**3. The V→I mapping within a crum is bijective.**

A crum covers a contiguous V-range of width W mapped to a contiguous I-range of identical width W ([INV-WIDTH-VALUE-EQUIVALENCE], [SS-SPAN] Finding 0031). Within a crum, the I-offset for any V-position `v` relative to the crum's V-origin is `v - V-origin`, giving I-address `I-origin + (v - V-origin)`. `retrieverestricted` returns the context (crum data) for crums overlapping the query; `span2spanset` then constructs I-spans by intersecting the query V-range with each crum's V-range and mapping the intersection offset into I-space. The result is clipped to the requested V-range, not the full crum extent.

**4. Crums are never wider than their allocated content.**

From [ST-VCOPY] (Finding 0046): `isanextensionnd()` only extends an existing crum rightward when the new content's I-origin equals the crum's I-reach exactly — i.e., when the new allocation is contiguous with the prior one. Extensions never create gaps or pre-allocate space. From [SS-INSERT-VWIDTH-ENCODING] (Finding 0076), `insertpm` sets the crum I-width by direct copy from the actual allocation span (`movetumbler(&lwidth, &crumwidth.dsas[I])`).

**5. I-addresses are monotonically allocated from the permascroll maximum — no lookahead or reservation.**

From [INV-MONOTONIC] (Finding 0061) and [SS-ADDRESS-SPACE] (Finding 0061): allocation is purely `findpreviousisagr` + `tumblerincrement`. There is no pre-reservation of I-address space beyond what is actually written. From [INV-NO-IADDR-REUSE] (Finding 0061): allocations are never recycled. The permascroll frontier is advanced only when bytes are physically inserted.

---

## The Only Subtle Risk

The crum merging path via `isanextensionnd` ([ST-VCOPY] Finding 0046) merges two physically contiguous allocations into one wider crum. This is safe: the resulting I-span is `[I-origin₁, I-origin₁ + W₁ + W₂)`, which is exactly the union of two already-allocated ranges — no unallocated space is included.

---

## Conclusion

When `vspanset2sporglset`/`permute` emits sporgls, each sporgl's I-span is bounded by the POOM crums that overlap the queried V-range. Those crums were created atomically with I-address allocation ([INV-ATOMICITY] Finding 0042), carry widths equal to the exact byte counts allocated ([INV-WIDTH-VALUE-EQUIVALENCE]), and are never wider than the content that produced them. The query path clips results to the requested V-intersection, not to the full crum extent. There is no code path that rounds up to crum boundaries or reaches into the unallocated permascroll frontier.

---

## Code Exploration

I now have all the information needed. Here is the complete analysis.

---

## Answer: I-Spans Are Strictly Confined to Allocated Istream Addresses

The short answer is **no** — a sporgl's I-span can never extend past the allocated istream frontier. Neither rounding up to crum boundaries nor merging across them can expand an I-span beyond what was actually written. Here is the full trace.

---

### 1. Call Chain from `createlink`

```
fns.c:100       createlink()
do1.c:195       docreatelink()
do1.c:214–216   specset2sporglset()   ← for from/to/three specsets
sporgl.c:25     vspanset2sporglset()
sporgl.c:48     vspanset2ispanset()   ← V→I mapping
orglinks.c:393  permute()
orglinks.c:415  span2spanset()
retrie.c:83     retrieverestricted()  ← enfilade traversal
retrie.c:97     findcbcinarea2d()
context.c:176   context2span()        ← intersection + clip
sporgl.c:54–55  copy ispan → sporgl
```

---

### 2. What `vspanset2sporglset` Does with the ispan

`vspanset2sporglset` [sporgl.c:35–65] calls `vspanset2ispanset` for each vspan and then copies the result **verbatim** into the sporgl:

```c
// sporgl.c:48
vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
// sporgl.c:54–55
movetumbler(&ispanset->stream, &sporglset->sporglorigin);
movetumbler(&ispanset->width,  &sporglset->sporglwidth);
```

No arithmetic, no rounding — the sporgl I-span is exactly what `vspanset2ispanset`/`permute` returns.

---

### 3. How `permute` Finds Its I-Spans: Only Existing Crums

`span2spanset` [orglinks.c:425] calls:

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, V, NULL, I, NULL);
```

`retrieverestricted` [retrie.c:56] → `retrieveinarea` [retrie.c:87] → `findcbcinarea2d` [retrie.c:229]. This function **tree-walks the POOM enfilade** looking for bottom crums whose V-interval overlaps the restriction span. It can only find crums that **already exist in the tree** — crums representing content that was actually inserted. No crum beyond the allocated frontier exists to be found.

---

### 4. `context2span` Only Clips — Never Expands

For each found crum, `makecontextfromcbc` [context.c:151] records the crum's exact I-position and I-width from the stored crum fields:

```c
// context.c:160–161
movewisp(offsetptr,   &context->totaloffset);
movewisp(&crumptr->cwid, &context->contextwid);
```

`context2span` [context.c:176–212] then computes the intersection of this crum's I-range with the restriction V-span. Both adjustments are **reductive** (clips only):

```c
// context.c:191–194  — advance I-start if crum's V-start is before restriction
if (tumblercmp(&grasp.dsas[V], &lowerbound) == LESS)
    tumblerincrement(&grasp.dsas[I], 0,
        (INT)tumblerintdiff(&lowerbound, &grasp.dsas[V]), &grasp.dsas[I]);

// context.c:197–200  — retract I-reach if crum's V-reach is beyond restriction
if (tumblercmp(&reach.dsas[V], &upperbound) == GREATER)
    tumblerincrement(&reach.dsas[I], 0,
        -tumblerintdiff(&reach.dsas[V], &upperbound), &reach.dsas[I]);

// context.c:206–207  — write the result
movetumbler(&grasp.dsas[I], &foundspanptr->stream);
tumblersub(&reach.dsas[I], &grasp.dsas[I], &foundspanptr->width);
```

The resulting I-span is always a **subset** of the crum's actual I-extent. It is strictly proportional — no rounding, no boundary snap.

---

### 5. Crum I-Widths Are Set Exactly at Insertion Time — No Rounding

Tracing how I-widths get into crums in the first place confirms there is no rounding:

**In `inserttextgr` [granf2.c:83–108]:** The ispan width is computed as `lsa - spanorigin`, where `lsa` advances by exactly `textset->length` per piece [granf2.c:100]. No padding.

```c
// granf2.c:100
tumblerincrement(&lsa, 0, textset->length, &lsa);
// granf2.c:106
tumblersub(&lsa, &spanorigin, &ispanptr->width);  // exact byte count
```

**In `firstinsertionnd` [insertnd.c:199–218]:** Width copied verbatim.

```c
// insertnd.c:212–213
movewisp(origin, &ptr->cdsp);
movewisp(width,  &ptr->cwid);
```

**In `insertcbcnd` [insertnd.c:242–275]:**  
- **Merge path:** `isanextensionnd` [insertnd.c:301–309] only merges when the new origin **exactly** equals the existing crum's reach (checked via `lockeq`). When it does merge, it adds the two widths exactly: `dspadd(&ptr->cwid, width, &ptr->cwid, ...)` [insertnd.c:251]. No padding is added.  
- **New crum path:** `movewisp(width, &new->cwid)` [insertnd.c:266] — exact copy.

There is no crum-boundary rounding anywhere in the insertion path.

---

### 6. What about `makegappm` and the second cut?

`makegappm` [insertnd.c:124–172] is called before `doinsertnd` when content is being inserted *into* an existing V-extent (not appending). It cuts the POOM tree at the insertion V-address and shifts displaced crums. `findaddressofsecondcutforinsert` [insertnd.c:174–183] computes a second cut point:

```c
// insertnd.c:179–182
tumblerincrement(position, -1, 1, secondcut);
beheadtumbler(position, &intpart);
tumblerincrement(secondcut, 0, -tumblerintdiff(&intpart, &zero), secondcut);
tumblerincrement(secondcut, 1, 1, secondcut);
```

This is arithmetic for finding the correct tumbler address for the cut — it produces a well-defined V-address, not a rounding of an I-address. It does not affect any crum's stored I-width.

---

### Summary

| Stage | What happens to I-span extent |
|---|---|
| `findcbcinarea2d` finds bottom crums | Only crums for *existing* content; frontier is unreachable |
| `makecontextfromcbc` records crum I-range | Exact copy of stored `cwid.dsas[I]` |
| `context2span` clips to restriction | I-span can only *shrink*, never grow |
| `vspanset2sporglset` copies ispan → sporgl | Verbatim; no further arithmetic |
| Crum I-widths at insertion | Set exactly to `textset->length`; no boundary rounding |
| Crum merging (`isanextensionnd`) | Requires exact adjacency; adds widths exactly |

**The sporgl I-span is always the intersection of (a) the crum's actual allocated I-range and (b) the proportional mapping of the requested V-restriction. Neither the enfilade traversal nor `context2span` nor `vspanset2sporglset` can produce an I-address beyond what was allocated. No rounding to crum boundaries occurs anywhere in this path.**
