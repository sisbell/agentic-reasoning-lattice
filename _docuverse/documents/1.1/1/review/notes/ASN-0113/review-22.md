# Review of ASN-0113

## REVISE

### Issue 1: W14 states the count/report separation three times
**ASN-0113, "Invariants across the members" (W14) and the one-member worked instance**: W14's body reads "it is a total function, defined for every allocated `d` and every `S ∈ {s_C, s_L}` independently of whether the operation emits a member for that subspace. An empty subspace has `n_S(d) = 0` as a fact about `V_S(d) = ∅`, regardless of the report's membership." The two sentences say the same thing twice ("independently of whether the operation emits a member" ≡ "regardless of the report's membership"). The worked instance then says it a third and fourth time: "remains a fact ... well-defined independently of whether the report emits a link member. The report omits the empty subspace while the count of that subspace is still a defined zero — the very separation W14 records."
**Problem**: The single point — `n_S` is total and independent of report membership — is restated four times across two locations. A reader following the claim must skip past the repetition. This is the "two paragraphs say the same thing in different words" pattern the classifier targets.
**Required**: State the separation once in W14's body; in the worked instance, exhibit the fact (`n_{s_L}(d') = 0` while no link member is emitted) without re-explaining the principle.

### Issue 2: W18's defensive parenthetical restates the claim and pre-empts an absent objection
**ASN-0113, "Permanence of the report" (W18)**: "(We make no claim that arrangements are immutable in general: the foundation's vocabulary includes in-place arrangement mutations — K.μ⁻ contracts and K.μ~ reorders an existing `M(d)`, ASN-0047 — so a document's extents *can* change under editing. What the report cannot do is change while the state it views stands still.)"
**Problem**: This is a defensive justification ("We make no claim...") guarding against a misreading the claim does not invite, and its closing sentence restates W18's operative content ("any two queries against the *same* `Σ` return identical span-sets ... changes only when `M(d)` changes"). The mutation inventory adds no force to W18, which is purely about determinism on a fixed state.
**Required**: Drop the parenthetical; W18's "the report changes only when `M(d)` changes" already carries the point without the defensive framing or the restatement.

### Issue 3: Rhetorical flourish in a derivation slot
**ASN-0113, end of "What the pair reveals..." (W12)**: "The span-set is the report that returns *both* halves of what a document is — its content and its connections — in one observation."
**Problem**: This closing sentence follows the W12 witness construction but advances no reasoning — it is essay content occupying a structural slot after the proof has concluded.
**Required**: Remove it; the witness construction already establishes W12.

## OUT_OF_SCOPE

(none — the note confines out-of-scope topics to its Open Questions and defines no claims for them.)

VERDICT: REVISE
