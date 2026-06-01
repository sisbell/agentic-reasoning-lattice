# Review of ASN-0086

## REVISE

### Issue 1: Duplicate motivational prose — the "generic relation distinguishes only by content" point is made twice

**ASN-0086, Remark (under Definition — TupleAddress)**: "A generic mathematical typed relation is a subset of `℘(A) × ℘(A)` — a set of address-pair-pairs distinguished only by content. Our typed relation is richer: each tuple carries an address that participates in the relation's identity."

**ASN-0086, intro to "Tuple Identity (R0, R1, R2)"**: "A generic mathematical relation distinguishes its members only by content: two tuples with identical (F, G) are the same tuple. The substrate's relations do not work that way."

**Problem**: These two paragraphs, in adjacent sections, assert the same contrast (generic relation = content-only identity; substrate relation = address-carrying identity) in different words. This is the anti-bloat "two paragraphs in the same document say the same thing" pattern.

**Required**: Keep one. The Remark's `℘(A) × ℘(A)` framing is the more precise of the two; fold the section intro into it or delete the intro's first two sentences and open directly with the R0/R1/R2 enumeration.

### Issue 2: Defensive meta-prose in "Arrangement modification is out of scope"

**ASN-0086, "Arrangement modification is out of scope"**: "Under M2 every document's arrangement is empty at every reachable state, so the substrate admits no arrangement-modifying transition — `→` is the complete dom-extending vocabulary, and persistence claims (R6c) are stated and proved against `→` alone. No claim in this note relies on any transition M2 forbids."

**Problem**: The closing sentence ("No claim in this note relies on any transition M2 forbids") is a defensive justification that advances no reasoning — it pre-empts a hypothetical objection rather than stating a property. This is the flagged pattern of meta-prose that the precise reader must skip past.

**Required**: Delete the closing sentence. The substantive content (M2 ⟹ `→` is the complete dom-extending vocabulary) stands on its own.

### Issue 3: Consistency inventory in the State transition relation paragraph

**ASN-0086, State transition relation**: "...the substrate exposes no removal, replacement, or in-place mutation transition that touches `(dom(Σ.C), dom(Σ.M), dom(Σ.L))` (consistent with S0, L12, T8, and ASN-0093 M1/C0/L12 across the underlying ASNs)."

**Problem**: The parenthetical is a use-site/consistency inventory — it lists invariants the claim is "consistent with" without those citations doing load-bearing work in the sentence (the no-mutation fact is asserted as a property of `→`, not derived from the list). This is accreted cross-reference noise.

**Required**: Either delete the parenthetical, or if one specific invariant actually grounds the no-mutation claim (L12 + S0 + M2), cite only that and phrase it as a derivation rather than a consistency gesture.

## OUT_OF_SCOPE

### Topic 1: Retraction stability across arbitrary `↝` (non-`→`) transitions
R6a is stated over single `→`-steps and R6c over `→*`. Higher-layer `↝` transitions are covered only indirectly, by composing R7a's decomposition with R6c. A direct statement of nullification persistence across the categorical relation `↝` for conforming layers belongs in a future note that treats cross-layer composition explicitly; it is not an error here, since every relational-layer operation is a `→`-step.

VERDICT: REVISE
