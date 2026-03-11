# Review of ASN-0029

## REVISE

### Issue 1: AccountAddr undefined
**ASN-0029, D0 (EmptyCreation)**: "pre: a ∈ AccountAddr ∧ actor(op) = a"
**Problem**: `AccountAddr` is used as a type in D0's precondition but never formally defined. From context and T4, an account address is a tumbler with `zeros(a) = 1`, but this must be stated explicitly — it is a precondition on which D0's correctness depends.
**Required**: Define `AccountAddr = {a ∈ T : zeros(a) = 1}` alongside the `account(d)` definition, before D0.

### Issue 2: D0 existential scoping
**ASN-0029, D0**: "post: (E d : d ∉ Σ.D ∧ d ∈ Σ'.D ∧ account(d) = a : |Σ'.V(d)| = 0 ∧ Σ'.pub(d) = private) / frame: Σ'.D = Σ.D ∪ {d} ∧ ..."
**Problem**: The frame condition references `d`, but `d` is bound by the existential quantifier in the postcondition. As written, `d` in the frame is free — it does not refer to the same `d` established by the post. The standard formulation scopes the existential over both post and frame together.
**Required**: Restructure so the existential binds `d` across both postcondition and frame: `(E d : d ∉ Σ.D ∧ ... : [post conjuncts] ∧ [frame conjuncts])`.

### Issue 3: D0 and D12 do not establish D1
**ASN-0029, D1 (DocumentAllocation)**: "Within any account a, documents are allocated with strictly increasing addresses"
**Problem**: D1 is stated as an invariant and D0/D12 are the only operations that add documents to Σ.D, but neither operation's postcondition establishes the monotonicity D1 requires. D0's postcondition says only `(E d : d ∉ Σ.D ∧ account(d) = a : ...)` — any `d` not yet in Σ.D qualifies, including one that violates monotonicity. D12's Case 2 has the same gap. The ASN says D1 is "a specialization of T9" but never verifies that D0/D12 use the T9 allocator. The worked example assumes monotonic allocation ("A second own-account version produces `d_v' = 1.0.1.0.3.2`") but this is not established by any postcondition.
**Required**: Either (a) add to D0's postcondition: `(A d' : d' ∈ Σ.D ∧ account(d') = a : d' < d)`, and analogously for D12; or (b) add a postcondition clause stating the allocation follows T9/T10a, from which D1 follows.

### Issue 4: D13 Case 1 — descendant vs. immediate child
**ASN-0029, D13 (VersionPlacement)**: "account(d_s) = a_req ⟹ d_s ≼ d_v ∧ d_s ≠ d_v"
**Problem**: `d_s ≼ d_v ∧ d_s ≠ d_v` says only that `d_v` is *some* proper descendant of `d_s` in the tumbler hierarchy. It does not establish that `d_v` is an immediate child — `d_v` could be `d_s.1.1` (a grandchild) rather than `d_s.1`. The worked example then verifies `parent(d_v) = d_s`, which requires immediate child placement, but D13 does not guarantee this. The allocation mechanism (T10a) produces immediate children, but D13 does not invoke T10a.
**Required**: Strengthen Case 1 to `parent(d_v) = d_s` (using D14's definition of parent), or equivalently require that no document-level tumbler lies strictly between `d_s` and `d_v`: `d_s ≺ d_v ∧ ¬(E d'' : d_s ≺ d'' ≺ d_v)`.

### Issue 5: D14 — parent existence in Σ.D not derived
**ASN-0029, D14 (VersionForest)**: "parent(d) = max≼ {d' : d' ≺ d}"
**Problem**: D14 defines the version forest on the address space but does not establish that for any non-root `d ∈ Σ.D`, `parent(d) ∈ Σ.D`. This is the operational payoff of the forest — it connects D14 (structure) to D12 (version creation) and D2 (permanence). The derivation: non-root documents in Σ.D are created only by D12 Case 1; the source `d_s` is in Σ.D by precondition; if D13 is strengthened per Issue 4 so `parent(d_v) = d_s`, then `parent(d_v) ∈ Σ.D`; by D2, `d_s` persists. Without this derivation, the forest is a purely mathematical object disconnected from the system's document set.
**Required**: State and derive: `(A d : d ∈ Σ.D ∧ parent(d) defined : parent(d) ∈ Σ.D)`.

### Issue 6: D17 — no frame condition
**ASN-0029, D17 (ContentBasedDiscovery)**: "FINDDOCSCONTAINING(S) = {d ∈ Σ.D : ...}"
**Problem**: D17 specifies a return value but not a frame condition. Every operation specification in the ASN should state what it preserves. As a query, D17 should not modify state, but this is not stated. The D2 verification (document permanence) implicitly assumes D17 is a pure query, but this assumption is not grounded in D17's specification.
**Required**: Add frame: `Σ' = Σ` (no state change), or equivalently `Σ'.D = Σ.D ∧ Σ'.I = Σ.I ∧ (A d : d ∈ Σ.D : Σ'.V(d) = Σ.V(d) ∧ Σ'.pub(d) = Σ.pub(d))`.

## OUT_OF_SCOPE

### Topic 1: Associate access model
**Why out of scope**: D5(c) mentions "designated associates" who may access private documents, but the mechanism for designating associates is not formalized. The ASN explicitly acknowledges this. D12's precondition (`Σ.pub(d_s) ∈ {published, privashed} ∨ account(d_s) = a_req`) may need widening when the associate model is formalized — associates who can read a private document might also need versioning access. This is new territory for a future ASN.

### Topic 2: Privashed transition operations
**Why out of scope**: The ASN defines `private → published` and `private → privashed` transitions (D10a) but defers `privashed → private` and `privashed → published`. These are distinct operations with their own preconditions and consequences (the latter may retroactively bind the owner to D10's non-withdrawal obligation). Correctly scoped to open questions.

### Topic 3: D17 visibility filtering
**Why out of scope**: D17's quantifier ranges over all of Σ.D. Whether unpublished/private documents should be excluded from discovery results depends on the access model, which is not yet formalized. The open questions section correctly flags this.

### Topic 4: Cross-account version-source tracking
**Why out of scope**: D13 Case 2 creates a version with no structural ancestry link in the address. The relationship exists only through shared I-addresses. Whether the system should maintain an explicit version-source record (beyond content-based discovery) is a new design question, not an error in D13.

VERDICT: REVISE
