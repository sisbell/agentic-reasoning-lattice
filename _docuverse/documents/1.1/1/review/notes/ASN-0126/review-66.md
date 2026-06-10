# Review of ASN-0126

The formal development is sound. I checked every proof — P1–P6, the wp derivation, Lemma (RegisteredAdmissible), the projection bridge, the R-Scope transfer, and the worked illustration — and found no correctness gaps, no skipped cases, no hand-waves, no cross-ASN violations, and no foundation-notation reinvention. The proofs are complete (inductions have base + step, the wp accounts for every conjunct and correctly identifies C3 as newly live, the born-nullified arithmetic checks out: `a_R = ...2.3 ∉ coverage(G_rng)` and the citation lands at `g = ...2.4 ∈ coverage(G_rng)`). The boundary cases that matter here — `G = ∅` for Unary, self-nullifying retraction (C2), pre-existing retraction (C3), ghost targets — are all handled.

The note carries the `review-mode.anti-bloat` classifier. The findings below are the residual meta-prose instances that match its named patterns. They are prose trims, not structural fixes.

## REVISE

### Issue 1: Forward use-site annotation on the effect-identity definition
**ASN-0126, The shape-gated emit**: "Call this effect-identity; we appeal to it below wherever a →_sh-step must be read through its underlying K.λ."
**Problem**: The trailing clause enumerates downstream consumers of the definition rather than advancing it — the exact "definition's introduction enumerates downstream consumers" pattern. The name and the property it denotes are complete without it; each later invocation ("by effect-identity") already signals the use at its own site.
**Required**: Drop the trailing clause. Name effect-identity, state the property (added preconditions restrict when a step fires, not what it does), and stop.

### Issue 2: Editorial defense of proof method in the R-Scope transfer
**ASN-0126, Single-source**: "its conclusion `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` nonetheless transfers verbatim, by a frame argument simpler than re-deriving the intersection."
**Problem**: "simpler than re-deriving the intersection" compares the chosen argument to an unchosen alternative — a defensive justification of method that adds nothing to the frame argument that immediately follows it (and that argument is correct: same `(Σ, d_retr)`, `a_emit` blind to F ⟹ same `dom(Σ'.L)` ⟹ same `A_rel^{Σ'}`; the conclusion reads only that set and the fixed subtree).
**Required**: Drop "simpler than re-deriving the intersection"; present the frame argument directly.

### Issue 3: State-independence asserted before its premises, duplicating P4
**ASN-0126, Shape-conformance (closing)**: "The predicate therefore depends only on the tuple's span counts `|F|`, `|G|` and the shape recorded for K in the registry — a property of the tuple-plus-registration pair, evaluable identically at any reachable state."
**Problem**: The rider "evaluable identically at any reachable state" asserts cross-state stability — precisely P4 (Sh-confStateIndependence) — at a point where the premises that justify it (P1 RegistryInvariance, C0) have not yet been introduced; *Registry permanence* and *Registration entries* both come later. It is simultaneously a forward reference to unestablished machinery and a duplicate of P4. The supported clause (Sh-conf reads only span counts and the registry-recorded shape) is fine; the rider outruns it.
**Required**: End the sentence at the registry-shape dependence. Let P4 carry the cross-state claim, where P1 and C0 are in hand.

## OUT_OF_SCOPE

The six open questions (idem semantics, behavior catalog, default predicates, standard registrations, predicate composition, extension beyond F=1/N=3) correctly defer operational semantics and richer arity to the successor note. Nothing further to add here.

VERDICT: REVISE
