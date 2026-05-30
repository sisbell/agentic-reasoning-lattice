# Review of ASN-0084

## REVISE

### Issue 1: Post-state S8 maximality is deferred to the same downstream result in three separate places

**ASN-0084, "Invariant preservation" / "Canonical decomposition" / R-BLK closing paragraph**:
- "post-state S8 is established where it is consumed, in R-BLK below."
- "Foundation S8 (CorrespondenceRunPartition, ASN-0036) supplies this maximal-run partition and its uniqueness for any arrangement satisfying the ASN-0036 invariants."
- "The S8-unique maximal partition of M'(d) ... follows from foundation S8 (ASN-0036): its preconditions S8-fin, S2, S3, S8a, S8-depth are all preserved by the Invariant-preservation audit above..."

**Problem**: This is the forward-reference accretion pattern — multiple paragraphs in different sections all deferring the same claim (post-state S8 / maximal-run existence) to the same downstream location. The audit defers to R-BLK; R-BLK and the "Canonical decomposition" paragraph both re-derive the identical "follows from foundation S8 because the preconditions are preserved" statement. The substance is established once; the other two occurrences are restatement the precise reader must reconcile.

**Required**: State the post-state-S8 discharge once (it is genuinely a one-line consequence: dom is preserved and the S8 preconditions are in the invariant audit), and have the other sites point to it without re-arguing it.

### Issue 2: The Merge operation's operational use (canonical-partition recovery) is re-announced as deferred in four locations

**ASN-0084, "Canonical decomposition" / R-BLK final paragraph / CanonicalRunDecomposition table row / Open Question 6**:
- "The Merge operation above relates a valid partition to its maximal-run (coarsest) decomposition..."
- "The partition B' is valid but not necessarily maximal: B' may contain V-adjacent, I-adjacent pairs..."
- table: "operational reduction deferred to a future ASN"
- "By what operational process is the S8-unique maximal (canonical) run partition recovered from the valid partition B' that R-BLK produces...?"

**Problem**: That the merge-to-canonical *algorithm* is future work is a single fact stated four times across four sections. Defining Merge and proving it preserves S8-cons is legitimate content; repeatedly announcing that its operational deployment is deferred is not — it is the "multiple paragraphs defer to the same downstream location" pattern.

**Required**: Keep the Merge definition + S8-cons proof. Note the operational-recovery deferral exactly once (the Open Question is the natural home) and remove the duplicate announcements in the Canonical-decomposition prose, R-BLK closing, and the table row.

### Issue 3: Width-positivity derivation silently relies on CS3/CS4, the very clause R-CS3 proves is load-bearing

**ASN-0084, "Consequences of R-PRE" (Width positivity)**: "R-PRE(iv) places every depth-2 subspace-S position with ordinal in [ord(c_i), ord(c_{i+1})) into V_S(d), so the count of V-positions in [c_i, c_{i+1}) equals ord(c_{i+1}) − ord(c_i)."

**Problem**: The step "v ∈ [c_i, c_{i+1}) for subspace-S v ⟺ ord(v) ∈ [ord(c_i), ord(c_{i+1}))" holds only because the cuts themselves are subspace-S (CS3) at depth 2 (CS4) — otherwise the T1 comparison v vs c_i does not reduce to the ordinal comparison, and the count can be 0 while the ordinal difference is positive. R-CS3 (the very next-but-one lemma) constructs exactly this failure: an all-subspace-2 cut sequence yields ord-differences of 1 but α = β = ∅. So the derivation's conclusion "region non-degeneracy follows from (iii) and (iv)" is correct only because CS3 ⊂ (iii), yet the load-bearing role of CS3 is buried inside "subspace-S position." For internal consistency with R-CS3, name where CS3/CS4 enter this step.

**Required**: At the alignment step, cite CS3 (and CS4) explicitly as the reason cut ordinals correspond to V_S(d) positions, so the proof and R-CS3 agree on which clause carries the non-degeneracy.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: Correctly identified in Open Questions; generalizing the cut count and characterizing the closure of rearrangement composition is new territory, not a defect in the 3/4-cut treatment here.

### Topic 2: Documents with text-subspace depth m_1 > 2 and cross-subspace transposition
**Why out of scope**: The ASN explicitly restricts to m_1 = 2 and intra-text-subspace operation; lifting these restrictions is future work, and the scope statement is clear and self-consistent.

VERDICT: REVISE
