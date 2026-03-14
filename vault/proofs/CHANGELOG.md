# Proof Modules — Changelog

## 2026-03-13: TumblerAlgebra — extract shared definitions, rename for clarity

Extracted definitions duplicated across ASN-0034 modeling files into TumblerAlgebra.dfy:
- **LastNonzero** (+ LastNonzeroRec, LastNonzeroAt): last nonzero component position. From AllocatorDiscipline.dfy (was `LastSig`/`LastSigRec`/`LastSigIs`).
- **FindZero**: first zero in sequence from a given position. From SubspaceDisjoint.dfy.
- **AllocationInc** (+ AllocationIncMonotone): hierarchical increment TA5 and its monotonicity lemma. From AllocatorDiscipline.dfy / HierarchicalIncrement.dfy (was `Inc`/`IncStrictlyGreater`).
- **LessEq**: less-than-or-equal ordering. From ContiguousSubtrees.dfy.
- **SubtractResultAt**: characterize each component of TumblerSubtract result. From SubtractionStrictOrder.dfy (was `SubComponent`).

Renames reflect intent: `LastSig` → `LastNonzero` (self-documenting), `Inc` → `AllocationInc` (distinguishes allocation protocol from displacement arithmetic), `SubComponent` → `SubtractResultAt` (avoids ambiguity with "sub-component").

Added type aliases `Address = Tumbler` and `Displacement = Tumbler` for role clarity. Applied to `ActionPoint(w: Displacement)`, `TumblerAdd(a: Address, w: Displacement): Address`, `AllocationInc(t: Address, ...): Address`. Ordering and subtraction signatures stay as `Tumbler` (role-agnostic).

Planned rename for Allocation module: `AllocationPermanence` → `AddressPermanence`. ASN-0034 labels T8 "Allocation permanence" but T8's statement is about the address persisting, not the allocation act. The old ASN-0001 proofs used `AddressPermanence` which is more precise.

## 2026-03-13: ASN-0034 restart — clean slate

ASN-0034 (Tumbler Algebra) converged, replacing ASN-0001 as the foundation. Removed all deprecated modules: AddressAllocation (ASN-0001 property proofs), Foundation (Two-Space state model), DocumentOntology (ASN-0029 types), TwoSpace (ASN-0026 properties). These will be regenerated fresh against ASN-0034 as each downstream ASN is redrafted.

Retained: TumblerAlgebra/TumblerAlgebra.dfy (shared definitions). ASN-0034 property proofs will be generated into TumblerAlgebra/ alongside the definitions module.
