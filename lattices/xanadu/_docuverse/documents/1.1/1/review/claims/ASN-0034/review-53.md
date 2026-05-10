# Contract Review — ASN-0034 (cycle 1)

*2026-04-15 19:02*

### GlobalUniqueness

- `MISSING_POSTCONDITION: Domain Disjointness — the proof explicitly proves and labels a corollary: for any two distinct allocators A₁ ≠ A₂, dom(A₁) ∩ dom(A₂) = ∅. This is a direct consequence of GlobalUniqueness (a shared address would be a repeated output from two distinct events), but it is not stated anywhere in the formal contract.`
- `MISSING_POSTCONDITION: Well-defined owning allocator — the corollary further derives that the per-event producing-allocator assignment induces a unique owning allocator per address value (the unique A satisfying a ∈ dom(A)). This is proven as a consequence of Domain Disjointness but is absent from the contract.`

### PartitionMonotonicity

- `INACCURATE`: Postcondition (3) states the cross-depth ordering for "any `b` with `b_{#p+1} = 0` and `a` with `a_{#p+1} ≥ 1`" without restricting both addresses to the partition — i.e., the required constraints `p ≼ b` and `p ≼ a` are absent. The proof establishes this only for addresses within the respective child domains, and the T1 case (i) argument depends critically on the fact that "both types extend `p`, agreeing on positions 1,...,#p" before the divergence at position `#p+1`. Without `p ≼ b` and `p ≼ a`, the claim is false: take `p = [1, 2]` (so `#p = 2`), `b = [3, 0, 0]` (has `b_{3} = 0`, does not extend `p`), and `a = [1, 2, 1]` (has `a_{3} = 1`, extends `p`). Then `b_1 = 3 > 1 = a_1`, so T1 case (i) gives `a < b`, directly contradicting the contract's stated postcondition. The contract should read: for any `b` with `p ≼ b` and `b_{#p+1} = 0`, and any `a` with `p ≼ a` and `a_{#p+1} ≥ 1`: `b < a`.

### T4

- `MISSING_POSTCONDITION: T4a (SyntacticEquivalence) — the proof establishes that the non-empty field constraint is equivalent to three syntactic conditions: (1) no two adjacent zeros, (2) tumbler does not begin with zero, (3) tumbler does not end with zero. The contract records the semantic constraint but not this verified equivalence.`
- `MISSING_POSTCONDITION: T4b (UniqueParse) — the proof establishes that fields(t) is well-defined and uniquely computable from t alone (given T3). The contract makes no mention of fields(t) or its computability.`
- `MISSING_POSTCONDITION: T4c (LevelDetermination) — the proof establishes the bijection: zeros(t) = 0 ↔ node address, zeros(t) = 1 ↔ user address, zeros(t) = 2 ↔ document address, zeros(t) = 3 ↔ element address. The contract states only zeros(t) ≤ 3, omitting the bijective level correspondence.`
- `MISSING_PRECONDITION: T4b depends on T3 (CanonicalRepresentation) — the proof explicitly states "T3 is essential for T4b: canonical representation guarantees that the component sequence of t is fixed, so the separator positions computed by scanning for zeros are uniquely determined." This dependency is not captured in the contract.`

### T4c

- `MISSING_PRECONDITION: The proof explicitly uses T4b (UniqueParse) — specifically, "By T4b (UniqueParse), every zero in t is a field separator and every separator is a zero" — but T4b is not listed as a precondition in the contract. The contract states only "t satisfies the T4 constraints" but T4b is a theorem invoked in the argument, not a direct consequence of the raw T4 axiom alone.`
- `MISSING_POSTCONDITION: The proof establishes that zeros(t) counts exactly the number of field separators, and that the number of fields present equals zeros(t) + 1. This structural fact (separators = zeros, fields = zeros + 1) is proven but absent from the contract.`
- `MISSING_POSTCONDITION: The proof establishes both injectivity and surjectivity of the mapping separately and explicitly. The contract collapses this to "is a bijection" without capturing that injectivity means distinct zero counts imply distinct levels — a stronger directional claim that consumers of the contract may need.`
- `INACCURATE: The contract states zeros(t) ∈ {0,1,2,3} as a postcondition, but this follows directly from the T4 precondition (at most three zero-valued components), making it a consequence of the preconditions, not a new result established by the proof of T4c. It should either be noted as a restatement of T4 or omitted as trivial.`

### T8

- `INACCURATE: The Frame clause lists "pure arithmetic (⊕, ⊖)" but the proof explicitly includes a third member: "TumblerAdd, TumblerSub, and inc via TA5 when used as a pure function." The contract drops inc/TA5 from the Frame's enumeration of operations that preserve the allocated set exactly.`

### TA5

- `MISSING_POSTCONDITION: t' ∈ T`. The proof explicitly establishes this as a standalone step before verifying (a)–(d): "In both cases t' is a finite sequence of natural numbers with length ≥ 1, so t' ∈ T." This is a proven result — that the construction is closed under T — and belongs in the contract. The contract lists postconditions (a)–(d) but never asserts that the output is a valid tumbler.

6 mismatches.
