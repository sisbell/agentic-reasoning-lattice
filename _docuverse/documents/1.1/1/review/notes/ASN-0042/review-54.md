# Review of ASN-0042

## REVISE

### Issue 1: Worked example — `a₃` invoked in the Fork scenario without provenance in Σ.B
**ASN-0042, Worked Example, Fork (O10)**: "Suppose `π_A` wishes to modify the content at `a₃ = [1, 0, 7, 0, 1, 0, 1]`. Since `ω(a₃) = π_N ≠ π_A`..."
**Problem**: O10's formal contract requires `a ∈ Σ.B`. The bootstrap section presents its seed list as exhaustive ("we additionally seed the following addresses into `Σ_0.B`"), and the explicit list does not include `a₃`. The trajectory `Σ_0 → Σ_1 → Σ_2 = Σ_pre` then baptizes only the family `{[1, 0, 2, 0, k]}` and the namespace addresses `[1, 0, 2, 1], [1, 0, 2, 2]`, none of which is `a₃`. So `a₃ ∉ Σ_pre.B`, and `ω_{Σ_pre}(a₃)` is undefined — the precondition `a ∈ Σ.B` of the O10 invocation is unwitnessed.
**Required**: Either add `a₃` to the explicit Σ_0.B seed list (alongside `a_1`, with B6/B1 verification), or insert an explicit trajectory step in which `π_N` baptizes `a₃` (most-specific covering principal of `[1, 0, 7, 0, 1, 0, 1]` in `Π_0` is `π_N`; B6 check: `zeros([1, 0, 7, 0, 1]) + 1 = 3 ≤ 3`). Without one of these, the fork example invokes O10 with an unsatisfied precondition.

### Issue 2: AccountField postcondition (a) — "satisfying T4 and T4a" is malformed
**ASN-0042, acct(a) AccountField, Formal Contract Postconditions (a)**: "`acct(a)` is a valid tumbler satisfying T4 and T4a."
**Problem**: T4a (SyntacticEquivalence) is a Consequence of T4 — a biconditional asserting that T4's three positional clauses are equivalent to "every field segment is non-empty." A tumbler does not "satisfy T4a"; T4a is a meta-statement about T4. The phrasing conflates T4 with one of its derived equivalences.
**Required**: Drop "and T4a." T4 already entails the segment-non-emptiness reading via T4a.

### Issue 3: OwnershipDomainPermanence Step 4 is structurally redundant
**ASN-0042, OwnershipDomainPermanence proof, Step 4**: "*Step 4 — the case `pfx(π') ≼ pfx(π)` is impossible.* The above steps yielded `pfx(π) ≺ pfx(π')`; for completeness we note that the opposite nesting cannot arise."
**Problem**: Step 2 already established `pfx(π) ≺ pfx(π')` (strict prefix), which by the foundation's Prefix relation entails `#pfx(π) < #pfx(π')` and hence excludes `pfx(π') ≼ pfx(π)` directly. Step 4 derives nothing new — it reasserts a consequence of Step 2. As written it could be misread as supplying a case that Steps 1–3 left open.
**Required**: Either delete Step 4 or fold its single sentence into Step 2 (e.g., "and hence `pfx(π') ⋠ pfx(π)`") so the proof's case structure remains exhaustive without a phantom case.

### Issue 4: "By the same reasoning" in acct(a) Case zeros = 3
**ASN-0042, acct(a) AccountField proof, Case `zeros(a) = 3`**: "By the same reasoning as the `zeros(a) = 2` case — `N(a)` and `U(a)` each have at least one strictly positive component..."
**Problem**: The cases zeros=2 and zeros=3 are structurally identical for the construction `acct(a) = N(a) ++ [0] ++ U(a)`, since the trailing `D(a)` and `E(a)` fields don't enter the construction. The "by the same reasoning" gloss obscures the actual invariant being reused.
**Required**: State the structural fact explicitly: "the construction `acct(a) = N(a) ++ [0] ++ U(a)` depends only on `N(a)` and `U(a)`, which are non-empty and positive-componented by T4a + T4 regardless of whether further fields exist. Hence the zeros=2 verification transfers verbatim." This is two sentences, not a real expansion, and removes the citation-to-prior-case smell.

## OUT_OF_SCOPE

(None — the ASN already records its scope boundaries appropriately in the Scope section and Open Questions.)

VERDICT: REVISE
