I need to trace where D0 and D1 (from ASN-0034) appear in ASN-0061 and verify the rebase was done correctly. Let me examine the document carefully.

**D0** (DisplacementWellDefined): `a < b`, divergence `k` satisfies `k ≤ #a` → `b ⊖ a` well-defined.

**D1** (DisplacementRoundTrip): `a < b`, `divergence(a,b) ≤ #a`, `#a ≤ #b` → `a ⊕ (b ⊖ a) = b`.

Searching for all subtraction and round-trip sites in ASN-0061:

- **D-SHIFT**: uses `ord(v) ⊖ w_ord`, justified by **TA2** (general subtraction well-definedness: `a ≥ w`)
- **D-SEP**: proves `(ord(p) ⊕ w_ord) ⊖ w_ord = ord(p)`, justified by **TA4** (PartialInverse)
- **D-BJ**: uses `ord(v₁) ⊖ w_ord < ord(v₂) ⊖ w_ord`, justified by **TA3-strict**
- **D-BLK consistency**: uses `(vₘ − c) + j = (vₘ + j) − c`, justified by natural number arithmetic at depth 1

None of these sites use D0 or D1. The subtractions are `a ⊖ w` (TA2 form), not displacements `b ⊖ a` (D0 form). The round-trip is `(a ⊕ w) ⊖ w = a` (TA4 form), not `a ⊕ (b ⊖ a) = b` (D1 form). D0 and D1 don't appear in the body text, and they don't appear in the Properties Introduced table. All proofs are self-contained with their current citations.

# Rebase Review of ASN-0061

## REVISE

(none)

VERDICT: CONVERGED
