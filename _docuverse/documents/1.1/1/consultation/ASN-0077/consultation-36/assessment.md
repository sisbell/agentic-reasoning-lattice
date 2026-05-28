# Channel Assignment — ASN-0077 review-36

**Date:** 2026-05-28 10:35

## Issue 1: Combined K.μ⁺ + K.μ⁺_L chain claim is hand-waved
Reason: The fix is derivable from the ASN alone. The combined induction selects O11 or O11' at each M(d)-modifying step (per the step's transition kind) and O7 at non-M(d)-modifying steps; well-formedness preservation along the chain follows from the same arguments used in O11★/O11'★. All machinery is already present.

## Issue 2: Singleton I-span "squeeze" argument is too terse
Reason: The fix is derivable from the ASN alone. The expansion needs only T1 case analysis (cited from ASN-0034), prefix-copy region equality from TumblerAdd (already invoked earlier in the same case analysis), and T0 discreteness — all foundation-level facts the ASN already cites.

## Issue 3: Well-formedness preservation at Σ' is implicit in O11/O11'
Reason: The fix is derivable from the ASN alone. The corollary requires only: precondition (iii) preserved by domain growth (K.μ⁺/K.μ⁺_L are extensions), depth invariance (already shown in O11 sub-case (a) and O11' sub-case (b)), and precondition (vi) preserved by combining these — all argument fragments already present in the existing proofs.

## Issue 4: K.μ~ scenario admissibility insufficiently verified
Reason: The fix is derivable from the ASN alone. The verification needs K.μ~'s admissibility clauses from ASN-0047 (already cited as K.μ~-FIX and clause (ii) in the existing text); the remaining work is per-invariant checking against the specific bijection π, which is mechanical given the spec.

## Issue 5: O0(b) cumulative derivation buries the citable conclusion
Reason: The fix is derivable from the ASN alone. The closure conclusion is already established inside O0(b); the revision is purely structural — extract the existing argument as a stand-alone labeled lemma so it becomes citable.

## Issue 6: Missing labeled claim on K.μ⁻ and K.μ~ failure modes for V-span
Reason: The fix is derivable from the ASN alone. The K.μ⁻ admissibility-loss condition is already exhibited in the worked example (precondition (vi) failing post-contraction), and the K.μ~ non-preservation counterexample is fully worked out at Σ₁ → Σ₁'; the revision labels these existing constructions as formal negative claims.
