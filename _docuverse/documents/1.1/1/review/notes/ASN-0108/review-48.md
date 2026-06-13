# Review of ASN-0108

This is, by the standards that usually defeat an ASN, a careful note. There is no proof-by-checkmark, no "by similar reasoning," and the boundary cases that matter to windowing — empty matching set, exact-multiple termination, first-window-short, orphaned cursor — are each walked concretely with the W9a/W9 formulas checked against them. The weakest-precondition analysis of the offset-vs-identity cursor (W2) is the kind of non-trivial wp the standards demand, and I verified its three-way strict nesting (`membership-identity ⊊ frozen-prefix ⊊ weakest`) against its own witnesses; it holds. The partition proof (W4) correctly generalizes to a variable size schedule, and the charge-injectivity termination argument (W9b) is the right tool for a mutating set. The defects below are precision and prose, not broken proofs.

## REVISE

### Issue 1: The "relevant endset slot" is never defined, yet Gregory's key rests on it

**ASN-0108, "What κ is, concretely" (and W5, W8, W9b)**: "order each link by the **least I-address covered by its relevant endset slot**, read from the endset alone (L12) over *permanent* I-addresses (S0)."

**Problem**: "Relevant endset slot" is presented as a definite, previously-fixed notion — the later invocations write "the **fixed** relevant endset slot" (W8 walk; W9b derivation: "the least covered I-address of the fixed relevant endset slot by S0") — but it is never said *which* slot, nor how it is determined for a from-to-**type** query whose matching is any-endpoint discoverability. The note is explicitly aware that a state-dependent choice breaks everything ("a *currently-matched-endpoint* key would not be state-stable") and rules it out — but having ruled out the only state-given candidate (the matched endpoint), it substitutes an undefined one. This is load-bearing: the assertions that Gregory's key is **state-stable** (W5, "its value is permanent"), keeps `κ(c)` **computable** through orphaning (W8), and is one of the "either permanent key" cases in the termination accounting (W9b) all depend on the key being a fixed function of a fixed, immutable slot. As written, the reader cannot verify "the least covered I-address is invariant" because the object it is the least I-address *of* is undefined.

**Required**: State which endset(s) the key reads (from? to? from∪to? all slots?), and confirm the choice is state-independent for a multi-endpoint, any-endpoint-match query — or rephrase to "least I-address over a fixed, a-priori-designated endset slice, any such choice yielding permanence," so that the word "fixed" references a definition that exists.

### Issue 2: Editorial value-assertions and cross-section re-announcement (anti-bloat)

**ASN-0108, W5 / W6 / W9 / W9b**: representative instances —
- W5: "Cut-point preservation is therefore *load-bearing* — not merely a property the identity keys happen to supply."
- W6: "This is not a bug in the cursor — it is the unavoidable cost of pairing stateless re-execution with a key that is not allocation-monotone."
- W9b: "The distinction between cumulative inflow and instantaneous tail size is not cosmetic."
- W9 blockquote: "it certifies two *different* things under two *different* provisos — **computability** (W8) and **clause 1** (W5) — which must not be conflated."

**Problem**: This note carries the `review-mode.anti-bloat` classifier, and the connective tissue is where the accretion sits. In each case above the *demonstration* immediately preceding (the skip walk, the blind-spot walk, the size-1-loops-forever counterexample) has already established the point; the quoted sentence only asserts that the point is important. These are defensive value-assertions — "is load-bearing," "is not cosmetic," "is not a bug," "must not be conflated" — that the precise reader must read past to reach the next claim. Separately, the computability-vs-state-stability separation is drawn freshly in W8, re-announced as a "must not be conflated" warning in the W9 blockquote, and re-drawn a third time as the (i)/(i′) split in W9b — three sections saying the same thing in different words. The reasoning itself (the walks, the wp computation, the charge-injectivity) is not bloat and should stay.

**Required**: Excise the value-assertion asides; let the walks carry their own weight. State the computability/state-stability/value-totality taxonomy *once* (it belongs at W8, where the distinction is introduced) and have W9/W9b *reference* it rather than re-derive it.

### Issue 3: LP18 cited for a case its precondition excludes

**ASN-0108, W9b**: "links that become discoverable ahead of a cursor by the LP18 mechanism of ASN-0098 ... **whether or not the link was ever previously a member** (subsuming both a previously-orphaned link resurrecting (W7) and a born ghost (L4/L9 of ASN-0043) first entering the view)".

**Problem**: ASN-0098 LP18 (Resurrection) is stated under the precondition "if `a` is orphaned at `Σ`" — it is the orphan-specialized instance. The note correctly generalizes the *event* to never-member born ghosts but keeps the LP18 label for a case LP18 does not cover. The general fact — a link already in `dom(Σ.L)` becoming newly discoverable when an arrangement extension reaches a covered address — is the extension-monotonicity of projection (LP9), of which LP18 is the orphan special case.

**Required**: Cite LP9 (ExtensionMonotonicity) for the general "becomes discoverable ahead of the cursor" inflow event, with LP18 named as the orphan instance and L4/L9 for born ghosts — a one-citation fix, since the reasoning is already sound.

## OUT_OF_SCOPE

### Topic 1: Multi-document enumeration order
**Why out of scope**: The note scopes `Match(q, Σ)` to a single query document (`findlinks_V(W, d_q, Σ)`), and the W6 caveat that the address key is not *globally* allocation-monotone across independently-advancing home-document allocators is correctly deferred to Open Question 1. This is genuinely new territory, not a gap in the present claims.

### Topic 2: Completeness across a mutating result set; recoverability for non-permanent keys
**Why out of scope**: Open Questions 3 and 4 — the invariant relating successive calls' matching sets, and the protocol that distinguishes a genuinely empty successor set from an irrecoverable cursor under a non-permanent key — are properly held open. W7/W8/W9 establish that the present-tense reading and the computability hazard *exist*; specifying their resolution is future work.

### Topic 3: Query construction, satisfaction predicate, type-part refinement
**Why out of scope**: The note takes `Match` as given from ASN-0127 and defers "which region a query fixes" and the type-part refinement (ASN-0086) to query construction. This is a clean abstraction boundary, not an omission — the windowing guarantees use only M-fin and M-mut. The explicitly-listed out-of-scope operations (FINDNUMOFLINKSFROMTOTHREE, FINDLINKS/ASN-0099, MAKELINK, FOLLOWLINK, BEBE) are not claimed here, and W10 correctly defers cardinality to "a separate cardinality query — a distinct operation, out of scope here."

VERDICT: REVISE
