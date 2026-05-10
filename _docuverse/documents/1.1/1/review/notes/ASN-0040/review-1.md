# Review of ASN-0040

## REVISE

### Issue 1: No closure property on Σ.B

**ASN-0040, B1 proof**: "The next baptism in this namespace queries B for the maximum element of S(p, d) — which is cₘ — and increments by one to produce c_{m+1}."

**Problem**: B1's proof assumes baptism is the sole mechanism that adds elements to Σ.B, but no property establishes this. The ASN defines B0 (monotonic growth) and B2 (deterministic next address), but never states that Σ.B grows *only* through baptism. Without a closure property, an arbitrary operation could insert c₅ into B without c₁–c₄, violating B1. The proof even acknowledges a half of this dependency — "This argument also requires that no operation *outside* this namespace inserts an element into S(p, d)" — and points to B7. But B7 only covers other *baptisms*. Non-baptismal operations are unconstrained.

**Required**: Introduce a closure property: Σ'.B \ Σ.B ⊆ {next(Σ.B, p, d) : (p, d) valid} for all transitions Σ → Σ'. This is the missing axiom that B1's inductive step, B8's across-namespace argument, and the general integrity of the registry all depend on.

### Issue 2: B4 is vacuously true

**ASN-0040, Atomicity section**: "there is no observable state B' such that B ⊂ B' ⊂ B ∪ {a} and a ∉ B' during the transition."

**Problem**: Baptism adds a single element a to B. The only sets S with B ⊆ S ⊆ B ∪ {a} are B and B ∪ {a}. No set exists strictly between them in the subset ordering. The formal statement is satisfied trivially for any single-element insertion — it imposes no constraint. The prose correctly identifies the real requirement: "within a namespace, computation and commitment are indivisible" — preventing concurrent reads of the same hwm. But the formal statement expresses a different (and vacuous) property about intermediate set states.

**Required**: Reformulate B4 to express per-namespace serialization of the read-compute-write cycle. Something like: for any two baptisms β₁, β₂ targeting namespace (p, d), the commitment of one precedes the computation of the other. The existing prose already articulates this — the formalization needs to match.

### Issue 3: B₀ initial conditions leave B1 ungrounded

**ASN-0040, B1 proof**: "The base case is vacuous: when no child has been baptized, the empty set is trivially a prefix."

**Problem**: The inductive base case handles children(B₀, p, d) = ∅ — no children of p at depth d in the initial state. But B₀ is defined as "some non-empty seed set" without constraints. If B₀ contains {c₁, c₃} for some namespace (the first and third children with the second missing), B1 is violated at genesis, and the inductive argument cannot recover it. The ASN lists this as an open question but states B1 as an unconditional invariant.

**Required**: Either constrain B₀ (e.g., B₀ satisfies B1 for all namespaces) as an explicit precondition, or weaken B1 to hold for all states *reachable from a conforming B₀*. The open question is fine for future work, but B1's status should reflect the dependency.

### Issue 4: B3 fourth case claimed "excluded by construction" without the construction

**ASN-0040, Ghost elements section**: "The fourth case is excluded by construction: content requires an address, and an address requires baptism."

**Problem**: Content storage is explicitly out of scope. The "construction" that enforces "content requires an address, and an address requires baptism" has not been specified — it belongs to the content storage ASN. Claiming exclusion by construction when the construction is deferred is a forward reference to an unwritten specification.

**Required**: State the fourth case as a *requirement* on future content operations (any operation that populates a position must have t ∈ Σ.B as a precondition), not as a property already established. The distinction matters: a requirement is a contract that downstream ASNs must satisfy; "excluded by construction" claims the work is done.

### Issue 5: B5 does not cover sibling increments

**ASN-0040, Depth and field structure section**: "zeros(inc(p, d)) = zeros(p) + (d − 1)"

**Problem**: B5 is defined for d ≥ 1 (the first child). The sibling stream uses inc(cₙ, 0), which is k = 0 in TA5 — outside B5's domain. The stream's field-level consistency (all elements have the same zeros count) depends on zeros being invariant under sibling increment. This follows from TA5(c) — length preserved, only sig(t) modified, ordinal stays positive so no zero is created — but it is not stated. The B6 validity table implicitly assumes all stream elements share c₁'s zeros count. Without the sibling case, this assumption is ungrounded.

**Required**: State explicitly that sibling increment preserves zeros: `zeros(inc(t, 0)) = zeros(t)` for any t with a positive last significant component. Then note that all S(p, d) elements inherit the zeros count established by B5 at c₁.

### Issue 6: No concrete worked example

**ASN-0040, throughout**

**Problem**: The ASN cites Nelson's "2.1, 2.2, 2.3, 2.4" and Gregory's query-and-increment pattern as evidence, but never traces a specific baptism sequence through the formal machinery. No property (B1, B5, B6, B7, B8) is checked against concrete tumblers.

**Required**: Trace at least one baptism chain — e.g., from B₀ = {[1]}, baptize a user: next(B, [1], 2) = inc([1], 2) = [1, 0, 1]; then next(B', [1], 2) = inc([1, 0, 1], 0) = [1, 0, 2]. Verify B1 (children = {c₁, c₂}, contiguous prefix of length 2), B5 (zeros([1, 0, 1]) = 1 = 0 + 1), B6 (d = 2, zeros([1]) + 1 = 1 ≤ 3), and B7 against a parallel namespace. A single grounded sequence anchors the entire formal development.

### Issue 7: wp analysis is trivial

**ASN-0040, High water mark section**: "wp(baptize(p, d), hwm = N + 1) = (hwm = N)"

**Problem**: This wp says "to advance hwm from N to N + 1, hwm must be N." This is the definition of counting. The review standard requires non-trivial wp computation. The interesting wp targets are the invariants themselves: wp(baptize(p, d), B1 holds) — what preconditions does a single baptism need to preserve contiguous prefix? This would surface the closure property (Issue 1) and the B₀ dependency (Issue 3) as formal requirements rather than implicit assumptions.

**Required**: Compute wp for at least B1 (contiguous prefix preservation) or B8 (global uniqueness). The hwm wp may remain as supplementary, but it should not be the only wp analysis.

## OUT_OF_SCOPE

### Topic 1: Distributed baptism coordination
**Why out of scope**: Cross-replica ordering and decentralized uniqueness belong to a future ASN on replication, which is explicitly excluded from scope. The ASN correctly lists this as an open question.

### Topic 2: Bulk allocation semantics
**Why out of scope**: Baptizing a contiguous range in one operation is an optimization variant. The ASN's single-element formulation is the foundation; bulk allocation extends it. Correctly identified as an open question.

### Topic 3: Sub-element semantic significance
**Why out of scope**: Whether d = 1 at element level (producing sub-elements) is meaningful in Nelson's model is a document-structure question, not a baptism-mechanism question. The structural validity (T4 preserved) is established; semantic interpretation belongs downstream.

VERDICT: REVISE
