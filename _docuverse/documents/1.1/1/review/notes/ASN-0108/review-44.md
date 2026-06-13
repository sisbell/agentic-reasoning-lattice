# Review of ASN-0108

This is a careful, largely rigorous treatment. The WP analysis in "The Cursor" is correct (the nested membership-identity ⟹ frozen-prefix ⟹ weakest hierarchy checks out, including the past-the-end corner), the W4 partition proof handles the variable-`N` schedule correctly, the W9a count formula verifies against all four walks including the `m=0` and `N>m` boundaries, and the W9c/W9d tightness analysis is sound. The findings below are two genuine precision gaps and two instances of the accretive prose the anti-bloat classifier is watching for.

## REVISE

### Issue 1: W5's no-skip guarantee is headlined over a two-state condition but proved only over a whole-pass one

**ASN-0108, W5 (OrderStability)**: "it skips no link that was already an undelivered tail matcher when the cursor was set (a link matching in both the cursor-setting state and the resume state)"

**Problem**: "Skipped" (never delivered in *any* window) is a whole-pass property, but the link-condition in the headline — "matching in both the cursor-setting state and the resume state" — is a two-state, per-resume-step condition. The body silently strengthens the link-condition to *continuous* matching and adds a termination hypothesis: "clause 1 holds each surviving both-states tail matcher *in* After"; "*No skip* holds **on the added hypothesis that the pass terminates**"; "Without termination ... a still-matching tail matcher can sit in `After` forever, never delivered yet not skipped." A link that matches at two consecutive states (satisfying the headline) but orphans before any window reaches it is never delivered, yet the headline promises it is not skipped. W9b states the scope the proof actually delivers: "every link that is an undelivered tail matcher at some visited call ... and that *remains* matching until a later window could reach it is delivered exactly once." So the W5 headline over-promises relative to *both* its own body and W9b — an internal inconsistency, since the note demonstrably knows the correct scope.

**Required**: Restate W5's no-skip guarantee over links that *remain* matching until a window can reach them (the W9b scope), under the explicit termination hypothesis, and reserve the two-state "both-states" notion for the no-re-delivery half (which the body correctly shows is unconditional). The headline and the body should name the same set of links.

### Issue 2: the matched-content key is defined as "least covered I-address" but referred to as "matched content's I-address," which breaks the permanence the proofs rely on

**ASN-0108, key introduction**: "We take the key from the endset, **not** from whichever endpoint the link happens to match in a given state, and the choice is necessary: ... a multi-endpoint link can be reached through different I-addresses at different states — a *currently-matched-endpoint* key would not be state-stable — whereas the least covered I-address is invariant."

**ASN-0108, W9b**: "on resurrecting it returns at its permanent key (the link's own address by T8, or its matched content's I-address by S0)"

**Problem**: The permanence of this key — load-bearing for its state-stability (W5) and its computability-after-orphaning (W8) — requires it to be the *least covered I-address read from the immutable endset* (a fixed selection), exactly as the intro insists. But the name "matched-content key" and the W9b phrasing "matched content's I-address" denote, read literally, the *currently-matched* endpoint's address — a state-varying selection, precisely the "currently-matched-endpoint" the intro rules out as not state-stable. W9b's "by S0" justifies that each I-address is permanent (content never moves), but the permanence of the *key* needs the *selection* to be fixed; "matched content" does not supply that for a multi-endpoint link. Read with "matched content," W9b's permanence claim has a gap, and the terminology contradicts the intro's own definition.

**Required**: Use "least covered I-address (of the fixed relevant endset slot)" consistently — in W6, W8, and especially W9b — and drop the "matched content's I-address" phrasing, which reintroduces the state-dependence the key was constructed to avoid. The key name itself ("matched-content key") invites the confusion; consider whether a name keyed on the endset rather than the match is warranted.

### Issue 3: W8 disclaims two always-true conditions (defensive over-listing)

**ASN-0108, W8 (CursorSurvivesUnderComputableKey)**: "`After(c, Σ')` is defined by `κ(c)` alone ... and requires neither `c ∈ Match(q, Σ')`, nor that `c` remain an allocated address, nor that `c`'s allocation be unique."

**Problem**: Of the three disclaimed conditions, only the first ("`c ∈ Match`") is a meaningful disclaimer — Match is non-monotone, so a reader might assume the cursor must still match. The other two are foundation-guaranteed always true: link addresses are never removed from the allocated set (T8 / L12a), so "`c` remain an allocated address" holds unconditionally; and GlobalUniqueness makes every allocation unique, so "`c`'s allocation be unique" holds unconditionally. Disclaiming two conditions that can never fail is non-advancing defensive prose — a reader pauses to ask "could `c` become de-allocated? could its allocation be non-unique?" only to find the foundations already forbid both.

**Required**: Keep the load-bearing disclaimer ("does not require `c ∈ Match`") and drop the two vacuous ones. If the point is to emphasize that only computability of `κ(c)` matters, state that directly rather than enumerating non-conditions.

### Issue 4: the W6 caveat reopens by restating the within-home-document scope already in W6's body

**ASN-0108, W6 body**: "Under an address-based key the forward hypothesis holds within a single home document's link allocator, whose successive links carry strictly increasing addresses (foundation T9, forward allocation; a single allocator chain is strictly increasing)."

**ASN-0108, trailing caveat**: "One caveat bounds the address key's append-at-tail guarantee (W6): it is allocation-monotone only *within a single home document*, where the link allocator issues strictly increasing addresses (T9, forward allocation for `same_allocator`)."

**Problem**: The caveat's opening clause restates W6's body verbatim in substance (single-home-document scope, strictly increasing addresses, T9). The genuinely new content is its second half — the cross-document reopening of the blind spot and the Open Question 1 pointer. Two paragraphs say the same thing in different words before the new content arrives; a reader who absorbed W6's body must re-read the same scoping fact to reach the cross-document consequence.

**Required**: Open the caveat directly from the cross-document consequence ("Across multiple home documents, whose link allocators advance independently, the address key is not *globally* allocation-monotone ...") and cite W6 for the within-document scope rather than re-deriving it from T9 a second time.

## OUT_OF_SCOPE

### The deferred topics are correctly bounded
The note correctly imports the satisfaction predicate from ASN-0127 rather than re-deriving it, defers query construction (region/type via ASN-0086) to "query construction, outside this note," defers count-only retrieval to "a separate cardinality query ... out of scope here" (W10), and parks multi-document ordering, cross-call completeness, non-permanent-key cursor recovery, and progress-count correspondence as Open Questions rather than half-specifying them. Nothing of substance is improperly omitted; the boundary is well-drawn and no future-ASN material is smuggled in as a present claim.

VERDICT: REVISE
