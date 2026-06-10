# Review of ASN-0115

I checked the mathematics first. The core machinery is sound: the Confinement lemma (T5 + TumblerAdd) is correct; the `act` override is benign in the deep case (`#s > m_S(d)` forces `#v ≥ #s−1 > m_S(d) = #v`, an empty geometric intersection, so force-empty discards nothing); R6's no-interior-hole argument correctly reduces to a D-SEQ★ frontier tail; R7's repeatability proof handles the genuinely subtle point that `act`'s depth-compatibility branch reads the whole subspace state of `dⱼ`, not just the equated restriction; and R8's link-vacuity follows cleanly from CL-OWN + CL-UNIQ. Boundary cases (empty request, empty subspace, beyond-frontier, depth mismatch) are all covered. The wp analysis in R11 is non-trivial, and worked instances back R6/R8/R9/R10/R11. No rigor REVISE.

The findings are confined to residual prose accretion — which is what this review mode targets.

## REVISE

### Issue 1: R7 re-derives arrangement mutability already established in R4
**ASN-0115, R4 and R7**:
- R4: "resolution is against the *current* `Σ.M(dⱼ)`, which is mutable (K.μ⁻/K.μ⁺/K.μ~, ASN-0047; P3), so naming a version does not freeze it."
- R7: "A document's arrangement is the one mutable input: K.μ⁻, K.μ⁺, and K.μ~ (ASN-0047) edit `Σ.M(dⱼ)` in place, and P3 (ArrangementMutabilityOnly) marks `M` as the sole component that may lose information. RETRIEVEV therefore always resolves against the *current* `Σ.M(dⱼ)`, never a frozen snapshot…"

**Problem**: Both passages establish the identical core — the same three operations (K.μ⁻/K.μ⁺/K.μ~), the same P3, the same conclusion ("resolves against the current arrangement, not frozen"). R4 introduces it (to clarify that "current" means genuinely current under version naming); R7 re-derives it from scratch (to motivate repeatability's conditionality). The *applications* differ legitimately, but the K.μ+P3→mutable→current-not-frozen derivation is duplicated verbatim in substance. This is the "two paragraphs in different sections say the same thing" / "content relocated rather than removed" pattern — and the recent commit ("tighten version-naming mutability prose") suggests this is exactly the area still accreting.

**Required**: Condense R7's re-derivation to a back-reference, e.g. "the arrangement is the sole mutable input (R4; P3), so repeatability holds exactly when the consulted restriction is unchanged…" — keeping R7's repeatability-conditionality point, dropping the duplicate operation list and P3 re-explanation.

### Issue 2: R8 elaboration restates the box's disclosure point
**ASN-0115, R8** (prose after the two "*Why…*" proofs): "Each position resolves through `a` independently — whether delivered alone or alongside the other — so the shared home is established per-position, not jointly."

**Problem**: This sentence advances no reasoning the box has not already fixed. R8.ii states both positions resolve through `a` so `origin(a)` "is one and the same," and the box already states "The sharing is a fact of *resolution*, not of the delivered output… discloses nothing about the shared origin." "Per-position, not jointly" is a rewording of "fact of resolution, not output." The surrounding R8 elaboration ("Within content, identity is structural…"; "Nor does the operation merge…") carries the genuinely distinct points (identity-by-creation; no-dedup forced by R3); this sentence sits between them adding only a restatement the reader must skip past.

**Required**: Delete the sentence, or fold its one residual nuance into the box's existing disclosure clause.

I examined the two heavier defensive passages — the force-empty override rationale ("Force-empty is chosen over the geometric intersection because that intersection is discontinuous…") and the out-of-`{s_C, s_L}` "harmless rather than special-cased" paragraph — and judged them to earn their place: the first defends a genuinely counterintuitive definitional choice (overriding the natural geometric semantics) and contains the load-bearing "bites only there" lemma; the second discharges an admissible input the V-spec precondition does not exclude. Neither is flagged.

## OUT_OF_SCOPE

The topics a reader might expect but that belong elsewhere — inline provenance, permitted outright failure, dangling references under relaxed S3★, channel faithfulness, single straddling spans — are already deferred to the Open Questions and align with the stated scope exclusions. Nothing to add.

VERDICT: REVISE
