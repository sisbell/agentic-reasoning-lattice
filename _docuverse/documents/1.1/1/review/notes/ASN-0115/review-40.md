# Review of ASN-0115

The note is on-track: it specifies a pure query's semantics (R1–R11) as state-relative obligations any implementation must meet, grounded in the strand substrate. No drift. But the freshly-added depth-incompatible V-spec rule has been bolted onto the prose without being integrated into the operative definition of `act` or into the R6 proof that is supposed to house it. That leaves a definition contradicting itself and a proof that excludes the very case the rule was created for.

## REVISE

### Issue 1: `act(ρ, Σ)` is defined twice with conflicting content

**ASN-0115, "What a spec-set is, and what delivery is"** gives the operative definition:

> "`act(ρ, Σ) = dom(Σ.M(d)) ∩ ⟦σ⟧`"

unconditionally. But the V-spec definition earlier states an override:

> "by R6's discipline we take such a depth-incompatible spec to have empty active set (`act(ρ, Σ) = ∅`, overriding the geometric `dom(Σ.M(d)) ∩ ⟦σ⟧` lest a now-too-shallow start capture deeper content the citation never named)"

**Problem**: For a spec that was depth-compatible at minting but has `#s ≠ m_S(d)` at the consulting state `Σ` (reachable: `m_S(d)` re-pins after full clearance, ASN-0047), the two definitions disagree. A too-shallow start gives a *non-empty* geometric intersection — e.g. `s = [1,2]`, `s ⊕ ℓ = [1,7]` admits the deeper position `[1,3,4] ∈ ⟦σ⟧`, so if `d` binds depth-3 content there, `dom(Σ.M(d)) ∩ ⟦σ⟧ ≠ ∅` — while the override demands `∅`. Every downstream user of `act` (R0's `deliver`, `item` totality, R3, R6, R7's proof) consumes the formal box, i.e. the geometric form the override is meant to suppress. The operation's output is therefore undefined on exactly the case the new rule addresses.

**Required**: State `act` once, with the case split made operative: `act(ρ, Σ) = dom(Σ.M(d)) ∩ ⟦σ⟧` when `ρ` is depth-compatible at `Σ`, and `∅` otherwise. Then re-derive `item` totality, R3, R6, R7 against that operative definition (R7's "act and the resolved addresses agree position-for-position" silently computes the geometric form and must be checked against the overridden one).

### Issue 2: R6's guarantee and proof do not cover depth-incompatible specs

**ASN-0115, R6 (SilentGapFiltering)**: the box promises

> "Delivery succeeds and returns the items for the bound positions; the unbound positions are represented by their absence."

with "unbound" defined geometrically (`v ∈ ⟦σⱼ⟧ \ dom(Σ.M(dⱼ))`). The proof then case-splits and asserts:

> "Otherwise `V_S(d) ≠ ∅`, and the V-spec definition's depth-compatibility conjunct gives `#s = m_S(d)` ... which is the case the remainder of this argument analyses."

**Problem**: The note itself establishes (V-spec definition) that at a downstream state `V_S(d) ≠ ∅` can coexist with `#s ≠ m_S(d)`. In that case the depth-compatibility conjunct does *not* give `#s = m_S(d)` — it holds at minting, not at `Σ` — so the proof's `Otherwise` branch is invalid for the case the override exists to handle, and the remainder analyses only depth-compatible specs. Worse, the box's promise is *false* for depth-incompatible specs: a position in `dom(Σ.M(d)) ∩ ⟦σ⟧` is "bound" by R6's own geometric definition, yet the override (Issue 1) refuses to deliver it. So R6 both leaves a case unproven and asserts a guarantee the override contradicts. "By similar reasoning" / silent case-omission is exactly what the standard forbids.

**Required**: Either (a) restrict R6's sharpening explicitly to specs depth-compatible at `Σ` and discharge the depth-incompatible case separately (showing the no-interior-hole / terminal-overrun claims hold — vacuously or otherwise — once `act = ∅`), or (b) reconcile "returns the items for the bound positions" with the override so that "bound" means the overridden `act`, not the geometric intersection. Whichever is chosen, the `V_S(d) ≠ ∅ ∧ #s ≠ m_S(d)` case must be shown, not assumed away.

### Issue 3: the depth-incompatible rule is asserted by a forward reference R6 does not honor

**ASN-0115, V-spec definition**: "by R6's discipline we take such a depth-incompatible spec to have empty active set."

**Problem**: R6 houses no such discipline. R6 states silent gap filtering and the no-interior-hole sharpening, and its proof explicitly *assumes away* depth-incompatibility (`#s = m_S(d)`). Meanwhile R6's proof defers back to "the V-spec definition's depth-compatibility conjunct." The override (`act = ∅`) thus lives only in the V-spec prose, while being attributed to R6, while R6 defers to the V-spec definition — a circular deferral in which the cited rule exists at neither endpoint. A reader chasing "R6's discipline" to find the override's statement and justification finds only the assumption that the case never arises.

**Required**: State the override and its justification ("lest a too-shallow start capture deeper content") once, at the operative definition of `act` (Issue 1), and drop the "by R6's discipline" attribution. R6 may then *cite* that definition rather than be cited as its source.

### Issue 4 (anti-bloat): the "co-delivery discloses nothing" point is restated three times

**ASN-0115, R8 box / following paragraph / Synthesis**. The box: "discloses nothing about the shared origin"; the immediately following paragraph: "Co-delivery therefore establishes nothing about the relation between the two that two separate single-span deliveries would not: it carries no information a pair of isolated requests lacks"; the synthesis: "yet co-delivery discloses nothing about the sharing (R8)."

**Problem**: The box and the paragraph that follows it carry the same claim in different words (the paragraph adds a one-clause justification but no new claim). In a note explicitly flagged for forward-reference/meta-prose accretion, a claim stated in its box, restated in its discussion, and recapped in the synthesis is the redundancy pattern.

**Required**: Keep the justification ("`deliver` performs no comparison... resolves through `a` independently") once; delete the restated assertion so the box's claim is not paraphrased back-to-back.

## OUT_OF_SCOPE

### A single span straddling the content/link subspace boundary
**Why out of scope**: The note confines V-specs to ordinal-level spans (Confinement lemma keeps each within one subspace) and correctly defers the straddling case to its Open Questions. Designating both subspaces is achieved by composing per-subspace specs, not by one span — this is a future ASN, not a gap here.

META: not applicable — the ASN remains squarely a state-relative specification of a delivery operation; its defects are incompleteness around a newly-added rule, which is fixable.

VERDICT: REVISE
