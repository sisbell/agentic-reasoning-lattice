# Review of ASN-0113

I checked the load-bearing proofs (W3, W4, W10, W11, W19, W20) and the three worked instances against the foundation contracts.

**W3 (well-formedness).** `actionPoint(δ(n_S, m_S)) = m_S ≤ #start_S = m_S` (OrdinalDisplacement); reach `= shift(start_S, n_S) = [S,1,…,1,1+n_S]` (OrdinalShift). Holds, including the `m_S = 2` collapse.

**W4 (exact coverage).** T5 applied with the common prefix `p = [S,1,…,1]` (length `m_S−1`, `≥ 1` since `m_S ≥ 2`) pins interior components; the half-open bounds pin the last component to `1..n_S`; D-SEQ★ identifies the result as `V_S(d)`. Completeness and exclusivity both discharged. The depth-3 instance correctly exercises the non-vacuous interior-confinement path that `m_S = 2` leaves trivial — `[S,2,1]` (admissible last component, divergent interior) is excluded by T1 at position 2, exactly as claimed.

**W10/W11 (confinement, disjointness).** The T1 first-divergence argument is correct for `t` of any depth, and SC-NEQ (`1 ≠ 2`) closes disjointness. Note W10 correctly claims only the forward implication (`t ∈ ⟦ext⟧ ⟹ t₁ = S`), which is what the disjointness step needs.

**W19 (cardinality wp).** The three preconditions partition allocated states by the emptiness-bit pair; the `d ∈ dom(M)` conjunct is load-bearing only in the `⟨⟩` case (and harmlessly redundant elsewhere). Both directions are justified, and the weakest-precondition obligation is genuinely argued, not asserted.

**W20 (faithful count).** The arranged-vs-homed distinction is handled with care: CL-OWN + CL-UNIQ give the bijection onto `ran(M(d)|_{s_L})`, and the note correctly declines to claim a standing coupling between homed and arranged links, citing the contraction case. The content side is faithful by S2/S3★ and correctly counts *positions* (not distinct I-addresses, respecting shared content).

**Boundaries.** Empty-both (`⟨⟩`, W0/W19), single-occupied-subspace (worked `d'`, W14 absent-member-reads-zero), and `m_S = 2` vs `m_S = 3` depth boundaries are all exercised. W-pre cleanly separates unallocated (failure) from allocated-empty (`⟨⟩`). Purity (W8) characterizes the read-set down to `dom(M(d))`.

**Anti-bloat scan.** The empty-allocated→`⟨⟩` distinction appears in both the W-pre paragraph and W0, and "one step beyond W4" recurs, but each occurrence sits in a distinct structural role (precondition vs result-type; claim body vs status table) and the repetition is light. The three worked instances are each independently justified by a boundary the others do not cover. No defensive justification, use-site inventory, axiom rationale, or relocated-finding prose found. The note reads as already cleaned.

No REVISE items. The Open Questions correctly hold out-of-scope topics (overall extent, version fork, transclusion) rather than asserting claims about them.

VERDICT: CONVERGED
