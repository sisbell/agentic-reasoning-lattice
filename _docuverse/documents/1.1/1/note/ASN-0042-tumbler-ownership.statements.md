# ASN-0042 Claim Statements

*Source: ASN-0042-tumbler-ownership.md (revised 2026-03-15) — Extracted: 2026-05-14*

## Definition — OwnershipPrefix

`pfx : Π → T` is a total mapping assigning each principal its ownership prefix.

- *Axiom:* `pfx : Π → T` is a total mapping assigning each principal its ownership prefix.
- *Preconditions:* `π ∈ Π`.
- *Postconditions:* (a) `pfx(π) ∈ T`. (b) `T4(pfx(π))` — the prefix is a valid tumbler satisfying HierarchicalParsing.
- *Related properties (stated separately):* injectivity is O1b; the account-level boundary (`zeros(pfx(π)) ≤ 1`) is O1a.

## Definition — AccountField

- *Preconditions:* `a ∈ T` is a valid tumbler satisfying T4 (HierarchicalParsing) and T4a (SyntacticEquivalence).
- *Definition:* `acct(a) = a` when `zeros(a) = 0`; `acct(a) = N(a) ++ [0] ++ U(a)` when `zeros(a) ≥ 1`, where `N(a)` and `U(a)` are the node and user fields extracted by `fields(a)` (T4b UniqueParse), with component-wise access decidable from T3 (CanonicalRepresentation).
- *Postconditions:* (a) `acct(a)` is a valid tumbler satisfying T4. (b) `zeros(acct(a)) ≤ 1`: specifically, `zeros(acct(a)) = 0` when `zeros(a) = 0`, and `zeros(acct(a)) = 1` when `zeros(a) ≥ 1`. (c) When `zeros(a) ≤ 1`: `acct(a) = a`. (d) When `zeros(a) ≥ 2`: `acct(a)` is a proper prefix of `a` with `zeros(acct(a)) = 1`.

## Definition — OwnershipDomain

For principal `π ∈ Π`, define `dom(π) = {a ∈ T : pfx(π) ≼ a}`.

## Definition — AllocatedBy

- *Axiom:* `allocated_by_Σ(π, a)` is a primitive relation of the ownership model.
- *Signature:* `allocated_by_Σ : Principal × Tumbler → Bool`
- *Semantics:* `allocated_by_{Σ'}(π, a)` holds when the baptism procedure, executing on behalf of `π`, produced `a` during the transition yielding `Σ'`.
- *Constraints:* O5 (SubdivisionAuthority) — allocator is most-specific covering principal; O16 (AllocationClosure) — every new address has an allocator.

## Definition — DelegationPredicate

`delegated_Σ(π, π')` holds iff `π ∈ Π_Σ`, the successor state `Σ'` satisfies `Σ → Σ'`, and the six conditions hold for the pair `(π, π')`:

  (i)   `pfx(π) ≺ pfx(π')` — the delegate's prefix strictly extends the delegator's

  (ii)  `(A π'' ∈ Π_Σ : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π))` — delegator is most-specific covering principal for `pfx(π')` in `Π_Σ`

  (iii) `π' ∈ Π_{Σ'} ∖ Π_Σ` — the delegate is newly introduced

  (iv)  `zeros(pfx(π')) ≤ 1` — the delegate's prefix is at node or account level

  (v)   `T4(pfx(π'))` — the delegate's prefix is a valid tumbler address

  (vi)  `¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))` — no existing principal has a prefix strictly extending the new delegate's prefix

`delegated_Σ*` is the reflexive-transitive closure of `R_Σ` where `R_Σ(π, π')` iff `(E k : 0 ≤ k < n : delegated_{Σ_k}(π, π'))` along a witnessing path `Σ_0 → ... → Σ_n = Σ`.

## Definition — EffectiveOwner

`ω_Σ : Σ.B → Π_Σ` with:

  `ω_Σ(a) = π  ≡  π ∈ Π_Σ  ∧  pfx(π) ≼ a  ∧  (A π' ∈ Π_Σ : π' ≠ π ∧ pfx(π') ≼ a ⟹ #pfx(π) > #pfx(π'))`

---

## O0 — StructuralOwnership (AXIOM, predicate)

The ownership predicate `owns(π, a)` is decidable from `pfx(π)` and `a` alone, without consulting any mutable system state. The decision procedure inspects only two tumblers; no registry, table, or transition history is required.

O0 governs the two-place predicate `owns(π, a)`, not the one-place effective-owner function `ω(a)`. The structural-decidability claim of O0 is tight: a stranger handed the tumbler pair `(pfx(π), a)` can decide ownership; the same stranger handed only `a` cannot identify `ω(a)` without also being handed (a representation of) `Π_Σ`.

## O1 — PrefixDetermination (DEF, predicate)

Principal `π` owns address `a` iff `pfx(π)` is a prefix of `a`:

  `owns(π, a)  ≡  pfx(π) ≼ a`

where `p ≼ a` denotes that `p` is a prefix of `a` in the sense of Prefix (PrefixRelation) — the components of `p` match the leading components of `a`.

- *Definition:* `owns(π, a) ≡ pfx(π) ≼ a`, where `≼` is the prefix relation defined by Prefix (PrefixRelation).
- *Preconditions:* `π ∈ Π`, `a ∈ T`, `T4(pfx(π))`.
- *Postconditions:* `owns(π, a)` is a total, decidable predicate on `Π × T`.

## O1a — AccountOwnershipBoundary (AXIOM, predicate)

Ownership principals exist only at node level or account level:

  `(A π ∈ Π : zeros(pfx(π)) ≤ 1)`

Sub-account allocation — creating documents, versions, elements — does not introduce new ownership principals.

## O1b — PrefixInjectivity (AXIOM, lemma)

`(A π₁, π₂ ∈ Π : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

## O2 — OwnershipExclusivity (LEMMA, lemma)

For every reachable state `Σ` and every allocated address `a ∈ Σ.B`, there exists exactly one principal in `Π_Σ` that effectively owns `a` — equivalently, `ω_Σ : Σ.B → Π_Σ` is a total well-defined function:

  `(A Σ reachable, a ∈ Σ.B : (E! π ∈ Π_Σ : ω_Σ(a) = π))`

- *Preconditions:* `Σ` reachable from `Σ₀`, `a ∈ Σ.B`.
- *Postconditions:* `(E! π ∈ Π_Σ : ω_Σ(a) = π)` — exactly one principal satisfies the defining equivalence.
- *Invariant:* `ω` is a total well-defined function on `Σ.B` in every reachable state.

## Covering-chain lemma — PrefixesOfCommonAddressAreComparable (LEMMA, lemma)

Any two tumbler prefixes of a common address are `≼`-comparable:

  `(A x, p, q ∈ T : p ≼ x ∧ q ≼ x ⟹ p ≼ q ∨ q ≼ p)`

## MostSpecificCoveringUnique — MostSpecificCoveringUnique (LEMMA, lemma)

Whenever a principal achieves the maximum prefix length among the covering principals of a tumbler, that principal is unique:

  `(A Σ reachable, x ∈ T, π₁ π₂ ∈ Π_Σ : pfx(π₁) ≼ x ∧ pfx(π₂) ≼ x ∧ #pfx(π₁) = #pfx(π₂) = max{#pfx(π) : π ∈ Π_Σ ∧ pfx(π) ≼ x} ⟹ π₁ = π₂)`

## SelfOwnershipAtPrefix — SelfOwnershipAtPrefix (LEMMA, lemma)

Every principal is the effective owner of its own prefix:

  `(A Σ : Σ reachable from Σ₀ : (A π ∈ Π_Σ : ω_Σ(pfx(π)) = π))`

- *Preconditions:* `Σ` reachable from `Σ₀`, `π ∈ Π_Σ`.
- *Postconditions:* `ω_Σ(pfx(π)) = π`.
- *Invariant:* The boundary of `dom(π)` is structurally inhabited by `π` itself — every principal owns its own delegation point in every reachable state.

## O3 — OwnershipRefinement (LEMMA, lemma)

The effective owner of an address changes only when delegation introduces a principal with a strictly longer matching prefix. No other transition alters `ω`:

  `(A a ∈ Σ.B, Σ, Σ' : Σ → Σ' ∧ ω_{Σ'}(a) ≠ ω_Σ(a)  ⟹  (E π_d ∈ Π_Σ, π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a)) ∧ delegated_Σ(π_d, π')))`

- *Preconditions:* `Σ` reachable from `Σ₀`, `a ∈ Σ.B`, `Σ → Σ'`, `ω_{Σ'}(a) ≠ ω_Σ(a)`.
- *Postconditions:* `(E π_d ∈ Π_Σ, π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a)) ∧ delegated_Σ(π_d, π'))`.
- *Invariant:* `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))` for all transitions `Σ → Σ'` between reachable states, given `a ∈ Σ.B`.

## OwnershipDomainPermanence — OwnershipDomainPermanence (LEMMA, lemma)

No principal external to `dom(π)` can alter effective ownership within `dom(π)`. Changes to `ω(a)` for addresses in a principal's domain arise only from that principal's own delegation acts or from delegation acts of its sub-delegates:

  `(A π ∈ Π_Σ, Σ, Σ' : Σ → Σ' ∧ (E a ∈ dom(π) ∩ Σ.B : ω_{Σ'}(a) ≠ ω_Σ(a))  ⟹  (E π_d ∈ Π_Σ : pfx(π) ≼ pfx(π_d) ∧ (E π' ∈ Π_{Σ'} ∖ Π_Σ : delegated_Σ(π_d, π'))))`

Multi-step corollary (OwnershipDomainPermanence★): Let `Σ →⁺ Σ'` abbreviate `Σ → Σ_1 → ... → Σ_n = Σ'` for some `n ≥ 1`:

  `(A π ∈ Π_Σ, Σ, Σ', a : Σ reachable from Σ₀ ∧ Σ →⁺ Σ' ∧ a ∈ dom(π) ∩ Σ.B  ⟹  (A i, 0 ≤ i < n : ω_{Σ_{i+1}}(a) ≠ ω_{Σ_i}(a) ⟹ (E π_d^{(i)} ∈ Π_{Σ_i}, π'^{(i)} ∈ Π_{Σ_{i+1}} ∖ Π_{Σ_i} : pfx(π) ≼ pfx(π_d^{(i)}) ∧ delegated_{Σ_i}(π_d^{(i)}, π'^{(i)}))))`

- *Preconditions:* `Σ` reachable from `Σ₀`, `π ∈ Π_Σ`, `a ∈ dom(π) ∩ Σ.B`, `Σ → Σ'`, `ω_{Σ'}(a) ≠ ω_Σ(a)`.
- *Postconditions:* `(E π_d ∈ Π_Σ : pfx(π) ≼ pfx(π_d) ∧ (E π' ∈ Π_{Σ'} ∖ Π_Σ : delegated_Σ(π_d, π')))`.
- *Invariant:* Effective ownership within `dom(π)` is sovereign — no delegation by a principal external to `dom(π)` can alter `ω(a)` for any `a ∈ dom(π)`.

## O4 — DomainCoverage (LEMMA, lemma)

For every allocated address in any reachable state, at least one principal's prefix contains it:

  `(A Σ : Σ reachable from Σ₀ : (A a ∈ Σ.B : (E π ∈ Π_Σ : pfx(π) ≼ a)))`

- *Preconditions:* `Σ` reachable from `Σ₀`, `a ∈ Σ.B`.
- *Postconditions:* `(E π ∈ Π_Σ : pfx(π) ≼ a)`.
- *Invariant:* Coverage holds in every reachable state — no allocated address is orphaned from the principal hierarchy.

## O5 — SubdivisionAuthority (AXIOM, predicate)

Only the principal with the longest matching prefix may allocate new addresses within its domain:

  `(A Σ, Σ', a, π : Σ → Σ' ∧ π ∈ Π_Σ ∧ a ∈ Σ'.B ∖ Σ.B ∧ allocated_by_{Σ'}(π, a)  ⟹  pfx(π) ≼ a  ∧  (A π' ∈ Π_Σ : pfx(π') ≼ a ⟹ #pfx(π') ≤ #pfx(π)))`

## AccountPrefix — AccountPrefix (LEMMA, lemma)

`(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)`

- *Preconditions:* `a ∈ T`, `T4(a)`.
- *Postconditions:* `acct(a) ≼ a`. When `zeros(a) ≤ 1`: `acct(a) = a` (equality). When `zeros(a) ≥ 2`: `acct(a) ≺ a` (strict prefix).

## O6 — StructuralProvenance (LEMMA, lemma)

The effective owner of an allocated address is determined entirely by its account field:

  `(A a, b ∈ Σ.B : acct(a) = acct(b) ⟹ ω(a) = ω(b))`

- *Preconditions:* `a, b ∈ Σ.B`, `acct(a) = acct(b)`.
- *Postconditions:* `ω(a) = ω(b)`.
- *Invariant:* `pfx(ω(a)) ≼ acct(a)` for all `a ∈ Σ.B`.

Biconditional (proved in derivation): for any principal `π` with `zeros(pfx(π)) ≤ 1`:

  `pfx(π) ≼ a  ≡  pfx(π) ≼ acct(a)`

## O7 — OwnershipDelegation (LEMMA, lemma)

A principal `π` may delegate a sub-prefix to a new principal `π'`, provided the `delegated` relation is satisfied. Upon delegation:

  `(A π, π' : delegated(π, π') :`

  (a) `ω_{Σ'}(a) = π'` for all `a ∈ dom(π') ∩ Σ'.B`

  (b) `π'` may allocate new addresses within `dom(π')` (O5 applies to `π'`)

  (c) `π'` may delegate a sub-prefix `p''` with `pfx(π') ≺ p''` to a new principal `π''` whenever, at the prospective delegation state, both (ii) `π'` is the most-specific covering principal for `p''` — no existing principal has a prefix `pfx(π''') ≼ p''` with `pfx(π') ≺ pfx(π''')` — and (vi) no existing principal already extends `p''` strictly — `¬(E π''' ∈ Π : p'' ≺ pfx(π'''))`)

- *Preconditions:* `delegated_Σ(π, π')`, `Σ → Σ'`.
- *Postconditions:* (a) `(A a ∈ dom(π') ∩ Σ'.B : ω_{Σ'}(a) = π')`; (b) `π'` satisfies O5 for allocations within `dom(π')`; (c) the delegation relation is satisfiable with `π'` as delegator for any sub-prefix `p''` at every state at which (ii) `π'` remains the most-specific covering principal for `p''` and (vi) no existing principal has a prefix strictly extending `p''`.

## O8 — IrrevocableDelegation (LEMMA, lemma)

Once principal `π` delegates to `π'`, the delegating parent never regains effective ownership of addresses in the delegate's domain:

  `(A π, π', a, Σ_d, Σ' : Σ_d reachable from Σ₀ ∧ delegated_{Σ_d}(π, π') ∧ Σ_d →⁺ Σ' ∧ π' ∈ Π_{Σ'} ∧ a ∈ dom(π') ∩ Σ'.B : ω_{Σ'}(a) ≠ π)`

- *Preconditions:* `Σ_d` reachable from `Σ₀`, `delegated_{Σ_d}(π, π')`, `Σ_d →⁺ Σ'`, `π' ∈ Π_{Σ'}`, `a ∈ dom(π') ∩ Σ'.B`.
- *Postconditions:* `ω_{Σ'}(a) ≠ π`.
- *Invariant:* Once delegation occurs, the parent's prefix is permanently shorter than the delegate's, so the parent can never regain longest-match status for any address in the delegate's domain.

## O9 — NodeLocalOwnership (LEMMA, lemma)

For a principal `π`, the ownership predicate `owns(π, a)` can hold only for allocated addresses `a` whose node field extends the principal's node field:

  `(A π ∈ Π, a ∈ Σ.B : owns(π, a)  ⟹  N(pfx(π)) ≼ N(a))`

- *Preconditions:* `π ∈ Π`, `a ∈ Σ.B`, `owns(π, a)`.
- *Postconditions:* `N(pfx(π)) ≼ N(a)`. When `zeros(pfx(π)) = 1`: `N(pfx(π)) = N(a)` (equality). When `zeros(pfx(π)) = 0`: `N(pfx(π)) ≼ N(a)` (proper prefix permitted).

## O10 — DenialAsFork (LEMMA, lemma)

When principal `π` requires modification of content at address `a` but `ω(a) ≠ π`, the system provides an alternative: `π` may create a new address `a'` within `dom(π)`:

  (a) `ω(a') = π` — the new address is fully owned by the requesting principal

  (b) the original address `a` is unchanged — no ownership is transferred, no content is modified

  (c) `zeros(a') = zeros(pfx(π)) + 1` — the fork sits exactly one structural tier below the principal's prefix

- *Preconditions:* `Σ` reachable from `Σ₀`, `π ∈ Π_Σ`, `a ∈ Σ.B`, `ω(a) ≠ π`.
- *Postconditions:* `(E Σ', a' : Σ → Σ' ∧ a' ∈ dom(π) ∩ Σ'.B ∧ ω_{Σ'}(a') = π ∧ zeros(a') = zeros(pfx(π)) + 1 ∧ a ∈ Σ'.B)` — there exists a successor state `Σ'` (reached via a single authorized baptism from `Σ`) and a new address `a' = pfx(π).0.{hwm_0 + 1}` (where `hwm_0 := hwm(Σ.B, pfx(π), 2)`) such that `a'` is effectively owned by `π` in `Σ'`, sits exactly one structural tier below `pfx(π)`, and the original address `a` remains allocated and unmodified.
- *Unilateral postcondition (Unilateral O10★):* In every reachable state `Σ` and for every `π ∈ Π_Σ`, the existence claim is witnessed by a single baptism `Σ → Σ'` performed by `π` alone, producing `a' = pfx(π).0.{hwm_0 + 1}` ∈ `dom(π) ∩ Σ'.B` with `ω_{Σ'}(a') = π`. The unilateral guarantee is unconditional: PrefixBaptismCoupling ensures every sub-delegate's prefix lies in `Σ.B`, so the depth-2 component of every length-`(#pfx(π) + 2)` Form B sub-delegate prefix is at most `hwm_0`, and `hwm_0 + 1` is never claimed by any sub-delegate in every reachable state.

## O12 — PrincipalPersistence (AXIOM, predicate)

Once a principal joins Π, no operation removes it:

  `(A Σ, Σ' : Σ → Σ' ⟹ Π_Σ ⊆ Π_{Σ'})`

## O13 — PrefixImmutability (AXIOM, predicate)

Once established, a principal's ownership prefix cannot be altered:

  `(A π ∈ Π_Σ, Σ, Σ' : Σ → Σ' ∧ π ∈ Π_{Σ'} ⟹ pfx_{Σ'}(π) = pfx_Σ(π))`

## O14 — BootstrapPrincipal (AXIOM, predicate)

The initial principal set is non-empty and finite, every initially allocated address is covered by at least one initial principal, every initial principal's prefix is itself initially baptized, and the initial principals satisfy the structural constraints that O1a, O1b, T4, and pairwise non-nesting require:

  `Π₀ ≠ ∅  ∧  (A a ∈ Σ₀.B : (E π ∈ Π₀ : pfx(π) ≼ a))`

  `|Π₀| < ∞`

  `(A π ∈ Π₀ : zeros(pfx(π)) ≤ 1)`

  `(A π₁, π₂ ∈ Π₀ : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

  `(A π ∈ Π₀ : T4(pfx(π)))`

  `(A π₁, π₂ ∈ Π₀ : π₁ ≠ π₂ ⟹ pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁))`

  `(A π ∈ Π₀ : pfx(π) ∈ Σ₀.B)`

## O15 — PrincipalClosure (AXIOM, predicate)

Principals enter Π exclusively through bootstrap (in Π₀) or through a delegation act of an existing principal subject to six structural conditions; no other mechanism introduces principals. Each state transition introduces at most one new principal:

  `(A Σ, Σ' : Σ → Σ' ⟹ |Π_{Σ'} ∖ Π_Σ| ≤ 1)`

  `(A π' ∈ Π_{Σ'} ∖ Π_Σ : (E π ∈ Π_Σ :`
  `      (i)   pfx(π) ≺ pfx(π')`
  `      (ii)  (A π'' ∈ Π_Σ : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π))`
  `      (iii) π' ∈ Π_{Σ'} ∖ Π_Σ`
  `      (iv)  zeros(pfx(π')) ≤ 1`
  `      (v)   T4(pfx(π'))`
  `      (vi)  ¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π'')) ))`

## FiniteRegistry — FiniteRegistry (LEMMA, lemma)

In every reachable state, the principal registry is finite:

  `(A Σ : Σ reachable from Σ₀ : |Π_Σ| < ∞)`

## NestingByDelegation — NestingByDelegation (LEMMA, lemma)

In every reachable state `Σ`, any two distinct principals are either non-nesting in their prefixes, or one strictly extends the other and the extending principal was introduced via a chain of delegations originating at the shorter-prefix principal:

  `(A Σ : Σ reachable from Σ₀ : (A π₁, π₂ ∈ Π_Σ : π₁ ≠ π₂ ⟹`
  `      (pfx(π₁) and pfx(π₂) are non-nesting) ∨`
  `      (pfx(π₁) ≺ pfx(π₂) ∧ delegated_Σ*(π₁, π₂)) ∨`
  `      (pfx(π₂) ≺ pfx(π₁) ∧ delegated_Σ*(π₂, π₁)) ))`

where `delegated_Σ*(π, π')` is the reflexive-transitive closure of `R_Σ(π, π')` iff `(E k : 0 ≤ k < n : delegated_{Σ_k}(π, π'))` along the witnessing path `Σ_0 → Σ_1 → ... → Σ_n = Σ`.

## O16 — AllocationClosure (AXIOM, predicate)

Every address entering `Σ.B` in a state transition was allocated by some principal in `Π_Σ`:

  `(A Σ, Σ', a : Σ → Σ' ∧ a ∈ Σ'.B ∖ Σ.B  ⟹  (E π ∈ Π_Σ : allocated_by_{Σ'}(π, a)))`

## O17 — AllocatedAddressValidity (LEMMA, lemma)

Every allocated address is a valid tumbler:

  `(A Σ, a : a ∈ Σ.B ⟹ T4(a))`

## O18 — DelegationBaptizes (AXIOM, predicate)

Delegation materially baptizes the delegate's prefix freshly — the transition that introduces a new principal into `Π` enters its prefix into `Σ.B` as a newly registered tumbler, not previously present:

  `(A Σ, Σ', π' : Σ → Σ' ∧ π' ∈ Π_{Σ'} ∖ Π_Σ ⟹ pfx(π') ∈ Σ'.B ∖ Σ.B)`

## PrefixBaptismCoupling — PrefixBaptismCoupling (LEMMA, lemma)

In every reachable state, every principal's prefix is itself baptized:

  `(A Σ : Σ reachable from Σ₀ : (A π ∈ Π_Σ : pfx(π) ∈ Σ.B))`

- *Preconditions:* `Σ` reachable from `Σ₀`, `π ∈ Π_Σ`.
- *Postconditions:* `pfx(π) ∈ Σ.B`.
- *Invariant:* Principal registry and baptismal registry are coupled in every reachable state — no principal exists without an allocated prefix.

## DelegatorAllocatesPrefix — DelegatorAllocatesPrefix (LEMMA, lemma)

The delegating parent is the allocator of the delegate's prefix in the delegation transition:

  `(A Σ, Σ', π_d, π' : Σ reachable from Σ₀ ∧ delegated_Σ(π_d, π') ∧ Σ → Σ' ⟹ allocated_by_{Σ'}(π_d, pfx(π')))`

- *Preconditions:* `Σ` reachable from `Σ₀`, `delegated_Σ(π_d, π')`, `Σ → Σ'`.
- *Postconditions:* `allocated_by_{Σ'}(π_d, pfx(π'))`.
- *Invariant:* The two registries (principal `Π` and baptismal `B`) are coupled by a single allocator at every delegation act: the same `π_d` whose authority condition (ii) admits `π'` into `Π` is the allocator whose O5 authority enters `pfx(π')` into `B`.
