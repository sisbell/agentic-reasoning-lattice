# Review of ASN-0054

## REVISE

### Issue 1: A0 invariant category and K.μ⁻ gap

**ASN-0054, A0 (V-Domain Contiguity)**: "A0 is a per-state invariant of all reachable states, in the same category as S2, S3, S8a, S8-depth, and S8-fin. The formal mechanism: K.μ⁺ and K.μ~ preconditions must be extended to require that the resulting arrangement satisfies A0."

**Problem**: The arrangement invariants lemma (ASN-0047) proves S2, S3, S8a, S8-depth, and S8-fin are preserved by *each elementary transition*. The proof for K.μ⁻ is: these properties are preserved by restriction of M(d). Contiguity is not preserved by restriction — removing an interior V-position from a contiguous domain produces a non-contiguous domain. The formal mechanism extends K.μ⁺ and K.μ~ but says nothing about K.μ⁻. A raw K.μ⁻ removing position v_j (with 0 < j < n−1) satisfies ASN-0047's K.μ⁻ precondition (d ∈ E_doc) while violating A0.

The ASN later acknowledges this: "Intermediate states within a composite may temporarily violate A0 (as when INSERT first shifts positions rightward, creating a gap, before filling it)." But this contradicts "in the same category" — S2/S3/S8a/S8-depth/S8-fin hold at every intermediate state; A0 does not. A0 is a composite-boundary invariant, not an elementary-transition invariant.

**Required**: Either (a) reclassify A0 as a composite-level invariant with a proof that every valid composite restores it (distinct from the per-elementary proof strategy of the arrangement invariants lemma), or (b) extend K.μ⁻ preconditions to require that the resulting arrangement satisfies A0 — which restricts K.μ⁻ to endpoint removal and forces gap-closing into a different elementary transition. In either case, drop "in the same category as S2, S3, S8a, S8-depth, and S8-fin."

### Issue 2: V(d) uniform depth relies on unstated single-subspace assumption

**ASN-0054, The Text Domain**: "By S8-depth, all elements share a common tumbler depth we call L(d)."

**Problem**: S8-depth guarantees depth uniformity *within a single subspace* (positions sharing the same first component). V(d) is defined as {v ∈ dom(Σ.M(d)) : v₁ ≥ 1}, which may include positions from multiple subspaces (v₁ = 1, v₁ = 2, etc.). S8-depth does not give uniform depth across different first-component values. If V(d) contains a position with v₁ = 1 at depth 2 and a position with v₁ = 2 at depth 3, L(d) is undefined.

It is true that A0 + S8-fin force V(d) into a single subspace (by the same infinite-chain argument used in A1 — positions with v₁ = 1 produce an unbounded ascending chain below any position with v₁ = 2). But L(d) is introduced *before* A0 is stated, so A0 cannot be invoked to justify L(d). The derivation order is circular.

**Required**: Either restrict the definition to a single subspace — V(d) = {v ∈ dom(Σ.M(d)) : v₁ = 1} — so S8-depth directly yields L(d), or state an explicit invariant that the text domain contains positions from at most one subspace identifier and derive L(d) from that.

### Issue 3: Worked example invokes zero displacement

**ASN-0054, Worked Example**: "M(d)([1, 1]) = [3, 0, 1, 0, 5] = a₁ ⊕ [0, 0, 0, 0, 0]"

**Problem**: [0, 0, 0, 0, 0] is a zero tumbler. TumblerAdd requires w > 0 (TA0 precondition: w is positive). The main text correctly notes: "At i = 0 no displacement arithmetic is needed — the base case is the definition of a_s." The worked example contradicts this by writing an explicit ⊕ with a zero displacement.

**Required**: Replace "a₁ ⊕ [0, 0, 0, 0, 0]" with "a₁ (base case)" to match the convention established in the run definition.

### Issue 4: A6 partition cites wrong property

**ASN-0054, A6 (Partition)**: "Every V-position in V(d) belongs to exactly one run (S2: M(d) is a function, so each V-position has a unique I-address and hence a unique run assignment)."

**Problem**: S2 (ArrangementFunctional) says each V-position maps to exactly one I-address. This is about functional uniqueness of M(d), not about partitioning V(d) into runs. Unique run assignment follows from the construction: runs are maximal contiguous break-free intervals of a contiguous index set, which partition that set by definition. The inference "unique I-address → unique run assignment" is a non sequitur — run assignment is determined by position within the break structure, not by the I-address value.

**Required**: Replace the S2 citation with the actual justification: maximal break-free intervals of a contiguous index set partition it by construction.

### Issue 5: A12 equality condition omits V-span width

**ASN-0054, A12 (Arrangement Equality)**: "M(d₁) = M(d₂) as partial functions iff their canonical decompositions agree: same number of runs p, and for each j, start(σ_V(R_j^{d₁})) = start(σ_V(R_j^{d₂})) and σ_I(R_j^{d₁}) = σ_I(R_j^{d₂})."

**Problem**: The condition checks V-span starts and I-spans but does not explicitly check V-span widths. The implication — that I-span equality determines run length r_j, which together with V-start equality determines the V-span — is valid but unstated. A reader checking the reverse direction must reconstruct: I-span width encodes r_j; V-span width is [0,...,0,r_j] at depth L(d); V-start equality forces L(d₁) = L(d₂); therefore V-spans match.

**Required**: Either state the full condition (σ_V matching, not just start matching) or add a one-line note that V-span width is determined by I-span width and the shared depth.

## OUT_OF_SCOPE

### Topic 1: Link subspace invariants
**Why out of scope**: The ASN explicitly restricts to the text subspace (v₁ ≥ 1). Link subspace structure (v₁ = 0) is acknowledged in open questions and belongs in a future ASN addressing link addressing.

### Topic 2: Formal operation definitions as elementary composites
**Why out of scope**: INSERT, DELETE, REARRANGE, and COPY are described by postconditions. Their decomposition into ASN-0047 elementary transitions (K.α, K.μ⁺, K.μ⁻, K.μ~, K.ρ) is deferred. The A0 preservation arguments are conditional on the postconditions being achieved — validating that these postconditions are achievable via valid composites is the concern of a future operations ASN.

### Topic 3: L(d) constancy across document lifetime
**Why out of scope**: Whether the V-depth can change across editing operations is acknowledged in open questions. This ASN establishes per-state properties; cross-version depth constraints are separate.

### Topic 4: Allocation discipline constraints on run structure
**Why out of scope**: T10a constrains how I-addresses are produced but this ASN treats I-addresses as given. The question of what run patterns allocation discipline permits is acknowledged in open questions.

VERDICT: REVISE
