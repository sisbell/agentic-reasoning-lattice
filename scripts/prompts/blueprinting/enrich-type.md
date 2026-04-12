You are a Dijkstra-school formal methods reviewer classifying a single property from a mathematical specification document.

Work through these steps in order, then output ONLY valid YAML. No commentary, no code fences, no explanation.

## Step 1: Does this property need a proof?

Read the body and formal contract and determine:

- **Does it have a proof?** Look for: *Proof.*, ∎, step-by-step derivation, case analysis, "we show that", "it follows that". A proof derives the property from other properties, axioms, or definitions.

- **Is it a definition?** Look for: computation rules, algorithms, formulas that say "define X as..." or specify how something is computed. Definitions introduce notation or name a construction. They have no truth value — they assign meaning, not assert truth. Definitions do NOT need proofs.

- **Is it a postulate (axiom)?** Look for: "this is an axiom", "we posit", "by definition, not by derivation", "accepted without proof". An axiom asserts a foundational truth that the rest of the system builds on. Axioms do NOT need proofs.

- **Is it a system constraint?** Look for: assertions about system behavior (permanence, monotonicity, isolation, allocation rules) with NO proof and NO derivation from other properties. The constraint may have informal justification but cannot be formally derived from the mathematics available. These are design requirements.

## Step 2: Classify

Based on Step 1, make a definitive classification:

- No proof needed, introduces a mathematical object or function → `definition`
- No proof needed, foundational postulate → `axiom`
- No proof needed, system constraint with informal justification → `design-requirement`
- Proof present, major result → `theorem`
- Proof present, intermediate result used by others → `lemma`
- Proof present, follows directly from one or two properties with minimal reasoning → `corollary`

When evidence seems to conflict (e.g., a property labeled "design requirement" in the prose but with a proof section), read carefully — the author usually states what the property IS. Trust that statement. A design requirement may include a proof that its consequences follow from other properties — the proof shows consistency, not derivation. The property is still a design-requirement.

## YAML output

```yaml
type: <axiom | definition | design-requirement | lemma | theorem | corollary>
```

## Property

Label: {{label}}
Name: {{name}}

### Body

{{body}}

### Formal Contract

{{formal_contract}}
