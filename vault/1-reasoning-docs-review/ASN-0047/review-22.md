# Review of ASN-0047

## REVISE

### Issue 1: S2–S8-fin arrangement invariants lack a composition lemma

**ASN-0047, Elementary transitions / Reachable-state invariants**: "A general constraint applies to all transitions that modify arrangements: the ASN-0036 arrangement invariants — S2 (functional), S3 (referential integrity), S8a (V-position well-formedness), S8-depth (uniform depth within subspace), S8-fin (finite domain) — must hold at the final state of every composite transition. These are not postconditions of individual elementary transitions; they are invariants of the reachable state space."

**Problem**: This paragraph floats between the formal definitions — it is neither part of the valid composite definition (which has only conditions (1) and (2)) nor derived as a consequence. The individual elementary transition definitions *do* show preservation (K.μ⁺ via precondition/disjoint extension, K.μ⁻ via restriction, K.δ via empty arrangement, others via frame), but the composition step — "since each elementary transition preserves these per-state properties, any finite composition does as well" — is never stated. The ASN provides exactly this composition step for P0/P1/P2 via the "Permanence from elementary frames" lemma ("By transitivity over any finite sequence satisfying (1), the composite inherits all three permanence properties"), but S2–S8-fin receive no analogous treatment. The reachable-state theorem's inductive step then says "as derived above for P8 and S2–S8-fin," pointing to the scattered inline arguments without a bridge to composites.

Additionally, the claim "These are not postconditions of individual elementary transitions" is misleading. Each elementary transition *does* preserve S2–S8-fin — K.μ⁺ establishes them via precondition, K.μ⁻ preserves them by restriction, others hold them in frame. The sentence seems to mean "not listed explicitly as ensures clauses," but it reads as "might not be preserved by individual steps."

**Required**: Either (a) add S2–S8-fin as a third condition in the valid composite definition and note that it is satisfied by the transition definitions, or (b) add a composition lemma parallel to "Permanence from elementary frames":

> *Lemma (Arrangement invariants from elementary preservation).* Every valid composite transition preserves S2, S3, S8a, S8-depth, and S8-fin. Each elementary transition preserves these properties: K.μ⁺ establishes them via its preconditions (disjoint extension for S2, referential integrity for S3, explicit S8a/S8-depth/S8-fin requirements); K.μ⁻ preserves them by restriction of M(d); K.δ for documents produces the empty arrangement (vacuously satisfying all five); all other transitions hold M in frame. Since each step of a valid composite preserves these per-state properties, they hold at every intermediate and final state.

Rewrite the floating "general constraint" paragraph to reference this lemma instead of standing as an ungrounded assertion.

### Issue 2: P4 proof — per-elementary framing obscures the composite-level argument

**ASN-0047, P4 (Provenance bounds), Inductive step**: "We verify that each valid composite transition preserves Contains(Σ) ⊆ R, assuming it holds before the transition. We must check all five elementary transitions and the distinguished composite K.μ~."

**Problem**: The proof announces a check of "all five elementary transitions" but then uses Δ = {(a, d) : d ∈ E'\_doc ∧ a ∈ ran(M'(d)) \ ran(M(d))} — a composite-level quantity defined between the composite's initial and final states. J1, the coupling constraint that does the heavy lifting for K.μ⁺, is likewise a composite-level constraint. The per-elementary framing ("K.μ⁺ yields Contains(Σ') ⊆ Contains(Σ) ∪ Δ") suggests the analysis is about individual elementary steps, when it is actually about the composite's net effect.

The core argument is two lines: for any (a, d) ∈ Contains(Σ'), either a ∈ ran(M(d)) — handled by IH and P2 — or a ∈ ran(M'(d)) \ ran(M(d)) — handled by J1. The six-bullet case analysis arrives at the same place but through a framing that conflates elementary and composite levels.

**Required**: Restructure the inductive step to lead with the composite-level argument: split Contains(Σ') into pre-existing and newly introduced containment pairs, handle each by IH+P2 and J1 respectively, then note that the individual elementary analyses confirm *why* only K.μ⁺ introduces new containment and why other transitions are harmless. The per-elementary bullets can remain as supporting detail, but the composite-level structure should be primary.

## OUT_OF_SCOPE

### Topic 1: Root node allocation uniqueness
The initial state designates a bootstrap node n₀, and K.δ permits creating additional root nodes (IsNode(e)) without a parent precondition. GlobalUniqueness (ASN-0034) is proven for the hierarchical allocation mechanism with parent prefixes. For root nodes, which have no parent, the mechanism ensuring globally unique addresses is unspecified. This is allocation protocol design, not a gap in the transition taxonomy.

**Why out of scope**: Allocation protocol details (how addresses are generated and coordinated) belong to a separate ASN; ASN-0047 correctly treats freshness as a precondition (e ∉ E).

### Topic 2: Link-subspace V-position constraints
S8a constrains only text-subspace V-positions (v₁ ≥ 1). K.μ⁺ and K.μ~ can operate on link-subspace positions (v₁ = 0) without S8a-level constraints. The ASN acknowledges this by deferring "the structural distinction between documents and links — endset semantics, subspace layout" to a separate analysis.

**Why out of scope**: Link semantics and subspace-specific constraints are deferred by design; the elementary transitions are intentionally general.

### Topic 3: Transitive provenance chains
The provenance relation R records direct containment (document d held address a). When content is transcluded through a chain (d₁ → d₂ → d₃), each hop generates its own (a, dᵢ) entry via J1, but the chain structure is not recorded. Whether chain provenance requires explicit representation is a separate design question.

**Why out of scope**: The ASN's open questions section identifies this explicitly; the current flat provenance model is sufficient for the transition taxonomy.

VERDICT: REVISE
