# Review of ASN-0048

## REVISE

### Issue 1: TA7a (SubspaceClosure) applied to I-addresses without justification

**ASN-0048, Content allocation**: "In the ordinal-only formulation (TA7a), a₁ = [x] and inc([x], 0) = [x + 1], so a₂ = [x + 1] = a₁ ⊕ [1]; by induction, aᵢ = a₁ ⊕ [i − 1]."

**Problem**: TA7a defines the ordinal-only formulation for V-space positions within a subspace: "a position in subspace S with identifier N and ordinal x is represented as the single-component tumbler [x] for arithmetic purposes, with N held as structural context." I-space addresses are element-level tumblers (form N.0.U.0.D.0.E), not V-space positions. TA7a does not cover them. The same misapplication recurs in I7(c) where `aⱼ ⊕ [δ + k] = (aⱼ ⊕ [δ]) ⊕ [k]` is applied to I-addresses, and in I7(d) where `aₖ₊₁ = a₁ ⊕ [k]` treats I-addresses as single-component ordinals.

The mathematics is correct — single-component ordinal arithmetic works identically regardless of interpretation. But TA7a is scoped to V-space, and citing it for I-addresses is unjustified by the foundation. Under full tumbler arithmetic, `a₁ ⊕ [1]` with a multi-component `a₁` has action point k = 1, which operates on the node field component, not the element ordinal. The ordinal-only formulation rescues this, but that formulation isn't established for I-addresses.

**Required**: Either (a) establish an analogous ordinal-only formulation for I-addresses within a single document's allocation stream — the document prefix N.0.U.0.D.0 serves as structural context paralleling TA7a's subspace identifier — or (b) derive contiguity directly from TA5(c) and inc(·, 0) without invoking TA7a: each `inc(·, 0)` increments at `sig(t)` by exactly 1, giving `aᵢ₊₁ = inc(aᵢ, 0)`, from which the correspondence properties follow.

### Issue 2: I0(d) derivation from T9 alone is insufficient

**ASN-0048, Content allocation**: "Clause (d) is T9 (ForwardAllocation, ASN-0034): d's allocator produces addresses strictly increasing over time."

**Problem**: I0(d) quantifies over ALL `a ∈ dom(C)` with `origin(a) = d` — every I-address ever allocated under d's prefix. T9 guarantees ordering within a single allocator stream (`same_allocator(a, b) ∧ allocated_before(a, b) ⟹ a < b`), but T10a permits child allocator spawning. Child allocations under d's prefix also satisfy `origin(a) = d`, yet T9 does not order them against the parent stream's subsequent allocations.

The fact is true: by T1's lexicographic ordering, a parent's next sibling allocation P.(x+1) exceeds all child allocations P.x.* because they diverge at the first element component where x < x+1. But this argument requires T1 and the prefix structure, not T9 alone.

**Required**: Either (a) state explicitly that d's content allocation uses a single stream — no child spawning for content — which holds if INSERT is the sole content-creating operation and always uses `inc(·, 0)`, or (b) provide the cross-allocator ordering argument via T1 lexicographic comparison at the divergence point.

### Issue 3: Incomplete invariant verification

**ASN-0048, Preservation**: "We verify that INSERT maintains the invariants established by ASN-0036 and ASN-0047. The method: check each invariant against I-post."

**Problem**: The section verifies S0, S2, S3, S8a, S8-depth, S8-fin, P0, P1, P2, P4 but omits P6 (ExistentialCoherence), P7 (ProvenanceGrounding), and P7a (ProvenanceCoverage) — all three listed in ASN-0047's ReachableStateInvariants as holding at every reachable state. Each is straightforward:

- **P6**: For fresh `aᵢ`, `origin(aᵢ) = d ∈ E_doc = E'_doc` (by I0(b), I-pre, I-post(b)). For existing `a ∈ dom(C)`, pre-state P6 and `E_doc = E'_doc`.
- **P7**: For `(aᵢ, d) ∈ R' \ R`, `aᵢ ∈ dom(C')` by Phase 1. For `(a, d') ∈ R`, `a ∈ dom(C) ⊆ dom(C')` by pre-state P7 and S1.
- **P7a**: For fresh `aᵢ`, `(aᵢ, d) ∈ R'` by Phase 4. For existing `a ∈ dom(C)`, pre-state P7a and P2.

The claim of verifying "the invariants established by ASN-0036 and ASN-0047" should match what is actually checked.

**Required**: Either verify P6, P7, P7a explicitly, or add a sentence citing ReachableStateInvariants (ASN-0047): since INSERT is a valid composite transition (established by the coupling constraint verification), ReachableStateInvariants guarantees P6, P7, P7a hold in the post-state.

### Issue 4: Coalescing claim contradicts I7 and I8

**ASN-0048, Correspondence runs under INSERT**: "the coalescing mechanism extends the existing run in place rather than creating a new one, keeping the run count at m"

**Problem**: I7(d) states that the freshly inserted content "always forms a single correspondence run of width w" — a distinct new run present in every post-INSERT decomposition. I8 gives a lower bound of m + 1 (no split) or m + 2 (with split). The claim of m runs contradicts both.

Coalescing IS possible when two conditions hold simultaneously: (1) the insertion point is at a run boundary (V-position adjacency), AND (2) the new run's I-start `a₁` equals the left neighbor's I-end + 1 (I-address contiguity). Condition (2) requires no intervening allocations under d's prefix since that neighbor's content was allocated — the sequential-typing scenario. The ASN presents coalescing as requiring only condition (1), omitting the I-address contiguity requirement entirely.

Additionally, I7 says "the post-state run decomposition is" with a definite article implying uniqueness. But S8 (ASN-0036) guarantees existence of a decomposition, not uniqueness. A coalesced decomposition is equally valid. If I7 describes one particular decomposition, it should say so.

**Required**: Either (a) remove the coalescing paragraph — it describes an implementation optimization, not a specification property, and its informal presentation contradicts the preceding formal analysis — or (b) reconcile it with I7/I8: state that I7 gives the canonical non-coalesced decomposition, that adjacent runs may be merged when their I-addresses are contiguous, that this contiguity requires no intervening allocations (not merely V-position adjacency), and adjust the definite article in I7 accordingly.

## OUT_OF_SCOPE

### Topic 1: INSERT into the link subspace
The ASN confines the V-shift to the text subspace (s ≥ 1). Inserting link structure (s = 0) requires the link ontology to be formalized first. I5 correctly establishes the subspace boundary.
**Why out of scope**: Links are not yet specified. This is new territory, not a gap in the current ASN.

### Topic 2: Run minimality guarantees
Whether a conforming implementation must maintain a maximally coalesced (minimal) run decomposition is left open. S8 requires only existence of some valid decomposition.
**Why out of scope**: This is an implementation constraint question already flagged in the Open Questions, not a state-transition invariant.

VERDICT: REVISE
