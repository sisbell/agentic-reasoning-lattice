# Review of ASN-0108

The technical content is sound. I checked the weakest-precondition analysis (W2), the partition proof (W4), the sufficiency/necessity decomposition of W5, the inflow-charging argument (W9b), and the termination formula (W9a) against the four boundary walks (m=0, N>m, exact-multiple, non-divisible). The math holds, the citations to the foundations are accurate, and the edge-case coverage is genuinely thorough — the W2 nesting (membership-identity ⟹ frozen-prefix ⟹ genuine wp) is correctly strict, and the W9a count `⌈m/N⌉ + [N|m]` checks against all four walks including m=0.

The findings below are prose-density issues, which is exactly what the `review-mode.anti-bloat` classifier is asking me to surface: the claim statements have accreted mechanism, cross-references, and defensive asides that belong in the proof prose.

## REVISE

### Issue 1: Claim statements W5 and W9 carry their own proofs and cross-references
**ASN-0108, W5**: "Clause 1 at the held cursors is *sufficient* but **not necessary** — coherence is inherently a *whole-pass* property: a tail link that drops below one cursor can rise back above a later cursor and be delivered there exactly once, so per-cursor clause-1 failures can *cancel* over the pass and leave delivery coherent (the cancellation walk below)."
**ASN-0108, W9**: "It is **not** secured by computability at `c` alone; it *is* secured by clause 1 ... — W5's discipline, here serving as W9b's termination condition (i), sufficient but not necessary and with the cut-point-failure mechanics exactly as W5 gives them (absent the cancellation W5 tolerates, a clause-1 failure drops a still-matching tail matcher permanently below the cursor at which it failed, out of the pass)."
**Problem**: The claim slot is meant to state the guarantee. Here it states the guarantee *and* the mechanism for why a side condition is unnecessary *and* a forward pointer to the walk that demonstrates it. The cancellation mechanism is already demonstrated by walk 3 and the cut-point mechanics by W9c; restating them inside the W5/W9 statements is essay content in a structural slot.
**Required**: Reduce the W5 statement to the property (clause 1 sufficient-not-necessary; clause 2 not necessary; coherence is whole-pass) and the W9 statement to the two readings (local fact under key-computability; global guarantee under clause 1 at every visited cursor). Move the cancellation/cut-point mechanics to the proof prose and the walks, which already carry them.

### Issue 2: W5's exposition cannot stand without three downstream claims
**ASN-0108, W5 (sufficiency proof)**: "*No skip* is conditional on termination: ... the terminal short window forces `After(final cursor) = ∅` (W9's local fact under computability) ... so no-skip rests on W9b's termination conditions, not on cut-stability." The same paragraph also reaches forward to "the W6 blind spot."
**Problem**: W5 sits in the Stability section, ahead of Termination (W9/W9b) and ahead of W6. Its no-skip half is stated by deferring forward to W9's local fact and W9b's conditions, while W9b in turn back-references W5's clause 1 as its condition (i). This is the forward-reference accretion the classifier targets: a Stability claim that depends on not-yet-stated Termination claims, gestured at rather than carried.
**Required**: State W5's coherence as the two clean conditionals it actually is — "clause 1 at every visited cursor ⟹ no re-delivery (unconditional); clause 1 + termination ⟹ no skip" — and let W9b cite W5 for the termination side, so the dependency flows one way. The forward pointers to W9/W9b can then be dropped.

### Issue 3: Defensive aside rebutting a wrong reason
**ASN-0108, W5**: "The allocation axioms are orthogonal to this freezing: T8 (no address is ever removed) with LP13 keep `c` a persistent allocated address, and GlobalUniqueness (ASN-0034) keeps it uniquely identifying, but the freezing is state-independence alone."
**Problem**: This sentence exists to pre-empt the objection "isn't it allocation permanence that makes the address key work?" — it enumerates three foundation axioms in order to say they are *not* what is doing the work. That is a defensive justification; it does not advance the claim that `κ(a) = a` is state-stable, which the preceding sentence (`κ_Σ(a) = κ_{Σ'}(a) = a`) already establishes.
**Required**: Drop it, or compress to a phrase: the address key is state-stable because `κ(a) = a` is state-independent — no axiom citation needed.

### Issue 4: W7 re-states M-mut's loss direction with its full citation chain
**ASN-0108, W7**: "`Match(q, ·)` may lose members across evolution even though `dom(Σ.L)` only grows — the loss direction of (M-mut): a link delivered in window `i` may be absent from the recomputed matching set at a later window `j > i` if, between the calls, its matched endpoint content was removed from the consulted arrangement `d_q` (D-NONMONO's `K.μ⁻` case; ASN-0098 LP12) and it was thereby orphaned (M-mut's per-`d_q` sense)."
**Problem**: W7 cites `(M-mut)` and then re-derives it with the identical mechanism and citations (`D-NONMONO`'s `K.μ⁻` case, `LP12`, "orphaned") already given verbatim in the State section's M-mut. Two passages say the same thing in different words; only the windowing-specific consequence (delivered-in-`i`, absent-in-`j`; completeness relative to each call's state) is new content.
**Required**: Cite M-mut for the loss direction and keep only W7's own contribution — the per-window delivered-then-absent consequence and the present-tense completeness reading.

## OUT_OF_SCOPE

### Topic 1: Global ordering across multiple home documents
**Why out of scope**: The note correctly restricts the address key's allocation-monotonicity to a single home document (W6, and the caveat after W6a) and defers the multi-document enumeration discipline to Open Question 1. This is new territory, not a defect — the per-document scoping is honest and the deferral is appropriate.

### Topic 2: The cardinality/progress-sizing query
**Why out of scope**: W10 correctly states that absolute progress ("k of m") requires a separate cardinality operation and explicitly marks it "out of scope here," matching the scope exclusion of count-only retrieval (FINDNUMOFLINKSFROMTOTHREE). The correspondence between delivery order and a companion count is appropriately left to a future ASN (Open Question 5).

VERDICT: REVISE
