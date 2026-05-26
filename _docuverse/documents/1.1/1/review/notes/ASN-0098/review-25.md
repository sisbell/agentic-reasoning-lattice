# Review of ASN-0098

## REVISE

### Issue 1: M0 citation misapplied for documents not necessarily in dom(M)

**ASN-0098, "Boundary and Width Behaviour" section, LP-Fin proof and achievability section's descendant/ancestor cases**:

The LP-Fin proof states (in the sub-case analysis after establishing `#d ≤ #d_0`): "Admissibility further requires d to be T4-valid with zeros(d) = 2. By M0 (ASN-0093), d_0 is T4-valid with zeros(d_0) = 2; let z_1 < z_2 ≤ #d_0 denote d_0's two zero positions."

The descendant case states: "By M0 (ASN-0093) applied to both documents, d_0 and d' are T4-valid with zeros(d_0) = zeros(d') = 2. The prefix d_0 contributes exactly two zeros to d'..."

The ancestor case states symmetrically: "zeros(d') = zeros(d_0) = 2 by M0..."

**Problem**: M0 (DocumentTumblerWellFormed, ASN-0093) is `(A d ∈ dom(M) :: ValidAddress(d) ∧ zeros(d) = 2)` — it yields the structural property only for documents currently in dom(M). The argument's intended generality goes beyond this:

1. LP-Fin's precondition is `s ∈ F`, where F is defined by structural shape alone (`F = {a ∈ T : (E d ∈ T, s ∈ {s_C, s_L}, k ≥ 1 :: zeros(d) = 2 ∧ d satisfies T4 ∧ a = [d, 0, s, k])}`). F-elements need not have d_0 in dom(M).

2. The achievability section's descendant/ancestor analysis explicitly considers d' that may sit outside dom(M). The ASN says earlier in the same section: "We do not require d ∈ dom(Σ_e.M) — future K.σ transitions can register additional documents whose chains then become active, and the tightness condition must guard against those too."

For any d outside dom(M), M0 yields nothing. The structural property is supplied by F's definition or by ChainElementT4Validity (ASN-0093), neither of which requires dom(M) membership.

**Required**: Replace the M0 citations in LP-Fin's proof and in the descendant/ancestor cases with citations to F's structural definition (the explicit conjunct `zeros(d) = 2 ∧ d satisfies T4` in F's set-builder formula) or to ChainElementT4Validity (ASN-0093). The ASN already adopts the ChainElementT4Validity route earlier in the same section — "Equivalently, T4-validity of `a` follows directly from ChainElementT4Validity (ASN-0093) applied to any sub-allocator chain that would emit `a`" — so consistency points to that source. The conclusions are unchanged; only the citation requires correction.

## OUT_OF_SCOPE

None — the ASN's Open Questions section appropriately defers reverse-discovery, V-order/I-order coupling, link-to-link endset semantics, cross-document operation equivalence, and fork-composite link-subspace projection to future ASNs.

VERDICT: REVISE
