# Dafny Review — Divergence Analysis

You are reviewing results from Dafny verification against an ASN (Architectural Specification Note). Classify each divergence as a genuine spec issue or a proof artifact.

## Background

Dafny is a verification-aware language. When a proof succeeds, we compare the proved statement against the original ASN property. A **divergence** occurs when the agent had to change the property to make the proof work — adding preconditions, strengthening invariants, or weakening conclusions.

A divergence can be:
1. **Genuine spec issue**: The ASN property is ambiguous, too strong, or missing a precondition that Dafny exposed — the spec should be updated
2. **Proof artifact**: Extra helper lemmas, quantifier instantiation hints, type coercions, ordering of proof steps, or encoding details — things the ASN doesn't need to care about

Common proof artifacts:
- Helper lemmas that decompose a proof step (the ASN property still holds as stated)
- Quantifier triggers or `calc` blocks added for Dafny's solver
- Type casts or conversions between `int` and `nat`
- Finiteness/well-foundedness requirements that are implicit in the ASN's mathematical domain
- `decreases` clauses for termination proofs
- `assert` hints to guide the verifier through intermediate steps

## ASN Under Review

{{asn_text}}

## Divergence Evidence

{{divergence_evidence}}

## Properties That Verified Clean

{{verified_summary}}

## Instructions

Write a review in the following format:

```
# Review of ASN-NNNN

Based on Dafny verification

## REVISE (only if genuine spec issues exist)

### Issue N: LABEL — description

For each genuine issue:
- State what the divergence reveals about the spec
- Quote the relevant ASN property text
- Explain specifically what needs to change (missing precondition, over-strong claim, ambiguous wording)
- If the fix is obvious, suggest it

## DEFER

### Topic N: description

For proof artifacts and clean verifications:
- Briefly explain why each is deferred
- Group proof artifacts together with explanation of why the ASN doesn't need to change

VERDICT: REVISE or CONVERGED
```

Rules:
- Only genuine spec problems or ambiguities belong in REVISE
- Proof artifacts go in DEFER with a clear explanation of why
- Be specific and concise — no boilerplate
- If ALL divergences are proof artifacts, verdict is CONVERGED
- If ANY divergence reveals a real spec issue, verdict is REVISE

Write the review using the Write tool to the output path provided below.
