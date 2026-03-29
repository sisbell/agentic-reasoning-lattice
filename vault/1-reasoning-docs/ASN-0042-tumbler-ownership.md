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

We introduce the principals. Let `Π` denote the set of *principals* — the ownership subjects. Each principal `π ∈ Π` is associated with an *ownership prefix* `pfx(π) ∈ T`, a valid tumbler (satisfying T4) that serves as the root of their namespace. The mapping `pfx` is injective — distinct principals have distinct prefixes:

**O1b (PrefixInjectivity).** `(A π₁, π₂ ∈ Π : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`

Without injectivity, two principals sharing a prefix could both claim longest-match, and the effective owner function `ω` (defined in O2 below) would not yield a unique result.

The ownership question "does `π` own `a`?" is answered by examining these two tumblers alone:

**O0 (StructuralOwnership).** Whether principal `π` owns address `a` is decidable from `pfx(π)` and `a` alone, without consulting any mutable system state.

The decision procedure is prefix containment:

**O1 (PrefixDetermination).** Principal `π` owns address `a` iff `pfx(π)` is a prefix of `a`:

  `owns(π, a)  ≡  pfx(π) ≼ a`

where `p ≼ a` denotes that `p` is a prefix of `a` in the sense of T5 — the components of `p` match the leading components of `a`.


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

This follows from O5 (SubdivisionAuthority, stated below), O14 (BootstrapPrincipal), and O16 (AllocationClosure): allocation only occurs within an existing principal's domain, so every allocated address is born under a covering prefix. The derivation: by O14, the initial state has a principal covering all initially allocated addresses. If `a` is newly allocated in a transition Σ → Σ', then by O16 there exists a principal `π ∈ Π_Σ` that allocated `a`, and by O5 `pfx(π) ≼ a`. By O12, `π` persists in Σ'. For addresses already in `Σ.alloc`, their covering principals persist in `Σ'` (O12) with unchanged prefixes (O13), so coverage is preserved. By induction on the transition history, O4 holds in every reachable state.

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

Well-definedness of `ω` requires three observations: (i) by O4, at least one principal's prefix contains any allocated address; (ii) any two containing prefixes are linearly ordered by the prefix relation — we show this explicitly: suppose `p₁ ≼ a` and `p₂ ≼ a`, and WLOG `#p₁ ≤ #p₂`. For every `i ≤ #p₁`, the prefix relation gives `(p₁)ᵢ = aᵢ` and `(p₂)ᵢ = aᵢ`, hence `(p₁)ᵢ = (p₂)ᵢ`. Since `p₁` agrees with `p₂` on all `#p₁` components and `#p₁ ≤ #p₂`, we have `p₁ ≼ p₂`. Therefore the set of covering prefixes is totally ordered by `≼`. Moreover, this set is finite: each covering prefix `p ≼ a` is uniquely determined by its length (since `p = [a₁, …, a_{#p}]`), and there are at most `#a` possible lengths, so the covering set has at most `#a` elements. A finite totally ordered set has a maximum; thus the longest prefix exists and is unique; and (iii) by O1b, the principal holding that longest prefix is unique. Together these give `(E! π :: ω(a) = π)`.

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

**AccountLevelPermanence (Account-level permanence).** Account-level prefixes can nest — `pfx(π₁) = [1, 0, 2]` and `pfx(π₂) = [1, 0, 2, 3]` both satisfy O1a, and delegation from `π₁` to `π₂` changes `ω` for addresses in `dom(π₂)`. But such delegation requires an act of `π₁` itself: by O5 (for allocation) and condition (ii) of the `delegated` relation (for delegation), only the most-specific covering principal may allocate or delegate within its domain. By O15 (PrincipalClosure), delegation is the exclusive mechanism for introducing principals post-bootstrap. No delegation can introduce a principal whose prefix extends `pfx(π)` without `π`'s involvement. We show this by induction on the order in which principals enter Π.

*Base case.* For bootstrap principals `π ∈ Π₀`, O14's non-nesting constraint gives `(A π₁, π₂ ∈ Π₀ : π₁ ≠ π₂ ⟹ pfx(π₁) ⋠ pfx(π₂))` — no other bootstrap principal has a prefix extending `pfx(π)`.

*Inductive step.* Suppose `π' ∈ Π_{Σ'} ∖ Π_Σ` is introduced by delegation. By condition (vi), no existing principal in `Π_Σ` has a prefix strictly extending `pfx(π')`. By condition (ii), the delegator is the most-specific covering principal for `pfx(π')`. These two conditions together mean that `π'` enters Π with no unauthorized sub-domains already occupied and only through an act of the principal that controls `pfx(π')`. For the inductive claim: suppose `π` is an existing principal and `pfx(π) ≺ pfx(π')`. Then `π'`'s introduction changes `ω` within `dom(π)` — but this introduction was authorized by the most-specific covering principal for `pfx(π')`, which is either `π` itself or a sub-delegate of `π` (whose authority derives from `π` by the inductive hypothesis). Conversely, if `pfx(π') ≺ pfx(π)`, condition (vi) would have blocked the introduction — `π` already has a prefix extending `pfx(π')`. Hence no delegation can place a principal inside `dom(π)` without `π`'s involvement (direct or through sub-delegates).

Nelson confirms: "User 3 controls allocation of children directly under 3. User 3.2 controls everything under 3.2. User 3 cannot modify User 3.2's documents" (consultation, LM 4/20, 4/29, 2/29). The parent controls baptism; the child controls content. Changes to `ω` within `dom(π)` arise only from `π`'s own delegation choices, or recursively from sub-delegates' choices within their own sub-domains. This is Nelson's "forevermore": not that `ω` is static within `dom(π)`, but that no external act can alter it. The addresses `π` has not sub-delegated remain permanently under `π`'s effective ownership.

This raises a tension that Nelson himself acknowledges. He mentions "someone who has bought the document rights" (LM 2/29), implying ownership can *transfer*. But the address permanently encodes the originating account (by O6 and T8), and Gregory's codebase contains no transfer mechanism whatsoever — no FEBE command, no data structure, no protocol step. We take the conservative reading: O3 describes the refinement regime for the system as specified. Transfer, if it exists, would require machinery that overrides the address-derived ownership — a registry external to the address structure — and Nelson leaves such machinery unspecified. The address is a birth certificate; a transfer would require a separate deed. We record this as an open question.


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

We first observe a structural property of `acct`: for any valid tumbler `a`, the account field is a prefix of the address itself:

**AccountPrefix (AccountPrefix).** `(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)`

The T4 restriction is essential: `acct` relies on field parsing (FieldParsing from ASN-0034), which requires T4 validity — for a tumbler like `[0, 0, 1]`, the field boundaries are ill-defined and `acct` is not well-defined. By O17, all allocated addresses satisfy T4, so the restriction does not limit application.

When `zeros(a) = 0`, `acct(a) = a` and the claim is trivial. When `zeros(a) ≥ 1`, `acct(a)` is the truncation of `a` through its user field — the leading `N₁...Nα.0.U₁...Uβ` components — so `acct(a)` is literally a prefix of `a` by construction.

The proof of O6 proceeds in two directions. *Forward:* we must show that for any principal `π` with `zeros(pfx(π)) ≤ 1`, `pfx(π) ≼ a` implies `pfx(π) ≼ acct(a)`. Two cases arise from the zero count.

When `zeros(pfx(π)) = 0`: the prefix contains no zero separators, so every component of `pfx(π)` is nonzero. Since `pfx(π) ≼ a`, the first `#pfx(π)` components of `a` all equal the corresponding components of `pfx(π)`, and are therefore all nonzero. Two sub-cases arise from the zero count of `a`.

When `zeros(a) = 0`: by FieldParsing, the entire tumbler `a` is its node field, so `acct(a) = a`. Since `pfx(π) ≼ a = acct(a)`, the result is immediate.

When `zeros(a) ≥ 1`: by T4's field structure (FieldParsing), the nonzero components preceding `a`'s first zero separator constitute `a`'s node field. Since `pfx(π)`'s components are all nonzero and match `a`'s leading components, `pfx(π)` lies entirely within `a`'s node field: `pfx(π) ≼ N(a)`. And `N(a) ≼ acct(a)` by the definition of `acct` (which includes the node field and, when present, the user field). Hence `pfx(π) ≼ acct(a)`.

In both sub-cases, `pfx(π) ≼ acct(a)`.

When `zeros(pfx(π)) = 1`: the prefix has the form `N₁...Nα.0.U₁...Uβ`, with a zero separator at position `α + 1`. The prefix relation `pfx(π) ≼ a` forces `a_{α+1} = 0`. By T4 applied to `a`, all components before this zero are positive (they match `N₁...Nα`, which are positive by T4 applied to `pfx(π)`), so this zero cannot be adjacent to another zero or appear at position 1 — it must be `a`'s node-user field separator. This aligns `pfx(π)`'s field structure with `a`'s: the node fields match (`a`'s node field is `N₁...Nα`), and the prefix relation forces `pfx(π)`'s user-field components `U₁...Uβ` to match the first `β` components of `a`'s user field. Since `acct(a)` captures `a` through its full user field, `pfx(π) ≼ acct(a)`.

In both cases, `pfx(π) ≼ a` implies `pfx(π) ≼ acct(a)`. *Reverse:* suppose `pfx(π) ≼ acct(a)`. By AccountPrefix, `acct(a) ≼ a`. By transitivity of the prefix relation, `pfx(π) ≼ a`. We conclude the biconditional:

  `pfx(π) ≼ a  ≡  pfx(π) ≼ acct(a)`

Now, when `acct(a) = acct(b)`, substitution gives `pfx(π) ≼ acct(a) ≡ pfx(π) ≼ acct(b)`, and hence `pfx(π) ≼ a ≡ pfx(π) ≼ b`. The set of covering principals — and thus the longest match — is identical.

The effective owner's prefix is always embedded within the account field: `pfx(ω(a)) ≼ acct(a)`. We derive this in four steps. (1) By O1a, `zeros(pfx(ω(a))) ≤ 1`. By T4's field structure (FieldParsing), a valid tumbler with at most one zero separator has at most node and user fields — it contains no document-field or element-field components. (2) By definition of `ω`, `pfx(ω(a)) ≼ a`, so the components of `pfx(ω(a))` match `a`'s leading components. (3) Two cases arise from the zero count. When `zeros(pfx(ω(a))) = 0`: the prefix contains no zero separators, so every component is nonzero; since `pfx(ω(a)) ≼ a`, the first `#pfx(ω(a))` components of `a` are all nonzero, which places them entirely within `a`'s node field; hence `pfx(ω(a)) ≼ N(a) ≼ acct(a)`. When `zeros(pfx(ω(a))) = 1`: the prefix has the form `N.0.U`, and the zero separator at position `α + 1` in the prefix forces — via the prefix relation — a zero at the same position in `a`, aligning `a`'s node-user field boundary with the prefix's; the prefix's user-field components then match `a`'s user-field prefix; since `acct(a)` captures `a` through its full user field, `pfx(ω(a)) ≼ acct(a)`. (4) Hence `#pfx(ω(a)) ≤ #acct(a)` and `pfx(ω(a)) ≼ acct(a)`. The containment may be strict when the address occupies a sub-account position that the effective owner controls but has not delegated. Nelson permits this: "Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose" (LM 4/17). An account-level principal may create sub-account positions as organizational namespaces, ghost elements, or internal partitions without introducing a new ownership principal — the owner decides what sub-numbering means. Equality `pfx(ω(a)) = acct(a)` holds when no intermediate sub-account structure extends beyond the owner's prefix; this is the common case for addresses allocated directly at the principal's own account level.

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

Postcondition (a) is categorical, not conditional. By condition (vi) of the `delegated` relation, no principal in `Π_Σ` has a prefix strictly extending `pfx(π')`; by condition (i), `#pfx(π') > #pfx(π)` where `π` is the most-specific principal in `Π_Σ` covering `pfx(π')`. Hence `π'` has the strictly longest matching prefix in `Π_{Σ'}` for every address in `dom(π')`, and O2 yields `ω_{Σ'}(a) = π'` unconditionally.

The authorization constraint is carried by the `delegated` relation — condition (ii) requires `π` to be the most-specific covering principal. This prevents a grandparent from delegating within a sub-domain it has already handed off: if `π₁` delegates `[1, 0, 2, 3]` to `π₂`, then `π₁` cannot subsequently delegate `[1, 0, 2, 3, 5]` to `π₃`, because `π₂` — not `π₁` — is the most-specific covering principal for that prefix.

Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers" (LM 4/17). The allocation mechanism is uniform ("the entire tumbler works like that," LM 4/19), but the resulting authority is hierarchical: delegation at node and account level creates principals with full sovereignty over their domain, while allocation at document and version level exercises mechanical subdivision rights within the parent principal's domain without establishing independent ownership standing.

The delegation is irrevocable:

**O8 (IrrevocableDelegation).** Once principal `π` delegates to `π'`, the delegating parent never regains effective ownership of addresses in the delegate's domain:

  `(A π, π', a, Σ, Σ' : delegated_Σ(π, π') ∧ a ∈ dom(π') ∩ Σ'.alloc ∧ Σ →⁺ Σ' : ω_{Σ'}(a) ≠ π)`

The formulation captures irrevocability without overclaiming. It says the *parent* can never recover the addresses, while permitting the delegate `π'` to sub-delegate (via O7(c)): if `π'` delegates to `π''` with `pfx(π') ≺ pfx(π'')`, then `ω(a) = π''` for `a ∈ dom(π'')` — the address leaves `π'`'s effective ownership but does not return to `π`. The domain restriction `dom(π') ∩ Σ'.alloc` ensures `ω` is applied only to addresses where it is defined (grounded by O4).

This is a consequence of O3 and O12: once `π'` holds a longer matching prefix than `π`, only a delegation of a *still-longer* prefix can supersede `π'` — and by condition (ii) of the `delegated` relation, only `π'` itself can perform such delegation. The prefix `pfx(π)` is permanently shorter than `pfx(π')` (by O13), so `π` can never regain longest-match status. Nelson: "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). There is no revocation command, no forced reclamation. Gregory confirms: `validaccount` is a stub that unconditionally returns TRUE — the system has no machinery for checking or revoking delegation. Once the sub-prefix exists, the delegate owns it permanently.

The combination of O3 (OwnershipRefinement), O8 (IrrevocableDelegation), O12 (PrincipalPersistence), O13 (PrefixImmutability), and T8 (AllocationPermanence) means the ownership structure of the address space is *monotonically growing*. New ownership domains are created through delegation but never destroyed. The tree of ownership deepens but never prunes.


## Node-Locality

Ownership authority does not propagate across node boundaries. A principal's effective ownership is bounded by its node prefix.

**O9 (NodeLocalOwnership).** For a principal `π`, the ownership predicate `owns(π, a)` can hold only for allocated addresses `a` whose node field extends the principal's node field:

  `(A π ∈ Π, a ∈ Σ.alloc : owns(π, a)  ⟹  N(pfx(π)) ≼ N(a))`

Two cases arise from O1a. When `zeros(pfx(π)) = 1` (account-level), the prefix has the form `N.0.U`, and the zero separator forces field-boundary alignment: `pfx(π) ≼ a` requires `a`'s first zero to appear at the same position as the prefix's zero, giving `N(a) = N(pfx(π))` — full equality. When `zeros(pfx(π)) = 0` (node-level), the prefix is entirely within the node field and contains no boundary markers, so `pfx(π) ≼ a` gives only `N(pfx(π)) ≼ N(a)` — the address may have a longer node field. This is structurally permitted: T10a allows `inc([1, 2], 1) = [1, 2, 1]` (still `zeros = 0`), so addresses with node fields strictly extending the principal's exist.

In both cases, the essential constraint holds: ownership cannot cross node boundaries. A principal at node `[1]` cannot own addresses at node `[2]`, because `[1]` is not a prefix of `[2, ...]`. The node field's leading components must match — only the *length* of the node field may differ, and only for node-level principals.

The consequence is that the same human being would hold *separate, independent* ownership roots on each node — distinct principals with distinct prefixes, distinct domains, and no structural relationship between them. Nelson's "docuverse" is a forest of independently owned trees rooted at nodes, not a single tree with a universal authority. The node operator delegates accounts within its node; those accounts have no automatic standing on any other node.

Gregory's implementation has no cross-node communication, no remote ownership lookup, and no federation of identity. The account tumbler is per-session, per-node. But the abstract property does not depend on these implementation choices — it follows from the prefix geometry of T4 and the structural ownership predicate of O1.


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

In both cases, `π` can always produce an address it effectively owns. The fork operation's postcondition `ω(a') = π` is satisfiable in every reachable state.

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
| O1 | `owns(π, a) ≡ pfx(π) ≼ a` — ownership is prefix containment | introduced |
| O1a | `(A π ∈ Π : zeros(pfx(π)) ≤ 1)` — ownership principals exist only at node or account level | design requirement |
| O1b | `pfx` is injective — distinct principals have distinct prefixes | design requirement |
| O2 | Every allocated address has exactly one effective owner `ω(a)`, determined by longest matching prefix | from O4, O1b |
| O3 | `ω(a)` changes only through delegation introducing a longer matching prefix — monotonic refinement | from T8, O12, O13, O1b |
| AccountLevelPermanence | No external delegation can alter effective ownership within `dom(π)` — changes to `ω(a)` inside a principal's domain arise only from that principal's own acts or its sub-delegates' acts | corollary of O3, O5, O8, O12, O15 |
| O4 | `(A a ∈ Σ.alloc : (E π ∈ Π : pfx(π) ≼ a))` — every allocated address is covered by some principal | introduced |
| O5 | Only the principal with the longest matching prefix may allocate within its domain — subdivision authority | design requirement |
| AccountPrefix | `(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)` — the account field is a prefix of any valid address | introduced |
| O6 | `acct(a) = acct(b) ⟹ ω(a) = ω(b)` — effective owner determined entirely by account field | introduced |
| O7 | Delegation (authorized by `delegated`) confers effective ownership (O2), subdivision authority (O5), and recursive delegation (O7) | introduced |
| O8 | `delegated_Σ(π, π') ∧ a ∈ dom(π') ∩ Σ'.alloc ∧ Σ →⁺ Σ' ⟹ ω_{Σ'}(a) ≠ π` — delegating parent never regains ownership | introduced |
| O9 | `(A π ∈ Π, a ∈ Σ.alloc : owns(π, a) ⟹ N(pfx(π)) ≼ N(a))` — ownership bounded by node field | introduced |
| O10 | Non-ownership of target yields a fork: new address under the requesting principal's domain | introduced |
| O11 | Principal identity is axiomatic to the ownership model — authentication is external | axiom |
| O12 | `(A Σ, Σ' : Σ → Σ' ⟹ Π_Σ ⊆ Π_{Σ'})` — principal persistence | design requirement |
| O13 | `pfx_{Σ'}(π) = pfx_Σ(π)` for all transitions — prefix immutability | design requirement |
| O14 | `Π₀ ≠ ∅`, initial principals cover all initially allocated addresses, `zeros ≤ 1`, `pfx` injective on `Π₀`, `T4(pfx(π))`, and pairwise non-nesting — bootstrap with O1a/O1b/T4/non-nesting base cases | design requirement |
| O15 | Principals enter Π exclusively through bootstrap or delegation; `\|Π_{Σ'} ∖ Π_Σ\| ≤ 1` per transition | design requirement |
| O16 | `(A a ∈ Σ'.alloc ∖ Σ.alloc : (E π ∈ Π_Σ : allocated_by_{Σ'}(π, a)))` — allocation closure | design requirement |
| O17 | `(A Σ, a : a ∈ Σ.alloc ⟹ T4(a))` — every allocated address is a valid tumbler | axiom |
| `ω(a)` | `effectiveOwner : Σ.alloc → Principal` — the effective owner function (defined only for allocated addresses) | introduced |
| OwnershipDomain | `{a ∈ T : pfx(π) ≼ a}` — the ownership domain of a principal | introduced |
| `acct(a)` | When `zeros(a) = 0`: `acct(a) = a`; when `zeros(a) ≥ 1`: truncation through user field | introduced |
| `allocated_by_Σ(π, a)` | Primitive relation: `a` was allocated by `π` in transition producing `Σ`; mechanism out of scope, constrained by O5 and O16 | introduced |
| Delegation | `π'` introduced into `Π` by act of `π`, with `pfx(π) ≺ pfx(π')`, `π` most-specific covering principal, no existing principal extends `pfx(π')`, `zeros(pfx(π')) ≤ 1`, and `T4(pfx(π'))` | introduced |
| `pfx(π)` | `ownershipPrefix : Principal → Tumbler` — injective, `zeros(pfx(π)) ≤ 1`, `T4(pfx(π))` | introduced |


## Open Questions

- Must the system provide a mechanism for ownership transfer, and if so, what invariants must it preserve given that structural provenance (O6) is inalienable?
- Must the system enforce that no principal can claim an ownership prefix that overlaps an existing principal's domain, and what are the invariants of this enforcement?
- What formal guarantees must the system provide about content accessibility when the effective owner ceases to exist as a principal?
- Must ownership domains be dense (every address in the domain is reachable) or can gaps exist between baptized siblings within a domain?
- What invariants must a cross-node identity federation satisfy to remain consistent with O9, if such federation is introduced?
- What formal relationship must hold between the provenance recorded in an address (O6) and the effective owner (O2) if ownership transfer is permitted?
- Must delegation events be recorded, or is the structural evidence of the address hierarchy sufficient to reconstruct the delegation history?
