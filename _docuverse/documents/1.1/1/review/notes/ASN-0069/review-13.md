# Review of ASN-0069

The ASN derives CREATENEWVERSION rigorously: identity allocation by sub-allocator, content sharing by transclusion, source isolation by frame composition, and transitive identity through fork chains. Most claims have detailed derivations with explicit citations; edge cases (empty source via V7, sibling forks via V10, chain forks via V11) are addressed; design commitments beyond J4 (V4, V4b literal V-position inheritance; V7 K.δ-alone composite) are explicit and justified.

## REVISE

### Issue 1: V11 stated with a stronger premise than the derivation requires
**ASN-0069, V11**: The premise reads "no transition between consecutive fork composites modifies *any source's arrangement*" and a subsequent Remark observes "A tightened premise — no transition... modifies any chain source's *content-subspace* arrangement — would yield the same conclusion."
**Problem**: The conclusion is content-subspace-scoped, the derivation reads only `V_{s_C}(d^{i-1}_new)` and `M^{i-1}(d^{i-1}_new)|_{V_{s_C}(d^{i-1}_new)}` at each step's pre-state, yet the property is stated with a premise that forbids link-subspace and other non-load-bearing modifications. Downstream consumers will either over-constrain their callers or have to re-derive V11 with the looser hypothesis.
**Required**: State V11 with the tightened premise as the primary form. The simplicity advantage is small; correctness of the bounds belongs in the property itself.

### Issue 2: V8b non-monotonicity discussion does not justify exhaustiveness
**ASN-0069, V8b**: "subsequent K.μ⁻ on either side may move `v` out... and subsequent K.μ⁺ may re-install a binding...; K.μ~ may remap an image. The operational mechanics... are properties of K.μ⁻, K.μ⁺, and K.μ~ as defined in ASN-0047, not of the fork operation."
**Problem**: The list enumerates K.μ⁻, K.μ⁺, K.μ~ as the transitions that affect `Π_g`, but does not state that no other elementary transition can change it. K.α (preserves arrangements), K.λ (preserves arrangements), K.μ⁺_L (extends link subspace only, leaves `V_{s_C}` untouched), K.ρ (preserves arrangements), K.δ (initializes new entities' arrangements to ∅) all need to be excluded for the list to be exhaustive. Without the exclusion, the claim "Π_g may shift" is informally consistent but formally incomplete.
**Required**: One sentence stating that the other elementary transitions (K.α, K.λ, K.μ⁺_L, K.ρ, K.δ) leave `Corr_g` invariant by their frame conditions on `M`, so `Π_g` shifts only via K.μ⁻ / K.μ⁺ / K.μ~ on d_src or d_new.

### Issue 3: V0 Effects-table annotation for the R' set equality uses awkward notation
**ASN-0069, V0**: "R' = R ∪ {(a, d_new) : a ∈ ran(M'(d_new))} (V9, with set equality by K.δ frame R¹ = R + K.μ⁺ frame R² = R¹ + K.ρ × n cumulative effect)"
**Problem**: The "+" in "R¹ = R + K.μ⁺ frame R² = R¹ +" reads as if it were arithmetic. The intended meaning is sequential composition of frame conditions across elementary steps. A careful reader parses this only by referring back to the verification section.
**Required**: Rephrase as "R¹ = R (K.δ frame), then R² = R¹ (K.μ⁺ frame), then R^{2+n} = R² ∪ {(a, d_new) : a ∈ ran(M²(d_new))} (K.ρ × n cumulative)" or similar with sequential connectives.

### Issue 4: V4b's derivation forward-references V0
**ASN-0069, "The Arrangement Layer", V4b derivation**: "the K.μ⁺ phase of V0 adds exactly the positions of V_{s_C}(d_src) — this domain restriction is V4's design commitment of this ASN..."
**Problem**: V4b is derived in §"The Arrangement Layer" but cites "the K.μ⁺ phase of V0" before V0 is formally defined in §"The Fork Composite". The reasoning is circular at the textual level: V4b is presented as derived from V0's effects, but V0's Effects table cites V4b. The substantive content is correct, but the presentation order makes the design commitment chain unclear.
**Required**: Either (a) reorder so V0 is defined first with V4/V4b stated as part of its effects rather than derived, or (b) make explicit that V4b is itself a design commitment of V0, and V0's Effects "M'(d_new)(v) undefined for v ∉ V_{s_C}(d_src)" is the primary formulation with V4b as a restatement.

## OUT_OF_SCOPE

The ASN's own Open Questions section catalogs deferrals appropriately (concurrent forks, descendant discoverability, snapshot vs living forks, forks of transcludents, version-space coherence, V-stream depth renumbering, fork-then-delete sequencing). These are well-scoped.

### Topic: Activation point of A_v(d_src)
**Why out of scope**: ASN-0047's SubAllocatorAxiom explicitly activates A_C(d) and A_L(d) at d's K.δ event but does not give an analogous activation axiom for A_v(d). ASN-0069 reasonably uses A_v(d_src) as defined in the Allocator hierarchy. The activation gap is a foundation issue (ASN-0047), not a defect in ASN-0069.

VERDICT: REVISE
