# Production Drive

*Design note. An LLM behavioral force that pushes toward action. Off-ramp categories in review classification exist to channel this force safely.*

## The force

LLMs generate text. Generation is the fundamental action. When an LLM reviewer reads content, it finds things to say about it — observations, tightenings, possible improvements, alternative framings. The drive is toward production: engage with the material, generate analysis, trigger action.

Without structure to channel this drive, every observation becomes a mandatory action. Every finding triggers a revision. Every interesting topic encountered during review becomes in-scope work. The review cycle over-revises (surface expansion from unnecessary fixes) and over-expands (scope creep from engaging with material that belongs elsewhere).

This is the same force that produces add-bias at the revision layer. The reviser generates text rather than deleting because generation is the fundamental action. The reviewer generates findings and pushes them toward action categories because action is the fundamental output. Same drive, two layers.

## The off-ramps

Classification categories that permit production without triggering action are the design response to the production drive.

**OBSERVE** (claim convergence review). The reviewer produces its observation — satisfying the drive — without triggering a revise cycle. Without OBSERVE, every observation the reviewer generates becomes REVISE. The reviewer can't say "I noticed this, it's not worth acting on." Every tightening opportunity, every stylistic preference, every minor quantifier imprecision triggers a revision whose fix adds surface that becomes the next cycle's review target. The result is [Surface Expansion](../equilibrium/surface-expansion.md) driven not by the reviser's bias but by the reviewer's inability to observe without acting.

**OUT_OF_SCOPE** (discovery review). The reviewer engages with interesting material it encounters — satisfying the drive — without committing the note to covering it. Without OUT_OF_SCOPE, the reviewer's engagement with adjacent topics becomes in-scope derivation. The note expands to cover material that belongs in a future inquiry. OUT_OF_SCOPE channels the engagement into [scope promotion](../patterns/scope-promotion.md) — the finding becomes a candidate for a new inquiry rather than an obligation on the current note.

Both off-ramps have the same structure: they let the LLM produce (satisfying the drive) without triggering downstream consequences (preventing over-action). The off-ramp is not a problem to manage. It is the solution to the production drive.

## What goes wrong without off-ramps

The system operated without OBSERVE during early claim convergence. Every reviewer finding was binary — CLEAN or FOUND. Every FOUND triggered a revise. The result: tightening findings (loose phrasing, minor style, alternative framings) generated revisions whose fixes added prose, whose prose generated new findings, whose findings generated new revisions. The surface expanded monotonically. Cones ran eight cycles without converging. The reviewer was doing its job (noticing real imperfections) and the system was punishing it (every observation forced action).

Adding OBSERVE gave the reviewer a way to notice without forcing action. The convergence criterion changed from "zero findings" (unreachable — prose is never perfect under infinite scrutiny) to "zero REVISE findings" (reachable — correctness issues are exhaustible). The off-ramp made convergence possible.

## Calibration

The off-ramp must be calibrated so that legitimate action items don't get swept into it alongside the noise. If OBSERVE absorbs genuine REVISE items — ungrounded symbols, structural inconsistencies — the off-ramp is too attractive and the cone doesn't converge for a different reason: correctness issues are parked instead of fixed.

Two mechanisms calibrate the off-ramp:

**The discrimination test.** A classification-time threshold with concrete positive triggers for action (ungrounded symbol, unjustified inference, missing case, unsound proof step, structural inconsistency, silent precondition, unresolved reference) and a narrow definition of the off-ramp (strictly non-load-bearing observations where a reasonable reader could leave the claim unchanged). Findings default to REVISE; OBSERVE must be justified against the narrow criteria. A prior formulation framed the test as "would an incorrect fix be worse than leaving it?" — which read as a safety check and biased classifications into the off-ramp regardless of whether the finding named a concrete action trigger. The current REVISE-first formulation names the triggers directly. Stated in the review prompt, operates at classification time.

**Voice discipline.** The [Voice Principle](../principles/voice.md) reduces the number of findings generated in the first place. "Dijkstra speaks only when genuinely compelled" makes silence a disciplined performance rather than a failure to produce. The reviewer generates fewer observations because the voice frames not-emitting as rigor. Fewer findings generated means fewer findings to classify, means less pressure on the off-ramp.

Voice reduces volume. The discrimination test routes what remains. Together they keep the off-ramp from absorbing action items while still providing the pressure relief the production drive requires.

## Related

- [The Voice Principle](../principles/voice.md) — voice discipline reduces the volume of findings the production drive generates. The off-ramp handles what remains after voice has done its work.
- [Convergence Protocol](../protocols/convergence-protocol.md) — the off-ramp categories (OBSERVE, OUT_OF_SCOPE) are specializations of the convergence protocol's `comment` subtypes. Only `comment.revise` participates in the convergence predicate.
- [Note Convergence Protocol](../protocols/note-convergence-protocol.md) — uses OUT_OF_SCOPE as the off-ramp. Channels the production drive into lattice growth through scope promotion.
- [Claim Convergence Protocol](../protocols/claim-convergence-protocol.md) — uses OBSERVE as the off-ramp. Channels the production drive into audit trail without blocking convergence.
- [Surface Expansion](../equilibrium/surface-expansion.md) — the failure mode when there is no off-ramp. Every observation triggers action; action adds surface; surface generates observations. The off-ramp breaks the loop.
- [Prose Sprawl](../equilibrium/prose-sprawl.md) — add-bias is the revision-layer manifestation of the same production drive. Voice discipline addresses add-bias at revision; the off-ramp addresses the production drive at classification.
- [Scope Promotion](../patterns/scope-promotion.md) — OUT_OF_SCOPE is an off-ramp that produces real lattice growth. The production drive's engagement with adjacent material, channeled through scope promotion, becomes new inquiries.
- [Self-Healing Areas](../design-notes/self-healing.md) — off-ramp calibration is an observation-layer concern. An over-attractive off-ramp is a form of detection failure: the system sees the issue but doesn't act.