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

The consequence: sub-account allocation creates addresses within the allocating principal's domain but does not partition that domain into sub-ownerships. A document address `N.0.U.0.D.0.E` and a different document address `N.0.U.0.D'.0.E'` under the same account are owned by the same principal — the one whose prefix matches `N.0.U`. The account level is the atom of ownership; below it, there is only the binary distinction of "mine" versus "not mine."


## Ownership Domains

Each principal's prefix determines a set of addresses — their *domain*:

**Definition (Ownership Domain).** For principal `π ∈ Π`, define `dom(π) = {a ∈ T : pfx(π) ≼ a}`.

By T5 (ContiguousSubtrees), every ownership domain is a contiguous interval under the lexicographic order T1. This is a mathematical consequence of prefix containment and the tree-to-line mapping, not a policy choice. If `a, c ∈ dom(π)` and `a ≤ b ≤ c`, then `b ∈ dom(π)`. No address can escape from the interior of someone's domain.

Domains nest. A node operator's domain contains all account domains at that node. An account holder's domain contains all document addresses under that account. The nesting respects the field structure:

  `zeros(pfx(π₁)) < zeros(pfx(π₂)) ∧ pfx(π₁) ≼ pfx(π₂)  ⟹  dom(π₂) ⊆ dom(π₁)`

A principal at a higher hierarchical level (fewer zeros in their prefix, hence a broader scope) whose prefix is itself a prefix of another's contains that principal's entire domain.


## The Exclusivity Invariant

Can two principals simultaneously own the same address?

Nelson uses the definite article throughout: "*the* owner of a given item" (LM 4/20), not "an owner." Gregory's predicate returns a boolean — true or false, with no provision for multiple true results from distinct principals. The system requires exactly one effective owner per address.

For non-nesting prefixes, T10 (PartitionIndependence) gives disjointness immediately: two principals whose prefixes satisfy `pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁)` have disjoint domains. The interesting case is nested domains — when a node operator's domain contains an account holder's. Here, Nelson is explicit: the node operator creates accounts, but "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). Delegation permanently transfers effective ownership of the subdomain.

We first state a coverage requirement — every allocated address falls within some principal's domain:

**O4 (DomainCoverage).** For every allocated address, at least one principal's prefix contains it:

  `(A a ∈ Σ.alloc : (E π ∈ Π : pfx(π) ≼ a))`

This follows from O5 (SubdivisionAuthority, stated below): allocation only occurs within an existing principal's domain, so every allocated address is born under a covering prefix. The derivation: if `a` was newly allocated, then by O5 the allocator holds a prefix `p` with `p ≼ a`. By induction on allocation history, the first address was allocated by the bootstrap principal (the initial node operator), whose prefix covers the initial allocation. Every subsequent allocation extends an existing principal's domain. Hence O4 holds in every reachable state.

We resolve nesting by specificity:

**O2 (OwnershipExclusivity).** For every allocated address `a`, there exists exactly one principal that effectively owns `a`:

  `(A a ∈ Σ.alloc : (E! π ∈ Π : ω(a) = π))`

where `ω(a)` — the *effective owner* — is the principal with the longest matching prefix:

  `ω(a) = π  ≡  pfx(π) ≼ a  ∧  (A π' ∈ Π : π' ≠ π ∧ pfx(π') ≼ a : #pfx(π) > #pfx(π'))`

Well-definedness of `ω` requires three observations: (i) by O4, at least one principal's prefix contains any allocated address; (ii) any two containing prefixes are linearly ordered by the prefix relation (if `p₁ ≼ a` and `p₂ ≼ a`, either `p₁ ≼ p₂` or `p₂ ≼ p₁` — because both are prefixes of the same tumbler, and the prefix relation on a single path in the tree is total), hence the longest prefix is unique; and (iii) by O1b, the principal holding that longest prefix is unique. Together these give `(E! π :: ω(a) = π)`.

The exclusivity of ownership is load-bearing. If two parties owned the same address, the system could not determine who is entitled to subdivide the space beneath it (O5 below), who originated the content (O6 below), or whose delegation created the address. Every downstream property depends on O2.


## Permanence and Refinement

Nelson is emphatic: ownership does not expire.

> "Once assigned a User account, the user will have full control over its subdivision forevermore." (LM 4/29)

"Forevermore" is strong language in a technical specification. But the naive reading — that `ω(a)` never changes — is too strong. Consider a node operator `π₁` with `pfx(π₁) = [1]`. Before any delegation, `ω(a) = π₁` for every address `a` with node field `1`. When `π₁` delegates account prefix `[1, 0, 2]` to principal `π₂`, the effective owner of every address under `[1, 0, 2]` changes from `π₁` to `π₂` — the longer prefix wins. Nelson's "forevermore" does not mean `ω` never changes; it means the *account holder's* ownership is permanent, because no finer-grained principal can be introduced below account level (by O1a).

The correct invariant is monotonic refinement — `ω(a)` can change only through delegation, and only by becoming more specific:

**O3 (OwnershipRefinement).** The effective owner of an address changes only when delegation introduces a principal with a strictly longer matching prefix. No other transition alters `ω`:

  `(A a ∈ Σ.alloc, Σ, Σ' : Σ → Σ' ∧ ω_{Σ'}(a) ≠ ω_Σ(a)  ⟹  (E π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a))))`

The argument: `ω(a)` depends on three inputs — the address `a`, the set of principals `Π`, and their prefixes. The address `a` is permanent (T8). No operation changes an existing principal's prefix (delegation creates new principals, it does not alter existing ones). Hence `ω(a)` can change only when `Π` grows — i.e., when delegation introduces a new principal whose prefix is a prefix of `a` and is longer than the current effective owner's.

Refinement is one-directional: `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))` in all transitions. Once a principal `π` becomes the effective owner through longest-match, only a *more specific* delegation can supersede it.

**Corollary (Account-level permanence).** For an account-level principal `π` with `zeros(pfx(π)) = 1`, O1a guarantees that no ownership principal has a prefix strictly extending `pfx(π)` — sub-account allocation creates addresses within `dom(π)` but does not introduce new principals. Therefore, once `ω(a) = π` for `a ∈ dom(π)`, no subsequent delegation can produce a longer matching prefix, and `ω(a) = π` holds in all future states. This is precisely Nelson's "forevermore."

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

- **O5**: `ω([1, 0, 2]) = π_A` — the allocator owns the containing prefix. ✓
- **O6**: `acct(a₂) = [1, 0, 2] = pfx(π_A)` — provenance names the owner. ✓

**Account-level permanence.** Since `zeros(pfx(π_A)) = 1`, O1a ensures no principal with a longer prefix extending `[1, 0, 2]` can join `Π`. Sub-account allocation (documents, versions, elements) does not create principals. Hence `ω(a₁) = π_A` and `ω(a₂) = π_A` in all future states. Nelson's "forevermore" holds.

Now consider address `a₃ = [1, 0, 7, 0, 1, 0, 1]` under a different account. `pfx(π_A) = [1, 0, 2] ⋠ a₃` (component 3: `2 ≠ 7`). Only `pfx(π_N) = [1] ≼ a₃`, so `ω(a₃) = π_N`. The node operator retains effective ownership of all addresses not covered by a delegated account.


## Structural Provenance

The ownership prefix is embedded in the permanent address. Because the account-level prefix `acct(a)` is a structural component of `a`, and addresses are permanent (T8), the system can always determine who originally allocated any content:

**O6 (StructuralProvenance).** The account-level prefix of any allocated address permanently identifies the owning principal:

  `(A a ∈ Σ.alloc : zeros(pfx(ω(a))) = 1  ⟹  acct(a) = pfx(ω(a)))`

For account-level principals, the address structure and the ownership function coincide — `acct(a)` names the effective owner directly.

Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" (LM 2/40).

Provenance is not a right that can be exercised or waived — it is an inalienable structural fact. Even if ownership were to transfer (contrary to O3, and through some unspecified mechanism), the address would still record the original principal's identity. The new owner might act upon the content, but the address would forever testify to its origin. This separation — between *who created* and *who currently holds rights* — is what makes ownership transfer conceptually possible without violating address permanence. The address encodes provenance; ownership encodes authority. Under the system as specified, these coincide. Under a hypothetical transfer regime, they would diverge.

Gregory confirms: the User field in the tumbler `Node.0.User.0.Doc.0.Element` is a permanent structural component. The `tumbleraccounteq` function reads these components directly from the mantissa array. There is no indirection, no lookup, no level of abstraction that could mask the origin.


## Subdivision Authority

Of the rights that ownership confers, one is essential to the ownership model itself: the right to create sub-positions.

**O5 (SubdivisionAuthority).** Only the effective owner of a domain may allocate new addresses within it:

  `(A a ∈ T : a newly allocated under prefix p  ⟹  ω(p) = allocator)`

Nelson: "The owner of a given item controls the allocation of the numbers under it" (LM 4/20). This is the *right to baptize* — not the baptism mechanism itself (which belongs to the tumbler baptism specification), but the authorization constraint that governs who may invoke it.

Gregory confirms: `docreatenewdocument` always uses `taskptr->account` — the session's own prefix — as the allocation hint. The allocation algorithm operates within the boundary determined by the session's account tumbler. There is no parameter that allows specifying someone else's prefix as the allocation target.

O5 interacts with O2. Because ownership is exclusive, exactly one principal may allocate at any point in the address space. Because ownership is determined by prefix (O1), the authorized allocator is determined structurally. The conjunction of O2 and O5 means the address space grows exclusively through the actions of the principals who own each region — no external intervention, no administrative override, no "root user" who may allocate anywhere.


## Delegation

Ownership is not held at a single level — it flows downward through the hierarchy. Nelson calls this "baptism," but we must separate two concepts: *ownership delegation*, which introduces a new principal into `Π`, and *allocation*, which creates addresses within an existing principal's domain. The allocation mechanism is uniform at all levels (T10a); the ownership consequences differ.

**O7 (OwnershipDelegation).** A principal `π` may delegate a sub-prefix `p'` extending `pfx(π)` to a new principal `π'`, provided the delegation respects O1a — the new prefix must satisfy `zeros(p') ≤ 1`:

  `(A π, π' : pfx(π) ≺ pfx(π') ∧ zeros(pfx(π')) ≤ 1 ∧ delegated(π, π') : rights(π', dom(π')) ≅ rights(π, dom(π)))`

where `≅` denotes structural equivalence of the rights bundle: the same right to subdivide (O5), the same provenance encoding (O6), and the same ability to delegate further. Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers" (LM 4/17). The allocation mechanism is uniform ("the entire tumbler works like that," LM 4/19), but the resulting authority is hierarchical: delegation at node and account level creates principals with full sovereignty over their domain, while allocation at document and version level exercises mechanical subdivision rights within the parent principal's domain without establishing independent ownership standing.

The delegation is irrevocable:

**O8 (IrrevocableDelegation).** Once principal `π` delegates sub-prefix `p'` to `π'`, the delegation cannot be reversed by any system operation:

  `(A π, π', a : delegated(π, π') ∧ a ∈ dom(π') : ω(a) = π'  in all subsequent states)`

This is a consequence of O3: once `π'` holds the longest matching prefix for `a ∈ dom(π')`, only a delegation of a still-longer prefix could supersede it. At account level, O1a ensures no such longer principal can exist. Nelson: "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). There is no revocation command, no forced reclamation. Gregory confirms: `validaccount` is a stub that unconditionally returns TRUE — the system has no machinery for checking or revoking delegation. Once the sub-prefix exists, the delegate owns it permanently.

The combination of O3 (OwnershipRefinement), O8 (IrrevocableDelegation), and T8 (AllocationPermanence) means the ownership structure of the address space is *monotonically growing*. New ownership domains are created through delegation but never destroyed. The tree of ownership deepens but never prunes.


## Node-Locality

Ownership authority does not propagate across node boundaries. A principal's effective ownership is bounded by its node prefix.

**O9 (NodeLocalOwnership).** For a principal `π` whose prefix begins with node field `N`, the ownership predicate `owns(π, a)` can hold only for addresses `a` whose node field equals `N`:

  `(A π ∈ Π, a ∈ T : owns(π, a)  ⟹  nodeField(a) = nodeField(pfx(π)))`

This follows directly from O1 and the prefix relation: if `pfx(π) ≼ a`, then the leading components of `a` match those of `pfx(π)`, including the entire node field. An address on node `1.2` cannot have `1.1.0.U` as a prefix. The node digits are not special in the comparison — they are simply the leading components of the prefix, and like all prefix components, they must match exactly.

The consequence is that the same human being would hold *separate, independent* ownership roots on each node — distinct principals with distinct prefixes, distinct domains, and no structural relationship between them. Nelson's "docuverse" is a forest of independently owned trees rooted at nodes, not a single tree with a universal authority. The node operator delegates accounts within its node; those accounts have no automatic standing on any other node.

Gregory's implementation has no cross-node communication, no remote ownership lookup, and no federation of identity. The account tumbler is per-session, per-node. But the abstract property does not depend on these implementation choices — it follows from the prefix geometry of T4 and the structural ownership predicate of O1.


## The Fork as Ownership Boundary

When a principal seeks to modify content it does not own, the system's response is not an error but a creative act. This is the architectural expression of the ownership boundary.

**O10 (DenialAsFork).** When principal `π` requires modification of content at address `a` but `ω(a) ≠ π`, the system provides an alternative: `π` may create a new address `a'` within `dom(π)` that structurally relates to `a`:

  (a) `ω(a') = π` — the new address is fully owned by the requesting principal

  (b) when `zeros(pfx(π)) = 1`: `acct(a') = pfx(π)` — the address structure records `a'` as belonging to `π`'s account domain

  (c) the original address `a` is unchanged — no ownership is transferred, no content is modified

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
| O5 | Only `ω(p)` may allocate new addresses extending `p` — subdivision authority | introduced |
| O6 | `zeros(pfx(ω(a))) = 1 ⟹ acct(a) = pfx(ω(a))` — structural provenance for account-level principals | introduced |
| O7 | Ownership delegation (at node/account level) confers the same rights bundle recursively | introduced |
| O8 | Delegation is irrevocable — no operation reverses a sub-prefix assignment | introduced |
| O9 | Ownership authority is bounded by node prefix — no cross-node ownership | introduced |
| O10 | Non-ownership of target yields a fork: new address under the requesting principal's domain | introduced |
| O11 | Principal identity is axiomatic to the ownership model — authentication is external | introduced |
| `ω(a)` | `effectiveOwner : ValidAddress → Principal` — the effective owner function | introduced |
| `dom(π)` | `{a ∈ T : pfx(π) ≼ a}` — the ownership domain of a principal | introduced |
| `acct(a)` | When `zeros(a) = 0`: `acct(a) = a`; when `zeros(a) ≥ 1`: truncation through user field | introduced |
| `pfx(π)` | `ownershipPrefix : Principal → Tumbler` — injective, `zeros(pfx(π)) ≤ 1` | introduced |


## Open Questions

- Must the system provide a mechanism for ownership transfer, and if so, what invariants must it preserve given that structural provenance (O6) is inalienable?
- Must the system enforce that no principal can claim an ownership prefix that overlaps an existing principal's domain, and what are the invariants of this enforcement?
- What formal guarantees must the system provide about content accessibility when the effective owner ceases to exist as a principal?
- Must ownership domains be dense (every address in the domain is reachable) or can gaps exist between baptized siblings within a domain?
- What invariants must a cross-node identity federation satisfy to remain consistent with O9, if such federation is introduced?
- What formal relationship must hold between the provenance recorded in an address (O6) and the effective owner (O2) if ownership transfer is permitted?
- Must delegation events be recorded, or is the structural evidence of the address hierarchy sufficient to reconstruct the delegation history?
