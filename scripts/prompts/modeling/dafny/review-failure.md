# Dafny Review — Verification Failure Analysis

Classify this verification failure as a genuine spec issue or a proof artifact.

## Background

Dafny verification can fail for several reasons:

1. **Genuine spec issue**: The property is too strong, missing a precondition, or contradictory — Dafny exposed a real problem
2. **Proof artifact**: The property is correct but the proof strategy is insufficient — needs better decomposition, helper lemmas, or different approach
3. **Compile failure**: Type errors, syntax issues, or missing declarations — the translation is wrong, not the spec

Common proof artifacts:
- Missing helper lemma that decomposes a complex step
- Quantifier instantiation the solver can't find automatically
- Induction hypothesis not applied at the right point
- Recursive function termination not proven (needs `decreases` clause)

## Property

{{property_text}}

## Dafny Source

{{dafny_source}}

## Verification Errors

{{verification_errors}}

## Instructions

Respond with exactly one of these formats:

For a proof artifact (property is correct, proof needs work):
```
PROOF_ARTIFACT | <brief explanation of what the proof needs>
```

For a compile/translation error:
```
TRANSLATION_ERROR | <what's wrong with the Dafny translation>
```

For a genuine spec issue:
```
SPEC_ISSUE | <what the failure reveals about the property>

What needs to change: <specific fix — missing precondition, over-strong claim, etc.>
```

Compare the Dafny declaration against the property's *Formal Contract:* fields:
- `requires` must match *Preconditions:* — any added/missing requires is a divergence
- `ensures` must match *Postconditions:* — any added/missing ensures is a divergence
- Axioms should be `axiom`, not `lemma`
- Definitions should be `function`/`predicate`, not `lemma`

Be specific and concise.
