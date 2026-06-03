# Channel Assignment — ASN-0071 review-14

**Date:** 2026-06-02 22:56

## Issue 1: Malformed set-containment chain in the codomain argument
Reason: Purely a proof-formatting fix; the correct bounding chain `(dom(C) ∪ dom(L)) ∩ dom(C) = dom(C)` follows from S3★ and the subspace-confinement subset claim, both already established within the ASN. No external channel needed.

## Issue 2: find(Q)(Σ) is undefined when a queried source document is absent from Σ.E_doc
Reason: A definitional hygiene fix — naming the partial function's domain via the precondition `(A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)` or binding vspec's Σ to find's evaluation state. M1 and P1 are already cited in the ASN, so the remedy is internal.
