# Review of ASN-0087

This is a mature, heavily-revised operation ASN. The correctness machinery is sound: I checked the decomposition `K.λ ; K.μ⁺_L`, the precondition reduction (`ℓ ∉ ran(Σ_mid.M(d))` via the S3★/S3★-aux chain), the invariant discharge (S2 two-part exclusion, CL-UNIQ, D-MIN★/D-SEQ★/D-CTG★ in both empty and non-empty cases), and the wp analysis (the reflexive disjunct is a genuine non-trivial case). Boundary cases — first link, subsequent link, empty non-type slots, reflexive endset, forward-reaching endset resurrection, `d_target = d` vs `≠ d` — are all handled. No correctness or depth gap found.

The findings are confined to the anti-bloat axis this note is flagged for: duplicated formal claims and restatement.

## REVISE

### Issue 1: M-NoContentEffect duplicates M-Frame
**ASN-0087, Claims table**: M-Frame states `Σ'.C = Σ.C`; M-NoContentEffect states "For every `a ∈ dom(Σ.C)`: `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`."
**Problem**: The M-NoContentEffect formal claim is logically entailed by M-Frame's `Σ'.C = Σ.C` (function equality already gives domain persistence and pointwise value preservation). Two table rows carry the same formal content. The substantive observation in "What Does Not Change" — that referencing is read-only because the endset stores spans, not bytes — is worth keeping as commentary, but it does not need a second formal claim that restates the frame.
**Required**: Drop the M-NoContentEffect formal claim (or fold its content into M-Frame), retaining only the read-only observation as prose.

### Issue 2: Atomicity section closes by restating its own opening
**ASN-0087, Atomicity**: closing sentence "A reader observing `Σ_mid` would see the link in `dom(L)` but not in `M(d)`."
**Problem**: This restates the section's opening bullets verbatim in different words — "`ℓ ∈ dom(Σ_mid.L)` … the link exists" and "`ℓ ∉ ran(Σ_mid.M(d))` — the link is not yet visible in any V-arrangement." Same content, said twice within one short section.
**Required**: Remove the closing restatement; the bullets already establish it.

### Issue 3: Value-permanence stated three times
**ASN-0087, "Permanence of the Recording" / M-Perm / "Permanence"**: value/coverage permanence appears in the "Permanence of the Recording" section (via LP13), again as claim M-Perm, and once more in the closing "Permanence" section ("what is permanent is the link's I-address and value").
**Problem**: The closing "Permanence" section's genuine new content is the *binding* mutability (`v_ℓ ↦ ℓ` fixed by K.μ~ clause (v), removable only by K.μ⁻); its recap of value-permanence overlaps the earlier section and M-Perm. The "two paragraphs say the same thing" pattern.
**Required**: In the closing "Permanence" section, reference the established value-permanence rather than re-deriving it, and let the section carry only the binding-mutability result that is its actual contribution.

## OUT_OF_SCOPE

The six Open Questions (forward-reaching endset well-formedness, deferred-consistency model, intermediate-state visibility protocol, never-allocated type references) are correctly deferred — they concern protocol-layer or future-ASN territory, not defects here.

VERDICT: REVISE
