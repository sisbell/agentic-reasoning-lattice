# Channel Assignment — ASN-0043 review-170

**Date:** 2026-05-31 02:45

## Issue 1: L12 carries a forward-reference / downstream-consumer note that does not advance the immutability claim
Reason: The fix is pure deletion of a forward-referencing aside; what to remove and why is fully specified by the ASN's own structure (L12's two-part claim, L13 as the proper home). No design-intent or implementation evidence is needed.

## Issue 2: L9 and L11b assert "Σ′ extending Σ" but never discharge its conjuncts
Reason: StateExtension's three conjuncts are defined within this ASN, and the construction data (`Σ'.C = Σ.C`, `Σ'.M = Σ.M`, `Σ'.L = Σ.L ∪ {fresh ↦ …}`) is already present in both proofs; the discharge is mechanical from definitions. No external channel needed.
