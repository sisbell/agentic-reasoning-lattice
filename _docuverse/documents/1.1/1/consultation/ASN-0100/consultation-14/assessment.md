# Channel Assignment — ASN-0100 review-14

**Date:** 2026-05-27 16:32

```
## Issue 1: P6 (ExistentialCoherence) not explicitly verified
Reason: The fix is fully specified by the review itself — a one-line discharge using INSERT's existing precondition `d ∈ dom(M)` and the already-established INS.frame.E. The invariant P6 is defined in cited ASN-0047 and requires no design or implementation input.
```

```
## Issue 2: P7 (ProvenanceGrounding) not explicitly verified
Reason: Discharge follows from forced ordering K.α before K.ρ (already established in §Atomicity) plus P0 inheritance (already established under §Permanence). Pure internal bookkeeping against existing ASN-0047 invariant and existing proof structure.
```

```
## Issue 3: TS2 invocation depends implicitly on S8-depth
Reason: Pure citation addition — both TS2 (ASN-0034) and S8-depth (ASN-0036) are already cited elsewhere in this ASN, and the equal-depth precondition is supplied unambiguously by pre-state S8-depth on V_{s_C}(d). No external input required.
```

```
## Issue 4: INS.M-exhaustive verification for K.μ⁻-omitted cases is implicit
Reason: The substrate decomposition section already enumerates cases i.a, i.b, ii where K.μ⁻ is omitted; the fix rewords the exhaustiveness justification to cover those cases using the already-stated K.μ⁺ amendment and frame reasoning.
```

```
## Issue 5: §Coverage and link discoverability — subspace closure of shift map
Reason: OrdAddHom (b clause, ASN-0036) is already cited in this ASN for subspace preservation of shift (see §Effect Two). Adding the same citation in the projection derivation is mechanical and derivable from existing references.
```

```
## Issue 6: Atomicity discussion of K.ρ commutativity needs J1★ caveat
Reason: The composite-boundary vs per-state distinction is already developed throughout §Atomicity and Canonical Order; the fix is a single clarifying sentence consistent with the existing two-level atomicity framework. Internal exposition adjustment only.
```

```
## Issue 7: Empty-case worked example handles only sub-case (i.a)
Reason: Case (i.b) is already fully analysed in the substrate decomposition section, including why K.μ⁻ omission is the canonical-decomposition choice. The fix either extends the worked example mechanically from existing case (i.b) analysis or notes conceptual identity — both internal.
```

```
## Issue 8: §Sequential text-subspace structure empty-case derivation needs OrdinalShiftBase citation for k=0
Reason: OrdinalShiftBase (ASN-0058) is already cited multiple times in this ASN for the shift(t, 0) = t convention; adding the citation at the k=0 step in the empty-case derivation is a pure consistency fix against an already-established reference.
```
