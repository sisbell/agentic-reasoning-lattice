# Review of ASN-0091

## REVISE

(no items)

## OUT_OF_SCOPE

(none — the ASN's "Open Questions" section properly defers link-subspace rearrangement semantics, transclusion-split guarantees, observational equivalence, run-cardinality bounds, and the inverse question of bijection realisability to future ASNs)

The ASN demonstrates substantial rigor:

- **Abstract/concrete separation** is clean: RA-reg through RA-adm define the Vstream-only class, with REARRANGE_K (via ASN-0047's K.μ~) discharged clause-by-clause.
- **Subspace preservation** is given a careful two-stage proof (RE-subpres), with the binary constraint (Stage 1 via S3★-aux) and cross-direction exclusions (Stage 2 via S3★ + L14) explicitly worked.
- **All foundation invariants** are discharged per-invariant: ASN-0036 (S0/S1/S2/S4/S5/S7a-d/S8a/S8-fin/S8-depth/S9), ASN-0047 extended (D-CTG★/D-MIN★/D-SEQ★/S3★/S3★-aux/CL-OWN/CL-UNIQ/P4★/S8★), ASN-0093 substrate (M0/M1), state-component invariants by RA-frame inheritance, and P4a by the SequentialTransitionAxiom history-fixity argument.
- **Four worked examples** verify claims concretely: 3-cut pivot, 4-cut swap, interior cuts exercising R-EXT, and bijection non-uniqueness under shared I-addresses (S5). Each trace verifies S2, S8a, S8-depth, S3★, D-CTG★/D-MIN★/D-SEQ★, S3★-aux, CL-OWN, CL-UNIQ, P4★, S8★ concretely against the post-state arrangement.
- **Run-cardinality witnesses** (RE-frag, RE-coal, RE-eq) are constructively exhibited with explicit chain-disjoint-adjacency reasoning (inline lemma rigorously argued from TA5(c) + T3 + T10a.6).
- **Multi-step composition** is properly conditioned: RE-trans★'s (iii) requires no step targets origin(a); RE-other★ requires no step targets d'; RE-ext★ requires v in the in-S exterior of every targeting step.
- **The two-step (+, −) trace** explicitly demonstrates the spatial-partitioning construction with verified cardinality counts at each step (4→5→4).
- **Boundary cases** are addressed: empty domain (vacuous), identity π (Σ' = Σ), shared I-addresses (witness non-uniqueness with two distinct π demonstrated), interior cuts (R-EXT exercised), cut beyond V_S(d)'s extent (c_{n−1} = [1,7] outside V_S(d) handled correctly).
- **The bijection-class characterisation** correctly identifies π's freedom under shared I-addresses, with four sub-inferences (mapping-into, restriction-injective, restriction-surjective, equicardinality) jointly establishing the per-block bijection condition.
- **Foundation citations** are confined to listed foundation ASNs (0034, 0036, 0047, 0053, 0058, 0084, 0093, 0098). No cross-references to non-foundation ASNs.
- **OrdinalShiftBase convention** (`t + 0 = t`, `t + k = shift(t, k)` for k ≥ 1) is properly inherited from ASN-0058.

The ASN's prose is tight, the proofs chain explicitly, and no hand-waves disguise gaps. The depth standard is met: every postcondition has derived consequences, every claim has a proof, and concrete examples verify the key claims against actual state values.

VERDICT: CONVERGED
