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

We introduce the principals. Let `Π` denote the set of *principals* — the ownership subjects. Each principal `π ∈ Π` is associated with an *ownership prefix* `pfx(π) ∈ T`, a valid tumbler (satisfying T4) that serves as the root of their namespace. The ownership question "does `π` own `a`?" is answered by examining these two tumblers alone:

**O0 (StructuralOwnership).** Whether principal `π` owns address `a` is decidable from `pfx(π)` and `a` alone, without consulting any mutable system state.

The decision procedure is prefix containment:

**O1 (PrefixDetermination).** Principal `π` owns address `a` iff `pfx(π)` is a prefix of `a`:

  `owns(π, a)  ≡  pfx(π) ≼ a`

where `p ≼ a` denotes that `p` is a prefix of `a` in the sense of T5 — the components of `p` match the leading components of `a`.


## The Account-Level Boundary

Not every prefix match constitutes an ownership claim. The tumbler hierarchy has four structural levels — node, user, document, element — separated by zero-valued components (T4). Ownership operates at the *account level*: the combined node-and-user fields determine the owner. This is the crucial structural insight.

Define `acct(a)` as the truncation of tumbler `a` through its user field — the tumbler `N₁...Nα.0.U₁...Uβ`, having `zeros(acct(a)) = 1` per ASN-0034's field parsing. Two addresses with the same account prefix have the same owner; two with different account prefixes have different owners:

  `(A a, b ∈ Σ.alloc : acct(a) = acct(b)  ≡  (E π : π ∈ Π : owns(π, a) ∧ owns(π, b)))`

Why the account level and not some finer granularity? We observe a structural reason. The zero separators in the tumbler serve as boundary markers in the ownership computation. Gregory's `tumbleraccounteq` walks the mantissa of both tumblers in lockstep. For each *non-zero* component in the account tumbler, the document's component must match exactly. For each *zero* in the account tumbler, the zero counter advances and the document's component at that position is unchecked. When the counter reaches *two* — the second zero — the function returns true unconditionally. Everything in the document tumbler beyond the second zero is ignored.

This reveals the abstract property. The ownership predicate uses the zero structure of T4 to locate the boundary between "what must match" and "what is owned." The first zero separates the node field from the user field; the second zero terminates the account and begins the owned subspace. A would-be "sub-account" prefix like `N.0.U.0.D` has its third field — the document portion — fall *after* the second zero, and hence is never examined by the ownership predicate. This is not a bug; it is a structural consequence of how field boundaries and ownership boundaries coincide.

We formalize:

**O1a (AccountBoundary).** The ownership predicate operates at the account-field granularity. For any two tumblers `p` and `a`, if `acct(p) = acct(a)` then the ownership predicate yields the same result as if we tested with `acct(p)` directly:

  `(A p, a ∈ T : pfx(π) ≼ a  ≡  acct(pfx(π)) ≼ a)`

The ownership boundary terminates at the field separator following the user field — the second zero in the tumbler's field structure. Components beyond this boundary belong to the owned space and are not part of the ownership predicate.

This has a non-obvious consequence: sub-range delegation at finer than account granularity is *structurally impossible* within the ownership model. An extended prefix `N.0.U.0.D` is ownership-equivalent to the shorter prefix `N.0.U` — both claim exactly the same set of addresses. Any finer partitioning of authority must be handled by a mechanism outside the structural ownership model (and Nelson provides none). The account level is the atom of ownership; below it, there is only the binary distinction of "mine" versus "not mine."


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

We resolve nesting by specificity:

**O2 (OwnershipExclusivity).** For every allocated address `a`, there exists exactly one principal that effectively owns `a`:

  `(A a ∈ Σ.alloc : (E! π ∈ Π : ω(a) = π))`

where `ω(a)` — the *effective owner* — is the principal with the longest matching prefix:

  `ω(a) = π  ≡  pfx(π) ≼ a  ∧  (A π' ∈ Π : π' ≠ π ∧ pfx(π') ≼ a : #pfx(π) > #pfx(π'))`

Well-definedness of `ω` requires three observations: (i) at least one principal's prefix contains any allocated address (the address was baptized by someone who holds a containing prefix), (ii) any two containing prefixes are linearly ordered by the prefix relation (if `p₁ ≼ a` and `p₂ ≼ a`, either `p₁ ≼ p₂` or `p₂ ≼ p₁` — because both are prefixes of the same tumbler, and the prefix relation on a single path in the tree is total), and (iii) the longest among a linearly ordered finite set is unique. Together these give `(E! π :: ω(a) = π)`.

The exclusivity of ownership is load-bearing. If two parties owned the same address, the system could not determine who is entitled to subdivide the space beneath it (O5 below), who originated the content (O6 below), or whose delegation created the address. Every downstream property depends on O2.


## Permanence

Nelson is emphatic: ownership does not expire.

> "Once assigned a User account, the user will have full control over its subdivision forevermore." (LM 4/29)

"Forevermore" is strong language in a technical specification. Combined with T8 (AllocationPermanence) — allocated addresses are never removed — we obtain:

**O3 (OwnershipPermanence).** If `ω(a) = π` in state `Σ`, then `ω(a) = π` in all subsequent states `Σ'`:

  `(A a ∈ T, π ∈ Π, Σ, Σ' : ω_Σ(a) = π ∧ Σ →* Σ' : ω_{Σ'}(a) = π)`

The argument is clean: ownership is determined by `pfx(π)` and `a` (by O0). The address `a` is permanent (by T8). The prefix `pfx(π)` is permanent (no operation reassigns a principal's prefix — delegation creates new principals, it does not alter existing ones). Since the ownership computation takes immutable inputs, it cannot yield a different result in any future state.

This raises a tension that Nelson himself acknowledges. He mentions "someone who has bought the document rights" (LM 2/29), implying ownership can *transfer*. But the address permanently encodes the originating account (by O1a and T8), and Gregory's codebase contains no transfer mechanism whatsoever — no FEBE command, no data structure, no protocol step. We take the conservative reading: O3 holds for the system as specified. Transfer, if it exists, would require machinery that overrides the address-derived ownership — a registry external to the address structure — and Nelson leaves such machinery unspecified. The address is a birth certificate; a transfer would require a separate deed. We record this as an open question.


## Structural Provenance

The ownership prefix is embedded in the permanent address. Because the account-level prefix `acct(a)` is a structural component of `a`, and addresses are permanent (T8), the system can always determine who originally allocated any content:

**O6 (StructuralProvenance).** The account-level prefix of any allocated address permanently identifies the allocating principal:

  `(A a ∈ Σ.alloc : acct(a) identifies the allocating principal in perpetuity)`

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

Ownership is not held at a single level — it flows downward through the hierarchy. Nelson calls this "baptism," but we separate the *authorization structure* (who may delegate to whom) from the *allocation mechanism* (how new addresses are computed). The authorization structure is what concerns us.

**O7 (RecursiveDelegation).** If principal `π` creates a new sub-prefix `p'` extending `pfx(π)` and assigns it to a new principal `π'`, then `π'` acquires the same structural rights over `dom(π')` that `π` holds over `dom(π)`:

  `(A π, π' : pfx(π) ≺ pfx(π') ∧ delegated(π, π') : rights(π', dom(π')) ≅ rights(π, dom(π)))`

where `≅` denotes structural equivalence of the rights bundle: the same right to subdivide (O5), the same provenance encoding (O6), and the same ability to delegate further. The pattern repeats without bound. Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers" (LM 4/17). And: "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts" (LM 4/19).

The delegation is irrevocable:

**O8 (IrrevocableDelegation).** Once principal `π` delegates sub-prefix `p'` to `π'`, the delegation cannot be reversed by any system operation:

  `(A π, π', a : delegated(π, π') ∧ a ∈ dom(π') : ω(a) = π'  in all subsequent states)`

Nelson: "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). There is no revocation command, no forced reclamation. Gregory confirms: `validaccount` is a stub that unconditionally returns TRUE — the system has no machinery for checking or revoking delegation. Once the sub-prefix exists, the delegate owns it permanently.

The combination of O3 (OwnershipPermanence), O8 (IrrevocableDelegation), and T8 (AllocationPermanence) means the ownership structure of the address space is *monotonically growing*. New ownership domains are created through delegation but never destroyed. The tree of ownership deepens but never prunes.


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

  (b) `acct(a') = pfx(π)` — the address structure records `a'` as belonging to `π`'s domain

  (c) the original address `a` is unchanged — no ownership is transferred, no content is modified

Nelson: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links" (LM 2/45). Gregory confirms the structural mechanism: `docreatenewversion`, when invoked on a document belonging to a different account, routes the allocation through `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` — placing the fork under the requesting principal's account, not under the source document.

The forked address lives entirely within `dom(π)`. It satisfies O2 (π is its exclusive owner), O3 (that ownership is permanent), O5 (π may further subdivide it), and O6 (its provenance records π as the creator). From the ownership model's perspective, the fork is a new independent address that happens to share content identity with the original — a relationship that belongs to the content model, not the ownership model.

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
4. *Permanent* — no operation changes it (O3)
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
| O1a | Ownership operates at account-field granularity; components beyond the second field separator are not part of the ownership predicate | introduced |
| O2 | Every allocated address has exactly one effective owner `ω(a)`, determined by longest matching prefix | introduced |
| O3 | `ω(a)` is invariant once `a` is allocated — ownership is permanent | introduced |
| O5 | Only `ω(p)` may allocate new addresses extending `p` — subdivision authority | introduced |
| O6 | `acct(a)` permanently identifies the allocating principal — structural provenance | introduced |
| O7 | Delegated sub-prefixes confer the same rights bundle recursively | introduced |
| O8 | Delegation is irrevocable — no operation reverses a sub-prefix assignment | introduced |
| O9 | Ownership authority is bounded by node prefix — no cross-node ownership | introduced |
| O10 | Non-ownership of target yields a fork: new address under the requesting principal's domain | introduced |
| O11 | Principal identity is axiomatic to the ownership model — authentication is external | introduced |
| `ω(a)` | `effectiveOwner : ValidAddress → Principal` — the effective owner function | introduced |
| `dom(π)` | `{a ∈ T : pfx(π) ≼ a}` — the ownership domain of a principal | introduced |
| `acct(a)` | Truncation of `a` to its node-and-user prefix (`zeros = 1`) | introduced |
| `pfx(π)` | `ownershipPrefix : Principal → Tumbler` — the principal's namespace root | introduced |


## Open Questions

- Must the system provide a mechanism for ownership transfer, and if so, what invariants must it preserve given that structural provenance (O6) is inalienable?
- Must the system enforce that no principal can claim an ownership prefix that overlaps an existing principal's domain, and what are the invariants of this enforcement?
- What formal guarantees must the system provide about content accessibility when the effective owner ceases to exist as a principal?
- Must ownership domains be dense (every address in the domain is reachable) or can gaps exist between baptized siblings within a domain?
- What invariants must a cross-node identity federation satisfy to remain consistent with O9, if such federation is introduced?
- What formal relationship must hold between the provenance recorded in an address (O6) and the effective owner (O2) if ownership transfer is permitted?
- Must delegation events be recorded, or is the structural evidence of the address hierarchy sufficient to reconstruct the delegation history?
