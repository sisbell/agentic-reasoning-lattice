Reading the dependency chain from S0 through S1 through S3, then checking how S5 discharges those invariants in its witnesses.

S1's proof is tight: S0 gives `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)`, universally instantiated over `dom(Σ.C)`, yields `dom(Σ.C) ⊆ dom(Σ'.C)` by definition. No gap.

S2's proof follows from the type declaration by definition of partial function. Correctly labeled as an axiom. No gap.

S5's witnesses discharge S0/S1 vacuously via the empty transition relation (no transitions to quantify over), and discharge S2/S3 explicitly by construction. The use of T3 to establish pairwise distinctness from distinct last components is correct in both constructions. The satisfiability proof is sound.

S3 is the problem.

### S3 (ReferentialIntegrity) — invariant asserted, not established

**Class**: REVISE
**Foundation**: S0 (ContentImmutability), S1 (StoreMonotonicity)
**ASN**: S3 body — "Any transition that establishes a V-mapping `M(d)(v) = a` must therefore have `a ∈ dom(Σ'.C)` in the post-state. S1 (store monotonicity) then guarantees that once `a` enters `dom(C)` it remains, so a valid reference cannot become dangling through any subsequent state transition."
**Issue**: The phrase "must therefore have `a ∈ dom(Σ'.C)`" is not a consequence of S0 or S1 — it is the claim under proof. S0 says existing C-entries persist; S1 derives domain monotonicity from S0. Together they establish: if `a ∈ dom(Σ.C)` at time of mapping, `a` remains in `dom(Σ'.C)` thereafter. They say nothing about whether a transition is permitted to add `M'(d)(v) = a` where `a ∉ dom(Σ'.C)`. A transition that inserts a V-mapping to a fresh I-address not yet stored in C would violate S3, and neither S0 nor S1 rules it out. The full inductive proof requires: (a) the initial state satisfies S3 (vacuously, if M starts empty), and (b) every transition that extends M only maps to addresses already in `dom(C)` at the time of extension — a protocol-level constraint nowhere stated as an axiom or derived from S0/S1. S3 has no proof block and no axiom designation; the formal contract section is absent entirely, unlike S1, S2, and S5 which each carry one. The depends list misdescribes S0 as supplying the "unreferenced content persists" property, which is a consequence of S0 alone and is not part of S3's own invariant.
**What needs resolving**: S3 must be either (a) declared an axiom (a protocol design constraint: every transition that adds a V-mapping `M'(d)(v) = a` must have `a ∈ dom(Σ'.C)`) with a formal contract block carrying that designation, or (b) proved via an inductive argument whose inductive step cites an axiom ruling out the problematic transition type. The current informal argument — citing S1 for preservation of existing valid references — establishes at most one half of the inductive step and provides no base case argument. The formal contract block (invariant, preconditions, depends with correct provenance) must be added to match the presentation of S1, S2, and S5.

---

### S0 (ContentImmutability) — no formal contract or axiom designation

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S0 — the claim is stated but carries no formal contract block and no explicit axiom label; contrast with S2, whose formal contract begins "Axiom: Σ.M(d) is declared with the partial-function type T ⇀ T."
**Issue**: S0 is the root assumption from which S1 is proved and on which S3 and S5 depend. S1's formal contract calls S0 a "precondition," implying it is accepted without proof within this ASN. But S0 carries no "Axiom:" designation, no formal contract wrapper, and no depends. Its axiomatic status is inferable from prose context ("This is the central invariant of the two-stream architecture") and from the absence of a proof, but is not declared. A reader relying on the document's formal structure — not its prose — cannot distinguish S0 from an unproved derived claim. S2 is the reference case for how an axiom is formally presented here.
**What needs resolving**: Add a formal contract block to S0 with an explicit axiom designation, paralleling S2's structure. No change to the statement is required.

VERDICT: REVISE