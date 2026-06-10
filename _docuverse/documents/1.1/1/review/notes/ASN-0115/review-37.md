# Review of ASN-0115

I worked the proofs through. The core machinery is sound: the Confinement lemma discharges correctly from T5 + TumblerAdd (`p ≼ s`, `p ≼ reach(σ)`, then T5 with `s ≤ t ≤ reach(σ)`); R6's gap analysis correctly leans on D-SEQ★ to rule out interior holes in the bindable slice and on the `act = ∅`/`act ≠ ∅` split to pin the canonical start; R7's insistence on comparability (`Σ →* Σ'`) over mere common ancestry is genuinely load-bearing (divergent branches could re-allocate one address with two values); R8's link-vacuity follows from CL-OWN + CL-UNIQ; the wp in R11 correctly reduces to the single live condition with store-membership as automatic consequence rather than independent conjunct. Boundaries (empty spec-set, empty `act`, `V_S(d) = ∅`, terminal overrun, deeper-than-`m_S` named positions) are all handled. The worked instances check out arithmetically. I have no correctness finding.

The note carries the anti-bloat classifier, and there is one instance to surface.

## REVISE

### Issue 1: R8's "Three points deserve emphasis" inflates its justifications

**ASN-0115, R8 (TransclusionCoResolution)**: The box's three guarantees are sound and the three justifications below it are real. But the justification is wrapped in rhetorical scaffolding:

- (a) The First point appends a tangential aside — "`it is reference, not copy, and 'any detached copy someone keeps is frozen and dead' precisely because copying severs this`" — a philosophical flourish about *detached copies*, which RETRIEVEV never makes. The precise reader skips it to reach the next substantive sentence; it does not advance the reference-not-copy claim it decorates.
- (b) The First point closes with an inter-paragraph forward-deferral, "`That identity is a property of how the delivery is computed, not of the delivered bytes, as the next point makes precise`" — a signpost to the Second point rather than content.
- (c) The "`Three points deserve emphasis`" enumeration is essayistic framing over what are three justification steps (identity-preserving via the S4 contrast; no-disclosure via per-position resolution and no-comparison; no-merge forced by R3 and witnessed by the absent `consolidatespans`).

**Problem**: Essay content and forward-reference signposting in a justification slot — exactly the accretion pattern the anti-bloat pass targets. The substance (the three "why"s) is legitimate; the "deserve emphasis" framing, the detached-copy aside, and the "as the next point makes precise" deferral are not.

**Required**: State the three justifications in flowing prose — identity-preserving co-resolution (S4 contrast), the sharing is internal to resolution (per-position resolution, no comparison), no merge (forced by R3; absent `consolidatespans`) — without the "Three points deserve emphasis" enumeration, the "frozen and dead copy" aside, or the inter-point "as the next point makes precise" deferral.

## OUT_OF_SCOPE

The Open Questions already bound the genuine future territory correctly — inline-provenance delivery, fail-outright-vs-partial, unbound-reference resolution, channel faithfulness, and the single straddling-span case — and R10 correctly delivers a link *reference* (`⟨ref, a⟩`) rather than the link's endset structure, leaving READLINK/FOLLOWLINK untouched. No additional out-of-scope topics surface, and no in-scope claim strays into the deferred operations.

VERDICT: REVISE
