# ASN-0041: Tumbler Ownership

*2026-03-15*

We wish to understand what it means to own a tumbler position. The tumbler algebra (ASN-0034) gives us an address space — a hierarchically structured, totally ordered, permanently expanding namespace. But an address space without ownership is merely a coordinate system. We seek the layer of meaning that determines who may act upon the namespace and under what constraints.

The investigation reveals a surprising finding: ownership in Xanadu is not a relation stored in a table but a *theorem about addresses*. The address itself encodes its owner. This has deep consequences — the authorization model collapses to prefix containment, the access control model reduces to a binary distinction, and the response to "permission denied" is not an error but a creative act.

We derive each property from Nelson's design intent, corroborated by Gregory's implementation evidence. The method is: state what the system must guarantee, then discover what structural properties of ownership are necessary and sufficient.


## Ownership as a Structural Predicate

The first question: how does the system determine who owns an address?

Nelson's design gives a striking answer. Ownership is not recorded in an external registry — it is *computed from the address itself*:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." (LM 4/17)

Gregory's implementation confirms this decisively. The sole ownership predicate in udanax-green — `isthisusersdocument` — reduces entirely to `tumbleraccounteq`, a prefix comparison between the document's tumbler and the session's account tumbler. There is no ownership table, no registry, no separate data structure. The function body is a single delegating call: `return tumbleraccounteq(tp, &taskptrx->account)`.

We formalize this observation. Let `Π` denote the set of *principals* — the ownership subjects. We postulate a function `pfx : Π → T` assigning each principal an *ownership prefix*, a valid tumbler representing the root of their namespace. The system need not store "who owns what" because the answer is derivable:

**O0 (StructuralOwnership).** There exists a function `pfx : Π → T` such that whether principal `π` owns address `a` is decidable from `pfx(π)` and `a` alone, without consulting any mutable system state.

How is the decision made? Prefix containment. We say `p` is a *prefix* of `a`, written `p ≼ a`, when the components of `p` match the leading components of `a` — the same relation used in T5 and T6 of the tumbler algebra. The ownership predicate is:

**O1 (PrefixDetermination).** Principal `π` owns address `a` iff `pfx(π)` is a prefix of `a`:

  `owns(π, a)  ≡  pfx(π) ≼ a`

The prefix that determines ownership corresponds, through ASN-0034's field parsing, to the combined node and user fields. Recall from T4 that a valid address has the form `N₁...Nα.0.U₁...Uβ.0.D₁...Dγ.0.E₁...Eδ`. We define `acct(a)` as the truncation of `a` through its user field — the tumbler `N₁...Nα.0.U₁...Uβ`, having `zeros(acct(a)) = 1`. Then T6(b) gives us decidable field-level containment: whether two addresses share the same node and user fields is computable from the addresses alone. Two addresses with identical account-level prefixes have the same owner; two with different account-level prefixes have different owners:

  `(A a, b ∈ Σ.alloc : acct(a) = acct(b)  ≡  (E π : π ∈ Π : owns(π, a) ∧ owns(π, b)))`

This is a strong claim. It says ownership is not merely *consistent with* the address structure — it *is* the address structure. The tumbler is not just a name; it is a title deed.

Gregory's `tumbleraccounteq` reveals the mechanism precisely. The function walks both mantissa arrays in lockstep. For each non-zero component in the account tumbler, the document's mantissa must match exactly; a mismatch returns false. When two consecutive zeros appear in the account tumbler — the double-zero terminator that marks the end of the account's field structure — the function returns true unconditionally, regardless of what the document's mantissa holds beyond that point. This is not a plain byte-for-byte prefix match; it is an account-aware prefix match that respects the zero-delimited field structure of T4.


## Ownership Domains

The prefix-ownership model gives each principal a *domain* — the set of all addresses they own.

**Definition (Ownership Domain).** For principal `π ∈ Π`, define `dom(π) = {a ∈ T : pfx(π) ≼ a}`.

By T5 (ContiguousSubtrees), every ownership domain is a contiguous interval under the lexicographic order T1. If `a` and `c` both belong to `dom(π)`, and `a ≤ b ≤ c`, then `b ∈ dom(π)`. No address can "escape" from the middle of someone's domain. This is not a design choice — it is a mathematical consequence of prefix containment and lexicographic ordering.

Domains nest. A node operator's domain contains all account domains at that node. An account holder's domain contains all document domains under that account. The nesting respects the field structure of T4:

  `zeros(pfx(π₁)) < zeros(pfx(π₂)) ∧ pfx(π₁) ≼ pfx(π₂)  ⟹  dom(π₂) ⊆ dom(π₁)`

A principal at a higher hierarchical level (fewer zeros in their prefix) whose prefix contains another's prefix contains that principal's entire domain. Nelson articulates this recursive structure: "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on" (LM 4/19).


## The Exclusivity Invariant

We now ask: can two principals simultaneously own the same address?

Nelson uses the definite article consistently — "*the* owner of a given item" (LM 4/20), not "an owner." Gregory's predicate returns a boolean — true or false, never "also owned by another." The system requires exactly one effective owner per address.

For non-nesting prefixes, T10 (PartitionIndependence) gives us disjointness immediately: two principals whose prefixes satisfy `pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁)` have disjoint domains. The interesting case is nested domains — when a node operator's domain contains an account holder's. Here, Nelson is explicit: the node operator creates accounts, but "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). Delegation transfers effective ownership of the subdomain.

We resolve nesting by specificity. Define:

**O2 (OwnershipExclusivity).** For every allocated address `a`, there exists exactly one principal that effectively owns `a`:

  `(A a ∈ Σ.alloc : (E! π ∈ Π : ω(a) = π))`

where `ω(a)` — the *effective owner* — is the principal with the longest matching prefix:

  `ω(a) = π  ≡  pfx(π) ≼ a  ∧  (A π' ∈ Π : π' ≠ π ∧ pfx(π') ≼ a : #pfx(π) > #pfx(π'))`

The longer the prefix, the more specific the ownership claim. Well-definedness follows from three observations: (i) at least one principal's prefix contains any allocated address (the address was created by someone), (ii) any two containing prefixes are linearly ordered by the prefix relation (if `p₁ ≼ a` and `p₂ ≼ a` and both are prefixes of `a`, either `p₁ ≼ p₂` or `p₂ ≼ p₁`), and (iii) the longest such prefix is unique.

Several of Nelson's guarantees depend on O2 being inviolable. Modification rights require unambiguous authority: "Only the owner has a right to withdraw a document or change it" (LM 2/29) — if two parties owned the same position, conflicting modifications would be irreconcilable. Royalty accounting requires an unambiguous recipient: "the remainder becomes the author's profit" (LM 5/12) — dual ownership would make royalty disposition ambiguous. Origin traceability requires a unique source: "You always know where you are, and can at once ascertain the home document of any specific word or character" (LM 2/40) — this guarantee collapses under shared ownership.


## Permanence

Nelson is emphatic: ownership does not expire.

> "Once assigned a User account, the user will have full control over its subdivision forevermore." (LM 4/29)

"Forevermore" is strong language in a technical specification. Combined with T8 (AllocationPermanence) — allocated addresses are never removed from the address space — we obtain:

**O3 (OwnershipPermanence).** If `ω(a) = π` in state `Σ`, then `ω(a) = π` in all subsequent states `Σ'`:

  `(A a ∈ T, π ∈ Π, Σ, Σ' : ω_Σ(a) = π ∧ Σ →* Σ' : ω_{Σ'}(a) = π)`

The argument: ownership is determined by `pfx(π)` and `a` (by O0). The address `a` is permanent (by T8). The prefix `pfx(π)` is permanent (once a principal holds a prefix, no operation reassigns it). Therefore the ownership computation cannot yield a different result in any future state.

This raises a tension. Nelson acknowledges that ownership can be *transferred* — "someone who has bought the document rights" (LM 2/29) — but provides no mechanism. No FEBE command transfers ownership. No data structure records the transfer. Gregory's implementation has no support for it whatsoever. We take the conservative position: O3 holds for the system as specified. Transfer, if it exists, would require extra-structural machinery — a registry that overrides the address-derived ownership — and Nelson does not formalize such machinery. We record transfer as an open question.


## The Rights of Ownership

What does ownership confer? Nelson enumerates a specific bundle. We formalize each as a property that any implementation must satisfy.

**O4 (ModificationExclusivity).** Only the effective owner of a document address may modify content at that address. For any modification operation `op` targeting address `a`:

  `pre(op, a)  ⟹  ω(a) = actor(op)`

Nelson: "Only the owner has a right to withdraw a document or change it" (LM 2/29). Gregory confirms: `checkforopen` in the BERT module gates write access through `isthisusersdocument` — the prefix match must succeed before any write operation proceeds.

**O5 (SubdivisionAuthority).** Only the effective owner of a domain may allocate new addresses within it. The right to create sub-addresses is exclusive:

  `(A a ∈ T : a newly allocated under prefix p  ⟹  ω(p) = allocator)`

Nelson: "The owner of a given item controls the allocation of the numbers under it" (LM 4/20). This is the *right to baptize* — the most fundamental right of ownership. Gregory confirms: `docreatenewdocument` always uses `taskptr->account` (the session's own prefix) as the allocation hint. You cannot create addresses in someone else's domain.

**O6 (StructuralProvenance).** The address of allocated content permanently encodes the identity of the allocating principal. Because `acct(a)` — the account-level prefix — is a structural component of the address, and addresses are permanent (T8), the system can always determine who originally allocated any content:

  `(A a ∈ Σ.alloc : acct(a) identifies the allocating principal in perpetuity)`

Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" (LM 2/40). This is not a right that can be exercised or waived — it is an inalienable structural fact. If ownership were to transfer, the address would still record the original principal's identity. The new owner could modify the content, but the address would forever testify to its origin.

**O7 (RoyaltyEntitlement).** The effective owner of a published document is entitled to compensation proportional to usage. For every delivery of content at address `a` to any requestor:

  `(A a ∈ Σ.published, requestor ∈ Π : delivery(a, requestor) ⟹ ω(a) receives credit)`

Nelson: "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned" (LM 2/43). The cash register mechanism — "a system-maintained counter" (LM 5/13) — is an architectural enforcement of this right. Compensation is automatic, per-byte, and unblockable by either party.


## The Publication Contract

Rights alone do not capture ownership's full meaning. Nelson's design imposes *obligations* that transform ownership upon publication. Private documents give their owners nearly absolute sovereignty. Publication trades sovereignty for participation in a commons.

Let `Σ.published ⊆ Σ.alloc` be the set of published document addresses. The act of publication is irreversible:

**O8 (PublicationMonotonicity).** Once a document address enters `Σ.published`, it remains there in all subsequent states:

  `(A d, Σ, Σ' : d ∈ Σ.published ∧ Σ →* Σ' : d ∈ Σ'.published)`

Nelson: "It is in the common interest that a thing once published stay published, as in the world of paper" (LM 2/43). Publication is append-only, like the address space itself. This is a deliberate architectural choice — it guarantees that links and transclusions referencing published content will never dangle due to the author's voluntary withdrawal.

Three obligations flow from publication:

**O9 (AccessibilityObligation).** The effective owner of a published document must maintain its accessibility. Unilateral withdrawal is not a system operation:

  `(A d ∈ Σ.published : accessible(d) unless external_due_process(d))`

Nelson: "Its author may not withdraw it except by lengthy due process" (LM 2/43). The system provides no WITHDRAW command for published content. Withdrawal requires process external to the system — negotiation or court order. This is an obligation the system imposes on the owner, not a right it grants.

**O10 (LinkFreedom).** No principal may prevent any other principal from creating links whose endpoints reference content within a published document:

  `(A d ∈ Σ.published, π ∈ Π : π may create links targeting content at d)`

Nelson: "Each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract" (LM 2/43). Link freedom is a reciprocal obligation — what you must permit, others must permit in turn. Architecturally, links are independent objects stored at the *creator's* address, not the target's. The target owner cannot touch them because they are outside the target owner's domain: "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to" (LM 4/12).

**O11 (QuotationFreedom).** Any principal may reference (transclude) content from a published document into their own documents, with automatic royalty per O7 as the sole compensation:

  `(A d ∈ Σ.published, π ∈ Π : π may transclude content from d, subject only to O7)`

Nelson: "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document'" (LM 2/45).

Together, O8–O11 define the *publication contract*: an owner who publishes accepts binding constraints on sovereignty in exchange for participation in the interconnected docuverse. The contract is symmetric — what you must permit others to do with your work, you gain the right to do with theirs. The tradeoff is precise: you give up control over use but never give up compensation for use.


## The Ownership–Access Dichotomy

The system recognizes exactly two modes of relation to content: you own it, or you do not. There is no middle ground.

**O12 (BinaryAccess).** For any principal `π` and document address `d`, exactly one of the following holds:

  (i) `ω(d) = π` — full authority (read, modify, withdraw subject to O9, subdivide)

  (ii) `ω(d) ≠ π` — authority determined by publication status:
  - if `d ∈ Σ.published`: read and link access (per O10, O11)
  - if `d ∉ Σ.published`: no access, unless `π` is a designee (mechanism unspecified)

Nelson: "A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone" (LM 2/42). There is no concept of delegated write access, co-editing, or shared authority. The "designee" or "associate" mechanism is mentioned but never specified technically — Nelson acknowledges the gap: "Private documents. (Currently all documents are visible to all users.)" (LM 4/79).

Gregory confirms the binary model. The `checkforopen` function in the BERT module has exactly two paths: if `isthisusersdocument` returns true, write access is granted; otherwise, only read access is permitted (and only if no conflicting write lock exists). There are no ACLs, no permission matrices, no role hierarchies in the codebase.

The architectural consequence is profound. In conventional systems, "permission denied" is a terminal error. In Xanadu, it is a *creative act*:

**O13 (DenialAsFork).** When a principal `π` requires modification of document `d` but `ω(d) ≠ π`, the system provides an alternative path: `π` may create a new document `d'` within `dom(π)` that references `d` through transclusion:

  (a) `ω(d') = π` — the new document is fully owned by the requesting principal

  (b) `d` is unchanged — no content is copied; identity is preserved through reference

  (c) `acct(d') = pfx(π)` — the address structure records `d'` as belonging to `π`'s domain, not `d`'s

Nelson: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links" (LM 2/45). Gregory confirms: `docreatenewversion`, when invoked on a document belonging to a different account, places the new version under the *requestor's* account rather than under the source document: `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)`.

O13 transforms the access control problem from a permission system into a namespace partitioning problem. The only "permission" concept needed is prefix containment. Everything else — collaboration, annotation, criticism, derivation — is handled through the forking mechanism and the permanent interconnection of the address space.


## Recursive Delegation

The ownership model is self-similar at every level of the hierarchy.

Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers" (LM 4/17). And: "So the docuverse is all really one big forking document" (LM 4/18).

**O14 (RecursiveDelegation).** If principal `π` creates a new sub-prefix `p'` extending `pfx(π)` and assigns it to a new principal `π'`, then `π'` acquires the same bundle of rights over `dom(π')` that `π` holds over `dom(π)`:

  `(A π, π' : pfx(π) ≺ pfx(π') ∧ delegated(π, π') : rights(π', dom(π')) ≅ rights(π, dom(π)))`

where `≅` denotes structural equivalence of the rights bundle — the same rights (O4, O5, O6, O7) and the same obligations upon publication (O8–O11). The delegate may further subdivide `dom(π')` and delegate sub-domains with the same recursive authority. The pattern repeats without bound.

The delegation is irrevocable:

**O15 (IrrevocableDelegation).** Once principal `π` delegates sub-prefix `p'` to `π'`, the delegation cannot be reversed by any system operation. The effective owner of addresses in `dom(π')` is `π'` permanently:

  `(A π, π', a : delegated(π, π') ∧ a ∈ dom(π') : ω(a) = π'  in all subsequent states)`

Nelson: "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29). There is no revocation mechanism — no REVOKEACCOUNT in the FEBE protocol, no forced reclamation operation. Gregory confirms: `validaccount` unconditionally returns TRUE; the system has no machinery for checking or revoking delegation.

The combination of O3 (OwnershipPermanence), O15 (IrrevocableDelegation), and T8 (AllocationPermanence) means the ownership structure of the address space is *monotonically growing*. New ownership domains can be created through delegation but never destroyed. The tree of ownership deepens but never prunes.


## The Custodian Exception

One relationship in Nelson's design requires separate treatment. The storage vendor operates the physical infrastructure — stores bytes, forwards requests, maintains the system — but does not own the content within it.

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material, and not to breach the confidence of any customer, examining customers' stored materials only as required for the orderly maintenance of the system." (LM 5/14–5/15)

**O16 (CustodialAccess).** A custodian is a principal with operational access to content within a domain it does not own, subject to contractual obligations of preservation and privacy. Custodial access confers no ownership rights:

  `(A c ∈ custodians, a ∈ Σ.alloc : custodialAccess(c, a) ∧ ω(a) ≠ c  ⟹`
  `  c may not modify content at a ∧ c may not allocate under a ∧ c may not withdraw a)`

The custodian relationship is contractual — enforced by the franchise agreement between Project Xanadu and Storage Vendors — not structural. It is the sole exception to the binary access model of O12. Custody is also survivable: "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations" (LM 5/16). The owner's content and position transfer intact; infrastructure failure never becomes ownership revocation.


## Summary of the Model

The model we have derived has a severe elegance. Ownership is: (1) structural — computed from the address, not stored; (2) exclusive — exactly one effective owner per address; (3) permanent — no operation changes it; (4) absolute within its domain — full control over modification and subdivision; (5) constrained by publication — publication trades sovereignty for participation; (6) binary in access — own it fully or fork from it; (7) recursively delegable — the same pattern repeats at every level; and (8) irrevocable — delegation is permanent, like the addresses themselves.

The design philosophy is clear: minimize the authorization model to the point where the only permission concept needed is prefix containment. The system replaces the conventional permission hierarchy — users, groups, roles, ACLs — with a single structural predicate. Everything else is handled by the forking mechanism: if you cannot modify it, make your own version. Ownership is structural; permission is social.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| O0 | Ownership of an address by a principal is decidable from the principal's prefix and the address alone, without mutable state | introduced |
| O1 | `owns(π, a) ≡ pfx(π) ≼ a` — ownership is prefix containment | introduced |
| O2 | Every allocated address has exactly one effective owner `ω(a)`, determined by longest matching prefix | introduced |
| O3 | `ω(a)` does not change once `a` is allocated — ownership is permanent | introduced |
| O4 | Only `ω(a)` may modify content at `a` — modification exclusivity | introduced |
| O5 | Only `ω(p)` may allocate new addresses extending `p` — subdivision authority | introduced |
| O6 | `acct(a)` permanently identifies the allocating principal — structural provenance | introduced |
| O7 | `ω(a)` receives credit for every delivery of content at published address `a` — royalty entitlement | introduced |
| O8 | `Σ.published` is monotonically non-decreasing — publication is irreversible | introduced |
| O9 | Owner of published document must maintain its accessibility — no unilateral withdrawal | introduced |
| O10 | No principal may prevent links targeting content in a published document — link freedom | introduced |
| O11 | Any principal may transclude published content, subject only to O7 — quotation freedom | introduced |
| O12 | Access is binary: full authority (owner) or read-only/none (non-owner) — no intermediate permissions | introduced |
| O13 | Denial of modification access yields a fork — new document under the requesting principal's domain | introduced |
| O14 | Delegated sub-prefixes confer the same rights bundle recursively | introduced |
| O15 | Delegation is irrevocable — no operation reverses a sub-prefix assignment | introduced |
| O16 | Custodians have operational access without ownership rights — contractual, not structural | introduced |
| `Σ.published` | `published : set<DocAddress>` — the set of published document addresses | introduced |
| `ω(a)` | `effectiveOwner : ValidAddress → Principal` — the effective owner function | introduced |
| `dom(π)` | `{a ∈ T : pfx(π) ≼ a}` — the ownership domain of a principal | introduced |
| `acct(a)` | Truncation of `a` to its node-and-user prefix (`zeros = 1`) | introduced |


## Open Questions

- Must the system provide a mechanism for ownership transfer, and if so, what invariants must such a mechanism preserve given that structural provenance (O6) is inalienable?
- What must the system guarantee about content accessibility when storage payment lapses — does address permanence (T8) imply content accessibility, or can content become unreachable while its address persists?
- Must the system enforce that no principal can claim an ownership prefix that overlaps an existing principal's domain, and if so, at what granularity?
- What formal guarantees must the designee mechanism satisfy — must designee status be revocable, and must it be per-document or per-account?
- What must the system guarantee about custodial transitions — when content migrates between storage vendors, what invariants bind the incoming custodian?
- Can ownership obligations (O9–O11) be satisfied when the effective owner ceases to exist as a principal — must the system guarantee orphan document accessibility?
- Must the system record delegation events (who delegated what to whom), or is the structural evidence of the address hierarchy sufficient?
