# Review of ASN-0051

## REVISE

### Issue 1: SV6 (BoundaryExclusion) proof is wrong and the theorem is likely false

**ASN-0051, Content Allocation and the Boundary Theorem**: "By T4 (HierarchicalParsing), an element-level tumbler has exactly three zero separators, so no further child-spawning (TA5 with k > 0) can produce a valid element-level address — it would exceed the three-separator limit."

**Problem**: This claim is false for k' = 1. TA5(d) with k = 1 from an element-level tumbler t (zeros(t) = 3) produces t' with #t' = #t + 1, zero intermediate positions (k − 1 = 0), and a final component of 1. The result has zeros(t') = 3 — still element-level, T4 satisfied. The proof conflates all child-spawning (k > 0) with separator-adding child-spawning (k ≥ 2).

Counterexample: Document D allocates elements at ordinals [1] through [n], producing I-addresses [D.0.1] through [D.0.n]. A link is created with endset span ([D.0.1], [0,0,0,0,0,0,n]), so reach = [D.0.n+1]. Later, the allocator spawns a child via inc([D.0.n], 1) = [D.0.n.1], and K.α allocates content there. Address [D.0.n.1] is element-level (zeros = 3), has origin D (same document prefix), and satisfies [D.0.n] < [D.0.n.1] < [D.0.n+1] (prefix rule at position 7, then component comparison). So [D.0.n.1] ∈ ⟦([D.0.1], [0,0,0,0,0,0,n])⟧, contradicting SV6.

The proof's Case 2 has a secondary error: it cites TA7a (SubspaceClosure) for origin-closure, but TA7a establishes subspace closure (first element-field component), not origin closure (document prefix N.0.U.0.D). Origin closure does hold when the action point is within the element field — by TumblerAdd's copy behavior at positions before the action point — but the cited lemma doesn't establish it, and the proof doesn't address spans whose action point is outside the element field.

**Required**: Either (a) establish a missing invariant that constrains endset span widths to prevent child-depth addresses from entering the range (e.g., restrict coverage to same-depth tumblers), or (b) abandon SV6 and characterize what actually enters existing endset coverage over time. SV13(f) must be corrected accordingly.

### Issue 2: SV11 (PartialSurvivalDecomposition) proof invokes S1 without verifying its precondition

**ASN-0051, Partial Survival**: "The intersection of two convex sets under a total order is convex, so each non-empty term is itself a contiguous set expressible as a span (S1, IntersectionClosure, under level-compatibility)."

**Problem**: S1 requires level-uniform spans with level_compat(start(α), start(β)), i.e., #start(α) = #start(β). An endset span's start s is an element-level I-address; a mapping block's I-start a is also element-level (by S3 + S7b). But element-level tumblers can have different lengths — element fields can have multiple components (e.g., [1] vs [1,1] via child allocators with k = 1). The ASN never verifies that the endset span start and the mapping block I-start have the same tumbler length. S1's precondition is not discharged.

The conclusion is likely salvageable: the I-extent of a mapping block consists of same-length tumblers (TA5(c) preserves length), and ordinal increment is monotonic (TA-strict), so the intersection of any T1-interval with a mapping block's I-extent is a contiguous subsequence of same-length tumblers, expressible as a level-uniform span. But this argument uses monotonicity within the block, not S1.

**Required**: Replace the S1 invocation with the correct argument: the intersection of a T1-interval with a mapping block's I-extent {a + k : 0 ≤ k < n} is contiguous because ordinal increment is monotonic, and all elements share the same tumbler length, so the contiguous subsequence is a level-uniform span.

### Issue 3: SV10 (DiscoveryResolutionIndependence) uses informal language in its formal statement

**ASN-0051, The Discovery-Resolution Distinction**: `"(E Σ, a, d, s :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ resolve(Σ.L(a).s, d) yields only partial coverage)"`

**Problem**: "yields only partial coverage" is not a formal predicate. The intended meaning appears to be π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s) — the projection is a proper subset of the coverage — but this is never stated precisely.

**Required**: Replace with a formal predicate, e.g.: `resolve(Σ.L(a).s, d) ≠ ∅ ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s)`, or whatever the intended condition is.

### Issue 4: SV9 (DiscoveryMonotonicity) applies "dom" to a set

**ASN-0051, Link Discovery**: `"(A Σ → Σ' :: dom(discover_s(A) in Σ) ⊆ dom(discover_s(A) in Σ'))"`

**Problem**: `discover_s(A) = {a ∈ dom(Σ.L) : coverage(Σ.L(a).s) ∩ A ≠ ∅}` — this is a set, not a function. "dom" is meaningless on a set. The intended statement is `discover_s(A) in Σ ⊆ discover_s(A) in Σ'`.

**Required**: Drop "dom" from both sides.

### Issue 5: No concrete worked example

**ASN-0051, throughout**

**Problem**: The ASN introduces projection, resolution, discovery, vitality, and partial survival — none verified against a specific scenario. The standards require: "the ASN should verify its key postconditions against at least one specific scenario from the implementation evidence." A single worked example (e.g., a document with five I-addresses, a link whose from-endset covers three of them, followed by a contraction removing one — checking π, resolve, and discover before and after) would ground every definition and expose any definitional errors immediately.

**Required**: Add at least one concrete example that exercises projection, resolution, and discovery through an arrangement change (extension, contraction, or reordering), with explicit tumbler values and step-by-step evaluation.

## OUT_OF_SCOPE

### Topic 1: Resolve semantics under within-document sharing
**Why out of scope**: When multiple V-positions map to the same I-address (S5), resolve returns all of them. The ASN correctly notes |resolve(e,d)| ≥ |π(e,d)| but does not specify how a reader should interpret multiple resolution hits for a single I-address. This is an interface/presentation concern, acknowledged in the open questions.

### Topic 2: Fragment ordering and canonical representation
**Why out of scope**: Whether the fragments of a partially surviving endset have a canonical ordering is an index/query design question. The ASN establishes that fragments are spans and their union is a normalizable span-set (via S8). The canonical ordering question is acknowledged in the open questions and belongs in an enfilade or index ASN.

### Topic 3: Discovery latency and consistency model
**Why out of scope**: Whether newly created links are discoverable immediately or eventually is a distributed systems concern. The ASN correctly specifies the steady-state invariants (SV8, SV9) without constraining the consistency model.

VERDICT: REVISE
