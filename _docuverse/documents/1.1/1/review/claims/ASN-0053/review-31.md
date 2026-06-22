I read all foundation statements, then each ASN claim in full. Here is what I found.

---

**S3 (MergeEquivalence) — proof of s < r:** The proof writes "s < r since the union is non-empty" but gives no citation for the non-emptiness of ⟦α⟧. The non-emptiness requires start(α) < reach(α), which is TA-strict's postcondition instantiated at (start(α), width(α)). TA-strict does not appear in S3's depends list. The more direct route — r = max(reach(α), reach(β)) ≥ reach(α) > start(α) = s by TA-strict on α — makes the missing dependency explicit. Without the grounding citation the precondition chain for invoking WF is broken at the "s < r" gate.

**S3b (MergeSplitInverse) — non-emptiness of α and β:** Case A writes "start(α) < reach(α) = start(β) (since α is non-empty)" and "start(β) < reach(β) (β is non-empty)"; Case B uses the same pair of inequalities with the roles swapped. Both are invocations of TA-strict, but TA-strict appears in neither S3b's depends list nor its proof text. The interiority of the split point in each case rests on these inequalities; the depends list (S3, S4, WR) supplies no path back to the grounding axiom.

**S4 (SplitPartition) — p ∈ T not stated in preconditions:** The formal contract precondition says "p is an interior point of σ, i.e. s < p < reach(σ)" without stating p ∈ T. T1's ordering relation is defined over T × T; the expressions s < p and p < reach(σ) are ill-typed if p ∉ T. The proof later says "the given interior point, already in T" only in the postconditions block, not in the preconditions where it is needed to type-check the ordering constraints.

---

### TA-strict missing from S3 and S3b depends
**Class**: REVISE
**Foundation**: TA-strict (StrictIncrease) — postcondition `a ⊕ w > a` under Pos(w) and actionPoint(w) ≤ #a
**ASN**: S3 proof step "s < r since the union is non-empty"; S3b Case A "start(α) < reach(α) = start(β) (since α is non-empty)" and "start(β) < reach(β)"; S3b Case B analogous steps
**Issue**: Each of these steps uses start < reach for a well-formed span, which is exactly TA-strict instantiated at the span's (start, width). Neither S3 nor S3b lists TA-strict in its depends. The proof chain from these inequalities to a grounding foundation claim is broken.
**What needs resolving**: TA-strict must be added to S3's and S3b's depends lists, and the proof steps that use it must be made explicit rather than collapsed into "since α/β is non-empty."

---

### p ∈ T missing from S4 precondition
**Class**: REVISE
**Foundation**: T1 (LexicographicOrder) — strict total order on T, meaning all operands of < must be in T
**ASN**: S4 formal contract precondition: "p is an interior point of σ, i.e. s < p < reach(σ)"
**Issue**: The ordering constraints s < p and p < reach(σ) invoke T1, whose domain is T. The formal contract does not declare p ∈ T; the only mention of p's carrier membership appears in the postconditions block ("the given interior point, already in T"), not in the preconditions where the ordering is first asserted. A consumer discharging S4's preconditions would have no textual obligation to supply p ∈ T.
**What needs resolving**: Add p ∈ T explicitly to S4's preconditions, at the same level as s ∈ T (which is subsumed by σ's well-formedness) and reach(σ) ∈ T (established by TumblerAdd).

---

### WR formal contract lists derived facts as preconditions
**Class**: OBSERVE
**Foundation**: (presentation)
**ASN**: WR formal contract preconditions: "s < reach(σ) (TA-strict on T12); … divergence(s, reach(σ)) = k ≤ #s of type (i) (T1, Divergence)"
**Issue**: These are intermediate results established inside the proof, not obligations the caller must supply. Listing them as preconditions implies a caller must verify divergence type (i) before invoking WR, when in fact the sole input is a well-formed level-uniform span. The proof derives everything else from that assumption. The precondition block and the proof body are out of register with each other, which is visible but does not affect soundness.

---

VERDICT: REVISE