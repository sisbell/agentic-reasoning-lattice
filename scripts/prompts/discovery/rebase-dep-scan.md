You are extracting the dependency list for a single property in a formal specification.

## Property
**Label**: {{label}}
**ASN**: {{asn_label}}
**Declared depends**: {{depends}}

## Property text (derivation section from ASN)
{{property_text}}

## Foundation labels available
{{available_labels}}

## Task

Read the property's derivation text above. Identify every foundation label (from the available labels list) that this property **logically depends on** — meaning the property's formal statement or its proof/derivation would be invalid without that foundation property.

Do NOT include labels that are merely mentioned for context, comparison, or historical reference. Only include labels that are load-bearing for this property's correctness.

Output ONLY a YAML list, nothing else:

```yaml
depends_on:
  - label: T7
    asn: 34
    reason: "used in disjointness derivation: dom(Σ.L) ∩ dom(Σ.C) = ∅"
  - label: S7b
    asn: 36
    reason: "paralleled for link addresses: zeros(a) = 3"
```

If the property has no foundation dependencies (purely introduced), output:

```yaml
depends_on: []
```
