# Review of ASN-0128

## REVISE

### Issue 1: I6's necessity argument silently relies on the attainability convention that DR states explicitly
**ASN-0128, I6 (IdemEmitSurfaceContract), "The wp, assembled"**: "The formula is necessary as well as sufficient: a rejected call returns no address (a `pre` failure, or a miss with invalid `d`), and an admitted miss failing C3 deposits born nullified with no I0-equal active tuple anywhere at the post-state — the miss hypothesis at Σ, undisturbed by a deposit that lands inactive — so POST fails in every excluded case."

**Problem**: For rejected calls, "POST fails" is not evaluable as written: `POST(a★)` is parameterized by the returned address, and a rejected call returns none, so the predicate has no instance to be false at. The claim that the wp is false on rejection holds only under the attainability convention `wp(g → S, R) ≡ g ∧ wp(S, R)` — which this note states once, in DR ("The equivalence is read as ASN-0126's WP lemma reads its own wp — the attainability convention … is in force: on a rejected call nothing fires and the wp is false outright"), but not in I6. The gap is not hypothetical pedantry: the note's own gate-first scenario (I1's "Order — gate first": a two-span F rejected by the `|F| = 1` shape while an I0-equal single-span F' stands active) furnishes a state where the call is rejected yet an active tuple satisfying POST's body exists — exactly the configuration for which DR shows a "bare guarantee" reading would falsify the displayed equivalence (its P0-failing-resident-target case). DR distinguishes the two necessity routes per precondition — wp false by convention on rejection, postcondition genuinely false on the admitted failing branch — and I6, computing a parallel wp in the same note, conflates them into a single "POST fails."

**Required**: Bring I6's necessity argument to DR's standard: state (or import by one clause) the attainability convention at I6's wp display, and split the necessity cases as DR does — rejected calls falsify the wp by the convention alone; the admitted miss failing C3 falsifies POST genuinely at the returned address. The sufficiency direction and the rest of I6 are unaffected.

### Issue 2: The I5 ↔ I6-corollary relationship is stated three times in three consecutive blocks
**ASN-0128, I5; "The exposed signature"; I6's Corollary**:
- I5's closing sentence: "The branch's consolidated contract — postcondition, weakest precondition, the modulo made exact — is I6's idem-⊥ corollary."
- The exposed signature's closing sentence: "The outcome taxonomy — rejection, hit, deposit — and its per-branch contract are I6's, with I5's idem-⊥ branch as its corollary."
- I6's corollary opening: "I5's branch is this contract's miss with `hit ≡ ⊥`: …"

**Problem**: This is the forward-reference accretion pattern the note carries the classifier for: two anticipatory deferrals to the same downstream location, saying the same thing in different words, followed by the delivery itself. Only the third statement carries content; the first two are pointers the reader must skip past, and the first (I5's) is pure deferral — I5 has already delivered its branch semantics, and restating where its contract lives adds nothing the section structure doesn't already show. This is the same pattern the previous cycle removed from I0/I0a, recurring two blocks later.

**Required**: State the relationship once, at I6's corollary, where it is delivered. At most one forward pointer survives — the exposed-signature sentence has a structural excuse (the signature introduces the outcome taxonomy and must say where its per-branch contract lives); I5's closing sentence should be deleted outright.

## OUT_OF_SCOPE

### Topic 1: The serializing authority in I4
I4 resolves concurrent emits by appeal to "a serializing authority [that] orders the two calls before either becomes a step," inherited from `→_sh` being a sequential interleaved relation. The authority's own semantics — atomicity unit, fairness, whether dedup-check-plus-deposit is one indivisible unit per call — is unspecified.
**Why out of scope**: A concurrency model is new machinery; this note correctly confines itself to what the sequential relation supports, and I4's per-interleaving analysis is complete on its own terms.

### Topic 2: Rejection-reason observability at the partial surface
The exposed `Emit_K` and `Nullify_Binary` collapse every rejection cause — gate failure, invalid `d` on a miss, P-tgt failure — into "no step, no address." Whether a caller can distinguish them (an error taxonomy over the partial operation) is unaddressed, and neither the note's "What this note doesn't cover" list nor its open questions name it.
**Why out of scope**: The substrate contract is complete without it; distinguishing rejection causes is API-surface territory for a successor note, not an error in this one.

VERDICT: REVISE
