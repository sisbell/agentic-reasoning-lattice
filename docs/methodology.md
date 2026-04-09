# Methodology

This project applies incremental formal specification to a system where the design authority (Ted Nelson) and implementation evidence (Roger Gregory's udanax-green) exist but no formal specification does. The methodology follows established industry practice in formal methods: incremental refinement (Abrial), Design by Contract (Meyer), and lightweight formal methods (Jackson). It is adapted for a setting where the specification must be elicited from domain authorities rather than written from requirements.

The central idea: start from informal understanding, refine incrementally toward machine-checked proofs, and let each stage of formalization expose errors in the previous stage. This is not novel — it is the standard progression from informal to formal. What is specific to this project is the discovery-first approach (the specification is elicited, not prescribed) and the tight feedback loop between text-based formalization and mechanical verification.

```
Discovery → Blueprinting → Formalization ⇄ Modeling
  (elicit)    (decompose)     (specify)      (verify)
```

The unit of work is the ASN. Each ASN progresses through these stages independently — at any point in the project, some ASNs may be in discovery, others in blueprinting, others cycling between formalization and modeling. The dependency lattice determines the order: foundation ASNs must be verified before the ASNs that build on them.

Each stage refines the same content at increasing precision. Discovery captures reasoning in natural language. Blueprinting decomposes it into verifiable units. Formalization assigns precise contracts. Modeling checks those contracts mechanically — and when modeling finds errors, they flow back to formalization, tightening the specification until both agree.

## [Discovery](discovery.md)

Elicit the system's structure through consultation with domain authorities. Properties are discovered, not invented — they emerge from understanding design intent and implementation evidence. The key principles:

- **Two independent channels** — design intent (Nelson) and implementation evidence (Gregory), kept separate by a vocabulary firewall
- **Abstract Specification Notes (ASNs)** — each ASN is a reasoning document: Dijkstra-style derivation prose with embedded properties, covering one topic. ASNs form a dependency lattice — each declares what it depends on and what it covers, building on verified foundations
- **Convergence through review** — structured consultation, review, and revision cycles until the reasoning is internally consistent
- **Properties emerge, not prescribed** — the structure of the system reveals itself through careful questioning

The core artifact is the ASN. Properties are stated in natural language with enough precision to be unambiguous, but the emphasis is on the reasoning that justifies them.

Discovery produces informal but rigorous reasoning. The problem: an ASN may contain dozens of properties embedded in pages of prose. It cannot be formalized as a whole — the next stage addresses this.

## [Blueprinting](blueprinting.md)

Prepare a reasoning document for formalization. The key principles:

- **Decompose** into atomic units — each property stands alone with its derivation and dependencies
- **Classify** each property — axiom, definition, lemma, corollary, design requirement
- **Map dependencies** — which properties follow from which
- **Establish vocabulary** — shared notation definitions across all properties
- **Contract** each property — preconditions, postconditions, invariants, or definition following Design by Contract

A large informal document cannot be formalized reliably in one pass. Blueprinting breaks it into units small enough to reason about precisely, then assigns each unit a formal contract that downstream verification can check.

With properties decomposed and contracted, formalization can operate on each one independently — the next stage does exactly this.

## Formalization

Verify and tighten the formal contracts from blueprinting through independent review cycles. The key principles:

- **Per-property scope** — each property is reviewed with only its dependencies for context, making review tractable and parallelizable
- **Cross-cutting scope** — whole-ASN analysis catches what per-property reviews miss: conflation of distinct concepts, missing cases, circular reasoning
- **Convergence** — review cycles repeat until all reviewers agree the contracts are consistent, complete, and faithful to the derivation prose
- **Incremental** — only re-examine what changed; unchanged properties carry forward

Formalization does not change the properties — it tightens their formal expression until the contracts are precise enough for mechanical verification.

Converged contracts are ready for the final test: can a machine verify them? This is where modeling closes the loop.

## Modeling

Verify formalized properties mechanically. The key principles:

- **Two independent verification methods** — bounded model checking (Alloy) and full formal proofs (Dafny), each catching different classes of errors
- **Counterexamples are ground truth** — a counterexample from Alloy is a concrete bug in the spec, not a matter of interpretation
- **Dependency-ordered proofs** — Dafny builds in topological order, each property importing verified results from its dependencies
- **Feedback into formalization** — counterexamples and proof failures feed back as findings, driving the formalization-modeling loop until both converge

Modeling provides what text-based review cannot: mechanical certainty.

## Closing the Loop

The formalization-modeling boundary is where the specification earns trust. A counterexample from Alloy or a proof failure from Dafny is not a tool problem — it is a finding about the specification itself. These findings flow back into formalization: the affected property's contract is revised, the formalization review cycle re-converges on the changed properties, and modeling runs again.

This loop repeats until all models are consistent and all proofs pass. The specification is done when formalization and modeling agree — when every property has a formal contract that text-based review accepts and mechanical verification confirms.

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
