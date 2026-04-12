# Formalize — ASN-0036 / S7

*2026-04-12 15:46*

- `MISSING_PRECONDITION: GlobalUniqueness (ASN-0034)` — The Uniqueness section of the proof directly invokes GlobalUniqueness to establish postcondition (c): "for documents d₁ ≠ d₂ created by distinct allocation events, GlobalUniqueness (ASN-0034) guarantees their document-level tumblers are distinct." This is the load-bearing premise for (c), yet it appears nowhere in the contract's precondition list.

- `MISSING_PRECONDITION: S4 (origin-based identity)` — The Permanence step explicitly invokes S4: "By S4 (origin-based identity), distinct allocation events produce distinct addresses, so the address `a` itself is never reassigned or reused." This is required to close the invariant argument (that attribution cannot be severed because the address is never reassigned). S4 is absent from the contract's precondition list.

- `MISSING_PRECONDITION: T3 (CanonicalRepresentation, ASN-0034)` — The Uniqueness step invokes T3: "By T3 (CanonicalRepresentation, ASN-0034), this distinctness is decidable by component-wise comparison." T3 is required to operationalize the uniqueness claim — without it the proof cannot assert that origin discrimination is unambiguous. It is absent from the contract's precondition list.
