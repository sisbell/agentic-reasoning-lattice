# Review of ASN-0117

I read this as a non-destructive arrangement operation realized as an ASN‑0047 `K.μ⁻ + K.μ⁺` composite (or a lone `K.μ⁻` when `R = ∅`), with the content store held in strict frame. I checked the composite decomposition, the coupling discharge (J0/J1★/J1'★), the frame clauses, the gap‑closure arithmetic, the boundary cases, and the discoverability wp. The technical content is sound: the net effect of the composite genuinely equals ASN‑0082's left‑shift displacement (DEL‑SHIFT/DEL‑LEFT/DEL‑DOM read off D‑SHIFT/D‑L/D‑DOM), the `R = ∅` single‑`K.μ⁻` case correctly invokes J2 self‑sufficiency, the within‑document‑sharing subtlety in DEL‑REMOVE is handled by the count‑plus‑label‑vacancy form, and the wp is genuinely weakest (the reverse inclusion `D(d,Σ') ⊆ D(d,Σ)` is automatic under range shrinkage, so equality reduces to the stated per‑link existential). The boundary suite (leading span, suffix, delete‑all, sharing, transclusion) is thorough.

The one class of issue I surface is in the note's declared `review-mode.anti-bloat` lane.

## REVISE

### Issue 1: Link-survival-by-byte-anchoring restated across four sites
**ASN-0117, multiple sections**: The core fact — *a link anchors to I-addresses, not V-positions, so it survives deletion because the bytes persist* — is developed in full at least four times:
- the opening problem statement ("any links to those bytes remain stably attached");
- §"A span, not a position" ("A link is anchored to bytes (I-addresses), not to positions… A link could not survive deletion if deletion annihilated the bytes");
- §P4 ("A link's endsets reference I-addresses, not V-positions… The link is anchored to bytes that still exist; the strap stays attached");
- the transclusion worked example ("any link whose coverage contains a_3 or a_4 stays discoverable…").

**Problem**: In a ~7000-word note these are not distinct steps of an argument; the §"A span, not a position" link-witness paragraph and the §P4 development say the same thing in different words. A precise reader re-encounters the same claim and must check whether each instance adds content; they do not. This is the compounding pattern the anti-bloat lane targets.
**Required**: Keep one load-bearing site (P4, where LinkSurvival is formally established via LP3/LP12/LP16/LP17/LP18) and reduce the others to a single pointer or excise the restatement. The §"A span, not a position" section's distinct contribution (the span as the minimal unit exposing the binding/being seam) can stand without re-arguing link survival.

### Issue 2: Implementation-mechanics parenthetical in the delete-everything boundary
**ASN-0117, "delete everything" boundary**: "(We note only as an observation, not an abstract claim, that an implementation's internal index structure may retain shape after full deletion that a freshly-created empty document would not have; abstractly the two empty arrangements are query-indistinguishable…)"
**Problem**: This is implementation-mechanics commentary sitting in an abstract-spec boundary check; the only abstract content (both denote the empty partial function, hence indistinguishable) is one clause buried in a hedge.
**Required**: Drop the implementation-shape observation; keep the one-line abstract statement that both empty arrangements denote `∅` if it is needed at all.

## OUT_OF_SCOPE

(none beyond the topics the note already routes to its Open Questions — lower-boundary deletion, concurrency, content-discovery index, backtrack reconstructibility, and orphaned-link obligations are all properly deferred there rather than claimed.)

VERDICT: REVISE
