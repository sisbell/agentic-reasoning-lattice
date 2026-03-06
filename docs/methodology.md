# Methodology — Design Principles

The pipeline's design is grounded in formal methods principles — discovered empirically through building the system, then identified as established ideas from Abrial's Event-B, Baier & Katoen's model checking, and the Dijkstra/Hoare constructive tradition. These principles apply to any system where AI agents construct formal or semi-formal artifacts about complex systems.

The core insight: **the principles behind formal methods are not about math notation or proof tools. They're about how to structure reasoning about complex systems.** When AI agents do that reasoning instead of humans, the same structural principles apply — because the complexity challenges are the same.

## Five Principles

### 1. Independence of Evidence Channels

When constructing a model, the specification source and the validation source must be structurally independent, or errors in understanding propagate to both and become invisible.

**In this project:** Nelson (design intent) and Gregory (implementation evidence) cannot see each other's vocabulary. Mixed answers were empirically worse before the separation was enforced. See [Expert Consultation](expert-consultation.md).

**In formal methods:** model checking requires independent property and model inputs (Baier & Katoen). IV&V demands independent specification and testing teams. The principle is universal.

### 2. Properties as the Atomic Unit

The smallest useful unit of formal reasoning is a claim that can be true or false — a property. Features are bundles of properties. Use cases are narratives with implicit properties. You can compose properties, decompose them, prove them, refute them. You can't do any of that with a narrative.

**In this project:** each Nelson question targets one guarantee. Each guarantee maps to one ASN property label (DEL1, DEL2...). Each ASN property maps to one Dafny lemma or postcondition. The pipeline operates on properties as its unit of work.

**Two fundamental types** (Abrial §1.8.3):
- **Invariants** (safety): conditions that must hold permanently
- **Reachability** (liveness): events that must eventually occur

### 3. Vocabulary as Abstraction Enforcement

Abstraction levels must be enforced at the language level, not by discipline. If a specification channel can use implementation terms, it will, and the resulting properties will couple to one realization instead of generalizing.

**In this project:** `nelson-questions.md` bans implementation terms (I-addresses, V-space, spanfilade). This is structural — if Nelson can say "spanfilade," the answers couple to udanax-green's data structures and the properties won't hold for any other conforming implementation.

**The same insight** behind type systems, API boundaries, and information hiding — applied to the specification process itself.

### 4. The Model Is a New Artifact, Not a Description

Modeling is construction, not transcription. The model exists to reason with, not to document. A model from which properties are derived is fundamentally different from a description of existing behavior.

**In this project:** the ASNs don't describe udanax-green. They construct a model (the POOM, operations on it, invariants) from which properties are derived. The discovery agent synthesizes both channels into properties that neither source stated directly.

**The test:** can you discover something from the artifact that wasn't explicitly put in? From documentation, never. From a model, always — that's what makes it a model. The DEL1 contradiction found in ASN-0005 review 2 (clauses 2 and 3 jointly inconsistent) was a consequence of the model's structure, not something anyone wrote in.

**Abrial** (§1.7): "Formal methods are techniques used to build blueprints adapted to our discipline. Such blueprints are called formal models."

### 5. Iteration Is Structural, Not a Sign of Failure

The discovery of what matters is part of the work, not a precondition for it. What you need to prove is not known at the beginning — it emerges through the modeling process.

**In this project:** the pipeline is iterative (inquiry → consultation → discovery → review → revise). The review cycle exists because the first pass never gets the properties right. This is not a deficiency.

**Abrial** (Prologue): "what we have to prove is not known right from the beginning... What we have to prove evolves with our understanding of the problem and our (non-linear) progress in the construction process."

## Formal Methods Grounding

### Abrial's Event-B

The pipeline maps directly to Abrial's modeling framework:

| Abrial | Pipeline |
|--------|----------|
| Blueprint (formal model) | ASN |
| Requirements document | Inquiry + consultation answers |
| Labeled fragments (FUN, SAF, DEL...) | ASN properties (DEL1, INS1, S0...) |
| Explanatory text | ASN prose surrounding properties |
| Invariant properties | Safety guarantees (permanence, identity) |
| Reachability properties | Liveness guarantees (reversibility) |
| Refinement steps | Successive ASNs at finer detail |
| Proof obligations | Review cycle; Dafny verification |
| Animation | Executable Dafny specs + golden tests |
| Legacy code | udanax-green |
| The modeler | Discovery agent |

Key Abrial principles realized in the pipeline:
- **Legacy code is not the requirements document** (Prologue) — udanax-green is evidence, not specification
- **Proofs debug the model** (Prologue) — verification failures reveal ASN flaws
- **Correctness is relative to the model** (Prologue) — the ASN is an approximation, not Platonic truth
- **Refinement as increasing precision** (§1.8.5) — successive ASNs reveal finer structure

### Baier & Katoen Model Checking

The model checking framework requires two structurally independent inputs:

```
Property specification  →  ┌──────────┐
  (what must hold)          │ Verifier │ → yes/no + counterexample
System model            →  └──────────┘
  (what the system does)
```

- Nelson → raw material for property specification
- Gregory → raw material for the system model

At the ASN stage, this structure guides the consultation architecture. At the Dafny stage, it is fully realized: Nelson-sourced properties become `ensures`/`invariant` clauses, Gregory-sourced evidence becomes test methods, and Z3 is the verifier.

## Three Concerns, Three Mechanisms

A valid modeling process must address three distinct concerns:

### 1. Consistency — are the properties internally coherent?

**ASN phase:** review → revise cycle. AI agents reason within the model and find contradictions.

**Dafny phase:** Z3 verification. Mechanical, exhaustive.

### 2. Intent — do the properties capture the right thing?

**ASN phase:** temporary gap — no mechanism catches properties that are internally consistent but capture the wrong intent. Accepted because revision cost is low.

**Dafny phase:** golden tests — executable spec run against known-good input/output pairs from the actual system. If the spec passes Z3 but fails a golden test, the property captures the wrong intent.

### 3. Scope — what's not modeled yet?

**Both phases:** OUT_OF_SCOPE items and open questions. The human reads these and decides what to investigate next. This is the strategic question that only the human can answer.

```
Consistency:  Z3 verification (mechanical, exhaustive)
Intent:       Golden tests (executable spec vs. known-good behavior)
Scope:        OUT_OF_SCOPE items / open questions (human judgment)
```

## What Changes When AI Does the Reasoning

### Independence becomes easier to enforce

With human teams, it's hard to prevent a domain expert from thinking about implementation. With LLM agents, you control what goes into the prompt. The vocabulary firewall achieves something formal methods always wanted but struggled to enforce with human teams.

### Iteration becomes cheaper

Abrial's review cycles took months of human effort. AI-assisted review → revise cycles take minutes. This changes the economics of formal methods fundamentally — the historical cost objection disappears. What remains are the structural principles, and those were always the valuable part.

### The formal model is for the machines

The human doesn't read the ASN properties in detail or follow the formal derivations. The human reads OUT_OF_SCOPE items (scope questions) and investigates specific failures (golden test disagreements). Internal model consistency — the REVISE cycle — is fully delegated. The human trusts it the way they trust a compiler.

The formal model needs to be rigorous not because a human will read it, but because AI agents will reason with it. Sloppy models produce sloppy derivations.

### The structural requirements do not change

Independence, property-orientation, abstraction enforcement, constructive modeling — these are complexity management principles that apply regardless of who or what is doing the reasoning. An AI agent that mixes specification and implementation in one prompt has the same contamination problem a human team has when the spec writer and the developer are the same person.

## The System Perspective

The pipeline centers the **system**, not the **user**:

- States, transitions, guards, invariants
- No users, no use cases, no scenarios, no actors
- Humans are modeled as part of the environment — just another source of transitions

This is the shared foundation of the constructive formal tradition (Dijkstra, Hoare, Lamport, Abrial). A system perspective produces **properties** — formal claims that can be composed, decomposed, proved, and refuted. A user perspective produces **narratives** — sequences of actions and expected outcomes that cannot.

The pipeline doesn't ignore the designer perspective — the inquiry and Nelson channels translate it into system properties through a structured process. The inquiry is where intent lives. By the time the discovery agent builds the model, the perspective is purely system-centric.

## References

- Abrial, J.-R. *Modeling in Event-B: System and Software Engineering*. Cambridge University Press, 2010.
- Baier, C. and Katoen, J.-P. *Principles of Model Checking*. MIT Press, 2008.
- Back, R.-J. and von Wright, J. *Refinement Calculus: A Systematic Introduction*. Springer, 1998.
