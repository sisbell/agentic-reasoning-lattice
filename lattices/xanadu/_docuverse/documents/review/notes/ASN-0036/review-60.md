## Review of ASN-0036 Against ASN-0034 Foundation Statements

### 1. Stale Labels

**Finding 1.** The S8 proof cites T1 as `T1(i) (LexicographicOrdering, ASN-0034)`. No property named "LexicographicOrdering" exists in ASN-0034. T1's label is `LexicographicTotalOrder`.

> *"From v ≤ t with first divergence at m: t_m ≥ v_m by T1(i) (LexicographicOrdering, ASN-0034): the first component at which two equal-length tumblers disagree determines their order."*

**Finding 2.** D-CTG proof body, D-CTG-depth formal contract preconditions, and D-SEQ formal contract preconditions all cite T1 as `T1(i) (TumblerOrdering, ASN-0034)`. No property named "TumblerOrdering" exists in ASN-0034. The correct label is `LexicographicTotalOrder`. The two incorrect names are also inconsistent with each other.

> *D-CTG proof: "The strict inequality at component j follows from v₁ < v₂ by T1(i) (TumblerOrdering, ASN-0034)"*
> *D-CTG-depth formal contract: "T1(i) (TumblerOrdering, ASN-0034)"*
> *D-SEQ formal contract: "T1(i) (TumblerOrdering, ASN-0034)"*

Contrast with correctly-labeled citations elsewhere in the same ASN: `T4 (FieldSeparatorConstraint, ASN-0034)`, `T5 (PrefixContiguity, ASN-0034)`, `T3 (CanonicalRepresentation, ASN-0034)` — all match foundation labels exactly.

### 2. Structural Drift

(none)

### 3. Local Redefinitions

(none)

### 4. Registry Misclassification

(none)

### 5. Missing Dependencies

(none)

### 6. Exhaustiveness Gaps

(none)

---

`RESULT: 2 FINDINGS`
