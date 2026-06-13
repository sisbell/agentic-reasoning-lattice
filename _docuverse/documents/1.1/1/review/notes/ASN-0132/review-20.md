# Review of ASN-0132

This is a careful note. The central decision — that the unit of counting is link identity (CN-UNIT) — is argued through all four competing units rather than asserted; CN-MONO carries a genuine two-case weakest-precondition derivation in which the precondition is shown idle in the ordinary case and load-bearing in the retraction case; and the two worked examples (the frozen store and the census-in-motion) check out under arithmetic verification, including the prefix-incomparability of the link siblings, the coverage bounds of `F`, and the home-set bite at `d₂`. The dependency citations are all to foundation ASNs (0034, 0036, 0043, 0047, 0058, 0086, 0093, 0098, 0121, 0127); no notation is reinvented; J4's "no other elementary steps" clause does discharge the version-refraction reduction in CN-UNIT (d).

Two issues remain.

## REVISE

### Issue 1: CN-ORPHAN states "the gap is exactly the orphans" against the wrong baseline
**ASN-0132, "Counting the unsurfaced"**: "the counted set is a superset of what any document surfaces (the cross-document reach FL-REACH, ASN-0121), so the count is at least the number of links any one document surfaces. **The gap is exactly the orphans.**"

**Problem**: Two different baselines are juxtaposed and the gap claim is attached to the wrong one. FL-REACH bounds the count by the *union* `⋃_d { a : addressable ∧ sat ∧ discoverable_from(a, d) }`, and `count − |⋃_d ...| = orphans` is correct against that union. But the sentence immediately before "The gap is exactly the orphans" establishes a *single-document* baseline ("the count is at least the number of links any one document surfaces"). Against a single fixed `d`, the gap is

`count − |{a : addressable ∧ sat ∧ discoverable_from(a, d)}| = orphans ∪ {a : addressable ∧ sat, discoverable from some d' but not d}`,

which strictly exceeds the orphan count whenever any satisfying link is surfaced by a document other than `d`. So "the gap is exactly the orphans" is false against the singular baseline the preceding clause just named, and true only against the union baseline that clause skipped over. The summary-table entry inherits the same ambiguity ("a superset of what any document surfaces, the gap being exactly the orphans").

**Required**: Tie the gap to the union explicitly — e.g., "`count` exceeds `|⋃_d {satisfying, addressable, discoverable-from-d}|` (FL-REACH) by exactly the orphans; it exceeds any *single* document's surfaced count by at least the orphans, and generally more." Either drop the intervening "any one document" clause or distinguish the two baselines.

### Issue 2: CN-RETRACT restates the view/store distinction past the point it has been made
**ASN-0132, "Retraction and permanence"**: after the substantive sentence "The two statements — gone from the count and kept in the store — are about two different sets: the active view shrinks while the store does not," the paragraph continues: "**This is the count-level form of the view/store distinction the architecture maintains everywhere**: withdrawal removes a thing from the current arrangement of what is active, never from the permanent record of what exists. A count taken against the active view excludes the withdrawn link at once; a count that could be taken against a prior view would still include it. **Both are honest, because each counts the set it names.**"

**Problem**: The substantive content (two different sets; immediate exclusion; persistence in store) is complete before the bolded sentences. The "count-level form of the view/store distinction the architecture maintains everywhere" sentence is a thematic restatement, and "Both are honest, because each counts the set it names" is a closing flourish; neither advances the reasoning of CN-RETRACT. This is one instance of a recurring "this is the count-level form/expression of [foundation property]" signpost (cf. CN-STAB: "the count-level expression of the survivability of links under editing"), where CN-ENUM already establishes once that count mirrors enumeration. The flagged note carries `review-mode.anti-bloat`; this is the kind of thematic accretion it targets.

**Required**: Cut the architectural restatement and the "Both are honest" flourish; retain "the active view shrinks while the store does not" and the prior-view contrast (the latter does introduce a genuinely new object). Lean on CN-ENUM once rather than re-announcing the count-mirrors-enumeration relationship at each claim.

## OUT_OF_SCOPE

### Topic 1: the deferred open questions
**Why out of scope**: The six open questions — content-identity-vs-V-position count agreement, the concurrency discipline making count-equals-length hold across two inquiries, caching conditions, fragmented-endset deduplication, count-vs-enumeration cost asymmetry, and federated count — are correctly deferred. In particular the deduplication question (#4) is the right home for the Gregory back-end defect the implementation note records; the ASN correctly frames that defect as a deviation *from* CN-UNIT rather than evidence against it, and does not attempt to specify the dedup guarantee here. No scope violation: CN-ENUM relates to but does not redefine ASN-0121's enumeration, and CN-OBT scopes delivery out rather than specifying it.

VERDICT: REVISE
