# Review of ASN-0093

## REVISE

### Issue 1: Reinvented notation for a foundation term

**ASN-0093, Link store invariants / "Terminological note"**: "The substrate uses *structural inc-chain* as the nomenclature for what ASN-0043's L1c calls a *T10a-conforming step sequence*; the rename is purely terminological and the per-step admissibility content is identical."

**Problem**: The ASN admits, in its own prose, that it renames a foundation concept without changing its content. This is exactly the prohibited pattern: invent local notation for something a foundation already defines, then carry a note reconciling the two. The same note is duplicated for C1c ("The same terminological note applies to C1c's chain on the content side").

**Required**: Drop "structural inc-chain" and use the ASN-0043 term. Delete the reconciling note entirely.

### Issue 2: Axiom prose explains what is *not* axiom content

**ASN-0093, SubAllocatorAxiom, FirstEmission clause**: "This clause carries only the structural form of the first emission. The freshness commitment `a ∉ dom(C) ∪ dom(L)` (resp. `ℓ ∉ dom(L) ∪ dom(C)`) at the K.α (resp. K.λ) event is *not* axiom content; it is restated as the derived lemma FirstEmissionFreshness below."

**Problem**: This is rationale-about-the-axiom (scope demarcation, "not axiom content," forward pointer to where freshness lives) rather than statement of the axiom. The "independently citable as discharge premises" framing on the axiom header is the same pattern. It explains why the clause is carved this way, not what it asserts.

**Required**: State the three clauses as content. Remove the "not axiom content / restated below" demarcation prose; FirstEmissionFreshness's own statement already scopes itself.

### Issue 3: Defensive justification of L1c's form via forward references

**ASN-0093, L1c discussion**: "The substrate states L1c in its per-step inc-rule form — not as the stronger 'every intermediate `tᵢ` inhabits a T10a-tracked allocator's domain at the state of emission.' The strong form fails for the anchor traversal and the first emission, which inhabit no T10a-tracked allocator domain at the moment of allocation; SubAllocatorAxiom.FirstEmission (below) closes the bootstrap gap..."

**Problem**: A paragraph imagining and rebutting a stronger form the ASN does not adopt, deferring twice to downstream axiom clauses, followed by a defensive parenthetical ("Note that 'per-step inc-rule form' here refers only to the contrast..."). This advances no reasoning about L1c itself; it justifies a phrasing choice.

**Required**: State L1c's chain form directly. Cut the contrast-with-stronger-form paragraph and the parenthetical.

### Issue 4: Document-design rationale in the state model

**ASN-0093, "Note on `M`'s shape"**: "This is a semantic shift, not a notational one — the substrate's vocabulary for 'document allocated' runs through `dom(M)` rather than through `E_doc`." Followed by: "`M` is kept as a partial function (rather than a set `D ⊆ T`) so higher layers extend it rather than reintroduce a component."

**Problem**: Both sentences justify *why* the representation was chosen and how it relates to a higher-layer model — design rationale, not specification of the substrate's state. The substrate stands on its own terms; the comparison to `E_doc` and the higher-layer extension argument are out-of-scope motivation.

**Required**: State `M : T ⇀ (T ⇀ T)` with `dom(M)` = allocated documents. Remove the semantic-shift and "kept as partial so higher layers extend it" justifications.

### Issue 5: Use-site inventory after the per-chain disciplines

**ASN-0093, Per-chain disciplines (closing paragraph)**: "The substrate's transition-indexed proofs (ChainMembershipForOrigin, StoreT4Validity, FirstEmissionFreshness, and the discharge matrix entries) cite these per-chain disciplines freely, since each holds once-and-for-all on the sibling stream `S(b_·(d), 1)` the instant `d` is registered."

**Problem**: A downstream-consumer inventory that does not advance the disciplines' meaning. The disciplines are already established as ASN-0040 citations; listing who cites them is bookkeeping. The "Sub-allocator chains" table entry repeats this ("Consumed by every per-chain discipline below and by SubAllocatorAxiom.ChainDiscipline").

**Required**: Remove the consumer inventory. State each discipline and its source; let citing sites cite.

### Issue 6: Same downstream location deferred to from multiple sections

**ASN-0093**: FirstEmissionFreshness is invoked, with near-identical "supplied by FirstEmissionFreshness (which derives the conclusion from L0 + SC-NEQ + ...)" prose, in K.α's first-emit bullet, K.λ's first-emit bullet, the discharge matrix row, and the simultaneous-induction framing ("FirstEmissionFreshness is consumed at the K.α/K.λ first-emit precondition discharge"). Its proof location is announced from each ("see lemma proof above," "established under the same simultaneous-induction discipline").

**Problem**: The same premise-list and the same deferral are restated in four places. This is the multi-site-deferral pattern; it compounds maintenance and obscures the single derivation.

**Required**: State the freshness premise-chain once at the lemma; at each use site cite "FirstEmissionFreshness" with no repeated premise enumeration.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal / tombstoning (Open Questions)
**Why out of scope**: Explicitly deferred and listed as out of scope; the three-path discussion is forward design space, not a substrate claim. No error.

### Topic 2: Arrangement mutation, entity stratification, provenance
**Why out of scope**: The substrate correctly states arrangement-side ASN-0036 invariants hold vacuously (`M(d) = ∅`) and defers the mutation primitives. Correct factoring, not a gap.

Note on proofs checked: the Cross-document disjointness proof (both the prefix-incomparable and properly-prefixing `d₁ ≺ d₂` branches), the C1c/L1c chain exhibitions, ChainMembershipForOrigin's contiguous-prefix induction, FirstEmissionFreshness's circularity avoidance (use of L0 at Σ, not Σ'), and the worked-example computations (Steps 2–9) all check out — no correctness defects found. The simultaneous-induction discipline is sound (no step consumes a same-step conclusion).

VERDICT: REVISE
