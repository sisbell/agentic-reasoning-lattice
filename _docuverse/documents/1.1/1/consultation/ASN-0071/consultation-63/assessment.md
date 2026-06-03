# Channel Assignment — ASN-0071 review-63

**Date:** 2026-06-03 11:39

## Issue 1: The central multi-vspec union is never exercised by a concrete example
Reason: Internal. Adding a two-source worked query that exercises the union and cross-source dedup is a mechanical application of the existing `iaddrs`/`find` definitions against the already-constructed state — no design intent or implementation evidence is needed.

## Issue 2: Imprecise characterization of the relaxation of ASN-0058's ContentReference
Reason: Internal. Correcting which ContentReference conjuncts are kept, strengthened, retained, or dropped is a comparison against ASN-0058's and ASN-0053's definitions already cited in this ASN; the facts are fully determined by those texts.

## Issue 3: Unproven coincidence claim with `resolve`
Reason: Internal. Whether to derive or delete the `resolve` coincidence rests on ASN-0058's `resolve`/decomposition definitions and this ASN's `iaddrs_one`; the one-line coverage argument (or its removal) is derivable from definitions already in scope.

## Issue 4 (anti-bloat): Subspace confinement stated twice
Reason: Internal. Replacing the re-derivation in *Resolution* with a citation of the corollary proven in *The query* is a purely editorial dedup within this ASN.
