# Dependency Check — ASN-0036 (cycle 1)

*2026-04-12 19:08*

## Dependency Report: ASN-0036 vs ASN-0034

---

### 1. Stale Labels

**F1 — S8a cites T5 under the wrong name.**

S8a body text reads:

> "Since all V-positions in subspace `s` extend the single-component prefix `[s]`, **T5 (PrefixContiguity, ASN-0034)** guarantees they form a contiguous interval under T1"

The foundation names this property `T5 — ContiguousSubtrees`. The label `PrefixContiguity` does not exist in the foundation. (Note: S8's own proof later cites the same property correctly as `T5 (ContiguousSubtrees, ASN-0034)`.)

**F2 — D-SEQ Step 3 cites T1 under the wrong name.**

D-SEQ Step 3 reads:

> "By **T1(i) (TumblerOrdering, ASN-0034)**, v₁ < v₂ since they agree on components 1 through m − 1 and differ first at component m where k₁ < k₂."

The foundation names this property `T1 — LexicographicOrder`. The label `TumblerOrdering` does not exist in the foundation. (Other T1 citations in the same ASN — in D-CTG-depth and D-CTG — correctly use `LexicographicOrder` or omit the parenthetical name.)

---

### 2. Structural Drift

(none)

---

### 3. Local Redefinitions

(none)

---

### 4. Registry Misclassification

(property table not provided in submitted material — cannot assess)

---

### 5. Missing Dependencies

(none) — all foundation citations are to ASN-0034, which is the sole declared dependency.

---

`RESULT: 2 FINDINGS`

## Result

Converged after 2 cycles.

*Elapsed: 578s*
