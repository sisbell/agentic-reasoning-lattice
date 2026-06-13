# Review of ASN-0131

I checked the construction and every derived claim against the foundations. The mathematics is sound: RE-DEF is decidable as argued (finite image by S8-fin, span membership by T2, `nullified` computable per ASN-0086); RE-SEL composes correctly from F-V/F-FIND/F-MATCH; the RE-UDIST factoring through `Avail(Σ)` is valid because `touch_W(e)` is `a`-independent; the worked instance's type-disjointness, straddle-span, and per-endset readings all check; RE-CWP's weakest precondition is correctly derived and its `R = ∅` boundary correctly collapses to `RE = ∅`; and RE-RET's backward direction is properly discharged via R0a (antichain) + R-Scope (single-tuple scope). I found no correctness gap. The findings below are prose accretion (the note carries `review-mode.anti-bloat`) plus one minor consistency point.

## REVISE

### Issue 1: Defensive-justification accretion in the worked instance's type-endset argument
**ASN-0131, "A worked instance" (the `e₃` bullet)**: The load-bearing field-agreement proof correctly concludes "So no content address extends `θ`, giving `coverage(e₃) ∩ dom(Σ.C) = ∅`." Three defensive asides then follow: (i) "T7 (SubspaceDisjointness, ASN-0034) would only convert a *known* identifier mismatch into distinctness, which is not what we need here"; (ii) "the 'every extension carries `θ`'s identifier' reading fails outright — an extension `θ.0.x` has `zeros > 3`, is T4-invalid, and has no `E₁` at all"; (iii) "(This is a property of the *coverage*, strictly stronger than `θ ∉ dom(Σ.C)`: a `θ` merely absent from `dom(Σ.C)` — say a document-level prefix of `a₂` with `zeros = 2` — could still satisfy `θ ≼ a₂`...)".
**Problem**: This is an illustrative example, and its sibling endsets `e₂′`, `e₃′` are handled by bare stipulation (`coverage(e₂′) ∩ {a₂} = ∅`) with no proof at all. Even granting the full `e₃` proof, the three asides are proof-defense — each guards the technique against a misreading. Aside (iii) in particular imagines a `zeros = 2` `θ` that the example's own stipulation (`zeros(θ) = 3`, element-level) excludes — exactly the "imagines a case the precondition already excludes" pattern. A reader tracking "does `e₃` touch the region?" must skip past all three to reach the answer.
**Required**: Drop the asides; either keep only the single load-bearing field-agreement proof, or stipulate `coverage(e₃) ∩ dom(Σ.C) = ∅` as setup parallel to `e₂′`/`e₃′`.

### Issue 2: Forward-reference accretion around the content-subspace restriction
**ASN-0131, "The region, and what it resolves to" and "When does an endset touch the region?" (the standalone "Why confine W" paragraph)**: The first passage plants a within-document forward pointer — "we record just below why it is the right domain" — and a dedicated paragraph later opens "Why confine `W` to the content subspace?", runs a full rationale for the precondition, and closes "A link-subspace region is the coherent but separate query Open Question 7 takes up; we do not develop it here."
**Problem**: This is precondition-rationale prose that defers both within-document ("just below") and forward (to OQ7). The genuinely informative payload — *a link-subspace region would resolve to an image in `dom(Σ.L)` and surface link-aimed anchoring* — is a legitimate "what the operation does/does not do" statement, but it belongs in OQ7's own statement, not as a standalone defense of the precondition. The "we record just below why" pointer plus the full standalone justification is the forward-reference-accretion shape the classifier targets.
**Required**: Remove the "we record just below" pointer; fold the one-sentence semantic content (link-subspace → image in `dom(Σ.L)`) into OQ7's statement, and reduce the in-body justification to the single fact that `W ⊆ s_C` keeps the image content-valued (`I ⊆ dom(Σ.C)`).

### Issue 3: RE-EDIT states retraction as unconditional removal; RE-RET makes it conditional
**ASN-0131, Claims Introduced, RE-EDIT**: "`K.λ` moves it *through `Σ.L`* (ordinary emission may add a pair, a retraction removes via the addressable population)."
**Problem**: RE-RET establishes that a retraction is a `K.λ` that emits a fresh *addressable* link `b`, and that "a retraction's net effect on `RE` is removal only" holds *only under the net-removal-only hypothesis* `coverage(Θ) ∩ dom(Σ.C) = ∅` — a property the note explicitly says ASN-0086 does not furnish — with the flagged exception that, absent it, `b` can add the pair `(3, Θ)`. RE-EDIT's partition ("ordinary emission may add" vs "a retraction removes") therefore states unconditionally, in the classification summary, what RE-RET shows is conditional, and the "ordinary emission" framing reads the retraction case out of the "may add a pair" clause that would otherwise cover `b`'s contribution.
**Required**: Soften RE-EDIT's retraction clause to track RE-RET — e.g., "a retraction removes via the addressable population (RE-RET; the emitter may itself contribute `(3, Θ)` absent the net-removal-only hypothesis)."

## OUT_OF_SCOPE

### Topic 1: Θ–content disjointness for retraction emitters (OQ6)
**Why out of scope**: RE-RET's dependence on `coverage(Θ) ∩ dom(Σ.C) = ∅` is a property of the retraction layer (ASN-0086), not of this query. The note handles it correctly — it states the result conditionally, derives the `Θ`-disjointness it *can* (from-set/to-set, unconditionally, via the unit-depth field-agreement argument), and routes the residue to OQ6. This is not a defect to re-raise; it is correctly deferred.

### Topic 2: Intersection-distributivity (OQ4) and link-subspace regions (OQ7)
**Why out of scope**: The union half (RE-UDIST) is derived; intersection-distributivity genuinely fails under the non-injective arrangement (M13/M14, ASN-0058) and is correctly left open. The link-subspace region variant is a distinct query, correctly deferred. Both are appropriately scoped as open questions, not gaps in this ASN.

VERDICT: REVISE
