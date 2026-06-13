# Review of ASN-0108

The technical content here is sound. I checked the weakest-precondition analyses (W2's identity-vs-offset nesting, W8/W9's computability conditions), the partition proof (W4 under variable schedules), the charge/multiplicity argument (W9b), and every concrete walk (the four W9a stride cases, plus the W5 cut-point/tail-reorder/cancellation walks, W6 blind-spot, W8 orphaned-cursor, W9c non-termination). The wp formula `j' = j ∨ (j ≥ m' ∧ j' ≥ m')` is genuinely the weakest precondition; the W9a count `⌈m/N⌉ + [N divides m]` checks against all four walks; boundary cases (empty set, `N > m`, exact multiple, orphaned cursor, insertion-below-cursor) are all exercised. Citations to 0034/0043/0086/0093/0098/0127 are accurate. There are **no correctness, missing-case, or depth REVISE items**.

The findings below are anti-bloat: residual meta-prose accretion the `review-mode.anti-bloat` classifier asks me to surface. They are real and specific, so the verdict is REVISE — but they are targeted trims, not a logic problem.

## REVISE

### Issue 1: W5 develops the cancellation point in three passes, the first two near-verbatim
**ASN-0108, W5**: The claim statement says

> "a tail link that drops below one cursor can rise back above a later cursor and be delivered there exactly once, so per-cursor clause-1 failures can cancel over the pass and leave delivery coherent (the cancellation walk below)"

and the immediately following "Sufficiency does not run backwards" paragraph repeats it almost word for word:

> "Because a link that drops below one cursor can rise back above a later cursor and be delivered there exactly once, the per-transition failures can cancel and the pass stays coherent (cancellation walk below)."

The cancellation walk then demonstrates the same fact a third time, and W9 re-references it again ("per-cursor failures can cancel over the pass (the W5 cancellation walk)").

**Problem**: The paragraph's genuine contribution is the *event-vs-outcome* framing ("a clause-1 failure is an event whereas a skip or a duplicate is an outcome") — that is the reason sufficiency does not reverse, and it is worth keeping. The cancellation sentence itself is carried by the claim statement and proven by the walk; restating it verbatim in between is the "two paragraphs say the same thing in different words" pattern.
**Required**: Keep the event/outcome insight and the walk; drop the verbatim cancellation restatement from the connective paragraph.

### Issue 2: The key-permanence premise is established up front, then re-derived at each use site
**ASN-0108, "What κ is, concretely"** already establishes that the matched-content key is permanent, with the load-bearing citations:

> "This key is permanent: an I-address is never reassigned, and content is never moved or removed from the Istream (S0) ... leaves the content I-address — and the link's endset — intact: S0, L12, LP11."

Yet the same premise is re-derived, with the same citations, at three downstream claims that each need only a *different consequence* of it:

- **W5**: "its value is a fixed function of the immutable endset (L12) over permanent I-addresses (S0), so both clauses hold"
- **W8**: "its value, the least covered I-address, is a fixed function of the link's immutable endset (L12/LP13), so ... κ(c) stays computable"
- **W9b(i′)**: "Gregory's matched-content I-address key, whose cursor key persists with the endset by L12/LP13"

The address key's permanence/value-totality follows the same shape — established in "What κ is" ("a link's address never changes"), then re-derived in W5 ("κ_Σ(a) = κ_{Σ'}(a) = a at every state") and W8 ("κ(c) = c is the identity applied to a value already in the reader's hand").

**Problem**: This is use-site re-narration. The permanence of each key is a one-time fact; only the consequence drawn from it (state-stability in W5, computability-through-orphaning in W8, computability-for-termination in W9b) is claim-specific.
**Required**: State each key's permanence once in "What κ is" and cite that establishment at W5/W8/W9b, deriving only the claim-specific consequence at each site. This removes the repeated `L12/LP13/S0` derivations without touching any logic.

### Issue 3: Undemonstrated "load-bearing" emphasis
**ASN-0108, W5**: "Both halves of coherence are scoped to links matching across the cursor's transition, and the scoping is load-bearing in each."

**Problem**: Unlike cut-point preservation — whose load-bearingness the cut-point walk actually demonstrates with a skip — the both-states scoping is asserted load-bearing with no witness. It is the defensive-emphasis pattern: the scoping's necessity is self-evident (a link matching in only one state cannot be "delivered exactly once" across the transition), so the emphasis adds assertion rather than argument.
**Required**: State the scoping plainly, or show concretely what breaks if it is dropped. Minor, but it is the kind of connective emphasis this review mode is asked to thin.

## OUT_OF_SCOPE

The scope boundaries are respected. W10 correctly defers cardinality ("a separate cardinality query — a distinct operation, out of scope here") without defining it; count-only and full-set retrieval are not specified. The multi-document enumeration discipline (W6's within-a-single-home-document caveat) is parked in Open Question 1 rather than half-answered. Nothing here needs extraction — the future work is appropriately deferred, not erroneously included.

VERDICT: REVISE
