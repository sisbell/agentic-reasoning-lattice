You are scanning a claim for the non-logical symbols it introduces — its formal-logic *signature*. Extract any constants, function symbols, relation symbols, or named constructions this claim DEFINES (not just uses).

Output ONLY valid YAML. No commentary, no code fences, no explanation.

## Definition vs usage

A definition introduces a symbol or term for the first time:
- "Let ⊕ denote tumbler addition"
- "Define the action point as..."
- "We write sig(t) for..."
- "zeros(t) = #{i : ...}"
- A formula that names a new construction or function

A usage just references an already-defined symbol:
- "By TA0, a ⊕ w is well-defined"
- "the action point k satisfies..."
- "since zeros(v) = 0"

Only report DEFINITIONS, not usages. Logical and set-theoretic notation (∈, ⊆, ∀, ⟹, =, etc.) is the formal language's notation — not part of any claim's signature.

## YAML structure

```yaml
signature:
  - symbol: "<notation>"
    meaning: "<brief definition>"
```

If this claim defines no new notation:

```yaml
signature: []
```

## Claim

Label: {{label}}
Name: {{name}}

### Body

{{body}}
