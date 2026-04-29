# Contract Review — ASN-0034 (cycle 1)

*2026-04-08 08:53*

### T10a-N

- `INACCURATE: Precondition says "k > 0 for at least one step" but the proof's critical assumption is the opposite — the allocator uses k = 0 (i.e., produces t₁ = inc(t₀, 0) with k = 0). That is the relaxation being tested. The k > 0 step (t₂ = inc(t₁, 1)) is a consequence of the construction, not the precondition. The precondition should read: the allocator uses k = 0 for at least one sibling step (the k = 0 restriction is relaxed/absent).`

- `MISSING_PRECONDITION: The proof requires both k = 0 and k = 1 steps in sequence (inc(t₀, 0) then inc(t₁, 1)). The contract mentions only "k > 0 for at least one step" and omits the k = 0 step entirely, which is the entire point of the counterexample.`

- `INACCURATE: Postcondition says "There exist siblings t₁ ≼ t₂" — this is self-contradictory. If t₁ ≼ t₂ (t₁ is a proper prefix of t₂), they are not siblings; they are nested. The proof establishes that the two addresses intended as siblings end up in a proper-prefix relation: t₁ ≼ t₂. The postcondition should say "t₁ is a proper prefix of t₂ (the intended siblings are nested)", not label them siblings while simultaneously asserting a prefix relation.`

### T10a

`

The contract captures only the axiom (the design constraint itself) but omits all three proven consequences and the necessity result that the proof section explicitly establishes.

- `MISSING_POSTCONDITION: T10a.1 (Uniform sibling length) — all siblings produced by a single allocator have the same length as its base address`
- `MISSING_POSTCONDITION: T10a.2 (Non-nesting sibling prefixes) — distinct siblings from the same allocator are prefix-incomparable, satisfying the T10 precondition`
- `MISSING_POSTCONDITION: T10a.3 (Length separation) — child allocator outputs have strictly greater length than any parent sibling output, with additive separation across nesting levels`
- `MISSING_POSTCONDITION: T10a-N (Necessity) — relaxing the k=0 restriction for siblings permits prefix nesting, so the constraint is not merely sufficient but necessary`

### T4

- `MISSING_POSTCONDITION: T4b (UniqueParse) — the proof establishes that fields(t) is well-defined and the parse is unique; the contract captures only the axiom constraints and omits any statement that field extraction is a well-defined, computable function`
- `MISSING_POSTCONDITION: T4c (LevelDetermination) — the proof establishes a bijection between zeros(t) ∈ {0,1,2,3} and hierarchical level (node/user/document/element); this correspondence is proven as a consequence of T4 but is absent from the contract`

### T8

- `MISSING_POSTCONDITION: The proof's Case 3 (Allocation) establishes the precise form of the state change — allocated(s') = allocated(s) ∪ {a_new} — but the contract's Frame clause only covers the two cases where allocated(s') = allocated(s). The specific structure of the allocation transition (a single-element union with a fresh address) is proven and not captured anywhere in the contract.`

### TA4

`

- `STALE: The contract body contains a paragraph beginning "Gregory's analysis confirms that ⊕ and ⊖ are NOT inverses in general..." referencing absadd implementation details, operand-order asymmetry, and an incomplete sentence "The reverse direction is equally necessary:" — none of this appears in TA4's proof section and appears to be stale content from a different property or review context. It should be removed.`

### TA7a

`

- `MISSING_PRECONDITION: For ⊖, the formal statement quantifies over w > 0 — "(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ T)" — but the contract lists only o ∈ S, w ∈ T, o ≥ w for the subtraction preconditions, omitting w > 0.`

6 mismatches.
