# Review of ASN-0100

I verified the operation contract, all three effects (allocation, placement, shift), every per-state invariant in ASN-0047's `ExtendedReachableStateInvariants`, the composite-boundary couplings (J0, J1★, J1'★), P3, and P4★/P4a/P7a, plus the worked examples and both wp analyses.

## REVISE

(none)

The proof obligations are discharged to the standard required:

- **Edge cases covered.** Beginning (`j=0`), append (`j=N`, K.μ⁻ omitted), interior, empty-document first insertion (`ValidFirstInsertionPosition` with caller-chosen `m`), and the non-obvious empty-arrangement-but-nonempty-allocator-chain sub-case are all handled explicitly, with correct K.μ⁻ case routing (i.a / i.b / ii) distinguishing forced omission from canonical-decomposition choice.
- **Hard invariants shown, not waved.** S2 functionality rests on an explicit pairwise-disjointness argument (component arithmetic + TS2 source uniqueness) closed by INS.M-exhaustive. S8★ correctly uses C1a (restriction decomposition) rather than M2 — and the ASN itself flags that M2's S3 precondition fails for the whole extended-state arrangement when `V_{s_L}(d') ≠ ∅`, falling back to per-subspace S3★. The Insertion-run collapse is justified through M7 adjacency via INS.chain-shift (`inc(·,0)=shift(·,1)` from T4-validity ⟹ `sig=#`), not asserted.
- **D-CTG★ closed-interval form** is discharged over the full depth-`m_C` slice including off-prefix tuples (via D-CTG-depth), with the `m_C=2` degenerate case noted.
- **Foundation lemma reuse is disciplined.** I3 (ASN-0082) is cited only for its shift clause and affirmative companion lemmas; I3-V/I3-CS/I3-CX/I3-C are explicitly disclaimed as belonging to a shift-only model whose post-state is properly contained in INSERT's. I3-S7 is correctly *not* cited (its justification rests on the I3-C content frame INSERT breaks).
- **wp analyses are non-trivial** (tight-endset discoverability collapses to pre-state discoverability; P4★ for a fixed address resolves to a decidable chain-membership predicate). Concrete example verifies the region partition, projection-shift correspondence, J0/J1★/J1'★ discharge, and a non-tight alternative.
- **Atomicity** correctly separates SequentialTransitionAxiom's elementary-level guarantee from the required composite-level precondition, and the long K.ρ/K.μ⁺ reordering discussion self-corrects a prior unsound "reorder R away" argument.

Minor presentational note (non-blocking): the table entry INS.M-shift "discharged by I3" is shorthand — the shift-image *equality* holds by INSERT's own K.μ⁺ construction, with I3's companion lemmas supplying only the invariant-preservation half. The body already makes this distinction precisely, so no change is required.

## OUT_OF_SCOPE

The "INSERT vs. COPY" section and the version-chain corollary (INS.identity.version) touch deferred topics, but each is used only to characterize INSERT's identity-by-allocation property and explicitly disclaims specifying COPY or version creation. No scope violation.

VERDICT: CONVERGED
