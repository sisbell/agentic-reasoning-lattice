# ASN-0045 Formal Statements

*Source: ASN-0045-tumbler-fields.md (revised 2026-03-17) — Index: 2026-03-18 — Extracted: 2026-03-18*

## E.node — IsNode (INV, predicate(Tumbler))

ValidAddress(t) ∧ zeros(t) = 0

## E.account — IsAccount (INV, predicate(Tumbler))

ValidAddress(t) ∧ zeros(t) = 1

## E.document — IsDocument (INV, predicate(Tumbler))

ValidAddress(t) ∧ zeros(t) = 2

## E.element — IsElement (INV, predicate(Tumbler))

ValidAddress(t) ∧ zeros(t) = 3
