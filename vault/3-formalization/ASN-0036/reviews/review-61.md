# Cone Review — ASN-0036/S5 (cycle 1)

*2026-04-14 13:39*

I've read the ASN as a system. Three cross-property findings.

### S6 is formally identical to S1
**Foundation**: N/A (internal cross-property)
**ASN**: S6 (Persistence independence) vs S1 (Store monotonicity)
**Issue**: S6's formal invariant `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C))` for every transition `Σ → Σ'` is logically equivalent to S1's `dom(Σ.C) ⊆ dom(Σ'.C)` for every transition — these are the same statement by definition of subset inclusion. The qualifier "independently of all arrangement functions `M(d)`" adds nothing because S1 already quantifies over ALL state transitions, which includes those that modify arrangements. The Frame clause ("S6 holds for all possible values of `Σ'.M(d)`, including `Σ'.M(d) = ∅`") is equally redundant — "every state transition" already covers those cases. Both properties derive from S0 by the same one-step argument. In S5's conformance definition, requiring both S1 and S6 at each transition is formally tautological. The narrative distinction (S6 names the anti-GC commitment) is real, but the formal statement captures none of it.
**What needs resolving**: If S6 is meant to express something S1 does not — the claim that content persistence is *structurally independent* of arrangement state, not merely universally quantified over transitions — the formal statement must express that additional content. Otherwise S6 should be acknowledged as a named restatement of S1 rather than presented as a separate property with its own proof, contract, and frame conditions.

---

### Content-store addresses are never formally connected to the allocation scheme
**Foundation**: GlobalUniqueness, T10a (ASN-0034)
**ASN**: S4 (Origin-based identity), S1 narrative ("S1 is the content-store specialisation of T8"), S5 constructions
**Issue**: The ASN's state model defines `Σ = (C, M)` where `C` maps I-addresses to values. ASN-0034's allocation model defines tumbler addresses produced by `inc(t, k)` within an allocator tree governed by T10a. No property in this ASN establishes the bridge: that I-addresses *are* tumbler addresses, or that entries enter `dom(Σ.C)` via allocation events as defined by GlobalUniqueness. Three properties depend on this bridge: (1) S4 invokes GlobalUniqueness, which requires its inputs to be addresses arising from allocation events — but S4's precondition `a₁, a₂ ∈ dom(Σ.C)` doesn't entail they were produced by such events. (2) S1's narrative claims it "specialises T8" from allocated addresses to content-store addresses, assuming `dom(Σ.C) ⊆ allocated(s)` — a containment that is never stated. (3) S5's constructions perform "Allocate a fresh I-address `a` and store `Σ₁.C = {a ↦ w}`" — an operation whose relationship to `inc(t, k)` or root initialization is assumed but unstated, so S5's claim that its traces occur "within a system conforming to T10a" is not formally grounded.
**What needs resolving**: The ASN needs a formal statement connecting its state model to ASN-0034's addressing scheme — either an axiom that I-addresses are tumbler addresses and that content creation is mediated by the allocation mechanism, or an explicit typing constraint that `dom(Σ.C) ⊆ T` where `T` is the tumbler space, together with a statement that every address entering `dom(C)` is the output of an allocation event.

---

### S3's precondition list conflates established properties with per-operation verification conditions
**Foundation**: N/A (S3 contract structure)
**ASN**: S3 (Referential integrity), formal contract: "Preconditions: AX-1 (initial empty state); S1 (store monotonicity); every operation adding or modifying a V-mapping `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)` in the post-state."
**Issue**: AX-1 is an axiom. S1 is a proved consequence of S0. Both are established properties of the system. The third item — "every operation adding or modifying a V-mapping ensures `a ∈ dom(Σ'.C)`" — is neither: it is a sufficient condition *derived within S3's own proof*, a verification obligation that must be discharged by each future operation specification. Listing it alongside AX-1 and S1 as a "precondition" obscures the distinction between what the ASN has established (AX-1, S1) and what it requires of not-yet-specified operations. This makes S3 a conditional invariant — it holds IF all operations satisfy the obligation — but the contract presents it with the same status as unconditional invariants like S1. The proof itself correctly identifies the obligation as "a design requirement: every operation specification … must individually discharge [it]," but the formal contract does not reflect this distinction.
**What needs resolving**: S3's formal contract should distinguish between its preconditions (properties already established: AX-1, S1) and its per-operation verification condition (a schema that future operation specifications must satisfy). This could be a separate "Verification obligation" or "Per-operation requirement" field, making explicit that S3's invariance is contingent on a condition that this ASN identifies but does not discharge.
