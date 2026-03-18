# ASN-0042 Formal Statements

*Source: ASN-0042-tumbler-ownership.md (revised 2026-03-15) — Index: 2026-03-16 — Extracted: 2026-03-16*

## Definition — OwnershipPrefix

`pfx : Principal → Tumbler` — injective mapping from principals to ownership prefixes.
Constraints: `zeros(pfx(π)) ≤ 1`, `T4(pfx(π))` for all `π ∈ Π`.

## Definition — OwnershipDomain

`dom(π) = {a ∈ T : pfx(π) ≼ a}`

## Definition — AccountField

`acct(a)`: when `zeros(a) = 0`, `acct(a) = a`; when `zeros(a) ≥ 1`, `acct(a)` is the truncation of `a` through its user field — the tumbler `N₁...Nα.0.U₁...Uβ`, having `zeros(acct(a)) = 1`.

## Definition — EffectiveOwner

`ω(a) = π  ≡  pfx(π) ≼ a  ∧  (A π' ∈ Π : π' ≠ π ∧ pfx(π') ≼ a : #pfx(π) > #pfx(π'))`

`ω : Σ.alloc → Principal` (defined only for allocated addresses).

## Definition — StrictPrefix

`p ≺ a  ≡  p ≼ a ∧ p ≠ a`

(equivalently, `p ≼ a ∧ #p < #a` — the equivalence holds because `p ≼ a ∧ #p = #a` gives `p = a` by T3)

## Definition — AllocatedBy

`allocated_by_Σ : Principal × Tumbler → Bool` — primitive relation: address `a` was allocated by principal `π` in the transition producing state `Σ`. Mechanism out of scope; constrained by O5 and O16.

## Definition — Delegated

`delegated_Σ(π, π')`: principal `π'` was introduced into `Π` by an act of `π` in state transition `Σ → Σ'`, subject to:

  (i) `pfx(π) ≺ pfx(π')`

  (ii) `π` is the most-specific covering principal for `pfx(π')` at the time of delegation: `(A π'' ∈ Π_Σ : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π))`

  (iii) `π' ∈ Π_{Σ'} ∖ Π_Σ`

  (iv) `zeros(pfx(π')) ≤ 1`

  (v) `T4(pfx(π'))`

  (vi) `¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))`

---

## O0 — StructuralOwnership (INV, predicate(Principal, Tumbler))

Whether principal `π` owns address `a` is decidable from `pfx(π)` and `a` alone, without consulting any mutable system state.

---

## O1 — PrefixDetermination (INV, predicate(Principal, Tumbler))

`owns(π, a)  ≡  pfx(π) ≼ a`

where `p ≼ a` denotes that `p` is a prefix of `a` in the sense of T5 — the components of `p` match the leading components of `a`.

---

## O1a — AccountBoundary (INV, predicate(State))

`(A π ∈ Π : zeros(pfx(π)) ≤ 1)`

---

## O1b — PrefixInjective (INV, predicate(State))

`(A π₁, π₂ ∈ Π : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

---

## O2 — OwnershipExclusivity (LEMMA)

`(A a ∈ Σ.alloc : (E! π ∈ Π : ω(a) = π))`

Well-definedness requires: (i) by O4, at least one covering principal exists; (ii) any two covering prefixes are linearly ordered — if `p₁ ≼ a` and `p₂ ≼ a` with `#p₁ ≤ #p₂`, then for every `i ≤ #p₁`, `(p₁)ᵢ = aᵢ = (p₂)ᵢ`, hence `p₁ ≼ p₂`; the covering set is finite (at most `#a` elements); a finite totally ordered set has a unique maximum; (iii) by O1b, the principal holding that longest prefix is unique.

---

## O3 — OwnershipRefinement (LEMMA, transition)

`(A a ∈ Σ.alloc, Σ, Σ' : Σ → Σ' ∧ ω_{Σ'}(a) ≠ ω_Σ(a)  ⟹  (E π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a))))`

Corollary: `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))` in all transitions.

---

## O4 — DomainCoverage (LEMMA)

`(A a ∈ Σ.alloc : (E π ∈ Π : pfx(π) ≼ a))`

---

## O5 — SubdivisionAuthority (INV, predicate(State, State), transition)

`(A Σ, Σ', a, π : Σ → Σ' ∧ a ∈ Σ'.alloc ∖ Σ.alloc ∧ allocated_by_{Σ'}(π, a)  ⟹  pfx(π) ≼ a  ∧  (A π' ∈ Π_Σ : pfx(π') ≼ a ⟹ #pfx(π') ≤ #pfx(π)))`

---

## AccountPrefix — AccountPrefix (LEMMA)

`(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)`

---

## O6 — StructuralProvenance (LEMMA)

`(A a, b ∈ Σ.alloc : acct(a) = acct(b) ⟹ ω(a) = ω(b))`

Biconditional (used in proof): `pfx(π) ≼ a  ≡  pfx(π) ≼ acct(a)` for all `π` with `zeros(pfx(π)) ≤ 1`.

Containment: `pfx(ω(a)) ≼ acct(a)` for all `a ∈ Σ.alloc`.

---

## O7 — OwnershipDelegation (POST, ensures)

`(A π, π' : delegated(π, π') :`

  (a) `ω_{Σ'}(a) = π'` for all `a ∈ dom(π') ∩ Σ'.alloc`

  (b) `π'` may allocate new addresses within `dom(π')` (O5 applies to `π'`)

  (c) `π'` may delegate sub-prefixes `p''` with `pfx(π') ≺ p''` per O7 recursively

---

## O8 — IrrevocableDelegation (LEMMA)

`(A π, π', a, Σ, Σ' : delegated_Σ(π, π') ∧ a ∈ dom(π') ∩ Σ'.alloc ∧ Σ →⁺ Σ' : ω_{Σ'}(a) ≠ π)`

---

## O9 — NodeLocalOwnership (LEMMA)

`(A π ∈ Π, a ∈ T : owns(π, a)  ⟹  nodeField(pfx(π)) ≼ nodeField(a))`

Two cases from O1a:
- When `zeros(pfx(π)) = 1`: `pfx(π) ≼ a` forces `nodeField(a) = nodeField(pfx(π))` (equality)
- When `zeros(pfx(π)) = 0`: `pfx(π) ≼ a` gives only `nodeField(pfx(π)) ≼ nodeField(a)` (prefix containment)

---

## O10 — DenialAsFork (POST, ensures)

When principal `π` requires modification of content at address `a` but `ω(a) ≠ π`, the system provides alternative address `a'` within `dom(π)` satisfying:

  (a) `ω(a') = π`

  (b) address `a` is unchanged — `ω(a)` is unaltered, no content modified, no ownership transferred

Structural consequence of (a): since `ω(a') = π` gives `pfx(π) ≼ a'`, the O6 biconditional yields `pfx(π) ≼ acct(a')`.

Existence: such `a'` exists in every reachable state:
- When `zeros(pfx(π)) = 1`: no sub-delegate can cover any document-level address in `dom(π)` (a sub-delegate prefix extending `N.0.U` would require a second zero to match document-level addresses, violating O1a)
- When `zeros(pfx(π)) = 0`: choose user-field value `u` exceeding all user-field components of all existing sub-delegate prefixes (finite set; T0a guarantees existence); then `a' = pfx(π).0.u.0.1.0.1` satisfies `pfx(π) ≼ a'` and `ω(a') = π`

---

## O11 — IdentityAxiomatic (INV)

`(A session : session.account = pfx(π)  is an axiom of the session, not a theorem of the ownership model)`

The ownership model treats principal identity as given. Properties O0–O10 hold for any consistent mapping from sessions to account tumblers; the binding mechanism is external.

---

## O12 — PrincipalPersistence (INV, predicate(State, State), transition)

`(A Σ, Σ' : Σ → Σ' ⟹ Π_Σ ⊆ Π_{Σ'})`

---

## O13 — PrefixImmutable (INV, predicate(State, State), transition)

`(A π ∈ Π_Σ, Σ, Σ' : Σ → Σ' ∧ π ∈ Π_{Σ'}  ⟹  pfx_{Σ'}(π) = pfx_Σ(π))`

---

## O14 — BootstrapPrincipal (INV, predicate(State))

`Π₀ ≠ ∅  ∧  (A a ∈ Σ₀.alloc : (E π ∈ Π₀ : pfx(π) ≼ a))`

`(A π ∈ Π₀ : zeros(pfx(π)) ≤ 1)`

`(A π₁, π₂ ∈ Π₀ : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

`(A π ∈ Π₀ : T4(pfx(π)))`

`(A π₁, π₂ ∈ Π₀ : π₁ ≠ π₂ ⟹ pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁))`

---

## O15 — PrincipalClosure (INV, predicate(State, State), transition)

`(A Σ, Σ' : Σ → Σ' ⟹ |Π_{Σ'} ∖ Π_Σ| ≤ 1)`

`(A π' ∈ Π_{Σ'} ∖ Π_Σ : (E π ∈ Π_Σ : delegated_Σ(π, π')))`

---

## O16 — AllocationClosure (INV, predicate(State, State), transition)

`(A Σ, Σ', a : Σ → Σ' ∧ a ∈ Σ'.alloc ∖ Σ.alloc  ⟹  (E π ∈ Π_Σ : allocated_by_{Σ'}(π, a)))`

---

## O17 — AllocatedAddressValid (INV, predicate(State))

`(A Σ, a : a ∈ Σ.alloc ⟹ T4(a))`

Initial state: `(A a ∈ Σ₀.alloc : T4(a))`.

---

## Corollary — AccountPermanence (LEMMA)

For any principal `π` in any reachable state, changes to `ω` within `dom(π)` arise exclusively from `π`'s own delegation acts or from sub-delegates' acts within their own sub-domains. No external act can alter `ω` within `dom(π)` without `π`'s involvement.

Base case: `(A π₁, π₂ ∈ Π₀ : π₁ ≠ π₂ ⟹ pfx(π₁) ⋠ pfx(π₂))` — no bootstrap principal has a prefix extending another's.

Inductive step: for any `π' ∈ Π_{Σ'} ∖ Π_Σ` introduced by delegation with `pfx(π) ≺ pfx(π')`, the delegator is (by condition (ii) of `delegated`) the most-specific covering principal for `pfx(π')` — either `π` itself or a sub-delegate of `π` by the inductive hypothesis. Condition (vi) blocks any introduction of `π'` where `pfx(π') ≺ pfx(π)` for some existing `π`.

Conclusion: `(A π ∈ Π_Σ, a ∈ dom(π) ∩ Σ.alloc : ω_Σ(a) ≠ π ⟹ (E π' ∈ Π_Σ : pfx(π) ≺ pfx(π') ∧ pfx(π') ≼ a ∧ π' introduced through delegation chain rooted at π))`
