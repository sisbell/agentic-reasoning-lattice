# ASN-0042: Tumbler Ownership

*2026-03-15*

We are looking for what it means to *own* a position in the tumbler hierarchy. The tumbler algebra (ASN-0034) gives us a permanently expanding, totally ordered, hierarchically structured address space. But the algebra is silent on authority — it tells us that addresses exist and how they compare, not who may act upon them. Ownership is the layer of meaning that binds addresses to principals.

The investigation yields a central finding: ownership is not a table the system maintains but a *theorem about addresses*. The two-place ownership predicate `owns(π, a)` — "does this principal own this address?" — reduces to a prefix comparison between `pfx(π)` and `a`, requiring no consultation of mutable system state. The one-place effective-owner function `ω(a)` — "who owns this address?" — must additionally consult the principal registry to select the longest matching prefix; it is state-relativized, not absolute. Authorization decisions reduce to prefix comparison; identifying *which* principal authorizes requires the registry. This has consequences for delegation, for the boundaries of authority, and for the architectural response when a principal encounters content it does not own.

We derive each property from Nelson's design intent, corroborated by Gregory's implementation evidence, and state them at the level of abstraction required of any conforming implementation.


## Ownership as a Structural Predicate

We begin with the most fundamental question: how does the system determine who owns an address?

Nelson gives a striking answer. Ownership is not recorded in a registry external to the address — it is *readable from the address itself*:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." (LM 4/17)

Gregory's implementation confirms this with unusual force. The sole ownership predicate in udanax-green — `isthisusersdocument` — delegates entirely to `tumbleraccounteq`, a function that compares two tumbler mantissa arrays digit by digit. No table is consulted. No file is opened. No registry is queried. The function receives two tumblers, performs arithmetic on their components, and returns a boolean. If we removed the function and replaced it with any other function that performs the same comparison, the system's ownership behavior would be identical. Ownership *is* the comparison.

**pfx(π) (OwnershipPrefix).**

We introduce the principals. Let `Π` denote the set of *principals* — the ownership subjects. Each principal `π ∈ Π` is associated with an *ownership prefix* `pfx(π) ∈ T`, a valid tumbler (satisfying T4) that serves as the root of their namespace. The mapping `pfx` is injective — distinct principals have distinct prefixes (formalized as O1b below).

The mapping `pfx : Π → T` is a primitive of the ownership model. Its codomain is constrained to valid tumblers — `pfx(π) ∈ T` with `T4(pfx(π))` — so that field extraction (T4b) and the hierarchical level `zeros(pfx(π))` are determinate and the prefix comparison `pfx(π) ≼ a` of O1 is well-defined. The further structural constraints, injectivity (O1b) and the account-level bound `zeros(pfx(π)) ≤ 1` (O1a), are stated and proved as separate properties.

*Formal Contract:*
- *Axiom:* `pfx : Π → T` is a total mapping assigning each principal its ownership prefix.
- *Preconditions:* `π ∈ Π`.
- *Postconditions:* (a) `pfx(π) ∈ T`. (b) `T4(pfx(π))` — the prefix is a valid tumbler satisfying HierarchicalParsing.
- *Related properties (derived invariants, stated separately):* injectivity is O1b; the account-level boundary (`zeros(pfx(π)) ≤ 1`) is O1a.

**O1b (PrefixInjectivity).** `(A π₁, π₂ ∈ Π : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

Without injectivity, two principals sharing a prefix could both claim longest-match, and the effective owner function `ω` (defined in O2 below) would not yield a unique result.

The ownership question "does `π` own `a`?" is answered by examining these two tumblers alone:

**O0 (StructuralOwnership).** The ownership predicate `owns(π, a)` is decidable from `pfx(π)` and `a` alone, without consulting any mutable system state. The decision procedure inspects only two tumblers; no registry, table, or transition history is required.

O0 governs the two-place predicate `owns(π, a)`, not the one-place effective-owner function `ω(a)`. The latter ranges over the principal registry to select the longest matching prefix, so its evaluation requires `(a, Π_Σ, pfx)` — the registry is consulted to enumerate candidates. Deciding `owns(π, a)` requires only the tumbler pair `(pfx(π), a)`; this is why `tumbleraccounteq` accepts both tumblers as arguments and not just the address.

The decision procedure is prefix containment:

**O1 (PrefixDetermination).** Principal `π` owns address `a` iff `pfx(π)` is a prefix of `a`:

  `owns(π, a)  ≡  pfx(π) ≼ a`

where `p ≼ a` denotes that `p` is a prefix of `a` in the sense of Prefix (PrefixRelation) — the components of `p` match the leading components of `a`. T5 (ContiguousSubtrees) is the structural property of the address space that `≼` partitions the space into contiguous subtrees; the relation itself is supplied by Prefix.

O1 is a definition: we define the ownership predicate `owns(π, a)` to be identical with prefix containment `pfx(π) ≼ a`. We verify that the definition is well-formed and that it satisfies the decidability requirement O0.

*Well-formedness.* The prefix relation `≼` is defined by Prefix (PrefixRelation): `p ≼ a ⟺ #a ≥ #p ∧ (A i : 1 ≤ i ≤ #p : pᵢ = aᵢ)`. For `owns(π, a)` to be well-defined, two conditions must hold. First, `pfx(π)` must be a valid tumbler — this holds by the definition of `pfx`, which requires every principal's prefix to satisfy T4 (HierarchicalParsing). Second, the component-wise comparison must be determinate — by T3 (CanonicalRepresentation), each component `pᵢ` and `aᵢ` is a uniquely determined natural number, so equality at each position is decidable.

*Decidability.* The prefix check `pfx(π) ≼ a` requires one length comparison `#a ≥ #pfx(π)` followed by at most `#pfx(π)` component comparisons, each a comparison of natural numbers. The entire computation uses `pfx(π)` and `a` alone, consulting no mutable system state. This satisfies the design requirement O0 (StructuralOwnership): ownership is decidable from the prefix and the address without external state.

*Design justification.* Nelson states that "numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies" (LM 4/17) — ownership is legible from the address itself. Gregory's `tumbleraccounteq` confirms the decision procedure: it walks the mantissa arrays of two tumblers in lockstep, comparing components. The definition `owns(π, a) ≡ pfx(π) ≼ a` formalizes this structural containment exactly. ∎

*Formal Contract:*
- *Definition:* `owns(π, a) ≡ pfx(π) ≼ a`, where `≼` is the prefix relation defined by Prefix (PrefixRelation).
- *Preconditions:* `π ∈ Π`, `a ∈ T`, `T4(pfx(π))`.
- *Postconditions:* `owns(π, a)` is a total, decidable predicate on `Π × T`.


## The Account-Level Boundary

Not every prefix match constitutes an ownership claim. The tumbler hierarchy has four structural levels — node, user, document, element — separated by zero-valued components (T4). The allocation mechanism is uniform across all levels — any address holder can subdivide — but ownership authority is hierarchical, and the hierarchy has a definite floor.

Nelson is explicit on this point: "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). This is the strongest authority statement in the specification, and it appears only at the account level. At the document level, ownership is defined with specific enumerated rights: "only the owner has a right to withdraw a document or change it" (LM 2/29). At the version level, Nelson is deliberately cautious: "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation" (LM 4/29). The design intent is clear: baptism (allocation) is uniform; authority (ownership) flows from the account. Everyone at every level can fork sub-addresses — that is the mechanism. But what one can *do* with what one has forked depends on one's position in the ownership hierarchy.

We formalize this asymmetry:

**O1a (AccountOwnershipBoundary).** Ownership principals exist only at node level or account level:

  `(A π ∈ Π : zeros(pfx(π)) ≤ 1)`

Sub-account allocation — creating documents, versions, elements — does not introduce new ownership principals. It exercises the allocator's rights within an existing principal's domain.

**acct(a) (AccountField).**

Define `acct(a)` for any valid tumbler `a`: when `zeros(a) = 0` (node-level), `acct(a) = a` (so `zeros(acct(a)) = 0`); when `zeros(a) ≥ 1`, `acct(a)` is the tumbler whose components are `N(a)` followed by `[0]` followed by `U(a)` — using the foundation's field projections defined by T4b (UniqueParse), with component-wise access decidable from T3 (CanonicalRepresentation) — and `zeros(acct(a)) = 1` in this branch. The two branches together yield `zeros(acct(a)) ≤ 1` for every valid tumbler. We adopt the local abbreviation `fields(a) ≡ (N(a), U(a), D(a), E(a))` for the tuple of T4b's four partial projections (each component undefined when the corresponding field is absent), used as informal shorthand throughout this ASN whenever convenient.

Gregory confirms the account-level boundary with unusual force. His `tumbleraccounteq` walks the mantissa of both tumblers in lockstep. For each non-zero component in the account tumbler, the document's component must match. For each zero, the counter advances. When the counter reaches two — the second zero — the function returns true unconditionally. Everything beyond the second zero is ignored. The implementation has no mechanism for finer-grained discrimination: `isthisusersdocument` (in all three build targets — `be.c`, `socketbe.c`, `xumain.c`) delegates directly to `tumbleraccounteq` with no intervening check. There is no per-document, per-version, or per-element authorization predicate anywhere in the codebase. The BERT system tracks per-document open/close state, but its authorization fallback is `isthisusersdocument` — account-level.

The consequence: sub-account allocation (creating documents, versions, elements) creates addresses within the allocating principal's domain but does not partition that domain into sub-ownerships. A document address `N.0.U.0.D.0.E` and a different document address `N.0.U.0.D'.0.E'` under the same account are owned by the same principal — the one whose prefix matches `N.0.U`. Below the account level, there is only the binary distinction of "mine" versus "not mine."

O1a permits nesting *within* the account level. T4 allows multi-component user fields: `pfx(π₁) = [1, 0, 2]` and `pfx(π₂) = [1, 0, 2, 3]` both satisfy `zeros ≤ 1`, and `pfx(π₁) ≺ pfx(π₂)`. Nelson designed this deliberately: "accounts can spin off accounts" (LM 4/19). The User field is a tree, not a flat namespace — a principal may delegate a sub-account by forking a longer user field within its own prefix. Gregory confirms: `tumbleraccounteq` applied to account `[1, 0, 2, 3]` checks positions 0, 2, and 3, while account `[1, 0, 2]` checks only positions 0 and 2 — the child account is a strict refinement. What O1a prevents is *document-level* or *element-level* principals: no principal has `zeros(pfx(π)) ≥ 2`. The floor of ownership is the account level, but within that floor, the user-field tree can grow arbitrarily deep.

We first record the field-structure facts that both the well-formedness of `acct(a)` and the prefix relation `acct(a) ≼ a` (AccountPrefix, *Structural Provenance* below) rely on, proving them once here.

**Field decomposition (FD).** For a valid tumbler `a` satisfying T4 with `zeros(a) = z`, T4b (UniqueParse) decomposes `a` uniquely into `z + 1` fields — node, then (for `z ≥ 1`) user, (for `z ≥ 2`) document, (for `z = 3`) element — each a contiguous segment with a single zero between consecutive segments. By T4a (SyntacticEquivalence) every segment is non-empty (node length `α ≥ 1`, user length `β ≥ 1` when present, and so on), and by T4's positive-component constraint every non-separator component is strictly positive; the separators occupy exactly the zero-valued positions, the first at position `α + 1`, the second (if present) at `α + 1 + β + 1`, and so on. Component-wise access is decidable from T3 (CanonicalRepresentation), so the decomposition is computable from `a` alone. The case distinction `z ∈ {0, 1, 2, 3}` is exhaustive by T4's zero-count clause.

Well-formedness of `acct(a)` follows from FD. When `zeros(a) = 0`, `a` is node-level, `acct(a) = a`, and `zeros(acct(a)) = 0`. When `zeros(a) = 1`, `a = N(a) ++ [0] ++ U(a)` with no further components, so `acct(a) = N(a) ++ [0] ++ U(a) = a` and `zeros(acct(a)) = 1`. When `zeros(a) ≥ 2`, the construction `acct(a) = N(a) ++ [0] ++ U(a)` depends only on the node and user segments, which by FD have `α ≥ 1` and `β ≥ 1` strictly positive components: the result has length `α + 1 + β`, exactly one zero (at position `α + 1`, flanked by the positive last node component and first user component, so no adjacent zeros and no leading or trailing zero), hence satisfies T4 with `zeros(acct(a)) = 1`. In every case `acct(a)` is a valid tumbler satisfying T4 with `zeros(acct(a)) ≤ 1`. ∎

We record the shared field-structure fact this case analysis establishes, reused by AccountPrefix below. **(FieldStructure)** For a T4-valid `a`, `fields(a)` decomposes `a` uniquely (T4b) into non-empty field segments (T4a) of strictly positive components (T4), delimited by `a`'s `zeros(a)` zero separators. When `zeros(a) = 0`, `acct(a) = a`. When `zeros(a) ≥ 1`, the node and user fields occupy the leading `#acct(a) = α + 1 + β` positions (`α, β ≥ 1`), and `acct(a) = N(a) ++ [0] ++ U(a)` reproduces exactly those leading components of `a`; any document/element fields (present iff `zeros(a) ≥ 2`) occupy positions strictly after `α + 1 + β`.

*Formal Contract:*
- *Preconditions:* `a ∈ T` is a valid tumbler satisfying T4 (HierarchicalParsing — positive non-separator components, at most three zeros) and T4a (SyntacticEquivalence — no adjacent zeros, no leading or trailing zero).
- *Definition:* `acct(a) = a` when `zeros(a) = 0`; `acct(a) = N(a) ++ [0] ++ U(a)` when `zeros(a) ≥ 1`, where `N(a)` and `U(a)` are the node and user fields extracted by `fields(a)` (T4b UniqueParse), with component-wise access decidable from T3 (CanonicalRepresentation).
- *Postconditions:* (a) `acct(a)` is a valid tumbler satisfying T4. (b) `zeros(acct(a)) ≤ 1`: specifically, `zeros(acct(a)) = 0` when `zeros(a) = 0`, and `zeros(acct(a)) = 1` when `zeros(a) ≥ 1` — the two branches together yielding the ≤ 1 bound. (c) When `zeros(a) ≤ 1`: `acct(a) = a`. (Justification: `zeros(a) = 0` is immediate from the definition `acct(a) = a`; `zeros(a) = 1` follows because T4b's UniqueParse decomposes `a` uniquely as `N(a) ++ [0] ++ U(a)` with no components beyond the user field, so the construction `N(a) ++ [0] ++ U(a)` reconstructs `a` itself.) (d) When `zeros(a) ≥ 2`: `acct(a)` is a proper prefix of `a` with `zeros(acct(a)) = 1`.


## Ownership Domains

Each principal's prefix determines a set of addresses — their *domain*:

**Definition (OwnershipDomain).** For principal `π ∈ Π`, define `dom(π) = {a ∈ T : pfx(π) ≼ a}`.

*Notation.* `dom(π)` applies to a principal (the prefix-defined subset of `T`), distinct from `dom(A)` of T10a (ASN-0034), which enumerates an allocator's per-stream chain `{tₙ : n ≥ 0}`; argument kind disambiguates.

Before developing ownership domains' nesting structure, we extract a structural fact about the prefix relation `≼` that the subsequent proofs invoke repeatedly. The fact is a direct consequence of Prefix (PrefixRelation) of ASN-0034 and is independent of T5 (ContiguousSubtrees); we state it once as a named lemma:

**Covering-chain lemma (PrefixesOfCommonAddressAreComparable).** Any two tumbler prefixes of a common address are `≼`-comparable:

  `(A x, p, q ∈ T : p ≼ x ∧ q ≼ x ⟹ p ≼ q ∨ q ≼ p)`

*Proof.* By Prefix (PrefixRelation), `p ≼ x` expands to `#x ≥ #p ∧ (A i : 1 ≤ i ≤ #p : pᵢ = xᵢ)`, and `q ≼ x` expands to `#x ≥ #q ∧ (A i : 1 ≤ i ≤ #q : qᵢ = xᵢ)`. Both `p` and `q` agree with `x` on their respective leading components. Without loss of generality let `#p ≤ #q`. For each `i` with `1 ≤ i ≤ #p`, both equalities apply: `pᵢ = xᵢ = qᵢ`. Hence `pᵢ = qᵢ` for `1 ≤ i ≤ #p`, and `#p ≤ #q`, so `p ≼ q` by the Prefix definition. By T3 (CanonicalRepresentation), the component equalities are well-defined; no further appeal to T5 is required. ∎

The lemma admits an immediate specialization: when `p = pfx(π₁)`, `q = pfx(π₂)`, and `x = a` for some `a ∈ Σ.B`, any two principals covering `a` have nested prefixes; the same specialization applies with a principal's prefix `pfx(π')` in place of the address.

By T5 (ContiguousSubtrees), every ownership domain is a contiguous interval under the lexicographic order T1. This is a mathematical consequence of prefix containment and the tree-to-line mapping, not a policy choice. If `a, c ∈ dom(π)` and `a ≤ b ≤ c`, then `b ∈ dom(π)`. No address can escape from the interior of someone's domain.

Domains nest whenever prefixes nest:

  `pfx(π₁) ≼ pfx(π₂)  ⟹  dom(π₂) ⊆ dom(π₁)`

The proof unfolds the prefix relation componentwise. Suppose `a ∈ dom(π₂)`, so `pfx(π₂) ≼ a`: by Prefix (PrefixRelation) of ASN-0034, this expands to `#a ≥ #pfx(π₂)` and `pfx(π₂)ⱼ = aⱼ` for `1 ≤ j ≤ #pfx(π₂)`. The hypothesis `pfx(π₁) ≼ pfx(π₂)` likewise expands to `#pfx(π₁) ≤ #pfx(π₂)` and `pfx(π₁)ᵢ = pfx(π₂)ᵢ` for `1 ≤ i ≤ #pfx(π₁)`. Composing the two component equalities: for each `i` with `1 ≤ i ≤ #pfx(π₁)`, we have `pfx(π₁)ᵢ = pfx(π₂)ᵢ = aᵢ`. The length chain `#pfx(π₁) ≤ #pfx(π₂) ≤ #a` gives `#a ≥ #pfx(π₁)`. Both clauses of the Prefix relation are satisfied, so `pfx(π₁) ≼ a`, hence `a ∈ dom(π₁)`. This is the prefix relation's transitivity, derived directly from the Prefix (PrefixRelation) definition. This covers all nesting cases — both cross-level (a node operator's domain containing an account domain) and same-level (an account holder's domain containing a sub-account domain, as when `pfx(π₁) = [1, 0, 2]` and `pfx(π₂) = [1, 0, 2, 3]` both satisfy O1a with `zeros = 1`).

As a corollary, when the nesting is cross-level — `zeros(pfx(π₁)) < zeros(pfx(π₂))` — the containing principal operates at a strictly higher level of the field hierarchy (node containing account, for instance). But the defining condition is prefix containment alone, not the zero count.


## State Axioms

The transition-discipline axioms below constrain transition-induced changes; the initial state `Σ₀` is governed by O14 (for the principal registry `Π₀`) and by ASN-0040's bootstrap clause B₀ conf. (for the baptismal registry `Σ₀.B`). The constraints O5 (SubdivisionAuthority) and O16 (AllocationClosure) apply to transition-induced allocations only — addresses entering `Σ.B` via a `→` step — and not to bootstrap-seeded addresses, whose well-formedness is the responsibility of ASN-0040.

*Notation.* Throughout this ASN, `Σ.B` denotes the baptismal registry (`Σ.B ⊆ T`) introduced in ASN-0040 — the set of tumblers that have been brought into existence by the baptism procedure. We say "allocated address" and "address in `Σ.B`" interchangeably; from the ownership model's perspective, every address requiring an effective owner is one that the system has baptized. We adopt the foundation's notation rather than introducing a separate `Σ.B` symbol.

*On registry monotonicity.* The monotonicity the proofs below require is baptismal-registry monotonicity `Σ.B ⊆ Σ'.B`, supplied by B0 (Irrevocability) of ASN-0040. This is formally distinct from T8 of ASN-0034, which establishes allocator-domain monotonicity `allocated(s) ⊆ allocated(s')`.

*Reachability convention.* All states `Σ` discussed in this ASN are assumed to be *reachable from the bootstrap state* `Σ₀` — that is, there exists a finite sequence `Σ₀ → Σ_1 → ... → Σ` of state transitions producing `Σ`. The convention licenses iterated application of O12 (PrincipalPersistence) to conclude `Π₀ ⊆ Π_Σ` from a finite-length transition sequence. Each property's formal contract restates the reachability precondition explicitly whenever the proof relies on it; properties whose derivations are entirely state-local (e.g., the AccountField, AccountPrefix, and PrefixDetermination definitions, which constrain a single tumbler or principal without quantifying over transitions) need no reachability hypothesis.

**O12 (PrincipalPersistence).** Once a principal joins Π, no operation removes it:

  `(A Σ, Σ' : Σ → Σ' ⟹ Π_Σ ⊆ Π_{Σ'})`

Nelson's architecture contains no concept of account revocation, and Gregory's codebase contains no deletion path for account entries.

**O13 (PrefixImmutability).** Once established, a principal's ownership prefix cannot be altered:

  `(A π ∈ Π_Σ, Σ, Σ' : Σ → Σ' ∧ π ∈ Π_{Σ'} ⟹ pfx_{Σ'}(π) = pfx_Σ(π))`

The prefix is a tumbler, and the tumbler algebra provides no operation that mutates an existing tumbler in place. Since addresses are permanent (T8) and the prefix is structurally embedded in its domain's addresses, altering it would require rewriting every address in the domain — an operation the system does not support.

**O14 (BootstrapPrincipal).** The initial principal set is non-empty and finite, every initially allocated address is covered by at least one initial principal, every initial principal's prefix is itself initially baptized, and the initial principals satisfy the structural constraints that O1a, O1b, T4, and pairwise non-nesting require of all bootstrap principals:

  `Π₀ ≠ ∅  ∧  (A a ∈ Σ₀.B : (E π ∈ Π₀ : pfx(π) ≼ a))`

  `|Π₀| < ∞`

  `(A π ∈ Π₀ : zeros(pfx(π)) ≤ 1)`

  `(A π₁, π₂ ∈ Π₀ : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

  `(A π ∈ Π₀ : T4(pfx(π)))`

  `(A π₁, π₂ ∈ Π₀ : π₁ ≠ π₂ ⟹ pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁))`

  `(A π ∈ Π₀ : pfx(π) ∈ Σ₀.B)`

The second clause asserts bootstrap finiteness: the system starts with finitely many principals. This is the base case for the finiteness invariant `|Π_Σ| < ∞` (FiniteRegistry, derived below), on which NestingByDelegation's `R_Σ` relies for the existence of a single maximal-length covering principal. The third clause is the base case for O1a: every initial principal has a node-level or account-level prefix. The fourth clause is the base case for O1b: no two initial principals share a prefix. The fifth clause is the base case for T4: every initial principal's prefix is a valid tumbler address. The sixth clause requires pairwise non-nesting: no bootstrap principal's prefix extends another's. Without this, a bootstrapped principal could nest within another's domain — modifying `ω` for addresses in that domain through delegation acts the covering principal never authorized — and the Account-level permanence Corollary would fail. The seventh clause is the base case for O18 (DelegationBaptizes): every bootstrap principal's prefix is itself baptized at `Σ₀`. This is independent of the coverage conjunct of the first clause, which runs in the opposite direction — every initially allocated address is *covered* by some initial principal, which does not imply that each initial principal's *own* prefix is among the initially baptized addresses. The seventh clause closes that gap. Together with the inductive steps — delegation preserves O1a via condition (iv), O1b via the length contradiction (shown below), T4 via condition (v), and O18 via its inductive clause — these clauses establish that O1a, O1b, T4, and O18 hold in every reachable state.

In a single-node system, `Π₀ = {π_N}` where `π_N` is the node operator with a node-level prefix (`zeros = 0 ≤ 1`); non-nesting holds vacuously (a singleton set has no distinct pairs), and all other base-case clauses hold trivially — a single-component positive tumbler like `[1]` satisfies T4 (no zeros, no adjacency or boundary violations). In a multi-node system, `Π₀` contains one initial principal per node (e.g., principals at `[1]` and `[2]`), each independently covering its node's allocatable addresses. These are node-level prefixes (satisfying the third clause), distinct node addresses are distinct tumblers (satisfying the fourth clause by T3), each is a positive single-component tumbler satisfying T4 (satisfying the fifth clause), and no single-component positive tumbler is a prefix of another single-component positive tumbler with a different value (satisfying the sixth clause). The formalization permits both cases: the existential quantifier ranges over all of `Π₀`, not a single distinguished element. Without these base cases, the inductive arguments for O1a, O1b, T4, and O4 cannot begin.

**O15 (PrincipalClosure).** Principals enter Π exclusively through bootstrap (in Π₀) or through a delegation act of an existing principal subject to six structural conditions, named the *delegation predicate* `delegated_Σ(π, π')` (formally defined immediately following the inline statement of the conditions); no other mechanism introduces principals. The conditions are labelled (i)–(vi) so that subsequent proofs may cite them by number. Each state transition introduces at most one new principal, and any newly introduced principal `π'` traces back to a delegating predecessor `π` whose prefix is a strict ancestor of `pfx(π')`:

  `(A Σ, Σ' : Σ → Σ' ⟹ |Π_{Σ'} ∖ Π_Σ| ≤ 1)`

  `(A π' ∈ Π_{Σ'} ∖ Π_Σ : (E π ∈ Π_Σ :`
  `      (i)   pfx(π) ≺ pfx(π')`
  `      (ii)  (A π'' ∈ Π_Σ : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π))`
  `      (iii) π' ∈ Π_{Σ'} ∖ Π_Σ`
  `      (iv)  zeros(pfx(π')) ≤ 1`
  `      (v)   T4(pfx(π'))`
  `      (vi)  ¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π'')) ))`

Condition (iii) — `π' ∈ Π_{Σ'} ∖ Π_Σ`, the delegate is newly introduced — restates the outer binder as an explicit conjunct so the labels are contiguous. The reading of the conjuncts: (i) the delegate's prefix strictly extends the delegator's, (ii) the delegator is the most-specific covering principal of `pfx(π')` in `Π_Σ` (the authorization clause — delegation requires subdivision authority), (iii) the delegate is newly introduced, (iv) the delegate's prefix is at node or account level, (v) the delegate's prefix is a valid tumbler, and (vi) no existing principal already occupies a sub-domain of `pfx(π')` (enforcing top-down delegation order). Nelson's design contains no concept of principals appearing outside the delegation hierarchy, and Gregory's codebase provides no mechanism for it.

**Definition (delegated).** We name the conjunction of conditions (i)–(vi) above the *delegation predicate*, with a four-place signature: `delegated(Σ, Σ', π, π')` holds iff `Σ → Σ'`, `π ∈ Π_Σ`, `π' ∈ Π_{Σ'} ∖ Π_Σ` (condition (iii)), and conditions (i), (ii), (iv), (v), (vi) hold for `(π, π')` at `Σ`. Both transition endpoints are explicit parameters; condition (iii) pins which successor `Σ'` introduces `π'`, so the predicate's meaning never depends on a contextually-supplied successor. Where a formula already binds a transition `Σ → Σ'`, we write `delegated_Σ(π, π')` as an abbreviation for `delegated(Σ, Σ', π, π')` with that same `Σ'`; the subscript form is used only when `Σ'` is named in the surrounding formula. The reflexive-transitive closure `delegated_Σ*` is a separate relation, built from the structural parent relation `R_Σ` on the single state `Σ` defined alongside NestingByDelegation below.

**FiniteRegistry (FiniteRegistry, derived).** In every reachable state, the principal registry is finite:

  `(A Σ : Σ reachable from Σ₀ : |Π_Σ| < ∞)`

We derive this from O14 and O15. *Base case:* By O14, `|Π₀| < ∞`. *Inductive step:* Suppose `|Π_Σ| < ∞` and `Σ → Σ'`. By O15, `|Π_{Σ'} ∖ Π_Σ| ≤ 1`, so `|Π_{Σ'}| ≤ |Π_Σ| + 1`. The sum of a finite cardinal and 1 is finite, hence `|Π_{Σ'}| < ∞`. By induction over the (finite-length) transition sequence `Σ₀ → Σ_1 → ... → Σ`, every reachable state has `|Π_Σ| < ∞`. ∎

The reachability premise itself is structural: states are reached by composing finitely many `→` transitions starting from `Σ₀`. The induction does not require an external "finitely many transitions" axiom — it is induction over the path length, which is by definition a natural number.

**NestingByDelegation (derived).** In every reachable state `Σ`, any two distinct principals are either non-nesting in their prefixes, or one strictly extends the other and the extending principal was introduced into `Π` via a chain of delegations originating at the shorter-prefix principal:

  `(A Σ : Σ reachable from Σ₀ : (A π₁, π₂ ∈ Π_Σ : π₁ ≠ π₂ ⟹`
  `      (pfx(π₁) and pfx(π₂) are non-nesting) ∨`
  `      (pfx(π₁) ≺ pfx(π₂) ∧ delegated_Σ*(π₁, π₂)) ∨`
  `      (pfx(π₂) ≺ pfx(π₁) ∧ delegated_Σ*(π₂, π₁)) ))`

where `delegated_Σ*(π, π')` is the reflexive-transitive closure of a *parent relation* `R_Σ` defined purely on the final state `Σ`, with no reference to a witnessing path. For a non-bootstrap principal `π' ∈ Π_Σ`, let `R_Σ(π, π')` hold iff `π` is the most-specific covering principal of `pfx(π')` in `Π_Σ` — the unique `π ∈ Π_Σ` with `pfx(π) ≺ pfx(π')` of maximal prefix length. This `π` is unique: the covering principals of the common tumbler `pfx(π')` are `≼`-comparable (covering-chain lemma, Ownership Domains section) and have pairwise distinct prefixes (O1b), so their prefix lengths are distinct and a single maximal-length one exists. Then `delegated_Σ* = ∪_{m ≥ 0} R_Σ^m`, where `R_Σ^0` is the identity relation on `Π_Σ` and `R_Σ^{m+1} = R_Σ^m ∘ R_Σ`. Equivalently, `delegated_Σ*(π, π')` iff `π = π'` or there is a finite chain `π = π^{(0)}, π^{(1)}, ..., π^{(m)} = π'` (`m ≥ 1`) of principals in `Π_Σ` with each consecutive pair `(π^{(j)}, π^{(j+1)})` related by `R_Σ`.

This structural `R_Σ` coincides with the introducing-delegation relation, and the coincidence is path-independent. When O15 introduces `π'` at some state `Σ_k`, condition (ii) names its delegator as the most-specific covering principal of `pfx(π')` in `Π_{Σ_k}`. No principal whose prefix lies strictly between `pfx(π)` and `pfx(π')` can enter `Π` after `Σ_k`: such a `π*` would have `pfx(π*) ≺ pfx(π')`, yet at its own introducing state `π'` is already present, so condition (vi) — `¬(E π'' : pfx(π*) ≺ pfx(π''))` — would be violated by `π'' = π'`. Hence the most-specific covering principal of `pfx(π')` is identical in `Π_{Σ_k}` and in the larger `Π_Σ`, so `R_Σ(π, π')` holds for exactly the introducing delegator `π`, independent of which witnessing path reached `Σ`. Equality `pfx(π₁) = pfx(π₂)` is excluded by O1b (preserved across transitions — see below).

We derive this by induction on the transition sequence `Σ₀ → Σ_1 → ... → Σ`.

*Base case:* By O14's sixth clause, all initial principals in `Π_{Σ_0}` have pairwise non-nesting prefixes. So the first disjunct holds directly for every pair `π₁, π₂ ∈ Π_{Σ_0}` with `π₁ ≠ π₂`.

*Inductive step:* Suppose the invariant holds at `Σ_n` and `Σ_n → Σ_{n+1}` via some delegation `delegated_{Σ_n}(π_d, π')` introducing `π'` (by O15, at most one new principal per step; if none is introduced, the invariant is preserved trivially — every disjunct at `Σ_n` lifts to `Σ_{n+1}` by the witness-preservation argument given immediately below). Consider any pair `π₁, π₂ ∈ Π_{Σ_{n+1}}` with `π₁ ≠ π₂`. If both lie in `Π_{Σ_n}`, the IH applies at `Σ_n` and each disjunct lifts to `Σ_{n+1}`. *Witness preservation:* the non-nesting disjunct depends only on the two prefixes, which are preserved across `Σ_n → Σ_{n+1}` by O13 (PrefixImmutability) — `pfx_{Σ_{n+1}}(π_j) = pfx_{Σ_n}(π_j)` for `j ∈ {1, 2}`, since both lie in `Π_{Σ_n}` — so non-nesting at `Σ_n` carries over to `Σ_{n+1}`. The strict-extension disjuncts have the form `delegated_{Σ_n}^*(π_a, π_b)`, a chain of `R_{Σ_n}`-steps; since `R` is monotone — `R_{Σ_n} ⊆ R_{Σ_{n+1}}`, because prefixes are immutable (O13) and (as shown at the definition) the most-specific covering principal of any prefix is preserved as `Π` grows — the same chain witnesses `delegated_{Σ_{n+1}}^*(π_a, π_b)`. Otherwise one of `π₁, π₂` is `π'`; without loss of generality let `π₂ = π'` and `π₁ ∈ Π_{Σ_n}` (`π₁ = π'` would force `π₁ = π₂`). Compare `pfx(π₁)` and `pfx(π')`:

- *Non-nesting:* The first disjunct holds. ✓
- *`pfx(π') ≺ pfx(π₁)`:* Forbidden by condition (vi) of `delegated_Σ` (stated with O15 above), which requires `¬(E π'' ∈ Π_{Σ_n} : pfx(π') ≺ pfx(π''))`. Since `π₁ ∈ Π_{Σ_n}` witnesses such a `π''`, this case is impossible.
- *`pfx(π') = pfx(π₁)`:* Forbidden by condition (ii) of `delegated_{Σ_n}(π_d, π')`. By (ii), `π_d` is the most-specific covering principal of `pfx(π')` in `Π_{Σ_n}`. Taking `π'' = π₁` in (ii): since `pfx(π₁) ≼ pfx(π')` (immediate from `pfx(π') = pfx(π₁)`), we get `#pfx(π₁) ≤ #pfx(π_d)`. But `#pfx(π₁) = #pfx(π')` and by condition (i), `#pfx(π_d) < #pfx(π')`. Combining: `#pfx(π') = #pfx(π₁) ≤ #pfx(π_d) < #pfx(π')` — contradiction. This case is impossible.
- *`pfx(π₁) ≺ pfx(π')`:* We must establish `delegated_{Σ_{n+1}}*(π₁, π')`. By condition (ii), the delegator `π_d` is the most-specific principal in `Π_{Σ_n}` covering `pfx(π')`, so `pfx(π_d) ≼ pfx(π')`. From the hypothesis `pfx(π₁) ≺ pfx(π')`, `π₁` also covers `pfx(π')`. Both `pfx(π_d)` and `pfx(π₁)` are prefixes of the common tumbler `pfx(π')`, so by the covering-chain lemma (Ownership Domains section) they are `≼`-comparable. Three sub-cases exhaust the comparison:
   * *`pfx(π_d) ≺ pfx(π₁)` (strict).* This case is impossible. The strict extension gives `#pfx(π₁) > #pfx(π_d)`, and `π₁ ∈ Π_{Σ_n}` covers `pfx(π')`, contradicting condition (ii) — which requires `#pfx(π'') ≤ #pfx(π_d)` for every `π'' ∈ Π_{Σ_n}` covering `pfx(π')`. Eliminated by the most-specific clause.
   * *`pfx(π_d) = pfx(π₁)`.* By O1b at `Σ_n`, equal prefixes force `π_d = π₁`. The delegation step `delegated_{Σ_n}(π_d, π')` is itself the chain `delegated_{Σ_{n+1}}*(π₁, π')`. ✓
   * *`pfx(π₁) ≺ pfx(π_d)` (strict).* Apply the IH to the pair `(π₁, π_d) ∈ Π_{Σ_n} × Π_{Σ_n}` (distinct by the strict prefix relation, so the IH's hypothesis `π₁ ≠ π_d` is met). Since `pfx(π₁) ≺ pfx(π_d)`, the IH's first disjunct (non-nesting) is excluded; its third disjunct (`pfx(π_d) ≺ pfx(π₁)`) contradicts our strict ordering; so the second disjunct applies, yielding `delegated_{Σ_n}*(π₁, π_d)`. Concatenating with the current step `delegated_{Σ_n}(π_d, π')` produces `delegated_{Σ_{n+1}}*(π₁, π')`. ✓

In every sub-case, one of the three disjuncts holds for `(π₁, π')`. By symmetry, the same holds for `(π', π₂)` when `π₁ = π'`. Induction completes the derivation. ∎

NestingByDelegation makes the structural geometry of `Π_Σ` explicit: principals form a forest under the strict-extension order, with the roots being the bootstrap principals of `Π_{Σ_0}`, and parent-child edges supplied by delegation events. The proofs of O10 (sub-delegate prefix maxima) and OwnershipDomainPermanence★ (sub-delegate inheritance) tacitly rely on this geometry — sub-delegates of a principal `π` are precisely the descendants of `π` in the forest, and any other principal in `Π_Σ` has a non-nesting prefix.

**allocated_by_Σ(π, a) (AllocatedBy).**

We take `allocated_by_Σ(π, a)` — "address `a` was allocated by principal `π` in the transition producing state `Σ`" — as a primitive relation of the ownership model. Its mechanism (the baptism procedure that generates addresses and enters them into `Σ.B`) is out of scope; what the ownership model constrains is its signature and the properties it must satisfy (O5, O16). The signature:

  `allocated_by_Σ : Principal × Tumbler → Bool`

Two constraints bind the relation. O5 (SubdivisionAuthority) requires the allocator to be the most-specific covering principal: if `allocated_by_{Σ'}(π, a)` then `pfx(π) ≼ a` and no `π' ∈ Π_Σ` has a longer prefix covering `a`. O16 (AllocationClosure) requires every newly allocated address to have an allocator: if `a ∈ Σ'.B ∖ Σ.B` then some `π ∈ Π_Σ` satisfies `allocated_by_{Σ'}(π, a)`.

*Axiom:* `allocated_by_Σ(π, a)` is a primitive relation of the ownership model.
- *Signature:* `allocated_by_Σ : Principal × Tumbler → Bool`
- *Semantics:* `allocated_by_{Σ'}(π, a)` holds when the baptism procedure, executing on behalf of `π`, produced `a` during the transition yielding `Σ'`.
- *Constraints:* O5 (SubdivisionAuthority) — allocator is most-specific covering principal; O16 (AllocationClosure) — every new address has an allocator.
- *Mechanism:* Out of scope; belongs to the tumbler baptism specification.

**O5 (SubdivisionAuthority).** Only the principal with the longest matching prefix may allocate new addresses within its domain:

  `(A Σ, Σ', a, π : Σ → Σ' ∧ π ∈ Π_Σ ∧ a ∈ Σ'.B ∖ Σ.B ∧ allocated_by_{Σ'}(π, a)  ⟹  pfx(π) ≼ a  ∧  (A π' ∈ Π_Σ : pfx(π') ≼ a ⟹ #pfx(π') ≤ #pfx(π)))`

This formulation avoids applying `ω` to the prefix itself (which may not yet be in `Σ.B`); instead it directly constrains the allocator to be the most-specific covering principal in `Π_Σ`. The quantifier `a ∈ Σ'.B ∖ Σ.B` restricts O5 to transition-induced allocations: bootstrap-seeded addresses in `Σ₀.B` are governed by ASN-0040's B₀ conf., not by O5.

**O16 (AllocationClosure).** Every address entering `Σ.B` in a state transition was allocated by some principal in `Π_Σ`:

  `(A Σ, Σ', a : Σ → Σ' ∧ a ∈ Σ'.B ∖ Σ.B  ⟹  (E π ∈ Π_Σ : allocated_by_{Σ'}(π, a)))`

This is the address-side counterpart of O15: just as principals enter Π exclusively through bootstrap or delegation, addresses enter `Σ.B` exclusively through allocation by an existing principal. Gregory confirms: every allocation path in udanax-green originates from a session with an account tumbler — there is no mechanism for addresses to appear without an allocating principal.

**O17 (AllocatedAddressValidity, derived).** Every allocated address is a valid tumbler:

  `(A Σ, a : a ∈ Σ.B ⟹ T4(a))`

This is ASN-0040's B10 (T4ValidityInvariant), imported as a load-bearing fact of the ownership model. B10 is established in ASN-0040 as a derived invariant of `Σ.B` from B₀ conf. (the bootstrap clause: every seed element satisfies T4) and B6 (ValidDepth, the precondition of `Bop` ensuring TA5a IncrementPreservesT4 applies). We cite B10 directly rather than reaxiomatize: the foundation produces no addresses outside `Σ.B` satisfying T4. The property is load-bearing because `acct(a)` and `N(a)` depend on T4b (UniqueParse) of ASN-0034, whose well-definedness of `fields(t)` requires T4 validity; without it, O6's proof (via AccountPrefix) and O9's proof (via `N(a)`) have gaps.

**O18 (DelegationBaptizes).** Delegation materially baptizes the delegate's prefix freshly — the transition that introduces a new principal into `Π` enters its prefix into `Σ.B` as a newly registered tumbler, not previously present:

  `(A Σ, Σ', π' : Σ → Σ' ∧ π' ∈ Π_{Σ'} ∖ Π_Σ ⟹ pfx(π') ∈ Σ'.B ∖ Σ.B)`

The base case is supplied by O14's seventh clause (`(A π ∈ Π₀ : pfx(π) ∈ Σ₀.B)`), which establishes the membership conclusion for the bootstrap state (the freshness conjunct has no transition source at bootstrap and is vacuous there). The inductive step is the formula above: when `Σ → Σ'` introduces `π' ∈ Π_{Σ'} ∖ Π_Σ`, the same transition records `pfx(π') ∈ Σ'.B` with the prefix not in `Σ.B` immediately prior. Gregory's `findpreviousisagr` issues every account slot as a fresh entry in the granfilade tree, never re-purposing a previously baptized tumbler as a new principal's prefix.

**PrefixBaptismCoupling (derived).** In every reachable state, every principal's prefix is itself baptized:

  `(A Σ : Σ reachable from Σ₀ : (A π ∈ Π_Σ : pfx(π) ∈ Σ.B))`

We derive this by induction on the transition sequence `Σ₀ → Σ_1 → ... → Σ`.

*Base case.* In the initial state `Σ₀`, the claim is `(A π ∈ Π_{Σ_0} : pfx(π) ∈ Σ_0.B)`. This is O14's seventh clause directly.

*Inductive step.* Assume every `π ∈ Π_{Σ_n}` satisfies `pfx_{Σ_n}(π) ∈ Σ_n.B`, and consider a transition `Σ_n → Σ_{n+1}`. By O15 (PrincipalClosure), every principal in `Π_{Σ_{n+1}}` either was already present in `Π_{Σ_n}` or is the unique newcomer admitted by the delegation conditions (since `|Π_{Σ_{n+1}} ∖ Π_{Σ_n}| ≤ 1`). Let `π ∈ Π_{Σ_{n+1}}` be arbitrary; two cases exhaust its membership.

*Case 1 — `π ∈ Π_{Σ_n}` (carried forward).* By O13 (PrefixImmutability), `pfx_{Σ_{n+1}}(π) = pfx_{Σ_n}(π)`, and the IH gives `pfx_{Σ_n}(π) ∈ Σ_n.B`. By B0 (Irrevocability) of ASN-0040, `Σ_n.B ⊆ Σ_{n+1}.B`, so `pfx_{Σ_{n+1}}(π) ∈ Σ_{n+1}.B`.

*Case 2 — `π ∈ Π_{Σ_{n+1}} ∖ Π_{Σ_n}` (newly introduced).* By O18 (DelegationBaptizes), `pfx(π) ∈ Σ_{n+1}.B` directly.

In both cases, `pfx(π) ∈ Σ_{n+1}.B`. Induction on the transition sequence carries the property to every reachable state. ∎

The named derived property collects the four foundation steps — O14's seventh clause (bootstrap base case), O15 (closure of `Π` by bootstrap or delegation, which makes the case split exhaustive), O18 (the delegation-step inductive case), and B0 of ASN-0040 (Irrevocability, carrying baptized prefixes forward across transitions via `Σ_n.B ⊆ Σ_{n+1}.B`).

*Formal Contract:*
- *Preconditions:* `Σ` reachable from `Σ₀`, `π ∈ Π_Σ`.
- *Postconditions:* `pfx(π) ∈ Σ.B`.
- *Invariant:* Principal registry and baptismal registry are coupled in every reachable state — no principal exists without an allocated prefix.


## The Exclusivity Invariant

Can two principals simultaneously own the same address?

Nelson uses the definite article throughout: "*the* owner of a given item" (LM 4/20), not "an owner." Gregory's predicate returns a boolean — true or false, with no provision for multiple true results from distinct principals. The system requires exactly one effective owner per address.

For non-nesting prefixes, T10 (PartitionIndependence) gives disjointness immediately: two principals whose prefixes satisfy `pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁)` have disjoint domains. The interesting case is nested domains — when a node operator's domain contains an account holder's. Here, Nelson is explicit: the node operator creates accounts, but "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). Delegation permanently transfers effective ownership of the subdomain.

We first state a coverage requirement — every allocated address falls within some principal's domain:

**O4 (DomainCoverage).** For every allocated address in any reachable state, at least one principal's prefix contains it:

  `(A Σ : Σ reachable from Σ₀ : (A a ∈ Σ.B : (E π ∈ Π_Σ : pfx(π) ≼ a)))`

The reachability quantifier is essential: the proof is by induction on the length of the transition sequence leading to `Σ`, and the induction operates along the witnessing path. We prove that in every reachable state `Σ`, every allocated address is covered by at least one principal's prefix.

*Base case.* In the initial state `Σ₀`, the claim is `(A a ∈ Σ₀.B : (E π ∈ Π₀ : pfx(π) ≼ a))`. This is the coverage conjunct of O14's first clause (BootstrapPrincipal), which asserts exactly that the initial principals cover all initially allocated addresses. The base case holds.

*Inductive step.* Assume the claim holds in state `Σ`: every `a ∈ Σ.B` has a covering principal in `Π_Σ`. We must show it holds in any successor state `Σ'` with `Σ → Σ'`. Let `a ∈ Σ'.B` be an arbitrary allocated address. Two cases arise, exhausting `Σ'.B = Σ.B ∪ (Σ'.B ∖ Σ.B)`.

*Case 1: `a ∈ Σ.B` (address was already allocated).* By the inductive hypothesis, there exists `π ∈ Π_Σ` with `pfx(π) ≼ a`. By O12 (PrincipalPersistence), `Π_Σ ⊆ Π_{Σ'}`, so `π ∈ Π_{Σ'}`. By O13 (PrefixImmutability), `pfx_{Σ'}(π) = pfx_Σ(π)`, so the prefix relation `pfx_{Σ'}(π) ≼ a` is preserved. Hence `a` has a covering principal in `Π_{Σ'}`.

*Case 2: `a ∈ Σ'.B ∖ Σ.B` (address is newly allocated).* By O16 (AllocationClosure), there exists a principal `π ∈ Π_Σ` such that `allocated_by_{Σ'}(π, a)` — every newly allocated address was allocated by some existing principal. By O5 (SubdivisionAuthority), whenever `π` allocates `a`, the first conjunct of the postcondition gives `pfx(π) ≼ a` — the allocator's prefix covers the allocated address. By O12, `π ∈ Π_Σ ⊆ Π_{Σ'}`, and by O13, `pfx_{Σ'}(π) = pfx_Σ(π)`. Hence `pfx_{Σ'}(π) ≼ a`, and `a` has a covering principal in `Π_{Σ'}`.

In both cases, every address in `Σ'.B` is covered by a principal in `Π_{Σ'}`. By induction on the transition sequence, the coverage invariant holds in every reachable state. ∎

*Formal Contract:*
- *Preconditions:* `Σ` reachable from `Σ₀`, `a ∈ Σ.B`. The reachability premise is load-bearing: the induction over the transition sequence `Σ₀ → ... → Σ` requires a finite witnessing path, and the inductive step's appeal to O12 (PrincipalPersistence) and O13 (PrefixImmutability) operates along that path. Without reachability, no base case anchors the coverage claim.
- *Postconditions:* `(E π ∈ Π_Σ : pfx(π) ≼ a)`.
- *Invariant:* Coverage holds in every reachable state — no allocated address is orphaned from the principal hierarchy.

We resolve nesting by specificity. Before stating exclusivity we name the principal that wins the contest:

**ω_Σ(a) (EffectiveOwner).** The *effective owner* of an allocated address `a` at a reachable state `Σ` is the principal in `Π_Σ` with the longest matching prefix. Formally, `ω_Σ : Σ.B → Π_Σ` is the partial function defined by:

  `ω_Σ(a) = π  ≡  π ∈ Π_Σ  ∧  pfx(π) ≼ a  ∧  (A π' ∈ Π_Σ : π' ≠ π ∧ pfx(π') ≼ a : #pfx(π) > #pfx(π'))`

The domain restriction `ω_Σ : Σ.B → Π_Σ` is load-bearing: both the address `a` (input) and the selected principal (output) are state-relativized, and the quantifier ranges over the state-relativized principal registry `Π_Σ` rather than a global `Π`. This is a partial definition until we show that the right-hand side picks out exactly one principal in every reachable state. That is the content of O2.

*Notation.* We write bare `ω(a)` and `Π` for `ω_Σ(a)` and `Π_Σ` when the state is fixed by context, supplying the subscript whenever states must be disambiguated.

**O2 (OwnershipExclusivity).** For every reachable state `Σ` and every allocated address `a ∈ Σ.B`, there exists exactly one principal in `Π_Σ` that effectively owns `a` — equivalently, `ω_Σ : Σ.B → Π_Σ` is a total well-defined function:

  `(A Σ reachable, a ∈ Σ.B : (E! π ∈ Π_Σ : ω_Σ(a) = π))`

We prove that for every `a ∈ Σ.B` exactly one principal `π` satisfies the defining equivalence of `ω(a)`. The argument decomposes into four steps: non-emptiness of the covering set, total ordering of covering prefixes, finiteness, and uniqueness of the witnessing principal.

*Step 1: Non-emptiness.* Let `a ∈ Σ.B` and define `C(a) = {π ∈ Π : pfx(π) ≼ a}`, the set of principals whose prefix covers `a`. By O4 (DomainCoverage), every allocated address falls within at least one principal's domain, so `C(a) ≠ ∅`.

*Step 2: Total ordering of covering prefixes.* By the covering-chain lemma (PrefixesOfCommonAddressAreComparable, established above), any two tumbler prefixes of a common address are `≼`-comparable. Applied to `pfx(π₁), pfx(π₂)` for any `π₁, π₂ ∈ C(a)` — both prefixes of the common address `a` — the prefixes are comparable. Since `π₁, π₂` were arbitrary members of `C(a)`, `{pfx(π) : π ∈ C(a)}` is a chain under `≼`.

*Step 3: Finiteness.* Each covering prefix `p ≼ a` is uniquely determined by its length: since `p ≼ a` requires `pᵢ = aᵢ` for all `1 ≤ i ≤ #p`, the prefix of length `k` covering `a` can only be `[a₁, …, a_k]`. By T3 (CanonicalRepresentation), each component `aᵢ` is a uniquely determined natural number, so this prefix is unique. There are at most `#a` possible lengths (from `1` to `#a`), so `|C(a)| ≤ #a`. The covering set is finite.

*Step 4: Existence and uniqueness of the maximum.* A non-empty finite chain has a unique maximum. Therefore there exists a unique maximal length `ℓ* = max{#pfx(π) : π ∈ C(a)}`, and by Step 3 the covering prefix of length `ℓ*` is uniquely determined as `[a₁, …, a_{ℓ*}]`. It remains to show that exactly one principal holds this prefix. Suppose `π₁, π₂ ∈ C(a)` both satisfy `#pfx(π₁) = #pfx(π₂) = ℓ*`. By Step 3, `pfx(π₁) = [a₁, …, a_{ℓ*}] = pfx(π₂)`. By O1b (PrefixInjectivity), equal prefixes imply `π₁ = π₂`. Hence there is exactly one principal `π* ∈ C(a)` achieving the maximal prefix length, and `π*` satisfies the defining equivalence: `pfx(π*) ≼ a` and for every `π' ≠ π*` with `pfx(π') ≼ a`, `#pfx(π*) > #pfx(π')`.

We conclude: for every `a ∈ Σ.B`, there exists exactly one `π ∈ Π` with `ω(a) = π`. Equivalently, `ω : Σ.B → Π` is a total well-defined function in every reachable state. ∎

*Formal Contract:*
- *Definition:* `ω_Σ : Σ.B → Π_Σ` with `ω_Σ(a) = π ≡ π ∈ Π_Σ ∧ pfx(π) ≼ a ∧ (A π' ∈ Π_Σ : π' ≠ π ∧ pfx(π') ≼ a ⟹ #pfx(π) > #pfx(π'))`.
- *Preconditions:* `Σ` reachable from `Σ₀`, `a ∈ Σ.B`. Reachability is inherited from O4 (DomainCoverage), which Step 1 of the proof invokes for non-emptiness of the covering set `C(a)`. Steps 2–4 (chain ordering, finiteness, uniqueness) are state-local and do not introduce additional reachability obligations beyond O4's.
- *Postconditions:* `(E! π ∈ Π_Σ : ω_Σ(a) = π)` — exactly one principal satisfies the defining equivalence.
- *Invariant:* `ω` is a total well-defined function on `Σ.B` in every reachable state.

**SelfOwnershipAtPrefix (derived).** Every principal is the effective owner of its own prefix:

  `(A Σ : Σ reachable from Σ₀ : (A π ∈ Π_Σ : ω_Σ(pfx(π)) = π))`

Let `Σ` be reachable from `Σ₀` and `π ∈ Π_Σ`. By PrefixBaptismCoupling, `pfx(π) ∈ Σ.B`, so `ω_Σ(pfx(π))` is defined (O2 supplies `ω : Σ.B → Π_Σ` as a total function in every reachable state). We show `π` is the unique longest-match principal at `pfx(π)`. Reflexivity of the prefix relation gives `pfx(π) ≼ pfx(π)`, so `π ∈ C(pfx(π))`. For any other `π'' ∈ C(pfx(π))` with `π'' ≠ π`: `pfx(π'') ≼ pfx(π)`, and by O1b (PrefixInjectivity) `π'' ≠ π` forces `pfx(π'') ≠ pfx(π)`. The conjunction `pfx(π'') ≼ pfx(π) ∧ pfx(π'') ≠ pfx(π)` yields the strict prefix `pfx(π'') ≺ pfx(π)`, hence `#pfx(π'') < #pfx(π)`. Therefore `π` achieves the strictly longest match in `C(pfx(π))`. By O2's defining equivalence, `ω_Σ(pfx(π)) = π`. ∎

A concrete instance at the boundary `a₆ = pfx(π_A) = [1, 0, 2]` appears in the *Worked Example* below.

*Formal Contract:*
- *Preconditions:* `Σ` reachable from `Σ₀`, `π ∈ Π_Σ`.
- *Postconditions:* `ω_Σ(pfx(π)) = π`.
- *Invariant:* The boundary of `dom(π)` is structurally inhabited by `π` itself — every principal owns its own delegation point in every reachable state.

The exclusivity of ownership is load-bearing. If two parties owned the same address, the system could not determine who is entitled to subdivide the space beneath it (O5 below), who originated the content (O6 below), or whose delegation created the address. Every downstream property depends on O2.


## Permanence and Refinement

Nelson is emphatic: ownership does not expire.

> "Once assigned a User account, the user will have full control over its subdivision forevermore." (LM 4/29)

"Forevermore" is strong language in a technical specification. But the naive reading — that `ω(a)` never changes — is too strong. Consider a node operator `π₁` with `pfx(π₁) = [1]`. Before any delegation, `ω(a) = π₁` for every address `a` with node field `1`. When `π₁` delegates account prefix `[1, 0, 2]` to principal `π₂`, the effective owner of every address under `[1, 0, 2]` changes from `π₁` to `π₂` — the longer prefix wins. Nelson's "forevermore" does not mean `ω` never changes; it means the *account holder's* sovereignty is permanent — changes to `ω` within an account holder's domain can arise only from the account holder's own delegation acts (see the Corollary below).

The correct invariant is monotonic refinement — `ω(a)` can change only through delegation, and only by becoming more specific:

**O3 (OwnershipRefinement).** The effective owner of an address changes only when delegation introduces a principal with a strictly longer matching prefix. No other transition alters `ω`:

  `(A a ∈ Σ.B, Σ, Σ' : Σ → Σ' ∧ ω_{Σ'}(a) ≠ ω_Σ(a)  ⟹  (E π_d ∈ Π_Σ, π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a)) ∧ delegated_Σ(π_d, π')))`

We prove that every change in effective ownership is witnessed by a new principal with a strictly longer matching prefix, by examining what the effective owner function depends on and what a state transition can alter.

The effective owner `ω_Σ(a)` is defined (O2) as the principal in `Π_Σ` with the longest prefix matching `a`. This definition depends on exactly three inputs: the address `a`, the set of principals `Π_Σ`, and the prefix function `pfx` restricted to `Π_Σ`. We show that a transition `Σ → Σ'` can disturb at most one of these inputs.

*The address is invariant.* By B0 (Irrevocability) of ASN-0040, once `a ∈ Σ.B`, the address `a` persists in the baptismal registry of every subsequent state with unchanged components.

*No existing principal is removed.* By O12 (PrincipalPersistence), `Π_Σ ⊆ Π_{Σ'}`. Every principal present in `Σ` remains present in `Σ'`.

*No existing prefix is altered.* By O13 (PrefixImmutability), for every `π ∈ Π_Σ`, `pfx_{Σ'}(π) = pfx_Σ(π)`. The prefix of every surviving principal is identical across the transition.

These three facts together imply that the set of covering principals from `Π_Σ` is preserved exactly:

  `{π ∈ Π_Σ : pfx_Σ(π) ≼ a} = {π ∈ Π_{Σ'} ∩ Π_Σ : pfx_{Σ'}(π) ≼ a}`

The first equality follows from O12 (`Π_Σ ⊆ Π_{Σ'}`) and O13 (`pfx_{Σ'} = pfx_Σ` on `Π_Σ`). In particular, the longest match among `Π_Σ` — which is `ω_Σ(a)` — remains a covering principal in `Σ'` with the same prefix length.

Now suppose `ω_{Σ'}(a) ≠ ω_Σ(a)`. Since `ω_Σ(a)` is still present in `Π_{Σ'}` with the same prefix (by O12 and O13), and since `ω_Σ(a)` was the longest match in `Π_Σ`, the only way for the longest-match computation over `Π_{Σ'}` to yield a *different* result is for some principal in `Π_{Σ'} ∖ Π_Σ` to cover `a` with a strictly longer prefix. That is, there must exist `π' ∈ Π_{Σ'} ∖ Π_Σ` satisfying both `pfx(π') ≼ a` and `#pfx(π') > #pfx(ω_Σ(a))`.

To see why the new principal's prefix must be *strictly* longer: if `#pfx(π') ≤ #pfx(ω_Σ(a))`, then `ω_Σ(a)` would still be the longest (or tied-longest) match. We rule out the equal-length case `#pfx(π') = #pfx(ω_Σ(a))` explicitly in two lines. *Line 1 — equal-length covering prefixes coincide componentwise with `a`.* By Prefix (PrefixRelation), `pfx(π') ≼ a` gives `pfx(π')ᵢ = aᵢ` for `1 ≤ i ≤ #pfx(π')`, and `pfx(ω_Σ(a)) ≼ a` gives `pfx(ω_Σ(a))ᵢ = aᵢ` for `1 ≤ i ≤ #pfx(ω_Σ(a))`; under the assumed equality `#pfx(π') = #pfx(ω_Σ(a))`, both ranges coincide, so `pfx(π')ᵢ = aᵢ = pfx(ω_Σ(a))ᵢ` for `1 ≤ i ≤ #pfx(π') = #pfx(ω_Σ(a))`. Hence the two prefixes are equal as tumblers: `pfx(π') = pfx(ω_Σ(a))`. *Line 2 — equal prefixes force principal identity, contradicting distinctness.* By O1b (PrefixInjectivity), `pfx(π') = pfx(ω_Σ(a))` forces `π' = ω_Σ(a)`. But `π' ∈ Π_{Σ'} ∖ Π_Σ` (newly introduced) while `ω_Σ(a) ∈ Π_Σ`, contradicting `π' ∉ Π_Σ`. Hence `#pfx(π') = #pfx(ω_Σ(a))` is impossible, and the shorter case `#pfx(π') < #pfx(ω_Σ(a))` leaves `ω_Σ(a)` as the longest match (contradicting `ω_{Σ'}(a) ≠ ω_Σ(a)`). So a new covering principal can only displace `ω_Σ(a)` by being strictly longer.

By O15 (PrincipalClosure), `π' ∈ Π_{Σ'} ∖ Π_Σ` arrived through bootstrap or through delegation. The reachability hypothesis (`Σ` reachable from `Σ₀` — see the reachability convention above) supplies a finite-length transition sequence `Σ₀ → Σ_1 → ... → Σ`; iterated application of O12 (PrincipalPersistence) along that sequence gives `Π₀ ⊆ Π_Σ`. Combined with `π' ∉ Π_Σ`, the bootstrap case is excluded. The remaining clause of O15 supplies an existing principal `π_d ∈ Π_Σ` satisfying conditions (i)–(vi) — that is, `delegated_Σ(π_d, π')` holds. Every change to `ω(a)` is attributable to a specific delegation act in the transition `Σ → Σ'`, witnessed by the pair `(π_d, π')`.

We conclude: `ω_{Σ'}(a) ≠ ω_Σ(a)` implies `(E π_d ∈ Π_Σ, π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a)) ∧ delegated_Σ(π_d, π'))` — the new principal `π'` arrived via a specific delegation act by `π_d`, not by bootstrap. ∎

*Corollary (monotonic refinement).* For every transition `Σ → Σ'` between reachable states and every `a ∈ Σ.B`, `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))`. The precondition `a ∈ Σ.B` ensures `ω_Σ(a)` is defined; the corollary then derives `ω_{Σ'}(a)` is defined via B0 (Irrevocability of ASN-0040), since `Σ.B ⊆ Σ'.B` so `a ∈ Σ'.B`. (The corollary makes no claim about addresses `a ∈ Σ'.B ∖ Σ.B` newly baptized in the transition — for such addresses, `ω_Σ(a)` is undefined and the inequality is ill-formed.) We split on whether the effective owner changes. *Case `ω_{Σ'}(a) = ω_Σ(a)`:* the same principal owns `a` in both states, and by O13 (PrefixImmutability) its prefix is unchanged, so `#pfx(ω_{Σ'}(a)) = #pfx(ω_Σ(a))`. *Case `ω_{Σ'}(a) ≠ ω_Σ(a)`:* by the proof body just established, the new effective owner has a strictly longer prefix, so `#pfx(ω_{Σ'}(a)) > #pfx(ω_Σ(a))`. Both cases yield `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))`. Once a principal `π` becomes the effective owner through longest-match, only a *more specific* delegation can supersede it.

*Formal Contract:*
- *Preconditions:* `Σ` reachable from `Σ₀`, `a ∈ Σ.B`, `Σ → Σ'`, `ω_{Σ'}(a) ≠ ω_Σ(a)`.
- *Postconditions:* `(E π_d ∈ Π_Σ, π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a)) ∧ delegated_Σ(π_d, π'))` — the change is witnessed by both the new principal `π'` (with a strictly longer matching prefix) and the delegator `π_d` (the existing principal whose authority condition (ii) admits `π'`).
- *Invariant:* `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))` for all transitions `Σ → Σ'` between reachable states, *given* `a ∈ Σ.B` (so that both `ω_Σ(a)` and — via B0 of ASN-0040 — `ω_{Σ'}(a)` are defined).

**OwnershipDomainPermanence (Ownership-domain permanence).** No principal external to `dom(π)` can alter effective ownership within `dom(π)`. The property holds at every principal level — node, account, and sub-account along delegation chains — and quantifies over arbitrary `π ∈ Π_Σ`; the historically motivating instance is the account-level case (Nelson's "forevermore"), but the formal statement is general. Changes to `ω(a)` for addresses in a principal's domain arise only from that principal's own delegation acts or from delegation acts of its sub-delegates:

  `(A π ∈ Π_Σ, Σ, Σ' : Σ → Σ' ∧ (E a ∈ dom(π) ∩ Σ.B : ω_{Σ'}(a) ≠ ω_Σ(a))  ⟹  (E π_d ∈ Π_Σ : pfx(π) ≼ pfx(π_d) ∧ (E π' ∈ Π_{Σ'} ∖ Π_Σ : delegated_Σ(π_d, π'))))`

That is: if any address in `dom(π)` changes effective owner across a single transition, the delegator `π_d` responsible for that transition has a prefix extending `pfx(π)` — the delegator is `π` itself or a principal whose prefix `π` covers (in informal language, `π_d` is `π` or a sub-delegate of `π`).

We prove this directly for a single transition `Σ → Σ'`. The formal statement quantifies over one transition; we make no induction on transition count. Multi-step closure — that the chain of delegators introducing principals into `dom(π)` traces back to `π` — follows by repeated application of the single-transition result and is discussed informally below.

Assume `Σ` reachable from `Σ₀`, `π ∈ Π_Σ`, `a ∈ dom(π) ∩ Σ.B`, `Σ → Σ'`, and `ω_{Σ'}(a) ≠ ω_Σ(a)`.

*Step 1 — a new principal with a strictly longer matching prefix witnesses the change.* By O3 (OwnershipRefinement) (whose reachability precondition is satisfied by the present hypothesis), `ω_{Σ'}(a) ≠ ω_Σ(a)` implies the existence of `π' ∈ Π_{Σ'} ∖ Π_Σ` with `pfx(π') ≼ a` and `#pfx(π') > #pfx(ω_Σ(a))`. By O15 (PrincipalClosure), `π'` entered `Π` either through bootstrap (`π' ∈ Π₀`) or through delegation. By the reachability hypothesis, there is a finite-length transition sequence `Σ₀ → Σ_1 → ... → Σ`; iterated application of O12 (PrincipalPersistence) along that sequence gives `Π₀ ⊆ Π_Σ`. Combined with `π' ∉ Π_Σ`, this excludes `π' ∈ Π₀`, ruling out the bootstrap case. The remaining clause of O15 applies: there exists `π_d ∈ Π_Σ` with `delegated_Σ(π_d, π')`.

*Step 2 — the new principal's prefix strictly extends `pfx(π)`.* Since `a ∈ dom(π)`, we have `pfx(π) ≼ a`. The chain `#pfx(π') > #pfx(ω_Σ(a)) ≥ #pfx(π)` holds: the second inequality follows because `π ∈ Π_Σ` covers `a`, and `ω_Σ(a)` is by O2 the longest-prefix covering principal in `Π_Σ`. Hence `#pfx(π') > #pfx(π)`. Both `pfx(π)` and `pfx(π')` are prefixes of `a`. From the definition of the prefix relation — `p ≼ a` iff `#a ≥ #p ∧ (A i : 1 ≤ i ≤ #p : pᵢ = aᵢ)` — we have `pfx(π)ᵢ = aᵢ` for `1 ≤ i ≤ #pfx(π)` and `pfx(π')ᵢ = aᵢ` for `1 ≤ i ≤ #pfx(π')`. Taking WLOG the shorter `#pfx(π)` ≤ `#pfx(π')` (established above), for each `i ≤ #pfx(π)` both equalities give `pfx(π)ᵢ = aᵢ = pfx(π')ᵢ`. Hence `pfx(π) ≼ pfx(π')` by the same definition. Combined with the strict length inequality, `pfx(π) ≺ pfx(π')`.

*Step 3 — the delegator's prefix extends `pfx(π)`.* By condition (i) of the `delegated` relation, `pfx(π_d) ≺ pfx(π')`. By condition (ii), `π_d` is the most-specific covering principal of `pfx(π')` in `Π_Σ`: `(A π'' ∈ Π_Σ : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π_d))`. From Step 2, `pfx(π) ≼ pfx(π')` and `π ∈ Π_Σ`, so taking `π'' = π` gives `#pfx(π) ≤ #pfx(π_d)`. Both `pfx(π)` and `pfx(π_d)` are prefixes of `pfx(π')` (the former by Step 2; the latter by condition (i)). Applying the definition of `≼` to `pfx(π')` as the common extending tumbler: `pfx(π)ᵢ = pfx(π')ᵢ` for `1 ≤ i ≤ #pfx(π)` and `pfx(π_d)ᵢ = pfx(π')ᵢ` for `1 ≤ i ≤ #pfx(π_d)`. For each `i ≤ #pfx(π)` (which is `≤ #pfx(π_d)`) both equalities hold, giving `pfx(π)ᵢ = pfx(π_d)ᵢ`. Hence `pfx(π) ≼ pfx(π_d)`.

Steps 1–3 establish the postcondition for a single transition: `(E π_d ∈ Π_Σ : pfx(π) ≼ pfx(π_d) ∧ (E π' ∈ Π_{Σ'} ∖ Π_Σ : delegated_Σ(π_d, π')))`. ∎

**Corollary (OwnershipDomainPermanence★, multi-step).** The single-transition property extends to the transitive closure `Σ →⁺ Σ'`: every change to `ω(a)` for `a ∈ dom(π) ∩ Σ.B` along any reachable transition sequence is induced by delegators whose prefixes all extend `pfx(π)`. Let `Σ →⁺ Σ'` abbreviate `Σ → Σ_1 → ... → Σ_n = Σ'` for some `n ≥ 1`:

  `(A π ∈ Π_Σ, Σ, Σ', a : Σ reachable from Σ₀ ∧ Σ →⁺ Σ' ∧ a ∈ dom(π) ∩ Σ.B  ⟹  (A i, 0 ≤ i < n : ω_{Σ_{i+1}}(a) ≠ ω_{Σ_i}(a) ⟹ (E π_d^{(i)} ∈ Π_{Σ_i}, π'^{(i)} ∈ Π_{Σ_{i+1}} ∖ Π_{Σ_i} : pfx(π) ≼ pfx(π_d^{(i)}) ∧ delegated_{Σ_i}(π_d^{(i)}, π'^{(i)}))))`

We prove this by induction on the path length `n`. The reachability of each intermediate `Σ_i` is automatic: `Σ` is reachable from `Σ₀` by hypothesis, and `Σ →⁺ Σ_i` extends the witnessing sequence — composition of finite transition sequences yields a finite transition sequence — so `Σ_i` is reachable from `Σ₀` for every `0 ≤ i ≤ n`. *Base case `n = 1`:* The hypothesis reduces to a single transition `Σ → Σ'`; the single-transition OwnershipDomainPermanence applies directly (its reachability precondition is the present hypothesis), yielding the required `π_d^{(0)}` with `pfx(π) ≼ pfx(π_d^{(0)})` whenever `ω(a)` changes.

*Inductive step.* Assume the corollary holds for sequences of length `n`; consider a sequence of length `n + 1`: `Σ → Σ_1 → ... → Σ_n → Σ_{n+1}`. By the induction hypothesis applied to the prefix `Σ →⁺ Σ_n`, the chain conclusion holds for every transition with index `0 ≤ i < n` along that prefix. It remains to handle the final transition `Σ_n → Σ_{n+1}`. The single-transition OwnershipDomainPermanence applies provided `Σ_n` reachable from `Σ₀` (discharged above) and `a ∈ dom(π) ∩ Σ_n.B` — we discharge the latter from the original hypotheses. The persistence of `a` follows from B0★ (MultiStepIrrevocability) of ASN-0040 applied along the path `Σ →⁺ Σ_n`: `a ∈ Σ.B ⊆ Σ_n.B` since the baptismal registry is monotone under the reflexive-transitive closure of `→`. The persistence of `π ∈ Π_{Σ_n}` follows from iterated O12: `Π_Σ ⊆ Π_{Σ_1} ⊆ ... ⊆ Π_{Σ_n}`, so `π ∈ Π_{Σ_n}`. The persistence of `a ∈ dom(π)` is structural — `dom(π) = {a : pfx(π) ≼ a}` depends only on `pfx(π)` and `a`, both of which are fixed as values (O13 immutability for the prefix; tumbler addresses are immutable values in `Σ.B` under B0 of ASN-0040). With premises discharged, the single-transition statement yields the required `π_d^{(n)}` with `pfx(π) ≼ pfx(π_d^{(n)})` whenever `ω_{Σ_{n+1}}(a) ≠ ω_{Σ_n}(a)`. Combined with the inductive conclusion for the earlier transitions, the chain conclusion holds for all `0 ≤ i ≤ n`. ∎

The corollary's content is Nelson's "forevermore": every delegator that participates in a chain of changes to `ω(a)` within `dom(π)` has a prefix extending `pfx(π)`, so the chain always begins with `π`'s own delegation act and no delegator outside `dom(π)` can induce a change. When `π` has not yet exercised delegation authority at `Σ` — for instance, the state at which `π` itself was introduced — NestingByDelegation places every link of the inducing chain strictly between `Σ` and the state of the change (each intermediate principal strictly extends `pfx(π)` by condition (i), so by O12 monotonicity it is introduced only after `Σ`).

Nelson confirms: "User 3 controls allocation of children directly under 3. User 3.2 controls everything under 3.2. User 3 cannot modify User 3.2's documents" (consultation, LM 4/20, 4/29, 2/29). The parent controls baptism; the child controls content. Changes to `ω` within `dom(π)` arise only from `π`'s own delegation choices, or recursively from sub-delegates' choices within their own sub-domains. This is Nelson's "forevermore": not that `ω` is static within `dom(π)`, but that no external act can alter it. The addresses `π` has not sub-delegated remain permanently under `π`'s effective ownership.

This raises a tension that Nelson himself acknowledges. He mentions "someone who has bought the document rights" (LM 2/29), implying ownership can *transfer*. But the address permanently encodes the originating account (by O6 and T8), and Gregory's codebase contains no transfer mechanism whatsoever — no FEBE command, no data structure, no protocol step. We take the conservative reading: O3 describes the refinement regime for the system as specified. Transfer, if it exists, would require machinery that overrides the address-derived ownership — a registry external to the address structure — and Nelson leaves such machinery unspecified. The address is a birth certificate; a transfer would require a separate deed. We record this as an open question.

*Formal Contract:*
- *Preconditions:* `Σ` reachable from `Σ₀`, `π ∈ Π_Σ`, `a ∈ dom(π) ∩ Σ.B`, `Σ → Σ'`, `ω_{Σ'}(a) ≠ ω_Σ(a)`.
- *Postconditions:* `(E π_d ∈ Π_Σ : pfx(π) ≼ pfx(π_d) ∧ (E π' ∈ Π_{Σ'} ∖ Π_Σ : delegated_Σ(π_d, π')))` — the responsible delegator `π_d` and the newly introduced principal `π'` are both witnessed existentially; the new principal is the cause of the ownership change.
- *Invariant:* Effective ownership within `dom(π)` is sovereign — no delegation by a principal external to `dom(π)` can alter `ω(a)` for any `a ∈ dom(π)`.


## Worked Example

We verify the properties against a concrete scenario. Let principals `π_N` and `π_M` be node operators with `pfx(π_N) = [1]` (`zeros = 0`) and `pfx(π_M) = [2]` (`zeros = 0`) — two independent nodes in a multi-node system. Initially, `Π₀ = {π_N, π_M}`.

*Convention.* Subscript labels `Σ_0, Σ_1, Σ_2, …` denote trajectory milestones, not single transitions; each segment may comprise multiple `Bop` calls whose cumulative `Σ.B` is recorded at the next milestone (order-immaterial by B0 Irrevocability of ASN-0040).

We check that O14's bootstrap clauses are satisfied: `Π₀ ≠ ∅`; each `pfx` has `zeros ≤ 1` (both have `zeros = 0`); `pfx` is injective on `Π₀` (`[1] ≠ [2]`); each prefix satisfies T4 (HierarchicalParsing — single positive component, zero-count `0 ≤ 3`) and T4a (SyntacticEquivalence — no adjacent zeros, no leading or trailing zero — vacuously, since there are no zeros); the pair is non-nesting (`[1] ⋠ [2]` and `[2] ⋠ [1]`, since component 1 differs); and each principal's prefix lies in `Σ₀.B` (we assume the bootstrap state was seeded with `[1], [2] ∈ Σ₀.B`, satisfying O14's seventh clause; additional seeds required for downstream B1 obligations are tabulated below). `|Π₀| = 2 < ∞`. ✓

**Bootstrap seeds.** `Σ_0`'s baptismal registry is a single bootstrap snapshot whose well-formedness (B1 contiguity, B6 depth) is ASN-0040's responsibility. From the ownership perspective only two facts matter: which addresses are in `Σ_0.B`, and who covers them. Beyond `[1], [2]` (O14's seventh clause), we seed four positions, all covered by `π_N` (since `[1] ≼ ·` and `[2] ⋠ ·` for each):

| Seed | Coverage in `Π_0` |
|------|-------------------|
| `[1, 0, 1]` | `π_N` |
| `[1, 0, 2, 0, 1], [1, 0, 2, 0, 2], [1, 0, 2, 0, 3]` | `π_N` |
| `a_1 = [1, 0, 2, 0, 3, 0, 1]` | `π_N` |
| `a_3 = [1, 0, 7, 0, 1, 0, 1]` | `π_N` |

The delegated prefix `[1, 0, 2]` is deliberately *not* seeded — it is baptized at the delegation transition below, satisfying O18's freshness conjunct.

**State Σ₀.** `π_N` and `π_M` are the bootstrap principals. For any address `a` with node field `1`, `ω(a) = π_N` (the only matching prefix in `Π₀`); for any address `a` with node field `2`, `ω(a) = π_M`. O2 holds — each address has a single longest match. O4 holds for any address under either node.

**Delegation.** `π_N` delegates account prefix `[1, 0, 2]` to new principal `π_A`. Now `Π_{Σ₁} = {π_N, π_M, π_A}`.

*Verifying the conditions of `delegated_{Σ₀}(π_N, π_A)`:*

- **(i)** `pfx(π_N) ≺ pfx(π_A)`: `[1] ≺ [1, 0, 2]` — the delegate's prefix strictly extends the delegator's (length 1 vs 3, components match). ✓
- **(ii)** `π_N` is the most-specific covering principal for `[1, 0, 2]` in `Π_{Σ₀}`: the candidates whose prefix covers `[1, 0, 2]` are those `π''` with `pfx(π'') ≼ [1, 0, 2]`. Of `{π_N, π_M}`, only `π_N` (with `[1] ≼ [1, 0, 2]`) covers; `π_M`'s prefix `[2]` does not. So `π_N` is the unique — and hence most-specific — covering principal. ✓
- **(iii)** `π_A ∈ Π_{Σ₁} ∖ Π_{Σ₀}`: newly introduced. ✓
- **(iv)** `zeros(pfx(π_A)) = 1 ≤ 1`: account-level prefix. ✓
- **(v)** `T4(pfx(π_A))`: `[1, 0, 2]` has one zero (not adjacent to any other zero), positive components flanking the zero, no leading/trailing zero — every present field (node `[1]`, user `[2]`) non-empty. ✓
- **(vi)** `¬(E π'' ∈ Π_{Σ₀} : pfx(π_A) ≺ pfx(π''))`: the only principals are `π_N` (prefix `[1]`, shorter than `[1, 0, 2]`, cannot be strict extension) and `π_M` (prefix `[2]`, not even a covering relation). No existing principal has a prefix strictly extending `[1, 0, 2]`. ✓

*Verifying O7's postconditions for `π_A`:*

- **O7(a)**: For every `a ∈ dom(π_A) ∩ Σ₁.B`, `ω_{Σ₁}(a) = π_A`. Any such `a` has `pfx(π_A) = [1, 0, 2] ≼ a`. Pre-existing covering principals from `Π_{Σ₀}`: only `π_N` (since `π_M`'s `[2]` cannot cover an address starting with `1`), and `#pfx(π_N) = 1 < 3 = #pfx(π_A)`. By O2, `ω_{Σ₁}(a) = π_A`. ✓
- **O7(b)**: `π_A` may allocate within `dom(π_A)` per O5. The most-specific covering check now ranges over `Π_{Σ₁}`; for `a` strictly extending `[1, 0, 2]`, `π_A` is the unique principal with longest matching prefix. ✓
- **O7(c)**: `π_A` may further delegate sub-prefixes such as `[1, 0, 2, 3]` to a new principal `π_B`; conditions (i)–(vi) of the delegation relation become satisfiable with `π_A` in the role of delegator. (This sub-delegation is exercised in *Verifying O8* below.) ✓

**State Σ₁.** The address `a₁ = [1, 0, 2, 0, 3, 0, 1]` (a document element under account `[1, 0, 2]`) is seeded in `Σ_0.B` under `π_N`'s coverage per the bootstrap snapshot table above — `a₁` enters the baptismal registry at genesis with no preceding transition, and `π_N` is its most-specific covering principal in `Π_0` (since only `pfx(π_N) = [1] ≼ a₁`, and `pfx(π_M) = [2] ⋠ a₁`). Bootstrap seeding is a property of `Σ_0` itself, not the product of an allocation by `π_N`; we therefore reserve the verb "allocate" for transition-induced entries (the post-`Σ_0` baptisms enumerated in the *Trajectory* paragraph below) and use "seed" / "is in `Σ_0.B`" / "under `π_N`'s coverage" for the genesis-state contents recorded in the bootstrap snapshot. Following the delegation `delegated_{Σ_0}(π_N, π_A)` introducing `π_A` with `pfx(π_A) = [1, 0, 2]`, both principals' prefixes cover `a₁`: `[1] ≼ a₁` and `[1, 0, 2] ≼ a₁`. The longer match is `[1, 0, 2]`, so `ω_{Σ_1}(a₁) = π_A`. We verify:

- **O0**: `owns(π_A, a₁)` is decidable from `pfx(π_A) = [1, 0, 2]` and `a₁ = [1, 0, 2, 0, 3, 0, 1]` alone. ✓
- **O1**: `pfx(π_A) ≼ a₁` — the first three components match. ✓
- **O1a**: `zeros(pfx(π_A)) = 1 ≤ 1`. ✓
- **O1b**: `pfx(π_N) = [1] ≠ [1, 0, 2] = pfx(π_A)`, so injectivity holds. ✓
- **O2**: `ω(a₁) = π_A` — unique longest match. `π_N` also matches but `#[1, 0, 2] > #[1]`. ✓
- **O3 (refinement)**: In the transition `Σ₀ → Σ₁`, `ω(a₁)` changed from `π_N` to `π_A`. O3's postcondition exhibits both delegator and delegate witnesses for the change. *Delegator witness:* `π_d = π_N ∈ Π_{Σ₀}` — the existing principal whose condition (ii) authorization admits the new delegate, satisfying `delegated_{Σ₀}(π_N, π_A)` as verified in *Verifying the conditions of `delegated_{Σ₀}(π_N, π_A)`* above. *Delegate witness:* `π' = π_A ∈ Π_{Σ₁} ∖ Π_{Σ₀}` with `pfx(π_A) ≼ a₁` and `#pfx(π_A) = 3 > 1 = #pfx(π_N) = #pfx(ω_{Σ₀}(a₁))`. The pair `(π_d, π') = (π_N, π_A)` discharges O3's postcondition `(E π_d ∈ Π_Σ, π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a)) ∧ delegated_Σ(π_d, π'))`. ✓
- **O4**: `pfx(π_N) ≼ a₁` provides coverage. ✓

**Allocation.** `π_A` allocates element address `a₂ = [1, 0, 2, 0, 5, 0, 1]`. This is sub-account allocation — no new principal is created. `Π` is unchanged.

- **O5**: `pfx(π_A) = [1, 0, 2] ≼ a₂` and `π_A` has the longest matching prefix — the allocator is the most-specific covering principal. ✓
- **O6**: `acct(a₂) = [1, 0, 2] = pfx(π_A)` — the account field directly names the effective owner (equality case). ✓

**Concrete witness for SelfOwnershipAtPrefix.** By PrefixBaptismCoupling, `pfx(π_A) = [1, 0, 2] ∈ Σ_1.B`. We verify SelfOwnershipAtPrefix at the concrete boundary `a₆ = pfx(π_A) = [1, 0, 2]`. The covering set is `C(a₆) = {π ∈ Π_{Σ_1} : pfx(π) ≼ [1, 0, 2]}`. Candidates: `π_N` (prefix `[1]`, `[1] ≼ [1, 0, 2]` since the first component matches and `#[1] ≤ #[1, 0, 2]`), `π_M` (prefix `[2]`, fails: `2 ≠ 1`), `π_A` (prefix `[1, 0, 2]`, `[1, 0, 2] ≼ [1, 0, 2]` reflexively — every component matches and lengths are equal). So `C(a₆) = {π_N, π_A}` with prefix lengths `1` and `3`. The longest match is `π_A`, hence `ω(a₆) = π_A`. ✓

**Sub-account namespaces.** Between `π_A`'s introduction at `Σ_1` and the delegation of `[1, 0, 2, 3]` to `π_B` below, `π_A` baptizes two sub-account positions `[1, 0, 2, 1]` and `[1, 0, 2, 2]` as organizational namespaces — addresses entered into `Σ.B` without introducing new principals. By O5, `π_A` is the most-specific covering principal of each and is authorized as allocator; by O15, namespace baptism admits no new principal, so `Π` is unchanged. Their well-formedness (B6 depth, B1 contiguity within `S([1, 0, 2], 1)`) holds by ASN-0040; we record only the ownership-relevant outcome `Σ_2.B ⊇ {[1, 0, 2, 1], [1, 0, 2, 2], a_2}`, which also supplies ASN-0040's B1 prerequisite for baptizing `[1, 0, 2, 3]` at the later delegation.

We verify the ownership properties under one of the namespaces. Address `a₄ = [1, 0, 2, 1, 0, 1, 0, 1]` is a document element under `[1, 0, 2, 1]`:

- **O2**: Both `pfx(π_N) = [1] ≼ a₄` and `pfx(π_A) = [1, 0, 2] ≼ a₄`. Longest match: `ω(a₄) = π_A`. ✓
- **O6**: `acct(a₄) = [1, 0, 2, 1]` and `pfx(ω(a₄)) = [1, 0, 2]`. The containment `pfx(ω(a₄)) ≼ acct(a₄)` holds but equality does not — the account field extends beyond the owner's prefix because `[1, 0, 2, 1]` has not been delegated. The provenance invariant holds: any address with `acct = [1, 0, 2, 1]` has effective owner `π_A`. ✓
- **O5**: Only `π_A` may allocate within either namespace sub-account — the most-specific covering principal. ✓

O18 (DelegationBaptizes) makes each namespace baptism a permanent commitment: since `[1, 0, 2, 1], [1, 0, 2, 2] ∈ Σ_2.B`, no future delegation transition can use either as a new principal's prefix — delegated prefixes must be drawn from `Σ'.B ∖ Σ.B`, but these slots are now occupied. Namespace baptism and principal baptism are mutually exclusive futures for the same prefix, so provenance under `acct = [1, 0, 2, 1]` (and likewise `[1, 0, 2, 2]`) remains `π_A` forever. The next available slot in the stream, `[1, 0, 2, 3] = c_3`, is correspondingly free for either continuation; the running trajectory takes the *delegation* branch in *Verifying O8* below, baptizing `[1, 0, 2, 3]` as `pfx(π_B)` at `Σ_2 → Σ_3`, where the freshness conjunct of O18 is satisfied because `[1, 0, 2, 3] ∉ Σ_2.B`. (Symmetrically, had `π_A` instead chosen to baptize `[1, 0, 2, 3]` as a third namespace, O18 would foreclose any later delegation of `[1, 0, 2, 3]`, and `π_A` would advance to `c_4 = [1, 0, 2, 4]` to introduce a new principal. The two branches are mutually exclusive: the worked example pursues the delegation branch from here on.)

**Account-level permanence.** By condition (ii) of the delegation relation, only `π_A` (the most-specific covering principal for any prefix extending `[1, 0, 2]` in `Π_{Σ_1}`) can delegate sub-accounts extending `[1, 0, 2]`. The node operator `π_N` cannot introduce such a principal — `π_N`'s effective ownership of addresses under `[1, 0, 2]` was superseded when `π_A` was delegated. Addresses `a₁` and `a₂` will remain under `ω = π_A` unless `π_A` itself delegates a sub-account covering them. If `π_A` were to delegate sub-account `[1, 0, 2, 3]` to `π_B`, addresses extending `[1, 0, 2, 3, ...]` would have `ω = π_B` — but addresses `a₁ = [1, 0, 2, 0, ...]` and `a₂ = [1, 0, 2, 0, ...]` are not in `dom(π_B)` (the fourth component `0 ≠ 3`), so they remain under `π_A`. Nelson's "forevermore": sovereignty against external interference.

*Verifying O8 (Irrevocability) for `π_N` over `a₁` across multiple states.* The delegation `delegated_{Σ₀}(π_N, π_A)` introduces `π_A` in state Σ₁ with `pfx(π_A) = [1, 0, 2]`, and `a₁ = [1, 0, 2, 0, 3, 0, 1] ∈ dom(π_A) ∩ Σ₁.B`. O8's postcondition requires `ω_{Σ'}(a₁) ≠ π_N` for every `Σ'` with `Σ₀ →⁺ Σ'`. We trace three successor states:
- *Σ₁ (immediately post-delegation):* the covering principals for `a₁` in `Π_{Σ₁} = {π_N, π_M, π_A}` are `π_N` (prefix `[1]`, length 1) and `π_A` (prefix `[1, 0, 2]`, length 3); `π_M`'s `[2]` does not cover. Longest match: `ω_{Σ₁}(a₁) = π_A ≠ π_N`. ✓
- *Σ₂ (after `π_A` allocates `a₂`):* allocation does not change `Π` or any prefix. The covering set and longest match are unchanged: `ω_{Σ₂}(a₁) = π_A ≠ π_N`. ✓
- *Σ₃ (after `π_A` delegates sub-account `[1, 0, 2, 3]` to `π_B`):* `Π_{Σ₃} = {π_N, π_M, π_A, π_B}`. The address `a₁ = [1, 0, 2, 0, 3, 0, 1]` has fourth component `0`, but `pfx(π_B) = [1, 0, 2, 3]` has fourth component `3`, so `pfx(π_B) ⋠ a₁`; `π_B` does not cover. The longest match for `a₁` remains `π_A`. `ω_{Σ₃}(a₁) = π_A ≠ π_N`. ✓

The mechanism is exactly what the proof of O8 articulates: `π_N`'s prefix `[1]` has length 1, `π_A`'s prefix has length 3, and by O13 (PrefixImmutability) neither length changes across transitions. Any state with `π_A` in `Π` exhibits a covering principal strictly longer than `π_N`'s prefix, so `π_N` cannot achieve the longest match. The irrevocability persists even when `π_A` sub-delegates: address `a₁` migrates only to principals with prefixes strictly extending `[1, 0, 2]`, which are themselves strictly longer than `π_N`'s `[1]`. Effective ownership refines downward; it never returns up the tree.

*Verifying O9 (Node-locality) across nodes.* Consider address `a₅ = [2, 0, 1, 0, 1, 0, 1]` — node `[2]`, user `[1]`, document `[1]`, element `[1]`. We check O9 (`owns(π, a) ⟹ N(pfx(π)) ≼ N(a)`) for each principal in `Π_{Σ₁}` and confirm consistency with the longest-match outcome:
- `π_M` (`pfx(π_M) = [2]`, `N(pfx(π_M)) = [2]`): `pfx(π_M) ≼ a₅` (first component `2 = 2`), so `owns(π_M, a₅)` holds. `N(a₅) = [2]` and `N(pfx(π_M)) = [2] ≼ [2]`. ✓
- `π_N` (`pfx(π_N) = [1]`, `N(pfx(π_N)) = [1]`): the prefix condition `pfx(π_N) ≼ a₅` requires `(a₅)₁ = 1`, but `(a₅)₁ = 2`. So `owns(π_N, a₅)` is false. O9 is vacuously satisfied. We further note that even if one tried to force `N(pfx(π_N)) = [1] ≼ N(a₅) = [2]`, the relation fails: `1 ≠ 2`. The structural barrier is in the node field itself — no account-level principal under node `[1]` can ever own an address under node `[2]`.
- `π_A` (`pfx(π_A) = [1, 0, 2]`, `N(pfx(π_A)) = [1]`): `pfx(π_A) ≼ a₅` requires `(a₅)₁ = 1`, false. `owns(π_A, a₅)` is false; O9 vacuous.

Longest match: only `π_M` covers `a₅`. `ω(a₅) = π_M`. The node operator for node `[2]` exclusively governs all addresses under that node — `π_N` and `π_A`, both rooted at node `[1]`, are structurally barred from owning any address whose node field is `[2]`. This is O9 in operation: ownership authority cannot cross the node boundary because the first field of any address syntactically anchors which node-rooted principals can cover it.

Now consider a sub-delegation under `π_M`: suppose `π_M` later delegates account prefix `[2, 0, 1]` to `π_C`. Address `a₅` has account field `[2, 0, 1]`; after this delegation, `ω(a₅) = π_C` (longer match). For O9: `N(pfx(π_C)) = [2] ≼ N(a₅) = [2]`. ✓ A principal under node `[2]` may govern addresses under node `[2]`, but the node-boundary remains rigid — no chain of delegations originating from `π_N` (node `[1]`) can ever introduce a principal whose prefix crosses into node `[2]`, because delegation condition (i) requires `pfx(π) ≺ pfx(π')`, which preserves the first component.

Now consider address `a₃ = [1, 0, 7, 0, 1, 0, 1]` under a different account. `pfx(π_A) = [1, 0, 2] ⋠ a₃` (component 3: `2 ≠ 7`). Only `pfx(π_N) = [1] ≼ a₃`, so `ω(a₃) = π_N`. The node operator retains effective ownership of all addresses not covered by a delegated account.

**Fork (O10).** Suppose `π_A` wishes to modify the content at `a₃ = [1, 0, 7, 0, 1, 0, 1]`. Since `ω(a₃) = π_N ≠ π_A`, the system does not grant modification. Instead, `π_A` creates a fork: a new document-level address `a' = [1, 0, 2, 0, 6]` within `dom(π_A)`. We trace the single-baptism trajectory and verify O10's conditions.

*Trajectory.* `π_A` has `pfx(π_A) = [1, 0, 2]` with `zeros = 1`. The pre-fork state `Σ_pre := Σ_2` is reached from `Σ_0` by the *Delegation* and *Allocation* segments above; `π_A` (the most-specific covering principal of `[1, 0, 2]`, O5-authorized) additionally baptizes `[1, 0, 2, 0, 4]` and `[1, 0, 2, 0, 5]` in the document stream `S([1, 0, 2], 2)`. Each baptism's well-formedness (B6 depth, B1 contiguity) holds by ASN-0040. The ownership-relevant outcome is the cumulative registry `Σ_2.B ⊇ Σ_0.B ∪ {[1, 0, 2], [1, 0, 2, 0, 4], [1, 0, 2, 0, 5], a_2, [1, 0, 2, 1], [1, 0, 2, 2]}`, so `children(Σ_pre.B, [1, 0, 2], 2) = {[1, 0, 2, 0, k] : 1 ≤ k ≤ 5}` and `hwm(Σ_pre.B, [1, 0, 2], 2) = 5`.

The single baptism: `b_1 = next(Σ_pre.B, [1, 0, 2], 2) = [1, 0, 2, 0, 6]` (sibling-advance branch, `hwm = 5 > 0`; well-formedness by ASN-0040 B6). This is a document-level address with `zeros = 2`. *O5 check at `Σ_pre`:* the most-specific covering principal of `[1, 0, 2, 0, 6]` in `Π_{Σ_pre} = {π_N, π_M, π_A}` is `π_A` (matches first three components; `π_N` matches only `[1]`; `π_M` does not cover); no sub-delegate of `π_A` exists, and any would have positive at position 4, where `b_1` has 0. `π_A` is O5-authorized. Result: `Σ_pre → Σ'` with `b_1 = a' ∈ Σ'.B`.

*Verifying O10's postconditions at `Σ'`:*

- **O10(a)**: `pfx(π_A) = [1, 0, 2] ≼ [1, 0, 2, 0, 6] = a'`, and `π_A` has the longest matching prefix in `Π_{Σ'}`, so `ω_{Σ'}(a') = π_A`. ✓
- **O10(a) corollary**: by (a), `pfx(π_A) = [1, 0, 2] ≼ a'`; the O6 biconditional gives `pfx(π_A) ≼ acct(a') = [1, 0, 2]`. ✓
- **O10(b)**: `a₃ ∈ Σ_pre.B ⊆ Σ'.B` (by B0 Irrevocability of ASN-0040 — the baptismal registry is monotone under `→`). `Π_{Σ'} = Π_{Σ_pre}` (baptism introduces no principals by O15). Hence `ω_{Σ'}(a₃) = ω_{Σ_pre}(a₃) = π_N` as before — no content modified, no ownership transferred. ✓

*Field-opening boundary case.* The trajectory above used the sibling-advance branch of `next` (`hwm_0 = 5`). The complementary field-opening branch arises when `hwm_0 = 0` — no depth-2 child of the fresh principal's prefix has yet been baptized in the corresponding granfilade stream. We exhibit this branch by continuing the running scenario with a sub-delegation: `π_A` delegates account prefix `[1, 0, 2, 3]` to a fresh principal `π_B`, producing state `Σ_3` (as referenced in the O8 verification above). *Verifying `delegated_{Σ_2}(π_A, π_B)`:* (i) `pfx(π_A) = [1, 0, 2] ≺ [1, 0, 2, 3] = pfx(π_B)` (length 3 vs 4, components match). ✓ (ii) `π_A` is the most-specific covering principal of `[1, 0, 2, 3]` in `Π_{Σ_2} = {π_N, π_M, π_A}`: `π_A`'s `[1, 0, 2]` covers; `π_N`'s `[1]` covers but is shorter; `π_M`'s `[2]` fails. ✓ (iii) `π_B ∈ Π_{Σ_3} ∖ Π_{Σ_2}`. ✓ (iv) `zeros(pfx(π_B)) = 1 ≤ 1` (account-level — the user field continues, no new zero introduced). ✓ (v) `T4(pfx(π_B))`: one zero at position 2, flanked by positive components, no leading/trailing zero, all field components positive. ✓ (vi) No existing principal extends `[1, 0, 2, 3]` strictly: `Π_{Σ_2} ∖ {π_A} = {π_N, π_M}`, neither extending. ✓ Hence `Σ_2 → Σ_3` is a delegation transition; by O18, `pfx(π_B) = [1, 0, 2, 3] ∈ Σ_3.B`, and by DelegatorAllocatesPrefix, `allocated_by_{Σ_3}(π_A, [1, 0, 2, 3])`.

*Verifying `hwm_0 = 0` at `Σ_3`.* Along this trajectory no element of the depth-2 stream `S([1, 0, 2, 3], 2)` has been baptized: the delegation `Σ_2 → Σ_3` materializes only `pfx(π_B)` (O18), and the prior baptisms are anchored under different parents, so by ASN-0040's parent-anchoring they do not populate `S([1, 0, 2, 3], 2)`. Hence `hwm(Σ_3.B, [1, 0, 2, 3], 2) = 0`. Had `π_A` baptized within `S([1, 0, 2, 3], 2)` pre-delegation, `hwm_0` would exceed zero and `π_B`'s first fork would take the sibling-advance branch.

*Forking by `π_B` at `Σ_3` via the field-opening branch.* Suppose `π_B` requires modification of content at some address it does not effectively own — say `a₃ = [1, 0, 7, 0, 1, 0, 1]` from the running scenario (`ω_{Σ_3}(a₃) = π_N` since `[1, 0, 7, …]`'s first three components do not extend `[1, 0, 2]`, let alone `[1, 0, 2, 3]`). The single baptism: `b_1 = next(Σ_3.B, [1, 0, 2, 3], 2)`. Since `hwm_0 = 0` (established above), the field-opening branch applies: `b_1 = inc([1, 0, 2, 3], 2) = [1, 0, 2, 3, 0, 1]` (TA5(d), appending the document-field separator and first document index). The resulting `a' = [1, 0, 2, 3, 0, 1]` has `zeros = 2` (document level), with `pfx(π_B) = [1, 0, 2, 3] ≼ a'` (the first four components reproduce `pfx(π_B)`).

*O5 check at `Σ_3`:* `π_B` is the most-specific covering principal of `[1, 0, 2, 3, 0, 1]` in `Π_{Σ_3} = {π_N, π_M, π_A, π_B}`. Candidates: `π_N` (prefix `[1]`, covers, length 1); `π_M` (prefix `[2]`, fails); `π_A` (prefix `[1, 0, 2]`, covers, length 3); `π_B` (prefix `[1, 0, 2, 3]`, covers, length 4). Longest match: `π_B`. No sub-delegate of `π_B` exists yet (`Π_{Σ_3} ∖ {π_B} = {π_N, π_M, π_A}` — none has a prefix strictly extending `[1, 0, 2, 3]` by condition (vi) at the moment `π_B` was delegated). ✓ (Baptism well-formedness by ASN-0040 B6.) *O10(a) at the post-baptism state* `Σ_4`: `pfx(π_B) ≼ a'` and `π_B` has the longest matching prefix in `Π_{Σ_4} = Π_{Σ_3}` (baptism introduces no principals by O15), so `ω_{Σ_4}(a') = π_B`. ✓ *O10(b):* every pre-existing baptized address persists in `Σ_4.B` (B0 Irrevocability of ASN-0040) and `Π_{Σ_4} = Π_{Σ_3}`; in particular, `ω_{Σ_4}(a₃) = ω_{Σ_3}(a₃) = π_N`, unchanged. ✓

Along the witnessing path traced above, `S([1, 0, 2, 3], 2)` is virgin at `Σ_3`, so `π_B`'s first fork invokes the field-opening branch with `hwm_0 = 0`; on alternative trajectories where the delegator pre-populates the stream, the same fork instead traverses sibling-advance. Unilateral O10★ is robust to either branch: the user-field-separator argument articulated below for `π_A` transposes to `π_B` by substituting `pfx(π_B)` for `pfx(π_A)`, and applies identically to both branch outputs — `inc(pfx(π_B), 2) = [1, 0, 2, 3, 0, 1]` (field-opening) and `inc([1, 0, 2, 3, 0, k], 0) = [1, 0, 2, 3, 0, k + 1]` (sibling-advance) are both document-level addresses whose separator at position `#pfx(π_B) + 1 = 5` structurally defeats every potential sub-delegate prefix of `π_B`.

The fork transforms the ownership boundary into a creative act: `π_A` now has a fully owned address `a'` whose content identity may relate to `a₃`'s content (through the content model), but whose ownership is entirely independent. The trajectory illustrates Unilateral O10★: for an account-level principal, the fork is unilateral regardless of `Σ_pre`'s state, because the user-field separator at position `#pfx(π_A) + 1 = 4` of any document-level extension structurally defeats every potential sub-delegate prefix (each of which must have a positive component there, by O1a's `zeros ≤ 1` saturation), and `hwm + 1` is by O18's baptismal coupling never pre-claimed by a sub-delegate. If `π_A` subsequently wishes to place content (e.g., an inclusion-link target referencing `a₃`'s content) inside `a'`, it may baptize further within `dom(a')` by repeated field-opening — but the descent is `π_A`'s choice within its sovereignty, not a requirement of O10.


## Structural Provenance

The ownership prefix is embedded in the permanent address. Because every principal's prefix satisfies `zeros(pfx(π)) ≤ 1` (O1a), the longest-match computation depends only on the node and user fields — the portion captured by `acct(a)`. The document and element fields are irrelevant to ownership determination.

**O6 (StructuralProvenance).** The effective owner of an allocated address is determined entirely by its account field:

  `(A a, b ∈ Σ.B : acct(a) = acct(b) ⟹ ω(a) = ω(b))`

We prove that equal account fields imply equal effective owners by showing that the prefix comparisons determining ownership depend only on the account field. The argument requires a structural property of `acct`: for any valid tumbler `a`, the account field is a prefix of the address itself:

**AccountPrefix (AccountPrefix).** `(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)`

We prove that for any tumbler `a` satisfying T4 (HierarchicalParsing), `acct(a) ≼ a` — the account field is a prefix of the address. The T4 restriction is essential: `acct` relies on the field decomposition `fields(a)` whose well-definedness is given by T4b (UniqueParse) — for a tumbler like `[0, 0, 1]`, adjacent zeros violate T4a (SyntacticEquivalence) and the field decomposition is ill-defined. By O17 (AllocatedAddressValidity, derived from ASN-0040 B10), all allocated addresses satisfy T4, so the restriction does not limit application.

The Prefix (PrefixRelation) definition of ASN-0034 requires two conditions: `#a ≥ #acct(a)` and `(A i : 1 ≤ i ≤ #acct(a) : acct(a)ᵢ = aᵢ)`. Both follow directly from FieldStructure (established with AccountField above). When `zeros(a) = 0`, FieldStructure gives `acct(a) = a`, so `acct(a) ≼ a` reflexively. When `zeros(a) ≥ 1`, FieldStructure gives that `acct(a) = N(a) ++ [0] ++ U(a)` reproduces exactly the leading `#acct(a) = α + 1 + β` components of `a` (discharging the component condition), and that any document/element fields occupy positions strictly after `α + 1 + β` — so `#a = #acct(a)` when `zeros(a) = 1` (no further fields) and `#a > #acct(a)` when `zeros(a) ≥ 2` (discharging the length condition). Hence `acct(a) ≼ a` in every case, with equality when `zeros(a) ≤ 1` and strict prefix when `zeros(a) ≥ 2`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `T4(a)`.
- *Definition:* `acct(a) = a` when `zeros(a) = 0`; `acct(a) = N(a) ++ [0] ++ U(a)` when `zeros(a) ≥ 1`.
- *Postconditions:* `acct(a) ≼ a`. When `zeros(a) ≤ 1`: `acct(a) = a` (equality). When `zeros(a) ≥ 2`: `acct(a) ≺ a` (strict prefix).

The proof of O6 proceeds in two directions. *Forward:* we must show that for any principal `π` — by O1a (AccountOwnershipBoundary), every principal satisfies `zeros(pfx(π)) ≤ 1` — the relation `pfx(π) ≼ a` implies `pfx(π) ≼ acct(a)`. Two cases arise from the zero count.

When `zeros(pfx(π)) = 0`: the prefix contains no zero separators, so every component of `pfx(π)` is nonzero. Since `pfx(π) ≼ a`, the first `#pfx(π)` components of `a` all equal the corresponding components of `pfx(π)`, and are therefore all nonzero. Two sub-cases arise from the zero count of `a`.

When `zeros(a) = 0`: by T4c (LevelDetermination), zero count zero means the tumbler is a node-level address — the entire sequence is the node field, so `acct(a) = a`. Since `pfx(π) ≼ a = acct(a)`, the result is immediate.

When `zeros(a) ≥ 1`: by T4b (UniqueParse), `fields(a)` decomposes `a` uniquely; the components preceding `a`'s first zero separator constitute `a`'s node field `N(a)`. Since `pfx(π)`'s components are all nonzero and match `a`'s leading components, `pfx(π)` lies entirely within `a`'s node field: `pfx(π) ≼ N(a)`. And `N(a) ≼ acct(a)` by the definition of `acct` (which includes the node field and, when present, the user field). Hence `pfx(π) ≼ acct(a)`.

In both sub-cases, `pfx(π) ≼ acct(a)`.

When `zeros(pfx(π)) = 1`: the prefix has the form `N₁...Nα.0.U₁...Uβ`, with a zero separator at position `α + 1`. The prefix relation `pfx(π) ≼ a` forces `a_{α+1} = 0`, hence `zeros(a) ≥ 1`. By T4's positive-component constraint applied to `a`, all components before this zero are positive (they match `N₁...Nα`, which are positive by T4 applied to `pfx(π)`), so by T4a (SyntacticEquivalence) this zero cannot be adjacent to another zero or appear at position 1; by T4b (UniqueParse) applied to `a`, `a`'s field decomposition is unique, and since positions `1..α` are positive while `a_{α+1} = 0`, position `α + 1` is uniquely identified as `a`'s node-user field separator. This aligns `pfx(π)`'s field structure with `a`'s: the node fields match (`a`'s node field is `N₁...Nα`), and the prefix relation forces `pfx(π)`'s user-field components `U₁...Uβ` to match the first `β` components of `a`'s user field. Since `acct(a)` captures `a` through its full user field, `pfx(π) ≼ acct(a)`.

In both cases, `pfx(π) ≼ a` implies `pfx(π) ≼ acct(a)`. *Reverse:* suppose `pfx(π) ≼ acct(a)`. By AccountPrefix, `acct(a) ≼ a`. By transitivity of the prefix relation, `pfx(π) ≼ a`. We conclude the biconditional:

  `pfx(π) ≼ a  ≡  pfx(π) ≼ acct(a)`

Now, when `acct(a) = acct(b)`, substitution gives `pfx(π) ≼ acct(a) ≡ pfx(π) ≼ acct(b)`, and hence `pfx(π) ≼ a ≡ pfx(π) ≼ b`. The set of covering principals is identical for `a` and `b`. By O2 (OwnershipExclusivity), the effective owner `ω` is the unique longest-match principal in the covering set; since the covering sets coincide, the longest match is the same, giving `ω(a) = ω(b)`. ∎

*Corollary (owner prefix containment).* The effective owner's prefix is always embedded within the account field: `pfx(ω(a)) ≼ acct(a)`. We derive this in four steps. (1) By O1a, `zeros(pfx(ω(a))) ≤ 1`. By T4c (LevelDetermination), a valid tumbler with at most one zero separator is at most an account-level address — it contains no document-field or element-field components. (2) By definition of `ω`, `pfx(ω(a)) ≼ a`, so the components of `pfx(ω(a))` match `a`'s leading components. (3) Two cases arise from the zero count. When `zeros(pfx(ω(a))) = 0`: the prefix contains no zero separators, so every component is nonzero; since `pfx(ω(a)) ≼ a`, the first `#pfx(ω(a))` components of `a` are all nonzero, which places them entirely within `a`'s node field; hence `pfx(ω(a)) ≼ N(a) ≼ acct(a)`. When `zeros(pfx(ω(a))) = 1`: the prefix has the form `N.0.U`, and the zero separator at position `α + 1` in the prefix forces — via the prefix relation — a zero at the same position in `a`, aligning `a`'s node-user field boundary with the prefix's; the prefix's user-field components then match `a`'s user-field prefix; since `acct(a)` captures `a` through its full user field, `pfx(ω(a)) ≼ acct(a)`. (4) Hence `#pfx(ω(a)) ≤ #acct(a)` and `pfx(ω(a)) ≼ acct(a)`. The containment may be strict when the address occupies a sub-account position that the effective owner controls but has not delegated. Nelson permits this: "Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose" (LM 4/17). An account-level principal may create sub-account positions as organizational namespaces, ghost elements, or internal partitions without introducing a new ownership principal — the owner decides what sub-numbering means. Equality `pfx(ω(a)) = acct(a)` holds when no intermediate sub-account structure extends beyond the owner's prefix; this is the common case for addresses allocated directly at the principal's own account level.

*Formal Contract:*
- *Preconditions:* `a, b ∈ Σ.B`, `acct(a) = acct(b)`.
- *Postconditions:* `ω(a) = ω(b)`.
- *Invariant:* `pfx(ω(a)) ≼ acct(a)` for all `a ∈ Σ.B`.

Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" (LM 2/40).

Provenance is not a right that can be exercised or waived — it is an inalienable structural fact. Even if ownership were to transfer (contrary to O3, and through some unspecified mechanism), the address would still record the original principal's identity. The new owner might act upon the content, but the address would forever testify to its origin. This separation — between *who created* and *who currently holds rights* — is what makes ownership transfer conceptually possible without violating address permanence. The address encodes provenance; ownership encodes authority. Under the system as specified, these coincide. Under a hypothetical transfer regime, they would diverge.

Gregory confirms: the User field in the tumbler `Node.0.User.0.Doc.0.Element` is a permanent structural component. The `tumbleraccounteq` function reads these components directly from the mantissa array. There is no indirection, no lookup, no level of abstraction that could mask the origin.


## Subdivision Authority

Of the rights that ownership confers, one is essential to the ownership model itself: the right to create sub-positions. O5 (SubdivisionAuthority) requires that the allocator of any newly baptized address be the most-specific covering principal in `Π_Σ`. We develop here its consequences for the relation between allocation and effective ownership.

*Corollary (allocator is effective owner for non-introducing transitions).* If `Σ → Σ'` is a transition with `Π_{Σ'} = Π_Σ` (no principal introduced) and `allocated_by_{Σ'}(π, a)` for `a ∈ Σ'.B ∖ Σ.B`, then `ω_{Σ'}(a) = π`. *Proof.* O5 supplies `pfx(π) ≼ a` and `(A π' ∈ Π_Σ : pfx(π') ≼ a ⟹ #pfx(π') ≤ #pfx(π))`. By O13 (PrefixImmutability), every `π' ∈ Π_Σ` retains its prefix at `Σ'`; combined with the hypothesis `Π_{Σ'} = Π_Σ` (and O12 (PrincipalPersistence), which is consistent with it), the covering set and prefix-length data in `Π_{Σ'}` coincide with those in `Π_Σ`. Hence `π` achieves the unique longest match in `Π_{Σ'}` for `a`. By O2 (applied at `Σ'`), `ω_{Σ'}(a) = π`. ∎

For introducing transitions — delegation, where `Π_{Σ'} ∖ Π_Σ = {π'}` and O18 baptizes `pfx(π')` simultaneously — the effective-owner outcome at the baptized prefix is `π'` (the delegate, not the delegator/allocator), and that case is captured by O7(a) rather than this corollary.

Nelson: "The owner of a given item controls the allocation of the numbers under it" (LM 4/20). This is the *right to baptize* — not the baptism mechanism itself (which belongs to the tumbler baptism specification), but the authorization constraint that governs who may invoke it.

Gregory confirms: `docreatenewdocument` always uses `taskptr->account` — the session's own prefix — as the allocation hint. The allocation algorithm operates within the boundary determined by the session's account tumbler. There is no parameter that allows specifying someone else's prefix as the allocation target.

O5 interacts with O2. Because ownership is exclusive, exactly one principal may allocate at any point in the address space. Because ownership is determined by prefix (O1), the authorized allocator is determined structurally. The conjunction of O2 and O5 means the address space grows exclusively through the actions of the principals who own each region — no external intervention, no administrative override, no "root user" who may allocate anywhere.


## Delegation

Ownership is not held at a single level — it flows downward through the hierarchy. Nelson calls this "baptism," but we must separate two concepts: *ownership delegation*, which introduces a new principal into `Π`, and *allocation*, which creates addresses within an existing principal's domain. The allocation mechanism is uniform at all levels (T10a); the ownership consequences differ.

We first recall the delegation relation. We use the *strict prefix* relation throughout: `p ≺ a  ≡  p ≼ a ∧ p ≠ a` (equivalently, `p ≼ a ∧ #p < #a` — the equivalence holds because `p ≼ a ∧ #p = #a` gives `p = a` by T3).

The delegation predicate `delegated(Σ, Σ', π, π')` was defined in *State Axioms* alongside O15 (PrincipalClosure), with `delegated_Σ(π, π')` as the abbreviation used when `Σ'` is fixed by the surrounding formula. We restate the six conditions here for ready reference:

  (i) `pfx(π) ≺ pfx(π')` — the delegate's prefix strictly extends the delegator's

  (ii) `π` is the most-specific covering principal for `pfx(π')` at the time of delegation: `(A π'' ∈ Π_Σ : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π))`

  (iii) `π' ∈ Π_{Σ'} ∖ Π_Σ` — the delegate is newly introduced

  (iv) `zeros(pfx(π')) ≤ 1` — the delegate's prefix is at node or account level

  (v) `T4(pfx(π'))` — the delegate's prefix is a valid tumbler address

  (vi) `¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))` — no existing principal has a prefix strictly extending the new delegate's prefix

Condition (ii) is the authorization constraint — delegation requires O5's subdivision authority. A principal cannot delegate within a sub-domain that has already been delegated to someone else. This grounds the distinction between direct delegation (`π → π'`) and transitive delegation (`π → π' → π''`): when `π` delegates to `π'` and `π'` later delegates to `π''`, we have `delegated(π, π')` and `delegated(π', π'')` but not `delegated(π, π'')`.

Condition (vi) enforces top-down delegation order: a parent prefix must be delegated before any child prefix within it. Without this condition, a higher-level principal could delegate a longer prefix before the shorter enclosing prefix — for instance, delegating `[1, 0, 2, 3]` to `π₂` and subsequently `[1, 0, 2]` to `π₁`, leaving `π₂`'s sub-domain inside `dom(π₁)` without `π₁`'s authorization. Condition (ii) alone does not prevent this: it examines prefixes *of* the target (whether the delegator is the most-specific covering principal), not extensions *beyond* the target (whether some existing principal already occupies a sub-domain). With (vi), when `π'` enters Π, no principal already occupies a sub-domain of `dom(π')`, so `π'` has full authority over its domain from the moment of creation.

Delegation preserves O1a (AccountPrefix). By condition (iv), any `π'` admitted by the `delegated` relation satisfies `zeros(pfx(π')) ≤ 1`. Since O1a requires exactly this — that every principal's prefix is at node or account level — the new principal satisfies O1a by construction; existing principals persist by O12 (PrincipalPersistence) with prefixes preserved by O13 (PrefixImmutability), so their `zeros(pfx(π))` values are unchanged from `Σ` to `Σ'`. O1a is maintained. The base case for the induction is O14's third clause (`(A π ∈ Π₀ : zeros(pfx(π)) ≤ 1)`); non-delegation transitions preserve O1a trivially, since O15 admits no new principal and O13 fixes existing prefixes. By induction on the reachability sequence, O1a holds in every reachable state.

Delegation preserves T4 (ValidAddress). By condition (v), the delegate's prefix satisfies T4 directly — no adjacent zeros, no leading or trailing zero, and every present field non-empty. This is not redundant with condition (iv): a prefix such as `[1, 2, 0]` satisfies `zeros ≤ 1` but violates T4 (trailing zero, empty user field). Condition (v) excludes such prefixes. Existing principals persist by O12 (PrincipalPersistence) and their prefixes are unchanged by O13 (PrefixImmutability), so `T4(pfx(π))` is preserved for every `π ∈ Π_Σ` at `Σ'`. T4 is maintained across the transition. The base case for the induction is O14's fifth clause (`(A π ∈ Π₀ : T4(pfx(π)))`); non-delegation transitions preserve T4 trivially, since O15 admits no new principal and O13 fixes existing prefixes. By induction on the reachability sequence, every principal's prefix satisfies T4 in every reachable state.

Delegation preserves O1b (PrefixInjectivity). Suppose for contradiction that `pfx(π') = pfx(π''')` for some existing `π''' ∈ Π_Σ`. Then `pfx(π''') ≼ pfx(π')`, so by condition (ii) of the delegation relation, `#pfx(π''') ≤ #pfx(π)`. But from condition (i), `pfx(π) ≺ pfx(π')`, giving `#pfx(π) < #pfx(π')`. Combining: `#pfx(π''') ≤ #pfx(π) < #pfx(π') = #pfx(π''')` — a contradiction. Hence every delegation introduces a principal with a prefix distinct from all existing prefixes. By O15, each transition introduces at most one new principal, so no pairwise collision among newly introduced principals can occur — the proof against existing principals is exhaustive. Existing-vs-existing pairwise distinctness carries from `Σ` to `Σ'` by O13 (PrefixImmutability): for any `π'_1, π'_2 ∈ Π_Σ` with `π'_1 ≠ π'_2`, the inductive hypothesis (O1b at `Σ`) gives `pfx_Σ(π'_1) ≠ pfx_Σ(π'_2)`, and O13 yields `pfx_{Σ'}(π'_i) = pfx_Σ(π'_i)` for `i ∈ {1, 2}`, so `pfx_{Σ'}(π'_1) ≠ pfx_{Σ'}(π'_2)`. O1b is maintained across all state transitions. The base case for the induction is O14's fourth clause (`pfx` injective on `Π₀`); non-delegation transitions preserve O1b trivially, since O15 admits no new principal and the inductive hypothesis on `Π_Σ` is carried unchanged by O13 to `Π_{Σ'}`. By induction on the reachability sequence, O1b holds in every reachable state. This closes the proof chain: delegation preserves O1a, T4, and O1b, which ensures `ω` (O2) yields a unique principal at a valid hierarchy level with `fields(·)` well-defined (T4b UniqueParse).

**DelegatorAllocatesPrefix (derived).** The delegating parent is the allocator of the delegate's prefix in the delegation transition. Equivalently, the principal-registry side of the delegation act (introducing `π'` into `Π`) and the baptismal-registry side (entering `pfx(π')` into `Σ.B`) are bound by a single allocator — `π_d`:

  `(A Σ, Σ', π_d, π' : Σ reachable from Σ₀ ∧ delegated_Σ(π_d, π') ∧ Σ → Σ' ⟹ allocated_by_{Σ'}(π_d, pfx(π')))`

We derive this from O18 (DelegationBaptizes), O16 (AllocationClosure), O5 (SubdivisionAuthority), condition (ii) of the delegation relation, and O1b (PrefixInjectivity). *Freshness.* By the strengthened O18, the delegation transition `Σ → Σ'` introducing `π' ∈ Π_{Σ'} ∖ Π_Σ` gives `pfx(π') ∈ Σ'.B ∖ Σ.B` directly — the delegate's prefix is registered in `Σ'.B` and not present in `Σ.B`. The freshness conjunct removes the need to argue against an earlier sub-position allocation: O18 records the design commitment that principal prefixes are reserved (their first entry into the baptismal registry is the delegation transition that introduces them). *Allocator identification.* Given `pfx(π') ∈ Σ'.B ∖ Σ.B`, O16 supplies `π_a ∈ Π_Σ` with `allocated_by_{Σ'}(π_a, pfx(π'))`. By O5 applied to the current transition, `π_a` is the most-specific covering principal of `pfx(π')` in `Π_Σ`. By condition (ii) of `delegated_Σ(π_d, π')`, `π_d` is also the most-specific covering principal of `pfx(π')` in `Π_Σ`. Suppose `π_a ≠ π_d`. Both have `pfx(π_a), pfx(π_d) ≼ pfx(π')` with `#pfx(π_a) = #pfx(π_d)` (each achieving the maximum). By the covering-chain lemma, `pfx(π_a)` and `pfx(π_d)` are `≼`-comparable; with equal lengths, the prefix relation forces equality `pfx(π_a) = pfx(π_d)` (each is a prefix of the other by length, and the components agree componentwise with `pfx(π')`). By O1b, `π_a = π_d` — contradicting the supposition. Hence `π_a = π_d`, and `allocated_by_{Σ'}(π_d, pfx(π'))` holds. ∎

*Formal Contract:*
- *Preconditions:* `Σ` reachable from `Σ₀`, `delegated_Σ(π_d, π')`, `Σ → Σ'`.
- *Postconditions:* `allocated_by_{Σ'}(π_d, pfx(π'))` — the delegator is the allocator of the delegate's prefix in the delegation transition.
- *Invariant:* The same `π_d` whose authority condition (ii) admits `π'` into `Π` is the allocator whose O5 authority enters `pfx(π')` into `B`. The two-views-of-one-act coupling between the principal and baptismal registries is O18's content; this property locates the single allocator.

The derived property states a coupling: when a delegation transition fires, the delegator is the unique principal whose O5 authority underwrites the baptism of the new prefix. Gregory's implementation realizes this coupling concretely — `findpreviousisagr` enters the new account slot into the granfilade under the session's own account-tumbler authority, so the delegator and the allocator are necessarily the same process.

**O7 (OwnershipDelegation).** A principal `π` may delegate a sub-prefix to a new principal `π'`, provided the `delegated` relation is satisfied (which entails `zeros(pfx(π')) ≤ 1` by condition (iv)) and `π` holds subdivision authority over `pfx(π')`. Upon delegation:

  `(A π, π' : delegated(π, π') :`

  (a) `ω_{Σ'}(a) = π'` for all `a ∈ dom(π') ∩ Σ'.B`

  (b) `π'` may allocate new addresses within `dom(π')` (O5 applies to `π'`)

  (c) `π'` may delegate a sub-prefix `p''` with `pfx(π') ≺ p''` to a new principal `π''` whenever, at the prospective delegation state, both (ii) `π'` is the most-specific covering principal for `p''` — no existing principal has a prefix `pfx(π''') ≼ p''` with `pfx(π') ≺ pfx(π''')` — and (vi) no existing principal already extends `p''` strictly — `¬(E π''' ∈ Π : p'' ≺ pfx(π'''))`. The right is recursive: conditions (ii) and (vi) of the `delegated` relation become re-checking obligations on the prospective delegation state, exactly the constraints that bound `π` when `π` delegated to `π'`

We prove each postcondition under the hypothesis that `delegated_Σ(π, π')` holds for a transition `Σ → Σ'`, with `π ∈ Π_Σ` and `π' ∈ Π_{Σ'} ∖ Π_Σ`.

*Postcondition (a): `ω_{Σ'}(a) = π'` for all `a ∈ dom(π') ∩ Σ'.B`.*

Let `a ∈ dom(π') ∩ Σ'.B` be arbitrary. By the definition of domain, `pfx(π') ≼ a`, so `π'` covers `a`. We must show that `π'` achieves the strictly longest matching prefix among all principals in `Π_{Σ'}`.

By O15 (PrincipalClosure), at most one new principal enters `Π` per transition, and `π'` is that principal by condition (iii). Therefore `Π_{Σ'} = Π_Σ ∪ {π'}`. Let `π'' ∈ Π_Σ` with `pfx(π'') ≼ a` be an arbitrary pre-existing covering principal.

By the covering-chain lemma (PrefixesOfCommonAddressAreComparable, *Ownership Domains* section), the two prefixes `pfx(π'')` and `pfx(π')` of the common address `a` are `≼`-comparable. Three cases exhaust the comparison.

*Case `pfx(π') ≺ pfx(π'')`* — then `π'' ∈ Π_Σ` has a prefix strictly extending `pfx(π')`, contradicting condition (vi) of the delegation relation: `¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))`.

*Case `pfx(π') = pfx(π'')`* — by condition (ii), `π` is the most-specific covering principal for `pfx(π')` in `Π_Σ`, so `#pfx(π'') ≤ #pfx(π)`. But `#pfx(π'') = #pfx(π')`, and by condition (i), `#pfx(π) < #pfx(π')`. Combining: `#pfx(π) < #pfx(π') = #pfx(π'') ≤ #pfx(π)` — contradiction.

*Case `pfx(π'') ≺ pfx(π')`* — by condition (ii), `#pfx(π'') ≤ #pfx(π)`, and by condition (i), `#pfx(π) < #pfx(π')`. Therefore `#pfx(π'') < #pfx(π')`.

Only the third case is consistent. Every pre-existing covering principal `π'' ∈ Π_Σ` satisfies `#pfx(π'') < #pfx(π')`. Since the only new principal in `Π_{Σ'}` is `π'` itself, `π'` achieves the unique longest matching prefix in `Π_{Σ'}` for `a`. By O2 (OwnershipExclusivity), `ω_{Σ'}(a) = π'`.

*Postcondition (b): O5 applies to `π'`.*

O5 (SubdivisionAuthority) requires that the allocator of a new address be the most-specific covering principal. By postcondition (a), `ω_{Σ'}(a) = π'` for every `a ∈ dom(π') ∩ Σ'.B` — `π'` has the longest matching prefix in its domain. For any new address `a` allocated within `dom(π')` in a successor transition `Σ' → Σ''`, O5's two conjuncts are: `pfx(π') ≼ a` (which holds by `a ∈ dom(π')`) and `(A π'' ∈ Π_{Σ'} : pfx(π'') ≼ a ⟹ #pfx(π'') ≤ #pfx(π'))` (which holds because postcondition (a) established that no principal in `Π_{Σ'}` has a longer matching prefix within `dom(π')` than `π'`). Hence `π'` satisfies O5's authorization condition for allocating within `dom(π')`.

*Postcondition (c): recursive delegation (conditional on remaining most-specific).*

Since `π' ∈ Π_{Σ'}`, the delegation relation's conditions are satisfiable with `π'` as delegator for a sub-prefix `p''` with `pfx(π') ≺ p''` *immediately upon entry* — that is, at `Σ'`. Condition (i) holds by the choice of `p''`. Condition (ii) requires that `π'` be the most-specific covering principal of `p''` in `Π_{Σ'}` — equivalently, no `π'' ∈ Π_{Σ'}` with `pfx(π'') ≼ p''` has `#pfx(π'') > #pfx(π')`. We derive this directly from condition (vi) of the original delegation `delegated_Σ(π, π')`: `¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))` — no principal in `Π_Σ` has a prefix strictly extending `pfx(π')`. By O15, `Π_{Σ'} ∖ Π_Σ = {π'}`, and `pfx(π')` does not strictly extend itself, so the same non-existence carries over: no `π'' ∈ Π_{Σ'}` has `pfx(π') ≺ pfx(π'')`. Hence no covering principal of `p''` in `Π_{Σ'}` has prefix length exceeding `#pfx(π')`; `π'` achieves the maximum, satisfying condition (ii). Conditions (iv), (v), and (vi) constrain the target prefix `p''`, not the delegator, and are obligations on the choice of delegate prefix. *At later states* `Σ'' ⪰ Σ'`, condition (ii) requires re-checking: if `π'` has itself already delegated some `p* ⪯ p''` to a principal `π*` with `pfx(π') ≺ pfx(π*) ≼ p''`, then `π*` — not `π'` — is the most-specific covering principal for `p''` at `Σ''`, and `π'` cannot delegate `p''`. Postcondition (c) thus asserts the *right* to delegate sub-prefixes, conditional on `π'` retaining most-specific-covering status; it does not assert an absolute right against subsequent sub-delegations by `π'` itself. The recursion may continue indefinitely along any chain whose successive delegates remain consistent with this condition. We witness the recursion with a chain of account-level delegates rooted at a node principal `π_0` with `pfx(π_0) = [1]` (`zeros = 0`). *Boundary step* `π_0 → π_1`: `pfx(π_1) = [1, 0, 1]` opens the user field (appending the separator and first user-field component), with `pfx(π_0) ≺ pfx(π_1)`, `zeros = 1`, and T4 holding (single zero at position 2, flanked by positives). *Uniform inductive step* `π_k → π_{k+1}` for `k ≥ 1`: `pfx(π_{k+1}) = [1, 0, 1, …, 1]` (`k + 3` components) appends one user-field component to `pfx(π_k)`, preserving `pfx(π_k) ≺ pfx(π_{k+1})`, `zeros = 1`, and T4. A bare appeal to T0(b) (UnboundedLength) does not suffice — its length-`n` witnesses carry `zeros = 0`, violating condition (iv) — but this account-level chain extends to arbitrary length while keeping `zeros = 1`. Conditions (ii) and (vi) hold at each link because the covering set of `pfx(π_{k+1})` in the state after `π_0, …, π_k` are introduced is exactly `{π_0, …, π_k}` — by NestingByDelegation, any other principal's prefix is non-nesting with the chain, hence cannot cover `pfx(π_{k+1})` (covering-chain lemma) — whose maximal-length member is `π_k`. We do not claim termination; the construction extends as far as the chosen sequence of delegates permits.

The authorization constraint is carried by the `delegated` relation — condition (ii) requires `π` to be the most-specific covering principal. This prevents a grandparent from delegating within a sub-domain it has already handed off: if `π₁` delegates `[1, 0, 2, 3]` to `π₂`, then `π₁` cannot subsequently delegate `[1, 0, 2, 3, 5]` to `π₃`, because `π₂` — not `π₁` — is the most-specific covering principal for that prefix.

Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers" (LM 4/17). The allocation mechanism is uniform ("the entire tumbler works like that," LM 4/19), but the resulting authority is hierarchical: delegation at node and account level creates principals with full sovereignty over their domain, while allocation at document and version level exercises mechanical subdivision rights within the parent principal's domain without establishing independent ownership standing. ∎

*Formal Contract:*
- *Preconditions:* `delegated_Σ(π, π')`, `Σ → Σ'`.
- *Postconditions:* (a) `(A a ∈ dom(π') ∩ Σ'.B : ω_{Σ'}(a) = π')`; (b) `π'` satisfies O5 for allocations within `dom(π')`; (c) the delegation relation is satisfiable with `π'` as delegator for any sub-prefix `p''` (with `pfx(π') ≺ p''`) at every state at which (ii) `π'` remains the most-specific covering principal for `p''` — no existing sub-delegate `π''' ∈ Π` with `pfx(π') ≺ pfx(π''') ≼ p''` has been introduced — and (vi) no existing principal has a prefix strictly extending `p''`. Both conditions trivially satisfied at `Σ'`; checkable at later states.
- *Invariant:* Delegation confers full sovereignty — the delegate becomes the effective owner of its entire domain immediately upon delegation, and acquires the rights to allocate and sub-delegate within that domain.

The delegation is irrevocable:

**O8 (IrrevocableDelegation).** Once principal `π` delegates to `π'`, the delegating parent never regains effective ownership of addresses in the delegate's domain:

  `(A π, π', a, Σ_d, Σ' : Σ_d reachable from Σ₀ ∧ delegated_{Σ_d}(π, π') ∧ Σ_d →⁺ Σ' ∧ π' ∈ Π_{Σ'} ∧ a ∈ dom(π') ∩ Σ'.B : ω_{Σ'}(a) ≠ π)`

The formulation captures irrevocability without overclaiming. It says the *parent* can never recover the addresses, while permitting the delegate `π'` to sub-delegate (via O7(c)): if `π'` delegates to `π''` with `pfx(π') ≺ pfx(π'')`, then `ω(a) = π''` for `a ∈ dom(π'')` — the address leaves `π'`'s effective ownership but does not return to `π`. The domain restriction `dom(π') ∩ Σ'.B` ensures `ω` is applied only to addresses where it is defined (grounded by O4). The hypothesis `π' ∈ Π_{Σ'}` forces the trajectory `Σ_d →⁺ Σ'` to pass through `π'`'s introducing delegation transition `Σ_d → Σ_d^{post}` (by O15, principals enter only via bootstrap or delegation).

We prove that in every state `Σ'` reachable from the delegation state, the delegating parent `π` is never the effective owner of any address in the delegate's domain. The argument is direct: we show that the longest-match computation in `Σ'` always finds a principal with a strictly longer prefix than `π`, so `π` cannot be `ω_{Σ'}(a)`.

Let `Σ_d` denote the state in which `delegated_{Σ_d}(π, π')` holds (with `Σ_d` reachable from `Σ₀` by hypothesis), and let `Σ'` be any state with `Σ_d →⁺ Σ'` (`Σ'` is then also reachable from `Σ₀`, by composing the witnessing sequence to `Σ_d` with the transitions to `Σ'`). Let `a ∈ dom(π') ∩ Σ'.B` be arbitrary.

*The delegate persists with an unchanged prefix.* Let `Σ_d^{post}` be the target of the introducing transition `Σ_d → Σ_d^{post}` at which `π'` enters `Π`. Since O12 (PrincipalPersistence) forbids re-introduction and O15 (PrincipalClosure) admits `π'` only via this delegation (condition (iii) gives `π' ∉ Π_{Σ_d}`, excluding bootstrap), `π'` has a unique introduction event, so the hypothesis `π' ∈ Π_{Σ'}` forces the trajectory `Σ_d →⁺ Σ'` to pass through `Σ_d^{post}`. By O13 (PrefixImmutability) iterated along `Σ_d^{post} →^* Σ'`, `pfx_{Σ'}(π') = pfx_{Σ_d^{post}}(π')`. The delegate is present at `Σ'` with the prefix it received at the delegation transition.

*The delegate covers the address.* Since `a ∈ dom(π')`, the definition of domain gives `pfx(π') ≼ a`. This relation depends only on the components of `pfx(π')` and `a`. By O13, `pfx(π')` is immutable. By B0★ (MultiStepIrrevocability) of ASN-0040 applied along the sub-trajectory `Σ_d^post →* Σ'`, `a` — being baptized — persists in the baptismal registry with unchanged components. Therefore `pfx_{Σ'}(π') ≼ a` holds in `Σ'`.

*The delegate's prefix is strictly longer than the parent's.* By condition (i) of the delegation relation, `pfx_{Σ_d}(π) ≺ pfx_{Σ_d^{post}}(π')` — the delegator's prefix at the delegation transition's source strictly extends to the delegate's prefix at the transition's target — which gives `#pfx_{Σ_d}(π) < #pfx_{Σ_d^{post}}(π')`. By O13 iterated along `Σ_d →^* Σ'` (and using O12 to carry `π` from `Π_{Σ_d}` into `Π_{Σ'}`), both prefixes are immutable: `pfx_{Σ'}(π) = pfx_{Σ_d}(π)` and `pfx_{Σ'}(π') = pfx_{Σ_d^{post}}(π')`. The strict length inequality `#pfx_{Σ'}(π) < #pfx_{Σ'}(π')` holds at every `Σ'` with `π' ∈ Π_{Σ'}`.

*The parent cannot be the longest match.* The effective owner `ω_{Σ'}(a)` is defined (O2) as the principal in `Π_{Σ'}` with the longest matching prefix for `a`. We have established that `π' ∈ Π_{Σ'}` with `pfx_{Σ'}(π') ≼ a` and `#pfx_{Σ'}(π') > #pfx_{Σ'}(π)`. Therefore `π'` (or some other principal with a still-longer prefix) achieves a longer match than `π`. The longest-match principal must have a prefix at least as long as `pfx(π')`, which is strictly longer than `pfx(π)`. Hence `ω_{Σ'}(a) ≠ π`.

To see this last step precisely: suppose for contradiction that `ω_{Σ'}(a) = π`. Then by the definition of `ω`, `π` would need to satisfy `(A π'' ∈ Π_{Σ'} : π'' ≠ π ∧ pfx_{Σ'}(π'') ≼ a ⟹ #pfx_{Σ'}(π) > #pfx_{Σ'}(π''))`. But `π' ∈ Π_{Σ'}` with `π' ≠ π` (they are distinct — `π` was already in `Π` before delegation while `π'` was newly introduced, and their prefixes differ in length) and `pfx_{Σ'}(π') ≼ a`, yet `#pfx_{Σ'}(π) < #pfx_{Σ'}(π')` — contradicting the requirement. Therefore `ω_{Σ'}(a) ≠ π`.

Note that the proof makes no claim about *who* the effective owner is — only that it is not `π`. The effective owner may be `π'` itself, or it may be a sub-delegate `π''` introduced by `π'` with `pfx(π') ≺ pfx(π'')`. In the latter case, `ω_{Σ'}(a) = π''` for `a ∈ dom(π'')` — the address leaves `π'`'s effective ownership but does not return to `π`, because `#pfx(π'') > #pfx(π') > #pfx(π)` and the argument above applies equally to `π''`. ∎

*Design confirmation.* Nelson: "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). There is no revocation command, no forced reclamation. Gregory confirms: `validaccount` is a stub that unconditionally returns TRUE — the system has no machinery for checking or revoking delegation. Once the sub-prefix exists, the delegate owns it permanently.

*Formal Contract:*
- *Preconditions:* `Σ_d` reachable from `Σ₀`, `delegated_{Σ_d}(π, π')`, `Σ_d →⁺ Σ'`, `π' ∈ Π_{Σ'}`, `a ∈ dom(π') ∩ Σ'.B`.
- *Postconditions:* `ω_{Σ'}(a) ≠ π`.
- *Invariant:* Once delegation occurs, the parent's prefix is permanently shorter than the delegate's, so the parent can never regain longest-match status for any address in the delegate's domain.

The combination of O3 (OwnershipRefinement), O8 (IrrevocableDelegation), O12 (PrincipalPersistence), O13 (PrefixImmutability), and B0 (Irrevocability, of ASN-0040) means the ownership structure of the address space is *monotonically growing*. New ownership domains are created through delegation but never destroyed. The tree of ownership deepens but never prunes.


## Node-Locality

Ownership authority does not propagate across node boundaries. A principal's effective ownership is bounded by its node prefix.

**O9 (NodeLocalOwnership).** For a principal `π`, the ownership predicate `owns(π, a)` can hold only for allocated addresses `a` whose node field extends the principal's node field:

  `(A π ∈ Π, a ∈ Σ.B : owns(π, a)  ⟹  N(pfx(π)) ≼ N(a))`

We must show that if `owns(π, a)` holds for an allocated address `a`, then `N(pfx(π)) ≼ N(a)` — the principal's node field is a prefix of the address's node field. By O1 (PrefixDetermination), `owns(π, a) ≡ pfx(π) ≼ a`, so the hypothesis gives `pfx(π) ≼ a`: by the Prefix (PrefixRelation) definition of ASN-0034, the components of `pfx(π)` match the leading components of `a`, that is, `#a ≥ #pfx(π)` and `aᵢ = pfx(π)ᵢ` for all `1 ≤ i ≤ #pfx(π)`. By O1a (AccountOwnershipBoundary), `zeros(pfx(π)) ≤ 1`. Two cases exhaust the possibilities.

*Case 1: `zeros(pfx(π)) = 0` (node-level principal).* Every component of `pfx(π)` is strictly positive — T4's positive-component constraint requires that every non-separator component be positive, and the absence of zeros means every component is a non-separator. By T4c (LevelDetermination), a tumbler with no zeros is a node-level address, and by T4b (UniqueParse) its node field is the tumbler itself: `N(pfx(π)) = pfx(π)`, with `#N(pfx(π)) = #pfx(π)`.

Since `pfx(π) ≼ a`, the first `#pfx(π)` components of `a` match those of `pfx(π)` and are therefore all strictly positive. By T4b (UniqueParse), the node field `N(a)` consists of the components of `a` preceding the first zero-valued component (or all components of `a` if no zero occurs). Since positions `1` through `#pfx(π)` of `a` are all positive, the first zero of `a` — if it exists — occurs at position `#pfx(π) + 1` or later. Therefore `#N(a) ≥ #pfx(π) = #N(pfx(π))`. The first `#N(pfx(π))` components of `N(a)` are `a₁, ..., a_{#pfx(π)}`, which equal `pfx(π)₁, ..., pfx(π)_{#pfx(π)}` by the prefix relation, and these are exactly the components of `N(pfx(π))`. Hence `N(pfx(π)) ≼ N(a)`.

Note that the inequality may be strict: TA5(d) permits `inc([1, 2], 1) = [1, 2, 1]` with `zeros = 0`, so addresses with node fields strictly extending the principal's node field exist. In such cases `N(pfx(π)) ≺ N(a)` — the address belongs to a longer node path that shares the principal's node prefix.

*Case 2: `zeros(pfx(π)) = 1` (account-level principal).* By T4b (UniqueParse), T4a (SyntacticEquivalence), and T4's positive-component constraint, the prefix has the form `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ` with `α ≥ 1` and `β ≥ 1` (non-empty field constraint from T4a), where every `Nᵢ > 0` (positive-component constraint from T4) and every `Uⱼ > 0`. The node field is `N(pfx(π)) = [N₁, ..., Nₐ]`, and the single zero sits at position `α + 1`.

Since `pfx(π) ≼ a`, the first `α + 1 + β` components of `a` match those of `pfx(π)`:
- Positions `1` through `α`: `aᵢ = Nᵢ > 0` for each `1 ≤ i ≤ α`.
- Position `α + 1`: `a_{α+1} = 0`, matching the zero separator of `pfx(π)`.
- Positions `α + 2` through `α + 1 + β`: `a_{α+1+j} = Uⱼ > 0` for each `1 ≤ j ≤ β`.

By T4b (UniqueParse), the node field `N(a)` consists of the components of `a` before `a`'s first zero. Since positions `1` through `α` are all positive and position `α + 1` is zero, the first zero of `a` is at position `α + 1`. Hence `N(a) = [a₁, ..., aₐ] = [N₁, ..., Nₐ] = N(pfx(π))`. The prefix relation holds with equality: `N(pfx(π)) = N(a)`, which implies `N(pfx(π)) ≼ N(a)`.

In both cases `N(pfx(π)) ≼ N(a)`. The case distinction is exhaustive by O1a. ∎

The consequence is that ownership cannot cross node boundaries. A principal at node `[1]` cannot own addresses at node `[2]`, because `[1]` is not a prefix of `[2, ...]`. The node field's leading components must match — only the *length* of the node field may differ, and only for node-level principals (Case 1 above).

The same human being would therefore hold *separate, independent* ownership roots on each node — distinct principals with distinct prefixes, distinct domains, and no structural relationship between them. Nelson's "docuverse" is a forest of independently owned trees rooted at nodes, not a single tree with a universal authority. The node operator delegates accounts within its node; those accounts have no automatic standing on any other node.

Gregory's implementation has no cross-node communication, no remote ownership lookup, and no federation of identity. The account tumbler is per-session, per-node. But the abstract property does not depend on these implementation choices — it follows from the prefix geometry of T4 and the structural ownership predicate of O1.

*Formal Contract:*
- *Preconditions:* `π ∈ Π`, `a ∈ Σ.B`, `owns(π, a)`.
- *Postconditions:* `N(pfx(π)) ≼ N(a)`. When `zeros(pfx(π)) = 1`: `N(pfx(π)) = N(a)` (equality). When `zeros(pfx(π)) = 0`: `N(pfx(π)) ≼ N(a)` (proper prefix permitted).


## The Fork as Ownership Boundary

When a principal seeks to modify content it does not own, the system's response is not an error but a creative act. This is the architectural expression of the ownership boundary.

**O10 (DenialAsFork).** When principal `π` requires modification of content at address `a` but `ω(a) ≠ π`, the system provides an alternative: `π` may create a new address `a'` within `dom(π)`:

  (a) `ω(a') = π` — the new address is fully owned by the requesting principal

  (b) the original address `a` is unchanged — no ownership is transferred, no content is modified

  (c) `zeros(a') = zeros(pfx(π)) + 1` — the fork sits exactly one structural tier below the principal's prefix (user level when `π` is node-level, document level when `π` is account-level), reflecting the namespace-vs-content split that the construction `a' = pfx(π).0.{hwm_0 + 1}` produces in a single baptism. Content-bearing depth (element level, `zeros = 3`) is not guaranteed by O10 itself; it requires further organizational baptisms within `dom(a')`, conducted under the same sovereignty.

Condition (a) entails a structural consequence: since `ω(a') = π` gives `pfx(π) ≼ a'`, and the O6 biconditional (`pfx(π) ≼ a' ≡ pfx(π) ≼ acct(a')`, holding for all principals with `zeros(pfx(π)) ≤ 1` — i.e., all principals by O1a) yields `pfx(π) ≼ acct(a')`. The address structure necessarily records the fork within the requesting principal's account domain. This holds for both `zeros = 0` and `zeros = 1`; no case distinction is needed. Condition (c) is enforced by the construction `a' = pfx(π).0.{hwm_0 + 1}` (verified below), not by an additional axiom: the single zero appended in `next(Σ.B, pfx(π), 2)` adds exactly one zero separator to `pfx(π)`, raising the zero count by one regardless of branch (field-opening or sibling-advance). The clause makes formal the namespace-vs-content distinction that the *Forking at greater depth* discussion below develops in prose: O10 guarantees the next structural tier (user from node, document from account), and no more.

Nelson: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links" (LM 2/45). Gregory confirms the structural mechanism: `docreatenewversion`, when invoked on a document belonging to a different account, routes the allocation through `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` — placing the fork under the requesting principal's account, not under the source document.

The forked address lives entirely within `dom(π)`. It satisfies O2 (π is its exclusive owner), O3 corollary (π's account-level ownership is permanent), O5 (π may further subdivide it), and O6 (its provenance records π as the creator). From the ownership model's perspective, the fork is a new independent address that happens to share content identity with the original — a relationship that belongs to the content model, not the ownership model.

We must establish that such an `a'` exists in every reachable state — that `π` can always find an address within `dom(π)` where it remains the effective owner. The argument is unified: a single baptism by `π` produces such an address in every reachable state, with the trajectory length independent of `zeros(pfx(π))`.

*Construction.* Let `hwm_0 := hwm(Σ.B, pfx(π), 2)`, and set `a' = pfx(π).0.{hwm_0 + 1}`. The trajectory is a single baptism `a' = next(Σ.B, pfx(π), 2)`. By ASN-0040's `next` semantics, when `hwm_0 = 0` (no children in `S(pfx(π), 2)`), `next` reduces to the field-opening branch `inc(pfx(π), 2) = pfx(π).0.1` (TA5(d), extending by two positions); when `hwm_0 ≥ 1`, the sibling-advance branch yields `inc(pfx(π).0.{hwm_0}, 0) = pfx(π).0.{hwm_0 + 1}` (TA5(c), same length and zeros count). The resulting `a'` is at user level (`zeros(a') = 1`) when `zeros(pfx(π)) = 0`, and at document level (`zeros(a') = 2`) when `zeros(pfx(π)) = 1`. In both cases `pfx(π) ≼ a'` (the first `#pfx(π)` components of `a'` reproduce `pfx(π)`), so `a' ∈ dom(π)`.

*B6 verification.* The single baptism invokes `Bop(pfx(π), 2)`. ASN-0040's B6 (ValidDepth) requires (i) `T4(pfx(π))`, (ii) `d ∈ {1, 2}`, and (iii) `zeros(pfx(π)) + (d − 1) ≤ 3`. With `d = 2`: by O1a, `zeros(pfx(π)) ∈ {0, 1}`, so `zeros(pfx(π)) + (d − 1) = zeros(pfx(π)) + 1 ∈ {1, 2}`, both bounded by `3`. `T4(pfx(π))` holds via O14's fifth clause for bootstrap principals and via condition (v) of the delegation relation for subsequently introduced principals (preserved by O13). B6 is satisfied; the baptism is a well-defined operation of ASN-0040.

*Non-coverage analysis.* We show `ω_{Σ'}(a') = π` by ruling out sub-delegate coverage of `a'`. Every sub-delegate `π_i` of `π` (i.e., `π_i ∈ Π_Σ` with `pfx(π) ≺ pfx(π_i)`) satisfies `zeros(pfx(π_i)) ≤ 1` by O1a. Classify by the component of `pfx(π_i)` at position `#pfx(π) + 1`:

  - *Form A (`pfx(π).x.…`):* the component at position `#pfx(π) + 1` is strictly positive — either because `pfx(π_i)` extends the node field (`zeros(pfx(π_i)) = 0`, only possible when `zeros(pfx(π)) = 0`) or because the prefix proceeds further within the same field before reaching its zero separator (`zeros(pfx(π_i)) = 1` with the separator strictly later). Coverage of `a'` would require `pfx(π_i)_{#pfx(π) + 1} = a'_{#pfx(π) + 1} = 0`, contradicting Form A's positive component. No Form A sub-delegate covers `a'`.

  - *Form B (`pfx(π).0.Y`):* the component at position `#pfx(π) + 1` is `0` — a zero separator falls immediately after `pfx(π)`. When `zeros(pfx(π)) = 1`, this would consume a second zero (the first already at `pfx(π)`'s own user-field separator), violating O1a's `zeros(pfx(π_i)) ≤ 1`; hence Form B is empty in the `zeros(pfx(π)) = 1` case, and the analysis terminates here. When `zeros(pfx(π)) = 0`, the separator is `pfx(π_i)`'s user-field separator. Length `#pfx(π_i) = #pfx(π) + 1` (so `pfx(π_i) = pfx(π).0`, a trailing zero with empty user field) is excluded by T4 validity (condition (v)); hence `#pfx(π_i) ≥ #pfx(π) + 2`. By T4a (SyntacticEquivalence — non-empty user-field segment requires a positive component immediately after the separator), T4's positive-component constraint, and O1a (`zeros(pfx(π_i)) ≤ 1`), `pfx(π_i)` continues with strictly positive user-field components and no further zero, with first user-field component `U^{(i)}_1 = pfx(π_i)_{#pfx(π) + 2}`. Since `a'` has length exactly `#pfx(π) + 2`, any Form B sub-delegate of length `> #pfx(π) + 2` is not a prefix of `a'` by length alone. A Form B sub-delegate of length exactly `#pfx(π) + 2` (so `pfx(π_i) = pfx(π).0.U^{(i)}_1`) covers `a'` iff `U^{(i)}_1 = hwm_0 + 1`.

  Restricting attention to length-(#pfx(π) + 2) Form B sub-delegates — the only ones that can cover `a'` by length, per the length analysis above — apply PrefixBaptismCoupling: for each such `π_i ∈ Π_Σ`, the entire prefix is `pfx(π_i) = pfx(π).0.U^{(i)}_1`, and PrefixBaptismCoupling places this prefix in `Σ.B`. Hence `pfx(π).0.U^{(i)}_1 ∈ Σ.B`. By ASN-0040's definition of `S(pfx(π), 2)` as the sibling stream of depth-2 tumblers under `pfx(π)` — every element has the form `pfx(π).0.k` for some `k ≥ 1` — the tumbler `pfx(π).0.U^{(i)}_1` lies in `S(pfx(π), 2)`. Combined with its membership in `Σ.B`, we have `pfx(π).0.U^{(i)}_1 ∈ S(pfx(π), 2) ∩ Σ.B`. By B1 (ContiguousPrefix), `children(Σ.B, pfx(π), 2) = {pfx(π).0.k : 1 ≤ k ≤ hwm_0}`, so `pfx(π).0.U^{(i)}_1 ∈ children(Σ.B, pfx(π), 2)` forces `U^{(i)}_1 ≤ hwm_0`. So `U^{(i)}_1 ≠ hwm_0 + 1`, and no length-(#pfx(π) + 2) Form B sub-delegate covers `a'`. Combined with the prior exclusion of longer Form B sub-delegates by length, no Form B sub-delegate covers `a'`.

In both `zeros(pfx(π)) = 0` and `zeros(pfx(π)) = 1` cases, no sub-delegate of `π` covers `a'`. To conclude that `π` itself achieves the unique longest match, we must also rule out competition from non-sub-delegate covering principals. Let `π'' ∈ Π_Σ` be any covering principal of `a'` with `π'' ≠ π` — i.e., `pfx(π'') ≼ a'`. Both `pfx(π'')` and `pfx(π)` are prefixes of `a'`; by the covering-chain lemma (O2's Step 2 — any two prefixes of the same address are `≼`-comparable), they are linearly ordered. Three cases exhaust the comparison: (1) `pfx(π'') = pfx(π)` is excluded by O1b (PrefixInjectivity) given `π'' ≠ π`; (2) `pfx(π) ≺ pfx(π'')` makes `π''` a sub-delegate of `π`, ruled out by the Form A/B analysis above; (3) `pfx(π'') ≺ pfx(π)`, which forces `#pfx(π'') < #pfx(π)`. Only case (3) remains, so every non-`π` covering principal in `Π_Σ` has prefix length strictly less than `#pfx(π)`. Hence `π` achieves the unique longest matching prefix in `Π_Σ` for `a'`, and `ω_{Σ'}(a') = π` (where `Σ'` is the post-baptism state; `Π_{Σ'} = Π_Σ` by O15, since baptism introduces no principals).

*Per-baptism authorization.* The single baptism is performed by `π`, the most-specific covering principal of `a'` at `Σ` (by the non-coverage analysis). O5 (SubdivisionAuthority) is satisfied. B6 holds (verified above). The baptism is authorized.

*Trajectory closure.* The baptism does not modify `Π` (by O15) or remove any pre-existing baptized address from the registry (by B0 Irrevocability of ASN-0040: `Σ.B ⊆ Σ'.B`). The original address `a` remains in `Σ'.B` with its ownership unchanged: `ω_{Σ'}(a) = ω_Σ(a) ≠ π`. The fork postcondition is satisfied: `a' ∈ dom(π) ∩ Σ'.B ∧ ω_{Σ'}(a') = π`, with `a ∈ Σ'.B` unchanged. ∎

> *Unilateral O10★.* In every reachable state `Σ` and for every `π ∈ Π_Σ`, there exists `Σ → Σ'` — a single baptism by `π` alone — witnessing the fork postcondition with `a' = pfx(π).0.{hwm_0 + 1}` ∈ `dom(π) ∩ Σ'.B` and `ω_{Σ'}(a') = π`, where `hwm_0 = hwm(Σ.B, pfx(π), 2)`.

The single-baptism witness is unconditional: PrefixBaptismCoupling ensures every sub-delegate's prefix lies in `Σ.B`, so `hwm_0` already reflects all pre-claimed user-field slots, and `hwm_0 + 1` is never one of them. `π`'s sibling-advance (or field-opening, when `hwm_0 = 0`) lands on a slot it is O5-authorized for and B6-bounded for. This matches Nelson's design intent: "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). The "forevermore" clause forbids ongoing cooperative roles across the parent/sub-delegate boundary; the parent's fork at `hwm_0 + 1` is structurally outside every sub-delegate's authority and structurally inside `π`'s. Gregory's allocator behaves identically: `findpreviousisagr` advances unilaterally past delegated slots, treating the granfilade as the sole source of truth — no inter-session signaling, no shared counter, no lock. The abstract baptismal coupling captures exactly this implementation property.

*Forking at greater depth.* The minimum witness produces an address at user level (`zeros(a') = 1` when `zeros(pfx(π)) = 0`) or document level (`zeros(a') = 2` when `zeros(pfx(π)) = 1`) — one structural tier below `pfx(π)`. The fork postcondition imposes no minimum depth; the consultation confirms that `docreatenewversion`'s unowned-version path through `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` produces exactly the document-level address `pfx(π).0.N` (depth=2, account.0.N form) in one allocation call. A principal may continue baptizing within `dom(a')` to descend further — to document level from user, or to element level for inclusion-link content placement — by repeated O5-authorized field-openings on freshly baptized parents; the descent is `π`'s organizational choice within its sovereignty, not a requirement of O10.

The structural significance of `a'` differs across the two cases. For an account-level principal (`zeros(pfx(π)) = 1`), the single baptism produces a content-bearing document address (`zeros(a') = 2`), and Gregory's `docreatenewversion` exercises this single-call path directly. For a node-level principal (`zeros(pfx(π)) = 0`), the single baptism produces an account-level namespace address (`zeros(a') = 1`) — a structural slot for further allocation, not a content-bearing address. Nelson confines the node operator's role to account allocation ("the host computer allocates accounts," LM 4/19), and the four-field structure Node.0.User.0.Document.0.Element places no content under the bare node field: content addresses have `zeros ≥ 2`. Gregory's implementation provides no single FEBE call from a node-level prefix to a content-bearing document address — the operational path is `CREATENODE_OR_ACCOUNT` to baptize an account slot, then `CREATENEWDOCUMENT` from that account to baptize a document, each its own round-trip with its own B6 check. The O10 postcondition is satisfied at the structural level in both cases — `a'` is fully owned by `π` and the original address `a` is unchanged — but content placement under a node-level principal requires a second baptism `Bop(a', 2)` to descend from the user-level namespace slot to a document-level address (with B6 check `zeros(a') + (d − 1) = 1 + 1 = 2 ≤ 3` ✓, again O5-authorized since `π` remains the most-specific covering principal of any address strictly extending `a'`). The fork *as ownership boundary* (the architectural response O10 captures) is the structural act; content placement is the organizational continuation, conducted under the same sovereignty.

*Formal Contract:*
- *Preconditions:* `Σ` reachable from `Σ₀`, `π ∈ Π_Σ`, `a ∈ Σ.B`, `ω(a) ≠ π`.
- *Postconditions:* `(E Σ', a' : Σ → Σ' ∧ a' ∈ dom(π) ∩ Σ'.B ∧ ω_{Σ'}(a') = π ∧ zeros(a') = zeros(pfx(π)) + 1 ∧ a ∈ Σ'.B)` — there exists a successor state `Σ'` (reached via a single authorized baptism from `Σ`) and a new address `a' = pfx(π).0.{hwm_0 + 1}` (where `hwm_0 := hwm(Σ.B, pfx(π), 2)`) such that `a'` is effectively owned by `π` in `Σ'`, sits exactly one structural tier below `pfx(π)` (clause (c)), and the original address `a` remains allocated and unmodified. The construction satisfies O5 (`π` is the most-specific covering principal of `a'` by the Form A/B classification and O18 baptismal coupling) and ASN-0040's B6 (with `d = 2`, `zeros(pfx(π)) + (d − 1) = zeros(pfx(π)) + 1 ∈ {1, 2} ≤ 3`); `a'` is at user level (`zeros = 1`) when `zeros(pfx(π)) = 0` and at document level (`zeros = 2`) when `zeros(pfx(π)) = 1` — matching the `zeros(a') = zeros(pfx(π)) + 1` clause in both cases. The single-tier guarantee is exact: O10 does not promise content-bearing depth (element level, `zeros = 3`); descent to content placement requires further baptisms inside `dom(a')`, each its own O5-authorized step under `π`'s continuing sovereignty.
- *Unilateral postcondition (Unilateral O10★):* In every reachable state `Σ` and for every `π ∈ Π_Σ`, the existence claim is witnessed by a single baptism `Σ → Σ'` performed by `π` alone, producing `a' = pfx(π).0.{hwm_0 + 1}` ∈ `dom(π) ∩ Σ'.B` with `ω_{Σ'}(a') = π`. The unilateral guarantee is unconditional: PrefixBaptismCoupling ensures every sub-delegate's prefix lies in `Σ.B`, so the depth-2 component of every length-(#pfx(π) + 2) Form B sub-delegate prefix is at most `hwm_0`, and `hwm_0 + 1` is never claimed by any sub-delegate in every reachable state.
- *Invariant:* In every reachable state, every principal can unilaterally produce an address it effectively owns — the fork postcondition is satisfied by `π` alone in a single baptism, in every reachable state.

O10 transforms the ownership boundary from a wall into a fork point. The only "permission" concept the system needs is prefix containment. Everything else — collaboration, annotation, criticism, derivation — is handled by creating new owned addresses and establishing relationships between them. The conventional permission hierarchy (users, groups, roles, ACLs) is replaced by a single structural predicate and an unbounded supply of fresh addresses.


## Principal Identity and the Trust Boundary

One question remains: how does the system know which principal it is speaking to?

Nelson is silent on authentication mechanisms. Gregory's implementation reveals that the trust boundary lies *outside* the ownership model. The backend's `getxaccount` reads whatever tumbler the client sends over the wire and stores it as the session's account — `validaccount` returns TRUE unconditionally in all build configurations. The backend does not verify that the claimed account tumbler corresponds to a legitimate delegation. It trusts the assertion.

This is not a deficiency in the ownership *model* — it is a gap in the ownership *enforcement*. The model itself is clean: O0 through O10 hold regardless of how principal identity is established. The structural predicate `tumbleraccounteq` gives the correct answer for any two tumblers. The question of whether the *right* tumblers are being compared — whether the session's claimed account tumbler is the one the principal is actually entitled to — is a separate concern.

We record this as a scope boundary of the ownership model, not as a property.

*Scope note (Identity is exogenous).* The ownership model treats principal identity as given — it assumes the system has established which principal holds which prefix. The mechanism by which this establishment occurs (authentication, delegation verification, cryptographic binding) is external to the ownership model: the binding `session.account = pfx(π)` is an axiom of the session, not a theorem derivable within O0–O10. Any conforming implementation must provide *some* mechanism for binding sessions to principals, but the ownership properties O0–O10 are independent of which mechanism is chosen. The properties hold for any mapping from sessions to account tumblers, provided the mapping is consistent with the delegation structure.

This scope note records a boundary the model does not cross; it makes no verifiable claim about reachable states and so is not listed among the model's axioms or derived properties.


## Summary of the Model

The ownership model we have derived is spare. It has one predicate (prefix containment), one resolution rule (longest match), and one structural invariant (exclusivity). Everything else follows. Ownership is:

1. *Structural* — computed from the address, not stored (O0, O1)
2. *Account-bounded* — the field structure fixes the granularity (O1a)
3. *Exclusive* — exactly one effective owner per address (O2)
4. *Monotonically refined* — changes only through delegation, never reverses (O3)
5. *Provenance-encoding* — the address records origin inalienably (O6)
6. *Subdivision-gating* — only the owner may create sub-addresses (O5)
7. *Recursively delegable* — delegates receive the same rights (O7)
8. *Irrevocably delegated* — delegation is permanent (O8)
9. *Node-local* — authority is bounded by node prefix (O9)
10. *Fork-inducing at boundaries* — non-ownership produces new ownership (O10)

Principal identity (the binding of a session to a tumbler prefix) is exogenous to this model — see the Scope note in the *Principal Identity and the Trust Boundary* section. The ownership properties O0–O10 hold for any identity-binding mechanism the system chooses.

The design philosophy is clear: minimize the authorization model to the point where the only permission concept needed is prefix containment. The tumbler is not just a name — it is a title deed.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| O0 | Ownership of `a` by `π` is decidable from `pfx(π)` and `a` alone, without mutable state | from O1, Prefix, T3 (verification target of O1's definition) |
| O1 | `owns(π, a) ≡ pfx(π) ≼ a` — ownership is prefix containment | definition |
| O1a | `(A π ∈ Π : zeros(pfx(π)) ≤ 1)` — ownership principals exist only at node or account level | derived invariant; base case O14(iii), preserved by Delegation cond. (iv), O13, O15 |
| O1b | `pfx` is injective — distinct principals have distinct prefixes | derived invariant; base case O14(iv), preserved by Delegation length contradiction, O13, O15 |
| O2 | Every allocated address has exactly one effective owner `ω(a)`, determined by longest matching prefix | from O4, O1b, Prefix, T3, Covering-chain lemma |
| Covering-chain lemma (PrefixesOfCommonAddressAreComparable) | `(A x, p, q ∈ T : p ≼ x ∧ q ≼ x ⟹ p ≼ q ∨ q ≼ p)` — any two tumbler prefixes of a common address are `≼`-comparable | from Prefix, T3 |
| SelfOwnershipAtPrefix | `(A Σ reachable, π ∈ Π_Σ : ω_Σ(pfx(π)) = π)` — every principal effectively owns its own prefix | from O1b, O2, PrefixBaptismCoupling |
| O3 | `ω(a)` changes only through a delegation act introducing a new principal with a strictly longer matching prefix; the postcondition exhibits both the delegator `π_d` and the delegate `π'` — monotonic refinement | from B0 (ASN-0040), O12, O13, O1b, O14, O15 |
| OwnershipDomainPermanence | No external delegation can alter effective ownership within `dom(π)` — changes to `ω(a)` inside a principal's domain arise only from that principal's own acts or its sub-delegates' acts | from Delegation, O1b, O3, O14, O15, Prefix; multi-step corollary OwnershipDomainPermanence★ additionally from B0★ (ASN-0040) |
| O4 | `(A a ∈ Σ.B : (E π ∈ Π : pfx(π) ≼ a))` — every allocated address is covered by some principal | from O14, O16, O5, O12, O13 |
| O5 | Only the principal with the longest matching prefix may allocate within its domain — subdivision authority | axiom |
| AccountPrefix | `(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)` — the account field is a prefix of any valid address | from T3, T4, Prefix, AccountField |
| O6 | `acct(a) = acct(b) ⟹ ω(a) = ω(b)` — effective owner determined entirely by account field | from O1a, O2, O17, AccountPrefix |
| O7 | Delegation (authorized by `delegated`) confers effective ownership (O2), subdivision authority (O5), and recursive delegation (O7) | from Delegation, O2, O5, O15 |
| O8 | `Σ_d reachable ∧ delegated_{Σ_d}(π, π') ∧ Σ_d →⁺ Σ' ∧ π' ∈ Π_{Σ'} ∧ a ∈ dom(π') ∩ Σ'.B ⟹ ω_{Σ'}(a) ≠ π` — delegating parent never regains ownership | from Delegation, O2, O12, O13, O15, B0★ (ASN-0040) |
| O9 | `(A π ∈ Π, a ∈ Σ.B : owns(π, a) ⟹ N(pfx(π)) ≼ N(a))` — ownership bounded by node field | from O1, O1a, T4, Prefix |
| O10 | Non-ownership of target yields a fork: new address `a'` in `dom(π)` with `ω(a') = π`, `zeros(a') = zeros(pfx(π)) + 1` (one structural tier below `pfx(π)`), and original `a` unmodified | from O1a, O1b, O6, PrefixBaptismCoupling, TA5(c), TA5(d), ASN-0040 `next`, ASN-0040 `hwm`, ASN-0040 B6, B0 (ASN-0040) |
| O12 | `(A Σ, Σ' : Σ → Σ' ⟹ Π_Σ ⊆ Π_{Σ'})` — principal persistence | axiom |
| O13 | `pfx_{Σ'}(π) = pfx_Σ(π)` for all transitions — prefix immutability | axiom |
| O14 | `Π₀ ≠ ∅`, initial principals cover all initially allocated addresses, `\|Π₀\| < ∞`, `zeros ≤ 1`, `pfx` injective on `Π₀`, `T4(pfx(π))`, pairwise non-nesting, and every initial principal's prefix lies in `Σ₀.B` — bootstrap with finiteness/O1a/O1b/T4/non-nesting/O18 base cases | axiom |
| O15 | Principals enter Π exclusively through bootstrap or delegation; `\|Π_{Σ'} ∖ Π_Σ\| ≤ 1` per transition | axiom |
| FiniteRegistry | `(A Σ reachable : \|Π_Σ\| < ∞)` — the principal registry is finite in every reachable state | from O14, O15 |
| NestingByDelegation | `(A Σ reachable, π₁ ≠ π₂ ∈ Π_Σ : pfx(π₁), pfx(π₂) non-nesting ∨ delegated_Σ*(π₁, π₂) ∨ delegated_Σ*(π₂, π₁))` — distinct principals are either non-nesting or related by a chain of delegation events | from O1b, O12, O13, O14(vi), O15, delegation condition (vi), covering-chain lemma |
| O16 | `(A a ∈ Σ'.B ∖ Σ.B : (E π ∈ Π_Σ : allocated_by_{Σ'}(π, a)))` — allocation closure | axiom |
| O17 | `(A Σ, a : a ∈ Σ.B ⟹ T4(a))` — every allocated address is a valid tumbler | derived from ASN-0040 B10 |
| O18 | `Σ → Σ' ∧ π' ∈ Π_{Σ'} ∖ Π_Σ ⟹ pfx(π') ∈ Σ'.B ∖ Σ.B` — delegation materially baptizes the delegate's prefix as a fresh registration | axiom |
| PrefixBaptismCoupling | `(A Σ reachable, π ∈ Π_Σ : pfx(π) ∈ Σ.B)` — every principal's prefix is itself baptized in every reachable state | from O13, O14(vii), O15, O18, B0 (ASN-0040) |
| DelegatorAllocatesPrefix | `delegated_Σ(π_d, π') ∧ Σ → Σ' ⟹ allocated_by_{Σ'}(π_d, pfx(π'))` — the delegator is the allocator of the delegate's prefix in the delegation transition | from O18, O16, O5, Delegation condition (ii), O1b, covering-chain lemma |
| `ω_Σ(a)` | `ω_Σ : Σ.B → Π_Σ` — the state-relativized effective owner function (defined only for allocated addresses; both input and output are state-indexed) | from O4, O1b, Prefix, T3 |
| OwnershipDomain | `{a ∈ T : pfx(π) ≼ a}` — the ownership domain of a principal | introduced |
| `acct(a)` | When `zeros(a) = 0`: `acct(a) = a`; when `zeros(a) ≥ 1`: `acct(a) = N(a) ++ [0] ++ U(a)` (concatenation of node field, separator, user field) | from T4b, T3 |
| `allocated_by_Σ(π, a)` | Primitive relation: `a` was allocated by `π` in transition producing `Σ`; mechanism out of scope, constrained by O5 and O16 | axiom |
| Delegation | `π'` introduced into `Π` by act of `π`, with `pfx(π) ≺ pfx(π')`, `π` most-specific covering principal, no existing principal extends `pfx(π')`, `zeros(pfx(π')) ≤ 1`, and `T4(pfx(π'))` | introduced |
| `pfx(π)` | `ownershipPrefix : Principal → Tumbler` — total, codomain constrained to `T4(pfx(π))` | axiom (injectivity O1b and `zeros ≤ 1` O1a are derived invariants, not part of this axiom) |


## Open Questions

- Must the system provide a mechanism for ownership transfer, and if so, what invariants must it preserve given that structural provenance (O6) is inalienable?
- Must the system enforce that no principal can claim an ownership prefix that overlaps an existing principal's domain, and what are the invariants of this enforcement?
- What formal guarantees must the system provide about content accessibility when the effective owner ceases to exist as a principal?
- Must ownership domains be dense (every address in the domain is reachable) or can gaps exist between baptized siblings within a domain?
- What invariants must a cross-node identity federation satisfy to remain consistent with O9, if such federation is introduced?
- What formal relationship must hold between the provenance recorded in an address (O6) and the effective owner (O2) if ownership transfer is permitted?
- Must delegation events be recorded, or is the structural evidence of the address hierarchy sufficient to reconstruct the delegation history?
