# Review of ASN-0101

## REVISE

### Issue 1: D8's enumeration of preserved foundation invariants is incomplete

**ASN-0101, D8 Group (ii) and Group (iii)**: The Group (ii) list is "S4, S7a, S7b, S7c, S7d, L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, C-fin, NodeLineage (ASN-0036, ASN-0043, ASN-0093)". The Group (iii) list is "P0, P1, P2, P3, P4★, P4a, P6, P7, P7a, P8, L12a, L12b".

**Problem**: ASN-0093 defines foundation invariants not enumerated here: M0 (DocumentTumblerWellFormed) and C1, C1b, C1c, C2 belong in Group (ii) (per-state predicates over dom(M) or dom(C)); M1 (ArrangementMonotonicity) and C0 (ContentImmutability) belong in Group (iii) (transition predicates). The Group descriptions ("every clause of every invariant in this group", "the foundation invariants") read as exhaustive. Omitting these creates a gap between what is claimed preserved and what is explicitly enumerated.

**Required**: Add the missing invariants to the appropriate group, or scope the enumeration claim ("the foundation invariants listed").

### Issue 2: Worked example omits the link-subspace deletion case

**ASN-0101, A worked example**: "an analogous worked example with `S = s_L = 2` (depth typically `m_S = 2`) follows the same pattern, with I-addresses in `dom(L)` rather than `dom(C)` and with the link-subspace-specific invariants CL-OWN and CL-UNIQ being inherited rather than re-established."

**Problem**: The worked example exercises content-subspace deletion. CL-OWN and CL-UNIQ preservation is argued in D8 by source correspondence, but is not exercised concretely. A link-subspace example would non-trivially verify (i) that the post-state link-subspace I-addresses at positions in Q remain home-document allocated, (ii) that the link-subspace restriction remains injective after the shift bijects R onto Q, and (iii) D9's third bullet under the dom(L) clause of S3★. The current text gestures at the parallel without instantiating it.

**Required**: Provide a concrete link-subspace DEL example with at least three pre-state link-subspace V-positions and a non-trivial deletion (interior or partial-suffix), verifying CL-OWN, CL-UNIQ, and D9's link-store projection at the post-state.

### Issue 3: Composite-substitute argument misses the structural impossibility for link-subspace deletions

**ASN-0101, The operation**: "K.μ~ (ASN-0047) requires `|dom_C(M(d))| ≥ 2` as a formal precondition. When DEL operates on a content subspace with `n_S = 1`..."

**Problem**: ASN-0047 defines K.μ~ over content subspace only (its precondition is `|dom_C(M(d))| ≥ 2`, not `|dom_S(M(d))| ≥ 2`). For every link-subspace interior deletion, the K.μ⁻ + K.μ~ composite is structurally unconstructable — no K.μ~_L exists — independent of any cardinality or admissibility condition. The argument names content-subspace edge cases where the composite fails but does not acknowledge this stronger structural fact about link-subspace cases. The observability argument suffices on its own, but the non-availability argument as stated understates its own scope.

**Required**: Add a clause noting that K.μ~ is content-subspace only, so link-subspace interior deletions cannot be expressed by any K.μ⁻ + K.μ~ composite over the existing vocabulary — independent of the observability argument.

### Issue 4: Notation overload between L (left region) and L (link store)

**ASN-0101, throughout**: D0 defines `L := {v ∈ V_S(d) : v < s}` (the left region of V-positions). The state component `Σ.L : T ⇀ Link` (link store) is also denoted `L`. D8's S3★ argument uses both within the same paragraph ("positions in `L` inherit depth `m_S`" and "M(d)(u) ∈ dom(L)").

**Problem**: Disambiguation is left to the reader. While context usually suffices, the argument that S3★ is preserved (which involves `M(d)(u) ∈ dom(L)` where `u` is in the left region) requires the reader to track two distinct meanings of `L` in adjacent clauses.

**Required**: Rename the left/right region symbols (e.g., `V_L`, `V_R` or `Λ`, `Ρ`) to avoid collision with the link-store symbol from the foundations.

## OUT_OF_SCOPE

None. The ASN respects the scope statement — it does not address INSERT, COPY, REARRANGE mechanics, link semantics, version creation, or BEBE.

VERDICT: REVISE
