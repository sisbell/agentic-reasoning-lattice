# Review of ASN-0093

## REVISE

### Issue 1: Dangling `(a), (b), (c)` reference in the Link-withdrawal Open Question
**ASN-0093, Open Questions / Link withdrawal**: "The substrate makes no commitment among (a), (b), (c). Closing the gap... is deferred to a higher-layer ASN; the choice among the three paths is that ASN's load-bearing design decision."
**Problem**: Nothing in this note is labeled `(a)`, `(b)`, `(c)`. The preceding paragraph names three formulations in prose (value transition, arrangement-side, embedded-marker) but never enumerates them. This is a broken internal reference — the signature of prior-finding content relocated/edited without removing its labels. A precise reader cannot resolve the antecedent.
**Required**: Either introduce the `(a)/(b)/(c)` labels at the point the three formulations are named, or rewrite the second sentence to name them inline. Better: collapse the two paragraphs (see Issue 2).

### Issue 2: Duplicate deferrals across Scope and Open Questions
**ASN-0093, Scope "Deferred to higher-layer ASNs" vs. Open Questions**: Link withdrawal, arrangement mutation, document-address discipline, and higher-arity discipline are each deferred to the same downstream location in *both* sections.
**Problem**: The anti-bloat classifier flags "multiple paragraphs in different sections defer to the same downstream location." The Scope "Deferred" bullets and the Open Questions list say the same things in different words. The Link-withdrawal Open Question alone defers twice ("deferred to a future tombstoning ASN" and "deferred to a higher-layer ASN").
**Required**: Keep one deferral statement per topic. The Scope list is the natural home; trim the Open Questions to genuinely open design *questions*, not restatements of "this is deferred."

### Issue 3: Document-address discipline stated three times
**ASN-0093, K.σ section (two paragraphs) + Open Questions / Document address discipline**: "K.σ is the substrate-level document-introduction primitive; higher-layer ASNs... compose K.σ with their own additional preconditions..."; then "This substrate makes no commitment about *which* document addresses are admissible at K.σ beyond T4-validity and `zeros(d) = 2`..."; then again "*Document address discipline.* K.σ's precondition is structural-only..."
**Problem**: The same point — K.σ is structural-only, Nelson's baptism is a higher-layer tightening — is made three times. The "K.σ-plus-entity-set-tracking-plus-lineage-discipline-plus-version-allocator-activation" formulation also duplicates the Scope "Entity allocation" bullet.
**Required**: State the K.σ admissibility scope once (in the K.σ section), and remove the repetitions.

### Issue 4: ChainDiscipline lemma duplicates the preceding paragraph
**ASN-0093, "Sub-allocator chains are ASN-0040 sibling streams" vs. "Lemma (ChainDiscipline)"**: The paragraph already establishes "`A_C(d) = S(b_C(d), 1)` and `A_L(d) = S(b_L(d), 1)`, since each chain's first emission is `inc(anchor, 1)`... and successive elements advance by `inc(·, 0)`." The lemma immediately restates this verbatim in substance: "Instantiating `p = b_·(d)`, `k = 1`, the two coincide by construction."
**Problem**: Two paragraphs in the same section say the same thing. The lemma adds no step the paragraph lacked.
**Required**: Fold the named lemma into the paragraph (keep the name as a label on the existing statement), or delete the redundant prose and keep only the lemma.

### Issue 5: Defensive / scope meta-prose around forward references
**ASN-0093, multiple sites**:
- "ASN-0040's `SiblingStream` is infinite — defined for every `n ≥ 1`. This is load-bearing... A chain element exists at every index, including those past any finite truncation point, so the emission rule's pinning step always has a chain element to land on."
- "The substrate imports only ASN-0040's stream-level results, whose preconditions are `B6(b_·(d), 1)` (discharged above) and which require no allocator-tree embedding."
- "None is reproved from the increment primitives; the corollary forms consumed downstream are stated inline."
- L1c body: "the `k₁ = 2` and length-increasing clauses are preserved verbatim from the foundation form, not weakened."
**Problem**: These are defensive justifications ("not weakened," "load-bearing," "require no allocator-tree embedding") and use-site inventories that explain *why a citation is sound* rather than advancing the argument. The reader must skip past them to reach the actual claim.
**Required**: Delete. The B6-validity discharge already licenses the citations; restating that they are "imported only at stream level" and "not weakened" is noise.

### Issue 6: Essay content in discharge-matrix cells
**ASN-0093, Discharge matrix, L0 row under K.α and K.λ**: Each cell is a multi-sentence paragraph with "*First-emit branch:*" / "*Subsequent-emit branch:*" sub-arguments explaining that the precondition is "automatically satisfied... because DisjointSubAllocatorChains... since `a ∈ A_C(d)` by ChainDiscipline's closure under `inc(·, 0)`..."
**Problem**: Matrix cells are a structural slot for terse per-(invariant, transition) discharge pointers; these carry full derivations. The same is true of the L14 K.α cell. This is essay content in the wrong slot.
**Required**: Move the derivation to a short lemma or to the operation precondition prose, and leave the cell with a one-line pointer (e.g., "Discharged at new key via K.α precondition `E(a)₁ = s_C`; auto-satisfied — see L0 discharge note").

### Issue 7: Redundant structural preconditions on K.α / K.λ
**ASN-0093, K.α precondition** (and symmetric K.λ): lists `zeros(a) = 3 ∧ E(a)₁ = s_C`, `#E(a) ≥ 2`, `origin(a) = d`, *and* the chain-emission clause, while the *Parameter semantics* note states "(d, Σ) determines the conforming address uniquely."
**Problem**: Once the chain-emission clause fixes `a` on `A_C(d)`, every other structural precondition is a consequence: `zeros(a)=3` (ChainUniformZeroCount), `E(a)₁=s_C` (DisjointSubAllocatorChains), `#E(a)≥2` and `origin(a)=d` (ChainUniformLength + the `zeros=2` prefix). The discharge matrix itself admits the L0 precondition is "automatically satisfied." Listing derived facts as independent preconditions is over-specification.
**Required**: Either reduce the preconditions to the chain-emission clause plus value well-formedness, noting the structural facts as derived postconditions; or state explicitly that the structural clauses are a non-binding readability summary of the chain-emission consequence.

## OUT_OF_SCOPE

### Topic 1: Operational semantics of withdrawal/tombstoning
The choice among value-transition, arrangement-side, and embedded-marker withdrawal models is correctly deferred. (The *broken reference* in that discussion is the Issue-1 defect; the deferral itself is appropriate.)

### Topic 2: Arrangement-extension primitives (K.μ family)
The substrate fixing `M(d) = ∅` and deferring arrangement mutation is sound; arrangement-side invariants holding vacuously here is correctly noted.

META: (none — the ASN legitimately specifies abstract state, allocation operations, and their invariants; it has not drifted into implementation mechanics.)

VERDICT: REVISE
