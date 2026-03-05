# Alloy Review — Counterexample Analysis

You are reviewing results from Alloy bounded model checking against an ASN (Architectural Specification Note). Classify each counterexample as a genuine spec issue or a modeling artifact.

## Background

Alloy is a bounded model checker. For `check` commands:
- **UNSAT** = assertion holds within finite scope (no counterexample)
- **SAT** = counterexample found (assertion violated)

For `run` commands:
- **SAT** = instance found (predicate is satisfiable — good for non-vacuity)
- **UNSAT** = no instance (predicate unsatisfiable — may indicate vacuity)

A counterexample on a `check` can be:
1. **Genuine spec issue**: The property is too strong, missing a precondition, contradictory, or ambiguous
2. **Modeling artifact**: The Alloy translation doesn't faithfully capture the ASN's intent — bounded scope, integer overflow at Int ceiling, atom identity vs structural equality, seq length limits, etc.

Common modeling artifacts:
- Bounded scope cannot supply enough witnesses (e.g., unboundedness properties)
- Integer overflow: `plus[x,1]` wraps at Int ceiling — guard with `plus[v,1] > v`
- Atom identity: Alloy atoms are distinct by identity; two `Tumbler` atoms with identical `comps` are still different atoms
- Sequence length limits: `seq` length bounded by `seq` scope keyword
- Non-vacuity `run` commands that are SAT are expected (they confirm the model isn't vacuous) — these are NOT counterexamples

## ASN Under Review

{{asn_text}}

## Counterexample Evidence

{{counterexample_evidence}}

## Properties That Passed

{{passed_summary}}

## Instructions

Write a review in the following format:

```
# Review of ASN-NNNN

Based on Alloy run-N

## REVISE (only if genuine spec issues exist)

### Issue N: LABEL — description

For each genuine issue:
- State what the counterexample reveals about the spec
- Quote the relevant ASN property text
- Explain specifically what needs to change (missing precondition, over-strong claim, ambiguous wording)
- If the fix is obvious, suggest it

## SKIP

### Topic N: description

For modeling artifacts and passed properties:
- Briefly explain why each is skipped
- Group modeling artifacts together with explanation of the Alloy limitation

VERDICT: REVISE or CONVERGED
```

Rules:
- Only genuine spec problems or ambiguities belong in REVISE
- Modeling artifacts go in SKIP with a clear explanation of why
- Be specific and concise — no boilerplate
- If ALL counterexamples are modeling artifacts, verdict is CONVERGED
- If ANY counterexample reveals a real spec issue, verdict is REVISE

Write the review using the Write tool to the output path provided below.
