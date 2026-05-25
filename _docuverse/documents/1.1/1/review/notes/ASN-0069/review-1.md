# Review of ASN-0069

## REVISE

### Issue 1: V8c and V8 prose cite ASN-0068
**ASN-0069, V8c**: "compareversions(d_src, ⟨...⟩, d_new, ⟨...⟩) returns the same maximal runs as compareversions(d_new, ⟨...⟩, d_src, ⟨...⟩) modulo coordinate swap (CV-SYM of ASN-0068)"
**ASN-0069, §Arrangement Layer (V8 prose)**: "ASN-0068's compareversions operation reads this equality and returns the set of maximal correspondence runs"
**Problem**: ASN-0068 is not in the foundations list. Standard #7 forbids cross-ASN references except to foundations.
**Required**: Either drop the CV-SYM citation and state the symmetry independently (it follows from set equality of V-position pairs), or remove these references entirely.

### Issue 2: V1 derivation misidentifies the producing allocator
**ASN-0069, V1 derivation**: "By T10a.6 (DomainDisjointness, ASN-0034), the document sub-allocator of parent(d_src)'s account has a domain disjoint from every other allocator's domain. inc(d_src, 1) operates within this allocator's reach"
**Problem**: `inc(d_src, 1)` is not produced by `A_doc(parent(d_src))` — that allocator produces top-level documents under an account (first emission `inc(A, 2)`, then siblings by `inc(prev_doc, 0)`). The output `inc(d_src, 1)` is the first emission of the **version sub-allocator** `A_v(d_src)`, which is associated with `d_src` itself, not with `parent(d_src)`.
**Required**: Cite `A_v(d_src)` (defined in ASN-0047's Allocator hierarchy) as the producing allocator. The T10a.6 disjointness argument still applies, just to a different allocator.

### Issue 3: V1 derivation cites NodeUniqueAllocation for a document
**ASN-0069, V1 derivation (via ValidComposite verification at end)**: "By NodeUniqueAllocation and T10a's allocator discipline applied to the version sub-allocator of d_src (SubAllocatorAxiom), d_new ∉ E"
**Problem**: NodeUniqueAllocation (ASN-0047) is specifically about K.δ events with `IsNode(e)` — it guarantees freshness, bootstrap lineage, and registry tracking *for nodes*. `d_new` has `IsDocument(d_new)` (by KDeltaZerosK01 preserving `zeros = 2`), not `IsNode`, so NodeUniqueAllocation does not directly apply. Furthermore, SubAllocatorAxiom in ASN-0047 covers only `A_C` and `A_L`, not `A_v`.
**Required**: For document freshness, cite T10a's general allocator discipline applied to `A_v(d_src)`, and reference the Allocator hierarchy definition (not SubAllocatorAxiom) for `A_v`'s structure.

### Issue 4: V9 derivation uses J1, not J1★
**ASN-0069, V9 derivation**: "By J1 applied to the composite Σ →* Σ', every a ∈ ran(M'(d_new)) \ ran(M(d_new)) must have (a, d_new) ∈ R'"
**Problem**: ASN-0047 establishes that J1★ "supersedes J1 in the extended state" and that ValidComposite★ uses `J0, J1★, J1'★`. Since this ASN's V0 explicitly builds on the extended state (K.μ⁺_L compatible framework), J1★ is the operative coupling, not J1. The ValidComposite verification at the end correctly uses J1★ — V9 should be consistent.
**Required**: Change "By J1" to "By J1★" in V9's derivation. The substantive conclusion is the same (since all inherited mappings are content-subspace), but the citation should match the extended-state framework.

### Issue 5: V4 strengthens J4 without acknowledging the extension
**ASN-0069, V4**: Claims literal V-position inheritance: `(A v ∈ V_{s_C}(d_src) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_src)(v))`
**Problem**: J4 of ASN-0047 only constrains the *range*: `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})`. An implementation could satisfy J4 with partial domain coverage, rebased V-positions, or rearranged V→I correspondences. V4 commits to full literal inheritance — a strict strengthening of J4. The prose justifies this design choice but does not flag that V4 *extends* what J4 admits. The downstream verification (D-CTG★ preservation, V8 correspondence) relies on V4's full-inheritance commitment, not on J4 alone.
**Required**: Explicitly note that V4 strengthens J4's range-subset constraint to literal domain and mapping inheritance. State that this is a design commitment of this ASN, not derivable from J4 alone.

### Issue 6: V7 admits two distinct behaviors
**ASN-0069, V7**: "A fork of d_src with V_{s_C}(d_src) = ∅ may either fail (rejecting the operation) or reduce to K.δ alone... Both are consistent with V1–V6 and with the foundation invariants of ASN-0047"
**Problem**: Admitting non-determinism in a normative specification creates inter-implementation incompatibility. A user invoking CREATENEWVERSION on an empty source cannot rely on either behavior. The downstream property V11 (transitive identity through fork chains) breaks unpredictably: a fork-of-an-empty-fork might or might not exist depending on which path each implementation takes.
**Required**: Pick one behavior as normative, with rationale for the other being inadmissible. Or, if both must be admitted, name the choice as an implementation parameter and derive which downstream properties depend on it.

### Issue 7: V11a prefix transitivity derivation is informal
**ASN-0069, V11a derivation**: "Prefix is transitive: for any a, b, c ∈ T, a ≼ b ∧ b ≼ c ⟹ a ≼ c (this follows from agreement of components carrying through)"
**Problem**: Prefix (ASN-0034) defines `≼` but does not list transitivity as a postcondition. The argument "agreement of components carrying through" sketches the proof but doesn't cite the foundational steps (T0 transitivity of `≤` on ℕ for length, plus the component-agreement chain).
**Required**: Either derive Prefix transitivity from its definition with the foundation citations (T0's `≤` transitivity, plus component-equality transitivity), or note that this is a derived foundation fact and explicitly construct it in three lines.

### Issue 8: V8 implicit state for V_{s_C}(d_src)
**ASN-0069, V8**: "For every V-position v ∈ V_{s_C}(d_src) in the post-fork state, v ∈ dom(M'(d_new)) and M'(d_src)(v) = M'(d_new)(v)"
**Problem**: `V_{s_C}(d_src)` is state-dependent. The phrasing "in the post-fork state" is ambiguous — does it modify `V_{s_C}(d_src)` (post-fork content positions of source) or just establish the temporal frame for the conclusion? V5 makes pre- and post-fork `M(d_src)` equal, so they agree, but the ASN should be explicit.
**Required**: Clarify whether `V_{s_C}(d_src)` denotes pre-fork or post-fork content positions of `d_src` (V5 ensures they're equal, but the reader needs to know which state is the reference).

### Issue 9: V10(a) cites SubAllocatorAxiom for A_v
**ASN-0069, V10(a) derivation**: "By T10a's allocator discipline and SubAllocatorAxiom (ASN-0047), the version sub-allocator A_v(d_src) of d_src activates upon d_src's creation"
**Problem**: SubAllocatorAxiom in ASN-0047 (ContentLinkSubAllocatorExistence) explicitly axiomatizes `A_C` and `A_L`. The version sub-allocator `A_v` is defined in the Allocator hierarchy but not in SubAllocatorAxiom.
**Required**: Cite the Allocator hierarchy definition (ASN-0047) rather than SubAllocatorAxiom for `A_v`'s existence and activation.

## OUT_OF_SCOPE

(none — the ASN stays within the FORK operation's specification and does not encroach on excluded topics.)

VERDICT: REVISE
