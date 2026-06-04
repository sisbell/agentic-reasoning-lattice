# Review of ASN-0101

## REVISE

### Issue 1: N1 and N3 are established as load-bearing "facts the derivation relies on," then explicitly declared unnecessary
**ASN-0101, D10, "DEL-neutrality facts" and "Boundary derivation"**: The note opens by claiming "The boundary derivation below relies on three facts ... we establish them once here and cite them by name (N1, N2, N3) in the induction." But the derivation that follows establishes P4★ and P7a "from four premises, *none specific to the composite's final step*" (IH, J0, J1★, P2), and the text then states: "The step-agnostic derivation above already closes using only the induction hypothesis and the coupling constraints (J0, J1★), so it needs nothing further." Only N2 is actually invoked ("P4a at Σ' holds by N2"). N1 and N3 are reached only in a sentence that says they "confirm it adds no obligation the derivation must absorb."

**Problem**: N1 and N3 are not used by the proof. N1 in particular carries a full Λ/Q/V_{S'} case-split establishing `Contains_C(Σ') ⊆ Contains_C(Σ)` that the step-agnostic argument renders dead weight. The framing "the boundary derivation relies on three facts" is contradicted by the derivation itself, which relies on one (N2). This is exactly the accreted-fact pattern: substantial established prose that the argument does not consume.

**Required**: Either delete N1 and N3 (keeping N2, which discharges P4a), or restructure the boundary derivation to actually depend on them. The opening framing must match what the proof uses.

### Issue 2: σ_d's structural form and verification are derived twice (D0 effect and "What shifts")
**ASN-0101, D0 *Effect***: "the tumbler `u := [S, 1, ..., 1, k − n]` ... satisfies `shift(u, n) = ... = [S, 1, ..., 1, k] = v` by TumblerAdd's componentwise definition. So `σ_d(v) = [S, 1, ..., 1, k − n]`."
**ASN-0101, "What shifts: closing the gap"**: "the inverse simply decrements the last component: `u = [S, 1, ..., 1, k − n]`. Verification: `shift([S, 1, ..., 1, k − n], n) = ... = v` ✓."

**Problem**: The "What shifts" opening re-derives, with the same checkmark verification, the σ_d formula that D0's effect already established. D1's justification correctly cites D0 ("by the D0 effect's existence argument") rather than re-deriving; the "What shifts" prose does not. Its only non-duplicative content is the `σ_d(r) = s` gap-closure observation and the implementation/no-reconciliation notes.

**Required**: Replace the re-derivation with a citation to D0's effect, retaining only the genuinely new `σ_d(r) = s` observation and the implementation notes.

### Issue 3: The worked example verifies D8, D9, and D11 before those claims are stated
**ASN-0101, "A worked example"**: "*Verification of D8* — D8 (stated in *What is preserved* below) ...", "*Verification of D9 (link projection)* — D9 (stated in *Link discoverability* below) ...", "*Verification of D11 ...* — D11 (stated in *Weakest precondition for discoverability preservation* below) ...".

**Problem**: Three verification subsections each defer forward to a downstream section where the claim being verified is actually defined. The reader must jump forward to learn what D8/D9/D11 assert before the example's checks mean anything — the forward-reference accretion pattern (multiple paragraphs deferring to downstream locations). The natural order is to state a claim, then verify it.

**Required**: Either move the worked example(s) after the D8/D9/D11 statements, or move the claim statements ahead of the example, so each verification follows the claim it exercises.

## OUT_OF_SCOPE

None. The note correctly defers INSERT/COPY/REARRANGE mechanics, version creation, and orphan re-discovery to the Open Questions and future ASNs.

VERDICT: REVISE
