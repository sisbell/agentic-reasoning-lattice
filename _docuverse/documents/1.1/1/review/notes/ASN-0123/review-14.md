# Review of ASN-0123

This is an unusually rigorous note. The derivation-from-guarantees structure (G1–G3), the careful avoidance of B2's global precondition in `nextv`, the full four-case induction in VN-B1, the SA antichain proof, and the severance theorem (V9) are all complete and correct as far as I can verify them. The proofs do not hand-wave, the edge cases I tested (empty source `n=0`, first vs. subsequent fork, node-tier owner, fork-of-fork, shared/transcluded content, cross-owner) are all covered, and every cited ASN is a foundation. I found no correctness bug, no missing case, and no improper cross-reference. One depth gap remains.

## REVISE

### Issue 1: The headline guarantee — link carry-through — is never demonstrated against a concrete scenario

**ASN-0123, V10 (and V13, V9w)**: The note's introduction promises to prove "the carry-through of links anchored to content the version transcludes." V10 establishes the biconditional `project(a, i, v, Σ') ≠ ∅ ⟺ coverage(Σ.L(a).eᵢ) ∩ A ≠ ∅`, and V13/V9w establish the provenance and dual-witness machinery.

**Problem**: The note *does* verify its key postconditions concretely — but only the **addressing** ones. The VD worked instance (`d = 1.1.0.1.0.1` → `v₁, v₂, w`) checks V4 (trunc/ancestry), V5 (ranks), V6 (chain), V7 (base detection); the `modify_original_after_version` golden test grounds V2/V11; the GRANORGL/DOCISPAN evidence grounds V1/V9w. But the substantive **content-connectivity** claims — V10 (refractive links), V13 (the provenance rows `A × {v}`), and the *numeric* form of V9w's dual provenance — are established purely by abstract LP12 instantiation and coupling-citation, with *no* specific link, content arrangement, or provenance trace anywhere. The worked instance contains no content addresses, no arrangement, and no links at all; the implementation-evidence section discusses links only through the "strap between bytes" metaphor and a span-count remark, never a "link L on content C, fork, is L discoverable from the version?" scenario. This is the one place where the note's own demonstration standard (a multi-postcondition numeric trace, applied to V4–V7) is not extended to the claim that most distinguishes versioning from renaming.

Standard 6 makes a concrete check of key postconditions mandatory, and V10 is a headline postcondition (one of the six topics the note charters itself to prove). The asymmetry — full worked instance for the easy arithmetic claims, none for the novel connectivity claim — is the gap.

**Required**: Add one concrete fork trace exercising the content/link/provenance postconditions, parallel to the VD addressing instance. For example: source `d_src` arranging I-addresses `a₁, a₂` at content V-positions `[1,1], [1,2]` (with `a₁` shared at a second position to exercise `|A| < n`), and a link `ℓ` with from-endset `{(a₁, δ(1,#a₁))}`; then `VERSION(π, d_src)` and check, against the named `Σ'`:
- V2: `M'(v)([1,1]) = a₁`, `M'(v)([1,2]) = a₂`;
- V13: `R' ∖ R = {(a₁, v), (a₂, v)}`;
- V9w: `{(a₁, d_src), (a₁, v)} ⊆ R'`;
- V10: `project(ℓ, 1, v, Σ') = {[1,1]} ≠ ∅` because `a₁ ∈ coverage(ℓ) ∩ A`.

This would show the refraction guarantee operating on specific addresses, which abstract LP12 citation alone does not.

## OUT_OF_SCOPE

The eight Open Questions (concurrent-fork serialization, derivation-direction recovery for severed cross-owner forks, link-subspace carry obligation, location-fixed windowing, withdrawal semantics, provenance-after-contraction) are correctly deferred — each is genuinely new territory rather than a gap in this note, and the note answers within itself what it can (e.g., V2b/V10 settle that content anchoring is a *sufficient* cross-fork channel, leaving only "is anything *further* owed" open).

VERDICT: REVISE
