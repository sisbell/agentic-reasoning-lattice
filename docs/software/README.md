# Software Reverse-Engineering: Approach

*Design note. Grounded — demonstrated on the Xanadu hypertext system. How the [Two Data Authorities](../patterns/two-data-authorities.md) pattern and supporting machinery (claim convergence protocol, lattice) apply to legacy software reverse-engineering. Core framing: the system produces formal specifications, not new implementations.*

## Core claim

The system produces **specifications**, not implementations. What it outputs is rigorous formal articulations of what a legacy software system does and was intended to do. Verification happens via theorem proving (Dafny) and code execution.

The software already exists — the designer wrote documentation, the implementer wrote code. What the system adds: a formal specification tying the two together, machine-checkable and convertible to verified executable code.

## Convergence framework

### Verifier-relative convergence

Convergence is always relative to a downstream verifier. For software reverse-engineering, the [claim convergence protocol](../protocols/claim-convergence-protocol.md) drives claims toward precision at whatever scope the choreography selects:

| Scope | Verifier concern |
|---|---|
| Cone (adaptive) | proof soundness per claim, cluster consistency |
| Comprehensive | lattice-wide proof consistency |

At each scope, the protocol iterates until the convergence predicate holds — every `comment.revise` has a `resolution`.

### Cone as proof cluster

A cone is an apex claim plus its dependencies. In the software case, the apex is a theorem or operation and the dependencies are the axioms, definitions, and lemmas it cites. Convergence of a cone means:

- Apex's proof is consistent with its dependencies
- No declared-cycle issues
- All citations correctly licensed
- Formal contracts (preconditions, postconditions, frames) are complete

Full note convergence: all cones converged, lattice-wide citation and convention consistency confirmed.

## Verification: Dafny and code execution

Unlike the science domain (which uses an agentic Judger to check against target principles), the software domain's verifier is mechanical:

- **Dafny:** checks each claim's formal contract against its proof obligations. Binary per claim: verified or fails.
- **Code execution:** generated Rust (or equivalent) code runs and behaves as the specification claims.

Dafny verification is the "match convergence" analog — the specification holds against its claimed claims. Failed verification indicates either the specification is wrong or the proof is flawed; both require revising the lattice until Dafny is satisfied.

## What the system produces

- **Pre-verification:** candidate specifications articulated at increasing precision through the protocol architecture
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
- **Evidence channel:** Roger Gregory's udanax-green C implementation. Verb-in-packaging function names requiring un-wrapping.
- **Foundation output:** ASN-0034 (Tumbler Algebra) — ~80 converged claims covering sequence arithmetic, total order, prefix, addition, subtraction, displacement, allocation discipline, span algebra.
- **Downstream:** ASN-0036 (Strand Model) and additional notes build on the foundation.
- **Verification machinery:** Dafny proofs for formal contracts, Rust codegen (in progress) for executable output.

See [Legacy Software Discovery](../patterns/two-data-authorities-legacy-software.md) for the pattern-doc treatment with empirical findings from this domain (80-test saturation, 70/30 coinage split, noun/verb source-shape asymmetry).

## What transfers to other domains

The machinery (two-channel discovery via the [consultation protocol](../protocols/consultation-protocol.md), [note convergence](../protocols/note-convergence-protocol.md), [claim derivation](../protocols/claim-derivation-module.md), [claim convergence](../protocols/claim-convergence-protocol.md), cone structure, scope promotion, lattice) is domain-general. What changes across domains is the verifier at each scope. The [science domain approach](../science/README.md) describes the parallel framing for scientific discovery, where the verifier becomes experimental reproducibility rather than Dafny proof.

## Related

- [Two Data Authorities](../patterns/two-data-authorities.md) — parent pattern
- [Legacy Software Discovery](../patterns/two-data-authorities-legacy-software.md) — grounded pattern with empirical findings
- [Channel Asymmetry](../patterns/channel-asymmetry.md) — why shape-mismatch between channels forces coinage
- [Consultation Protocol](../protocols/consultation-protocol.md) — the two-channel consultation with vocabulary firewall and synthesis integrity
- [Note Convergence Protocol](../protocols/note-convergence-protocol.md) — drives notes to stability during discovery
- [Claim Convergence Protocol](../protocols/claim-convergence-protocol.md) — drives claims to formal precision; cone-scoped and comprehensive review as choreography
- [Science Approach](../science/README.md) — parallel framing for scientific domains