## Surface Check: ASN-0036 vs. Foundation ASN-0034

---

### 1. Stale Labels

**Finding 1.** D-CTG-depth proof (SharedPrefixReduction section):

> "The strict inequality at component j follows from v₁ < v₂ by T1(i) **(LexicographicOrdering, ASN-0034)**"

T1's canonical label in the foundation is **LexicographicTotalOrder**. No property named "LexicographicOrdering" exists in ASN-0034.

---

**Finding 2.** D-SEQ proof (Step 3, contiguity of k-values):

> "By T1(i) **(TumblerOrdering, ASN-0034)**, v₁ < v₂ since they agree on components 1 through m − 1..."

Again, T1's canonical label is **LexicographicTotalOrder**. No property named "TumblerOrdering" exists in ASN-0034.

---

### 2. Structural Drift

(none)

---

### 3. Local Redefinitions

(none)

---

### 4. Registry Misclassification

(none)

---

### 5. Missing Dependencies

(none) — all foundation citations resolve within the declared dependency on ASN-0034.

---

### 6. Exhaustiveness Gaps

(none)

---

`RESULT: 2 FINDINGS`
