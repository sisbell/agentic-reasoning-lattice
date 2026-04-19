# Software Reverse-Engineering: Approach

*Design note. Grounded — demonstrated on the Xanadu hypertext system. How the [Two Data Authorities](../patterns/two-data-authorities.md) pattern and supporting machinery (V-cycle, regional-review, lattice) apply to legacy software reverse-engineering. Core framing: the system produces formal specifications, not new implementations.*

## Core claim

The system produces **specifications**, not implementations. What it outputs is rigorous formal articulations of what a legacy software system does and was intended to do. Verification happens via theorem proving (Dafny) and code execution.

The software already exists — the designer wrote documentation, the implementer wrote code. What the system adds: a formal specification tying the two together, machine-checkable and convertible to verified executable code.

## Convergence framework

### Verifier-relative convergence

Convergence is always relative to a downstream verifier. For software reverse-engineering:

| Scale | Operator | Verifier |
|---|---|---|
| Local | local-review | proof soundness per property |
| Regional | regional-review | cluster proof consistency |
| Full | full-review | lattice proof consistency |

At each scale, the operator iterates until the verifier finds no new issues.

### Cone as proof cluster

A cone is an apex property plus its dependencies. In the software case, the apex is a theorem or operation and the dependencies are the axioms, definitions, and lemmas it cites. Regional convergence of a cone means:

- Apex's proof is consistent with its dependencies
- No declared-cycle issues
- All citations correctly licensed
- Formal contracts (preconditions, postconditions, frames) are complete

Full ASN convergence: all cones regionally converged, lattice-wide citation and convention consistency confirmed.

## Verification: Dafny and code execution

Unlike the science deployment (which uses an agentic Judger to check against target principles), the software deployment's verifier is mechanical:

- **Dafny:** checks each property's formal contract against its proof obligations. Binary per property: verified or fails.
- **Code execution:** generated Rust (or equivalent) code runs and behaves as the specification claims.

Dafny verification is the "match convergence" analog — the specification holds against its claimed properties. Failed verification indicates either the specification is wrong or the proof is flawed; both require revising the lattice until Dafny is satisfied.

## What the system produces

- **Pre-verification:** candidate specifications articulated at increasing precision through the pipeline
- **Post-verification:** Dafny-verified formal contracts plus executable code that instantiates them
- **Documentation:** a formal record of how designer intent maps to implementation behavior, with bidirectional citation

## What's being articulated

- What operations the system provides (named, signature-typed)
- What guarantees each operation makes (preconditions, postconditions, frames)
- What invariants hold across operations
- What named concepts bridge the design-prose layer and the implementation-code layer (the invented reasoning vocabulary)

## What's NOT being produced

- Not new software — Gregory's implementation already exists
- Not new design documents — Nelson wrote the intent
- Not novel algorithms — the system is formalizing existing ones
- Not discovering hypotheses about nature — the target is an artifact, not a natural phenomenon

The system's value is rigorous formalization of what was built, not invention of new constructs.

## Xanadu demonstration specifics

- **Theory channel:** Ted Nelson's *Literary Machines* and associated concept catalog. Noun-heavy descriptive prose.
- **Data channel:** Roger Gregory's udanax-green C implementation. Verb-in-packaging function names requiring un-wrapping.
- **Foundation output:** ASN-0034 (Tumbler Algebra) — ~80 formalized properties covering sequence arithmetic, total order, prefix, addition, subtraction, displacement, allocation discipline, span algebra.
- **Downstream:** ASN-0036 (Strand Model) and additional ASNs build on the foundation.
- **Verification machinery:** Dafny proofs for formal contracts, Rust codegen (in progress) for executable output.

See [Legacy Software Discovery](../patterns/two-data-authorities-legacy-software.md) for the pattern-doc treatment with empirical findings from this deployment (80-test saturation, 70/30 coinage split, noun/verb source-shape asymmetry).

## What transfers to other domains

The machinery (two-channel discovery, blueprinting, formalization, V-cycle, cone structure, scope promotion, lattice) is domain-general. What changes across domains is the verifier at each scale. The [science deployment approach](../science/README.md) describes the parallel framing for scientific discovery, where the verifier becomes experimental reproducibility rather than Dafny proof.

## Related

- [Two Data Authorities](../patterns/two-data-authorities.md) — parent pattern
- [Legacy Software Discovery](../patterns/two-data-authorities-legacy-software.md) — grounded pattern with empirical findings
- [Channel Asymmetry](../patterns/channel-asymmetry.md) — why shape-mismatch between channels forces coinage
- [Review V-Cycle](../design-notes/review-v-cycle.md) — multi-scale review architecture
- [Science Approach](../science/README.md) — parallel framing for scientific deployments
