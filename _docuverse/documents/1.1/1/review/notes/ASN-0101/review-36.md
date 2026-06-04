# Review of ASN-0101

I read this ASN closely, checking each of D0–D11 against the foundation contracts, tracing every boundary case, and verifying the three worked examples line by line. It is unusually thorough, and the places where specifications normally fail are handled explicitly here.

## Verification highlights (no defects found)

- **D0 effect / D1 gap closure.** The shift-inverse `σ_d` is constructed, not assumed: existence via TumblerAdd's componentwise rule on the D-SEQ★ form, uniqueness via TS2, order preservation via TS1 — uniform in `m_S ≥ 2`, correctly generalising ASN-0082's depth-2 D-BJ. The `m_S = 2` base of the containment reduction is handled separately (vacuous middle range) and the `m_S ≥ 3` case discharges `v_{j₀} ∈ {0, ≥2}` against `s` and `r` using only T1/T0, without illicitly assuming `v ∈ V_S(d)`.
- **D8.** Every conjunct of ASN-0047's `ExtendedReachableStateInvariants` (plus the composite-boundary trio and `ExtendedTransitionInvariants` P3) is accounted for across Groups (i)–(iii). The hard ones — S3★, S8★(c), CL-OWN, CL-UNIQ at positions where `Q ∩ X ≠ ∅` — are proven by an explicit source-correspondence argument, not "by similar reasoning." S8★(c) correctly routes through M12 with the full standing precondition set discharged at the post-state.
- **Boundary cases.** Empty post-state, deletion at start (the one configuration where D-MIN★ takes a non-vacuous `σ_d`-witness), deletion at end (`Π = ∅`), singleton interior, and non-singleton interior are each traced with the *route* of discharge made explicit. The worked content example deletes the middle of a single width-4 correspondence run (a_1..a_4 are I-adjacent), genuinely exercising run-splitting and the "no reconciliation across the gap" property — the partial-run case the rubric flags.
- **D9/D11.** The projection decomposition (unshifted Λ + bijection-shifted Π + bytewise S′) is correct, and the wp computations conjoin `enabled(DEL[d,σ])` with the pullback exactly as LP12a does, with the partial-deterministic negation identity `wp(S,¬Q) ≡ wp(S,true) ∧ ¬wp(S,Q)` correctly applied. Cardinality collapse `|project| − |project ∩ X|` checks out against the disjoint partition.
- **D10.** The composite-vs-atomic argument is sound (history-length difference of exactly two, robust to observational state collapse), the one-step vacuity of J0/J1★/J1'★ is proven per case, and — crucially — the ASN does **not** overclaim: it gives a concrete three-step counterexample showing DEL inside a multi-step composite can break composite-level J0. The LP-family extension catalogue covers LP2–LP21 plus LP-Sub/LP-Fin, dispatching each via D2/D3/D5/D6/D9/D11 or state-relativity.

I checked the previously-declined K.σ vocabulary finding: K.σ is present in the body's vocabulary list, so that inconsistency does not exist. I did not re-raise it.

## OUT_OF_SCOPE

### Topic 1: Full historical reconstruction and DELETE reversibility
**Why out of scope**: The Open Questions correctly defer recoverability mechanics, exact-arrangement recovery after re-insertion, and observer-relative reversibility to a versioning ASN. D2 + D5 supply the substrate; the mechanism is INSERT/version-creation territory, both excluded.

No META: the ASN defines abstract state, an operation, and its invariants, with implementation evidence (Gregory's two-knife, stale indices) explicitly framed as non-normative contrast. It has not drifted.

VERDICT: CONVERGED
