# Methodology

This project applies incremental formal specification to a system where the design authority (Ted Nelson) and implementation evidence (Roger Gregory's udanax-green) exist but no formal specification does. The methodology follows established industry practice in formal methods: incremental refinement (Abrial), Design by Contract (Meyer), and lightweight formal methods (Jackson). It is adapted for a setting where the specification must be elicited from domain authorities rather than written from requirements.

The central idea: start from informal understanding, refine incrementally toward machine-checked proofs, and let each stage of formalization expose errors in the previous stage. This follows the standard progression from informal to formal. What is specific to this project is the discovery-first approach (the specification is elicited from domain authorities) and the tight feedback loop between text-based formalization and mechanical verification.

```
Discovery → Blueprinting → Formalization ⇄ Modeling
  (elicit)    (decompose)     (specify)      (verify)
```

The unit of work is the ASN. Each ASN progresses through these stages independently. At any point in the project, some ASNs may be in discovery, others in blueprinting, others cycling between formalization and modeling. The dependency lattice determines the order: foundation ASNs must be verified before the ASNs that build on them.

Each stage refines the same content at increasing precision. Discovery captures reasoning in natural language. Blueprinting decomposes it into verifiable units. Formalization assigns precise contracts. Modeling checks those contracts mechanically. When modeling finds errors, they flow back to formalization, tightening the specification until both agree.

## [Discovery](discovery.md)

Elicit the system's structure through consultation with domain authorities. Discovery connects — it grows the lattice outward from a broad question to focused foundations. Properties emerge from understanding design intent and implementation evidence. The key principles:

- **Two independent channels** — design intent (Nelson) and implementation evidence (Gregory), kept separate by a vocabulary firewall
- **Abstract Specification Notes (ASNs)** — each ASN is a reasoning document: Dijkstra-style derivation prose with embedded properties, covering one topic. ASNs form a dependency lattice — each declares what it depends on and what it covers, building on verified foundations
- **Convergence through review** — structured consultation, review, and revision cycles until the reasoning is internally consistent
- **Properties emerge, not prescribed** — the structure of the system reveals itself through careful questioning

The core artifact is the ASN. Properties are stated in natural language with enough precision to be unambiguous, but the emphasis is on the reasoning that justifies them.

Discovery produces informal but rigorous reasoning. The problem: an ASN may contain dozens of properties embedded in pages of prose. It cannot be formalized as a whole. The next stage addresses this.

## [Blueprinting](blueprinting.md)

Construct an intermediate representation of the reasoning document that identifies its properties and their relationships. The blueprint makes formal specification possible by answering structural questions before formalization begins. The key principles:

- **Decompose into atomic units** — a reasoning document contains dozens of interleaved properties. Each must be isolated with its own statement, justification, and proof before it can be verified independently.
- **Classify each property** — axiom, definition, design requirement, lemma, theorem, corollary. The classification determines how formalization treats it — axioms are accepted, definitions are named, theorems are proven.
- **Map dependencies** — which properties follow from which. Explicit dependencies let formalization process properties in the right order and propagate changes when a proof is revised.
- **Establish vocabulary** — decomposition isolates properties, but each property may reference notation defined elsewhere. The shared vocabulary preserves this context so properties can be understood and verified independently.

With properties decomposed, classified, and their dependencies mapped, formalization can operate on each one independently. The next stage does exactly this.

## [Formalization](formalization.md)

Produce formal contracts for each property and verify them through independent review cycles. Blueprinting identified the properties and their structure. Formalization makes each one precise enough for mechanical verification. The key principles:

- **Per-property scope** — each property is formalized with only its dependencies for context. This constraint drives convergence: the property must conform to its dependencies as given, not adjust them to make the proof easier.
- **Cross-cutting scope** — whole-ASN analysis catches what per-property review cannot: conflation of distinct concepts, precondition chain gaps, circular reasoning across properties.
- **Convergence** — review cycles repeat until changes trend to zero. A cache flush followed by a clean re-run that converges quickly confirms stability.
- **Incremental** — only re-examine what changed. When a property is revised, its downstream dependents are re-checked. Unchanged properties carry forward.

Formalization rewrites proofs to Dijkstra standard, assigns formal contracts (preconditions, postconditions, invariants, frame conditions), and verifies that each contract is faithful to the derivation. Per-property formalization converges like solving a system of equations one variable at a time with the others fixed. Cross-review is the escape valve for issues that per-property isolation cannot catch. See the [formalization design note](formalization.md) for why this works.

Converged contracts are ready for the final test: can a machine verify them? This is where modeling closes the loop.

## Modeling

Verify formalized properties mechanically. The key principles:

- **Two independent verification methods** — bounded model checking (Alloy) and full formal proofs (Dafny), each catching different classes of errors
- **Counterexamples are ground truth** — a counterexample from Alloy is a concrete bug in the spec, not a matter of interpretation
- **Dependency-ordered proofs** — Dafny builds in topological order, each property importing verified results from its dependencies
- **Feedback into formalization** — counterexamples and proof failures feed back as findings, driving the formalization-modeling loop until both converge

Modeling provides what text-based review cannot: mechanical certainty.

## Closing the Loop

The formalization-modeling boundary is where the specification earns trust. A counterexample from Alloy or a proof failure from Dafny is a finding about the specification itself. These findings flow back into formalization: the affected property's contract is revised, the formalization review cycle re-converges on the changed properties, and modeling runs again.

This loop repeats until all models are consistent and all proofs pass. The specification is done when formalization and modeling agree: every property has a formal contract that text-based review accepts and mechanical verification confirms.

## What Verification Proves and What It Cannot

Each stage provides a specific guarantee. Understanding what each stage *cannot* tell you is as important as understanding what it can.

**Contracts** are the claims — preconditions, postconditions, invariants, definitions stated in the ASN. They say what the system guarantees.

**Proofs** are the reasoning — Dijkstra-style derivation prose that justifies those claims. The proofs can have gaps, wrong steps, or missing cases, and the claims can still be true. A correct contract with a flawed proof is better than no contract at all.

**Formalization review** checks that the contracts are precise, internally consistent, and faithful to the derivation prose. It catches conflation, missing preconditions, and structural gaps between properties. But it operates on text — it can be wrong, and it can miss things that look plausible in natural language.

**Dafny verification** proves that the contracts are logically consistent and faithfully encoded — every contract field is translated correctly and every proof obligation is discharged. This is mechanical certainty. But Dafny cannot tell you:

- Whether a postcondition describes what the system *should* do — that is a design question, answered by the consultations with Nelson and Gregory
- Whether the axioms are the right axioms — those are posited from evidence, not derived
- Whether the system described by these contracts matches the actual implementation — that requires testing against the real system

**Golden tests** close the final gap. The contracts compile through Dafny to Go. Running that Go against the real system (udanax-green) checks whether the formalized specification matches reality. A golden test failure means the spec is internally consistent but doesn't describe the actual system.

The chain of trust runs from human judgment through mechanical verification to empirical testing. Each link strengthens a different part: consultations establish intent, formalization makes it precise, verification makes it consistent, testing makes it real. No single stage is sufficient — the specification earns trust from the combination.
