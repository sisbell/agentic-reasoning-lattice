### 1. Stale Labels

**Finding 1.** D-CTG inline proof cites `"T1(i) (LexicographicOrdering, ASN-0034)"`:

> "The strict inequality at component j follows from v₁ < v₂ by T1(i) (LexicographicOrdering, ASN-0034): the first component at which two equal-length tumblers disagree determines their order."

The foundation labels T1 as **LexicographicTotalOrder**, not "LexicographicOrdering".

---

**Finding 2.** D-SEQ Step 3 and its Formal Contract cite `"T1(i) (TumblerOrdering, ASN-0034)"`:

> "By T1(i) (TumblerOrdering, ASN-0034), v₁ < v₂ since they agree on components 1 through m − 1 and differ first at component m where k₁ < k₂."

Same foundation property T1 (**LexicographicTotalOrder**), different wrong parenthetical name ("TumblerOrdering").

### 2. Structural Drift

(none)

### 3. Local Redefinitions

(none)

### 4. Registry Misclassification

**Finding 3.** S8a is listed in the properties table with status `"from T4, S7b (ASN-0034)"` — implying full derivation — but the body text explicitly says **"S8a is a design requirement"** and its formal contract contains an axiom:

> "*Axiom:* V-positions are element-field tumblers — the fourth field in T4's decomposition of element-level addresses."

Every other property with an "Axiom:" in its formal contract (S0, S2, S3, S7a, S7b, S8-fin, S8-depth, D-CTG, D-MIN) is classified as "design requirement" in the table. S8a's axiomatic premise is absent from its "from" chain, making the table entry inconsistent with the body.

### 5. Missing Dependencies

(none)

### 6. Exhaustiveness Gaps

(none)

---

`RESULT: 3 FINDINGS`
