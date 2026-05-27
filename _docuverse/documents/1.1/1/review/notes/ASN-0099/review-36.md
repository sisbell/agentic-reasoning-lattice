# Review of ASN-0099

## REVISE

(No REVISE items found.)

After careful review, I find ASN-0099 unusually rigorous. Each claim is derived with an explicit chain rather than checkmark or "by similar reasoning." Boundary cases (empty query, empty link store, empty constraint set, empty constraint target, empty scope, empty endset) are all explicitly addressed. The worked example exercises 11 distinct queries against the formal claims, with verification paragraphs for F2, F3, F5, F6, F8, F9, F9★, F9★-cor, F10, F11, F13, F15, F17, F19, F20.

The load-bearing methodological commitment (A1b's closed-world reading of the substrate effect-clause convention at K.μ⁺, K.μ⁻, K.ρ) is handled with exemplary care: explicitly labeled as convention-grounded rather than derived, with convergent (non-constitutive) grounding from Nelson's design intent and Gregory's implementation, and an explicit "Why not a substrate revision" paragraph that addresses the alternative of foundation-level axiomatization. The A1 / A1a / A1b partition surfaces the interpretive commitment at every citation site.

Foundation citations (ASN-0034, ASN-0036, ASN-0043, ASN-0047, ASN-0058, ASN-0093, ASN-0098) are all to verified foundations; no non-foundation cross-references appear. The Open Questions section appropriately frames future work (phantom address semantics, distributed consistency, FOLLOWLINK inverse direction, access control composition) rather than treating these as gaps in this ASN.

Verification chains I spot-checked: F8's determinism chain (partial-function equality → L6 component-wise tuple equality → coverage determinism → predicate equality → set extensionality) is complete. F10a's case (i)/(ii) anchor lifting correctly handles the zero-count balance argument (M0's `zeros(d) = 2` forces appended components ≥ 1 under proper prefix). F4's realizability discharge correctly factors through K.λ's free endset choice (per L4 and K.λ's well-formedness preconditions), with the address `a` determined by K.λ's chain discipline rather than independently chosen. Query 11's cross-step precondition transfer (K.μ⁻ then K.μ⁺_L) correctly carries `ℓ ∈ dom(L)`, `origin(ℓ) = d_a`, `ℓ ∉ ran(M(d_a))`, and D-MIN★ admissibility across the intermediate state via A1b.

## OUT_OF_SCOPE

(No items flagged. The ASN's "What We Have Not Specified" section and "Open Questions" appropriately catalog future-work topics — phantom address semantics, multi-server consistency, FOLLOWLINK/RETRIEVEENDSETS inverse direction, access control composition, audit witnesses, timing bounds, combined filtered-and-scoped form. The Scope-listed exclusions (INSERT, DELETE, COPY, REARRANGE mechanics, version creation, replication) are not specified; the ASN cites K.μ⁺/K.μ⁻/K.μ~/K.δ only as foundation operations whose mechanics are defined elsewhere.)

VERDICT: CONVERGED
