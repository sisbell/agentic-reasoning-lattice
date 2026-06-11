# Review of ASN-0117

This ASN is in strong shape: the two-realisation construction (K.μ⁻+K.μ⁺ when a suffix survives, lone K.μ⁻ when it does not) is correctly case-split with the strict-extension and strict-contraction preconditions verified on both sides, the readback of DELETE's clauses against ASN-0082's contraction checks out clause by clause, the wp derivation's range identity `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` is exact (I verified the set algebra including the store-disjointness step that licenses dropping the `s_L` term), and the worked examples genuinely exercise the boundaries (leading-span, suffix, delete-everything, sharing, transclusion). Two issues remain.

## REVISE

### Issue 1: J1★ discharge contains a claim falsified by the ASN's own sharing analysis, and covers only half the post-state range
**ASN-0117, "What is removed…" → *Effect*, coupling paragraph**: "every survivor's I-address that the K.μ⁺ step re-places was already in the content-subspace range of M(d) at its old position in the initial state, so it fails J1★'s 'new to the range' trigger … — and the deleted addresses are simply absent from the final range."

**Problem**: Two defects in one sentence. (a) The closing clause is false under within-document sharing, which the ASN itself permits (S5/M13) and constructs concretely: in the "Within-document sharing" worked example, `a_5 ∈ A_del` yet `a_5` remains in the final range via the surviving `q_2`. The ASN's own wp section is built on exactly this distinction — only `A_del^{excl} = A_del \ M(d)(L ∪ R)` leaves the range, and the example computes `A_del^{excl} = ∅` while `A_del = {a_5}`. The coupling paragraph thus asserts what the wp section and DEL-REMOVE's parenthetical carefully deny. (b) The discharge justifies "no range-new content" only for the K.μ⁺-re-placed survivors (the images of `R`). The post-state content-subspace range is `M(d)(L) ∪ M(d)(R)`; the `M(d)(L)` half — addresses retained at their original positions by K.μ⁻ — is never mentioned, so the universal claim "DELETE introduces no range-new content" is argued for only one of its two summands.

**Required**: Either drop the "simply absent" clause (J1★ needs only post-range ⊆ pre-range, not any statement about what leaves) or restrict it to `A_del^{excl}`. Extend the discharge to both summands: every post-state content-subspace image is either retained on `L` at its own position (DEL-LEFT) or re-placed from `R` (DEL-SHIFT), and in both cases was in the pre-state content-subspace range, so J1★'s trigger conjunct is false for every `a`.

### Issue 2: DEL-CFRAME's discharge is stated twice with identical justification
**ASN-0117, *Effect* coupling paragraph vs. *Frame* bullet (DEL-CFRAME)**: The coupling paragraph derives the frame ("Both component steps fix the link store, the entity set, and the provenance relation … the R = ∅ single step has the same three clauses from J2's discharge above. We name this frame discharge DEL-CFRAME") and concludes "the three composite-boundary properties — P4★ …, P4a …, P7a … — hold there directly by ExtendedReachableStateInvariants (ASN-0047)." The DEL-CFRAME frame bullet then repeats both: "the frame discharge named above, holding in both realisations (the K.μ⁻/K.μ⁺ frame clauses for the composite, J2 for the R = ∅ single step; ASN-0047) … P4★, P4a, and P7a hold at the post-state boundary by ExtendedReachableStateInvariants (ASN-0047)."

**Problem**: This is the same discharge argued in two places with the same citation parenthetical, and the same P4★/P4a/P7a-at-boundary conclusion drawn twice — the duplicate-paragraph pattern this note's review mode flags. A contract clause restating the *formula* derived in prose is fine; re-arguing the justification in the clause slot is not, and it invites drift between the two copies on the next revision.

**Required**: Keep the derivation in one place. The Frame bullet should state the clause (`Σ'.L = Σ.L ∧ Σ'.E = Σ.E ∧ Σ'.R = Σ.R`, link store fixed in domain and value) and the genuinely new content (P1/P8 trivially preserved on the fixed entity set), and point to the coupling paragraph for the discharge and the boundary-properties conclusion rather than repeating both.

## OUT_OF_SCOPE

### Topic 1: Deletion at general V-position depth m > 2
**Why out of scope**: The operation is pinned to depth 2 because the foundation contraction (ASN-0082) is itself stated for `#p = 2`; the ASN says so explicitly and inherits the restriction honestly. Lifting DELETE to general `m_S` is new displacement work for a future ASN, not an error here.

### Topic 2: Deletion in the link subspace (de-arranging a link from a document)
**Why out of scope**: The precondition fixes `S = s_C`; K.μ⁻'s per-subspace vocabulary would admit contracting `V_{s_L}(d)`, but specifying that operation — its interaction with CL-OWN/CL-UNIQ and discoverability — is a distinct operation belonging to a future ASN.

VERDICT: REVISE
