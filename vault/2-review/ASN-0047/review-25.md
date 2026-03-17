# Review of ASN-0047

## REVISE

### Issue 1: Temporal decomposition table and text contradict the ASN's own formal analysis of K.δ

**ASN-0047, Temporal decomposition**: "No elementary transition modifies all three layers simultaneously — each touches at most two (K.δ for documents touches the existential and presentational layers; all others touch exactly one)."

**Table row**: `| Presentational | M | Fully mutable | K.μ⁺, K.μ⁻, K.μ~ (composite), K.δ† |`

**Problem**: The ASN's own formal analysis in the K.μ~ decomposition section explicitly establishes the opposite: "Since M is total with M(e) = ∅ for e ∉ E\_doc, the post-state satisfies M'(e) = M(e) — K.δ does not modify M." K.δ's frame is `(A d' :: M'(d') = M(d'))` — *all* arrangements unchanged. The footnote tries to salvage the table entry by appealing to semantic significance ("entity creation determines which empty arrangements become semantically meaningful"), but this is a philosophical observation, not a state modification. By the ASN's own definitions and proofs, K.δ modifies exactly one state component (E), placing it squarely and exclusively in the existential layer.

The downstream consequence: every elementary transition modifies components in exactly one temporal layer, giving the stronger and more elegant result "each touches exactly one" rather than the weaker "at most two." The current text obscures this clean separation.

**Required**: Remove K.δ† from the Presentational row and its footnote. Change "each touches at most two (K.δ for documents touches the existential and presentational layers; all others touch exactly one)" to "each touches exactly one." The observation that K.δ determines which empty arrangements become semantically meaningful can be retained as a parenthetical note without claiming K.δ "touches" the presentational layer.

## OUT_OF_SCOPE

### Topic 1: Fork arrangement relationship to source
**Why out of scope**: J4 constrains `ran(M'(d_new)) ⊆ ran(M(d_src))` but deliberately leaves open whether the fork must reproduce the source's full arrangement or may select a proper subset. This is a design question for the operation-level ASN, not an error in the transition taxonomy.

### Topic 2: Subspace boundaries under reordering
**Why out of scope**: K.μ~ permits any bijection π satisfying S8a and S8-depth, but whether π must respect subspace boundaries (keeping text-subspace positions within text, link-subspace positions within links) is a constraint on the operation REARRANGE, not on the elementary transition. The elementary transition correctly requires S8-depth in the result; subspace semantics belong to the operation specification.

### Topic 3: Document vs. link distinction within E\_doc
**Why out of scope**: The ASN groups links and documents in E\_doc, noting "The structural distinction between documents and links — endset semantics, subspace layout — belongs to a separate analysis." This is appropriate scope management — both participate identically in the transitions defined here.

VERDICT: REVISE
