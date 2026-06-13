# Review of ASN-0122

I checked every introduced claim against its cited foundations, reconstructed the proofs the ASN compresses, and ran the worked example independently. The relation is derived rather than posited, the stability theorems cover the entire transition vocabulary, and the boundary cases are part of the definitions rather than left to the reader. I could not find a skipped case, an unproven conjunct, or a hand-wave that fails to reconstruct. Details of the verification, and the few topics correctly deferred, are below.

## REVISE

None.

The following were the load-bearing checks, all of which hold:

- **corr derivation (X1, X2).** The address-vs-value dichotomy is genuinely argued, not asserted. X2's reachability construction is valid: each composite (K.α deposits identical `v` at fresh `a_i`, K.μ⁺ installs at the content-subspace minimum, K.ρ records) satisfies ValidComposite★ — intra-composite preconditions hold at the intermediate state, and J0/J1★/J1'★ hold between endpoints because the single range-new address and the single new provenance entry are the same pair. S4 then forces `a₁ ≠ a₂` regardless of `C(a₁) = C(a₂)`. The exclusion is correctly normative.
- **X9 (SubspaceVacuity).** All three sub-arguments check (CL-OWN single-valued `origin`; SD/L14 store disjointness; CL-UNIQ per-document injectivity), and the decomposition `corr = content-relation ⊔ {(p,p) : p ∈ P ∩ Q ∩ Inst_L}` is exhaustive over the four foot-subspace combinations. The losslessness statement is stated with precision (arrangement-domain information discarded, correspondence information not).
- **The hygiene/guarantee separation.** The `σ = ([1,5],[3])` witness is correct — `reach = [4]`, so `[2,7] ∈ ⟦σ⟧` with `subspace = s_L` — and the `∩ V_{s_C}(d_i)` clip discards it independent of the start-component predicate. X12's precondition note correctly attributes X9's losslessness to the clip, not to `subspace(start) = s_C`.
- **X4c, X10, X11.** The interval-clipping argument reconstructs fully (monotone feet + order-convex span ⇒ interval of `k` ⇒ at most one pair). X10(a)'s cardinality argument correctly splits `k₁ = 0` (TS4) from `k₁ ≥ 1` (TS3+TS4 / TS5). X11's partition is a genuine maximal-run argument: succ is a function (≤1 successor), TS2 gives ≤1 predecessor, TS4 forbids cycles, and the tie-break is necessary exactly under fan-out.
- **Worked example.** Recomputed end to end. The 3-element relation, the width-2/width-1 maximal split, the swap landing two chains on one first foot (exercising the second-foot key), the window clip dropping the boundary-crossing element to a single in-window pair, and the 6-element self-comparison with the disjoint-window detector returning `{b}` — all forced by the definitions.
- **X-T / X6 / X7.** The transport lemma is correct (res-preservation read both directions, injectivity carries the rectangle). The full edit vocabulary is covered — μ⁺, μ⁺_L, μ⁻ (suffix-retention), ASN-0082 shifting contraction, μ~ — with α/λ/ρ/δ dismissed by X5; nothing in the vocabulary is skipped. X6's two composition premises (endpoint persistence; edits interposed between an intermediate's incoming and outgoing steps) are exactly the right ones, and the post-arrival-vs-pre-arrival timing distinction in X6(c) is correct.

## OUT_OF_SCOPE

### Topic 1: n-way alignment and information-equivalence of matching-based reports
The first three Open Questions (irreducibility of position-level completeness, interoperable pair granularity, sound composition of pairwise reports into n-way alignment) are genuine future territory. The ASN correctly fixes a denotational conformance standard (R1–R3 binding, R4 reference) that makes pair granularity free, which is the right groundwork to defer the granularity-selection question rather than legislate it here.

### Topic 2: Derived correspondence-index consistency
The "what consistency contract must a cached/derived index satisfy" question is correctly deferred. X5's memorylessness pins the obligation ("any cache must be derived and exactly consistent, on pain of non-conformance") without specifying the index, which is the appropriate boundary for this ASN.

VERDICT: CONVERGED
