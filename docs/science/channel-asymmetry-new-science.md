# Channel Asymmetry in New-Science Domains

*Design note. Speculative. How the [Channel Asymmetry pattern](../patterns/channel-asymmetry.md) might apply when deploying the system on a new scientific domain. Extrapolation from one case (Xanadu) to a different axis; should be treated as conjecture rather than validated recipe.*

## Symbolic theory × numerical observation

A common class of scientific deployments would pair symbolic predictive theory (equations, named operators from established formalism) with numerical observational data (measurements, spectra, simulation outputs). Materials science, physics, and much of chemistry fit this shape.

The incommensurability here lives primarily on **modality** — theory speaks in equations and named operators; data speaks in values and instrument metadata. These don't concatenate: a numeric spectrum can't be pasted into a formal expression without interpretation. **Abstraction level** contributes secondarily: theory idealizes (non-interacting electrons, perfect lattices), data is specific (real samples with impurities, defects, finite size).

Operationally, the data channel can't dump raw numerical data into synthesis — no LLM can meaningfully process thousands of spectrum points or full simulation trajectories in context. It functions as a *query interface* over the raw sources: an agent with access to archives, instrument output, or simulation tools that answers specific mechanical questions ("what is κ for copper at 300K?") with cited specific values. Same structural pattern as the legacy-software case, where the data channel reads code on demand rather than handing the whole source over. The raw source stays native; only the channel's *answers* are structured.

If the [Channel Asymmetry](../patterns/channel-asymmetry.md) pattern holds, the dynamic should still emerge in this configuration, but through this different axis. Coinage would concentrate at anomalies — where existing formalism can't absorb the observed behavior. Inside well-covered regimes synthesis functions as validation; at the frontier it coins new terms to name whatever bridges the discrepancy.

## Related

- [Channel Asymmetry](../patterns/channel-asymmetry.md) — the parent pattern this note extends
- [Two Data Authorities](../patterns/two-data-authorities.md) — parent of the parent
