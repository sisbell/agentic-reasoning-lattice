# Review of ASN-0035

## REVISE

### Issue 1: N5 formal statement is weaker than the intended property
**ASN-0035, Sequential Children (N5)**: "`(A i : 1 ≤ i < k : (cᵢ)_{#cᵢ} + 1 = (cᵢ₊₁)_{#cᵢ₊₁})`"
**Problem**: The formal quantifier constrains only consecutive differences, not the starting value. It admits `children(p) = {[p, 5], [p, 6], [p, 7]}` — gap-free but not starting at 1. The ASN's own prose is stronger: "if `[p₁, ..., pₐ, 3]` is baptized, then `[p₁, ..., pₐ, 1]` and `[p₁, ..., pₐ, 2]` were necessarily baptized earlier." This complete initial segment property requires `(c₁)_{#c₁} = 1`, which the formal statement omits. Without it N5 is not self-contained — one cannot verify the property from a state snapshot alone without knowing that BAPTIZE starts children at 1.
**Required**: Add the initial condition. Either augment with `k ≥ 1 ⟹ (c₁)_{#c₁} = 1`, or replace the quantifier with the stronger `(A i : 1 ≤ i ≤ k : (cᵢ)_{#cᵢ} = i)`.

### Issue 2: N8 verification omits N2 from the state-dependent invariant enumeration
**ASN-0035, Always-Valid Intermediate States (N8)**: "The state-dependent invariants require preservation proofs for BAPTIZE (the sole operation that modifies Σ.nodes): N3 ... N4 ... N5 ..."
**Problem**: N2 (Single Root) quantifies over `Σ.nodes` — it is state-dependent. BAPTIZE modifies `Σ.nodes`, so N2 requires a preservation argument. That argument exists (the induction in N2's own section covers the BAPTIZE step), but N8's enumeration silently omits it. N8 claims to verify all invariants by exhaustive enumeration of two categories; the enumeration is incomplete.
**Required**: Add N2 to N8's list of state-dependent invariants preserved by BAPTIZE, with a back-reference to the inductive derivation already given in the N2 section.

### Issue 3: N15 introduces authorization concepts with no formal integration
**ASN-0035, Allocation Authority (N15)**: "Only an agent authorized by the parent node `p`'s owner can invoke BAPTIZE(p). This authority is established at the moment of baptism and is permanent."
**Problem**: Three gaps compound. (1) "Agent," "authorized," and "owner" are used but never defined — not even abstractly. (2) BAPTIZE's formal precondition is `p ∈ Σ.nodes`; no authorization predicate appears, so N15 constrains BAPTIZE in prose that BAPTIZE's specification does not enforce. (3) N15 sits in the properties table alongside formally verifiable invariants (N3, N5, etc.) but cannot be falsified as stated, because the terms it relies on have no definitions against which to check.
**Required**: Either integrate an abstract authorization predicate into BAPTIZE's precondition (e.g., `BAPTIZE(p) requires p ∈ Σ.nodes ∧ auth(caller, p)`, leaving `auth` abstract with a note that the account ontology ASN will formalize it), or remove N15 from the introduced properties and state it as a design principle to be formalized downstream. The current middle ground — asserting it as a property while leaving it unformalizable — is neither.

## OUT_OF_SCOPE

### Topic 1: Ownership model formalization
**Why out of scope**: The ASN correctly excludes "account creation and delegation (account ontology)." A formal model of who owns a node, how ownership is verified, and whether it can be transferred is new territory requiring its own ASN. N15 gestures at this territory; formalizing it is a separate effort.

### Topic 2: Node lifecycle transitions beyond baptism
**Why out of scope**: The ASN identifies three lifecycle phases (unbaptized, baptized-empty, baptized-populated) but the mechanisms for populating a node — account creation, document creation, content storage — are each future ASN topics, not gaps in this one.

VERDICT: REVISE
