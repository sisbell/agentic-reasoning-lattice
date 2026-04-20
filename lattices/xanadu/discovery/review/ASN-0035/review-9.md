# Review of ASN-0035

## REVISE

### Issue 1: N8 verification claims "all" but enumerates 8 of 16 properties

**ASN-0035, Gradual admission**: "We verify this by enumerating the state-dependent and structural invariants separately."

**Problem**: The enumeration covers five state-dependent invariants (N2–N6) and three structural properties (N9, N10, N16). Eight properties are unaddressed: N0, N1, N7, N11, N12, N13, N14, plus N8 itself. All eight are trivially preserved — none depend on `Σ.nodes` as mutable state, so BAPTIZE cannot violate them. But the verification claims to establish that "the system state satisfies all node invariants," and "all" demands a complete accounting. Skipping trivial cases without acknowledging their existence is the same structural gap as skipping hard cases — it leaves the reader to verify completeness by subtraction.

**Required**: Add a third category to the enumeration — call it "definitional and non-state-dependent" — listing N0, N1, N7, N11, N12, N13, N14 and stating explicitly that these do not depend on mutable state and are therefore preserved by any operation on `Σ.nodes`. One sentence suffices.

### Issue 2: Precondition exactness argument — mechanism claim imprecise for the C ≠ ∅ case

**ASN-0035, Baptism (Exactness of the precondition)**: "BAPTIZE adds n with parent(n) = p by construction — TA5 extends p by one component, so the first #p components of n equal those of p."

**Problem**: In the C = ∅ case, `n = inc(p, 1)` literally extends `p` by one component — TA5(d) appends to `p` directly. In the C ≠ ∅ case, `n = inc(max(C), 0)` operates on `max(C)` (a child of `p`), not on `p`. TA5(c) modifies the last component of `max(C)` at fixed length. The result `[p₁, ..., pₐ, c+1]` does have `p` as a prefix, but the mechanism is "TA5 modifies a sibling of max(C), preserving the shared prefix with p" — not "TA5 extends p." The conclusion `parent(n) = p` is correct in both cases, but the stated mechanism conflates two distinct operations. In the exactness section — where the argument for precondition necessity must be airtight — this conflation undermines the claimed rigor.

**Required**: Split into two cases. For C = ∅: "TA5(d) extends `p` by one component, giving `parent(n) = p`." For C ≠ ∅: "TA5(c) modifies `max(C)` at its last component while preserving all prior components; since `max(C)` shares prefix `p`, the result `n` also has `parent(n) = p`."

## OUT_OF_SCOPE

### Topic 1: Genesis semantics — axiom vs. operation
**Why out of scope**: The ASN correctly lists this as an open question. Whether `[1]` is an axiom of every reachable state or the product of a distinguished genesis operation is a separate design decision. The current ASN's inductive proofs are valid either way — the base case is `Σ.nodes = {r}` regardless of how it got there.

### Topic 2: Authorization model for BAPTIZE
**Why out of scope**: The ASN defers "who may invoke BAPTIZE for a given parent" to Account Ontology, which is the right boundary. The precondition `p ∈ Σ.nodes` is the structural minimum; authorization adds a layer on top without changing the structural properties.

### Topic 3: Interaction of BAPTIZE with content allocation
**Why out of scope**: Account creation, document creation, and element allocation beneath a node involve state components (`Σ.accounts`, I-space, V-space) that this ASN explicitly excludes. The node ontology establishes the prefix anchor; the entities beneath it are future ASNs' concern.

VERDICT: REVISE
