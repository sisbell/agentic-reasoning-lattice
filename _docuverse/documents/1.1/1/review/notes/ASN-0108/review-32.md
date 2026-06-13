# Review of ASN-0108

The mathematics here is sound and unusually deep. I checked the wp analysis in W2 (the membership-identity ⊊ frozen-prefix ⊊ weakest nesting is correct, including the orphaning witness `j=2, m'=1, j'=1`), the variable-schedule partition proof in W4, the three order-stability walks in W5 (cut-point skip, harmless tail reorder, clause-1 cancellation — each verified), the W6 blind-spot and W6a frame/F-LAMBDA bridge, the W8 cursor-survival walk, the W9 local-fact derivation, the W9a count formula against `m ∈ {0,2,4,5}` and `N>m`, and the W9b/W9c/W9d termination arguments. All hold. Boundary cases (empty set, exact multiple, first-window-short, orphaned cursor) are exercised concretely; citations resolve to provided foundations; scope is respected. No checkmark-proofs, no "by similarly."

The findings are confined to forward-reference accretion (the active anti-bloat lens) and one circular phrasing. The reasoning does not need repair; the connective meta-prose does.

## REVISE

### Issue 1: Forward-deferral bookkeeping and use-site inventory around the key comparison

**ASN-0108, key-definitions section / W5 / W6 / "ladder of key conditions"**: Four sites in different sections all defer to "W5/W6/W8 sort which key meets which guarantee," and one explicitly narrates the deferral:

- Key section, two near-identical sentences enumerating downstream consumers: "This section defines the three; the guarantees below — W5, W6, W8 — sort them." and, a few lines later, "How each of the three keys fares against the guarantees is settled by W5, W6, and W8 below."
- W6: "W6 is the natural — and sole — home of that comparison." … "and W6 is the entire abstract distance between Nelson's design intent and Gregory's implementation. The introduction and W5 defer to this comparison rather than restating it."
- Ladder: "let W5 and W8 settle which candidate key meets which" … "is the verdict of W5 and W8 below, stated there and not re-derived here."

**Problem**: This is the "multiple paragraphs in different sections defer to the same downstream location" and "definition's introduction enumerates downstream consumers" pattern compounded. The sentences document the note's own organization rather than advancing reasoning. "W6 is the natural — and sole — home of that comparison" and "The introduction and W5 defer to this comparison rather than restating it" are pure structural bookkeeping; the two key-section pointers say the identical thing twice. A precise reader skips all of them to reach the substance. (The load-bearing sentences inside the same W6 paragraph — both permanent keys make W5's and W8's hazards vacuous, so allocation-monotonicity is the sole difference — are genuine and should stay.)

**Required**: Delete the duplicated forward-pointer (keep at most one terse "W5/W6/W8 below settle which key meets which guarantee"). Strike the self-describing sentences ("W6 is the … sole home of that comparison," "The introduction and W5 defer to this comparison rather than restating it," "stated there and not re-derived here"). Keep the substantive verdicts where they are derived.

### Issue 2: A circular "necessary-and-sufficient condition"

**ASN-0108, W5**: "The genuine necessary-and-sufficient condition is global — over the whole pass, each both-states tail matcher is delivered exactly once — not any per-cursor local condition, precisely because local violations can offset one another."

**Problem**: The "condition" offered is the outcome restated — "each both-states tail matcher delivered exactly once" *is* the definition of coherent delivery. As written it reads as "coherence holds iff coherence holds." The real point — that no *per-cursor local* condition characterizes coherence, because clause-1 failures cancel across cursors — is sound (the cancellation walk demonstrates it), but presenting the global outcome as an independent "N&S condition" makes the reader stumble.

**Required**: State the actual content directly — e.g., "no per-cursor local condition characterizes coherence; only the whole-pass property does, since clause-1 failures at different cursors can cancel" — rather than dressing the outcome as a condition.

## OUT_OF_SCOPE

The deferred topics (multi-document allocation ordering, eventual delivery under a non-allocation-monotone key, the cross-state completeness invariant, distinguishing empty-successor from cursor-invalidation, delivery/sizing correspondence) are correctly parked in the Open Questions section rather than half-specified. Nothing to add.

VERDICT: REVISE
