# Prose Sprawl

A claim's narrative prose — the derivation, preamble, or argumentative commentary around the Formal Contract — keeps growing across review cycles. The math stays sound; the prose accumulates meta-commentary that does not advance the reasoning.

Prose is legitimately where reasoning lives at the formalization stage. What grows under Prose Sprawl is *non-reasoning prose* — citation tracking, exhaustiveness claims, bundling justifications, and design-decision asides that belong in no layer of the claim.

## Forces

**Defensive justification.** The reviser answers review findings by inlining rebuttals in the prose. "We avoid the binary-minimum operator because...", "This bundling is chosen because...", "ActionPoint does not appear in this list because...". Each rebuttal addresses a past finding at the cost of new surface for future findings.

**Genesis Attractor.** A file positioned as the authoritative home for a concept pulls prose about that concept even after structural splits close other channels. T0's role as "definition of the carrier and its operators" attracted ℕ-arithmetic prose back into T0 after its contract had been slimmed to the carrier set only. See [Contract Sprawl: Limits of the Resolution](contract-sprawl.md#limits-of-the-resolution).

**Exhaustiveness obligations.** A sentence claiming completeness ("standard properties of ℕ that downstream proofs cite — X, Y, Z") creates a defense-of-completeness loop. Each cycle finds a gap; reviser extends the enumeration; larger enumeration produces new gaps.

**Citation accounting in prose.** Instead of metadata, reviser writes out use sites inline: "invoked at twenty-two distinct sites, each a clause of NAT-order's Axiom. Irreflexivity is invoked once, at part (a) Case (i)...". Belongs in structured metadata or dependency graphs, never in prose.

**Reviser prompt rewards verbosity.** Instructions interpreted as calling for "rigor" or "precision" by LLMs produce prose expansion by default. The prose layer has no downward pressure; every revision cycle adds surface.

## Signal

The claim's word count grows across review cycles faster than its reasoning content. Concrete markers:

- Paragraphs that introduce no new claim, proof step, witness, or invariant
- Nested parentheticals three or more levels deep
- Sentences whose sole content is the structure or scope of other sentences
- Phrases like "this list is exhaustive," "explicitly endorses," "stated scope," "matches the convention"
- Inline enumerations of use sites: "TumblerAdd uses this at `0 + wₖ = wₖ`, D0 uses this at..."

A mature claim file whose prose:structure ratio is not decreasing — or is rising — across cycles is showing Prose Sprawl.

## Example: T0's ℕ preamble

After the T0 split (see [Contract Sprawl](contract-sprawl.md)), T0's contract was reduced to the carrier set only. Its *prose*, however, grew a ~950-word run-on paragraph that enumerated all nine NAT-* axioms, justified the bundling of each, enumerated downstream consumers of each clause, defended the exhaustiveness of the enumeration, and explained why commutativity was excluded.

None of the paragraph advanced the claim about `T = finite sequences over ℕ`. All of it was meta: the structure of a list in a different file, the usage pattern of axioms declared in different files, and defenses against reviewer findings that had asked about that structure.

Four cycles, four distinct review findings, four prose extensions. No convergence.

## Resolution

**Prefer structural fixes over textual extensions.** Most review findings that produce Prose Sprawl offered the reviewer two resolutions: a textual extension and a structural fix. The textual fix was taken by default and the file grew. The structural fix — delete the meta-claim, rephrase the exhaustiveness, route citation tracking to metadata — eliminates the source of the finding. This is the [Surface Expansion](surface-expansion.md) discipline applied to the prose surface.

**Strip categorical bloat classes.** Regardless of force, certain prose classes are never load-bearing reasoning:

- Citation-site enumeration (belongs in structured metadata)
- Exhaustiveness claims (delete unless cheaply provable)
- Bundling-justification paragraphs (one sentence if needed; delete the rest)
- Naming-choice meta-explanation (the name speaks for itself)
- Inline design-decision commentary about other files

Removing these does not lose reasoning. It removes anti-reasoning — prose whose role was to defend against past findings rather than to argue for the claim.

**Change the site's role if it is also a Genesis Attractor.** Removing content without rewriting the scope statement leaves the attractor active; content re-accumulates in the next review cycle. The role has to change.

## Related

- [The Coupling Principle](../principles/coupling.md) — prose sprawl is a coupling violation: the prose:formal ratio drifts above the 70/30 target. The coupling principle's signal table and feedback loop show how this detection drives V-Cycle prompt calibration.
- [Contract Sprawl](contract-sprawl.md) — shares forces. Contract Sprawl concentrates in structural sections; Prose Sprawl concentrates in narrative.
- [Index Sprawl](index-sprawl.md) — enumerative prose is a specific surface form of Prose Sprawl.
- [Surface Expansion](surface-expansion.md) — the shared mechanism across Contract/Prose/Index Sprawl. Prose Sprawl is the narrative-surface manifestation; monitoring and the general discipline live at the Surface Expansion level.
- [Review V-Cycle](../design-notes/review-v-cycle.md) — prose bloat is detected at full-review when cycle findings reference prose introduced by the previous cycle's revisions.