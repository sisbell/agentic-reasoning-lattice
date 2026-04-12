# Formalize — ASN-0036 / S7

*2026-04-12 15:00*

`

- `MISSING_PRECONDITION: S4 (origin-based identity, ASN-0034)` — the proof's permanence section explicitly invokes S4: "By S4 (origin-based identity), distinct allocation events produce distinct addresses, so the address `a` itself is never reassigned or reused." S4 is a direct dependency of the invariant's no-reuse guarantee, but is absent from the contract's precondition list.

- `MISSING_PRECONDITION: T3 (CanonicalRepresentation, ASN-0034)` — the proof's uniqueness-across-documents section explicitly invokes T3: "By T3 (CanonicalRepresentation, ASN-0034), this distinctness is decidable by component-wise comparison." T3 is cited as a step in establishing postcondition (c); it does not appear in the contract preconditions.
