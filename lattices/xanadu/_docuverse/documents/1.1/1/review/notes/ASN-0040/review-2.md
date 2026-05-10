# Review of ASN-0040

## REVISE

### Issue 1: WP analysis conflates sequential and concurrent reasoning, omits B4

**ASN-0040, Deterministic Allocation (wp section)**: "The second condition also requires that no non-baptismal mechanism inserted or removed elements from the namespace between read and commit — which is B0a."

**Problem**: The phrase "between read and commit" is a concurrent-execution concern — it invokes the possibility of interleaving modifications during the baptism's read-to-commit window. B0a prevents *non-baptismal* additions, but the actual "between read and commit" threat for same-namespace operations is a *concurrent baptism* — precisely what B4 (Namespace Serialization) prevents. The ASN's own B4 section demonstrates this failure mode explicitly: "If two baptisms both read hwm = m before either commits, both compute c_{m+1} and both attempt to commit the same address — violating B8." Yet B4 appears nowhere in either wp derivation.

The wp for B1 states `wp = B1 ∧ B0a`. The wp for B8 states `wp = B1 ∧ B7`. Both are correct under a sequential execution model — but the prose introduces temporal reasoning that belongs to a concurrent model, then attributes the serialization concern to B0a (wrong property) and omits B4 (right property).

**Required**: Either (a) drop the temporal phrase "between read and commit" and note that the wp assumes sequential execution, which B4 ensures at the system level, or (b) extend the concurrent analysis to include B4 as a dependency in both wp derivations. The current text attributes B4's role to B0a, which misleads about which property is load-bearing for serializability.

### Issue 2: B7 Case 3 has no concrete verification

**ASN-0040, Namespace Disjointness (Case 3)**: "position #p + 1... For S(p, 2): this position holds the zero separator from inc(p, 2), value 0. For S(p', 1): this position holds p'_{#p+1}... By T4, valid addresses do not end in zero, so p'_{#p+1} > 0."

**Problem**: The traced example (Steps 1–3) exercises only Case 1 of B7 (different stream lengths: "S([1], 2) elements have length 3; S([1, 0, 1], 2) elements have length 5"). Case 3 — nesting prefixes with equal element lengths, distinguished by zero-vs-nonzero at a single position — is the most subtle case and the one most likely to harbor an error. It should be grounded concretely.

**Required**: Add a traced verification of Case 3. A natural instance arises from the existing example: node [1] baptizes at d = 2 (S([1], 2), elements of length 3: [1, 0, 1], [1, 0, 2], ...) and node [1, 1] baptizes at d = 1 (S([1, 1], 1), elements of length 3: [1, 1, 1], [1, 1, 2], ...). Here [1] ≼ [1, 1] and both streams have element length 3. At position 2: S([1], 2) always has 0 (the zero separator); S([1, 1], 1) always has 1 (= p'₂ > 0 by T4). Trace through inc to verify both values explicitly.

### Issue 3: S0 cites TA-strict; should cite TA5(a)

**ASN-0040, Sibling Stream section**: "The stream is strictly increasing: (S0)... This follows from repeated application of TA-strict."

**Problem**: TA-strict is `(A a ∈ T, w > 0 : a ⊕ w > a)` — a property of the tumbler addition operator ⊕. S0 follows from repeated application of inc(cₙ, 0), whose strict increase is established by TA5(a): `t' > t`. The connection between inc and ⊕ is not established in ASN-0034 or this ASN — TA5 defines inc as an operation with specified properties, not as sugar for ⊕. For stream elements (where sig(t) = #t), the two operations coincide, but this equivalence requires showing that inc(cₙ, 0) = cₙ ⊕ w for w = [0, ..., 0, 1] with action point at sig(cₙ), which involves verifying the TumblerAdd precondition and the tail-replacement behavior.

**Required**: Either cite TA5(a) directly (which gives `t' > t` for inc without any detour through ⊕), or explicitly establish the inc-to-⊕ correspondence for stream elements before invoking TA-strict.

## OUT_OF_SCOPE

### Topic 1: Baptism-content coupling
B3 defines four cases (baptized ± occupied) and notes that the fourth (unbaptized + occupied) is forbidden, but defers the enforcement mechanism to downstream content-operation specifications. The interaction between Σ.B and content storage is a natural next ASN.
**Why out of scope**: Content storage is explicitly excluded; B3 correctly records the requirement without specifying the mechanism.

### Topic 2: Distributed baptism coordination
B4 ensures same-namespace serialization but the ASN does not address how replicated systems maintain B4 and B8 without centralized coordination — acknowledged in the open questions.
**Why out of scope**: Replication protocol is explicitly excluded in the scope statement.

VERDICT: REVISE
