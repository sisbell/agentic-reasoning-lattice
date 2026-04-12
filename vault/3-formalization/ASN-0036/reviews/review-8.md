# Formalize — ASN-0036 / S7

*2026-04-12 14:34*

- `MISSING_PRECONDITION: GlobalUniqueness (ASN-0034) — explicitly invoked in the "Uniqueness across documents" subproof ("GlobalUniqueness (ASN-0034) guarantees their document-level tumblers are distinct") and in the introductory paragraph. Postcondition (c) cannot be established without it.`
- `MISSING_PRECONDITION: S4 (origin-based identity) — explicitly invoked in the "Permanence" subproof ("By S4 (origin-based identity), distinct allocation events produce distinct addresses, so the address a itself is never reassigned or reused"). Required for postcondition (d).`
- `MISSING_PRECONDITION: T3 (CanonicalRepresentation, ASN-0034) — invoked in "Uniqueness across documents" to establish that document-tumbler distinctness is decidable by component-wise comparison. Required for the operational force of postcondition (c).`
