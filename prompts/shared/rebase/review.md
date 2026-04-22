# Dependency Cross-Reference Review

You are checking whether a claim's references to upstream ASN
claims are correct.

## Claim being checked

**Label**: {{claim_label}}

{{claim_section}}

## Upstream claim (from ASN-{{upstream_asn}})

**Label**: {{upstream_label}}

{{upstream_contract}}

## Check

Compare this claim's reference to the upstream claim:

- Does the local citation use the upstream's canonical name?
- Is the local claim a redefinition of the upstream claim?
  (Same invariant/postcondition re-derived locally instead of cited.)
- Does the dependency declaration in the claim table match the
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
