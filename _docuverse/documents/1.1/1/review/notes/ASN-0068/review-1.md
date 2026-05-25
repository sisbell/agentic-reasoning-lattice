# Review of ASN-0068

## REVISE

### Issue 1: CV-MAX proof is a sketch, not a proof
**ASN-0068, "The Result" (CV-MAX)**: "The uniqueness of the maximal decomposition follows the same line of reasoning that underwrites the canonical mapping-block decomposition of an arrangement (M12, ASN-0058). Walking left from any pair (v_a, v_b) ∈ corr_{a,b} while pointwise correspondence and restriction membership both hold reaches a unique left-maximal extension..."
**Problem**: The CV setting differs from M12 in two load-bearing ways: (i) the relation is over two documents requiring lockstep offsets, not a single function's blocks; (ii) the relation is many-to-many under self-transclusion, not single-valued. The "walking left" argument does not establish uniqueness. The real argument requires: given pair (v_a, v_b) in two purported maximal runs (v¹_a, v¹_b, n¹) and (v²_a, v²_b, n²), shift-strict-increase (TS4, ASN-0034) forces v¹_a − v²_a = v¹_b − v²_b (lockstep offset), then maximality of one run contradicts extensibility of the other.
**Required**: A proof that explicitly (a) shows the lockstep offset relationship via shift injectivity (TS2/TS4, ASN-0034), and (b) derives the contradiction at the inner endpoint when two runs containing the pair have distinct starting points.

### Issue 2: No concrete example
**ASN-0068, throughout**: No worked example anywhere in the ASN.
**Problem**: The ASN claims uniqueness of the maximal decomposition and discusses self-transclusion producing multiple runs, but never verifies these claims against any specific configuration. The reader has no way to check that the definitions produce the claimed behavior.
**Required**: At least one example, e.g., d_a with V-positions [s_C,1]→a, [s_C,2]→b, [s_C,3]→c and d_b with [s_C,1]→x, [s_C,2]→a, [s_C,3]→b. Verify the result is {(v_a+0, v_b+1, 2)} — one length-2 run, not two length-1 runs. A second example with self-transclusion (same I-address at multiple positions on both sides) to verify the many-to-many decomposition.

### Issue 3: k = 0 case for "v + k" notation not handled
**ASN-0068, "The Result"**: "The notation `v + k` denotes shift in the V-position depth of each document (ASN-0034)."
**Problem**: ASN-0034's OrdinalShift requires n ≥ 1; δ(0, m) is not a positive tumbler. The run condition uses `v_a + k` for `0 ≤ k < n`, so k = 0 is required. ASN-0058's OrdinalShiftBase convention defines `t + 0 = t`, but ASN-0068 does not cite it.
**Required**: Cite OrdinalShiftBase (ASN-0058) or state the convention `v + 0 := v` explicitly.

### Issue 4: Result type undefined
**ASN-0068, "The Input"**: "compareversions : (E_doc × SpanSet) × (E_doc × SpanSet) → Result"
**Problem**: The result type "Result" appears in the signature but is never defined. The text describes the result as a set of maximal correspondence runs (triples) and notes an equivalent span-pair presentation, but no formal type is given.
**Required**: Define Result, e.g., `Result := P(T × T × ℕ⁺)` (set of triples) or equivalently `P(Span × Span)`.

### Issue 5: CV-ATOM is redundant with CV-MAX
**ASN-0068, "Atomicity and Granularity" (CV-ATOM)**: "every V-position pair (v_a, v_b) with M(d_a)(v_a) = M(d_b)(v_b) = a is witnessed by a maximal correspondence run of width at least 1 containing it."
**Problem**: Every correspondence run has width n ≥ 1 by definition; "of width at least 1" adds nothing. The "witnessed by a max run" claim is exactly CV-MAX. As stated, CV-ATOM is a restatement of CV-MAX with extra words.
**Required**: Either delete CV-ATOM, or restate it as a non-trivial claim about granularity (e.g., that an isolated single-byte match producing an n=1 run is not absorbed into adjacent non-matching content, distinguishing the operation from threshold-based or block-aligned alternatives).

### Issue 6: Link-subspace case is essentially trivial
**ASN-0068, "The Input"**: "Comparing arrangements in s_L is meaningful (one can ask 'which link arrangements do two documents share?') but is a separate semantic concern, and the development here applies uniformly to either single subspace."
**Problem**: By CL-OWN (ASN-0047), every V-position in s_L of d's arrangement maps to a link with origin = d. For d_a ≠ d_b, no link can have both origins, so `M(d_a)(v_a) = M(d_b)(v_b)` for s_L positions has no solutions — corr_{a,b} restricted to s_L is empty for distinct documents. For d_a = d_b, CL-UNIQ makes M(d)|_{dom_L} injective, so the only correspondences are identity. The s_L case is degenerate, not a parallel meaningful comparison.
**Required**: Either acknowledge this consequence (the s_L comparison is structurally trivial under CL-OWN; the operation specializes to s_C in practice) or explain why s_L comparison is non-trivial despite CL-OWN, perhaps with a corollary that compareversions on s_L for d_a ≠ d_b returns ∅.

### Issue 7: Empty-restriction case not addressed
**ASN-0068, "The Input" (CV-IN)**: "R_a, R_b are normalized V-span-sets (ASN-0053)."
**Problem**: The empty span-set ⟨⟩ is vacuously normalized and satisfies all preconditions. When R_a = ⟨⟩, ⟦R_a⟧ = ∅, corr_{a,b} = ∅, and the result is ∅. This boundary case is admissible but not characterized.
**Required**: Add a sentence under CV-IN or CV-MAX noting that empty restrictions yield empty results.

### Issue 8: Self-comparison (d_a = d_b) not addressed
**ASN-0068, "The Input"**: "d_a, d_b ∈ E_doc"
**Problem**: The input admissibility allows d_a = d_b. The behavior should be characterized: every position trivially corresponds to itself, plus self-transclusions. The result is the identity decomposition plus extra runs for any self-transclusion.
**Required**: Either explicitly handle the self-comparison case (state what the result is) or explicitly exclude it via a precondition `d_a ≠ d_b`. The current text neither covers nor forbids it.

### Issue 9: CV-SYM proof not shown
**ASN-0068, "Symmetry"**: "This is immediate from the symmetry of the underlying relation... The maximal decomposition extends this pointwise symmetry to run-level symmetry: a maximal run in one ordering corresponds to a maximal run in the other, related by the swap of operand positions within the triple."
**Problem**: "Immediate" and "extends to" are not proofs. The claim requires verifying: (a) swapped triple is a correspondence run (immediate from equality symmetry), (b) maximality is preserved under swap (the conditions enumerate over both sides symmetrically). The verification is short but should be shown.
**Required**: A two-line verification showing that the maximality conditions in the swapped orientation are the same disjunction as in the original.

### Issue 10: Span-pair projection well-formedness not verified
**ASN-0068, "The Result"**: "A correspondence run (v_a, v_b, n) projects naturally to a pair of V-spans (σ_a, σ_b): σ_a = (v_a, δ(n, m_a)) and σ_b = (v_b, δ(n, m_b)). Both spans are level-uniform..."
**Problem**: Level-uniformity and T12 preconditions are asserted but not verified. The verification requires: Pos(δ(n, m_a)) (from n ≥ 1, by OrdinalDisplacement, ASN-0034); actionPoint(δ(n, m_a)) = m_a ≤ #v_a = m_a (S8-depth, ASN-0036); #start = #width = m_a (level-uniformity). One short paragraph.
**Required**: A brief verification chaining the foundation citations to discharge T12 and level-uniformity.

### Issue 11: "v − 1" predecessor notation insufficiently grounded
**ASN-0068, "The Result"**: "(Here 'valid V-predecessor at depth m' means the unique tumbler v' of depth m with v' + 1 = v, if such exists at depth m within the relevant subspace. By S8a and D-MIN★ (ASN-0047), the V-position [S, 1, ..., 1] is the minimum at any given depth and has no predecessor; in that case left-maximality is automatic.)"
**Problem**: The parenthetical defines predecessor inline and asserts D-MIN★ supplies the minimum, but uniqueness of the predecessor (given existence) is not established. By D-SEQ★ (ASN-0047), V-positions have the form [S, 1, ..., 1, k], so the predecessor of [S, 1, ..., 1, k] for k > 1 is [S, 1, ..., 1, k-1] (unique by shift injectivity, TS2/ASN-0034). The argument is short but absent.
**Required**: Cite TS2 (or shift injectivity) for predecessor uniqueness; cite D-SEQ★ for the structural form that makes the predecessor obvious.

## OUT_OF_SCOPE

### Topic 1: Replication coherence
**Why out of scope**: Properly raised as an open question. Replication/inter-server protocol is on the excluded list.

### Topic 2: Multi-version composition and history traversal
**Why out of scope**: Properly raised as open questions. Composing multiple comparisons across version histories is a meta-operation deserving its own ASN.

### Topic 3: Concurrent state modification during comparison
**Why out of scope**: Properly raised as an open question. Concurrent execution model is outside this ASN's scope.

### Topic 4: Complexity bounds on result size
**Why out of scope**: Properly raised in the bounded-size open question. Complexity is an operational/implementation concern.

VERDICT: REVISE
