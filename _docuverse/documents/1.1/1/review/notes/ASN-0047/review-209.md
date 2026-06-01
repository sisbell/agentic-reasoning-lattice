# Review of ASN-0047

This ASN is mature; its substantive transition arguments, worked examples, and per-state/composite-boundary invariant split hold up under scrutiny. The remaining issues are the meta-prose / reviser-drift patterns the `review-mode.anti-bloat` classifier directs me to surface. They are not size/splitting concerns (those were previously declined) — they are localized prose that the reader must skip past to follow a claim.

## REVISE

### Issue 1: S8★ definition — non-consumer inventory and non-maximality essay
**ASN-0047, *Amendments to existing transitions*, S8★ (per-subspace span decomposition)**: "S8★ asserts only the *existence* of a per-subspace run decomposition, not its maximality or uniqueness; the trivial length-1 decomposition used for `S8★(s_L)` below is demonstrably non-maximal whenever consecutive link positions are shift-aligned (e.g. `[s_L, 1] ↦ ℓ₁`, `[s_L, 2] ↦ ℓ₂`...). No property in this ASN consumes uniqueness: D-SEQ★ derives from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a (not from S8★), and every S8★ appeal in the preservation argument discharges to the existence of conditions (a)/(b) alone."
**Problem**: This is a use-site (non-consumer) inventory plus a defensive justification for dropping condition (c) — it explains *why the property is weakened and that nothing depends on the dropped part*, rather than advancing what S8★ says. The worked non-maximality example exists only to motivate the omission. This is exactly the flagged "definition's introduction enumerates downstream consumers" pattern.
**Required**: State S8★ as requiring conditions (a)/(b) only, established per-subspace by the two named routes (ASN-0036 S8 on the content projection; trivial length-1 on the link projection). Drop the non-consumer survey and the non-maximality illustration; if the absence of (c) needs a one-line note, make it one line.

### Issue 2: Contains(Σ) definition — use-site inventory and forward pointer
**ASN-0047, *Coupling and isolation*, Definition (Current containment)**: "The unscoped relation is used below only in the reordering-isolation argument (J3) and the staleness discussion; the provenance bound is carried not by `Contains(Σ)` but by its content-subspace restriction `Contains_C`, defined next, which P4★ constrains."
**Problem**: A definition's body should define, not inventory its own downstream uses. "Used below only in J3 and the staleness discussion" is a use-site catalogue; "the provenance bound is carried not by Contains(Σ) but by Contains_C, defined next" is a forward pointer that rots as sections move.
**Required**: Delete the sentence. Contains(Σ) is used where it is used; the distinction from Contains_C belongs at the P4★ definition (which already makes it), not embedded in the Contains(Σ) definition.

### Issue 3: P4a — framing essay in a definition/discharge slot
**ASN-0047, P4a definition box**: "We deliberately avoid the stronger 'past containment' framing. ValidComposite★ does not order the matching K.μ⁺ before the recording K.ρ, so the witnessing state Σ_k may be the present state Σ_n itself..." and the Class (b) discharge: "The 'transient failure' thus describes a real observable mid-composite state; restoration is structural (Σ' carries the witness), not temporal (no earlier state need carry it)."
**Problem**: These are essay paragraphs justifying a framing choice rather than stating or discharging the property. The formal content — "the witness may be Σ' itself" — is already carried by the existential ranging over `{Σ₀,...,Σ_n}` in the formula. The "structural not temporal" elaboration restates the same point a third time across the definition box and the discharge.
**Required**: Keep the formal statement (existential over trace states) and the one-line discharge (J1'★ supplies the witness at Σ'). Remove the "deliberately avoid past containment" and "structural not temporal" commentary, which says nothing the quantifier does not already say.

## OUT_OF_SCOPE

None. The substantive content stays within state, operations, and invariants.

VERDICT: REVISE
