# Channel Asymmetry in New-Science Domains

*Design note. How the [Channel Asymmetry pattern](../patterns/channel-asymmetry.md) applies when deploying the system on a new scientific domain. First-run evidence from a materials lattice (April 2026) — Maxwell 1867 theory paired with Dulong & Petit 1819 measurements — is folded in below.*

## Symbolic theory × numerical observation

A common class of scientific domains pairs symbolic predictive theory (equations, named operators from established formalism) with numerical observational data (measurements, spectra, simulation outputs). Materials science, physics, and much of chemistry fit this shape.

The incommensurability here lives primarily on **modality** — theory speaks in equations and named operators; data speaks in values and instrument metadata. These don't concatenate: a numeric spectrum can't be pasted into a formal expression without interpretation. **Abstraction level** contributes secondarily: theory idealizes (non-interacting electrons, perfect lattices), data is specific (real samples with impurities, defects, finite size).

## How the evidence channel is shaped depends on corpus size

Operationally the evidence channel has two shapes, chosen by the size and structure of the observational source:

- **Whole-corpus injection** — when the evidence is a bounded historical paper, tabulated result set, or curated excerpt that fits in context. The agent sees the full text and cites directly. This matches the shape of the legacy-software designer channel, where a bounded specification is injected wholesale.
- **Query interface over raw sources** — when the evidence is a large dataset, spectral archive, or simulation output. No LLM can meaningfully process thousands of spectrum points or full trajectories in context. The channel becomes an agent with access to archives or simulation tools that answers specific mechanical questions ("what is κ for copper at 300K?") with cited values. The raw source stays native; only the channel's *answers* are structured. Same structural pattern as the legacy-software *code* channel, which reads code on demand.

In either shape, the theory channel stays distinct: it carries vocabulary, operator names, and voice/era constraints rather than raw content.

## Observed on materials

The first materials run used whole-corpus injection on the evidence side: Dulong & Petit's 1819 paper (~27KB) was fed directly to the evidence agent. The theory side got vocabulary from Maxwell 1867 (vis viva, β, elastic encounter) plus constraints forbidding modern terminology (degrees of freedom, equipartition by name, Boltzmann, statistical mechanics).

The notes stayed in-era: the synthesis did not short-circuit to 3R, Boltzmann, or the modern degrees-of-freedom count. Constraint-shaping on the theory channel, combined with whole-corpus injection on the evidence channel, held the agent inside the target era's conceptual apparatus.

**What the run did not test.** The Dulong–Petit corpus names its own central observation (the "law of Dulong and Petit"); there was no unnamed anomaly for the synthesis to bridge. The pattern's coinage-at-anomalies prediction was not exercised. What did occur was a *scope-softening relabel*: the synthesis renamed the corpus's "equal-atomic-heat-capacity law" to "atomic-heat regularity," refusing to inherit the strength of the 1819 name. That is a real discipline behavior — the agent declines to promote a historical "law" beyond what the underlying evidence (4.2% scatter across thirteen elements) actually supports — but it is not the anomaly-bridging coinage the pattern predicts.

Testing the coinage prediction would require a corpus containing observations for which existing era-appropriate vocabulary has no name. The DP target is the wrong experiment for that; it is the right experiment for testing memorization discipline and scope restraint.

## Implication for the pattern

What held, in the observable sense: whole-corpus injection on the evidence side combined with vocabulary+constraint shaping on the theory side produces in-era synthesis. The coinage dynamic remains conjectured for the modality axis; a follow-up run on a corpus with unnamed anomalies is required to test it.

The one refinement from observation: **whole-corpus injection is a legitimate evidence-channel shape** for historical or bounded data, not a degenerate case that must be replaced by a query interface. The query-interface shape remains necessary for large datasets, but it is not the only shape.

## Related

- [Channel Asymmetry](../patterns/channel-asymmetry.md) — the parent pattern this note extends
- [Two Data Authorities](../patterns/two-data-authorities.md) — parent of the parent
