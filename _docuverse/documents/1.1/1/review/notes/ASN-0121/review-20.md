# Review of ASN-0121

## REVISE

### Issue 1: FL-WP omits the fresh-retraction-link entry, a third result-changing case

**ASN-0121, "The only result-changing transition" / FL-WP**: "*K.λ is the unique result-changing transition.* We compute its weakest precondition in the two cases that matter — the entry of a newly created link, and the survival of an existing match under a retraction-bearing K.λ."

**Problem**: FL-WP(a) is explicitly restricted to a fresh *ordinary* link — `coverage(Θ) ∉ [coverage(R)]`. FL-WP(b) computes only the *survival of existing matches* under a retraction-bearing K.λ; it says nothing about whether the freshly committed retraction link `b ∈ dom(Σ'.L) \ dom(Σ.L)` itself enters the answer. But a retraction tuple has value `(∅, G', R)`, and against a query with from-wildcard (`F = ∗`) it can satisfy `sat`: e.g. `q = (∗, ∗, ∗, Θ_R)` with `Θ_R` covering the retraction type `R` matches `b` via `lift(R, Θ_R) = true`. So the same K.λ step that FL-WP(b) analyses also *adds* a new member `b` to `findlinks(q, Σ')` — a result change neither (a) nor (b) characterizes. The table entry "Weakest precondition for the unique result-changing transition (K.λ)" therefore overstates: the wp characterization of K.λ's effect on the result is incomplete, contradicting the prose claim that K.λ is *the* result-changing transition whose wp is computed.

Note the addressability subtlety carries over: `b`'s entry condition involves `b ∉ nullified(Σ')` against `L_R^{Σ'} = L_R^Σ ∪ {(b, ∅, G')}`, so the *self-retraction* case `b ∈ coverage(G')` — explicitly set aside in FL-WP(b) "by scope" — becomes live precisely here.

**Required**: Add the third case (entry of a fresh retraction-type link), computing its wp — structurally FL-WP(a) with the ordinariness relaxed, `L_R` now extended by `b`'s own tuple, and the self-retraction conjunct retained — or explicitly justify excluding it (e.g., declare that retraction-type links are not result-members of interest and confine the operation's range, then state why). As written, the "two cases that matter" framing leaves a realizable result change underived.

## OUT_OF_SCOPE

### Topic 1: Version-/time-qualified inquiry into pre-retraction states
**Why out of scope**: The ASN explicitly inquires against the current state and marks the version-scoped behaviour as an open question; this is new territory, not an error here.

### Topic 2: I-address ↔ V-spec request equivalence under full-deletion
**Why out of scope**: The grammar admits only I-address requests; the arrangement-mediated phrasing is a separable front-end, correctly deferred to an open question.

VERDICT: REVISE
