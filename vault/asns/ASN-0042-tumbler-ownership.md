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

Define `acct(a)` for any valid tumbler `a`: when `zeros(a) = 0` (node-level), `acct(a) = a`; when `zeros(a) ≥ 1`, `acct(a)` is the truncation of `a` through its user field — the tumbler `N₁...Nα.0.U₁...Uβ`, having `zeros(acct(a)) = 1`.

Gregory confirms the account-level boundary with unusual force. His `tumbleraccounteq` walks the mantissa of both tumblers in lockstep. For each non-zero component in the account tumbler, the document's component must match. For each zero, the counter advances. When the counter reaches two — the second zero — the function returns true unconditionally. Everything beyond the second zero is ignored. The implementation has no mechanism for finer-grained discrimination: `isthisusersdocument` (in all three build targets — `be.c`, `socketbe.c`, `xumain.c`) delegates directly to `tumbleraccounteq` with no intervening check. There is no per-document, per-version, or per-element authorization predicate anywhere in the codebase. The BERT system tracks per-document open/close state, but its authorization fallback is `isthisusersdocument` — account-level.

The consequence: sub-account allocation (creating documents, versions, elements) creates addresses within the allocating principal's domain but does not partition that domain into sub-ownerships. A document address `N.0.U.0.D.0.E` and a different document address `N.0.U.0.D'.0.E'` under the same account are owned by the same principal — the one whose prefix matches `N.0.U`. Below the account level, there is only the binary distinction of "mine" versus "not mine."

O1a permits nesting *within* the account level. T4 allows multi-component user fields: `pfx(π₁) = [1, 0, 2]` and `pfx(π₂) = [1, 0, 2, 3]` both satisfy `zeros ≤ 1`, and `pfx(π₁) ≺ pfx(π₂)`. Nelson designed this deliberately: "accounts can spin off accounts" (LM 4/19). The User field is a tree, not a flat namespace — a principal may delegate a sub-account by forking a longer user field within its own prefix. Gregory confirms: `tumbleraccounteq` applied to account `[1, 0, 2, 3]` checks positions 0, 2, and 3, while account `[1, 0, 2]` checks only positions 0 and 2 — the child account is a strict refinement. What O1a prevents is *document-level* or *element-level* principals: no principal has `zeros(pfx(π)) ≥ 2`. The floor of ownership is the account level, but within that floor, the user-field tree can grow arbitrarily deep.


## Ownership Domains

Each principal's prefix determines a set of addresses — their *domain*:

**Definition (Ownership Domain).** For principal `π ∈ Π`, define `dom(π) = {a ∈ T : pfx(π) ≼ a}`.

By T5 (ContiguousSubtrees), every ownership domain is a contiguous interval under the lexicographic order T1. This is a mathematical consequence of prefix containment and the tree-to-line mapping, not a policy choice. If `a, c ∈ dom(π)` and `a ≤ b ≤ c`, then `b ∈ dom(π)`. No address can escape from the interior of someone's domain.

Domains nest. A node operator's domain contains all account domains at that node. An account holder's domain contains all document addresses under that account. The nesting respects the field structure:

  `zeros(pfx(π₁)) < zeros(pfx(π₂)) ∧ pfx(π₁) ≼ pfx(π₂)  ⟹  dom(π₂) ⊆ dom(π₁)`

A principal at a higher hierarchical level (fewer zeros in their prefix, hence a broader scope) whose prefix is itself a prefix of another's contains that principal's entire domain.


## State Axioms

The ownership model rests on four axioms about state evolution that the subsequent derivations assume. We state them explicitly.

**O12 (PrincipalPersistence).** Once a principal joins Π, no operation removes it:

  `(A Σ, Σ' : Σ → Σ' ⟹ Π_Σ ⊆ Π_{Σ'})`

Nelson's architecture contains no concept of account revocation. Gregory's codebase contains no deletion path for account entries. Addresses are permanent (T8), and a principal's prefix is a valid tumbler — removing the principal would orphan its domain with no effective owner, violating O4 below.

**O13 (PrefixImmutability).** Once established, a principal's ownership prefix cannot be altered:

  `(A π ∈ Π_Σ, Σ, Σ' : Σ → Σ' ∧ π ∈ Π_{Σ'} ⟹ pfx_{Σ'}(π) = pfx_Σ(π))`

The prefix is a tumbler, and the tumbler algebra provides no operation that mutates an existing tumbler in place. Since addresses are permanent (T8) and the prefix is structurally embedded in its domain's addresses, altering it would require rewriting every address in the domain — an operation the system does not support.

**O14 (BootstrapPrincipal).** The initial state contains at least one principal whose domain covers all initially allocatable addresses:

  `Π₀ ≠ ∅  ∧  (A a ∈ Σ₀.alloc : (E π ∈ Π₀ : pfx(π) ≼ a))`

In a single-node system, this is the node operator — the principal holding the node-level prefix from which all delegation proceeds. In a multi-node system, `Π₀` contains one initial principal per node (e.g., principals at `[1]` and `[2]`), each independently covering its node's allocatable addresses. The formalization permits both cases: the existential quantifier ranges over all of `Π₀`, not a single distinguished element. Without this base case, the inductive argument for O4 (DomainCoverage) cannot begin.

**O15 (PrincipalClosure).** Principals enter Π exclusively through bootstrap (in Π₀) or delegation (satisfying the `delegated` relation defined below). No other mechanism introduces principals. Each state transition introduces at most one new principal:

  `(A Σ, Σ' : Σ → Σ' ⟹ |Π_{Σ'} ∖ Π_Σ| ≤ 1)`

  `(A π' ∈ Π_{Σ'} ∖ Π_Σ : (E π ∈ Π_Σ : delegated_Σ(π, π')))`

Without this closure, O12 permits arbitrary growth of Π — a mechanism outside the delegation relation could introduce a principal at document level (violating O1a) or within a sub-domain without the effective owner's consent (circumventing the authorization guarantee of delegation condition (ii)). Nelson's design contains no concept of principals appearing outside the delegation hierarchy, and Gregory's codebase provides no mechanism for it. The at-most-one constraint reflects the atomic nature of a delegation act: one delegator, one delegate, one prefix.


## The Exclusivity Invariant

Can two principals simultaneously own the same address?

Nelson uses the definite article throughout: "*the* owner of a given item" (LM 4/20), not "an owner." Gregory's predicate returns a boolean — true or false, with no provision for multiple true results from distinct principals. The system requires exactly one effective owner per address.

For non-nesting prefixes, T10 (PartitionIndependence) gives disjointness immediately: two principals whose prefixes satisfy `pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁)` have disjoint domains. The interesting case is nested domains — when a node operator's domain contains an account holder's. Here, Nelson is explicit: the node operator creates accounts, but "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). Delegation permanently transfers effective ownership of the subdomain.

We first state a coverage requirement — every allocated address falls within some principal's domain:

**O4 (DomainCoverage).** For every allocated address, at least one principal's prefix contains it:

  `(A a ∈ Σ.alloc : (E π ∈ Π : pfx(π) ≼ a))`

This follows from O5 (SubdivisionAuthority, stated below) and O14 (BootstrapPrincipal): allocation only occurs within an existing principal's domain, so every allocated address is born under a covering prefix. The derivation: by O14, the initial state has a principal covering all initially allocated addresses. If `a` is newly allocated in a transition Σ → Σ', then by O5 the allocator is a principal `π` with `pfx(π) ≼ a`. By O12, `π` persists in Σ'. For addresses already in `Σ.alloc`, their covering principals persist in `Σ'` (O12) with unchanged prefixes (O13), so coverage is preserved. By induction on the transition history, O4 holds in every reachable state.

We resolve nesting by specificity:

**O2 (OwnershipExclusivity).** For every allocated address `a`, there exists exactly one principal that effectively owns `a`:

  `(A a ∈ Σ.alloc : (E! π ∈ Π : ω(a) = π))`

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

The argument: `ω(a)` depends on three inputs — the address `a`, the set of principals `Π`, and their prefixes. The address `a` is permanent (T8). By O13 (PrefixImmutability), no operation changes an existing principal's prefix. By O12 (PrincipalPersistence), no operation removes a principal from Π. Hence `ω(a)` can change only when `Π` grows — i.e., when delegation introduces a new principal whose prefix is a prefix of `a` and is longer than the current effective owner's.

Refinement is one-directional: `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))` in all transitions. Once a principal `π` becomes the effective owner through longest-match, only a *more specific* delegation can supersede it.

**Corollary (Account-level permanence).** Account-level prefixes can nest — `pfx(π₁) = [1, 0, 2]` and `pfx(π₂) = [1, 0, 2, 3]` both satisfy O1a, and delegation from `π₁` to `π₂` changes `ω` for addresses in `dom(π₂)`. But such delegation requires an act of `π₁` itself: by O5 (for allocation) and condition (ii) of the `delegated` relation (for delegation), only the most-specific covering principal may allocate or delegate within its domain. By O15 (PrincipalClosure), delegation is the exclusive mechanism for introducing principals post-bootstrap. No delegation can introduce a principal whose prefix extends `pfx(π)` without `π`'s involvement: condition (ii) of the `delegated` relation requires the delegator to be the most-specific covering principal for the new prefix. For any prefix extending `pfx(π)`, that most-specific covering principal is `π` itself (or a sub-delegate of `π` within `dom(π)`). Nelson confirms: "User 3 controls allocation of children directly under 3. User 3.2 controls everything under 3.2. User 3 cannot modify User 3.2's documents" (consultation, LM 4/20, 4/29, 2/29). The parent controls baptism; the child controls content. Changes to `ω` within `dom(π)` arise only from `π`'s own delegation choices, or recursively from sub-delegates' choices within their own sub-domains. This is Nelson's "forevermore": not that `ω` is static within `dom(π)`, but that no external act can alter it. The addresses `π` has not sub-delegated remain permanently under `π`'s effective ownership.

This raises a tension that Nelson himself acknowledges. He mentions "someone who has bought the document rights" (LM 2/29), implying ownership can *transfer*. But the address permanently encodes the originating account (by O6 and T8), and Gregory's codebase contains no transfer mechanism whatsoever — no FEBE command, no data structure, no protocol step. We take the conservative reading: O3 describes the refinement regime for the system as specified. Transfer, if it exists, would require machinery that overrides the address-derived ownership — a registry external to the address structure — and Nelson leaves such machinery unspecified. The address is a birth certificate; a transfer would require a separate deed. We record this as an open question.


## Worked Example

We verify the properties against a concrete scenario. Let principal `π_N` be a node operator with `pfx(π_N) = [1]` (`zeros = 0`). Initially, `Π = {π_N}`.

**State Σ₀.** `π_N` is the sole principal. For any address `a` with node field `1`, `ω(a) = π_N` (the only matching prefix). O2 holds trivially — one principal, one match. O4 holds: every allocated address under node `1` is covered by `pfx(π_N)`.

**Delegation.** `π_N` delegates account prefix `[1, 0, 2]` to new principal `π_A`. Now `Π = {π_N, π_A}`.

**State Σ₁.** Consider address `a₁ = [1, 0, 2, 0, 3, 0, 1]` (a document element under account `[1, 0, 2]`). Both principals' prefixes contain `a₁`: `[1] ≼ a₁` and `[1, 0, 2] ≼ a₁`. The longer match is `[1, 0, 2]`, so `ω(a₁) = π_A`. We verify:

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

**Lemma (AccountPrefix).** `(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)`

The T4 restriction is essential: `acct` relies on field parsing (FieldParsing from ASN-0034), which requires T4 validity — for a tumbler like `[0, 0, 1]`, the field boundaries are ill-defined and `acct` is not well-defined. All allocated addresses satisfy T4, so the restriction does not limit application.

When `zeros(a) = 0`, `acct(a) = a` and the claim is trivial. When `zeros(a) ≥ 1`, `acct(a)` is the truncation of `a` through its user field — the leading `N₁...Nα.0.U₁...Uβ` components — so `acct(a)` is literally a prefix of `a` by construction.

The proof of O6 proceeds in two directions. *Forward:* for any principal `π` with `zeros(pfx(π)) ≤ 1`, the prefix `pfx(π)` has at most node and user fields — by T4's field structure, a valid tumbler with `zeros ≤ 1` contains at most one zero separator, so its components span at most the node field and user field, with no document or element components. Since `pfx(π) ≼ a`, the components of `pfx(π)` match `a`'s leading components, and these leading components — being confined to node and user fields by the zero count — form a prefix of the components in `acct(a)`. Hence `pfx(π) ≼ a` implies `pfx(π) ≼ acct(a)`. *Reverse:* suppose `pfx(π) ≼ acct(a)`. By AccountPrefix, `acct(a) ≼ a`. By transitivity of the prefix relation, `pfx(π) ≼ a`. We conclude the biconditional:

  `pfx(π) ≼ a  ≡  pfx(π) ≼ acct(a)`

Now, when `acct(a) = acct(b)`, substitution gives `pfx(π) ≼ acct(a) ≡ pfx(π) ≼ acct(b)`, and hence `pfx(π) ≼ a ≡ pfx(π) ≼ b`. The set of covering principals — and thus the longest match — is identical.

The effective owner's prefix is always embedded within the account field: `pfx(ω(a)) ≼ acct(a)`. We derive this in four steps. (1) By O1a, `zeros(pfx(ω(a))) ≤ 1`. By T4's field structure (FieldParsing), a valid tumbler with at most one zero separator has at most node and user fields — it contains no document-field or element-field components. (2) By definition of `ω`, `pfx(ω(a)) ≼ a`, so the components of `pfx(ω(a))` match `a`'s leading components. (3) Two cases arise from the zero count. When `zeros(pfx(ω(a))) = 0`: the prefix contains no zero separators, so every component is nonzero; since `pfx(ω(a)) ≼ a`, the first `#pfx(ω(a))` components of `a` are all nonzero, which places them entirely within `a`'s node field; hence `pfx(ω(a)) ≼ nodeField(a) ≼ acct(a)`. When `zeros(pfx(ω(a))) = 1`: the prefix has the form `N.0.U`, and the zero separator at position `α + 1` in the prefix forces — via the prefix relation — a zero at the same position in `a`, aligning `a`'s node-user field boundary with the prefix's; the prefix's user-field components then match `a`'s user-field prefix; since `acct(a)` captures `a` through its full user field, `pfx(ω(a)) ≼ acct(a)`. (4) Hence `#pfx(ω(a)) ≤ #acct(a)` and `pfx(ω(a)) ≼ acct(a)`. The containment may be strict when the address occupies a sub-account position that the effective owner controls but has not delegated. Nelson permits this: "Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose" (LM 4/17). An account-level principal may create sub-account positions as organizational namespaces, ghost elements, or internal partitions without introducing a new ownership principal — the owner decides what sub-numbering means. Equality `pfx(ω(a)) = acct(a)` holds when no intermediate sub-account structure extends beyond the owner's prefix; this is the common case for addresses allocated directly at the principal's own account level.

Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" (LM 2/40).

Provenance is not a right that can be exercised or waived — it is an inalienable structural fact. Even if ownership were to transfer (contrary to O3, and through some unspecified mechanism), the address would still record the original principal's identity. The new owner might act upon the content, but the address would forever testify to its origin. This separation — between *who created* and *who currently holds rights* — is what makes ownership transfer conceptually possible without violating address permanence. The address encodes provenance; ownership encodes authority. Under the system as specified, these coincide. Under a hypothetical transfer regime, they would diverge.

Gregory confirms: the User field in the tumbler `Node.0.User.0.Doc.0.Element` is a permanent structural component. The `tumbleraccounteq` function reads these components directly from the mantissa array. There is no indirection, no lookup, no level of abstraction that could mask the origin.


## Subdivision Authority

Of the rights that ownership confers, one is essential to the ownership model itself: the right to create sub-positions.

**O5 (SubdivisionAuthority).** Only the principal with the longest matching prefix may allocate new addresses within its domain:

  `(A a ∈ T, π : a newly allocated by π  ⟹  pfx(π) ≼ a  ∧  (A π' ∈ Π : pfx(π') ≼ a ⟹ #pfx(π') ≤ #pfx(π)))`

This formulation avoids applying `ω` to the prefix itself (which may not yet be in `Σ.alloc`); instead it directly constrains the allocator to be the most-specific covering principal. Once `a` enters `Σ.alloc`, O2 gives `ω(a) = π` — the allocator becomes the effective owner of its own allocation.

Nelson: "The owner of a given item controls the allocation of the numbers under it" (LM 4/20). This is the *right to baptize* — not the baptism mechanism itself (which belongs to the tumbler baptism specification), but the authorization constraint that governs who may invoke it.

Gregory confirms: `docreatenewdocument` always uses `taskptr->account` — the session's own prefix — as the allocation hint. The allocation algorithm operates within the boundary determined by the session's account tumbler. There is no parameter that allows specifying someone else's prefix as the allocation target.

O5 interacts with O2. Because ownership is exclusive, exactly one principal may allocate at any point in the address space. Because ownership is determined by prefix (O1), the authorized allocator is determined structurally. The conjunction of O2 and O5 means the address space grows exclusively through the actions of the principals who own each region — no external intervention, no administrative override, no "root user" who may allocate anywhere.


## Delegation

Ownership is not held at a single level — it flows downward through the hierarchy. Nelson calls this "baptism," but we must separate two concepts: *ownership delegation*, which introduces a new principal into `Π`, and *allocation*, which creates addresses within an existing principal's domain. The allocation mechanism is uniform at all levels (T10a); the ownership consequences differ.

We first define the delegation relation, which the subsequent properties rely upon. We use the *strict prefix* relation throughout: `p ≺ a  ≡  p ≼ a ∧ p ≠ a` (equivalently, `p ≼ a ∧ #p < #a` — the equivalence holds because `p ≼ a ∧ #p = #a` gives `p = a` by T3).

**Definition (Delegation).** We write `delegated_Σ(π, π')` to mean that principal `π'` was introduced into `Π` by an act of `π` in state transition `Σ → Σ'`, subject to four structural constraints:

  (i) `pfx(π) ≺ pfx(π')` — the delegate's prefix strictly extends the delegator's

  (ii) `π` is the most-specific covering principal for `pfx(π')` at the time of delegation: `(A π'' ∈ Π_Σ : pfx(π'') ≼ pfx(π') ⟹ #pfx(π'') ≤ #pfx(π))`

  (iii) `π' ∈ Π_{Σ'} ∖ Π_Σ` — the delegate is newly introduced

  (iv) `zeros(pfx(π')) ≤ 1` — the delegate's prefix is at node or account level

Condition (ii) is the authorization constraint — delegation requires O5's subdivision authority. A principal cannot delegate within a sub-domain that has already been delegated to someone else. This grounds the distinction between direct delegation (`π → π'`) and transitive delegation (`π → π' → π''`): when `π` delegates to `π'` and `π'` later delegates to `π''`, we have `delegated(π, π')` and `delegated(π', π'')` but not `delegated(π, π'')`.

Delegation preserves O1a (AccountPrefix). By condition (iv), any `π'` admitted by the `delegated` relation satisfies `zeros(pfx(π')) ≤ 1`. Since O1a requires exactly this — that every principal's prefix is at node or account level — the new principal satisfies O1a by construction, and the existing principals are unchanged by O12. O1a is maintained.

Delegation preserves O1b (PrefixInjectivity). Suppose for contradiction that `pfx(π') = pfx(π''')` for some existing `π''' ∈ Π_Σ`. Then `pfx(π''') ≼ pfx(π')`, so by condition (ii) of the delegation relation, `#pfx(π''') ≤ #pfx(π)`. But from condition (i), `pfx(π) ≺ pfx(π')`, giving `#pfx(π) < #pfx(π')`. Combining: `#pfx(π''') ≤ #pfx(π) < #pfx(π') = #pfx(π''')` — a contradiction. Hence every delegation introduces a principal with a prefix distinct from all existing prefixes. By O15, each transition introduces at most one new principal, so no pairwise collision among newly introduced principals can occur — the proof against existing principals is exhaustive. O1b is maintained across all state transitions. This closes the proof chain: delegation preserves both O1a and O1b, which ensures `ω` (O2) yields a unique principal at a valid hierarchy level.

**O7 (OwnershipDelegation).** A principal `π` may delegate a sub-prefix to a new principal `π'`, provided the `delegated` relation is satisfied (which entails `zeros(pfx(π')) ≤ 1` by condition (iv)) and `π` holds subdivision authority over `pfx(π')`. Upon delegation:

  `(A π, π' : delegated(π, π') :`

  (a) `ω(a) = π'` for all `a ∈ dom(π') ∩ Σ.alloc` where `π'` has the longest matching prefix (O2 applies)

  (b) `π'` may allocate new addresses within `dom(π')` (O5 applies to `π'`)

  (c) `π'` may delegate sub-prefixes `p''` with `pfx(π') ≺ p''` per O7 recursively

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

**O9 (NodeLocalOwnership).** For a principal `π`, the ownership predicate `owns(π, a)` can hold only for addresses `a` whose node field extends the principal's node field:

  `(A π ∈ Π, a ∈ T : owns(π, a)  ⟹  nodeField(pfx(π)) ≼ nodeField(a))`

Two cases arise from O1a. When `zeros(pfx(π)) = 1` (account-level), the prefix has the form `N.0.U`, and the zero separator forces field-boundary alignment: `pfx(π) ≼ a` requires `a`'s first zero to appear at the same position as the prefix's zero, giving `nodeField(a) = nodeField(pfx(π))` — full equality. When `zeros(pfx(π)) = 0` (node-level), the prefix is entirely within the node field and contains no boundary markers, so `pfx(π) ≼ a` gives only `nodeField(pfx(π)) ≼ nodeField(a)` — the address may have a longer node field. This is structurally permitted: T10a allows `inc([1, 2], 1) = [1, 2, 1]` (still `zeros = 0`), so addresses with node fields strictly extending the principal's exist.

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
| O0 | Ownership of `a` by `π` is decidable from `pfx(π)` and `a` alone, without mutable state | introduced |
| O1 | `owns(π, a) ≡ pfx(π) ≼ a` — ownership is prefix containment | introduced |
| O1a | `(A π ∈ Π : zeros(pfx(π)) ≤ 1)` — ownership principals exist only at node or account level | introduced |
| O1b | `pfx` is injective — distinct principals have distinct prefixes | introduced |
| O2 | Every allocated address has exactly one effective owner `ω(a)`, determined by longest matching prefix | introduced |
| O3 | `ω(a)` changes only through delegation introducing a longer matching prefix — monotonic refinement | introduced |
| O4 | `(A a ∈ Σ.alloc : (E π ∈ Π : pfx(π) ≼ a))` — every allocated address is covered by some principal | introduced |
| O5 | Only the principal with the longest matching prefix may allocate within its domain — subdivision authority | introduced |
| AccountPrefix | `(A a ∈ T : T4(a) ⟹ acct(a) ≼ a)` — the account field is a prefix of any valid address | introduced |
| O6 | `acct(a) = acct(b) ⟹ ω(a) = ω(b)` — effective owner determined entirely by account field | introduced |
| O7 | Delegation (authorized by `delegated`) confers effective ownership (O2), subdivision authority (O5), and recursive delegation (O7) | introduced |
| O8 | `delegated_Σ(π, π') ∧ a ∈ dom(π') ∩ Σ'.alloc ∧ Σ →⁺ Σ' ⟹ ω_{Σ'}(a) ≠ π` — delegating parent never regains ownership | introduced |
| O9 | `owns(π, a) ⟹ nodeField(pfx(π)) ≼ nodeField(a)` — ownership bounded by node field | introduced |
| O10 | Non-ownership of target yields a fork: new address under the requesting principal's domain | introduced |
| O11 | Principal identity is axiomatic to the ownership model — authentication is external | introduced |
| O12 | `(A Σ, Σ' : Σ → Σ' ⟹ Π_Σ ⊆ Π_{Σ'})` — principal persistence | introduced |
| O13 | `pfx_{Σ'}(π) = pfx_Σ(π)` for all transitions — prefix immutability | introduced |
| O14 | `Π₀ ≠ ∅` and initial principals cover all initially allocated addresses — bootstrap | introduced |
| O15 | Principals enter Π exclusively through bootstrap or delegation; `|Π_{Σ'} ∖ Π_Σ| ≤ 1` per transition | introduced |
| `ω(a)` | `effectiveOwner : ValidAddress → Principal` — the effective owner function | introduced |
| `dom(π)` | `{a ∈ T : pfx(π) ≼ a}` — the ownership domain of a principal | introduced |
| `acct(a)` | When `zeros(a) = 0`: `acct(a) = a`; when `zeros(a) ≥ 1`: truncation through user field | introduced |
| `delegated_Σ(π, π')` | `π'` introduced into `Π` by act of `π`, with `pfx(π) ≺ pfx(π')`, `π` most-specific covering principal, and `zeros(pfx(π')) ≤ 1` | introduced |
| `pfx(π)` | `ownershipPrefix : Principal → Tumbler` — injective, `zeros(pfx(π)) ≤ 1` | introduced |


## Open Questions

- Must the system provide a mechanism for ownership transfer, and if so, what invariants must it preserve given that structural provenance (O6) is inalienable?
- Must the system enforce that no principal can claim an ownership prefix that overlaps an existing principal's domain, and what are the invariants of this enforcement?
- What formal guarantees must the system provide about content accessibility when the effective owner ceases to exist as a principal?
- Must ownership domains be dense (every address in the domain is reachable) or can gaps exist between baptized siblings within a domain?
- What invariants must a cross-node identity federation satisfy to remain consistent with O9, if such federation is introduced?
- What formal relationship must hold between the provenance recorded in an address (O6) and the effective owner (O2) if ownership transfer is permitted?
- Must delegation events be recorded, or is the structural evidence of the address hierarchy sufficient to reconstruct the delegation history?
