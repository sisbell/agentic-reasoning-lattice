# Cone Review — ASN-0034/TA3 (cycle 2)

*2026-04-16 07:46*

### TA3 Depends field cites three properties by incorrect identifiers
**Foundation**: (internal — foundation ASN)
**ASN**: TA3 (OrderPreservationUnderSubtractionWeak), formal contract Depends field
**Issue**: Three of the five dependencies in TA3's contract are cited with parenthetical identifiers that do not match the identifiers declared at the corresponding property definitions:

| Cited in TA3 Depends | Declared at property definition |
|---|---|
| `TA2 (WellFormedSubtraction)` | `TA2 (WellDefinedSubtraction)` |
| `T3 (EqualityFromComponentAgreement)` | `T3 (CanonicalRepresentation)` |
| `TA6 (ZeroTumblerOrdering)` | `TA6 (ZeroTumblers)` |

The other two citations (`TumblerSub (TumblerSub)`, `T1 (LexicographicOrder)`) match correctly, as do all citations in every other property's Depends field in this ASN. The mismatches are confined to TA3, suggesting its contract was written from memory rather than by reference. A formalization tool that resolves dependencies by identifier will fail to link these three edges of the dependency graph.
**What needs resolving**: TA3's Depends must use the same parenthetical identifiers that the cited properties declare. Either the citations in TA3 must be corrected to match the declarations, or (if the alternative names are preferred) the declarations at TA2, T3, and TA6 must be updated — but not both diverging.

---

### T3 formal contract omits Depends on T0
**Foundation**: (internal — T0 CarrierSetDefinition, not shown)
**ASN**: T3 (CanonicalRepresentation), formal contract — the contract contains only a Postcondition field, with no Preconditions and no Depends
**Issue**: T3's proof opens with "T3 follows from T0's definition of the carrier set. By T0, T is the set of all finite sequences over ℕ" and proceeds to derive the biconditional from T0's extensional definition of sequence equality. Every other property in this ASN that derives from T0 lists it in its Depends field (T1, TumblerSub, TA6 all cite T0). T3's contract is the sole exception — it has no Depends field at all. A formalization tool will see T3 as having zero upstream dependencies, when in fact its proof rests on T0's characterisation of the carrier set.
**What needs resolving**: T3's formal contract must include a Depends field citing T0 (CarrierSetDefinition), consistent with how every other property in this ASN treats T0.
