# ASN-0031: Account Creation

*2026-03-12*

ASN-0029 (Document Ontology) defines AccountAddr, the account prefix function `account(d)`, and uses `a ∈ AccountAddr` as a precondition for document creation (D0). But no ASN specifies how accounts enter the system. D0 requires the account to exist — something must create it.

This ASN fills that gap. The scope is deliberately narrow: what state tracks accounts, how they are created, and what invariants they satisfy. The properties are few because the tumbler address does most of the work — account prefix-freeness, for instance, is a structural consequence of the zero-field hierarchy, not an additional constraint.

---

## Account State

We introduce a single state component:

**AC-Σ (AccountSet).** Σ.A : Set(Tumbler) is the set of all allocated account addresses. Every member satisfies `zeros(a) = 1` (AccountAddr, ASN-0029). Every document has an account as a prefix:

    (A d : d ∈ Σ.D : (E a : a ∈ Σ.A : a ≼ d))

This is a well-formedness invariant on the joint state of accounts and documents. It ensures that `account(d)` (ASN-0029) always has a witness.

---

## Account Creation

Accounts are created by the node operator — the administrative authority for a node in the tumbler hierarchy. Nelson: "once assigned a User account, the user will have full control over its subdivision forevermore" [LM 4/29]. The node operator allocates the account; everything under it belongs to the account holder.

**AC0 (CreateAccount).** CREATEACCOUNT, given a node address `n` (a tumbler with `zeros(n) = 0`), produces an account `a` not previously allocated:

    pre:  zeros(n) = 0
    post ∧ frame:
      (E a : a ∉ Σ.A ∧ a ∈ Σ'.A ∧ zeros(a) = 1 ∧ n ≼ a :
           (A a' : a' ∈ Σ.A ∧ n ≼ a' : a' < a)
         ∧ Σ'.A = Σ.A ∪ {a}
         ∧ Σ'.D = Σ.D ∧ Σ'.I = Σ.I
         ∧ (A d : d ∈ Σ.D : Σ'.V(d) = Σ.V(d) ∧ Σ'.pub(d) = Σ.pub(d)))

The account address `a` has the form `N.0.U` where `n = N` is the node prefix. The allocation follows T9 (ForwardAllocation, ASN-0001): within a node, successive account addresses are strictly increasing. No documents are created — the account is an empty position, a subtree claimed. No existing state is disturbed.

**Worked example.** Node `n = 1` has existing accounts `1.0.1` and `1.0.3`. CREATEACCOUNT produces `a = 1.0.4` (the node-level allocator advances the user component past all existing user components under node 1). We verify: `1.0.1 < 1.0.4` (diverge at position 3, `1 < 4`) ✓; `1.0.3 < 1.0.4` (diverge at position 3, `3 < 4`) ✓.

---

## Account Invariants

**AC1 (AccountPermanence).** Once created, an account persists across all subsequent state transitions:

    a ∈ Σ.A  ⟹  a ∈ Σ'.A

This is necessary for `account(d)` to remain total. If the witnessing account could disappear, ownership would become partial — a document could exist with no owner. Nelson treats accounts as permanent structural positions allocated by the node operator and persisting indefinitely [LM 4/29].

**AC2 (AccountPrefixFreedom).** No account address is a prefix of another:

    (A a₁, a₂ : a₁ ∈ Σ.A ∧ a₂ ∈ Σ.A ∧ a₁ ≠ a₂ :
      ¬(a₁ ≼ a₂) ∧ ¬(a₂ ≼ a₁))

This follows from the zero-field structure: account addresses have exactly one zero separator (`zeros(a) = 1`), so extending an account address crosses a zero-field boundary into the document level. No account-level address can be a proper prefix of another account-level address. AC2 is what makes `account(d)` a function — without it, a document could have two account prefixes, and ownership would be ambiguous.

**AC3 (AccountCoverage).** Every document has an account:

    (A d : d ∈ Σ.D : account(d) ∈ Σ.A)

This is stronger than AC-Σ's existential — it says the specific account returned by `account(d)` (ASN-0029) is in Σ.A. Since D0 (EmptyCreation, ASN-0029) requires `a ∈ AccountAddr` and D12 (VersionCreation) either nests under the same account or creates under the requester's account, every document-creating operation places the new document under an existing account. AC3 is maintained inductively: it holds in the initial state (no documents, vacuously true), and each document-creating operation preserves it by construction.

---

## Interaction with ASN-0029

AC0 is the missing precondition supplier for D0. The chain is:

    CREATEACCOUNT(n) → a ∈ Σ.A     (AC0)
    a ∈ Σ.A → a ∈ AccountAddr       (AC0 postcondition: zeros(a) = 1)
    a ∈ AccountAddr → D0 precondition satisfied

Without AC0, D0's precondition `a ∈ AccountAddr` has no mechanism to become true. With it, the lifecycle is complete: the node operator creates accounts, account holders create documents.

---

## Open Questions

1. **Node creation.** This ASN assumes nodes exist (`zeros(n) = 0` in AC0's precondition). How nodes enter the system — whether there is a CREATENODE operation or whether the node set is fixed at system initialization — is not addressed.

2. **Account deletion.** AC1 makes accounts permanent. Nelson's design assumes accounts persist indefinitely, but whether a node operator should be able to decommission an account (and what happens to its documents) is an unexplored design question.

3. **Account metadata.** This ASN treats accounts as pure addresses with no associated metadata (display name, contact information, capabilities). Whether accounts carry metadata is an implementation concern outside the address-level specification.
