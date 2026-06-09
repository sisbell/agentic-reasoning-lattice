# Review of ASN-0117

I checked the operation against its precondition, both composite realisations (R≠∅ and R=∅), every frame and coupling obligation, the wp derivation, and all six worked examples. The ASN discharges its claims by explicit citation to the foundation contraction (ASN-0082) and the transition model (ASN-0047), and verifies its key postconditions against concrete scenarios.

The hard cases are all covered:
- **Boundary completeness** — leading-span (J=1, emptying-then-refilling the subspace and re-pinning S8-depth), suffix-delete and delete-everything (R=∅, the lone-K.μ⁻ realisation via J2 self-sufficiency), within-document sharing (A_del^excl = ∅), and cross-document transclusion (P5 verified concretely) are each exercised by a distinct worked example.
- **The count-vs-label subtlety** in DEL-REMOVE is handled correctly: q_3 stays in the domain (reoccupied by the shifted survivor) while the top c labels leave — the per-pair-absence trap is explicitly avoided.
- **Composite validity** — clause 1 (intermediate K.μ⁻/K.μ⁺ preconditions) and clause 2 (J0/J1★/J1'★ between initial and final) are discharged, licensing the offload of the full per-state invariant package to ExtendedReachableStateInvariants rather than re-proving each conjunct. The reachability offload is sound because composite-validity is actually established, not assumed.
- **The wp quantifier structure** (per-link existential, not per-slot universal) is correctly justified, and the reverse inclusion D(d,Σ')⊆D(d,Σ) is handled via range-shrinkage plus no-new-links.

I found no hand-waves, no missing conjuncts, and no unproven "by similar reasoning" steps. The anti-bloat patterns (forward-reference deferrals, defensive axiom rationale, use-site inventories, duplicated paragraphs) are not present in problematic form — the discursive opening is house-style motivation establishing the non-destruction semantics, and the cross-references within the document are backward, not deferring forward.

## OUT_OF_SCOPE

### Topic 1: Text deletion at depths m > 2
The precondition fixes `m = #p = 2`, matching foundation ASN-0082's contraction, which only covers depth-2 text positions. Deletion at deeper text V-positions (which the arrangement model permits in principle, m ≥ 2) is uncovered.
**Why out of scope**: This is a foundation limitation inherited correctly, not an error — the ASN explicitly states the m=2 restriction in its precondition rather than hiding it, and ASN-0082 supplies no deeper-depth displacement to cite.

META: not applicable — the ASN defines state effect, an operation, and invariants stated abstractly enough that any non-destructive-edit implementation must satisfy them.

VERDICT: CONVERGED
