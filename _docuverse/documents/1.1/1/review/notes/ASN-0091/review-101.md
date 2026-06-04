# Review of ASN-0091

## REVISE

### Issue 1: Reachability-of-Σ′ derivation restated in two sections

**ASN-0091, "REARRANGE_K Realises the Abstract Class" (RA-adm discharge) and "Composite-Boundary Properties"**:

RA-adm discharge: "K.μ~ is therefore a valid composite, and its K.μ⁻ + K.μ⁺ elementary decomposition ... appended to any trace witnessing reachability of Σ yields a trace witnessing reachability of Σ'."

Composite-Boundary Properties: "Appending that composite to a trace of valid composites witnessing Σ yields a trace of valid composites whose final state is Σ', so ASN-0047's ExtendedReachableStateInvariants delivers P4★ ∧ P4a ∧ P7a at Σ'."

**Problem**: The "append the realising composite to a witnessing trace ⟹ Σ′ reachable" derivation is fully carried out in the RA-adm discharge, then re-derived verbatim-in-substance in the Composite-Boundary section. The second section already back-references the validity discharge ("valid by the clause (i)–(v) and J3 discharge of ... above"); only the reachability conclusion needs to be reused, not re-proven. This is the "two paragraphs say the same thing in different words" pattern the anti-bloat lens targets — the reader must recognise the repeated argument to confirm nothing new is being claimed.

**Required**: In the Composite-Boundary section, cite the reachability fact established in the RA-adm discharge rather than re-deriving the trace-appending step; keep only what is new there (that Σ′ is a *composite boundary*, hence P4★ ∧ P4a ∧ P7a apply). Compress to a single sentence.

## OUT_OF_SCOPE

### Topic 1: Reconstitution of source spans after fragmentation
The RE-trans discussion explicitly defers "whether the two fragments jointly reconstitute the original source span" — correctly listed under Open Questions, not asserted. No action needed; flagged only to confirm it is properly scoped out.

### Topic 2: Link-subspace rearrangement semantics
The ASN restricts cuts to the content subspace (CS3, S = s_C) and leaves link-subspace reordering to a future ASN (Open Questions). Appropriate.

Note on what was checked and found sound: the K.μ~ admissibility discharge (clauses i–v) correctly rests on domain-preservation for the shape package; RE-ran/RE-μ two-case derivations are valid; Lemma L-chain's `x+1 = inc(x,0)` chain-closure argument is sound under ChainElementT4Validity; the coalescence/equality/collapse witnesses all compute correctly (verified R-P1/R-P2 reassignments and run cardinalities); Worked Example 4's witness non-uniqueness and RE-proj uniformity are well-posed. The five worked examples each exercise a distinct mechanism (basic pivot, 4-cut μ-delta, non-empty in-S exterior, bijection non-uniqueness, net-effect collapse) and are not redundant.

VERDICT: REVISE
