# ASN-0042 Formal Statements

*Source: ASN-0042-tumbler-ownership.md (revised 2026-03-15) — Extracted: 2026-03-22*

## Definition — OwnershipPrefix

`ownershipPrefix : Principal → Tumbler` — injective, `zeros(pfx(π)) ≤ 1`, `T4(pfx(π))`

## Definition — EffectiveOwner

`ω(a) = π  ≡  pfx(π) ≼ a  ∧  (A π' ∈ Π : π' ≠ π ∧ pfx(π') ≼ a : #pfx(π) > #pfx(π'))`

`effectiveOwner : Σ.alloc → Principal` — defined only for allocated addresses.

## Definition — OwnershipDomain

For principal `π ∈ Π`, define `dom(π) = {a ∈ T : pfx(π) ≼ a}`.

## Definition — AccountField

When `zeros(a) = 0`: `acct(a) = a`; when `zeros(a) ≥ 1`: `acct(a)` is the truncation of `a` through its user field — the tumbler `N₁...Nα.0.U₁...Uβ`, having `zeros(acct(a)) = 1`.

## Definition — AllocatedBy

`allocated_by_Σ : Principal × Tumbler → Bool`

Primitive relation: address `a` was allocated by principal `π` in the transition producing state `Σ`. Mechanism out of scope; constrained by O5 and O16.

## Definition — Delegated

`delegated_Σ(π, π')` holds when `π'` was introduced into `Π` by an act of `π` in state transition `Σ → Σ'`, subject to:

  (i) `pfx(π) ≺ pfx(π')` — the delegate's prefix strictly extends the delegator's

  (ii) `π` is the most-specific covering principal for `pfx(π')` at the time of delegation: `(A π'' ∈ Π_Σ : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π))`

  (iii) `π' ∈ Π_{Σ'} ∖ Π_Σ` — the delegate is newly introduced

  (iv) `zeros(pfx(π')) ≤ 1` — the delegate's prefix is at node or account level

  (v) `T4(pfx(π'))` — the delegate's prefix is a valid tumbler address

  (vi) `¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))` — no existing principal has a prefix strictly extending the new delegate's prefix

---

## O0 — StructuralOwnership (AX, axiom)

Whether principal `π` owns address `a` is decidable from `pfx(π)` and `a` alone, without consulting any mutable system state.

## O1 — PrefixDetermination (DEF, predicate)

Principal `π` owns address `a` iff `pfx(π)` is a prefix of `a`:

  `owns(π, a)  ≡  pfx(π) ≼ a`

where `p ≼ a` denotes that `p` is a prefix of `a` in the sense of T5 — the components of `p` match the leading components of `a`.

## O1a — AccountOwnershipBoundary (INV, predicate)

`(A π ∈ Π : zeros(pfx(π)) ≤ 1)`

## O1b — PrefixInjectivity (INV, predicate)

`(A π₁, π₂ ∈ Π : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

## O2 — OwnershipExclusivity (INV, lemma)

`(A a ∈ Σ.alloc : (E! π ∈ Π : ω(a) = π))`

where `ω(a)` is the principal with the longest matching prefix:

  `ω(a) = π  ≡  pfx(π) ≼ a  ∧  (A π' ∈ Π : π' ≠ π ∧ pfx(π') ≼ a : #pfx(π) > #pfx(π'))`

## O3 — OwnershipRefinement (INV, predicate)

`(A a ∈ Σ.alloc, Σ, Σ' : Σ → Σ' ∧ ω_{Σ'}(a) ≠ ω_Σ(a)  ⟹  (E π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a))))`

## O4 — DomainCoverage (INV, predicate)

`(A a ∈ Σ.alloc : (E π ∈ Π : pfx(π) ≼ a))`

## O5 — SubdivisionAuthority (INV, predicate)

`(A Σ, Σ', a, π : Σ → Σ' ∧ a ∈ Σ'.alloc ∖ Σ.alloc ∧ allocated_by_{Σ'}(π, a)  ⟹  pfx(π) ≼ a  ∧  (A π' ∈ Π_Σ : pfx(π') ≼ a ⟹ #pfx(π') ≤ #pfx(π)))`

## AccountPrefix — AccountPrefix (LEMMA, lemma)

`(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)`

Precondition: `T4(a)` is required; `acct` relies on field parsing (FieldParsing from ASN-0034), which requires T4 validity.

## O6 — StructuralProvenance (LEMMA, lemma)

`(A a, b ∈ Σ.alloc : acct(a) = acct(b) ⟹ ω(a) = ω(b))`

Derived biconditional (used in proof): `pfx(π) ≼ a  ≡  pfx(π) ≼ acct(a)` for all `π` with `zeros(pfx(π)) ≤ 1`.

Corollary: `pfx(ω(a)) ≼ acct(a)`.

## O7 — OwnershipDelegation (INV, predicate)

`(A π, π' : delegated(π, π') :`

  (a) `ω_{Σ'}(a) = π'` for all `a ∈ dom(π') ∩ Σ'.alloc`

  (b) `π'` may allocate new addresses within `dom(π')` (O5 applies to `π'`)

  (c) `π'` may delegate sub-prefixes `p''` with `pfx(π') ≺ p''` per O7 recursively

## O8 — IrrevocableDelegation (INV, predicate)

`(A π, π', a, Σ, Σ' : delegated_Σ(π, π') ∧ a ∈ dom(π') ∩ Σ'.alloc ∧ Σ →⁺ Σ' : ω_{Σ'}(a) ≠ π)`

## O9 — NodeLocalOwnership (INV, predicate)

`(A π ∈ Π, a ∈ T : owns(π, a)  ⟹  nodeField(pfx(π)) ≼ nodeField(a))`

## O10 — DenialAsFork (INV, predicate)

When principal `π` requires modification of content at address `a` but `ω(a) ≠ π`, the system provides an alternative: `π` may create a new address `a'` within `dom(π)` such that:

  (a) `ω(a') = π` — the new address is fully owned by the requesting principal

  (b) `a` is unchanged — no ownership is transferred, no content is modified

Precondition entailment: condition (a) entails `pfx(π) ≼ a'`, and the O6 biconditional yields `pfx(π) ≼ acct(a')`.

## O11 — IdentityAxiomatic (AX, axiom)

`(A session : session.account = pfx(π)  is an axiom of the session, not a theorem of the ownership model)`

The mechanism by which this establishment occurs (authentication, delegation verification, cryptographic binding) is external to the ownership model. Properties O0–O10 are independent of which mechanism is chosen, provided it is consistent with the delegation structure.

## O12 — PrincipalPersistence (INV, predicate)

`(A Σ, Σ' : Σ → Σ' ⟹ Π_Σ ⊆ Π_{Σ'})`

## O13 — PrefixImmutability (INV, predicate)

`(A π ∈ Π_Σ, Σ, Σ' : Σ → Σ' ∧ π ∈ Π_{Σ'}  ⟹  pfx_{Σ'}(π) = pfx_Σ(π))`

## O14 — BootstrapPrincipal (AX, axiom)

`Π₀ ≠ ∅  ∧  (A a ∈ Σ₀.alloc : (E π ∈ Π₀ : pfx(π) ≼ a))`

`(A π ∈ Π₀ : zeros(pfx(π)) ≤ 1)`

`(A π₁, π₂ ∈ Π₀ : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

`(A π ∈ Π₀ : T4(pfx(π)))`

`(A π₁, π₂ ∈ Π₀ : π₁ ≠ π₂ ⟹ pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁))`

## O15 — PrincipalClosure (INV, predicate)

`(A Σ, Σ' : Σ → Σ' ⟹ |Π_{Σ'} ∖ Π_Σ| ≤ 1)`

`(A π' ∈ Π_{Σ'} ∖ Π_Σ : (E π ∈ Π_Σ : delegated_Σ(π, π')))`

## O16 — AllocationClosure (INV, predicate)

`(A Σ, Σ', a : Σ → Σ' ∧ a ∈ Σ'.alloc ∖ Σ.alloc  ⟹  (E π ∈ Π_Σ : allocated_by_{Σ'}(π, a)))`

## O17 — AllocatedAddressValidity (INV, predicate)

`(A Σ, a : a ∈ Σ.alloc ⟹ T4(a))`
