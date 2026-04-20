# Contract Review — ASN-0034 (cycle 1)

*2026-04-08 09:24*

### T10a.3

- `MISSING_PRECONDITION: The proof requires that t (the tumbler passed to inc(t, k')) is one of the parent's siblings — this is needed to apply T10a.1 and conclude #t = γ. The contract states only "child spawned via inc(t, k') with k' > 0" without specifying that t must be a parent sibling.`

- `MISSING_POSTCONDITION: The proof explicitly concludes (via T3) that no child output can equal any parent sibling — tumblers of different lengths are distinct. The contract establishes the length inequality γ + k' > γ but does not state the resulting non-collision guarantee.`

- `MISSING_POSTCONDITION: The proof states "outputs at different depths never collide by length alone" as an explicit conclusion. The contract does not capture this cross-depth distinctness result, even though it follows from the length bound combined with T3.`

### T10a

`

- `MISSING_POSTCONDITION: T10a.1 (Uniform sibling length) — all siblings produced by a single allocator have the same length as its base address. This is a proven formal consequence of the axiom and should appear as a postcondition.`
- `MISSING_POSTCONDITION: T10a.2 (Non-nesting sibling prefixes) — distinct siblings from the same allocator are prefix-incomparable, satisfying the T10 precondition (same_allocator(a, b) ∧ a ≠ b → a and b are prefix-incomparable). This is a proven formal consequence and a key downstream interface guarantee.`
- `MISSING_POSTCONDITION: T10a.3 (Length separation) — child allocator outputs have strictly greater length than any parent sibling output, with additive separation across nesting levels. This is a proven formal consequence with a quantified bound.`
- `MISSING_POSTCONDITION: T10a-N (Necessity) — relaxing the k=0 restriction for siblings permits prefix nesting, violating the T10 precondition. The proof establishes this as a biconditional: the constraint is both sufficient (T10a.1–T10a.3) and necessary (T10a-N). The contract omits the necessary direction entirely.`

### T4

- `INACCURATE: The second axiom condition (A i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0 : tᵢ > 0) is a tautology in ℕ — any natural number that is nonzero is already > 0, so the condition adds no constraint. The positive-component constraint in the proof is stated per-field as (A i : 1 ≤ i ≤ α : Nᵢ > 0), (A j : 1 ≤ j ≤ β : Uⱼ > 0), etc., meaning field components are strictly positive. In ℕ this is equivalent to being nonzero, but the contract should express the constraint via fields(t) decomposition or drop the vacuous condition in favor of the structural conditions that already enforce it.`

- `MISSING_POSTCONDITION: T4b (UniqueParse) is not captured — the proof verifies that fields(t) is well-defined and computable from t alone for every valid address tumbler.`

- `MISSING_POSTCONDITION: T4c (LevelDetermination) is not captured — the proof verifies the bijection between zeros(t) ∈ {0,1,2,3} and hierarchical level: 0 → node, 1 → user, 2 → document, 3 → element, with each level producing addresses with exactly one zero count and each count corresponding to exactly one level.`

### T6

- `MISSING_POSTCONDITION: The contract states that (a)–(c) "terminate and return a boolean" and (d) "terminates and returns a boolean," but never states what the boolean represents — i.e., that each procedure returns YES if and only if the corresponding condition holds. The proof's central result is correctness (soundness and completeness), not merely termination. A contract capturing only termination is strictly weaker than what was proven.`

- `INACCURATE: The contract bundles (a)–(c) as "field-equality queries" without specifying the distinct conditions each decides. The proof establishes three separate claims: (a) returns YES iff N(a) = N(b); (b) returns YES iff N(a) = N(b) ∧ U(a) = U(b); (c) returns YES iff N(a) = N(b) ∧ U(a) = U(b) ∧ D(a) = D(b). Collapsing these into an undifferentiated "field-equality query" loses the specific content of each postcondition.`

- `MISSING_POSTCONDITION: The proof establishes a conditional behavior for absent fields — that (b) returns NO if either tumbler lacks a user field, (c) returns NO if either lacks a document field, and (d) requires both tumblers to possess document fields (else NO). The contract is silent on this case structure, leaving the postconditions incomplete for tumblers at node or user level.`

- `MISSING_POSTCONDITION: For (d), the proof establishes that the procedure returns YES iff γₐ ≤ γᵦ and D(a)ₖ = D(b)ₖ for all 1 ≤ k ≤ γₐ — i.e., D(a) is a prefix of D(b) in the sequence sense. The contract says only "the prefix query on document fields terminates and returns a boolean," omitting the correctness condition entirely.`

### TA7a

- `MISSING_POSTCONDITION: #(o ⊕ w) = #w` — The proof explicitly states this in Conjunct 1: "By TA0, o ⊕ w ∈ T, with #(o ⊕ w) = #w." This is a quantified result that distinguishes TA7a's ⊕ closure from the general TA0 statement and is load-bearing for callers reasoning about result length. The contract lists only `o ⊕ w ∈ T` and the S-membership condition, omitting the length identity entirely.

5 mismatches.
