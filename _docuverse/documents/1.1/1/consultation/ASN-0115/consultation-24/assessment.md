# Channel Assignment — ASN-0115 review-24

**Date:** 2026-06-09 22:05

## Issue 1: R8's boxed claim has absorbed its own proof
Reason: Pure reorganization within the ASN — the obligation statement and the subspace-dispatch/CL-OWN/CL-UNIQ derivation are both already present in the box; the fix relocates the proof into the following prose to match the R1–R5 convention this ASN establishes. No design intent or implementation evidence is at stake.

## Issue 2: R7's repeatability proof mis-cites immutability for link items
Reason: The correction is derivable from the ASN's own `item` definition (link positions deliver `⟨ref, a⟩`, carrying the address, never `Σ.L(a)`) and the proof's already-established address-agreement step; recognizing that L12/`Σ.L(a)` target a value the item never delivers requires only internal content.

## Issue 3: Standing-precondition paragraph carries a use-site inventory and a why-justification
Reason: Pure anti-bloat trim — dropping the R0–R11 use-site enumeration and the "load-bearing / may fail otherwise" justification to leave the bare scoping statement; nothing about design intent or implementation behavior is involved.
