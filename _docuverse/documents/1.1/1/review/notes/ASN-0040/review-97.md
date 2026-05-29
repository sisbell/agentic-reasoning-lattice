# Review of ASN-0040

The mathematics here is sound. I checked the load-bearing proofs — B7 (both equal- and unequal-length-parent sub-cases), the B1/B10/B_fin inductions, B8 Case 1's `m₂ ≥ m₁+1` step, and Bop freshness (the `a ∈ S(p,d) ⟹ (a ∈ s.B ⟹ a ∈ children)` collapse is correct) — and each holds. Case analyses are exhaustive, boundaries (m=0, d=1 vs d=2, seed-not-in-any-stream) are covered, and the concrete trace verifies postconditions against real addresses. My findings are confined to the accreted prose the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: Duplicated two-phase / "moment of baptism" framing
**ASN-0040, intro vs. "The baptismal registry"**: The intro already states "Baptism is a two-phase process: first, the system queries... second, it writes... The write — not the query — is the moment of baptism. A candidate computed but never written does not exist." The later `allocated(s)`-situating paragraph then repeats it: "allocated(s) is... the *query* phase... whereas s.B is... the candidates written into the persistent store, the *write* phase that is the moment of baptism."
**Problem**: Two paragraphs say the same thing in different words — exactly the anti-bloat duplication pattern. The *only* new content in the second paragraph is the mapping query↔`allocated(s)`, write↔`s.B` (i.e. that `s.B` is a distinct state component from the foundation's `allocated(s)`). The two-phase/"moment of baptism" restatement is noise the reader must skip past.
**Required**: Trim the second paragraph to the one substantive sentence — `s.B` (committed registry) is a new state component, distinct from `allocated(s)` (realized allocator domain) — and drop the repeated phase/"moment of baptism" prose.

### Issue 2: B4 elaboration restates the foundation Σ signature
**ASN-0040, B4 (Atomic Baptism)**: "each `baptize(p, d) ∈ Σ` is one transition edge by the foundation Σ signature: its registry update is committed on a single edge of `→`, with no intermediate observable state s_mid satisfying `s → s_mid → s'`."
**Problem**: In the foundation (NoDeallocation's Σ signature), *every* `op ∈ Σ` is a single partial-function edge — the "no intermediate observable state" clause is generic to all Σ operations, not specific to baptism, and adds nothing the signature does not already give. This is prose around a corollary explaining a property it inherits rather than asserting baptism-specific content. The baptism-relevant point (read-hwm / compute-next / commit-union collapse into one edge, so no same-namespace baptism interleaves between read and write) is the part worth stating and it is left implicit.
**Required**: Either state the baptism-specific atomicity content (the read-compute-commit triple is one indivisible edge, foreclosing interleaved same-namespace allocation), or reduce B4 to the named handle that B8/B9 cite and drop the generic Σ-signature restatement.

## OUT_OF_SCOPE

### Topic 1: Global (non-co-reachable) uniqueness
B8 is correctly weakened to *co-reachable* acts (single-path), and the distributed/cross-replica case is deferred to an open question. This is the right scoping given the axioms supplied here — no action needed; noting it only to confirm the weakening is deliberate and not a gap.

### Topic 2: Parent-prerequisite chain
Bop's "no parent-baptized prerequisite is imposed" is appropriately deferred to the ownership model (Open Questions / Scope). Correctly out of scope.

VERDICT: REVISE
