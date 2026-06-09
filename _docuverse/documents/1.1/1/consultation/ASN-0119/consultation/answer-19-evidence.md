## Question 19 [evidence]

> Given [INV-ENFILADE-CONFLUENCE], does performing a single 4-cut swap produce the same final POOM logical content as two separate sequential pivots achieving the same transposition, or do the intermediate states differ in discoverable results?

## KB Synthesis

## Same Final Content, Different Intermediate States

### Final POOM State: Equivalent

Both a 4-cut swap and two sequential pivots achieving the same transposition produce identical final query results.

From [ST-REARRANGE] (Finding 0056), REARRANGE modifies only `ptr->cdsp.dsas[index]` — the V-address displacement — and never touches I-addresses. Both approaches apply arithmetic offsets that produce the same net V→I mapping. The final set of (V-position, I-address) pairs is identical.

From [INV-ENFILADE-QUERY-INDEPENDENCE] and [INV-RETRIEVAL-TREE-INDEPENDENCE], query results are independent of internal crum arrangement. Even if the two approaches leave different internal tree shapes, `incontextlistnd`'s insertion-sort ([INV-RETRIEVAL-V-SORTED]) produces identical V-sorted output regardless of tree structure.

[INV-REARRANGE-IDENTITY] confirms both preserve the full multiset of I-addresses, so all downstream subsystems — link discovery, compare\_versions, transclusion — observe the same final state.

### Intermediate State: Observable and Distinct

Between Pivot 1 and Pivot 2, the document is in a partially-rearranged state that is fully queryable. `retrieve_contents`, `find_links`, and `compare_versions` all reflect this intermediate permutation. The 4-cut swap has no such observable intermediate — per [INV-ATOMICITY] (Finding 0042), the event loop's run-to-completion scheduling makes it atomic from any frontend's perspective.

### Confluence Does Not Directly Apply

[INV-ENFILADE-CONFLUENCE] governs concurrent **additions** to the permanent granfilade layer, where insertion order doesn't affect logical content. POOM mutations are explicitly the **mutable** layer ([SS-POOM-MUTABILITY]), not the permanent layer. Confluence is not stated for POOM mutation sequences and cannot be invoked here.

The final equivalence follows instead from displacement arithmetic being order-independent on disjoint V-regions: if two operation sequences apply the same net offset to each address, the final mapping is identical regardless of path.

---

## Code Exploration

I now have all the code I need. Here is the full analysis.

---

## INV-ENFILADE-CONFLUENCE: 4-Cut Swap vs. Two Sequential Pivots

**[INV-ENFILADE-CONFLUENCE]** is not a named finding in this repository. The closest referent is the CON0 confluence property analyzed in Finding 0041 — "physical non-confluence, logical confluence at the abstraction boundary" — applied here to the POOM rearrange subsystem rather than the permanent layer insertion subsystem. The analysis below extends that framework.

---

### 1. What Each Operation Does to the POOM

Both pivot and swap are implemented by a single function path:

```
fns.c:rearrange() → do1.c:dorearrange() → orglinks.c:rearrangepm() → edit.c:rearrangend()
```

The decisive code in `orglinks.c:137-142`:
```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`rearrangend` is a single function call. It operates atomically: the `bed.c` event loop runs `xanadu()` to completion per iteration [Finding 0042], and within `rearrangend` the offset application loop has no external access point between iterations. There is no observable intermediate state during a 4-cut swap.

---

### 2. The Offset Algebra

**`makeoffsetsfor3or4cuts` [edit.c:164-183]** is the algebraic core.

For a **4-cut swap** with sorted cuts c₀ < c₁ < c₂ < c₃, letting a = c₁−c₀ (width of R1) and b = c₃−c₂ (width of R3):

```c
diff[1] = c2 - c0;                         // R1 [c0,c1) shifts right
a = c1 - c0; b = c3 - c2;
diff[2] = b - a;                            // R2 [c1,c2) shifts by (b−a)
diff[3] = -(c2 - c0);  // sign flipped     // R3 [c2,c3) shifts left
```
[edit.c:170-176]

For a **3-cut pivot** with cuts c₀ < c₁ < c₂:

```c
diff[1] = c2 - c1;                          // R1 [c0,c1) moves right by size of R2
diff[2] = -(c1 - c0);  // sign flipped      // R2 [c1,c2) moves left by size of R1
```
[edit.c:178-180]

These offsets are applied per-crum [edit.c:125]:
```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

The region classifier `rearrangecutsectionnd` [edit.c:191-204] assigns each crum to interval 0–4 by scanning from the rightmost blade leftward and returning `i+1` at the first blade that lies at or left of the crum's origin. Region 0 and region 4 never move; regions 1–3 receive their respective `diff[i]`.

---

### 3. The Equal-Width Constraint

**The 4-cut swap produces a gap-free, non-overlapping V-space ONLY when a = b.**

Proof: The required destination for R1 to immediately follow R3 and R2 is `c₀ + b + (c₂ − c₁)`. The diff[1] applied by the algorithm is `c₂ − c₀`. For these to match:

```
c₂ − c₀  =  b + (c₂ − c₁)
         =  (c₃ − c₂) + c₂ − c₁
c₁ − c₀  =  c₃ − c₂
       a  =  b
```

When a ≠ b, the 4-cut swap shifts R1 to `[c₂, c₂+a)` and R2 to `[c₁+(b−a), c₂+(b−a))`, which overlap or leave gaps in V-space. `findcbcnd` [retrie.c:208-227] returns the **first** matching crum in sibling order:

```c
for (ptr = findleftson ((typecuc*)father); ptr; ptr = getrightbro (ptr))
    if (retr = findcbcnd (ptr, &grasp, address, index))
        break;
```

In the a ≠ b case, retrieve at overlapping addresses shadows one of the conflicting crums. **Two sequential pivots targeting the same transposition do not have this defect** — each pivot is contiguous by construction (the 3-cut offset algebra is algebraically tight for any widths).

All further analysis assumes a = b.

---

### 4. Two Pivots That Achieve the Identical Transposition

For the symmetric (a = b) 4-cut swap producing `R0 R3 R2 R1 R4`, the following two pivots achieve the same:

**Pivot 1:** cuts at `[c₀, c₁, c₃]` — swaps R1 with (R2+R3):
```
diff[1] = c3 − c1          // R1 moves right by (c3−c1)
diff[2] = −(c1 − c0) = −a  // (R2+R3) moves left by a
```
After pivot 1, V-space: `R0 · R2 · R3 · R1 · R4`

**Pivot 2:** cuts at `[c₀, c₀+(c₃−c₁), c₀+(c₃−c₁)+(c₂−c₁)]` in the post-pivot-1 address space — swaps R2 and R3:
```
diff[1] = c3 − c2 = b = a  // R2 moves right by b
diff[2] = −(c2 − c1)        // R3 moves left by (c2−c1)
```
After pivot 2, V-space: `R0 · R3 · R2 · R1 · R4`

**Net displacement for each region after both pivots:**

| Region | Original | Pivot 1 Δ | Pivot 2 Δ | Net Δ | Final |
|--------|----------|-----------|-----------|-------|-------|
| R1 [c₀,c₁) | as placed | +(c₃−c₁) | 0 | +(c₃−c₁) = +(c₂−c₀) | [c₂, c₂+a) |
| R2 [c₁,c₂) | as placed | −a | +b = +a | 0 | [c₁, c₂) |
| R3 [c₂,c₃) | as placed | −a | −(c₂−c₁) | −a−(c₂−c₁) = −(c₂−c₀) | [c₀, c₀+b) |

These match the 4-cut swap offsets exactly (diff[1]=c₂−c₀, diff[2]=0, diff[3]=−(c₂−c₀)), confirming identical V→I mappings.

Concrete verification: "ABCDEFGH" with c₀=2, c₁=4, c₂=6, c₃=8 (a=b=2):
- **4-cut swap**: BC→[6,8), DE stays, FG→[2,4) → **"AFGDEBCH"**
- **Pivot 1** [2,4,8]: BC→[6,8), DEFG→[2,6) → **"ADEFGBCH"** ← discoverable intermediate
- **Pivot 2** [2,4,6]: DE→[4,6), FG→[2,4) → **"AFGDEBCH"** ← identical to 4-cut result ✓

---

### 5. Intermediate States Differ and Are Discoverable

The 4-cut swap executes **atomically** within one `rearrangend` call [orglinks.c:139], which is one FEBE operation within one `xanadu()` invocation [bed.c, Finding 0042]. The loop at [edit.c:113-135] applies all offsets before returning. No RETRIEVE between iterations is possible.

The two-pivot path exposes its intermediate state **externally**: after pivot 1 but before pivot 2, a RETRIEVE on the POOM returns content in the partially-rearranged order (R0 R2 R3 R1 R4 in the example = "ADEFGBCH"). Any client FEBE operation issued between the two pivots observes this state. The intermediate state is distinct from any state observable during the atomic 4-cut swap.

---

### 6. Final State: Logically Identical, Physically Divergent

**Logical content (V→I mapping):** Identical. As shown in section 4, the net V-displacement applied to each leaf crum is numerically equal whether via 4-cut swap or two pivots. `whereoncrum` [retrie.c:345-397] computes position purely from `cdsp.dsas[index]` and `cwid.dsas[index]`, so `retrieve` [retrie.c:33-54] and `retrieveinspan` return the same values.

**Physical tree structure:** Divergent, for two reasons:

1. **Different cut boundaries.** `makecutsnd` [ndcuts.c:15-31] inscribes cut points into the enfilade via `slicecbcpm` [ndcuts.c:373-450]. Path A creates boundaries at {c₀, c₁, c₂, c₃}. Path B creates boundaries at {c₀, c₁, c₃} during pivot 1, then at different positions during pivot 2. These are different sets of V-address boundaries, producing different leaf crum granularities.

2. **Different recombine histories.** `recombinend` [recombine.c:104-131] merges sibling nodes via `ishouldbother` [recombine.c:150-163] — two nodes merge if their combined son count fits within `MAX2DBCINLOAF`. After pivot 1's recombine, R2 and R3 crums (which moved by the same offset in pivot 1) may be merged into a single node. Pivot 2 then re-splits this merged node via `makecutsnd`. After path A, no such merge-then-resplit occurs, leaving different crum boundaries in the tree.

This is the same "physical non-confluence, logical confluence" pattern identified in Finding 0041 CON0 for the permanent layer, now manifesting at the POOM rearrange layer. The difference is that for the permanent layer, CON0 concerns insertion order; here it concerns the path by which a given transposition is achieved. In both cases, **the abstraction boundary (what queries return) is confluent; the implementation (tree node layout, crum displacement encoding) is not.**

---

### 7. Summary Answer

| Property | 4-Cut Swap | Two Sequential Pivots |
|----------|------------|----------------------|
| Final V→I mapping (retrieve result) | **Identical** | **Identical** |
| Intermediate state observable | None (atomic) | Yes — "ADEFGBCH" between pivots |
| Physical POOM tree structure | Cut boundaries at {c₀,c₁,c₂,c₃} | Cut boundaries at different positions; recombine history differs |
| Valid for a ≠ b | No — overlapping V-addresses | Yes — always gap-free |

**To the question**: A single 4-cut swap and two sequential pivots achieving the same transposition produce **identical final POOM logical content** (all queries via `retrieve`/`retrievedinspan` return the same results), **provided a = b**. The intermediate states **do differ in discoverable results**: after the first pivot, a RETRIEVE issued before the second pivot returns content in a different order than the original or the final, and this state has no counterpart during the atomic 4-cut swap. The final physical POOM tree structure diverges (per the CON0 pattern of Finding 0041) but is invisible at the query boundary.

**Relevant source locations:**
- `edit.c:78-160` — `rearrangend`, the atomic rearrange kernel
- `edit.c:164-183` — `makeoffsetsfor3or4cuts`, offset algebra
- `edit.c:191-204` — `rearrangecutsectionnd`, region classifier
- `orglinks.c:137-142` — `rearrangepm`, single-call wrapper confirming atomicity
- `ndcuts.c:15-31` — `makecutsnd`, cut-boundary inscription
- `recombine.c:104-131` — `recombinend`, path-sensitive tree merging
- `retrie.c:208-227` — `findcbcnd`, V-address lookup (first-match semantics)
- `retrie.c:345-397` — `whereoncrum`, displacement-only position computation
