# Surface Expansion

Across successive review cycles, a claim's textual surface grows monotonically without corresponding growth in reasoning content. Each cycle's revisions net-add rather than net-remove. The file gets longer. Convergence does not arrive.

Surface expansion is the shared mechanism underneath [Contract Sprawl](contract-sprawl.md), [Prose Sprawl](prose-sprawl.md), and [Index Sprawl](index-sprawl.md). Those patterns name *where* expansion lands — formal contracts, narrative prose, enumeration lists. Surface expansion names the dynamic itself.

Convergence is coupling-holding at the artifact's natural ratio, not monotonic contraction. Each artifact has its own target — see [The Coupling Principle](../principles/coupling.md). Surface expansion is *decoupling*: one half (prose or formal) grows without the other, pushing the ratio off-target. Contraction is how a claim re-enters the target ratio after expansion; it is not the convergence state itself.

## Forces

**Textual-fix default.** Reviews routinely present two valid resolutions for a finding: (a) extend the prose to address it, or (b) restructure to dissolve the obligation that produced it. Revisers default to (a). The textual fix is locally cheaper, literally addresses the finding, and feels like direct engagement with the reviewer. The structural fix requires interpretive work and risks new findings.

**New surface attracts new findings.** Each added sentence is a new statement future reviewers can audit. An added exhaustiveness claim produces completeness-audit findings. An added citation enumeration produces citation-accounting findings. An added bundling justification produces bundling-audit findings. Surface breeds surface.

**Defensive justification.** Revisers answer review findings by inlining rebuttals into the prose rather than restructuring away the finding's premise. Each rebuttal addresses a past finding at the cost of new surface for future ones.

**Tightening findings that trigger revision.** When every reviewer observation — including loose phrasing, minor style, and quantifier precision — triggers a revise cycle, each cycle adds surface through fixes that are correct but not worth their cost. The growth is driven not by the reviser's bias alone but by the volume of findings that reach the reviser.

All four forces above drive prose expansion. The opposite direction — formal content growing without corresponding prose — is also surface expansion but manifests silently as stalled generative output rather than visible bloat. See the asymmetric failure modes in [The Coupling Principle](../principles/coupling.md).

## Signal

Surface expansion is directly measurable. Unlike the Sprawl patterns, which require a diagnostician to classify *where* expansion landed, surface expansion can be detected from file-level metrics.

Leading indicators:

- **Word delta per claim across cycles** — net-positive across N consecutive cycles
- **Prose:structure ratio trajectory** — rising over cycles indicates prose accumulating around stable structure
- **Net-add vs net-remove per revision** — a reviser whose revisions systematically net-add
- **Cycles since last contraction** — elapsed cycles without any net-remove revision

These indicators fire *before* the specific Sprawl variant is diagnosable. Monitoring can intervene on surface expansion without knowing yet whether the expansion is landing in the contract, in the prose, or in an enumeration.

Once expansion is confirmed, the Sprawl patterns take over as site-specific diagnostics: read the claim to see which surface is the site, then apply that pattern's resolution.

## Resolution

Two mechanisms contain surface expansion, operating at different stages.

**Voice discipline constrains what the reviser writes.** The [Voice Principle](../principles/voice.md) defines well-formed output through positive style structure — the Dijkstra voice, where every formal statement must be justified in the sentence that introduces it, every claim must be named, and state is described rather than narrated. Under this discipline, non-reasoning prose has no slot to land in. The structure itself is the constraint. Enumerated prohibition lists ("delete > restructure > add") proved unstable — too lax and the reviser adds; too strict and the reviser over-deletes. Voice discipline sidesteps the Goldilocks problem by defining what good prose looks like rather than listing what bad prose looks like.

**Finding classification constrains what reaches the reviser.** The REVISE/OBSERVE classification in the review prompt separates correctness findings (must act) from tightening observations (logged, no action). Tightening findings — the class most likely to produce expansion when acted on — do not trigger revision. The growth driver is removed because the reviser never sees the findings whose fixes would have added surface.

Together: voice shapes what the reviser writes when it does act, and classification determines when the reviser acts at all. Neither alone is sufficient — voice without classification still processes too many findings; classification without voice still produces add-biased fixes on the findings that do reach the reviser.

**When textual fixes are correct.** Genuine errors in reasoning, missing definitions, and incomplete proofs are textual by nature — add the missing content. The discipline is specifically against *meta-prose accretion*: prose whose role is to defend, justify, enumerate, or track rather than to reason. These categories remain useful as diagnostic markers — their presence signals that expansion has occurred — but the resolution is voice discipline plus finding classification, not a stripping checklist.

**For site-specific resolution, see the Sprawl patterns.** Contract Sprawl resolves by splitting Genesis Attractors. Prose Sprawl resolves by voice-constrained revision. Index Sprawl resolves by dropping exhaustiveness claims at their source.

## Origin

Observed across ASN-0034's review history (April 2026). Across ~6 review cycles and 80 claim files, total word count grew to 190,940 words. A compress pass — removing exhaustiveness claims, defensive justifications, inline citation tracking, bundling rationales, and naming-choice commentary — reduced it to 49,843 words (73.9% reduction) with no loss of reasoning.

Cycle-by-cycle inspection showed the same dynamic everywhere: reviews offered structural and textual resolutions; revisers took the textual ones; added surface attracted next-cycle findings; the file grew again. No cycle contracted.

Two specific cases in that history are preserved as reviewer-offered-escape-not-taken:

- **review-133 (April 17 2026).** T0's NAT-* enumeration: reviewer offered (a) extend the enumeration or (b) rephrase T0 so the list is non-exhaustive. Reviser took (a). T0 grew into the state that later required a full compress pass.
- **review-207 (April 17 2026).** TumblerAdd vs NAT-addassoc asymmetry: reviewer offered (a) integrate NAT-addassoc into T0's enumeration or (b) soften TumblerAdd's exhaustiveness language. Reviser took (a). NAT-addassoc.md grew from 6 lines to 20+ with an inline listing of its eight siblings — Index Sprawl in a file that needed none.

Both cases offered the structural fix in writing. Both took the textual fix. Both produced Sprawl that required separate cleanup.

## Surface expansion blinds review

A second-order observation from the April 2026 claim-convergence rerun of ASN-0034/TumblerAdd, after the compress pass and coupling-prompt updates.

Three cycles of the rerun produced three findings: a missing NAT-discrete contrapositive citation in T1 Case 1, an unstitched `≥` abbreviation in TumblerAdd's dominance conclusion, and an ambiguous NAT-cancel summand-absorption form. All three were genuine coupling gaps. All three were present throughout the pre-compress review history. **None had been found in the earlier cycles.**

Surface expansion does not just consume review cycles with noise — it prevents the reviewer from detecting real structural issues. A bloated file can run convergence cycles indefinitely without surfacing the coupling gaps it contains, because the reviewer's attention is occupied by the defensive meta-prose the Sprawl produced. Signal stays below the noise floor.

This reframes the cost of Sprawl. Beyond the direct cost (wasted cycles, ratio drift, maintenance burden), Sprawl silently corrupts the review process itself. Convergence is not merely delayed — it is unreachable on Sprawl-accumulating files, because the defects the review cycle is meant to find stay hidden.

The discipline the Coupling Principle enforces is therefore not a cleanliness preference. Restoring a file to its target ratio does not just reduce waste; it restores the reviewer's capability to find and fix coupling gaps that may have accumulated invisibly throughout the Sprawl-affected cycles.

## Related

- [Contract Sprawl](contract-sprawl.md), [Prose Sprawl](prose-sprawl.md), [Index Sprawl](index-sprawl.md) — site-specific manifestations of surface expansion. Use these for diagnosis once expansion is detected; use this doc for the shared mechanism and for monitoring.
- [The Voice Principle](../principles/voice.md) — the discipline that contains add-bias. Positive voice structure constrains the reviser to load-bearing prose by construction, replacing enumerated prohibition lists that proved unstable.
- [The Coupling Principle](../principles/coupling.md) — the parent discipline. Surface expansion is a coupling violation; the coupling principle's feedback loop shows how detection flows from delta-from-target through the Sprawl patterns.
- [Accretion](../patterns/accretion.md) — the healthy growth pattern. Accretion adds new claims without mutating existing ones; surface expansion is what happens when claims mutate instead.
- [Review/Revise Iteration](../patterns/review-revise-iteration.md) — the cycle within which expansion or contraction happens. Each iteration is a decision point where the voice discipline and finding classification operate.
- [Claim Convergence Protocol](../protocols/claim-convergence-protocol.md) — the full-review scale at which cumulative surface expansion becomes detectable across multiple claims at once. The REVISE/OBSERVE classification operates within the protocol's review prompts.