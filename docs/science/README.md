# Science Domain: Approach

*Design note. Discovery stage first-run landed on a materials lattice (April 2026); downstream stages (claim convergence, Judger match-eval) still to run. How the [Two Data Authorities](../patterns/two-data-authorities.md) pattern and its supporting machinery (claim convergence protocol, lattice) applies to scientific discovery. Core framing: the system produces hypotheses, not discoveries. Verification happens downstream.*

## Core claim

The system produces **hypotheses**, not discoveries — candidate principles articulated precisely enough to be tested. Verification (experimental, replication, or match against known answers) happens outside the system.

For a rediscovery evaluation, a hypothesis becomes a "finding" when it matches a known target. The AI still produced a hypothesis; the matching is external judgment.

## Observed on materials (discovery stage)

First run landed on the Dulong–Petit target under a single-campaign materials lattice (`dulong-petit-maxwell`): Maxwell's 1867 *Dynamical Theory of Gases* (theory channel) paired with Dulong & Petit's 1819 specific-heat paper (evidence channel). See [Campaigns](../design-notes/campaigns.md) for how campaigns bind a channel pair to a target and bridge vocabulary, letting one lattice support multiple simultaneous investigations.

Two notes produced:

- **ASN-0001** (broad inquiry, no `out_of_scope`): 18 claims spanning ontology, temperature, pressure, phases, intermolecular forces, Dulong–Petit. A survey.
- **ASN-0002** (foundation inquiry, `out_of_scope` excluding pressure/phase/transport): 15 claims disciplined to the constitution+heat layer. Explicitly flagged what is *postulated* from Clausius vs *derived*. Cleaner foundation.

What discovery demonstrated:
- **Hypothesis-shaped output:** both notes produced P-claims (propositions) and Σ-states (abstract state) with explicit "introduced" status — the shape the Judger needs.
- **Memorization discipline held:** neither note short-circuited to 3R, Boltzmann, Einstein/Debye, or "statistical mechanics." The DP regularity was correctly framed as approximate and regime-gated, consistent with Maxwell's β framework rather than the modern answer. Two minor terminology leaks ("degrees of freedom" once, an `equipartition` label) but prose stayed in-era.
- **Scope discipline via `out_of_scope`:** ASN-0002's narrower inquiry + explicit exclusions produced a tighter, more honest foundation note than ASN-0001's broad inquiry. Confirms the pattern that broad inquiries survey and narrower inquiries tighten.
- **Channel asymmetry on the modality axis:** theory channel carried vocabulary (vis viva, β, elastic encounter) and voice constraints; evidence channel carried the whole 1819 corpus. The configuration ran as predicted, but the corpus contained no unnamed anomaly — the coinage-at-anomalies prediction of the pattern was not exercised. What did emerge was scope-softening: the synthesis relabeled the corpus's "equal-atomic-heat-capacity law" as "atomic-heat regularity," refusing to inherit the strength of the historical name.

What remains untested:
- Whether the claim convergence protocol converges hypothesis cones on materials notes.
- Whether the Judger match-eval correctly identifies rediscovery vs novel candidate.
- Whether scope promotion behaves as it does on the software domain.
- Whether the channel-asymmetry pattern's coinage-at-anomalies prediction holds on materials. The Dulong–Petit corpus names its own central observation ("law of Dulong and Petit"), so no unnamed anomaly forced coinage in this run. A corpus with observations that existing vocabulary cannot absorb would be needed to test the prediction.

## Convergence framework

### Verifier-relative convergence

Convergence is always relative to a downstream verifier. Different domains have different verifiers; the iterative machinery is the same.

| Scope | Verifier concern |
|---|---|
| Cone (adaptive) | hypothesis articulation (testable) |
| Comprehensive | framework coherence |

At each scope, the [claim convergence protocol](../protocols/claim-convergence-protocol.md) iterates until the convergence predicate holds — every `comment.revise` has a `resolution`. Science cones stabilize when hypotheses are articulated precisely enough to test. The [software domain](../software/README.md) uses the same protocol with a different verifier (proof soundness via Dafny). Scope strategies (adaptive/cone-scoped, comprehensive) are choreography decisions within the protocol, not protocol-level constructs.

### Cone as hypothesis cluster

A cone is an apex claim plus its dependencies. In the science case, it serves as a hypothesis cluster:

- **Apex:** the hypothesis statement (a theorem-class claim)
- **Dependencies:** supporting axioms (e.g., kinetic theory background), definitions (operational: κ, σ), data-channel citations (specific measurements), coined concepts (e.g., "Lorenz number" as a named invariant)

Convergence of a cone = hypothesis ready for its scope.

### Sub-cluster vs. global note convergence

Multiple hypotheses can live in one note, each in its own cone. Cones converge independently because each apex has its own dependency set; cones don't necessarily share state.

A hypothesis is ready when its own cone converges — doesn't require the whole note to be globally converged. One cone can be stable while another is still cycling. The WF cone can be hypothesis-ready while the Curie cone is still being refined.

Full note convergence (all cones converged + no cross-cluster inconsistencies) is a stronger bar. Reserved for cases where the whole note is presented as a unified scientific model, not just a collection of independent hypotheses.

## Judger evaluation model

### Incremental per stable cone

The Judger evaluates cones as they stabilize, not only at end of run. As each cone reaches convergence, the Judger analyzes its apex against the target-principle list and records:

- **Match:** apex corresponds to a target principle → rediscovery
- **Novel candidate:** apex doesn't match any target → articulation-ready claim that isn't a rediscovery
- **Skip:** apex isn't a theorem-class claim (axiom, definition, design requirement) — not evaluated for match

Incremental evaluation lets you track progress during the run. Match rate accumulates as cones stabilize.

### Two kinds of convergence in play

- **Articulation convergence (AI-side):** cone stabilized; apex is testable. The AI has done its job.
- **Match convergence (eval-side):** apex matches known target. The external rediscovery metric.

A cone can articulation-converge without match-converging. Those land in the novel-candidate bucket.

## Domain specifics for science

The underlying machinery (two-channel discovery via the [consultation protocol](../protocols/consultation-protocol.md), note convergence, claim derivation, claim convergence, cone structure, scope promotion, lattice) is shared with the [software domain](../software/README.md). What's specific to science:

- **Verifier at each scope:** reproducibility-precision ("could another lab test this?") rather than proof-soundness.
- **Evidence channel:** query interface over measurements / simulation tools rather than code reading. Agent answers specific mechanical questions with cited values, not whole-source dumps.
- **Theory channel:** often more formally pre-shaped than a legacy-software designer's prose (equations and named operators already present). See [channel asymmetry in new-science domains](channel-asymmetry-new-science.md) for the shape implications.
- **Convergence bar:** protocol-specifiable rather than proof-citable.
- **External validation:** experimental test (or match-eval) rather than mechanical verification.

## Related

- [Software Approach](../software/README.md) — parallel framing for software reverse-engineering (the grounded domain)
- [Channel Asymmetry](../patterns/channel-asymmetry.md) — pattern; why shape-mismatch between channels forces coinage
- [Channel Asymmetry in New-Science Domains](channel-asymmetry-new-science.md) — how channel asymmetry applies in scientific domains (modality / numerical-observation axis)
- [Two Data Authorities](../patterns/two-data-authorities.md) — parent pattern
- [Consultation Protocol](../protocols/consultation-protocol.md) — the two-channel consultation with vocabulary firewall and synthesis integrity
- [Note Convergence Protocol](../protocols/note-convergence-protocol.md) — drives notes to stability during discovery
- [Claim Convergence Protocol](../protocols/claim-convergence-protocol.md) — drives claims to formal precision; cone-scoped and comprehensive review as choreography
- [Dependency Cone](../patterns/dependency-cone.md) — tight-coupling signal; relevant for non-converging hypothesis clusters