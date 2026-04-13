# Contract Review — ASN-0036 (cycle 2)

*2026-04-12 17:30*

### S7

`

- `MISSING_PRECONDITION: T3 (CanonicalRepresentation, ASN-0034) is explicitly invoked in the Uniqueness across documents sub-proof ("By T3 (CanonicalRepresentation, ASN-0034), this distinctness is decidable by component-wise comparison") but is absent from the contract's precondition list. All other named dependencies (S0, S4, S7a, S7b, T4, T10a, GlobalUniqueness) are listed; T3 is the sole omission.`

- `MISSING_POSTCONDITION: The proof establishes via T3 that the origin-distinctness result — origin(a₁) ≠ origin(a₂) — is decidable by component-wise comparison of the tumblers, without value comparison. This decidability claim is a proven result present in the proof body but is not captured in any of the three postconditions (a)–(c), nor in the invariant or frame. The frame says attribution requires no value comparison, but does not state the positive claim that the comparison is structurally decidable in O(min(|a₁|, |a₂|)) component checks.`

### ValidInsertionPosition

- `EXTRA_PRECONDITION: S8a — the proof does not use S8a as an assumption about the incoming arrangement. Under "S8a consistency," the proof *establishes* that every valid insertion position satisfies zeros(v) = 0 ∧ v > 0 (postcondition iii). S8a is a result of the definition, not a constraint the caller must supply. It should be removed from the preconditions list.`

2 mismatches.
