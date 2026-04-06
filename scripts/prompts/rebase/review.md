# Dependency Cross-Reference Review

You are checking whether a property's references to upstream ASN
properties are correct.

## Property being checked

**Label**: {{property_label}}

{{property_section}}

## Upstream property (from ASN-{{upstream_asn}})

**Label**: {{upstream_label}}

{{upstream_contract}}

## Check

Compare this property's reference to the upstream property:

- Does the local citation use the upstream's canonical name?
- Is the local property a redefinition of the upstream property?
  (Same invariant/postcondition re-derived locally instead of cited.)
- Does the dependency declaration in the property table match the
  actual usage in the proof?
- Are sub-label references (e.g., TA5(a), TA5(b)) used where the
  upstream exports only the parent label (e.g., TA5)?

## Output

Respond with exactly one line:

```
CLEAN | reason
```

or

```
FLAG | **Problem**: description. **Required**: specific fix instruction.
```

FLAG means the reference is incorrect and must be fixed. The
**Required** section must give a concrete, actionable instruction
that a reviser can execute without additional context.
