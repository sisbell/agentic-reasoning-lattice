# Review of ASN-0100

I read the full specification and checked each proof obligation against the foundation contracts. This ASN has clearly been through many revision cycles, and it shows: the hard cases that usually get hand-waved are all addressed explicitly.

## Verification performed

**Boundary cases — all covered.**
- *Position 0* (`j=0`): Left empty, full shift; K.μ⁻ shrinks `V_{s_C}` to ∅, K.μ⁺ rebuilds. ✓
- *Append* (`j=N`, `p_m=N+1`): Shifted-right empty, K.μ⁻ omitted. The ASN correctly notes `p` falls *outside* `V_{s_C}(d)` here and appeals to `ValidInsertionPosition` postcondition (b) directly rather than the set-membership form — a subtlety that would trip a careless proof. ✓
- *Empty document* (`ValidFirstInsertionPosition`): handled with the distinct ternary predicate, caller-chosen depth, K.μ⁻ omitted; the empty-arrangement vs. fresh-allocator-state sub-cases are separated correctly. ✓
- *`n=0`*: excluded by precondition. ✓

**The freshness argument** is sound and properly subtle: each `a_k`'s freshness is discharged against the intermediate state `Σ_k` (not the operation pre-state), with the `∉dom(C)` clause via ChainEnumerationInjectivity and the `∉dom(L)` clause via subspace separation (L0 + SC-NEQ). The boundary case `m_d=0` correctly routes to FirstEmissionFreshness.

**INS.chain-shift** is proved, not asserted: `inc(·,0)=shift(·,1)` is grounded in T4-validity → TA5-SigValid (`sig=#`) → TA5, iterated under TA5a + ChainUniformLength, composed by TS3. This is exactly the I-adjacency that M7 demands for the S8★ block collapse, and the merge is discharged rigorously.

**S2 functionality** — the pairwise disjointness of Left/Insertion/Shifted-right is verified by explicit component arithmetic (split correctly at `k=0` via OrdinalShiftBase vs. `k≥1` via TumblerAdd), with Shifted-right source uniqueness from TS2, and closure guaranteed by INS.M-exhaustive (no circularity: exhaustiveness is derived from the decomposition, not from S2).

**Tiling without gaps** (D-CTG★/D-MIN★/D-SEQ★) — the hardest invariant — is verified by showing the last-component values form the contiguous range `{1,…,N+n}`.

**All ~28 Class (a) per-state invariants** are addressed, grouped by the state component they range over, with the genuinely non-trivial ones (S4, L0's content clause, P6, P7) discharged against the *changed* `dom(C)` rather than dismissed by frame. The composite-boundary couplings J0/J1★/J1'★ and Class (b) properties are correctly delegated to the boundary.

**Depth requirements met:** worked examples (interior, append, empty) verify the regions and the projection trace concretely; wp analysis is computed for two genuinely non-trivial postconditions (tight-endset discoverability collapsing to the pre-state; P4★ for a specific address); the INS.identity corollaries are explicitly derived.

**Sophisticated points checked and found sound:**
- The K.ρ-after-K.μ⁺ ordering argument (keeping `R` self-consistent at every intermediate so the atomicity scope stays precisely two-fold, even though `R` is unprotected) holds against interleaving R-touching composites.
- The case-(ii) "canonical-decomposition choice vs. forced omission" distinction for K.μ⁻ is correct (`N≥1` makes the alternative shrink-`s_C` decomposition admissible).
- The disclaiming of ASN-0082's I3-V/I3-CS/I3-CX is justified — those characterize a shift-only post-state strictly contained in INSERT's, and the conflict at coinciding Insertion positions is identified precisely.

**Cross-ASN references:** every cited ASN (0034, 0036, 0047, 0053, 0058, 0082, 0093, 0098) is a listed foundation. No non-foundation references. The OrdinalShiftBase `shift(t,0):=t` convention is grounded in the foundation, not reinvented.

**Scope:** COPY/DELETE/REARRANGE/link-subspace/version creation are properly bounded out; INS.identity.version states an INSERT consequence without specifying version-creation mechanics.

## REVISE

None. After extensive scrutiny of the proofs, boundary cases, invariant coverage, and the atomicity/projection arguments, I found no claim stated without adequate derivation, no skipped case, and no invariant conjunct left unaddressed.

## OUT_OF_SCOPE

The ASN's own Open Questions and Scope sections correctly defer link-subspace insertion, INSERT self-composition closure, concurrent-INSERT serialization, and partial-failure recovery to future work. These are appropriately scoped, not gaps in this ASN.

VERDICT: CONVERGED
