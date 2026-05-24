# Channel Assignment — ASN-0051 review-52

**Date:** 2026-05-16 06:34

```
## Issue 1: SV5 proof notation conflates state-dependent and state-independent readings of the endset
Reason: Fix is purely notational — the ASN already defines `π(e, d) = coverage(e) ∩ ran(M(d))` with `e` as a state-independent endset value, and L12 is already in the lattice and cited elsewhere in this ASN. Tightening the unfolding to either anchor a link address or drop the redundant state subscript is derivable from existing definitions.
```

```
## Issue 2: SV9 monotonicity proof's "L-frame transition" enumeration depends on L being implicitly framed in ASN-0047, but the cited frame conditions do not say so
Reason: Citation-routing fix internal to the lattice — L12 (LinkImmutability) and L12a (LinkStoreMonotonicity) in ASN-0043 are the proper sources for entry preservation and domain non-growth, both already cited elsewhere in this ASN. No design or implementation input required.
```

```
## Issue 3: SV11 attainment witness shows only the single-block case
Reason: Constructing a p ≥ 2 attainment witness (or characterising the topological obstruction) is a pure mathematical exercise over the ASN's own block-decomposition and span-coverage machinery — no design intent or udanax behaviour informs whether m · p is tight for p ≥ 2.
```

```
## Issue 4: SV6 informal statement omits the structural restriction k > p₃
Reason: Editorial alignment — the formal Precondition list and SV13(f) already carry the k > p₃ qualifier; updating the informal headline to match is internal to the ASN.
```
