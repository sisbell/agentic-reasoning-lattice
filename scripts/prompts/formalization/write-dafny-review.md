# Dafny Review — Divergence and Quality Analysis

You are reviewing Dafny verification results against an ASN (Architectural Specification Note). Two concerns: (1) divergences between proved statements and ASN properties, (2) proof quality.

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

## Proof quality criteria

Beyond correctness, a good proof is readable and maintainable. Check for:

**Over-proving.** Explicit `assert` statements that restate what the solver
already knows. If removing an assertion and re-verifying would succeed, the
assertion is clutter. Chains of assertions walking through every logical step
are a sign the proof is fighting the solver rather than structuring the
argument.

**Missing abstraction.** Repeated patterns that should be a named helper
function or lemma. A constructive witness function (e.g., `WithComponent`)
is better than inline sequence construction repeated in multiple places.

**Bloated case analysis.** Branches with identical proof structure that
could be collapsed into fewer cases. Empty branches that the solver handles
should stay empty — but branches with redundant explicit assertions should
be simplified.

**Fighting the solver.** Long proof bodies where a structural change would
make the proof trivial. Signs: deeply nested assertions, `calc` blocks
restating obvious arithmetic, manual witness construction when the solver
can find the witness. The fix is usually a better decomposition, not more
hints.

**Sparse is better.** In a recursive/inductive proof, only the non-trivial
case should have a body. Base cases the solver handles should be empty or
have at most a one-line comment. A 10-line case body where 8 lines are
assertions the solver doesn't need is worse than an empty body.

## ASN Under Review

{{asn_text}}

## Divergence Evidence

{{divergence_evidence}}

## Properties That Verified Clean

{{verified_summary}}

## Dafny Source

{{dafny_source}}

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

## QUALITY

### File: PropertyName.dfy — PASS | SIMPLIFY

For each file, assess proof quality. PASS means the proof is clean and
maintainable. SIMPLIFY means it verifies but should be leaner.

For SIMPLIFY findings:
- Identify the specific problem (over-proving, missing abstraction, bloat)
- Quote the problematic section
- Suggest the simpler form

## SKIP

### Topic N: description

For proof artifacts and clean verifications:
- Briefly explain why each is skipped
- Group proof artifacts together with explanation of why the ASN doesn't need to change

VERDICT: REVISE | SIMPLIFY | CONVERGED
```

Rules:
- Only genuine spec problems or ambiguities belong in REVISE
- Proof artifacts go in SKIP with a clear explanation of why
- Quality issues go in QUALITY with specific suggestions
- Be specific and concise — no boilerplate
- VERDICT is REVISE if any divergence reveals a real spec issue
- VERDICT is SIMPLIFY if no spec issues but proofs need quality improvement
- VERDICT is CONVERGED if all divergences are artifacts AND proofs are clean

Write the review using the Write tool to the output path provided below.
