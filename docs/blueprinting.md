# Blueprinting

> "The people in charge of the development of large and complex systems should adopt a point of view shared by all mature engineering disciplines, namely that of using an artifact to reason about their future system during its construction." — Jean-Raymond Abrial, *Modeling in Event-B*

## The case for an intermediate representation

A reasoning document from discovery contains the right properties, but they're embedded in narrative prose — definitions interleaved with proofs, motivating examples alongside formal statements, architectural commentary woven through derivations. That narrative is how humans reason. But you cannot formalize narrative. You can only formalize the formal claims within it.

At some point, the narrative and the formal content must be separated. The formal claims need to stand on their own — each with a clear statement, explicit dependencies, and a classification that tells the verification pipeline what to do with it. The narrative stays as context for human reviewers. This separation is what blueprinting produces.

## What blueprinting produces

A monolithic reasoning document becomes a set of per-property file pairs. Each property gets two files: a YAML file carrying metadata (label, name, type, dependencies, vocabulary) and a markdown file carrying the body (statement, justification, proof).

The metadata makes the formal structure explicit: what this property is, what it depends on, what notation it introduces. The body preserves the interleaved narrative and formal content because formalization's reviewers need the narrative to understand the proof. Full separation comes later, at modeling, when only the formal contracts enter mechanical verification.

The metadata at blueprinting time is deliberately incomplete. Type classifications are best-effort, dependencies are extracted from prose but may be imprecise, vocabulary attribution has minor errors. Formalization tightens all of it. Blueprinting just needs to get the structure right enough that formalization can operate per-property.

This is the meet operation at the document scale — a single node in the document lattice becomes many nodes in the property lattice, each with explicit dependencies. Blueprinting is where the two granularities of the lattice diverge.

## Decomposition as progressive refinement

Blueprinting works in layers, each adding detail the previous layer could not see.

First, a mechanical split on section headers. No judgment — just string splitting. This produces sections of manageable size, each isolable.

Then, per-section analysis identifies the properties within each section. Each section is read with full context to make structural decisions: this bold header is a case split inside a proof, not a new property. These two definitions share a preamble but are logically independent. This "axiom" has a proof — it's really a design requirement whose consequences are derived.

Then, per-property classification and dependency extraction. Each property is analyzed independently: what type is it, what does its proof cite, what notation does it introduce.

Each layer refines what the previous produced. The section split doesn't know about properties. The property identification doesn't know about types. The classification doesn't know about vocabulary. Progressive refinement, not a single pass.

## The reasoning document as artifact

Discovery produces reasoning documents — Dijkstra-style prose with embedded properties. Blueprinting transforms them into structured per-property files. Formalization refines those files into precise contracts. Modeling translates the contracts into mechanically verifiable code.

At each stage, the same system properties are represented with increasing precision. The content doesn't change. The representation does. A property that discovery expressed as "content once stored is never modified" becomes a classified design-requirement with label S0, explicit dependencies, and eventually a formal contract with preconditions and postconditions that a theorem prover can verify.

The reasoning document is frozen once it enters blueprinting. It served its purpose. The reasoning is done, the properties are found. From this point forward, the per-property files are the working copy. This is deliberate: the reasoning document is the record of discovery. Modifying it during formalization would mix two concerns: finding properties and verifying them.

## Why structural issues are expected

Discovery agents reason to understand, not to verify. They name properties inconsistently, embed definitions inside proofs, derive intermediate results that other properties need but never formally declare. A property might be labeled "axiom" in one sentence and proven from other properties in the next paragraph. Two definitions might share a section because the author was thinking about them together, even though they're logically independent.

These are not bugs. They're the natural result of writing to understand rather than writing to verify. Blueprinting exists because the discovery process is messy and the formalization process needs clean inputs.