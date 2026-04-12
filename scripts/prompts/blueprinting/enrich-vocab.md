You are scanning a property for shared notation definitions. Extract any symbols, operations, or terminology that this property DEFINES (not just uses).

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

Only report DEFINITIONS, not usages. Common mathematical notation (∈, ⊆, ∀, ⟹, etc.) is not vocabulary.

## YAML structure

```yaml
vocabulary:
  - symbol: "<notation>"
    meaning: "<brief definition>"
```

If this property defines no new notation:

```yaml
vocabulary: []
```

## Property

Label: {{label}}
Name: {{name}}

### Body

{{body}}
