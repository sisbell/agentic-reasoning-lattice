# ASN-0042: Tumbler Ownership

*2026-03-15*

We are looking for what it means to *own* a position in the tumbler hierarchy. The tumbler algebra (ASN-0034) gives us a permanently expanding, totally ordered, hierarchically structured address space. But the algebra is silent on authority — it tells us that addresses exist and how they compare, not who may act upon them. Ownership is the layer of meaning that binds addresses to principals.

The investigation yields a central finding: ownership is not a table the system maintains but a *theorem about addresses*. The address itself — through its field structure — encodes its owner. Authorization reduces to prefix comparison. This has consequences for delegation, for the boundaries of authority, and for the architectural response when a principal encounters content it does not own.

We derive each property from Nelson's design intent, corroborated by Gregory's implementation evidence, and state them at the level of abstraction required of any conforming implementation.


## Ownership as a Structural Predicate

We begin with the most fundamental question: how does the system determine who owns an address?

Nelson gives a striking answer. Ownership is not recorded in a registry external to the address — it is *readable from the address itself*:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." (LM 4/17)

Gregory's implementation confirms this with unusual force. The sole ownership predicate in udanax-green — `isthisusersdocument` — delegates entirely to `tumbleraccounteq`, a function that compares two tumbler mantissa arrays digit by digit. No table is consulted. No file is opened. No registry is queried. The function receives two tumblers, performs arithmetic on their components, and returns a boolean. If we removed the function and replaced it with any other function that performs the same comparison, the system's ownership behavior would be identical. Ownership *is* the comparison.

**pfx(π) (OwnershipPrefix).**

We introduce the principals. Let `Π` denote the set of *principals* — the ownership subjects. Each principal `π ∈ Π` is associated with an *ownership prefix* `pfx(π) ∈ T`, a valid tumbler (satisfying T4) that serves as the root of their namespace. The mapping `pfx` is injective — distinct principals have distinct prefixes (formalized as O1b below).

The mapping `pfx` is a primitive of the ownership model — it is posited, not derived. We justify its well-formedness. Nelson's architecture requires that every principal possess a namespace root readable from the address itself: "numbers are owned by individuals or companies, and subnumbers under them are bestowed" (LM 4/17). The mapping `pfx` formalizes this assignment — each principal receives the tumbler that roots its namespace. The codomain constraint `pfx(π) ∈ T` places the prefix in the tumbler space; the validity requirement T4 (FieldSeparatorConstraint) ensures that zero-valued components parse unambiguously as field separators, that field extraction via T6 is well-defined, and that the hierarchical level `zeros(pfx(π))` — on which the account-level boundary O1a depends — is determinate. Without T4, the prefix comparison `pfx(π) ≼ a` used in the ownership predicate O1 might not be computable, because the prefix relation T5 requires component-wise comparison of well-defined components, which T4 (through T3) guarantees. The remaining structural constraints — injectivity (O1b) and `zeros(pfx(π)) ≤ 1` (O1a) — are stated and proved as separate properties. ∎

*Formal Contract:*
- *Axiom:* `pfx : Π → T` is a total mapping assigning each principal its ownership prefix.
- *Preconditions:* `π ∈ Π`.
- *Postconditions:* (a) `pfx(π) ∈ T`. (b) `T4(pfx(π))` — the prefix is a valid tumbler satisfying FieldSeparatorConstraint. (c) Injectivity: stated separately as O1b. (d) Account-level boundary: stated separately as O1a.

**O1b (PrefixInjectivity).** `(A π₁, π₂ ∈ Π : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

Without injectivity, two principals sharing a prefix could both claim longest-match, and the effective owner function `ω` (defined in O2 below) would not yield a unique result.

The ownership question "does `π` own `a`?" is answered by examining these two tumblers alone:

**O0 (StructuralOwnership).** Whether principal `π` owns address `a` is decidable from `pfx(π)` and `a` alone, without consulting any mutable system state.

The decision procedure is prefix containment:

**O1 (PrefixDetermination).** Principal `π` owns address `a` iff `pfx(π)` is a prefix of `a`:

  `owns(π, a)  ≡  pfx(π) ≼ a`

where `p ≼ a` denotes that `p` is a prefix of `a` in the sense of T5 — the components of `p` match the leading components of `a`.

O1 is a definition: we define the ownership predicate `owns(π, a)` to be identical with prefix containment `pfx(π) ≼ a`. We verify that the definition is well-formed and that it satisfies the decidability requirement O0.

*Well-formedness.* The prefix relation `≼` is defined by T5: `p ≼ a ⟺ #a ≥ #p ∧ (A i : 1 ≤ i ≤ #p : pᵢ = aᵢ)`. For `owns(π, a)` to be well-defined, two conditions must hold. First, `pfx(π)` must be a valid tumbler — this holds by the definition of `pfx`, which requires every principal's prefix to satisfy T4 (FieldSeparatorConstraint). Second, the component-wise comparison must be determinate — by T3 (CanonicalRepresentation), each component `pᵢ` and `aᵢ` is a uniquely determined natural number, so equality at each position is decidable.

*Decidability.* The prefix check `pfx(π) ≼ a` requires one length comparison `#a ≥ #pfx(π)` followed by at most `#pfx(π)` component comparisons, each a comparison of natural numbers. The entire computation uses `pfx(π)` and `a` alone, consulting no mutable system state. This satisfies the design requirement O0 (StructuralOwnership): ownership is decidable from the prefix and the address without external state.

*Design justification.* Nelson states that "numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies" (LM 4/17) — ownership is legible from the address itself. Gregory's `tumbleraccounteq` confirms the decision procedure: it walks the mantissa arrays of two tumblers in lockstep, comparing components. The definition `owns(π, a) ≡ pfx(π) ≼ a` formalizes this structural containment exactly. ∎

*Formal Contract:*
- *Definition:* `owns(π, a) ≡ pfx(π) ≼ a`, where `≼` is the prefix relation of T5.
- *Preconditions:* `π ∈ Π`, `a ∈ T`, `T4(pfx(π))`, `T4(a)`.
- *Postconditions:* `owns(π, a)` is a total, decidable predicate on `Π × T`.


## The Account-Level Boundary

Not every prefix match constitutes an ownership claim. The tumbler hierarchy has four structural levels — node, user, document, element — separated by zero-valued components (T4). The allocation mechanism is uniform across all levels — any address holder can subdivide — but ownership authority is hierarchical, and the hierarchy has a definite floor.

Nelson is explicit on this point: "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). This is the strongest authority statement in the specification, and it appears only at the account level. At the document level, ownership is defined with specific enumerated rights: "only the owner has a right to withdraw a document or change it" (LM 2/29). At the version level, Nelson is deliberately cautious: "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation" (LM 4/29). The design intent is clear: baptism (allocation) is uniform; authority (ownership) flows from the account. Everyone at every level can fork sub-addresses — that is the mechanism. But what one can *do* with what one has forked depends on one's position in the ownership hierarchy.

We formalize this asymmetry:

**O1a (AccountOwnershipBoundary).** Ownership principals exist only at node level or account level:

  `(A π ∈ Π : zeros(pfx(π)) ≤ 1)`

Sub-account allocation — creating documents, versions, elements — does not introduce new ownership principals. It exercises the allocator's rights within an existing principal's domain.

**acct(a) (AccountField).**

Define `acct(a)` for any valid tumbler `a`: when `zeros(a) = 0` (node-level), `acct(a) = a`; when `zeros(a) ≥ 1`, `acct(a)` is the tumbler whose components are `N(a)` followed by `[0]` followed by `U(a)` — using the foundation's field extraction functions (T6) — having `zeros(acct(a)) = 1`.

Gregory confirms the account-level boundary with unusual force. His `tumbleraccounteq` walks the mantissa of both tumblers in lockstep. For each non-zero component in the account tumbler, the document's component must match. For each zero, the counter advances. When the counter reaches two — the second zero — the function returns true unconditionally. Everything beyond the second zero is ignored. The implementation has no mechanism for finer-grained discrimination: `isthisusersdocument` (in all three build targets — `be.c`, `socketbe.c`, `xumain.c`) delegates directly to `tumbleraccounteq` with no intervening check. There is no per-document, per-version, or per-element authorization predicate anywhere in the codebase. The BERT system tracks per-document open/close state, but its authorization fallback is `isthisusersdocument` — account-level.

The consequence: sub-account allocation (creating documents, versions, elements) creates addresses within the allocating principal's domain but does not partition that domain into sub-ownerships. A document address `N.0.U.0.D.0.E` and a different document address `N.0.U.0.D'.0.E'` under the same account are owned by the same principal — the one whose prefix matches `N.0.U`. Below the account level, there is only the binary distinction of "mine" versus "not mine."

O1a permits nesting *within* the account level. T4 allows multi-component user fields: `pfx(π₁) = [1, 0, 2]` and `pfx(π₂) = [1, 0, 2, 3]` both satisfy `zeros ≤ 1`, and `pfx(π₁) ≺ pfx(π₂)`. Nelson designed this deliberately: "accounts can spin off accounts" (LM 4/19). The User field is a tree, not a flat namespace — a principal may delegate a sub-account by forking a longer user field within its own prefix. Gregory confirms: `tumbleraccounteq` applied to account `[1, 0, 2, 3]` checks positions 0, 2, and 3, while account `[1, 0, 2]` checks only positions 0 and 2 — the child account is a strict refinement. What O1a prevents is *document-level* or *element-level* principals: no principal has `zeros(pfx(π)) ≥ 2`. The floor of ownership is the account level, but within that floor, the user-field tree can grow arbitrarily deep.

We must show that `acct(a)` is well-defined for every valid tumbler `a` satisfying T4, that it produces a valid tumbler, and that its zero count is as claimed. The argument proceeds by cases on `zeros(a)`.

*Case `zeros(a) = 0`.* The tumbler `a` contains no zero-valued components, so by T4(c) (the zero count determines the hierarchical level bijectively), `a` is a node-level tumbler: the entire sequence constitutes the node field `N(a)`, and no user, document, or element fields are present. The definition stipulates `acct(a) = a`. This is well-defined: `a` is a valid tumbler by hypothesis, and `zeros(acct(a)) = zeros(a) = 0 ≤ 1`.

*Case `zeros(a) = 1`.* By T4(b), `fields(a)` decomposes `a` uniquely into a node field `N(a)` and a user field `U(a)`, separated by a single zero. No document or element fields are present. The definition stipulates `acct(a) = N(a) ++ [0] ++ U(a)`. But this concatenation reconstructs `a` itself — the entire tumbler is `N(a)` followed by one zero followed by `U(a)`, with no further components. Hence `acct(a) = a`. Validity: `a` satisfies T4 by hypothesis, and `zeros(acct(a)) = zeros(a) = 1`.

*Case `zeros(a) = 2`.* By T4(b), `fields(a)` decomposes `a` uniquely into `N(a)`, `U(a)`, and `D(a)`, with the structure `N(a) ++ [0] ++ U(a) ++ [0] ++ D(a)`. By T4(a), each field has at least one component, and all field components are strictly positive. Define `acct(a) = N(a) ++ [0] ++ U(a)`. The node field `N(a)` has `α ≥ 1` components, all strictly positive (by T4(a)); the user field `U(a)` has `β ≥ 1` components, all strictly positive. The constructed tumbler therefore has length `α + 1 + β`, begins and ends with a positive component (no leading or trailing zero), contains exactly one zero (at position `α + 1`), and has no adjacent zeros (the zero is flanked by the last component of `N(a)` and the first component of `U(a)`, both positive by T4). It satisfies T4 and has `zeros(acct(a)) = 1`.

*Case `zeros(a) = 3`.* By T4(b), `fields(a)` decomposes `a` uniquely into `N(a)`, `U(a)`, `D(a)`, and `E(a)`, with the structure `N(a) ++ [0] ++ U(a) ++ [0] ++ D(a) ++ [0] ++ E(a)`. Define `acct(a) = N(a) ++ [0] ++ U(a)`. By the same reasoning as the `zeros(a) = 2` case — `N(a)` and `U(a)` each have at least one strictly positive component by T4(a) — the constructed tumbler has exactly one zero, no adjacent zeros, no leading or trailing zero, and all non-separator components positive. It satisfies T4 and has `zeros(acct(a)) = 1`.

The case distinction is exhaustive: T4 constrains `zeros(a) ∈ {0, 1, 2, 3}`, and each value is handled. In every case, `acct(a)` is a valid tumbler satisfying T4, and `zeros(acct(a)) ≤ 1`. The field extraction functions `N(a)` and `U(a)` are uniquely determined by T4(b) and decidable by T6, so the construction is computable from `a` alone. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T` is a valid tumbler satisfying T4 (positive-component constraint, at most three zeros, no adjacent zeros, no leading or trailing zero).
- *Definition:* `acct(a) = a` when `zeros(a) = 0`; `acct(a) = N(a) ++ [0] ++ U(a)` when `zeros(a) ≥ 1`, where `N(a)` and `U(a)` are the node and user fields extracted by `fields(a)` (T4(b)), decidable by T6.
- *Postconditions:* (a) `acct(a)` is a valid tumbler satisfying T4. (b) `zeros(acct(a)) ≤ 1`. (c) When `zeros(a) ≤ 1`: `acct(a) = a`. (d) When `zeros(a) ≥ 2`: `acct(a)` is a proper prefix of `a` with `zeros(acct(a)) = 1`.


## Ownership Domains

Each principal's prefix determines a set of addresses — their *domain*:

**Definition (OwnershipDomain).** For principal `π ∈ Π`, define `dom(π) = {a ∈ T : pfx(π) ≼ a}`.

By T5 (ContiguousSubtrees), every ownership domain is a contiguous interval under the lexicographic order T1. This is a mathematical consequence of prefix containment and the tree-to-line mapping, not a policy choice. If `a, c ∈ dom(π)` and `a ≤ b ≤ c`, then `b ∈ dom(π)`. No address can escape from the interior of someone's domain.

Domains nest whenever prefixes nest:

  `pfx(π₁) ≼ pfx(π₂)  ⟹  dom(π₂) ⊆ dom(π₁)`

The proof is one step: if `a ∈ dom(π₂)` then `pfx(π₂) ≼ a`, and since `pfx(π₁) ≼ pfx(π₂)`, transitivity of the prefix relation gives `pfx(π₁) ≼ a`, hence `a ∈ dom(π₁)`. This covers all nesting cases — both cross-level (a node operator's domain containing an account domain) and same-level (an account holder's domain containing a sub-account domain, as when `pfx(π₁) = [1, 0, 2]` and `pfx(π₂) = [1, 0, 2, 3]` both satisfy O1a with `zeros = 1`).

As a corollary, when the nesting is cross-level — `zeros(pfx(π₁)) < zeros(pfx(π₂))` — the containing principal operates at a strictly higher level of the field hierarchy (node containing account, for instance). But the defining condition is prefix containment alone, not the zero count.


## State Axioms

The ownership model rests on five axioms about state evolution that the subsequent derivations assume. We state them explicitly.

**O12 (PrincipalPersistence).** Once a principal joins Π, no operation removes it:

  `(A Σ, Σ' : Σ → Σ' ⟹ Π_Σ ⊆ Π_{Σ'})`

Nelson's architecture contains no concept of account revocation. Gregory's codebase contains no deletion path for account entries. Addresses are permanent (T8), and a principal's prefix is a valid tumbler — removing a principal would reverse the refinement of `ω` for addresses in its domain (violating O3's monotonic refinement below) and undo a delegation act (violating O8's irrevocability below).

**O13 (PrefixImmutability).** Once established, a principal's ownership prefix cannot be altered:

  `(A π ∈ Π_Σ, Σ, Σ' : Σ → Σ' ∧ π ∈ Π_{Σ'} ⟹ pfx_{Σ'}(π) = pfx_Σ(π))`

The prefix is a tumbler, and the tumbler algebra provides no operation that mutates an existing tumbler in place. Since addresses are permanent (T8) and the prefix is structurally embedded in its domain's addresses, altering it would require rewriting every address in the domain — an operation the system does not support.

**O14 (BootstrapPrincipal).** The initial state contains at least one principal whose domain covers all initially allocated addresses, and the initial principals satisfy the structural constraints that O1a, O1b, T4, and pairwise non-nesting require of all bootstrap principals:

  `Π₀ ≠ ∅  ∧  (A a ∈ Σ₀.alloc : (E π ∈ Π₀ : pfx(π) ≼ a))`

  `(A π ∈ Π₀ : zeros(pfx(π)) ≤ 1)`

  `(A π₁, π₂ ∈ Π₀ : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

  `(A π ∈ Π₀ : T4(pfx(π)))`

  `(A π₁, π₂ ∈ Π₀ : π₁ ≠ π₂ ⟹ pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁))`

The second clause is the base case for O1a: every initial principal has a node-level or account-level prefix. The third clause is the base case for O1b: no two initial principals share a prefix. The fourth clause is the base case for T4: every initial principal's prefix is a valid tumbler address. The fifth clause requires pairwise non-nesting: no bootstrap principal's prefix extends another's. Without this, a bootstrapped principal could nest within another's domain — modifying `ω` for addresses in that domain through delegation acts the covering principal never authorized — and the Account-level permanence Corollary would fail. Together with the inductive steps — delegation preserves O1a via condition (iv), O1b via the length contradiction (shown below), and T4 via condition (v) — these clauses establish that O1a, O1b, and T4 hold in every reachable state.

In a single-node system, `Π₀ = {π_N}` where `π_N` is the node operator with a node-level prefix (`zeros = 0 ≤ 1`); non-nesting holds vacuously (a singleton set has no distinct pairs), and all other base-case clauses hold trivially — a single-component positive tumbler like `[1]` satisfies T4 (no zeros, no adjacency or boundary violations). In a multi-node system, `Π₀` contains one initial principal per node (e.g., principals at `[1]` and `[2]`), each independently covering its node's allocatable addresses. These are node-level prefixes (satisfying the second clause), distinct node addresses are distinct tumblers (satisfying the third clause by T3), each is a positive single-component tumbler satisfying T4 (satisfying the fourth clause), and no single-component positive tumbler is a prefix of another single-component positive tumbler with a different value (satisfying the fifth clause). The formalization permits both cases: the existential quantifier ranges over all of `Π₀`, not a single distinguished element. Without these base cases, the inductive arguments for O1a, O1b, T4, and O4 cannot begin.

**O15 (PrincipalClosure).** Principals enter Π exclusively through bootstrap (in Π₀) or delegation (satisfying the `delegated` relation defined below). No other mechanism introduces principals. Each state transition introduces at most one new principal:

  `(A Σ, Σ' : Σ → Σ' ⟹ |Π_{Σ'} ∖ Π_Σ| ≤ 1)`

  `(A π' ∈ Π_{Σ'} ∖ Π_Σ : (E π ∈ Π_Σ : delegated_Σ(π, π')))`

Without this closure, O12 permits arbitrary growth of Π — a mechanism outside the delegation relation could introduce a principal at document level (violating O1a) or within a sub-domain without the effective owner's consent (circumventing the authorization guarantee of delegation condition (ii)). Nelson's design contains no concept of principals appearing outside the delegation hierarchy, and Gregory's codebase provides no mechanism for it. The at-most-one constraint reflects the atomic nature of a delegation act: one delegator, one delegate, one prefix.

**allocated_by_Σ(π, a) (AllocatedBy).**

We take `allocated_by_Σ(π, a)` — "address `a` was allocated by principal `π` in the transition producing state `Σ`" — as a primitive relation of the ownership model. Its mechanism (the baptism procedure that generates addresses and enters them into `Σ.alloc`) is out of scope; what the ownership model constrains is its signature and the properties it must satisfy (O5, O16). The signature:

  `allocated_by_Σ : Principal × Tumbler → Bool`

This relation is primitive — it admits no derivation within the ownership model, and we justify its status as such. The ownership model's purpose is to constrain *who may allocate where* and to guarantee *that every allocation has an author*; the model does not define the mechanism by which allocation occurs. That mechanism belongs to the tumbler baptism specification, which produces the concrete act of generating an address and entering it into `Σ.alloc`. The ownership model receives this act as a fact — `allocated_by_{Σ'}(π, a)` holds precisely when the baptism procedure, executing on behalf of principal `π`, produced address `a` during the transition to state `Σ'` — and imposes two constraints upon it. First, O5 (SubdivisionAuthority) requires that the allocator be the most-specific covering principal: if `allocated_by_{Σ'}(π, a)` then `pfx(π) ≼ a` and no `π' ∈ Π_Σ` has a longer prefix that also covers `a`. Second, O16 (AllocationClosure) requires that every newly allocated address have an allocator: if `a ∈ Σ'.alloc ∖ Σ.alloc` then some `π ∈ Π_Σ` satisfies `allocated_by_{Σ'}(π, a)`. Together, O5 and O16 fully constrain the relation's behavior without defining its implementation. The relation's well-definedness is an obligation on any conforming baptism specification; the ownership model treats it as axiomatic. ∎

*Axiom:* `allocated_by_Σ(π, a)` is a primitive relation of the ownership model.
- *Signature:* `allocated_by_Σ : Principal × Tumbler → Bool`
- *Semantics:* `allocated_by_{Σ'}(π, a)` holds when the baptism procedure, executing on behalf of `π`, produced `a` during the transition yielding `Σ'`.
- *Constraints:* O5 (SubdivisionAuthority) — allocator is most-specific covering principal; O16 (AllocationClosure) — every new address has an allocator.
- *Mechanism:* Out of scope; belongs to the tumbler baptism specification.

**O16 (AllocationClosure).** Every address entering `Σ.alloc` in a state transition was allocated by some principal in `Π_Σ`:

  `(A Σ, Σ', a : Σ → Σ' ∧ a ∈ Σ'.alloc ∖ Σ.alloc  ⟹  (E π ∈ Π_Σ : allocated_by_{Σ'}(π, a)))`

This is the address-side counterpart of O15: just as principals enter Π exclusively through bootstrap or delegation, addresses enter `Σ.alloc` exclusively through allocation by an existing principal. Without this closure, addresses could appear in `Σ.alloc` through mechanisms outside the ownership model — the derivation of O4 requires that every newly allocated address was allocated by some principal, and O5 alone provides only the conditional form (if `π` allocated `a`, then `pfx(π) ≼ a`), not the existential (some `π` allocated `a`). Gregory confirms: every allocation path in udanax-green originates from a session with an account tumbler — there is no mechanism for addresses to appear without an allocating principal.

**O17 (AllocatedAddressValidity).** Every allocated address is a valid tumbler:

  `(A Σ, a : a ∈ Σ.alloc ⟹ T4(a))`

This axiom is load-bearing: `acct(a)` and `N(a)` depend on FieldParsing (ASN-0034), which requires T4 validity for well-defined field boundaries. Without it, O6's proof (which uses AccountPrefix, requiring `T4(a)`) and O9's proof (which uses `N(a)`, requiring `T4(a)`) have gaps. In the initial state, `(A a ∈ Σ₀.alloc : T4(a))`. For the inductive step, any conforming allocation mechanism must produce addresses satisfying T4 — this is an obligation on the baptism specification (out of scope) that the ownership model requires as an axiom.


## The Exclusivity Invariant

Can two principals simultaneously own the same address?

Nelson uses the definite article throughout: "*the* owner of a given item" (LM 4/20), not "an owner." Gregory's predicate returns a boolean — true or false, with no provision for multiple true results from distinct principals. The system requires exactly one effective owner per address.

For non-nesting prefixes, T10 (PartitionIndependence) gives disjointness immediately: two principals whose prefixes satisfy `pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁)` have disjoint domains. The interesting case is nested domains — when a node operator's domain contains an account holder's. Here, Nelson is explicit: the node operator creates accounts, but "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). Delegation permanently transfers effective ownership of the subdomain.

We first state a coverage requirement — every allocated address falls within some principal's domain:

**O4 (DomainCoverage).** For every allocated address, at least one principal's prefix contains it:

  `(A a ∈ Σ.alloc : (E π ∈ Π : pfx(π) ≼ a))`

We prove that in every reachable state `Σ`, every allocated address is covered by at least one principal's prefix. The proof is by induction on the length of the transition sequence leading to `Σ`.

*Base case.* In the initial state `Σ₀`, the claim is `(A a ∈ Σ₀.alloc : (E π ∈ Π₀ : pfx(π) ≼ a))`. This is the second clause of O14 (BootstrapPrincipal), which asserts exactly that the initial principals cover all initially allocated addresses. The base case holds.

*Inductive step.* Assume the claim holds in state `Σ`: every `a ∈ Σ.alloc` has a covering principal in `Π_Σ`. We must show it holds in any successor state `Σ'` with `Σ → Σ'`. Let `a ∈ Σ'.alloc` be an arbitrary allocated address. Two cases arise, exhausting `Σ'.alloc = Σ.alloc ∪ (Σ'.alloc ∖ Σ.alloc)`.

*Case 1: `a ∈ Σ.alloc` (address was already allocated).* By the inductive hypothesis, there exists `π ∈ Π_Σ` with `pfx(π) ≼ a`. By O12 (PrincipalPersistence), `Π_Σ ⊆ Π_{Σ'}`, so `π ∈ Π_{Σ'}`. By O13 (PrefixImmutability), `pfx_{Σ'}(π) = pfx_Σ(π)`, so the prefix relation `pfx_{Σ'}(π) ≼ a` is preserved. Hence `a` has a covering principal in `Π_{Σ'}`.

*Case 2: `a ∈ Σ'.alloc ∖ Σ.alloc` (address is newly allocated).* By O16 (AllocationClosure), there exists a principal `π ∈ Π_Σ` such that `allocated_by_{Σ'}(π, a)` — every newly allocated address was allocated by some existing principal. By O5 (SubdivisionAuthority), whenever `π` allocates `a`, the first conjunct of the postcondition gives `pfx(π) ≼ a` — the allocator's prefix covers the allocated address. By O12, `π ∈ Π_Σ ⊆ Π_{Σ'}`, and by O13, `pfx_{Σ'}(π) = pfx_Σ(π)`. Hence `pfx_{Σ'}(π) ≼ a`, and `a` has a covering principal in `Π_{Σ'}`.

In both cases, every address in `Σ'.alloc` is covered by a principal in `Π_{Σ'}`. By induction on the transition sequence, the coverage invariant holds in every reachable state. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ Σ.alloc`.
- *Postconditions:* `(E π ∈ Π : pfx(π) ≼ a)`.
- *Invariant:* Coverage holds in every reachable state — no allocated address is orphaned from the principal hierarchy.

We resolve nesting by specificity:

**O2 (OwnershipExclusivity).** For every allocated address `a`, there exists exactly one principal that effectively owns `a`:

  `(A a ∈ Σ.alloc : (E! π ∈ Π : ω(a) = π))`

We prove that for every allocated address `a`, there exists exactly one principal satisfying `ω(a) = π`, where `ω(a)` denotes the principal with the longest matching prefix: `ω(a) = π ≡ pfx(π) ≼ a ∧ (A π' ∈ Π : π' ≠ π ∧ pfx(π') ≼ a ⟹ #pfx(π) > #pfx(π'))`. The proof decomposes into existence and uniqueness.

*Existence.* Let `C(a) = {π ∈ Π : pfx(π) ≼ a}` denote the set of principals whose prefix covers `a`. By O4 (DomainCoverage), `C(a) ≠ ∅` for every `a ∈ Σ.alloc` — every allocated address falls within at least one principal's domain. We must show that `C(a)` admits a unique longest-prefix element.

The prefixes of principals in `C(a)` are totally ordered by the prefix relation. Let `p₁ = pfx(π₁)` and `p₂ = pfx(π₂)` for arbitrary `π₁, π₂ ∈ C(a)`, and suppose without loss of generality that `#p₁ ≤ #p₂`. Since `p₁ ≼ a`, we have `(p₁)ᵢ = aᵢ` for all `i ≤ #p₁`. Since `p₂ ≼ a`, we have `(p₂)ᵢ = aᵢ` for all `i ≤ #p₂`. For each `i ≤ #p₁`, both equalities hold, yielding `(p₁)ᵢ = aᵢ = (p₂)ᵢ`. Since `p₁` agrees with `p₂` on all `#p₁` components and `#p₁ ≤ #p₂`, we have `p₁ ≼ p₂`. Therefore any two prefixes in `{pfx(π) : π ∈ C(a)}` are comparable under `≼` — the covering set is a chain.

The set `C(a)` is finite: each covering prefix `p ≼ a` is uniquely determined by its length — it equals `[a₁, …, a_{#p}]` — and there are at most `#a` possible lengths, so `|C(a)| ≤ #a`.

A non-empty finite totally ordered set has a maximum. Therefore there exists a unique maximal length `ℓ* = max{#pfx(π) : π ∈ C(a)}`, and exactly one prefix of that length covers `a` (since the covering prefix of length `ℓ*` is determined: it must be `[a₁, …, a_{ℓ*}]`). Hence there exists a principal `π* ∈ C(a)` with `#pfx(π*) = ℓ*` satisfying the definition of `ω(a)`.

*Uniqueness.* Suppose for contradiction that two distinct principals `π₁ ≠ π₂` both satisfy `ω(a) = π₁` and `ω(a) = π₂`. Then both achieve the longest matching prefix: `#pfx(π₁) = #pfx(π₂) = ℓ*`. Since both prefixes cover `a` and share the same length, `pfx(π₁) = [a₁, …, a_{ℓ*}] = pfx(π₂)`. By O1b (PrefixInjectivity), `pfx(π₁) = pfx(π₂)` implies `π₁ = π₂`, contradicting the assumption of distinctness. Therefore `ω(a)` is unique.

We conclude: for every `a ∈ Σ.alloc`, there exists exactly one `π ∈ Π` with `ω(a) = π`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ Σ.alloc`.
- *Postconditions:* `(E! π ∈ Π : ω(a) = π)`.
- *Invariant:* Exclusivity holds in every reachable state — `ω` is a total function on `Σ.alloc`.

**ω(a) (EffectiveOwner).**

where `ω(a)` — the *effective owner* — is the principal with the longest matching prefix:

  `ω(a) = π  ≡  pfx(π) ≼ a  ∧  (A π' ∈ Π : π' ≠ π ∧ pfx(π') ≼ a : #pfx(π) > #pfx(π'))`

We prove that `ω` is a well-defined total function on `Σ.alloc` — that is, for every allocated address `a`, there exists exactly one principal `π` satisfying the defining equivalence. The argument decomposes into four steps: non-emptiness of the covering set, total ordering of covering prefixes, finiteness, and uniqueness of the witnessing principal.

*Step 1: Non-emptiness.* Let `a ∈ Σ.alloc` and define `C(a) = {π ∈ Π : pfx(π) ≼ a}`, the set of principals whose prefix covers `a`. By O4 (DomainCoverage), every allocated address falls within at least one principal's domain, so `C(a) ≠ ∅`.

*Step 2: Total ordering of covering prefixes.* We show that the prefixes `{pfx(π) : π ∈ C(a)}` form a chain under the prefix relation `≼`. Let `π₁, π₂ ∈ C(a)` be arbitrary, with `p₁ = pfx(π₁)` and `p₂ = pfx(π₂)`. Suppose without loss of generality that `#p₁ ≤ #p₂`. Since `p₁ ≼ a`, by T5 (PrefixRelation) we have `(p₁)ᵢ = aᵢ` for all `1 ≤ i ≤ #p₁`. Since `p₂ ≼ a`, we have `(p₂)ᵢ = aᵢ` for all `1 ≤ i ≤ #p₂`. For each `i` with `1 ≤ i ≤ #p₁`, both equalities hold, so `(p₁)ᵢ = aᵢ = (p₂)ᵢ`. The tumbler `p₁` agrees with `p₂` on all `#p₁` components, and `#p₁ ≤ #p₂`, so by T5 we have `p₁ ≼ p₂`. Since `π₁, π₂` were arbitrary members of `C(a)`, any two covering prefixes are comparable — the covering set is a chain.

*Step 3: Finiteness.* Each covering prefix `p ≼ a` is uniquely determined by its length: since `p ≼ a` requires `pᵢ = aᵢ` for all `1 ≤ i ≤ #p`, the prefix of length `k` covering `a` can only be `[a₁, …, a_k]`. By T3 (CanonicalRepresentation), each component `aᵢ` is a uniquely determined natural number, so this prefix is unique. There are at most `#a` possible lengths (from `1` to `#a`), so `|C(a)| ≤ #a`. The covering set is finite.

*Step 4: Existence and uniqueness of the maximum.* A non-empty finite chain has a unique maximum. Therefore there exists a unique maximal length `ℓ* = max{#pfx(π) : π ∈ C(a)}`, and by Step 3 the covering prefix of length `ℓ*` is uniquely determined as `[a₁, …, a_{ℓ*}]`. It remains to show that exactly one principal holds this prefix. Suppose `π₁, π₂ ∈ C(a)` both satisfy `#pfx(π₁) = #pfx(π₂) = ℓ*`. By Step 3, `pfx(π₁) = [a₁, …, a_{ℓ*}] = pfx(π₂)`. By O1b (PrefixInjectivity), equal prefixes imply `π₁ = π₂`. Hence there is exactly one principal `π* ∈ C(a)` achieving the maximal prefix length, and `π*` satisfies the defining equivalence: `pfx(π*) ≼ a` and for every `π' ≠ π*` with `pfx(π') ≼ a`, `#pfx(π*) > #pfx(π')`.

We conclude: for every `a ∈ Σ.alloc`, there exists exactly one `π ∈ Π` with `ω(a) = π`. The function `ω : Σ.alloc → Π` is total and well-defined in every reachable state. ∎

*Formal Contract:*
- *Definition:* `ω(a) = π ≡ pfx(π) ≼ a ∧ (A π' ∈ Π : π' ≠ π ∧ pfx(π') ≼ a ⟹ #pfx(π) > #pfx(π'))`.
- *Preconditions:* `a ∈ Σ.alloc`.
- *Postconditions:* `(E! π ∈ Π : ω(a) = π)` — exactly one principal satisfies the defining equivalence.
- *Invariant:* `ω` is a total function on `Σ.alloc` in every reachable state.

The exclusivity of ownership is load-bearing. If two parties owned the same address, the system could not determine who is entitled to subdivide the space beneath it (O5 below), who originated the content (O6 below), or whose delegation created the address. Every downstream property depends on O2.


## Permanence and Refinement

Nelson is emphatic: ownership does not expire.

> "Once assigned a User account, the user will have full control over its subdivision forevermore." (LM 4/29)

"Forevermore" is strong language in a technical specification. But the naive reading — that `ω(a)` never changes — is too strong. Consider a node operator `π₁` with `pfx(π₁) = [1]`. Before any delegation, `ω(a) = π₁` for every address `a` with node field `1`. When `π₁` delegates account prefix `[1, 0, 2]` to principal `π₂`, the effective owner of every address under `[1, 0, 2]` changes from `π₁` to `π₂` — the longer prefix wins. Nelson's "forevermore" does not mean `ω` never changes; it means the *account holder's* sovereignty is permanent — changes to `ω` within an account holder's domain can arise only from the account holder's own delegation acts (see the Corollary below).

The correct invariant is monotonic refinement — `ω(a)` can change only through delegation, and only by becoming more specific:

**O3 (OwnershipRefinement).** The effective owner of an address changes only when delegation introduces a principal with a strictly longer matching prefix. No other transition alters `ω`:

  `(A a ∈ Σ.alloc, Σ, Σ' : Σ → Σ' ∧ ω_{Σ'}(a) ≠ ω_Σ(a)  ⟹  (E π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a))))`

We prove that every change in effective ownership is witnessed by a new principal with a strictly longer matching prefix, by examining what the effective owner function depends on and what a state transition can alter.

The effective owner `ω_Σ(a)` is defined (O2) as the principal in `Π_Σ` with the longest prefix matching `a`. This definition depends on exactly three inputs: the address `a`, the set of principals `Π_Σ`, and the prefix function `pfx` restricted to `Π_Σ`. We show that a transition `Σ → Σ'` can disturb at most one of these inputs.

*The address is invariant.* By T8 (AllocationPermanence), once `a ∈ Σ.alloc`, the address `a` persists unchanged in every subsequent state. No component of `a` is modified.

*No existing principal is removed.* By O12 (PrincipalPersistence), `Π_Σ ⊆ Π_{Σ'}`. Every principal present in `Σ` remains present in `Σ'`.

*No existing prefix is altered.* By O13 (PrefixImmutability), for every `π ∈ Π_Σ`, `pfx_{Σ'}(π) = pfx_Σ(π)`. The prefix of every surviving principal is identical across the transition.

These three facts together imply that the set of covering principals from `Π_Σ` is preserved exactly:

  `{π ∈ Π_Σ : pfx_Σ(π) ≼ a} = {π ∈ Π_{Σ'} ∩ Π_Σ : pfx_{Σ'}(π) ≼ a}`

The first equality follows from O12 (`Π_Σ ⊆ Π_{Σ'}`) and O13 (`pfx_{Σ'} = pfx_Σ` on `Π_Σ`). In particular, the longest match among `Π_Σ` — which is `ω_Σ(a)` — remains a covering principal in `Σ'` with the same prefix length.

Now suppose `ω_{Σ'}(a) ≠ ω_Σ(a)`. Since `ω_Σ(a)` is still present in `Π_{Σ'}` with the same prefix (by O12 and O13), and since `ω_Σ(a)` was the longest match in `Π_Σ`, the only way for the longest-match computation over `Π_{Σ'}` to yield a *different* result is for some principal in `Π_{Σ'} ∖ Π_Σ` to cover `a` with a strictly longer prefix. That is, there must exist `π' ∈ Π_{Σ'} ∖ Π_Σ` satisfying both `pfx(π') ≼ a` and `#pfx(π') > #pfx(ω_Σ(a))`.

To see why the new principal's prefix must be *strictly* longer: if `#pfx(π') ≤ #pfx(ω_Σ(a))`, then `ω_Σ(a)` would still be the longest (or tied-longest) match. But ties cannot occur — by O1b (PrefixInjectivity), distinct principals have distinct prefixes, and two distinct prefixes of the same length that both cover `a` would agree on all their components (each matching the corresponding component of `a`) and hence be equal, contradicting distinctness. So a new covering principal can only displace `ω_Σ(a)` by being strictly longer.

We conclude: `ω_{Σ'}(a) ≠ ω_Σ(a)` implies `(E π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a)))`. ∎

*Corollary (monotonic refinement).* Since any new effective owner must have a strictly longer prefix than the one it displaces, `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))` in all transitions. Once a principal `π` becomes the effective owner through longest-match, only a *more specific* delegation can supersede it.

*Formal Contract:*
- *Preconditions:* `a ∈ Σ.alloc`, `Σ → Σ'`, `ω_{Σ'}(a) ≠ ω_Σ(a)`.
- *Postconditions:* `(E π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a)))`.
- *Invariant:* `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))` for all transitions `Σ → Σ'`.

**AccountLevelPermanence (Account-level permanence).** No principal external to `dom(π)` can alter effective ownership within `dom(π)`. Changes to `ω(a)` for addresses in a principal's domain arise only from that principal's own delegation acts or from delegation acts of its sub-delegates:

  `(A π ∈ Π_Σ, Σ, Σ' : Σ → Σ' ∧ (E a ∈ dom(π) ∩ Σ.alloc : ω_{Σ'}(a) ≠ ω_Σ(a))  ⟹  (E π_d ∈ Π_Σ : pfx(π) ≼ pfx(π_d) ∧ (E π' ∈ Π_{Σ'} ∖ Π_Σ : delegated_Σ(π_d, π'))))`

That is: if any address in `dom(π)` changes effective owner across a transition, the delegator `π_d` responsible for that transition has a prefix extending `pfx(π)` — the delegator is `π` itself or a sub-delegate of `π`.

We prove this by induction on the order in which principals enter Π, showing that every delegation whose new principal's domain intersects `dom(π)` is authorized by `π` or a sub-delegate of `π`.

*What can change ω within dom(π)?* By O3 (OwnershipRefinement), `ω_{Σ'}(a) ≠ ω_Σ(a)` implies the existence of a new principal `π' ∈ Π_{Σ'} ∖ Π_Σ` with `pfx(π') ≼ a` and `#pfx(π') > #pfx(ω_Σ(a))`. By O15 (PrincipalClosure), `π'` entered Π either through bootstrap or delegation. Since `π' ∈ Π_{Σ'} ∖ Π_Σ` and `Σ` is a reachable state past bootstrap, `π'` was introduced by delegation: there exists `π_d ∈ Π_Σ` with `delegated_Σ(π_d, π')`. The question reduces to: must `pfx(π) ≼ pfx(π_d)`?

*The new principal's prefix extends π's.* Since `a ∈ dom(π)`, we have `pfx(π) ≼ a`. Since `pfx(π') ≼ a` and `#pfx(π') > #pfx(ω_Σ(a)) ≥ #pfx(π)` (the inequality holds because `π` covers `a` and `ω_Σ(a)` is the longest match, so `#pfx(ω_Σ(a)) ≥ #pfx(π)`), the prefix `pfx(π')` is strictly longer than `pfx(π)`. Both `pfx(π)` and `pfx(π')` are prefixes of `a`, and by the nesting lemma for the prefix relation (T5), two prefixes of the same address are comparable: the shorter is a prefix of the longer. Hence `pfx(π) ≼ pfx(π')`, which gives `pfx(π) ≺ pfx(π')` since `#pfx(π) < #pfx(π')`.

*The delegator's prefix extends π's.* By condition (i) of the delegation relation, `pfx(π_d) ≺ pfx(π')`, so `pfx(π_d) ≼ pfx(π')`. By condition (ii), `π_d` is the most-specific covering principal for `pfx(π')`: `(A π'' ∈ Π_Σ : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π_d))`. We established `pfx(π) ≼ pfx(π')` (since `pfx(π) ≺ pfx(π')`), so `π` is among the covering principals of `pfx(π')` in `Π_Σ`, giving `#pfx(π) ≤ #pfx(π_d)`. Both `pfx(π)` and `pfx(π_d)` are prefixes of `pfx(π')` (the former shown above; the latter by condition (i)), and two prefixes of the same tumbler are comparable by T5's nesting lemma. Since `#pfx(π) ≤ #pfx(π_d)`, the shorter-or-equal prefix is a prefix of the longer-or-equal: `pfx(π) ≼ pfx(π_d)`.

This establishes the claim for a single transition. We now verify the two boundary conditions.

*Base case (bootstrap).* By O14 (BootstrapPrincipal), bootstrap principals satisfy pairwise non-nesting: `(A π₁, π₂ ∈ Π₀ : π₁ ≠ π₂ ⟹ pfx(π₁) ⋠ pfx(π₂))`. No bootstrap principal's prefix extends another's, so no bootstrap principal occupies a sub-domain of another. The first transition that can change `ω` within `dom(π)` must be a delegation — and the argument above applies.

*Inductive step (delegation introducing π' that nests within dom(π)).* Suppose `π' ∈ Π_{Σ'} ∖ Π_Σ` with `pfx(π) ≺ pfx(π')`. We showed `pfx(π) ≼ pfx(π_d)` where `π_d` is the delegator. There are two sub-cases. If `pfx(π_d) = pfx(π)`, then `π_d = π` (by O1b, PrefixInjectivity), and the delegation is `π`'s own act. If `pfx(π) ≺ pfx(π_d)`, then `π_d ∈ dom(π)` — `π_d` is a sub-delegate of `π`. By the inductive hypothesis, `π_d` itself entered Π through an act authorized by `π` or a sub-delegate of `π`. The delegation chain traces back to `π`.

Conversely, suppose `pfx(π') ≼ pfx(π)` — the new principal's prefix is a prefix of `π`'s, meaning `dom(π) ⊆ dom(π')`. By condition (vi) of the delegation relation, `¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))` — no existing principal has a prefix strictly extending `pfx(π')`. But `π ∈ Π_Σ` and `pfx(π') ≼ pfx(π)` with `pfx(π') ≠ pfx(π)` (since `#pfx(π') ≤ #pfx(π)` and `pfx(π') ≼ pfx(π)` with `#pfx(π') < #pfx(π)` gives `pfx(π') ≺ pfx(π)`) would give `pfx(π') ≺ pfx(π)`, contradicting condition (vi). The remaining possibility is `pfx(π') = pfx(π)`, but then `#pfx(π') = #pfx(π)`, contradicting `#pfx(π') > #pfx(ω_Σ(a)) ≥ #pfx(π)`. Hence this case cannot arise.

We conclude: every change to `ω(a)` within `dom(π)` is caused by a delegation whose delegator `π_d` satisfies `pfx(π) ≼ pfx(π_d)` — the delegator is `π` itself or a sub-delegate of `π`. No principal external to `dom(π)` can alter effective ownership within `dom(π)`. ∎

Nelson confirms: "User 3 controls allocation of children directly under 3. User 3.2 controls everything under 3.2. User 3 cannot modify User 3.2's documents" (consultation, LM 4/20, 4/29, 2/29). The parent controls baptism; the child controls content. Changes to `ω` within `dom(π)` arise only from `π`'s own delegation choices, or recursively from sub-delegates' choices within their own sub-domains. This is Nelson's "forevermore": not that `ω` is static within `dom(π)`, but that no external act can alter it. The addresses `π` has not sub-delegated remain permanently under `π`'s effective ownership.

This raises a tension that Nelson himself acknowledges. He mentions "someone who has bought the document rights" (LM 2/29), implying ownership can *transfer*. But the address permanently encodes the originating account (by O6 and T8), and Gregory's codebase contains no transfer mechanism whatsoever — no FEBE command, no data structure, no protocol step. We take the conservative reading: O3 describes the refinement regime for the system as specified. Transfer, if it exists, would require machinery that overrides the address-derived ownership — a registry external to the address structure — and Nelson leaves such machinery unspecified. The address is a birth certificate; a transfer would require a separate deed. We record this as an open question.

*Formal Contract:*
- *Preconditions:* `π ∈ Π_Σ`, `a ∈ dom(π) ∩ Σ.alloc`, `Σ → Σ'`, `ω_{Σ'}(a) ≠ ω_Σ(a)`.
- *Postconditions:* `(E π_d ∈ Π_Σ : pfx(π) ≼ pfx(π_d) ∧ delegated_Σ(π_d, π'))` where `π' ∈ Π_{Σ'} ∖ Π_Σ` is the new principal causing the ownership change.
- *Invariant:* Effective ownership within `dom(π)` is sovereign — no delegation by a principal external to `dom(π)` can alter `ω(a)` for any `a ∈ dom(π)`.


## Worked Example

We verify the properties against a concrete scenario. Let principal `π_N` be a node operator with `pfx(π_N) = [1]` (`zeros = 0`). Initially, `Π = {π_N}`.

**State Σ₀.** `π_N` is the sole principal. For any address `a` with node field `1`, `ω(a) = π_N` (the only matching prefix). O2 holds trivially — one principal, one match. O4 holds: every allocated address under node `1` is covered by `pfx(π_N)`.

**Delegation.** `π_N` delegates account prefix `[1, 0, 2]` to new principal `π_A`. Now `Π = {π_N, π_A}`.

**State Σ₁.** Suppose `a₁ = [1, 0, 2, 0, 3, 0, 1]` (a document element under account `[1, 0, 2]`) was allocated by `π_N` before delegation, so `a₁ ∈ Σ₀.alloc`. Both principals' prefixes contain `a₁`: `[1] ≼ a₁` and `[1, 0, 2] ≼ a₁`. The longer match is `[1, 0, 2]`, so `ω(a₁) = π_A`. We verify:

- **O0**: `owns(π_A, a₁)` is decidable from `pfx(π_A) = [1, 0, 2]` and `a₁ = [1, 0, 2, 0, 3, 0, 1]` alone. ✓
- **O1**: `pfx(π_A) ≼ a₁` — the first three components match. ✓
- **O1a**: `zeros(pfx(π_A)) = 1 ≤ 1`. ✓
- **O1b**: `pfx(π_N) = [1] ≠ [1, 0, 2] = pfx(π_A)`, so injectivity holds. ✓
- **O2**: `ω(a₁) = π_A` — unique longest match. `π_N` also matches but `#[1, 0, 2] > #[1]`. ✓
- **O3 (refinement)**: In the transition `Σ₀ → Σ₁`, `ω(a₁)` changed from `π_N` to `π_A`. The new principal `π_A ∈ Π_{Σ₁} ∖ Π_{Σ₀}` has `pfx(π_A) ≼ a₁` and `#pfx(π_A) = 3 > 1 = #pfx(π_N)`. ✓
- **O4**: `pfx(π_N) ≼ a₁` provides coverage. ✓

**Allocation.** `π_A` allocates document address `a₂ = [1, 0, 2, 0, 5, 0, 1]`. This is sub-account allocation — no new principal is created. `Π` is unchanged.

- **O5**: `pfx(π_A) = [1, 0, 2] ≼ a₂` and `π_A` has the longest matching prefix — the allocator is the most-specific covering principal. ✓
- **O6**: `acct(a₂) = [1, 0, 2] = pfx(π_A)` — the account field directly names the effective owner (equality case). ✓

**Sub-account namespace.** Now suppose `π_A` creates sub-account position `[1, 0, 2, 3]` as an organizational namespace — not delegated to a new principal. `Π` remains `{π_N, π_A}`. Address `a₄ = [1, 0, 2, 3, 0, 1, 0, 1]` is a document element under this sub-account. We verify:

- **O2**: Both `pfx(π_N) = [1] ≼ a₄` and `pfx(π_A) = [1, 0, 2] ≼ a₄`. Longest match: `ω(a₄) = π_A`. ✓
- **O6**: `acct(a₄) = [1, 0, 2, 3]` and `pfx(ω(a₄)) = [1, 0, 2]`. The containment `pfx(ω(a₄)) ≼ acct(a₄)` holds but equality does not — the account field extends beyond the owner's prefix because `[1, 0, 2, 3]` has not been delegated. The provenance invariant holds: any address with `acct = [1, 0, 2, 3]` has effective owner `π_A`. ✓
- **O5**: Only `π_A` may allocate within this sub-account — the most-specific covering principal. ✓

If `π_A` subsequently delegates `[1, 0, 2, 3]` to `π_B`, then `ω(a₄)` refines to `π_B` and `pfx(π_B) = acct(a₄) = [1, 0, 2, 3]` — provenance sharpens to equality.

**Account-level permanence.** By O5, only `π_A` (the effective owner of `dom(π_A)`) can delegate sub-accounts extending `[1, 0, 2]`. The node operator `π_N` cannot introduce such a principal — `π_N`'s effective ownership of addresses under `[1, 0, 2]` was superseded when `π_A` was delegated. Addresses `a₁` and `a₂` will remain under `ω = π_A` unless `π_A` itself delegates a sub-account covering them. If `π_A` were to delegate sub-account `[1, 0, 2, 3]` to `π_B`, addresses extending `[1, 0, 2, 3, ...]` would have `ω = π_B` — but addresses `a₁ = [1, 0, 2, 0, ...]` and `a₂ = [1, 0, 2, 0, ...]` are not in `dom(π_B)` (the fourth component `0 ≠ 3`), so they remain under `π_A`. Nelson's "forevermore": sovereignty against external interference.

Now consider address `a₃ = [1, 0, 7, 0, 1, 0, 1]` under a different account. `pfx(π_A) = [1, 0, 2] ⋠ a₃` (component 3: `2 ≠ 7`). Only `pfx(π_N) = [1] ≼ a₃`, so `ω(a₃) = π_N`. The node operator retains effective ownership of all addresses not covered by a delegated account.

**Fork (O10).** Suppose `π_A` wishes to modify the content at `a₃ = [1, 0, 7, 0, 1, 0, 1]`. Since `ω(a₃) = π_N ≠ π_A`, the system does not grant modification. Instead, `π_A` creates a fork: a new address `a' = [1, 0, 2, 0, 6, 0, 1]` within `dom(π_A)`. We verify O10's conditions:

- **O10(a)**: `pfx(π_A) = [1, 0, 2] ≼ [1, 0, 2, 0, 6, 0, 1] = a'`, and `π_A` has the longest matching prefix, so `ω(a') = π_A`. ✓
- **O10(a) corollary**: by (a), `pfx(π_A) = [1, 0, 2] ≼ a'`; the O6 biconditional gives `pfx(π_A) ≼ acct(a') = [1, 0, 2]`. ✓
- **O10(b)**: `a₃` is unchanged — `ω(a₃) = π_N` as before, no content modified, no ownership transferred. ✓

The fork transforms the ownership boundary into a creative act: `π_A` now has a fully owned address `a'` whose content identity may relate to `a₃`'s content (through the content model), but whose ownership is entirely independent.


## Structural Provenance

The ownership prefix is embedded in the permanent address. Because every principal's prefix satisfies `zeros(pfx(π)) ≤ 1` (O1a), the longest-match computation depends only on the node and user fields — the portion captured by `acct(a)`. The document and element fields are irrelevant to ownership determination.

**O6 (StructuralProvenance).** The effective owner of an allocated address is determined entirely by its account field:

  `(A a, b ∈ Σ.alloc : acct(a) = acct(b) ⟹ ω(a) = ω(b))`

We prove that equal account fields imply equal effective owners by showing that the prefix comparisons determining ownership depend only on the account field. The argument requires a structural property of `acct`: for any valid tumbler `a`, the account field is a prefix of the address itself:

**AccountPrefix (AccountPrefix).** `(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)`

We prove that for any tumbler `a` satisfying T4 (FieldSeparatorConstraint), `acct(a) ≼ a` — the account field is a prefix of the address. The T4 restriction is essential: `acct` relies on field parsing (FieldParsing from ASN-0034), which requires T4 validity for well-defined field boundaries — for a tumbler like `[0, 0, 1]`, adjacent zeros violate T4 and the field decomposition is ill-defined. By O17 (AllocatedAddressValidity), all allocated addresses satisfy T4, so the restriction does not limit application.

The prefix relation (T5) requires two conditions: `#a ≥ #acct(a)` and `(A i : 1 ≤ i ≤ #acct(a) : acct(a)ᵢ = aᵢ)`. By T3 (CanonicalRepresentation), each component `aᵢ` is a uniquely determined natural number, so component equality is well-defined. By T4, `zeros(a) ∈ {0, 1, 2, 3}`, and the field decomposition `fields(a)` is uniquely determined by `a` alone. We proceed by cases on `zeros(a)`.

*Case `zeros(a) = 0`.* The tumbler `a` contains no zero-valued components. By T4's field decomposition, the entire tumbler is its node field: `N(a) = a`, and no user, document, or element fields are present. By the definition of `acct` (AccountField), `acct(a) = a`. The prefix relation `a ≼ a` holds: `#a = #a` and `aᵢ = aᵢ` for all `1 ≤ i ≤ #a`.

*Case `zeros(a) = 1`.* By T4, `a` has the form `N₁. ... .Nα . 0 . U₁. ... .Uβ` with `α ≥ 1`, `β ≥ 1`, every `Nᵢ > 0`, and every `Uⱼ > 0`. The node field is `N(a) = [N₁, …, Nα]` and the user field is `U(a) = [U₁, …, Uβ]`. By AccountField, `acct(a) = N(a) ++ [0] ++ U(a) = [N₁, …, Nα, 0, U₁, …, Uβ]`. Since `a` has exactly one zero separator and only node and user fields, `a = [N₁, …, Nα, 0, U₁, …, Uβ] = acct(a)`. The prefix relation holds as in the previous case: `acct(a) = a` implies `acct(a) ≼ a`.

*Case `zeros(a) = 2`.* By T4, `a = N₁. ... .Nα . 0 . U₁. ... .Uβ . 0 . D₁. ... .Dγ` with `α ≥ 1`, `β ≥ 1`, `γ ≥ 1`, every `Nᵢ > 0`, every `Uⱼ > 0`, every `Dₖ > 0`. By AccountField, `acct(a) = [N₁, …, Nα, 0, U₁, …, Uβ]` with `#acct(a) = α + 1 + β`. The address has `#a = α + 1 + β + 1 + γ`. Since `γ ≥ 1`, `#a = α + 1 + β + 1 + γ ≥ α + 1 + β + 2 > α + 1 + β = #acct(a)`, satisfying the length condition `#a ≥ #acct(a)`. For the component condition: the first `α + 1 + β` components of `a` are `N₁, …, Nα, 0, U₁, …, Uβ`, which are exactly the components of `acct(a)`. Hence `acct(a)ᵢ = aᵢ` for all `1 ≤ i ≤ #acct(a)`, and `acct(a) ≼ a`.

*Case `zeros(a) = 3`.* By T4, `a = N₁. ... .Nα . 0 . U₁. ... .Uβ . 0 . D₁. ... .Dγ . 0 . E₁. ... .Eδ` with `α ≥ 1`, `β ≥ 1`, `γ ≥ 1`, `δ ≥ 1`, all field components strictly positive. By AccountField, `acct(a) = [N₁, …, Nα, 0, U₁, …, Uβ]` with `#acct(a) = α + 1 + β`. The address has `#a = α + 1 + β + 1 + γ + 1 + δ ≥ α + 1 + β + 4 > #acct(a)`. The first `α + 1 + β` components of `a` are again `N₁, …, Nα, 0, U₁, …, Uβ` — the document and element fields appear strictly after position `α + 1 + β`. Hence `acct(a)ᵢ = aᵢ` for all `1 ≤ i ≤ #acct(a)`, and `acct(a) ≼ a`.

In all four cases, `acct(a) ≼ a`. The case distinction is exhaustive: T4 constrains `zeros(a) ≤ 3`, and each value in `{0, 1, 2, 3}` is handled. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `T4(a)`.
- *Definition:* `acct(a) = a` when `zeros(a) = 0`; `acct(a) = N(a) ++ [0] ++ U(a)` when `zeros(a) ≥ 1`.
- *Postconditions:* `acct(a) ≼ a`. When `zeros(a) ≤ 1`: `acct(a) = a` (equality). When `zeros(a) ≥ 2`: `acct(a) ≺ a` (strict prefix).

The proof of O6 proceeds in two directions. *Forward:* we must show that for any principal `π` — by O1a (AccountOwnershipBoundary), every principal satisfies `zeros(pfx(π)) ≤ 1` — the relation `pfx(π) ≼ a` implies `pfx(π) ≼ acct(a)`. Two cases arise from the zero count.

When `zeros(pfx(π)) = 0`: the prefix contains no zero separators, so every component of `pfx(π)` is nonzero. Since `pfx(π) ≼ a`, the first `#pfx(π)` components of `a` all equal the corresponding components of `pfx(π)`, and are therefore all nonzero. Two sub-cases arise from the zero count of `a`.

When `zeros(a) = 0`: by FieldParsing, the entire tumbler `a` is its node field, so `acct(a) = a`. Since `pfx(π) ≼ a = acct(a)`, the result is immediate.

When `zeros(a) ≥ 1`: by T4's field structure (FieldParsing), the nonzero components preceding `a`'s first zero separator constitute `a`'s node field. Since `pfx(π)`'s components are all nonzero and match `a`'s leading components, `pfx(π)` lies entirely within `a`'s node field: `pfx(π) ≼ N(a)`. And `N(a) ≼ acct(a)` by the definition of `acct` (which includes the node field and, when present, the user field). Hence `pfx(π) ≼ acct(a)`.

In both sub-cases, `pfx(π) ≼ acct(a)`.

When `zeros(pfx(π)) = 1`: the prefix has the form `N₁...Nα.0.U₁...Uβ`, with a zero separator at position `α + 1`. The prefix relation `pfx(π) ≼ a` forces `a_{α+1} = 0`. By T4 applied to `a`, all components before this zero are positive (they match `N₁...Nα`, which are positive by T4 applied to `pfx(π)`), so this zero cannot be adjacent to another zero or appear at position 1 — it must be `a`'s node-user field separator. This aligns `pfx(π)`'s field structure with `a`'s: the node fields match (`a`'s node field is `N₁...Nα`), and the prefix relation forces `pfx(π)`'s user-field components `U₁...Uβ` to match the first `β` components of `a`'s user field. Since `acct(a)` captures `a` through its full user field, `pfx(π) ≼ acct(a)`.

In both cases, `pfx(π) ≼ a` implies `pfx(π) ≼ acct(a)`. *Reverse:* suppose `pfx(π) ≼ acct(a)`. By AccountPrefix, `acct(a) ≼ a`. By transitivity of the prefix relation, `pfx(π) ≼ a`. We conclude the biconditional:

  `pfx(π) ≼ a  ≡  pfx(π) ≼ acct(a)`

Now, when `acct(a) = acct(b)`, substitution gives `pfx(π) ≼ acct(a) ≡ pfx(π) ≼ acct(b)`, and hence `pfx(π) ≼ a ≡ pfx(π) ≼ b`. The set of covering principals is identical for `a` and `b`. By O2 (OwnershipExclusivity), the effective owner `ω` is the unique longest-match principal in the covering set; since the covering sets coincide, the longest match is the same, giving `ω(a) = ω(b)`. ∎

*Corollary (owner prefix containment).* The effective owner's prefix is always embedded within the account field: `pfx(ω(a)) ≼ acct(a)`. We derive this in four steps. (1) By O1a, `zeros(pfx(ω(a))) ≤ 1`. By T4's field structure (FieldParsing), a valid tumbler with at most one zero separator has at most node and user fields — it contains no document-field or element-field components. (2) By definition of `ω`, `pfx(ω(a)) ≼ a`, so the components of `pfx(ω(a))` match `a`'s leading components. (3) Two cases arise from the zero count. When `zeros(pfx(ω(a))) = 0`: the prefix contains no zero separators, so every component is nonzero; since `pfx(ω(a)) ≼ a`, the first `#pfx(ω(a))` components of `a` are all nonzero, which places them entirely within `a`'s node field; hence `pfx(ω(a)) ≼ N(a) ≼ acct(a)`. When `zeros(pfx(ω(a))) = 1`: the prefix has the form `N.0.U`, and the zero separator at position `α + 1` in the prefix forces — via the prefix relation — a zero at the same position in `a`, aligning `a`'s node-user field boundary with the prefix's; the prefix's user-field components then match `a`'s user-field prefix; since `acct(a)` captures `a` through its full user field, `pfx(ω(a)) ≼ acct(a)`. (4) Hence `#pfx(ω(a)) ≤ #acct(a)` and `pfx(ω(a)) ≼ acct(a)`. The containment may be strict when the address occupies a sub-account position that the effective owner controls but has not delegated. Nelson permits this: "Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose" (LM 4/17). An account-level principal may create sub-account positions as organizational namespaces, ghost elements, or internal partitions without introducing a new ownership principal — the owner decides what sub-numbering means. Equality `pfx(ω(a)) = acct(a)` holds when no intermediate sub-account structure extends beyond the owner's prefix; this is the common case for addresses allocated directly at the principal's own account level.

*Formal Contract:*
- *Preconditions:* `a, b ∈ Σ.alloc`, `acct(a) = acct(b)`.
- *Postconditions:* `ω(a) = ω(b)`.
- *Invariant:* `pfx(ω(a)) ≼ acct(a)` for all `a ∈ Σ.alloc`.

Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" (LM 2/40).

Provenance is not a right that can be exercised or waived — it is an inalienable structural fact. Even if ownership were to transfer (contrary to O3, and through some unspecified mechanism), the address would still record the original principal's identity. The new owner might act upon the content, but the address would forever testify to its origin. This separation — between *who created* and *who currently holds rights* — is what makes ownership transfer conceptually possible without violating address permanence. The address encodes provenance; ownership encodes authority. Under the system as specified, these coincide. Under a hypothetical transfer regime, they would diverge.

Gregory confirms: the User field in the tumbler `Node.0.User.0.Doc.0.Element` is a permanent structural component. The `tumbleraccounteq` function reads these components directly from the mantissa array. There is no indirection, no lookup, no level of abstraction that could mask the origin.


## Subdivision Authority

Of the rights that ownership confers, one is essential to the ownership model itself: the right to create sub-positions.

**O5 (SubdivisionAuthority).** Only the principal with the longest matching prefix may allocate new addresses within its domain:

  `(A Σ, Σ', a, π : Σ → Σ' ∧ a ∈ Σ'.alloc ∖ Σ.alloc ∧ allocated_by_{Σ'}(π, a)  ⟹  pfx(π) ≼ a  ∧  (A π' ∈ Π_Σ : pfx(π') ≼ a ⟹ #pfx(π') ≤ #pfx(π)))`

This formulation avoids applying `ω` to the prefix itself (which may not yet be in `Σ.alloc`); instead it directly constrains the allocator to be the most-specific covering principal. Once `a` enters `Σ.alloc`, O2 gives `ω(a) = π` — the allocator becomes the effective owner of its own allocation.

Nelson: "The owner of a given item controls the allocation of the numbers under it" (LM 4/20). This is the *right to baptize* — not the baptism mechanism itself (which belongs to the tumbler baptism specification), but the authorization constraint that governs who may invoke it.

Gregory confirms: `docreatenewdocument` always uses `taskptr->account` — the session's own prefix — as the allocation hint. The allocation algorithm operates within the boundary determined by the session's account tumbler. There is no parameter that allows specifying someone else's prefix as the allocation target.

O5 interacts with O2. Because ownership is exclusive, exactly one principal may allocate at any point in the address space. Because ownership is determined by prefix (O1), the authorized allocator is determined structurally. The conjunction of O2 and O5 means the address space grows exclusively through the actions of the principals who own each region — no external intervention, no administrative override, no "root user" who may allocate anywhere.


## Delegation

Ownership is not held at a single level — it flows downward through the hierarchy. Nelson calls this "baptism," but we must separate two concepts: *ownership delegation*, which introduces a new principal into `Π`, and *allocation*, which creates addresses within an existing principal's domain. The allocation mechanism is uniform at all levels (T10a); the ownership consequences differ.

We first define the delegation relation, which the subsequent properties rely upon. We use the *strict prefix* relation throughout: `p ≺ a  ≡  p ≼ a ∧ p ≠ a` (equivalently, `p ≼ a ∧ #p < #a` — the equivalence holds because `p ≼ a ∧ #p = #a` gives `p = a` by T3).

**Definition (Delegation).** We write `delegated_Σ(π, π')` to mean that principal `π'` was introduced into `Π` by an act of `π` in state transition `Σ → Σ'`, subject to six structural constraints:

  (i) `pfx(π) ≺ pfx(π')` — the delegate's prefix strictly extends the delegator's

  (ii) `π` is the most-specific covering principal for `pfx(π')` at the time of delegation: `(A π'' ∈ Π_Σ : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π))`

  (iii) `π' ∈ Π_{Σ'} ∖ Π_Σ` — the delegate is newly introduced

  (iv) `zeros(pfx(π')) ≤ 1` — the delegate's prefix is at node or account level

  (v) `T4(pfx(π'))` — the delegate's prefix is a valid tumbler address

  (vi) `¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))` — no existing principal has a prefix strictly extending the new delegate's prefix

Condition (ii) is the authorization constraint — delegation requires O5's subdivision authority. A principal cannot delegate within a sub-domain that has already been delegated to someone else. This grounds the distinction between direct delegation (`π → π'`) and transitive delegation (`π → π' → π''`): when `π` delegates to `π'` and `π'` later delegates to `π''`, we have `delegated(π, π')` and `delegated(π', π'')` but not `delegated(π, π'')`.

Condition (vi) enforces top-down delegation order: a parent prefix must be delegated before any child prefix within it. Without this condition, a higher-level principal could delegate a longer prefix before the shorter enclosing prefix — for instance, delegating `[1, 0, 2, 3]` to `π₂` and subsequently `[1, 0, 2]` to `π₁`, leaving `π₂`'s sub-domain inside `dom(π₁)` without `π₁`'s authorization. Condition (ii) alone does not prevent this: it examines prefixes *of* the target (whether the delegator is the most-specific covering principal), not extensions *beyond* the target (whether some existing principal already occupies a sub-domain). With (vi), when `π'` enters Π, no principal already occupies a sub-domain of `dom(π')`, so `π'` has full authority over its domain from the moment of creation.

Delegation preserves O1a (AccountPrefix). By condition (iv), any `π'` admitted by the `delegated` relation satisfies `zeros(pfx(π')) ≤ 1`. Since O1a requires exactly this — that every principal's prefix is at node or account level — the new principal satisfies O1a by construction, and the existing principals are unchanged by O12. O1a is maintained.

Delegation preserves T4 (ValidAddress). By condition (v), the delegate's prefix satisfies T4 directly — no adjacent zeros, no leading or trailing zero, and every present field non-empty. This is not redundant with condition (iv): a prefix such as `[1, 2, 0]` satisfies `zeros ≤ 1` but violates T4 (trailing zero, empty user field). Condition (v) excludes such prefixes. Existing principals' prefixes are unchanged by O12. T4 is maintained across the transition.

Delegation preserves O1b (PrefixInjectivity). Suppose for contradiction that `pfx(π') = pfx(π''')` for some existing `π''' ∈ Π_Σ`. Then `pfx(π''') ≼ pfx(π')`, so by condition (ii) of the delegation relation, `#pfx(π''') ≤ #pfx(π)`. But from condition (i), `pfx(π) ≺ pfx(π')`, giving `#pfx(π) < #pfx(π')`. Combining: `#pfx(π''') ≤ #pfx(π) < #pfx(π') = #pfx(π''')` — a contradiction. Hence every delegation introduces a principal with a prefix distinct from all existing prefixes. By O15, each transition introduces at most one new principal, so no pairwise collision among newly introduced principals can occur — the proof against existing principals is exhaustive. O1b is maintained across all state transitions. This closes the proof chain: delegation preserves O1a, T4, and O1b, which ensures `ω` (O2) yields a unique principal at a valid hierarchy level with well-defined field parsing.

**O7 (OwnershipDelegation).** A principal `π` may delegate a sub-prefix to a new principal `π'`, provided the `delegated` relation is satisfied (which entails `zeros(pfx(π')) ≤ 1` by condition (iv)) and `π` holds subdivision authority over `pfx(π')`. Upon delegation:

  `(A π, π' : delegated(π, π') :`

  (a) `ω_{Σ'}(a) = π'` for all `a ∈ dom(π') ∩ Σ'.alloc`

  (b) `π'` may allocate new addresses within `dom(π')` (O5 applies to `π'`)

  (c) `π'` may delegate sub-prefixes `p''` with `pfx(π') ≺ p''` per O7 recursively

We prove each postcondition under the hypothesis that `delegated_Σ(π, π')` holds for a transition `Σ → Σ'`, with `π ∈ Π_Σ` and `π' ∈ Π_{Σ'} ∖ Π_Σ`.

*Postcondition (a): `ω_{Σ'}(a) = π'` for all `a ∈ dom(π') ∩ Σ'.alloc`.*

Let `a ∈ dom(π') ∩ Σ'.alloc` be arbitrary. By the definition of domain, `pfx(π') ≼ a`, so `π'` covers `a`. We must show that `π'` achieves the strictly longest matching prefix among all principals in `Π_{Σ'}`.

By O15 (PrincipalClosure), at most one new principal enters `Π` per transition, and `π'` is that principal by condition (iii). Therefore `Π_{Σ'} = Π_Σ ∪ {π'}`. Let `π'' ∈ Π_Σ` with `pfx(π'') ≼ a` be an arbitrary pre-existing covering principal. Since both `pfx(π'')` and `pfx(π')` are prefixes of `a`, they are comparable under `≼` — by the covering chain argument established in O2 (OwnershipExclusivity), any two prefixes of the same address are linearly ordered by the prefix relation. Three cases exhaust the comparison.

*Case `pfx(π') ≺ pfx(π'')`* — then `π'' ∈ Π_Σ` has a prefix strictly extending `pfx(π')`, contradicting condition (vi) of the delegation relation: `¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))`.

*Case `pfx(π') = pfx(π'')`* — by condition (ii), `π` is the most-specific covering principal for `pfx(π')` in `Π_Σ`, so `#pfx(π'') ≤ #pfx(π)`. But `#pfx(π'') = #pfx(π')`, and by condition (i), `#pfx(π) < #pfx(π')`. Combining: `#pfx(π) < #pfx(π') = #pfx(π'') ≤ #pfx(π)` — contradiction.

*Case `pfx(π'') ≺ pfx(π')`* — by condition (ii), `#pfx(π'') ≤ #pfx(π)`, and by condition (i), `#pfx(π) < #pfx(π')`. Therefore `#pfx(π'') < #pfx(π')`.

Only the third case is consistent. Every pre-existing covering principal `π'' ∈ Π_Σ` satisfies `#pfx(π'') < #pfx(π')`. Since the only new principal in `Π_{Σ'}` is `π'` itself, `π'` achieves the unique longest matching prefix in `Π_{Σ'}` for `a`. By O2 (OwnershipExclusivity), `ω_{Σ'}(a) = π'`.

*Postcondition (b): O5 applies to `π'`.*

O5 (SubdivisionAuthority) requires that the allocator of a new address be the most-specific covering principal. By postcondition (a), `ω_{Σ'}(a) = π'` for every `a ∈ dom(π') ∩ Σ'.alloc` — `π'` has the longest matching prefix in its domain. For any new address `a` allocated within `dom(π')` in a successor transition `Σ' → Σ''`, O5's two conjuncts are: `pfx(π') ≼ a` (which holds by `a ∈ dom(π')`) and `(A π'' ∈ Π_{Σ'} : pfx(π'') ≼ a ⟹ #pfx(π'') ≤ #pfx(π'))` (which holds because postcondition (a) established that no principal in `Π_{Σ'}` has a longer matching prefix within `dom(π')` than `π'`). Hence `π'` satisfies O5's authorization condition for allocating within `dom(π')`.

*Postcondition (c): recursive delegation.*

Since `π' ∈ Π_{Σ'}`, the delegation relation's conditions are satisfiable with `π'` as delegator for a sub-prefix `p''` with `pfx(π') ≺ p''`. Condition (i) holds by the choice of `p''`. Condition (ii) is satisfiable because postcondition (a) establishes `π'` as the most-specific covering principal in `dom(π')` — for any `p''` with `pfx(π') ≺ p''`, we have `p'' ∈ dom(π')`, so `π'` has the longest matching prefix among principals in `Π_{Σ'}`, satisfying condition (ii) with `π'` in the role of delegator. Conditions (iv), (v), and (vi) constrain the target prefix `p''`, not the delegator, and are obligations on the choice of delegate prefix. The recursive structure is well-founded: each delegation introduces a principal with a strictly longer prefix (condition (i)), and prefix length is bounded by address length.

The authorization constraint is carried by the `delegated` relation — condition (ii) requires `π` to be the most-specific covering principal. This prevents a grandparent from delegating within a sub-domain it has already handed off: if `π₁` delegates `[1, 0, 2, 3]` to `π₂`, then `π₁` cannot subsequently delegate `[1, 0, 2, 3, 5]` to `π₃`, because `π₂` — not `π₁` — is the most-specific covering principal for that prefix.

Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers" (LM 4/17). The allocation mechanism is uniform ("the entire tumbler works like that," LM 4/19), but the resulting authority is hierarchical: delegation at node and account level creates principals with full sovereignty over their domain, while allocation at document and version level exercises mechanical subdivision rights within the parent principal's domain without establishing independent ownership standing. ∎

*Formal Contract:*
- *Preconditions:* `delegated_Σ(π, π')`, `Σ → Σ'`.
- *Postconditions:* (a) `(A a ∈ dom(π') ∩ Σ'.alloc : ω_{Σ'}(a) = π')`; (b) `π'` satisfies O5 for allocations within `dom(π')`; (c) the delegation relation is satisfiable with `π'` as delegator for sub-prefixes of `pfx(π')`.
- *Invariant:* Delegation confers full sovereignty — the delegate becomes the effective owner of its entire domain immediately upon delegation, and acquires the rights to allocate and sub-delegate within that domain.

The delegation is irrevocable:

**O8 (IrrevocableDelegation).** Once principal `π` delegates to `π'`, the delegating parent never regains effective ownership of addresses in the delegate's domain:

  `(A π, π', a, Σ, Σ' : delegated_Σ(π, π') ∧ a ∈ dom(π') ∩ Σ'.alloc ∧ Σ →⁺ Σ' : ω_{Σ'}(a) ≠ π)`

The formulation captures irrevocability without overclaiming. It says the *parent* can never recover the addresses, while permitting the delegate `π'` to sub-delegate (via O7(c)): if `π'` delegates to `π''` with `pfx(π') ≺ pfx(π'')`, then `ω(a) = π''` for `a ∈ dom(π'')` — the address leaves `π'`'s effective ownership but does not return to `π`. The domain restriction `dom(π') ∩ Σ'.alloc` ensures `ω` is applied only to addresses where it is defined (grounded by O4).

We prove that in every state `Σ'` reachable from the delegation state, the delegating parent `π` is never the effective owner of any address in the delegate's domain. The argument is direct: we show that the longest-match computation in `Σ'` always finds a principal with a strictly longer prefix than `π`, so `π` cannot be `ω_{Σ'}(a)`.

Let `Σ_d` denote the state in which `delegated_{Σ_d}(π, π')` holds, and let `Σ'` be any state with `Σ_d →⁺ Σ'`. Let `a ∈ dom(π') ∩ Σ'.alloc` be arbitrary.

*The delegate persists with an unchanged prefix.* By O12 (PrincipalPersistence), `Π_{Σ_d} ⊆ Π_{Σ'}`, and since `π' ∈ Π_{Σ_d}` (by condition (iii) of the delegation relation, `π'` entered `Π` at `Σ_d`), we have `π' ∈ Π_{Σ'}`. By O13 (PrefixImmutability), `pfx_{Σ'}(π') = pfx_{Σ_d}(π')`. The delegate is present in every future state with its original prefix.

*The delegate covers the address.* Since `a ∈ dom(π')`, the definition of domain gives `pfx(π') ≼ a`. This relation depends only on the components of `pfx(π')` and `a`. By O13, `pfx(π')` is immutable. By T8 (AllocationPermanence), `a` — being allocated — persists unchanged. Therefore `pfx_{Σ'}(π') ≼ a` holds in `Σ'`.

*The delegate's prefix is strictly longer than the parent's.* By condition (i) of the delegation relation, `pfx(π) ≺ pfx(π')`, which gives `#pfx(π) < #pfx(π')`. By O13, both prefixes are immutable: `pfx_{Σ'}(π) = pfx_{Σ_d}(π)` and `pfx_{Σ'}(π') = pfx_{Σ_d}(π')`. The strict length inequality `#pfx_{Σ'}(π) < #pfx_{Σ'}(π')` holds in every reachable state.

*The parent cannot be the longest match.* The effective owner `ω_{Σ'}(a)` is defined (O2) as the principal in `Π_{Σ'}` with the longest matching prefix for `a`. We have established that `π' ∈ Π_{Σ'}` with `pfx_{Σ'}(π') ≼ a` and `#pfx_{Σ'}(π') > #pfx_{Σ'}(π)`. Therefore `π'` (or some other principal with a still-longer prefix) achieves a longer match than `π`. The longest-match principal must have a prefix at least as long as `pfx(π')`, which is strictly longer than `pfx(π)`. Hence `ω_{Σ'}(a) ≠ π`.

To see this last step precisely: suppose for contradiction that `ω_{Σ'}(a) = π`. Then by the definition of `ω`, `π` would need to satisfy `(A π'' ∈ Π_{Σ'} : π'' ≠ π ∧ pfx_{Σ'}(π'') ≼ a ⟹ #pfx_{Σ'}(π) > #pfx_{Σ'}(π''))`. But `π' ∈ Π_{Σ'}` with `π' ≠ π` (they are distinct — `π` was already in `Π` before delegation while `π'` was newly introduced, and their prefixes differ in length) and `pfx_{Σ'}(π') ≼ a`, yet `#pfx_{Σ'}(π) < #pfx_{Σ'}(π')` — contradicting the requirement. Therefore `ω_{Σ'}(a) ≠ π`.

Note that the proof makes no claim about *who* the effective owner is — only that it is not `π`. The effective owner may be `π'` itself, or it may be a sub-delegate `π''` introduced by `π'` with `pfx(π') ≺ pfx(π'')`. In the latter case, `ω_{Σ'}(a) = π''` for `a ∈ dom(π'')` — the address leaves `π'`'s effective ownership but does not return to `π`, because `#pfx(π'') > #pfx(π') > #pfx(π)` and the argument above applies equally to `π''`. ∎

*Design confirmation.* Nelson: "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). There is no revocation command, no forced reclamation. Gregory confirms: `validaccount` is a stub that unconditionally returns TRUE — the system has no machinery for checking or revoking delegation. Once the sub-prefix exists, the delegate owns it permanently.

*Formal Contract:*
- *Preconditions:* `delegated_Σ(π, π')`, `a ∈ dom(π') ∩ Σ'.alloc`, `Σ →⁺ Σ'`.
- *Postconditions:* `ω_{Σ'}(a) ≠ π`.
- *Invariant:* Once delegation occurs, the parent's prefix is permanently shorter than the delegate's, so the parent can never regain longest-match status for any address in the delegate's domain.

The combination of O3 (OwnershipRefinement), O8 (IrrevocableDelegation), O12 (PrincipalPersistence), O13 (PrefixImmutability), and T8 (AllocationPermanence) means the ownership structure of the address space is *monotonically growing*. New ownership domains are created through delegation but never destroyed. The tree of ownership deepens but never prunes.


## Node-Locality

Ownership authority does not propagate across node boundaries. A principal's effective ownership is bounded by its node prefix.

**O9 (NodeLocalOwnership).** For a principal `π`, the ownership predicate `owns(π, a)` can hold only for allocated addresses `a` whose node field extends the principal's node field:

  `(A π ∈ Π, a ∈ Σ.alloc : owns(π, a)  ⟹  N(pfx(π)) ≼ N(a))`

We must show that if `owns(π, a)` holds for an allocated address `a`, then `N(pfx(π)) ≼ N(a)` — the principal's node field is a prefix of the address's node field. By O1 (PrefixDetermination), `owns(π, a) ≡ pfx(π) ≼ a`, so the hypothesis gives `pfx(π) ≼ a`: by T5, the components of `pfx(π)` match the leading components of `a`, that is, `#a ≥ #pfx(π)` and `aᵢ = pfx(π)ᵢ` for all `1 ≤ i ≤ #pfx(π)`. By O1a (AccountOwnershipBoundary), `zeros(pfx(π)) ≤ 1`. Two cases exhaust the possibilities.

*Case 1: `zeros(pfx(π)) = 0` (node-level principal).* Every component of `pfx(π)` is strictly positive — T4 (FieldSeparatorConstraint) requires that every non-separator component be positive, and the absence of zeros means every component is a non-separator. By T4's field decomposition, the node field of a tumbler with no zeros is the tumbler itself: `N(pfx(π)) = pfx(π)`, with `#N(pfx(π)) = #pfx(π)`.

Since `pfx(π) ≼ a`, the first `#pfx(π)` components of `a` match those of `pfx(π)` and are therefore all strictly positive. By T4, the node field `N(a)` consists of the components of `a` preceding the first zero-valued component (or all components of `a` if no zero occurs). Since positions `1` through `#pfx(π)` of `a` are all positive, the first zero of `a` — if it exists — occurs at position `#pfx(π) + 1` or later. Therefore `#N(a) ≥ #pfx(π) = #N(pfx(π))`. The first `#N(pfx(π))` components of `N(a)` are `a₁, ..., a_{#pfx(π)}`, which equal `pfx(π)₁, ..., pfx(π)_{#pfx(π)}` by the prefix relation, and these are exactly the components of `N(pfx(π))`. Hence `N(pfx(π)) ≼ N(a)`.

Note that the inequality may be strict: T10a (SiblingShallowChildDeep) permits `inc([1, 2], 1) = [1, 2, 1]` with `zeros = 0`, so addresses with node fields strictly extending the principal's node field exist. In such cases `N(pfx(π)) ≺ N(a)` — the address belongs to a longer node path that shares the principal's node prefix.

*Case 2: `zeros(pfx(π)) = 1` (account-level principal).* By T4, the prefix has the form `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ` with `α ≥ 1` and `β ≥ 1` (non-empty field constraint), where every `Nᵢ > 0` (positive-component constraint) and every `Uⱼ > 0`. The node field is `N(pfx(π)) = [N₁, ..., Nₐ]`, and the single zero sits at position `α + 1`.

Since `pfx(π) ≼ a`, the first `α + 1 + β` components of `a` match those of `pfx(π)`:
- Positions `1` through `α`: `aᵢ = Nᵢ > 0` for each `1 ≤ i ≤ α`.
- Position `α + 1`: `a_{α+1} = 0`, matching the zero separator of `pfx(π)`.
- Positions `α + 2` through `α + 1 + β`: `a_{α+1+j} = Uⱼ > 0` for each `1 ≤ j ≤ β`.

By T4, the node field `N(a)` consists of the components of `a` before `a`'s first zero. Since positions `1` through `α` are all positive and position `α + 1` is zero, the first zero of `a` is at position `α + 1`. Hence `N(a) = [a₁, ..., aₐ] = [N₁, ..., Nₐ] = N(pfx(π))`. The prefix relation holds with equality: `N(pfx(π)) = N(a)`, which implies `N(pfx(π)) ≼ N(a)`.

In both cases `N(pfx(π)) ≼ N(a)`. The case distinction is exhaustive by O1a. ∎

The consequence is that ownership cannot cross node boundaries. A principal at node `[1]` cannot own addresses at node `[2]`, because `[1]` is not a prefix of `[2, ...]`. The node field's leading components must match — only the *length* of the node field may differ, and only for node-level principals (Case 1 above).

The same human being would therefore hold *separate, independent* ownership roots on each node — distinct principals with distinct prefixes, distinct domains, and no structural relationship between them. Nelson's "docuverse" is a forest of independently owned trees rooted at nodes, not a single tree with a universal authority. The node operator delegates accounts within its node; those accounts have no automatic standing on any other node.

Gregory's implementation has no cross-node communication, no remote ownership lookup, and no federation of identity. The account tumbler is per-session, per-node. But the abstract property does not depend on these implementation choices — it follows from the prefix geometry of T4 and the structural ownership predicate of O1.

*Formal Contract:*
- *Preconditions:* `π ∈ Π`, `a ∈ Σ.alloc`, `owns(π, a)`.
- *Postconditions:* `N(pfx(π)) ≼ N(a)`. When `zeros(pfx(π)) = 1`: `N(pfx(π)) = N(a)` (equality). When `zeros(pfx(π)) = 0`: `N(pfx(π)) ≼ N(a)` (proper prefix permitted).


## The Fork as Ownership Boundary

When a principal seeks to modify content it does not own, the system's response is not an error but a creative act. This is the architectural expression of the ownership boundary.

**O10 (DenialAsFork).** When principal `π` requires modification of content at address `a` but `ω(a) ≠ π`, the system provides an alternative: `π` may create a new address `a'` within `dom(π)`:

  (a) `ω(a') = π` — the new address is fully owned by the requesting principal

  (b) the original address `a` is unchanged — no ownership is transferred, no content is modified

Condition (a) entails a structural consequence: since `ω(a') = π` gives `pfx(π) ≼ a'`, and the O6 biconditional (`pfx(π) ≼ a' ≡ pfx(π) ≼ acct(a')`, holding for all principals with `zeros(pfx(π)) ≤ 1` — i.e., all principals by O1a) yields `pfx(π) ≼ acct(a')`. The address structure necessarily records the fork within the requesting principal's account domain. This holds for both `zeros = 0` and `zeros = 1`; no case distinction is needed.

Nelson: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links" (LM 2/45). Gregory confirms the structural mechanism: `docreatenewversion`, when invoked on a document belonging to a different account, routes the allocation through `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` — placing the fork under the requesting principal's account, not under the source document.

The forked address lives entirely within `dom(π)`. It satisfies O2 (π is its exclusive owner), O3 corollary (π's account-level ownership is permanent), O5 (π may further subdivide it), and O6 (its provenance records π as the creator). From the ownership model's perspective, the fork is a new independent address that happens to share content identity with the original — a relationship that belongs to the content model, not the ownership model.

We must establish that such an `a'` exists in every reachable state — that `π` can always find an address within `dom(π)` where it remains the effective owner (i.e., `a' ∈ dom(π)` with no sub-delegate's prefix covering `a'`). The argument proceeds in two cases from O1a.

When `zeros(pfx(π)) = 1` (account-level principal): `π`'s prefix has the form `N.0.U`, spanning node and user fields. By O1a, every sub-delegate `π_i` of `π` also satisfies `zeros(pfx(π_i)) ≤ 1`. Since `pfx(π) ≺ pfx(π_i)`, the sub-delegate's prefix strictly extends `π`'s user field — it remains within the node-and-user-field region. Now consider document-level addresses within `dom(π)`: any address `a' = N.0.U.0.D.0.E` has `zeros(a') = 3`, and `pfx(π) ≼ a'`. For a sub-delegate `π_i` to cover `a'`, we would need `pfx(π_i) ≼ a'` with `zeros(pfx(π_i)) ≤ 1`. But `pfx(π_i)` is a proper extension of `pfx(π) = N.0.U` with at most one zero — it has the form `N.0.U.U'...` where all `U'...` are positive. The next component of `a'` after `U` is `0` (the user-document separator). The prefix relation requires `pfx(π_i)`'s next component to equal `0`, but that would give `zeros(pfx(π_i)) ≥ 2`, violating O1a. Hence no sub-delegate can cover any document-level address in `dom(π)`. Such addresses are always producible: from `pfx(π) = N.0.U`, apply `inc(pfx(π), 2)` to reach document level (appending `.0.1`, giving `N.0.U.0.1` with `zeros = 2`), then `inc(·, 2)` again to reach element level (appending `.0.1`, giving `N.0.U.0.1.0.1` with `zeros = 3`). By TA5(d), each `inc(·, k)` with `k > 0` extends the tumbler by `k` positions and produces a result strictly greater than its input.

When `zeros(pfx(π)) = 0` (node-level principal): `π`'s prefix is entirely within the node field. Sub-delegates `π_i` with `pfx(π) ≺ pfx(π_i)` and `zeros(pfx(π_i)) = 0` extend the node field. Sub-delegates with `zeros(pfx(π_i)) = 1` have entered the user field. In either case, the set of sub-delegates is finite: by O15, each state transition introduces at most one new principal, and the system has undergone finitely many transitions. By T0a (UnboundedComponents), component values are unbounded. Collect the user-field components of all existing sub-delegate prefixes that have entered the user field (`zeros(pfx(π_i)) = 1`). If no such sub-delegates exist, choose any `u ≥ 1` — the condition is vacuously satisfied. Otherwise, choose `u` exceeding the maximum user-field component among all such prefixes — such a value exists because a finite set of natural numbers has a maximum, and T0a guarantees a tumbler with that component value exists. Then the address `a' = pfx(π).0.u.0.1.0.1` satisfies `pfx(π) ≼ a'`, and no sub-delegate's prefix is a prefix of `a'` (the fresh `u` avoids all existing sub-delegate prefixes). Hence `ω(a') = π`.

In both cases, `π` can always produce an address it effectively owns. The fork operation's postcondition `ω(a') = π` is satisfiable in every reachable state. ∎

*Formal Contract:*
- *Preconditions:* `π ∈ Π_Σ`, `a ∈ Σ.alloc`, `ω(a) ≠ π`.
- *Postconditions:* `(E a' ∈ dom(π) : ω(a') = π ∧ a ∈ Σ.alloc)` — there exists an address `a'` in `dom(π)` effectively owned by `π`, and the original address `a` remains allocated and unmodified.
- *Invariant:* In every reachable state, every principal can produce an address it effectively owns — the fork postcondition is universally satisfiable.

O10 transforms the ownership boundary from a wall into a fork point. The only "permission" concept the system needs is prefix containment. Everything else — collaboration, annotation, criticism, derivation — is handled by creating new owned addresses and establishing relationships between them. The conventional permission hierarchy (users, groups, roles, ACLs) is replaced by a single structural predicate and an unbounded supply of fresh addresses.


## Principal Identity and the Trust Boundary

One question remains: how does the system know which principal it is speaking to?

Nelson is silent on authentication mechanisms. Gregory's implementation reveals that the trust boundary lies *outside* the ownership model. The backend's `getxaccount` reads whatever tumbler the client sends over the wire and stores it as the session's account — `validaccount` returns TRUE unconditionally in all build configurations. The backend does not verify that the claimed account tumbler corresponds to a legitimate delegation. It trusts the assertion.

This is not a deficiency in the ownership *model* — it is a gap in the ownership *enforcement*. The model itself is clean: O0 through O10 hold regardless of how principal identity is established. The structural predicate `tumbleraccounteq` gives the correct answer for any two tumblers. The question of whether the *right* tumblers are being compared — whether the session's claimed account tumbler is the one the principal is actually entitled to — is a separate concern.

We record this as an abstract property:

**O11 (IdentityAxiomatic).** The ownership model treats principal identity as given — it assumes the system has established which principal holds which prefix. The mechanism by which this establishment occurs (authentication, delegation verification, cryptographic binding) is external to the ownership model:

  `(A session : session.account = pfx(π)  is an axiom of the session, not a theorem of the ownership model)`

Any conforming implementation must provide *some* mechanism for binding sessions to principals, but the ownership properties O0–O10 are independent of which mechanism is chosen. The properties hold for any mapping from sessions to account tumblers, provided the mapping is consistent with the delegation structure.


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
11. *Identity-independent* — the model is parameterized by principal identity, not coupled to it (O11)

The design philosophy is clear: minimize the authorization model to the point where the only permission concept needed is prefix containment. The tumbler is not just a name — it is a title deed.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| O0 | Ownership of `a` by `π` is decidable from `pfx(π)` and `a` alone, without mutable state | design requirement |
| O1 | `owns(π, a) ≡ pfx(π) ≼ a` — ownership is prefix containment | from T4, T5 |
| O1a | `(A π ∈ Π : zeros(pfx(π)) ≤ 1)` — ownership principals exist only at node or account level | design requirement |
| O1b | `pfx` is injective — distinct principals have distinct prefixes | design requirement |
| O2 | Every allocated address has exactly one effective owner `ω(a)`, determined by longest matching prefix | from O4, O1b |
| O3 | `ω(a)` changes only through delegation introducing a longer matching prefix — monotonic refinement | from T8, O12, O13, O1b |
| AccountLevelPermanence | No external delegation can alter effective ownership within `dom(π)` — changes to `ω(a)` inside a principal's domain arise only from that principal's own acts or its sub-delegates' acts | from Delegation, O1b, O3, O14, O15, T5 |
| O4 | `(A a ∈ Σ.alloc : (E π ∈ Π : pfx(π) ≼ a))` — every allocated address is covered by some principal | from O14, O16, O5, O12, O13 |
| O5 | Only the principal with the longest matching prefix may allocate within its domain — subdivision authority | design requirement |
| AccountPrefix | `(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)` — the account field is a prefix of any valid address | from T3, T4, T5, AccountField |
| O6 | `acct(a) = acct(b) ⟹ ω(a) = ω(b)` — effective owner determined entirely by account field | from O1a, O2, O17, AccountPrefix |
| O7 | Delegation (authorized by `delegated`) confers effective ownership (O2), subdivision authority (O5), and recursive delegation (O7) | from Delegation, O2, O5, O15 |
| O8 | `delegated_Σ(π, π') ∧ a ∈ dom(π') ∩ Σ'.alloc ∧ Σ →⁺ Σ' ⟹ ω_{Σ'}(a) ≠ π` — delegating parent never regains ownership | from Delegation, O2, O12, O13, T8 |
| O9 | `(A π ∈ Π, a ∈ Σ.alloc : owns(π, a) ⟹ N(pfx(π)) ≼ N(a))` — ownership bounded by node field | from O1, O1a, T4, T5 |
| O10 | Non-ownership of target yields a fork: new address under the requesting principal's domain | from O1a, O6, O15, T0a, TA5(d) |
| O11 | Principal identity is axiomatic to the ownership model — authentication is external | axiom |
| O12 | `(A Σ, Σ' : Σ → Σ' ⟹ Π_Σ ⊆ Π_{Σ'})` — principal persistence | design requirement |
| O13 | `pfx_{Σ'}(π) = pfx_Σ(π)` for all transitions — prefix immutability | design requirement |
| O14 | `Π₀ ≠ ∅`, initial principals cover all initially allocated addresses, `zeros ≤ 1`, `pfx` injective on `Π₀`, `T4(pfx(π))`, and pairwise non-nesting — bootstrap with O1a/O1b/T4/non-nesting base cases | design requirement |
| O15 | Principals enter Π exclusively through bootstrap or delegation; `\|Π_{Σ'} ∖ Π_Σ\| ≤ 1` per transition | design requirement |
| O16 | `(A a ∈ Σ'.alloc ∖ Σ.alloc : (E π ∈ Π_Σ : allocated_by_{Σ'}(π, a)))` — allocation closure | design requirement |
| O17 | `(A Σ, a : a ∈ Σ.alloc ⟹ T4(a))` — every allocated address is a valid tumbler | axiom |
| `ω(a)` | `effectiveOwner : Σ.alloc → Principal` — the effective owner function (defined only for allocated addresses) | from O4, O1b, T5, T3 |
| OwnershipDomain | `{a ∈ T : pfx(π) ≼ a}` — the ownership domain of a principal | introduced |
| `acct(a)` | When `zeros(a) = 0`: `acct(a) = a`; when `zeros(a) ≥ 1`: truncation through user field | from T4, T6 |
| `allocated_by_Σ(π, a)` | Primitive relation: `a` was allocated by `π` in transition producing `Σ`; mechanism out of scope, constrained by O5 and O16 | axiom |
| Delegation | `π'` introduced into `Π` by act of `π`, with `pfx(π) ≺ pfx(π')`, `π` most-specific covering principal, no existing principal extends `pfx(π')`, `zeros(pfx(π')) ≤ 1`, and `T4(pfx(π'))` | introduced |
| `pfx(π)` | `ownershipPrefix : Principal → Tumbler` — injective, `zeros(pfx(π)) ≤ 1`, `T4(pfx(π))` | axiom |


## Open Questions

- Must the system provide a mechanism for ownership transfer, and if so, what invariants must it preserve given that structural provenance (O6) is inalienable?
- Must the system enforce that no principal can claim an ownership prefix that overlaps an existing principal's domain, and what are the invariants of this enforcement?
- What formal guarantees must the system provide about content accessibility when the effective owner ceases to exist as a principal?
- Must ownership domains be dense (every address in the domain is reachable) or can gaps exist between baptized siblings within a domain?
- What invariants must a cross-node identity federation satisfy to remain consistent with O9, if such federation is introduced?
- What formal relationship must hold between the provenance recorded in an address (O6) and the effective owner (O2) if ownership transfer is permitted?
- Must delegation events be recorded, or is the structural evidence of the address hierarchy sufficient to reconstruct the delegation history?
