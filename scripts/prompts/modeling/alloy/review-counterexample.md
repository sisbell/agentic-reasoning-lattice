# Alloy Review — Counterexample Analysis

Classify this counterexample as a genuine spec issue or a modeling artifact.

## Background

Alloy is a bounded model checker. A counterexample on a `check` means the assertion was violated within finite scope. This can be:

1. **Genuine spec issue**: The property is too strong, missing a precondition, contradictory, or ambiguous
2. **Modeling artifact**: The Alloy translation doesn't faithfully capture the property's intent — bounded scope, integer overflow, atom identity vs structural equality, seq length limits

Common modeling artifacts:
- Bounded scope cannot supply enough witnesses (e.g., unboundedness properties)
- Integer overflow: `plus[x,1]` wraps at Int ceiling
- Atom identity: two atoms with identical components are still different atoms
- Sequence length bounded by `seq` scope keyword
- Properties that assert existence of arbitrarily large structures

## Property

{{property_text}}

## Alloy Model

{{alloy_source}}

## Checker Output

{{checker_output}}

## Instructions

Respond with exactly one of these formats:

For a modeling artifact:
```
ARTIFACT | <brief explanation of the Alloy limitation>
```

For a genuine spec issue:
```
SPEC_ISSUE | <what the counterexample reveals about the property>

What needs to change: <specific fix — missing precondition, over-strong claim, etc.>
```

Compare the model's constraints and assertions against the property's *Formal Contract:* fields. If the model adds, removes, or modifies any contract field, note that as a divergence.

Be specific and concise.
