# Review of ASN-0043

## REVISE

### Issue 1: L3's formal statement admits empty type endsets despite prose claim of "tightening"

**ASN-0043, L3 (NEndsetStructure)**: "Per Nelson, every link carries a type endset; the conforming link store admits only N ≥ 3, and we tighten L3 accordingly below." Formal statement: `(A a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ ∈ Endset))`.

**Problem**: The "tightening" applies only to arity (N ≥ 3). Since `Endset = 𝒫_fin(Span)` admits ∅, an arity-3 link `(F, G, ∅)` with empty type endset formally satisfies L3 — yet the prose treats Gregory's empty-type-specset short-circuit as "outside this ASN's conforming link store." The mismatch propagates to L8: two empty-type links trivially have `coverage(.e₃) = ∅` on both sides, satisfying `same_type` — a degenerate equivalence class the prose does not anticipate.

**Required**: Either strengthen L3 (e.g., `coverage(Σ.L(a).e₃) ≠ ∅`) to match the prose, or revise the prose to acknowledge that empty type endsets are admissible and address the L8 consequence.

### Issue 2: L9 proof's conformance check awkwardly verifies model-level theorems as state invariants

**ASN-0043, L9 proof (conformance bullets)**: "L9, L11b. Both are model-level meta-lemmas — universal-existential statements over conforming states, not state-local invariants. Their preservation in `Σ'` follows by the same construction applied recursively..."

**Problem**: L9 and L11b are theorems quantified over conforming states. They don't need per-state verification — once proven once (as this very proof does), they apply to every conforming state automatically. The "recursive application" framing is structurally confused: it has L9 verify L9 at Σ' by applying L9. The framing is also internally inconsistent — L11b's proof correctly omits L9 from its conformance check while L9's proof includes L11b. The phrase "all L- and S-invariants" obscures the distinction between state-local invariants requiring verification (L0, L1, L1a–c, L3, L5, L6, L11a, L12, L14, L14a, L-fin) and items that follow once those are established (L2, L4, L7, L8, L9, L10, L11b, L12a, L12b, L13).

**Required**: Partition the conformance check into state-local invariants (verified) and theorems/lemmas/meta-claims (automatic). Drop L9 and L11b from L9's proof's verification list.

### Issue 3: L0's content-side universal silently strengthens ASN-0036

**ASN-0043, L0 (SubspacePartition)**: "every content address has subspace identifier `s_C`: `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`."

**Problem**: ASN-0036's S7c defines `subspace_I(a) = E(a)₁` but does not fix the value to any global constant — none of S0–S3, S7a–d, S8-fin, S8a–depth, D-CTG, D-MIN, D-SEQ pins it. L0's content-side universal — that every content address shares a single `s_C` — is a strengthening of the foundation, not a consequence. The ASN presents L0 as a symmetric partition without flagging that the content-side direction is new content. A reader trying to reconcile S7c (defines `subspace_I` without fixing it) with L0 (fixes it for content) gets no explanation.

**Required**: Note explicitly that L0 strengthens ASN-0036 by fixing the content subspace identifier as a global constant, or cite an ASN-0036 invariant that establishes the content-side universal (none currently does).

### Issue 4: L11b's "smallest i" construction relies on implicit T10a / AllocatedSet structure

**ASN-0043, L11b proof (construction of a')**: "By L-fin, `dom(Σ.L)` is finite, so there exists a least `i ≥ 1` with `a⁽ⁱ⁾ ∉ dom(Σ.L)`... Each `inc(·, 0)` step is a distinct T10a allocation event under the same allocator chain that produced `a`; by GlobalUniqueness... `a' = a⁽ⁱ⁾` is distinct from every element of `dom(Σ.L)`."

**Problem**: That `a' = a⁽ⁱ⁾` corresponds to a fresh T10a allocation event requires the implicit equivalence `(a⁽ⁱ⁻¹⁾, 0) has fired ⟺ a⁽ⁱ⁾ ∈ dom(Σ.L)`. The forward direction follows from L1c + L12 (fired link allocations remain in dom(Σ.L)). The backward direction follows from AllocatedSet's `domₛ(A) = {tᵢ : 0 ≤ i ≤ nₛ(A)}` initial-segment property (siblings of the allocator present in dom(Σ.L) form an initial segment of the sibling stream). Neither is cited; without them, the "smallest i" might be below the actual frontier or correspond to a (t, 0) pair that has already fired.

**Required**: Cite L1c + L12 for the forward direction (firings ⟹ membership in dom(Σ.L)) and AllocatedSet's initial-segment structure for the backward direction, so that the "smallest i with `a⁽ⁱ⁾ ∉ dom(Σ.L)`" is provably the next frontier rather than potentially a skipped sibling or a re-firing.

VERDICT: REVISE
