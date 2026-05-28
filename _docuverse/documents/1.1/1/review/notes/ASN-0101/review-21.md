# Review of ASN-0101

I'll examine the DELETE specification systematically: the operation definition (D0), the gap-closure mechanics (D1), the seven preservation claims (D2–D8), the projection consequences (D9), the vocabulary extension (D10), and the weakest preconditions (D11).

## Checking the core operation specification (D0)

The "Justification of the reduction" rigorously establishes that containment reduces to `p + n − 1 ≤ n_S`. The argument handles `m_S = 2` (vacuous middle range) and `m_S ≥ 3` (case analysis on `v_{j₀} = 0` vs `v_{j₀} ≥ 2`) explicitly. T1 case (i) is correctly invoked at each divergence position. The `v_i = s_i = r_i` for `1 ≤ i < j₀` step relies on the minimality of `j₀` and the structural form of `s` and `r` — sound.

The shift function `σ_d` is precisely specified: existence by construction, uniqueness by TS2.

## Checking D1's bijection argument

The order-preservation argument correctly invokes TS1's contrapositive to rule out `u₂ < u₁`. Injectivity falls out cleanly. The post-state characterization `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S − n}` is verified: Λ contributes `[1, p−1]`, Q contributes `[p, n_S−n]`, union is `[1, n_S−n]`. The empty case (`n_S = n`) is explicitly handled.

## Checking D8 (the omnibus)

This is the proof most at risk of hand-waving. The Group (i) analysis traces each invariant:

- The disjointness arguments (`Λ ∩ Q = ∅` by last-component ranges, cross-subspace by first-component) are explicit.
- The source correspondence argument (each post-state `v` has `M'(d)(v) = M(d)(u)` for unique `u`) is the load-bearing mechanism for S3★, S3★-aux, CL-OWN, CL-UNIQ.
- The CL-UNIQ argument (three-step: `Λ ∩ Π = ∅` by ranges; pre-state CL-UNIQ on `Λ ⊎ Π`; σ_d bijection on Π) correctly handles the case where positions `Q ∩ X ≠ ∅` are re-mapped.
- The S8★ singleton decomposition correctly discharges the existential S8 obligation regardless of whether ASN-0058 maximally-merged decomposition is preserved.

Group (ii) and (iii) frame discharges: I verified each invariant in the lists. P4★'s case analysis covers `d'' ≠ d` (via D5), `d'' = d, v ∈ Λ`, `d'' = d, v ∈ Q`, and `d'' = d, v ∈ V_{S'}(d)` — covering all routes.

## Checking the boundary cases

The enumeration covers empty post-state, deletion at start, deletion at end, singleton subspace, singleton interior, non-singleton interior, and cross-subspace independence. For each, the discharge route is traced — D-MIN★ via vacuous discharge in most cases, via non-vacuous σ_d-witness in the "deletion at start" case specifically. Λ ∪ Q upper bound `n_S − n` is correct across all routes.

## Checking the worked examples

The content-subspace example (n_S=4, n=2, p=2 at depth 3): I verified D-CTG★, D9 third bullet, D11 discoverability wp, and cardinality wp all check out against the concrete computation. The link-subspace example exercises CL-OWN and CL-UNIQ at depth 2. The cross-document example exercises D5 and D9 bullet 1.

The `a_1 ⊕ δ(4, #a_1) = [d, 0, 1, 5]` computation checks via TumblerAdd's componentwise rule.

## Checking D10's vocabulary extension

The J0/J1★/J1'★ vacuity arguments on a one-step DEL composite are sound:
- J0: `dom(C') = dom(C)` by D2, so `dom(C') \ dom(C) = ∅`.
- J1★: case analysis on `S` exhibits a pre-state witness whenever a post-state witness exists.
- J1'★: `R' = R` by D0 frame.

The Consequence paragraph correctly notes that this is *only* one-step vacuity; multi-step composites containing DEL can still fail composite-level J0 via the K.α–K.μ⁺–DEL example. This is the key non-triviality and is correctly identified.

The LP-family extension catalogue is exhaustive over ASN-0098's LP2★–LP14 with correct dispatch (D3 for LP2★/LP3★/LP13, D5 for LP4/LP5, D9 for the affected document, D11 supplanting LP12a/LP12b).

## Checking D11 (wp analysis)

DEL determinism is correctly argued (each component uniquely determined; σ_d^{-1} well-defined by TS2/D1). The wp negation equivalence follows from determinism within the precondition domain.

For discoverability from `d`:
- Post-state non-emptiness reduces correctly to `project_pre ∩ (dom(M(d)) \ X) ≠ ∅`, i.e., `project_pre ⊄ X`.
- The three-summand decomposition (Λ, σ_d(Π), V_{S'}) combines correctly under σ_d bijectivity.

For cardinality from `d`:
- `|project_post| = |project_pre ∩ V_{S'}(d)| + |project_pre ∩ Λ| + |project_pre ∩ Π| = |project_pre| − |project_pre ∩ X|`.

The cross-document wps coincide with pre-state predicates (D9 first bullet) — explicitly verified.

The cardinality-preservation specialization (`project_pre ∩ X = ∅`) is the correct boundary case.

The worked example checks: pre-state `project = {a_1, a_2, a_3, a_4}`, X-intersection = 2, predicted post-state cardinality = 2; cross-checks against the concrete post-state.

## REVISE

(none)

## OUT_OF_SCOPE

(none — the Open Questions section correctly identifies versioning, full reversibility, and causal ordering as future work, not gaps in this ASN)

VERDICT: CONVERGED
