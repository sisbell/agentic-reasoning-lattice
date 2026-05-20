# Review of ASN-0047

## REVISE

### Issue 1: D-CTG★/D-MIN★ strengthening lacks in-body justification

**ASN-0047, *Amendments to existing transitions* (D-CTG★/D-MIN★)**: "ASN-0036's D-CTG and D-MIN have a link-subspace exemption accommodating Nelson's tombstoning design (LM 4/9). This ASN introduces strengthened forms D-CTG★ and D-MIN★ that apply uniformly across both subspaces."

**Problem**: The strengthening removes the very exemption that Nelson's design relies on (LM 4/9 tombstoning), and the Open Questions section even acknowledges that "withdrawing an interior link requires withdrawing every link allocated after it." Yet the body proceeds with the strengthened form without justifying why uniform contiguity is the right choice. This is a substantive deviation from the source design that downstream K.μ⁻ shape derivations, J1★/J1'★ formulations, and the verification matrix all depend on. If a future ASN reverts to the exemption, much of this ASN would need revision.

**Required**: Provide in-body justification for the strengthening — argue that L12 (link immutability) + reverse-index discovery captures Nelson's tombstoning intent without the contiguity exemption, OR retain the exemption and adapt the K.μ⁻ admissible-shape derivation accordingly. Deferring this to Open Questions hides a load-bearing design choice.

### Issue 2: FrontierEquivalence premise (i) mislabels its foundation source

**ASN-0047, *Elementary transitions* (FrontierEquivalence lemma)**: "(i) *T10a per-`(t, 0)` uniqueness:* within `t`'s own sub-allocator chain, the `(t, 0)` pair fires at most once across the system history."

**Problem**: ASN-0034's T10a per-`(t, k')` uniqueness axiom is stated for k' ∈ {1, 2} (T2 child-spawning); k = 0 is the T1 sibling-increment regime. The at-most-once property for (t, 0) is *not* a direct T10a axiom — it follows from T10a's chain structure (`dom(A) = {tₙ : n ≥ 0}`, `tₙ₊₁ = inc(tₙ, 0)`) plus P1's E-monotonicity plus the operational precondition `inc(t, 0) ∉ E`. The "T10a per-(t, 0) uniqueness" labeling suggests a direct axiom that doesn't exist.

**Required**: Re-label as "T10a chain-advancement at (t, 0)" (or "T10a chain enumeration injectivity at (t, 0)"), and cite the derivation chain (T10a chain structure + P1 + precondition). The substance of FrontierEquivalence is correct; only the citation needs adjustment.

### Issue 3: K.μ~ matrix cells implicitly invoke full-clearance form

**ASN-0047, Class (a) verification matrix, K.μ~ column**: Entries say "inherits via K.μ⁻ + K.μ⁺ decomposition" without naming which decomposition.

**Problem**: The K.μ~ Decomposition section establishes that *multiple* admissible decompositions exist (partial-suffix forms at varying cuts, plus the universally-applicable full-clearance form). The text states the convention — "every K.μ~ verification argument in this ASN that does not name a specific cut point invokes the full-clearance form" — but the matrix itself doesn't reference this. A reader checking the matrix in isolation cannot tell which decomposition is being invoked, particularly for cells like D-CTG★/D-MIN★ where the partial-suffix admissibility condition matters.

**Required**: Add a matrix preamble note (alongside the existing "Frame entries against link-store invariants" note) stating that K.μ~ matrix entries invoke the full-clearance form, with reference to the Decomposition section's convention.

### Issue 4: K.μ⁻ admissible shape derivation under D-SEQ★ — non-circularity argument is sound but reads as circular

**ASN-0047, *K.μ⁻ admissible contraction shape*** : "D-SEQ★ applied at the post-state gives `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` for some `n'_S ≥ 1` directly. (*Non-circularity.* D-SEQ★ at Σ' here is the *local* D-SEQ★ derivation at the K.μ⁻ post-state...)"

**Problem**: The non-circularity parenthetical correctly identifies the dependency: K.μ⁻'s preconditions establish D-CTG★/D-MIN★/S8a/S8-depth/S8-fin at Σ', from which D-SEQ★ at Σ' is *re-derived* (not inherited). But the matrix entry for K.μ⁻ under D-CTG★/D-MIN★ says "per-subspace suffix shape forced by D-CTG★ + D-MIN★ + D-SEQ★ at the post-state" — listing D-SEQ★ as a *premise* for the suffix shape, while D-SEQ★ is itself derived from D-CTG★/D-MIN★/S8-related at Σ'. The matrix entry could mislead a reader into thinking D-SEQ★ is independently asserted at Σ' rather than re-derived.

**Required**: Clarify in the matrix entry (or in a footnote) that D-SEQ★ at Σ' is the *local re-derivation* from D-CTG★/D-MIN★/S8-related preconditions, not an independent post-state assertion. The depth-2/depth-≥3 D-SEQ★ derivation paragraph fires at every reachable state from the same per-state inputs — this should be visible from the matrix entry, not buried in a separate paragraph.

### Issue 5: K.μ~ admissibility clause (i) retention without operational role

**ASN-0047, *Decomposition of K.μ~***: "*Clause (i) is redundant given the other constraints and the inductive hypothesis*... Clause (i) is retained for definitional clarity — marking each step's S8a obligation explicitly rather than leaving it as a derived consequence — but it carries no independent verification burden."

**Problem**: The ASN simultaneously declares clause (i) redundant and retains it as part of K.μ~'s admissibility. This creates an awkward situation: a verifier checking admissibility might re-prove clause (i) thinking it's independent, when in fact the inductive hypothesis suffices. The "definitional clarity" justification is weak — the same clarity could be achieved by a derivation paragraph rather than a redundant clause.

**Required**: Either (a) remove clause (i) from admissibility and document the S8a postcondition as a derived consequence in K.μ~'s effect description, or (b) explicitly re-state in the K.μ~ definition that clause (i) is provably redundant and present for exposition only, so verifiers don't waste effort discharging it.

## OUT_OF_SCOPE

None — the ASN's scope decisions (deferring named operations, authority model, POOM internals, replication, etc.) are appropriate for an elementary-transition specification.

VERDICT: REVISE
