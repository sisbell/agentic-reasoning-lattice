# Review of ASN-0120

I checked the load-bearing derivations end to end: ML1's prefix-confinement (T5) and S3★ containment discharge, the recovery equation's two directions (LP-Fin Corollary traces, the TA5-SigValid shift/inc transfer, the TS3-composed S3 merge induction), the empty-resolution boundary, ML6's necessity-and-sufficiency for L3, the ValidComposite★ obligations (elementary preconditions at intermediate states, J0/J1★/J1'★ vacuity), the `a ∉ ran(M(d))` seating discharge, ML9's Facts (a)/(b) and the wp in both directions (including the `d' = d` boundary and the future-state extension), and the worked example's resolution trace and K.μ⁻ edit. All of these hold; the technical content is sound. What remains is one accretion finding under the anti-bloat classifier.

## REVISE

### Issue 1: MLop's consolidation scaffolding is document-organization narration, not specification
**ASN-0120, "The operation, consolidated (MLop)" and the residence section**: "Each piece of the contract was derived where it was needed — `wf` and `ρ` in the resolution section, the type precondition at ML6, `enabled` inside ML9's derivation, the seating rule and its depth convention in the residence section, the frame at ML10 — and a reader of the claims alone should not have to reassemble them. We therefore state the operation once, as a definition." Paired with the residence section's forward pointer: "the convention is carried, with the seating rule itself, into the operation's consolidated contract (MLop below)."

**Problem**: This is a use-site inventory plus a justification for the definition's existence — it explains *why MLop is in the document* rather than *what the operation is*. It matches the accretion patterns directly: a definition's introduction enumerating the sites its pieces came from instead of advancing the definition's meaning, and two passages in different sections managing the same consolidation relationship (a forward pointer in the residence section, a backward inventory at MLop). The operative content of MLop begins only at "`makelink(d, R₁, R₂, R₃)` is a partial operation on reachable states…"; everything before that sentence is prose the reader must skip to reach the contract. This is characteristic reviser drift around a paragraph added in a prior cycle.

**Required**: Open MLop with the definition itself: "**MLop (MakelinkOperation).** `makelink(d, R₁, R₂, R₃)` is a partial operation on reachable states, defined exactly on its enabling precondition …". Delete the derivation-site inventory and the "a reader of the claims alone should not have to reassemble them" sentence. In the residence section, reduce the forward pointer to a bare "(MLop)" citation on the depth convention.

## OUT_OF_SCOPE

(none — the two Open Questions, the empty non-type endset's meaning and link-subspace endset arguments, are correctly deferred rather than half-specified, and the ASN defines no claims for the scope-excluded operations)

VERDICT: REVISE
