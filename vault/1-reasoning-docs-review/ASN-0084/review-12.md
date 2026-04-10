# Review of ASN-0084

## REVISE

### Issue 1: R-DISP proof is incomplete — five region cases hand-waved

**ASN-0084, Displacement Analysis, R-DISP proof**: "The remaining regions follow identically — in each case, the j terms cancel and the common value depends only on region widths."

**Problem**: The lemma claims specific constant displacement values for seven distinct region cases (3-cut: exterior, α, β; 4-cut: exterior, α, μ, β). The proof shows only one case (3-cut α) and appeals to identical structure for the remaining six. While the algebraic pattern is genuinely the same (j cancels in every case), each case substitutes a different formula from R-PPERM/R-SPERM and produces a different constant value. In particular, the 4-cut μ case produces w_β − w_α (a difference of two widths, possibly negative), which is structurally distinct from the other cases that produce sums. A reader verifying R-DISP should be able to confirm each claimed value without re-deriving from R-SPERM.

**Required**: Show the computation for each non-trivial region. The 3-cut β case, 4-cut α, 4-cut μ, and 4-cut β each require a one-line expansion analogous to the 3-cut α case shown. The exterior cases (Δ = 0) can be dispatched in a single sentence since π is the identity there. The computations are short — showing all of them costs four lines and eliminates the hand-wave entirely.

### Issue 2: Range-preservation argument attributes "exactly one" to surjectivity alone

**ASN-0084, State and Vocabulary**: "Since π is surjective onto dom(M'(d)) = dom(M(d)), every u ∈ dom(M'(d)) has the form u = π(v) for exactly one v ∈ dom(M(d))."

**Problem**: Surjectivity gives "at least one" preimage. The "exactly one" conclusion additionally requires injectivity — i.e., bijectivity, which is established in the preceding sentence. The sentence attributes the uniqueness to surjectivity alone. The multiset-preservation argument that follows (showing multiplicities are preserved) depends on this uniqueness, so the attribution matters.

**Required**: Replace "Since π is surjective" with "Since π is a bijection" (or "Since π is bijective"). The rest of the derivation is correct.

## OUT_OF_SCOPE

### Topic 1: Self-inverse property of the 3-cut pivot

The 3-cut pivot with cut sequence (c₀, c₁, c₂) swaps regions α and β. Applying the same pivot a second time restores the original arrangement — the operation is an involution. The 4-cut swap is not generally an involution (unless w_α = w_β). This distinction is a natural consequence of the displacement structure (Δ_α = w_β and Δ_β = −w_α for the pivot, which compose to identity) but belongs in a future ASN on composition of rearrangements.

**Why out of scope**: This is a property of *sequences* of rearrangements, which the ASN explicitly defers to its open questions.

VERDICT: REVISE
