I read the foundation exports (TumblerAdd, T1, T12, ZPD, TumblerSub, Divergence, D1, NAT-order, NAT-addcompat) and then walked ASN-0053 as a system: S0 → WF → S6 → S2 → S11, plus the cross-claim precondition chains.

The mathematical core is sound. I walked the cases and confirm:

- **S0** composes the two ≤/<-chains by the four-case and two-case unfolding of `a ≤ b ≡ a < b ∨ a = b`, every branch reducing to T1(c) or substitution of equals; carrier membership is carried, not re-derived. Sound.
- **WF** discharges D1's fifth precondition `divergence(s,r) ≤ #s` by eliminating T1 case (ii) under `#s = #r` (successor-inequality + transitivity + irreflexivity drive `#s+1 ≤ #s` to absurdity), places `(s,r)` in Divergence case (i) at `k ≤ #s`, identifies `k = divergence(s,r)` by uniqueness, and reads `Pos`, `actionPoint = k ≤ #(r⊖s) = #s`, and length off TumblerSub. The five D1 preconditions and TumblerSub's positive-branch guard (`zpd(r,s)` defined, via Divergence symmetry + ZPD Relationship-to-Divergence) are all met. Sound.
- **S6** instantiates TumblerAdd's preconditions at `(s,ℓ)` before reading off `#reach = #ℓ = #s`. Sound.
- **S2** reduces to T12(b) `s ∈ span(s,ℓ)` under matching preconditions. Sound.
- **S11**: reach-tumblers placed in T via TumblerAdd before the boundary test; boundary characterization (`start(α) ≤ start(β)`, `reach(β) ≤ reach(α)`) correct, including the `reach(α) ∈ ⟦β⟧` contradiction; the (L)/(M)/(R) partition is exhaustive and disjoint, `(M) = ⟦β⟧` exactly under containment; λ and ρ discharge WF's carrier/order/length preconditions (ρ's `reach(·) ∈ T` from TumblerAdd, length via S6 + level_compat); the tightness argument correctly hinges on `reach(λ) = start(β) < reach(β) = start(ρ)` (gap real **because S2 forces β non-empty**) and on S0-convexity of any single `γ`. The worked instance ([1,3]/[1,5]) checks. Sound.

No correctness defect, missing case, broken precondition chain, or shifted definition. What I did find is reviser-drift / essay-in-structural-slot prose, plus one unstated lemma behind a parenthetical.

### S2 precondition prose refutes a misreading the typing already excludes
**Class**: OBSERVE
**Foundation**: T12 (preconditions `actionPoint(ℓ) ≤ #s`)
**ASN**: S2 body — "This second condition is a comparison of natural numbers … not of the end offset s ⊕ ℓ, which is a tumbler"; and Preconditions — "not the type-incoherent comparison of the tumbler s ⊕ ℓ against #s."
**Issue**: `actionPoint(ℓ) ≤ #s` is a ℕ-comparison on its face; `s ⊕ ℓ` never appears in the condition. The prose constructs a wrong reading (comparing `s ⊕ ℓ` to `#s`) and refutes it. This is the reviser-drift pattern "a paragraph imagines a case the precondition already excludes," appearing in both the proof body and a structural slot.
**What needs resolving**: State the precondition as `actionPoint(ℓ) ≤ #s` (`actionPoint(ℓ) ∈ ℕ`) without the contrast against an offset comparison no reader proposes.

### S0 Axiom/Depends slots explain what T1 does *not* export rather than stating the axiom
**Class**: OBSERVE
**Foundation**: T1 (postcondition (c), abbreviation `a ≤ b ≡ a < b ∨ a = b`)
**ASN**: S0 *Axiom*: "The non-strict compositions the proof needs … are *not* T1 exports; each is derived in the proof by case analysis…"; *Depends*: "it does not cite a ≤-transitivity, which T1 does not export."
**Issue**: The Axiom slot should record the ground fact T1 supplies (strict `<`, transitivity (c), the `≤` abbreviation). Instead it narrates the proof technique and emphasizes an absence (no exported ≤-transitivity). This matches "new prose around an axiom explains why the axiom is needed rather than what it says," and the Depends entry repeats the same absence-inventory.
**What needs resolving**: Reduce the Axiom slot to what T1 exports; let the proof body, not the contract slot, carry the "derived not cited" reasoning.

### S11 Axiom slot is a full prose re-derivation; redundant TumblerAdd/S6 citation is defended in prose
**Class**: OBSERVE
**Foundation**: TumblerAdd (carrier + result-length), S6 (length consequence)
**ASN**: S11 *Axiom* (the multi-sentence paragraph re-deriving the boundary characterization, the S0 bracketing, and WF discharge) and the Depends note "The proof names both identities in their own right — rather than only through S6's packaged length consequence — so TumblerAdd is cited here explicitly; it is the same foundation S6 is grounded on."
**Issue**: The Axiom slot restates the proof body in full (essay content in a structural slot). Separately, `#reach(σ) = #start(σ)` is sourced both from S6 (its packaged consequence) and from TumblerAdd raw, and the duplication is justified with defensive prose rather than removed — a use-site inventory that degrades the contract.
**What needs resolving**: Collapse the Axiom slot to the ground facts consumed (TumblerAdd carrier `a⊕w ∈ T`, result-length `#(a⊕w)=#w`); pick a single citation path for `#reach(σ)=#start(σ)` (S6 already packages it) and drop the meta-justification for citing both.

### S11 case (a) labels the empty-difference condition "α = β" without the width-uniqueness it presupposes
**Class**: OBSERVE
**Foundation**: D1 (round-trip / subtraction uniqueness)
**ASN**: S11 proof case "(a) Both boundaries coincide (α = β): difference is empty — 0 spans" and the postcondition "its cardinality is 0 when α = β, 1 when exactly one boundary coincides, and 2 when neither coincides."
**Issue**: The actual cardinality-0 condition the proof establishes is *both boundaries coincide* (`start(α)=start(β) ∧ reach(α)=reach(β)`, equivalently `⟦α⟧=⟦β⟧`). The cases for 1 and 2 are phrased in boundary-coincidence terms; case (a) silently switches to span-equality `α = β`. That equivalence holds for well-formed level-uniform spans (width is recoverable as `reach ⊖ start` via D1, so equal endpoints force equal width), but the claim does not derive it — the parenthetical presupposes width-uniqueness. The phrasing is also inconsistent with the other two cases.
**What needs resolving**: State the 0-cardinality condition in the same boundary-coincidence language as the 1/2 cases (or `⟦α⟧=⟦β⟧`); if span-equality `α=β` is asserted, cite the D1-grounded width-uniqueness that licenses it.

VERDICT: OBSERVE