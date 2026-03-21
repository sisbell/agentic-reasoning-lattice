# Review of ASN-0061

## REVISE

### Issue 1: D-CTG labeled (INV) but is not a universal invariant
**ASN-0061, Arrangement Contiguity**: "D-CTG — VContiguity (INV)"
**Problem**: The header labels D-CTG as (INV), which across ASN-0034/0036/0047/0058 means "holds in every reachable state." But the body text correctly states: "bare K.μ⁻ — a valid elementary transition under ASN-0047 — can violate D-CTG by removing a single interior V-position; D-CTG is therefore not preserved by all valid composites, only by those that constitute well-formed editing operations." This is a new category of property — a design constraint on editing operations — distinct from the P-series and S-series invariants that ASN-0047 guarantees for all reachable states. Future ASNs referencing D-CTG need to know it is weaker than those invariants.
**Required**: Use a distinct label (e.g., DESIGN or EDIT-INV) in the header, and add one sentence clarifying that D-CTG is not in the ASN-0047 reachable-state invariant set.

### Issue 2: Bound variable collision in D-CTG
**ASN-0061, Arrangement Contiguity**: `(A d, S, u, w : u ∈ V_S(d) ∧ w ∈ V_S(d) ∧ u < w : ...)`
**Problem**: The bound variable `w` in D-CTG's quantifier denotes a V-position, but throughout the rest of the ASN `w` is the deletion width displacement. Within the D-CTG formula the scoping is correct, but when reading D-CTG in the context of DELETE (which is every use), the collision invites misreading.
**Required**: Rename the bound variable in D-CTG (e.g., `u₂` or `q`).

### Issue 3: Worked example — wrong parenthetical in merge check
**ASN-0061, Worked Example**: "the two blocks are V-adjacent but not I-adjacent (b ≠ b + 3 − 1)"
**Problem**: The merge condition M7 (ASN-0058) requires `a₂ = a₁ + n₁`. Here `a₁ = b`, `n₁ = 1`, `a₂ = b + 3`. The check is `b + 3 ≠ b + 1` (equivalently `a₁ + n₁ ≠ a₂`). The parenthetical "b ≠ b + 3 − 1" evaluates to "b ≠ b + 2", which is true but is not the I-adjacency condition. The conclusion is correct; the arithmetic justifying it is not.
**Required**: Replace "(b ≠ b + 3 − 1)" with "(b + 1 ≠ b + 3)" or equivalently "(a₁ + n₁ ≠ a₂)".

### Issue 4: D-BLK B2 verification incomplete
**ASN-0061, Block Decomposition Effect, B1–B3 verification**: "Disjointness (B2): B_other is disjoint from the S blocks by subspace. Within S: B_left has V-extents ending before p; shifted B_right has V-extents starting at or beyond p (by D-SEP); no overlap."
**Problem**: This establishes three pairwise-disjointness claims — B_other vs S-blocks, B_left vs shifted B_right — but omits within-group disjointness for B_left and for shifted B_right. Within B_left: blocks are subsets of originally disjoint blocks (by B2 on the pre-state decomposition), and splitting preserves disjointness (M5). Within shifted B_right: the original right-region blocks were disjoint, and σ is order-preserving (D-BJ), so shifted V-extents remain disjoint. Both arguments are short but neither is stated.
**Required**: Add one sentence for each within-group case, citing the original B2 and (for shifted B_right) D-BJ.

## OUT_OF_SCOPE

### Topic 1: Depth generalization beyond ordinal depth 1
**Why out of scope**: D-PRE(iv) explicitly restricts to `#p = 2`. All proofs depend on depth-1 ordinal arithmetic (natural numbers). The open questions section already flags this. Generalizing D-SEP's round-trip and D-DP's contiguity preservation to deeper ordinals is genuine new work, not a correction.

### Topic 2: Link-subspace deletion
**Why out of scope**: D-PRE(iii) restricts to S ≥ 1 and the ASN notes "link-subspace deletion follows the same structure but we derive text-subspace first." This is a scoping decision, not an omission.

### Topic 3: D-CTG preservation by INSERT, COPY, REARRANGE
**Why out of scope**: The ASN correctly states this is "a separate verification obligation for each operation's ASN." D-CTG is introduced here; other operations prove their own preservation.

VERDICT: REVISE
