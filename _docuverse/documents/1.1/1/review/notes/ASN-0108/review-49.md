# Review of ASN-0108

The mathematics here has converged. I checked the load-bearing proofs and they hold:

- **W2** wp-analysis: the nesting `membership-identity ⟹ frozen-prefix (j'=j) ⟹ j'=j ∨ (j≥m' ∧ j'≥m')` is correct, including the past-the-end corner where both windows empty and `R` holds with `j'≠j`. The duplicate/omission walk is right.
- **W4** rank-block induction generalizes correctly to a variable schedule via cumulative cut-points `S_i`.
- **W6a** frame bridge (K.λ frames `M`/`C` → image frozen → F-LAMBDA at fixed `I` → disjoint Match growth) is sound.
- **W9a** count formula `⌈m/N⌉ + [N divides m]` checks against all four boundary walks (m=4,5,0; N>m).
- **W9b** charge-injectivity termination argument is valid; **W9c**'s zero-inflow loop and **W9d**'s clause-2 non-necessity are correctly demonstrated.

My findings are confined to the accretion the `review-mode.anti-bloat` classifier asks for. They cluster in the "What `κ` is, concretely" section, which has grown a preview of conclusions the W-claims then prove, plus defensive framing around the key definitions.

## REVISE

### Issue 1: κ-section refutes a key that is not a candidate
**ASN-0108, "The Enumeration Order" (Gregory bullet)**: "a multi-endpoint link can be reached through different I-addresses at different states — a currently-matched-endpoint key would not be state-stable — whereas the least I-address of a slice fixed before the query runs is invariant."
**Problem**: The three candidate keys are address, least-covered-I-address, and content-position. The "currently-matched-endpoint key" is a fourth construct introduced only to be refuted. The definition already fixes the slice *a priori*, so this is a paragraph imagining a case the definition excludes — a reviser-drift pattern. The load-bearing fact ("the least I-address of a fixed slice is invariant") stands without the strawman.
**Required**: Drop the "currently-matched-endpoint key would not be state-stable" refutation; keep the invariance statement.

### Issue 2: definition justified by downstream use rather than its own meaning
**ASN-0108, "The Enumeration Order" (Gregory bullet)**: "'Fixed' is here literal, and is exactly what the downstream claims invoke: the designated slice is settled before any pagination begins..." and "That independence is necessary, and the evidence supplies it".
**Problem**: The definitional content is "the slice is a function of the immutable link value, not of whichever endpoint matches." The clauses "is exactly what the downstream claims invoke" and "That independence is necessary, and the evidence supplies it" justify the definition by appeal to downstream consumers and defend it against objection rather than advancing its meaning.
**Required**: State the definition plainly; remove the downstream-justification and defensive framing.

### Issue 3: over-generalization in the key definition
**ASN-0108, "The Enumeration Order" (Gregory bullet)**: "Any such designation yields permanence; the single-endpoint case, where the designated slice and 'the matched endpoint' coincide unambiguously, is the special case."
**Problem**: The operation uses one designated slice. Generalizing to "any such designation" and casting single-endpoint as "the special case" is decorative — no W-claim needs the generality; each needs only that the chosen key is permanent.
**Required**: Cut, or reduce to the one chosen designation.

### Issue 4: foil bullet pre-announces the per-claim verdicts
**ASN-0108, "The Enumeration Order" (content-position bullet)**: "We carry it only as the cautionary foil: keying on position rather than identity is precisely what the windowing laws below must guard against."
**Problem**: The section's task is to define the three keys. "precisely what the windowing laws below must guard against" pre-states the conclusions that W5/W6/W8/W9 separately establish. The descriptive statement that the implementation does not use a position key is fine to keep; the forward-pointing verdict is redundant with the proofs it previews.
**Required**: Keep the definition and the "the link search emphatically does not" fact; drop the pre-announcement of the downstream verdicts.

### Issue 5: summary essay sentence in W6
**ASN-0108, W6 ("This is where the two permanent keys part...")**: "Allocation-monotonicity is their only behavioural divergence on the windowing laws."
**Problem**: An exhaustiveness/summary claim about the two permanent keys across all laws; it does not advance W6's append-at-tail argument.
**Required**: Cut.

## OUT_OF_SCOPE

### Topic 1: multi-home-document global enumeration order
**Why out of scope**: The W6 caveat and Open Question 1 correctly relegate the case where independently-advancing per-document allocators defeat a single allocation-monotone key. This is future territory, not an error here — no action needed.

### Topic 2: cross-call completeness invariant over a mutating set
**Why out of scope**: Open Question 3 correctly defers the invariant relating successive matching sets. W7's present-tense completeness reading is the right boundary for this note.

VERDICT: REVISE
