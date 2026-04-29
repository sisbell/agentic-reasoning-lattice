# Review of ASN-0085

## REVISE

### Issue 1: OrdAddHom precondition includes S8a, which the proof does not use

**ASN-0085, OrdAddHom**: "For a V-position `v` satisfying S8a with `#v = m ≥ 2`..."

**Problem**: The component-wise proof of `ord(v ⊕ w) = ord(v) ⊕ w_ord` uses only TumblerAdd mechanics — it examines three regions (`i < k`, `i = k`, `i > k`), computes both sides, and compares. At no point does the proof reference `zeros(v) = 0`, `v₁ ≥ 1`, or any other S8a condition. The identity and all three postconditions (a, b, c) hold for any `v ∈ T` with `#v ≥ 2`:

- **(a)** The component-wise equality is a TumblerAdd identity — the "copy prefix, add at action point, copy tail" decomposition commutes with stripping the first component whenever `k ≥ 2` (guaranteed by `w₁ = 0`, not by S8a).
- **(b)** `subspace(v ⊕ w) = subspace(v)` follows from `k ≥ 2` and TumblerAdd's copy rule at position 1. No S8a.
- **(c)** The reconstruction `v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord)` requires only `#(v ⊕ w) ≥ 2` (guaranteed by `#w = m ≥ 2` via TA0) for the vpos inverse. No S8a.

S8a is needed only by OrdAddS8a (which characterizes when the *result* satisfies S8a) and by the conditional postcondition of `ord` (which guarantees `ord(v) ∈ S`). Bundling S8a into OrdAddHom's precondition conflates the structural identity with the domain-specific guarantee, and forces every downstream use of the identity to establish S8a even when only the commutation property is needed — e.g., the subtraction homomorphism noted in the open questions, where the operand may not satisfy S8a.

**Required**: Either (a) weaken OrdAddHom's precondition to `v ∈ T, #v ≥ 2` (moving S8a to OrdAddS8a, which already carries it as its natural precondition), or (b) add a note that S8a is included for domain alignment and is not logically required by the identity — but option (a) is cleaner.

## OUT_OF_SCOPE

### Topic 1: Subtraction homomorphism and round-trip properties
**Why out of scope**: The ASN correctly identifies these as open questions. TA7a's conditional S-membership results for subtraction and TumblerSub's zero-padding semantics make the subtraction case substantially more complex than addition — new territory, not an omission in this ASN.

### Topic 2: Generalization to `#w ≠ m`
**Why out of scope**: The component-wise proof works for any `#w ≥ 2` with `actionPoint(w) ≤ #v`, but the V-position domain always uses matching-length displacements (S8-depth ensures common depth within a subspace). The `#w = m` restriction is defensible as a domain-semantic choice even if not strictly required by the proof.

VERDICT: REVISE
