# Divergences — B10 (RegistryT4Validity)

- **Line 52**: The ASN states B10 as a universal over all reachable registry states. The Dafny proof captures single-step preservation: given AllValid(B) and a B6-compliant baptism, B ∪ {fresh} remains AllValid. Full induction over the allocation state machine is outside scope.
