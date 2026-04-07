## Surface Check: ASN-0036 vs. ASN-0034

---

### 1. Stale Labels

**Finding 1 — "TumblerOrdering"**

D-CTG-depth formal contract preconditions cite: `T1(i) (TumblerOrdering, ASN-0034)`
D-SEQ proof: `By T1(i) (TumblerOrdering, ASN-0034), v₁ < v₂ since they agree on components 1 through m − 1`

Foundation T1 is labeled **LexicographicTotalOrder**. No property named "TumblerOrdering" exists in ASN-0034.

**Finding 2 — "LexicographicOrdering"**

S8 proof (uniqueness within subspace): `tⱼ > vⱼ (from v ≤ t by T1(i) (LexicographicOrdering, ASN-0034))`
D-CTG-depth proof body: `The strict inequality at component j follows from v₁ < v₂ by T1(i) (LexicographicOrdering, ASN-0034)`

Foundation T1 is labeled **LexicographicTotalOrder**, not "LexicographicOrdering". Two different wrong names are used for the same property across different proof sections — "TumblerOrdering" in the formal contracts, "LexicographicOrdering" in the proof bodies.

---

### 2. Structural Drift

(none)

---

### 3. Local Redefinitions

**Finding 3 — δ(k, m) re-introduced locally**

S8-depth formal contract: `*Definition:* δ(k, m) = [0, …, 0, k] of length m; for k > 0, actionPoint(δ(k, m)) = m.`

OrdinalDisplacement in ASN-0034 already defines this: *"For natural number n ≥ 1 and depth m ≥ 1, the ordinal displacement δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m."*

The S8-depth formal contract restates OrdinalDisplacement verbatim rather than citing it. The definition also does not appear in the properties table with status `introduced`, meaning the foundation concept was absorbed into S8-depth's formal contract without acknowledgment.

---

### 4. Registry Misclassification

(none)

---

### 5. Missing Dependencies

(none)

---

### 6. Exhaustiveness Gaps

(none)

---

`RESULT: 3 FINDINGS`
