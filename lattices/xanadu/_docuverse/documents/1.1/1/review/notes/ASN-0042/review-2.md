# Review of ASN-0042

## REVISE

### Issue 1: Account-level permanence corollary does not follow from O1a

**ASN-0042, Corollary (Account-level permanence)**: "For an account-level principal π with zeros(pfx(π)) = 1, O1a guarantees that no ownership principal has a prefix strictly extending pfx(π)"

**Problem**: O1a constrains `zeros(pfx(π)) ≤ 1` but says nothing about prefix nesting *within* a given zeros level. Two account-level principals can have nesting prefixes while both satisfying O1a. Example: `pfx(π₁) = [1, 0, 2]` (node=[1], user=[2], zeros=1) and `pfx(π₂) = [1, 0, 2, 3]` (node=[1], user=[2,3], zeros=1). Both satisfy O1a. T4 allows multi-component user fields. O7 allows delegation from π₁ to π₂ since `pfx(π₁) ≺ pfx(π₂)` and `zeros(pfx(π₂)) = 1 ≤ 1`. Under T10a, `inc([1,0,2], 1)` produces `[1,0,2,1]` with zeros=1 — a valid candidate for delegation.

Once π₂ exists, `ω(a) = π₂` for all `a ∈ dom(π₂)`, superseding π₁'s ownership. Nelson's "forevermore" breaks. The corollary is the load-bearing step for the central permanence claim and it does not hold as stated.

**Required**: Either (a) add a property that account-level prefixes cannot nest — e.g., restrict account-level principals to single-component user fields, which prevents nesting since equal components would violate O1b and unequal components don't nest — or (b) add a property that O7 delegation from account level cannot produce a prefix that extends another account-level prefix, or (c) weaken the permanence claim to hold only for principals with no strictly longer account-level prefix in Π.

### Issue 2: Effective owner function ω used outside its defined domain

**ASN-0042, O5 (SubdivisionAuthority)**: `(A a ∈ T : a newly allocated under prefix p ⟹ ω(p) = allocator)`

**Problem**: O2 defines ω only for allocated addresses: `(A a ∈ Σ.alloc : ...)`. O5 applies ω to a prefix `p` that may not be in Σ.alloc — a principal's ownership prefix is an authority root, not necessarily allocated content. The same issue affects the O4 derivation, which invokes "the allocator holds a prefix p" and implicitly applies ω to it. If principal prefixes are not in Σ.alloc, ω is undefined for them under O2's stated domain.

**Required**: Either extend O2's domain to all valid tumblers covered by O4 (any tumbler for which at least one principal's prefix is a prefix of it), or add a property that every principal's prefix is itself in Σ.alloc, or reformulate O5 to avoid ω — e.g., `(A a ∈ T : a newly allocated ⟹ (E π ∈ Π : pfx(π) ≼ a ∧ π = allocator))`.

### Issue 3: System state axioms assumed but not stated

**ASN-0042, O3 (OwnershipRefinement)**: "No operation changes an existing principal's prefix (delegation creates new principals, it does not alter existing ones)."

**Problem**: The O3 argument establishes monotonic refinement by assuming two facts that are never stated as formal properties:

(a) **Π is monotonically non-decreasing** — once a principal joins Π, it is never removed. O8 covers the delegation-specific case (irrevocable delegation), but no property prevents non-delegation operations from removing principals.

(b) **pfx is immutable** — once pfx(π) is set, no operation changes it. This is asserted inline ("No operation changes an existing principal's prefix") but not labeled or formalized.

Additionally, O4's inductive derivation requires a **bootstrap axiom**: the initial state has at least one principal whose prefix covers the initial allocation domain. The ASN refers to "the bootstrap principal (the initial node operator)" as though it is established, but no property states `Π₀ ≠ ∅` or characterizes the initial principal.

**Required**: State as explicit properties: (i) Π is monotonically non-decreasing across state transitions, (ii) pfx(π) is immutable once established, and (iii) the initial state contains at least one principal whose prefix covers all initially allocatable addresses. These are the axioms on which O3, O4, and O8 jointly depend.

### Issue 4: O7 formal statement uses undefined constructs

**ASN-0042, O7 (OwnershipDelegation)**: `rights(π', dom(π')) ≅ rights(π, dom(π))`

**Problem**: The formal statement uses `rights(·, ·)` (undefined function) and `≅` (undefined relation). Neither appears anywhere else in the ASN or the foundation. The narrative explains the intent — same O5, same O6, same delegation ability — but the formal statement adds notation that has no formal content. A reader cannot evaluate the universally quantified statement without knowing what `rights` returns or what `≅` compares.

**Required**: Either (a) replace the formal statement with a conjunction of the specific properties it asserts — e.g., "π' satisfies O5 over dom(π'), O6 holds for addresses in dom(π'), and π' may delegate sub-prefixes per O7 recursively" — or (b) formally define `rights` and `≅`. The current formulation is pseudo-formal: it looks like a specification but cannot be checked.

## OUT_OF_SCOPE

### Topic 1: Allocation–ownership interaction

The ASN does not derive consequences from the composition of O5 (subdivision authority) with T10a (allocator discipline). For example: that sibling allocations via `inc(·, 0)` remain within the allocator's domain, or that child allocations via `inc(·, k')` with `k'` adding a new zero separator cross into a new field level. These are straightforward consequences but unexplored.

**Why out of scope**: The baptism mechanism and allocation invariants are explicitly excluded from this ASN's scope. The interaction between ownership authority and allocation mechanics belongs in a baptism ASN.

### Topic 2: Principal cessation

The ASN's properties assume principals persist indefinitely (Π grows monotonically). What happens if a principal ceases to exist — does ω fall back to a shorter-prefixed principal? Does the domain become orphaned? The ASN's own open question covers this.

**Why out of scope**: The ASN correctly identifies this as new territory requiring machinery (custodial relationships, domain inheritance) not present in the current specification.

VERDICT: REVISE
