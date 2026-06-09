# Review of ASN-0116

The mathematics here is strong: the two-layer split is clean, the composite is exhibited step-by-step against the K-vocabulary with intermediate preconditions discharged, the contiguity/tiling argument is given directly (not hand-waved), the worked example checks the boundary cases (empty subspace, append, front-insertion), and P6 is a genuinely non-trivial weakest-precondition (containment, not emptiness). The block-disjointness reasoning and the "no block position is a shifted image" argument are both correct. The findings below are confined to redundancy/anti-bloat and a table omission, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: S8★ is re-derived after the post-state theorem already grants it
**ASN-0116, "Per-subspace run decomposition"**: "ExtendedReachableStateInvariants (ASN-0047) also demands S8★ ... This is automatic rather than an INSERT-specific obligation: M'(d) is finite (I3-fin) ... by S8 (CorrespondenceRunPartition, ASN-0036) ... S8★ for the whole post-state is inherited from S8 ... not re-proved."

**Problem**: The valid-composite section ends by licensing "the appeal to ExtendedReachableStateInvariants for its post-state," and that theorem lists S8★ among the per-state invariants. Unlike contiguity, S8a, S8-depth, finiteness, and content-side referential integrity — each of which is genuinely needed to discharge K.μ⁺'s clause-1 precondition and is correctly forward-referenced there — **S8★ is not a precondition of any composite step** (K.μ⁺'s precondition lists S8a/S8-depth/D-CTG/D-MIN/finiteness, not S8★). So S8★ is purely a post-state invariant already granted by the theorem; the explicit re-derivation via S8 adds nothing (the paragraph even says it is "automatic," then derives it, then says it is "not re-proved").

**Required**: Replace the derivation with one line: S8★ holds at the post-state by ExtendedReachableStateInvariants, INSERT being a valid composite. Keep only the P1↔run clarification if it carries weight.

### Issue 2: "mandatory, not optional" coupling-constraint prose stated twice
**ASN-0116, valid-composite section**: "a sequence that meets every transition precondition (clause 1) but violates a coupling constraint (clause 2) is *not* a valid composite — so the coupling constraints are mandatory, not optional, and we discharge them at the boundary below."
**ASN-0116, provenance section**: "... plus a composite-boundary coverage property — mandatory, not optional, by the composite-validity discipline established above (ValidComposite★ clause 2)."

**Problem**: ValidComposite★ clause 2 already states that coupling constraints must hold; the mandatoriness point is asserted in both sections, and the first instance restates the foundation's clause rather than the ASN's own content. This is the "new prose explaining why the axiom is needed" / cross-section repetition pattern.

**Required**: State the mandatoriness once (at the discharge site), and let the other location cite it without re-asserting.

### Issue 3: Claims table omits Effect/Frame clauses it elsewhere includes
**ASN-0116, "Claims Introduced"**: lists I-ALLOC, I-PROV, I-SHIFT, I-LEFT, I-NEW, I-DOM, F-SUB, F-DOC (mixing introduced and cited clauses).

**Problem**: I-IMM (an Effect clause, "cited (C0)"), F-LINK, and F-ENT (Frame clauses) appear in the Effect/Frame but are absent from the table, even though comparably-statused cited clauses (I-ALLOC, I-SHIFT) are listed. The inventory is inconsistent.

**Required**: Either add I-IMM/F-LINK/F-ENT for completeness, or state that the table excludes pure-frame clauses (and then drop I-ALLOC's "cited" siblings under the same rule).

## OUT_OF_SCOPE

### Topic 1: Transclusion at a shared insertion point, concurrent insertion, transclusion-provenance, post-edit fragmentation
**Why out of scope**: These are exactly the four Open Questions the ASN poses; they belong to COPY/transclusion (ASN-0118), concurrency, and later editing notes, not to native single-authority INSERT.

VERDICT: REVISE
