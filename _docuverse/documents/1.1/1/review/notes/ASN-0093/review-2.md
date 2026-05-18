# Review of ASN-0093

## REVISE

### Issue 1: Cross-document disjointness lemma Case B argument lacks case analysis

**ASN-0093, Cross-document disjointness chain proof, Case B**: "By Prefix (ASN-0034), the joint conjunction forces a position divergence: some `k ≤ min(#d₁, #d₂)` with `d₁[k] ≠ d₂[k]`."

**Problem**: Prefix's definition is `p ≼ q ⟺ #p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. The joint conjunction `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` does not immediately yield a position divergence at `k ≤ min(#d₁, #d₂)` — in the asymmetric-length subcases, one of the two `⋠` clauses is satisfied by length alone without supplying any component divergence, so the position-divergence witness must be extracted from the other clause. The three length subcases (`#d₁ < #d₂`, `#d₁ = #d₂`, `#d₁ > #d₂`) each need separate treatment.

**Required**: Spell out the three subcases. In `#d₁ < #d₂`: `d₂ ⋠ d₁` is automatic from length; `d₁ ⋠ d₂` requires some `i ≤ #d₁` with `d₁[i] ≠ d₂[i]`. Symmetric for `#d₂ < #d₁`. In `#d₁ = #d₂`: both `⋠` clauses must supply a component divergence (else `T3` collapses them).

### Issue 2: L1c/C1c chain exhibition for subsequent emission depends on an undeclared inductive property

**ASN-0093, L1c chain exhibition, Subsequent-emit case**: "within-chain freshness against the rest of A_L(d)'s chain is discharged by SubAllocatorAxiom.ChainDiscipline (T10a.7's EnumerationInjectivity)"

**Problem**: T10a.7 (EnumerationInjectivity) applies *within* a chain — its precondition fixes the domain as `{tₙ : n ≥ 0}`. For the freshness argument to fire, both `ℓ` and `ℓ_prev` must lie in A_L(d). K.λ's precondition pins `ℓ ∈ A_L(d)`, but `ℓ_prev = max{ℓ' ∈ dom(L) : origin(ℓ') = d}` is just the maximum of a state-derived set; that this maximum lies in A_L(d) requires the inductive invariant `dom(L) ∩ {ℓ' : origin(ℓ') = d} ⊆ A_L(d)`. The substrate doesn't state this lemma. The same gap occurs on the content side for K.α.

**Required**: Add a derived lemma `(A reachable Σ, d ∈ dom(M) :: dom(L) ∩ {ℓ' : origin(ℓ') = d} ⊆ A_L(d))` (and the content analog), with explicit inductive proof: base case empty, inductive step using K.λ's emission discipline plus the frame conditions of K.σ and K.α. Cite this lemma when discharging within-chain freshness for K.α and K.λ subsequent emissions.

### Issue 3: Transfer of T10a.7/T10a.1/T10a.8 to non-tree-embedded chains needs explicit justification

**ASN-0093, SubAllocatorAxiom.ChainDiscipline**: "This clause does not claim that A_C(d) and A_L(d) are embedded in T10a's global allocator tree as standalone allocators with (parent, spawnPt, spawnParam) triples; it claims only that each chain's emissions satisfy the per-chain disciplines T10a guarantees for sibling streams."

**Problem**: T10a.7's stated precondition in ASN-0034 is "Allocator A conforming to T10a." If A_C(d) and A_L(d) are explicitly *not* standalone T10a allocators, T10a.7's stated precondition is unmet. The transfer goes through only because T10a.7's actual proof uses only TA5(a), T1(a), T1(c), and NAT-* axioms — no tree-specific facts. Similarly T10a.1 and T10a.8 need inspection. The substrate currently cites these lemmas without showing the precondition is satisfied by a discipline-conforming chain.

**Required**: Add a remark (or short proposition) noting that the proofs of T10a.7, T10a.1, and T10a.8 in ASN-0034 depend only on `inc(·, 0)` chain structure and T4-validity preservation, hence apply to any sequence so structured — including A_C(d) and A_L(d) as supplied by ChainDiscipline. Cite this when invoking the three lemmas for the sub-allocator chains.

### Issue 4: SubAllocatorAxiom contains derivable content

**ASN-0093, SubAllocatorAxiom**: The axiom states four clauses (Exists, Disjoint, FirstEmission, ChainDiscipline) as primitive.

**Problem**: Two pieces of content are derivable from the rest:
- *Disjoint* follows from FirstEmission (pins structural first emissions `[d.0.s_C.1]` and `[d.0.s_L.1]`) plus ChainDiscipline (each chain is the `inc(·, 0)`-extension of its first emission). Within-chain `inc(·, 0)` advances `sig(t)`, which equals `#t` for T4-valid `t` (TA5-SigValid), while `E₁` sits at a strictly lower index when `#E ≥ 2`, so `E(·)₁` is fixed across each chain at the value of the first emission. The two chains then disagree at the position holding `E₁` (values `s_C ≠ s_L` by SC-NEQ).
- *FirstEmission's freshness commitment* (`a ∉ dom(C) ∪ dom(L)` at the K.α event) follows from the first-emit predicate `{a' ∈ dom(C) : origin(a') = d} = ∅` together with L0 (every prior content address with origin `≠ d` extends a disjoint `b_C(·)` by the Cross-document lemma) and SC-NEQ (every `ℓ ∈ dom(L)` has `E₁ = s_L ≠ s_C = E([d.0.s_C.1])₁`).

**Required**: Promote Disjoint and the freshness commitment to derived lemmas, or mark them explicitly as "axiom-stated for citation convenience" with a forward derivation. Keep the axiom minimal — Exists + FirstEmission's structural form + ChainDiscipline suffice.

### Issue 5: Worked example doesn't exercise cross-document case

**ASN-0093, Worked example**: The example traces K.σ, K.α, K.λ, and a second K.α — all under a single document `d = [1, 0, 2, 0, 5]`.

**Problem**: The Cross-document disjointness lemma is the load-bearing freshness premise for K.α/K.λ subsequent emissions, but the worked example never registers a second document and so never exercises the lemma. The example also doesn't comprehensively verify all invariants at each successor state — e.g., after Step 2 it notes some invariants without explicitly checking L1c at the new key, and after Step 3 it doesn't walk through every L-invariant.

**Required**: Extend the example to register a second document (e.g., `d' = [1, 0, 2, 0, 7]`) and emit content and a link under it. Verify (a) `b_L(d) ≠ b_L(d')` via the Case A position divergence at index `#d₁ + 1 = 6`, (b) all stated invariants at the post-K.σ(d') state, and (c) cross-document freshness for the K.α(d', …) and K.λ(d', …) emissions.

### Issue 6: "Active" terminology in SubAllocatorAxiom.Exists is informal

**ASN-0093, SubAllocatorAxiom.Exists**: "For every d ∈ dom(M), the content sub-allocator chain A_C(d) ... and the link sub-allocator chain A_L(d) ... are active."

**Problem**: Unlike ASN-0034's T10a, which defines `activated(A, s) ≡ A ∈ Act(s)` against a state-tracked activation set, the substrate has no `Act`-style state component or activation predicate. "Active" is left to context. The operational reading is "K.α/K.λ may emit from the chain," but this binding is implicit.

**Required**: Either define "active" explicitly (e.g., "A_C(d) is active at Σ iff d ∈ dom(M).Σ") or replace the term — for example, restate Exists as "for every d ∈ dom(M), the chains A_C(d) and A_L(d) (as defined by FirstEmission and ChainDiscipline) are admissible emission sources for K.α and K.λ respectively, and remain so at every successor state in which d ∈ dom(M)."

## OUT_OF_SCOPE

The ASN explicitly defers arrangement mutation, entity stratification, provenance recording, coupling constraints, link withdrawal, higher-arity links, document address discipline beyond T4-validity + `zeros = 2`, concurrency, sub-allocator stratification beyond `{s_C, s_L}`, and arrangement extension primitives. These are correctly itemized in the Open Questions section and are not gaps in this ASN.

VERDICT: REVISE
