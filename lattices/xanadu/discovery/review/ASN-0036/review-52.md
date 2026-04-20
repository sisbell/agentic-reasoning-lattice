## Surface Check: ASN-0036

### 1. Stale Labels

**Finding 1** — D-CTG-depth proof, paragraph beginning "The strict inequality at component j follows from v₁ < v₂":

> "The strict inequality at component j follows from v₁ < v₂ by T1(i) **(LexicographicOrdering, ASN-0034)**"

T1 is labeled **LexicographicTotalOrder** in the foundation. "LexicographicOrdering" does not exist.

**Finding 2** — D-SEQ proof, Step 3, paragraph beginning "Let k₁ < k₂ be two values attained":

> "By T1(i) **(TumblerOrdering, ASN-0034)**, v₁ < v₂ since they agree on components 1 through m − 1"

T1 is labeled **LexicographicTotalOrder** in the foundation. "TumblerOrdering" does not exist.

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
