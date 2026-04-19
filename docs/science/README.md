# Science Deployment: Approach

*Design note. Speculative — not yet run. How the [Two Data Authorities](../patterns/two-data-authorities.md) pattern and its supporting machinery (V-cycle, regional-review, lattice) would apply to scientific discovery. Core framing: the system produces hypotheses, not discoveries. Verification happens downstream.*

## Core claim

The system produces **hypotheses**, not discoveries — candidate principles articulated precisely enough to be tested. Verification (experimental, replication, or match against known answers) happens outside the system.

For a rediscovery evaluation, a hypothesis becomes a "finding" when it matches a known target. The AI still produced a hypothesis; the matching is external judgment.

## Convergence framework

### Verifier-relative convergence

Convergence is always relative to a downstream verifier. Different domains have different verifiers; the iterative machinery is the same.

| Scale | Operator | Science verifier |
|---|---|---|
| Local | local-review | hypothesis articulation (testable) |
| Regional | regional-review | cluster articulation (mutually consistent) |
| Full | full-review | framework coherence |

At each scale, the operator iterates until the relevant verifier finds no new issues. Science cones stabilize when hypotheses are articulated precisely enough to test. The [software deployment](../software/README.md) uses the same machinery with a different verifier (proof soundness via Dafny).

(All three scales use scale-based operator names: local-review, regional-review, full-review. The operator-name refactor is complete.)

### Cone as hypothesis cluster

A cone is an apex property plus its dependencies. In the science case, it serves as a hypothesis cluster:

- **Apex:** the hypothesis statement (a theorem-class claim)
- **Dependencies:** supporting axioms (e.g., kinetic theory background), definitions (operational: κ, σ), data-channel citations (specific measurements), coined concepts (e.g., "Lorenz number" as a named invariant)

Regional convergence of a cone = hypothesis ready for its scope.

### Sub-cluster vs. global ASN convergence

Multiple hypotheses can live in one ASN, each in its own cone. Cones converge independently because each apex has its own dependency set; cones don't necessarily share state.

A hypothesis is ready when its own cone regionally converges — doesn't require the whole ASN to be globally converged. One cone can be stable while another is still cycling. The WF cone can be hypothesis-ready while the Curie cone is still being refined.

Full ASN convergence (all cones regionally converged + no cross-cluster inconsistencies) is a stronger bar. Reserved for cases where the whole ASN is presented as a unified scientific model, not just a collection of independent hypotheses.

## Judger evaluation model

### Incremental per stable cone

The Judger evaluates cones as they stabilize, not only at end of run. As each cone reaches regional convergence, the Judger analyzes its apex against the target-principle list and records:

- **Match:** apex corresponds to a target principle → rediscovery
- **Novel candidate:** apex doesn't match any target → articulation-ready claim that isn't a rediscovery
- **Skip:** apex isn't a theorem-class claim (axiom, definition, design requirement) — not evaluated for match

Incremental evaluation lets you track progress during the run. Match rate accumulates as cones stabilize.

### Two kinds of convergence in play

- **Articulation convergence (AI-side):** cone stabilized; apex is testable. The AI has done its job.
- **Match convergence (eval-side):** apex matches known target. The external rediscovery metric.

A cone can articulation-converge without match-converging. Those land in the novel-candidate bucket.

## Deployment specifics for science

The underlying machinery (two-channel discovery, blueprinting, formalization, V-cycle, cone structure, scope promotion, lattice) is shared with the [software deployment](../software/README.md). What's specific to science:

- **Verifier at each V-cycle scale:** reproducibility-precision ("could another lab test this?") rather than proof-soundness.
- **Data channel:** query interface over measurements / simulation tools rather than code reading. Agent answers specific mechanical questions with cited values, not whole-source dumps.
- **Theory channel:** often more formally pre-shaped than a legacy-software designer's prose (equations and named operators already present). See [channel asymmetry in new-science domains](channel-asymmetry-new-science.md) for the shape implications.
- **Convergence bar:** protocol-specifiable rather than proof-citable.
- **External validation:** experimental test (or match-eval) rather than mechanical verification.

## Related

- [Software Approach](../software/README.md) — parallel framing for software reverse-engineering (the grounded deployment)
- [Channel Asymmetry](../patterns/channel-asymmetry.md) — pattern; why shape-mismatch between channels forces coinage
- [Channel Asymmetry in New-Science Domains](channel-asymmetry-new-science.md) — how channel asymmetry applies in scientific deployments (modality / numerical-observation axis)
- [Two Data Authorities](../patterns/two-data-authorities.md) — parent pattern
- [Review V-Cycle](../design-notes/review-v-cycle.md) — multi-scale review architecture
- [Dependency Cone](../patterns/dependency-cone.md) — tight-coupling signal; relevant for non-converging hypothesis clusters
