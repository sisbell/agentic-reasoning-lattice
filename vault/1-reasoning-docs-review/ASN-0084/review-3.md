# Review of ASN-0084

## REVISE

### Issue 1: Commutativity proof in R-BLK is incomplete and inconsistent across cases

**ASN-0084, R-BLK (Proof — commutativity)**: "For v = vⱼ + k in region α (3-cut case): π(v) = v + w_β …" / "The 4-cut μ case follows identically: π(v) = v + (w_β − w_α) …"

**Problem**: Three gaps.

(a) The proof covers 3-cut α, 3-cut β, exterior, and 4-cut μ. The **4-cut α and 4-cut β cases are not shown or mentioned**. The 4-cut α displacement is `w_β + w_μ` (not `w_β` as in 3-cut), and the 4-cut β formula maps from `c₂ + j` (not `c₁ + j`). These differ structurally from the 3-cut cases and cannot be dismissed by analogy without a word.

(b) The 4-cut μ case uses `π(v) = v + (w_β − w_α)`. When `w_α > w_β`, this expression is negative. No tumbler operation produces a negative displacement — this is integer arithmetic smuggled in without justification. The 3-cut β case, by contrast, correctly uses the explicit R-PPERM formula (`π(c₁ + j) = c₀ + j`). The μ case should do the same with R-SPERM.

(c) The proof mixes two incompatible styles: the 3-cut α case uses displacement shorthand (`π(v) = v + w_β`), while the 3-cut β case uses explicit permutation formulas (`v = c₁ + (j+k)`, `π(v) = c₀ + (j+k)`). This inconsistency makes the proof harder to verify and obscures whether each case is rigorous.

**Required**: Prove commutativity uniformly for all six region cases (exterior, 3-cut α, 3-cut β, 4-cut α, 4-cut μ, 4-cut β) using the explicit R-PPERM/R-SPERM formulas and natural-number associativity. The 4-cut cases are one-liners — for instance, 4-cut μ: `vⱼ = c₁ + j'`, so `π(vⱼ + k) = c₀ + w_β + (j' + k)` by R-SPERM and `π(vⱼ) + k = (c₀ + w_β + j') + k = c₀ + w_β + (j' + k)` by associativity.

---

### Issue 2: R-S3 label collision — swap clause vs. S3 preservation lemma

**ASN-0084, SwapPostcondition / Properties table**: The label `R-S3` is used for two unrelated things:
- The third swap clause: `M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j)` (defining where α content goes)
- The properties table entry: "Rearrangement preserves S3: ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C')"

**Problem**: A reader citing "R-S3" has no way to know which is meant without surrounding context. The S3 preservation derivation in the State and Vocabulary section doesn't carry the label R-S3 at all — the label appears only in the properties table and in the swap clause.

**Required**: Rename one. The swap clauses follow a systematic pattern (R-S1, R-S2, R-S3), so rename the S3 preservation lemma — e.g., `R-RI` (Rearrangement Referential Integrity) or `R-S3-PRES`.

---

### Issue 3: Block decomposition variable β collides with region β

**ASN-0084, Block Decomposition Transformation**: "A *block decomposition* of M(d) is a finite set B = {β₁, ..., βₘ} of blocks"

**Problem**: The letter β is already in use for the second region of the cut-point partition (`β = {v ∈ V_S(d) : c₁ ≤ v < c₂}`). In the worked examples, both senses appear: block `β₃ = ([1,5], E, 3)` is classified into region β during Phase 2. The sentence "block β₃ lies in region β" is needlessly confusing.

**Required**: Use a different letter for blocks in the decomposition — e.g., `B = {b₁, ..., bₘ}` or `B = {γ₁, ..., γₘ}`.

---

### Issue 4: "I-address multiset is invariant" — claim exceeds proof

**ASN-0084, State and Vocabulary**: "We derive that the I-address multiset is invariant."

**Problem**: The derivation shows `ran(M'(d)) = ran(M(d))`, which is set equality of the ranges. The word "multiset" claims that multiplicities are preserved (the number of V-positions mapping to each I-address is the same before and after). This stronger claim is true — it follows from π being a bijection — but the step from set equality to multiset equality is not shown.

**Required**: Either downgrade the claim to "range" (which suffices for S3 preservation) or add the one-sentence argument: since π is a bijection, for each I-address `a`, the preimage `{v : M(d)(v) = a}` is in bijection with `{π(v) : M(d)(v) = a} = {u : M'(d)(u) = a}`, so multiplicities are preserved.

---

### Issue 5: R-FRAME in properties table has no standalone counterpart

**ASN-0084, Properties Introduced table**: "R-FRAME | FRAME | Other subspaces, other documents, and content store are preserved | introduced"

**Problem**: No result labeled `R-FRAME` exists in the body. The frame conditions appear as `R-FRAME-P(a)(b)(c)` within the PivotPostcondition and `R-FRAME-S(a)(b)(c)` within the SwapPostcondition. The table entry is an unresolvable citation.

**Required**: Either split the table entry into `R-FRAME-P` and `R-FRAME-S`, or add a one-line consolidation in the body: "R-FRAME comprises R-FRAME-P and R-FRAME-S above."


## OUT_OF_SCOPE

### Topic 1: Generalization to V-position depth m > 2
**Why out of scope**: The ASN restricts to depth-2 V-positions and notes the generalization via D-CTG-depth. Establishing the generalization formally (showing all properties carry over to arbitrary depth) is a distinct contribution, not an error in this ASN.

### Topic 2: Systematic invariant preservation checklist
**Why out of scope**: The ASN proves the non-trivial invariants (S0 via frame, S2 via R-PIV/R-SWP, S3 via range preservation, S8 via R-BLK). Domain-dependent invariants (S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ) are trivially preserved because dom(M'(d)) = dom(M(d)), but the ASN doesn't state this explicitly. A comprehensive invariant preservation table would strengthen the ASN but its absence is not an error — the trivial cases follow from one sentence about domain preservation.

VERDICT: REVISE
