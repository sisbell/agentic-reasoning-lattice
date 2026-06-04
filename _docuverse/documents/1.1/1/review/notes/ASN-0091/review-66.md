# Review of ASN-0091

This note carries the `review-mode.anti-bloat` classifier. I find one substantive proof gap and several accreted-prose / over-derivation patterns.

## REVISE

### Issue 1: "K.μ~ is a valid composite" omits the coupling constraints

**ASN-0091, "Clause Correspondences and Per-Invariant Discharges" (reachability discharge)**: "In the non-trivial case, K.μ~'s admissibility clauses (i)–(v) are closed above, so K.μ~ is a valid composite; its K.μ⁻ + K.μ⁺ elementary decomposition (ASN-0047) is then a finite sequence of elementary transitions drawn from a valid composite."

**Problem**: ValidComposite★ (ASN-0047) has two clauses: (1) intra-composite sequencing — which the admissibility conditions (i)–(v) feed — and (2) the *coupling constraints* J0, J1★, J1'★ evaluated initial-to-final. The discharge establishes only (i)–(v) and leaps directly to "valid composite." Clause (2) is never addressed. Reachability of Σ' rests entirely on K.μ~ being a *valid* composite, so the omission undermines the whole reachability route (and with it the discharge of S3★, S3★-aux, CL-OWN, CL-UNIQ, S8★, P4★, P4a, P7a).

**Required**: Discharge clause (2) explicitly — J3 (ReorderingIsolation, ASN-0047) gives `C'=C ∧ L'=L ∧ E'=E ∧ R'=R` and renders J1★ vacuous for K.μ~; cite it (or the constraints directly) so "valid composite" is earned, not asserted from admissibility alone.

### Issue 2: The RA-adm discharge is a three-layer derivation where one layer suffices

**ASN-0091, "Clause Correspondences and Per-Invariant Discharges"**: the discharge splits RA-adm into a "shape package (constructive, from RA-dom)" layer, an "arrangement-dependent invariants (via reachability … + ExtendedReachableStateInvariants)" layer, and the "State-Component-Only Invariants" frame-inheritance layer.

**Problem**: RA-adm is defined as exactly the *per-state foundation invariants*. ExtendedReachableStateInvariants (ASN-0047) delivers that entire per-state list — S2, S8a, S8-fin, S8-depth, S8★, D-CTG★, D-MIN★, D-SEQ★, S4, S7a, S7b, S7d, P6, P7, P8, L0–L14, CL-OWN, CL-UNIQ — wholesale at any reachable state. Since the discharge already establishes Σ' reachable (unavoidably, for the arrangement-dependent invariants), the shape-package layer and the frame-inheritance treatment of the *per-state single-state predicates* (S4, S7a, S7b, S7d, M0, P6–P8, NodeLineage, ActivatedEmission, L0–L-fin, C1–C-fin) reproduce conclusions already in hand. The note even advertises the shape package as "depend[ing] only on RA-dom" as a virtue — but that independence buys nothing once reachability is required anyway. Only the *binary transition invariants* (S0, S1, M1, P0–P3, C0, L12 — not in the per-state list) genuinely need the separate transition-satisfaction argument.

**Required**: Discharge RA-adm in one step (Σ' reachable ⟹ ExtendedReachableStateInvariants), and confine the "State-Component-Only" section to the binary transition invariants that fall outside the per-state list. Remove the shape-package layer and the per-state-predicate frame-inheritance enumeration.

### Issue 3: Defensive prose about a rejected proof path

**ASN-0091, "Clause Correspondences and Per-Invariant Discharges"**: "We therefore do not appeal to a bare K.μ⁻ + K.μ⁺ pair — which would interpose a strictly contracted intermediate state whose elementary preconditions are not discharged — but to the empty composite, which returns Σ' = Σ directly."

**Problem**: This defends against an approach the note does not take. It explains why an alternative is wrong rather than advancing the argument — the reader who follows the empty-composite route does not need the rejected route narrated. This is the defensive-justification pattern the anti-bloat mandate targets.

**Required**: State the empty-composite realiser for the collapse case and stop; drop the contrast with the bare K.μ⁻+K.μ⁺ pair.

### Issue 4: Use-site inventory in the ChainDisjointAdjacency lemma

**ASN-0091, "Run Decomposition Is Not Invariant" (inline lemma, "Precondition fixing the successor identification")**: "This is the identification underlying every `a_{i+1} = a_i + 1` used in the run-decomposition witnesses below; it holds here precisely because the operands are chain elements, where `sig(·) = #·`."

**Problem**: The clause "This is the identification underlying every … used in the run-decomposition witnesses below" is a forward inventory of downstream consumers — it tells the reader where the fact will be reused rather than establishing the fact. The lemma's actual content (`x+1 = shift(x,1) = inc(x,0)` for T4-valid chain elements) stands without it.

**Required**: Delete the use-site pointer; keep only the identification itself.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
The note's Open Questions raise what invariants a link-subspace REARRANGE would preserve. CS3 hard-fixes the cut subspace to s_C, so this is genuinely future territory, not a gap here.

### Topic 2: Whether two fragments jointly reconstitute a transcluded source span
RE-trans correctly limits itself to per-fragment origin (RE-origin) and flags that joint reconstitution is "not established here." Belongs to a future bundle/transclusion ASN.

VERDICT: REVISE
