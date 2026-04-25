# Prose Sprawl

A claim's narrative prose — the derivation, preamble, or argumentative commentary around the Formal Contract — keeps growing across review cycles. The math stays sound; the prose accumulates meta-commentary that does not advance the reasoning.

Prose is legitimately where reasoning lives at the formalization stage. What grows under Prose Sprawl is *non-reasoning prose* — citation tracking, exhaustiveness claims, bundling justifications, and design-decision asides that belong in no layer of the claim.

## Forces

**Reviser add-bias.** When the reviser agent is handed a finding to fix, its default reflex is to *add* prose rather than restructure or delete. Two sub-modes:

- *Defensive justification.* The reviser answers review findings by inlining rebuttals in the prose. "We avoid the binary-minimum operator because...", "This bundling is chosen because...", "ActionPoint does not appear in this list because...". Each rebuttal addresses a past finding at the cost of new surface for future findings.
- *Move rather than delete.* When a reviewer says "drop X," the reviser relocates X to a different paragraph and considers the finding addressed. The drift persists; the next reviewer flags it again in its new home.

Together these constitute reviser add-bias: the prose grows monotonically even when each individual finding asked for simplification. The discipline that contains it is the [Voice Principle](../principles/voice.md) — positive style structure that leaves no slot for non-reasoning prose, rather than enumerated prohibitions that leave gaps.

**Genesis Attractor.** A file positioned as the authoritative home for a concept pulls prose about that concept even after structural splits close other channels. T0's role as "definition of the carrier and its operators" attracted ℕ-arithmetic prose back into T0 after its contract had been slimmed to the carrier set only. See [Contract Sprawl: Limits of the Resolution](contract-sprawl.md#limits-of-the-resolution).

**Exhaustiveness obligations.** A sentence claiming completeness ("standard properties of ℕ that downstream proofs cite — X, Y, Z") creates a defense-of-completeness loop. Each cycle finds a gap; reviser extends the enumeration; larger enumeration produces new gaps.

**Citation accounting in prose.** Instead of metadata, reviser writes out use sites inline: "invoked at twenty-two distinct sites, each a clause of NAT-order's Axiom. Irreflexivity is invoked once, at part (a) Case (i)...". Belongs in structured metadata or dependency graphs, never in prose.

**Tightening findings that trigger revision.** When every reviewer observation — including loose phrasing, minor style, and quantifier precision — triggers a revise cycle, each cycle adds surface through fixes that are correct but not worth their cost. The growth is driven not by the reviser's bias alone but by the volume of findings that reach the reviser. The REVISE/OBSERVE classification in the review prompt addresses this by preventing tightening findings from triggering revision at all.

## Signal

The claim's word count grows across review cycles faster than its reasoning content. Concrete markers:

- Paragraphs that introduce no new claim, proof step, witness, or invariant
- Nested parentheticals three or more levels deep
- Sentences whose sole content is the structure or scope of other sentences
- Phrases like "this list is exhaustive," "explicitly endorses," "stated scope," "matches the convention"
- Inline enumerations of use sites: "TumblerAdd uses this at `0 + wₖ = wₖ`, D0 uses this at..."

A mature claim file whose prose:structure ratio is not decreasing — or is rising — across cycles is showing Prose Sprawl.

Additional signal specific to reviser add-bias:

- **Finding N+1 flags content added in cycle N's revise.** If review cycle 5 flags a sentence the reviser introduced in cycle 1 or cycle 3, the driving force is the reviser's additions, not pre-existing prose drift. The revise commits are where the bloat originates.
- **Flagged-and-relocated content.** A paragraph flagged in cycle N reappears in a nearby paragraph in cycle N+1. Detectable from commit diffs: the reviser's revise commit shows a deletion *and* an insertion of similar content in a different location.

## Example: T0's ℕ preamble

After the T0 split (see [Contract Sprawl](contract-sprawl.md)), T0's contract was reduced to the carrier set only. Its *prose*, however, grew a ~950-word run-on paragraph that enumerated all nine NAT-* axioms, justified the bundling of each, enumerated downstream consumers of each clause, defended the exhaustiveness of the enumeration, and explained why commutativity was excluded.

None of the paragraph advanced the claim about `T = finite sequences over ℕ`. All of it was meta: the structure of a list in a different file, the usage pattern of axioms declared in different files, and defenses against reviewer findings that had asked about that structure.

Four cycles, four distinct review findings, four prose extensions. No convergence.

## Example: ASN-0034 TA-Pos cone (April 2026)

A six-cycle regional sweep on TA-Pos produced a cleaner instance of the add-bias pattern with a measurable trajectory. Findings per cycle: **5 → 1 → 1 → 2 → 4 → 4** — not monotonically decreasing.

The cycle-5 uptick contained defensive prose the reviser had introduced in cycle 1 when fixing the Pos/Zero dichotomy finding: a parenthetical about "a hypothetical length-0 tumbler" whose behavior under the biconditional was irrelevant because T0 excludes length-0 tumblers from `T`. Cycle 5 flagged the defensive prose. Cycle 6 then flagged it again — explicitly: "the response moved it to the content-of-partition paragraph rather than dropping it." The reviser had relocated rather than deleted.

Cycle 6 also flagged two other reviser-added pieces: a variable slip (`a` → `#t`) in T0 prose introduced when adding the `1 ≤ #a` axiom, and a misframed universal-as-existential in TA-Pos's Pos/Zero "witness" prose added in cycle 1.

The cone was halted after cycle 7 without convergence. Of ~17 findings across six cycles, four were reviser-introduced drift. The cone's pre-existing semantic issues (missing dichotomy, unformalized nonemptiness, overclaimed "additive identity") were legitimate and produced real axiomatic improvements — but each correct fix came with defensive prose that became the next cycle's review surface.

## Resolution

Two mechanisms contain Prose Sprawl, operating at different points in the pipeline:

**Voice discipline constrains what the reviser writes.** The [Voice Principle](../principles/voice.md) replaces enumerated prohibitions ("do not add defensive justifications, do not add meta-commentary...") with a positive style structure: the Dijkstra voice, where every formal statement must be justified in the sentence that introduces it, every claim must be named, and state is described rather than narrated. Under this discipline, non-reasoning prose has no slot to land in — the structure itself is the constraint. Empirically, the same cones that produced sprawl under prescriptive prohibition lists produced net-shrinking prose under voice discipline.

**Finding classification constrains what reaches the reviser.** The REVISE/OBSERVE classification in the review prompt separates correctness findings (must act) from tightening observations (logged, no action). Tightening findings — the class most likely to produce sprawl when acted on — do not trigger revision. The growth driver is removed because the reviser never sees the findings whose fixes would have added surface.

Together: voice shapes what the reviser writes when it does act, and classification determines when the reviser acts at all. Neither alone is sufficient — voice without classification still processes too many findings; classification without voice still produces add-biased fixes on the findings that do reach the reviser.

**Diagnostic markers remain useful.** Regardless of the resolution mechanism, certain prose classes are never load-bearing reasoning and their presence is a signal that sprawl has occurred:

- Citation-site enumeration (belongs in structured metadata)
- Exhaustiveness claims (defensible only if cheaply provable)
- Bundling-justification paragraphs
- Naming-choice meta-explanation
- Inline design-decision commentary about other files

These are recognition aids, not a stripping checklist. The discipline that prevents them is voice; the markers tell you when voice has slipped.

**Change the site's role if it is also a Genesis Attractor.** Removing content without rewriting the scope statement leaves the attractor active; content re-accumulates in the next review cycle. The role has to change.

## Related

- [The Voice Principle](../principles/voice.md) — the discipline that contains add-bias. Positive voice structure constrains the reviser to load-bearing prose by construction, replacing enumerated prohibition lists that proved unstable.
- [The Coupling Principle](../principles/coupling.md) — prose sprawl is a coupling violation: the prose:formal ratio drifts above the 70/30 target. The coupling principle's signal table and feedback loop show how this detection drives claim-convergence prompt calibration.
- [Contract Sprawl](contract-sprawl.md) — shares forces. Contract Sprawl concentrates in structural sections; Prose Sprawl concentrates in narrative.
- [Index Sprawl](index-sprawl.md) — enumerative prose is a specific surface form of Prose Sprawl.
- [Surface Expansion](surface-expansion.md) — the shared mechanism across Contract/Prose/Index Sprawl. Prose Sprawl is the narrative-surface manifestation; monitoring and the general discipline live at the Surface Expansion level.
- [Claim Convergence Protocol](../protocols/claim-convergence-protocol.md) — prose bloat is detected at full-review when cycle findings reference prose introduced by the previous cycle's revisions. The REVISE/OBSERVE classification operates within the protocol's review prompts.