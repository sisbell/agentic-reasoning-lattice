# Review of ASN-0102

## REVISE

### Issue 1: J1'★ coupling discharge is invalid for self-transclusion (and any copy of content `d` already references)

**ASN-0102, X14 (ContainmentRecording and coupling discharge)**: "The content-subspace range gains exactly `{a_j + i}` (X3, restricted to subspace `s_C`)" and "each `a_j + i` is a content address newly mapped in `d`'s content subspace at the copied position `v + c_j + i`. Every new provenance pair is therefore backed by a genuine content-subspace range extension, with no spurious record."

**Problem**: When `d_s = d` (self-transclusion, explicitly admitted in X10/X15) or when `d` already references the copied content from a prior copy, the resolved addresses `a_j + i` are *already* in `ran(Σ.M(d))`. They are therefore **not** in `ran(Σ'.M(d)) ∖ ran(Σ.M(d))` — the content-subspace range gains a *subset* of `{a_j+i}`, possibly empty. "Newly mapped at a position" is not the same as "new to the range." The derivation conflates the two. J1★ does not even fire for such addresses (its antecedent `a ∈ ran(M'(d)) ∖ ran(M(d))` is false), and J1'★ holds only because `(a_j+i, d)` is already in `R` by P4★ at the pre-state — *not* because of a "genuine range extension" as the proof claims. The stated reasoning for J1'★ is thus invalid even though the conclusion is salvageable by a different argument.

**Required**: Split the copied addresses into those genuinely new to `ran(M(d))` (range extensions, recorded by COPY's effect) and those already present (pairs already in `R` by P4★). Show J1'★ for both classes explicitly. Correct the "range gains exactly `{a_j+i}`" claim to the actual subset.

### Issue 2: X7's freed-gap justification is stated backwards

**ASN-0102, X7 (NonDestructivePlacement)**: "The gap `[v, v+W)` is V-space that held nothing of `d` before the relabelling. Hence no `(V, I)` binding is overwritten."

**Problem**: When `p ≤ n_S`, the V-positions `[s_C,1,…,1,c]` for `c ∈ [p, p+W)` *did* hold `d`'s content in the pre-state (the content that gets displaced). The gap is **created by** the relabelling `· + W`, not pre-existing "before the relabelling." As written the clause is false in exactly the non-trivial (displacement-occurring) case it is meant to justify.

**Required**: Restate as "the relabelling frees `[v, v+W)` by moving the bindings `≥ v` up to `[v+W, …]`, after which the copied region fills the freed range." The disjointness argument (TS1/TS2/TS4, copied ⊂ `[p,p+W)` vs displaced ⊂ `[p+W,…]`) is correct; only the temporal phrasing is wrong.

### Issue 3: Symbol `Σ` overloaded — state vs. transition vocabulary

**ASN-0102, Definition of COPY**: "we add it to the system's transition vocabulary `Σ` (ASN-0047)".

**Problem**: `Σ` is used throughout this ASN as a *system state* (`Σ = (Σ.C, Σ.L, Σ.E, Σ.M, Σ.R)`, transitions `Σ → Σ'`). Naming the operation set `Σ` in the same sentence collides directly with that usage and is confusing where it matters most — the one place the operation's status is declared.

**Required**: Use a distinct symbol for the transition vocabulary (the foundations use `Σ` for the operation set only in ASN-0034's NoDeallocation; elsewhere state is `Σ`). Disambiguate so a reader of this self-contained note cannot mistake the operation set for a state.

### Issue 4: S8a not discharged for the interior copied positions

**ASN-0102, X16 and Definition**: copied positions are `v + c = [s_C,1,…,1,p+c]` for `0 ≤ c < W`.

**Problem**: P4 (ValidInsertionPosition) discharges S8a only for the insertion anchor `v`. The interior copied positions `v+1, …, v+W−1` are new entries in `dom(Σ'.M(d))` and must independently satisfy S8a (`zeros = 0`, depth `≥ 2`, all components positive). X16 derives their last-component values for the density/tiling argument but never states that they meet S8a. It holds structurally (`s_C ≥ 1`, intermediate `1`s, last `p+c ≥ 1`, depth `m ≥ 2`), but a rigor-complete proof must say so.

**Required**: Add one line confirming every copied position `[s_C,1,…,1,p+c]` satisfies S8a, so S2 (functionality, via disjoint well-formed domains) and S8-depth are fully discharged for the post-state.

## OUT_OF_SCOPE

### Topic 1: COPY of link-subspace content (transcluding links)
P3 restricts the target to `S = s_C` and excludes `s_L`, so links cannot be transcluded by COPY. This is correctly excluded (link semantics are out of scope) and the ASN does not claim otherwise — no error here.

### Topic 2: Discoverability/containment of copied content after subsequent displacement
The Open Questions defer the invariant tying origin to continued discoverability after later operations, further-reference containment, time-varying views, and identity under an unreachable allocator. These are appropriately future ASNs, not gaps in this one.

VERDICT: REVISE
