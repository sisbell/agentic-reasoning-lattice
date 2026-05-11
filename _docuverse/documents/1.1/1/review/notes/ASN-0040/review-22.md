# Review of ASN-0040

## REVISE

### Issue 1: Invariant proofs do not explicitly handle Σ.B-frame transitions

**ASN-0040, B1 proof, inductive step**: "Consider a transition Σ → Σ' producing registry B'. By B0a (Baptismal Closure), the only mechanism that adds elements to B is baptism: B' = B ∪ {a} where a = next(B, p₀, d₀) for some (p₀, d₀) satisfying B6."

**Problem**: B0a partitions Op into two classes — baptismal operations *and* Σ.B-frame operations. For Σ.B-frame transitions, Σ'.B = Σ.B (no element added), so the proof's framing "B' = B ∪ {a}" does not apply. The proof implicitly collapses both cases into the baptismal case. The same gap appears in B10's inductive step ("By B0a (Baptismal Closure), the only mechanism that adds elements to B is baptism: B' = B ∪ {a}...").

**Required**: Each inductive step should explicitly partition transitions per B0a's structural assertion: (i) Σ.B-frame transition, B' = B, the invariant carries trivially since children(B', p, d) = children(B, p, d); (ii) baptismal transition, the existing case analysis applies. The argument is short in case (i), but its absence leaves the proof technically incomplete.

### Issue 2: Finiteness of Σ.B is not stated as a preserved invariant

**ASN-0040, next definition and Bop proof**: next's Formal Contract requires "B ⊆ T finite"; Bop's correctness invokes max(children(Σ.B, p, d)), which requires children — and hence Σ.B — to be finite.

**Problem**: B₀ conf. requires the seed to be finite, and B0a ensures each transition adds at most one element to Σ.B, so finite-Σ.B is preserved by induction. But this invariant is not stated. The Properties Introduced table lists no finiteness invariant. Without an explicit claim "Σ.B is finite in every reachable state", the precondition "B ⊆ T finite" on next is silently assumed at every call site (B2 proof, Bop proof, B7 proof, B8 proof, B9 proof) without discharge.

**Required**: Add an invariant — call it B_fin — stating `(A Σ : Σ reachable from Σ_init : Σ.B is finite)`. Prove by induction from B₀ conf. (finite base) using B0a (at most one new element per transition). Cite it where finiteness is consumed (next's preconditions, max(children) existence).

### Issue 3: Genesis inclusion is claimed "by stipulation of B₀ conf." but is not actually stipulated

**ASN-0040, Relationship to ASN-0034's allocated set**: "The bridge also covers genesis: `allocated(Σ_init) ⊆ Σ_init.B`, since every address inhabiting an activated allocator's initial domain is presumed to inhabit B₀ by stipulation of B₀ conf."

**Problem**: B₀ conf. (SeedConformance) stipulates three conditions: B₀ is finite; children(B₀, p, d) is a contiguous prefix; every t ∈ B₀ satisfies T4. None of these stipulates `allocated(Σ_init) ⊆ B₀`. The genesis inclusion is a separate cross-ASN obligation, not a corollary of B₀ conf. as written.

**Required**: Either (a) extend B₀ conf. to include "`allocated(Σ_init) ⊆ B₀`" as an additional clause, with the understanding that this clause is what the future content-storage/allocator-activation ASN must arrange at genesis; or (b) rephrase the bridge paragraph to acknowledge this as an additional cross-ASN axiom alongside the allocator-extension-is-baptismal bridge, rather than attributing it to B₀ conf.

### Issue 4: Bop's listed preconditions do not match the operation description

**ASN-0040, Bop description**: "PRE: B6(p, d) — depth validity (defined below); [parent prerequisite deferred to Open Questions]"

**ASN-0040, Bop Formal Contract**: "Preconditions: p ∈ T, d ∈ ℕ with d ≥ 1; B6(p, d) holds; Σ.B satisfies B1 and B10."

**Problem**: The text states a single substantive precondition (B6); the Formal Contract adds two state invariants (B1, B10). The relationship is not clarified. Reading the text alone, a caller would conclude only B6 is required; reading the contract, B1 and B10 appear as caller obligations. In fact, B1 and B10 are state invariants preserved by induction, not per-call obligations — but the document does not say so.

**Required**: Either drop B1 and B10 from the Formal Contract's Preconditions list (with a note that they are state invariants discharged by the inductive proofs in §B1 and §B10), or add them to the operation description text with the same clarifying note. Pick one style and apply it consistently.

### Issue 5: B6 necessity sub-case (b) at d = 2 conflated with sub-case (a)

**ASN-0040, B6 necessity proof, sub-case (b)**: "When d = 2, the trailing zero of p at position #p and the d − 1 = 1 intermediate zero from TA5(d) at position #p + 1 create adjacent zeros, so all stream elements violate T4 — this falls under the previous sub-case."

**Problem**: Sub-case (a) handled T4 defects in positions 1 through #p − 1 of p, propagated to stream elements via TA5(b). The d = 2 trailing-zero case is structurally different: p has no interior defect; the adjacent zeros arise at positions #p, #p + 1 of c₁, where the position-#p zero is from p's trailing position (preserved by TA5(b)) and the position-#p + 1 zero is the separator introduced by TA5(d). The violation is in the stream, not propagated from p's interior. "Falls under the previous sub-case" elides this distinction.

**Required**: Spell out the d = 2 propagation argument directly: c₁ has zeros at positions #p (from p_{#p} = 0 via TA5(b)) and #p + 1 (the separator from TA5(d) with d − 1 = 1), which are adjacent — violating T4(ii) at i = #p. By TA5(c) each subsequent sibling modifies only position sig(cₙ) > #p + 1, leaving these adjacent zeros undisturbed; by induction every cₙ has them.

## OUT_OF_SCOPE

None — the Scope section explicitly lists deferred topics (ownership, parent prerequisite, content, links, etc.) and the ASN respects those boundaries. The Open Questions list correctly identifies parent prerequisite, seed sets, distributed coordination, bulk allocation, and subspace partitioning as future work.

VERDICT: REVISE
