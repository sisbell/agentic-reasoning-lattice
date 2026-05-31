# Review of ASN-0086

This note is mathematically sound where I checked it — R0a's two-direction zero-count argument, R0a-Cor2's `#E = 2` derivation, R3/R6a/R6c, and the R7a replay (including the `a* = [d.0.s_L.1.1]` counterexample showing catalog (a) is insufficient) all hold up, and the worked-sketch tumbler arithmetic checks out. The findings below are mostly the forward-reference accretion the `review-mode.anti-bloat` classifier asks for, plus one redundant-derivation issue.

## REVISE

### Issue 1: Allocator-depth apparatus re-derives ASN-0093 structure for a worked-sketch aside
**ASN-0086, "Allocator Structure" / "Definition — zero-count depth" / "Definition — allocator-tree depth" / "Lemma — SharedDepthOneAllocator"**: "Under each document address `d ∈ dom(Σ.M)`, T10a admits at most one allocator at allocator-tree depth 1 below `d` ... `A_C(d) = A_{d.0.s_C.1}` ... and `A_L(d) = A_{d.0.s_L.1}` ... sit at allocator-tree depth 2".

**Problem**: The two depth definitions and SharedDepthOneAllocator re-derive allocator-tree facts that ASN-0093 (FirstEmission, ChainDiscipline, anchor construction `b_C(d) = inc(d, 2)`, `b_L(d) = inc(b_C(d), 0)`) already supplies. Neither "allocator-tree depth" nor "zero-count depth" nor the `A_{d.0.1}`/`A_x` naming is consumed by any R-claim — the only downstream use is the worked sketch's "Structural witness from ASN-0093" block, which itself states these facts are "witnessed by ChainDiscipline + FirstEmission, ASN-0093 — not operationally executed by K.λ." The apparatus is foundation re-derivation in service of a pedagogical aside.

**Required**: Drop SharedDepthOneAllocator and the two depth definitions; cite ASN-0093's FirstEmission/anchor construction directly at the worked-sketch structural witness. If the allocator-tree-vs-zero-count distinction is genuinely load-bearing somewhere, name the consuming claim.

### Issue 2: substrate-conforming layer Definition re-lists ~40 invariants no proof consumes item-by-item
**ASN-0086, "Definition — substrate-conforming layer"**: "*(a) Invariant Catalog.* The full L/S/M/C invariant list of ASN-0036, ASN-0043, and ASN-0093: ... L0 (SubspacePartition), L1 ... L-fin ... S0 ... D-SEQ ... M0 ... C-fin ..."

**Problem**: The definition's first sentence already says "The full L/S/M/C invariant list of ASN-0036, ASN-0043, and ASN-0093"; the bullet lists then re-enumerate every label, plus bookkeeping prose ("ASN-0093 additionally re-asserts the ASN-0043 L-invariants noted above; those are not re-listed"). R7a's own proof confirms the enumeration is not consumed entry-by-entry: its "Per-step substrate-invariant preservation" paragraph discharges preservation wholesale — "every replay step is a primitive K-op ... each preserves the entire invariant catalog ... by its own ASN-0093 contract." This is use-site inventory the reader must skip.

**Required**: Replace the exhaustive label lists with the blanket reference already present, retaining only the genuinely R7a-load-bearing item (catalog (b)'s ChainMembershipForOrigin, which the proof explicitly singles out as load-bearing).

### Issue 3: "single derivation site" announcement and dual forward references are document-ordering meta-prose
**ASN-0086, "Lemma — LinkStoreInvarianceUnderArrangement"**: "This is the single derivation of link-store invariance under arrangement-modifying steps; the Definition of `↦` and the Definition of BroadExtension cite it rather than re-deriving."

**Problem**: This sentence describes document structure, not the system. It is reached by two forward "(below)" pointers ("holds `Σ'.L = Σ.L` by LinkStoreInvarianceUnderArrangement (below)" in Definition of `↦`; "keep `Σ.L` identical by LinkStoreInvarianceUnderArrangement (below)" in Definition of BroadExtension) — the "multiple paragraphs defer to the same downstream location" pattern. The consolidation itself is good; the announcement of the consolidation is noise.

**Required**: Delete the announcement sentence; the lemma stands on its own. The two upstream uses can state the equality and cite the lemma without the "(below)" deferral framing.

### Issue 4: Consequences typology key is document-structure meta-prose
**ASN-0086, R2 "*Consequences.*"**: "Each bullet is tagged by type — [COROLLARY] for a theorem-level implication ... The typology is fixed once here and applied uniformly in subsequent Consequences sections (R3, R4, R5, R6c)."

**Problem**: "The typology is fixed once here and applied uniformly in subsequent Consequences sections (R3, R4, R5, R6c)" is a use-site inventory of where a notational convention recurs — it advances no reasoning. The tags themselves are fine; the meta-announcement of the tagging scheme and its consumer list is the noise.

**Required**: Keep the one-line legend defining the tags; remove the sentence enumerating which later sections reuse them.

### Issue 5: R7a carries defensive meta-prose re-arguing its own precondition
**ASN-0086, R7a, statement and proof opening**: "The substrate-conformance precondition makes the assumption explicit in the claim itself; the proof verifies that no further clause is needed to derive the decomposition." and "Any layer publishing an operation ... that violated any invariant in the catalog would by definition place the substrate in a state inconsistent with ASN-0036/ASN-0043 — the resulting `Σ'` would not be a conforming substrate state — so non-conforming layers fall outside R7a's scope."

**Problem**: Both passages argue about why the precondition is shaped as it is and re-exclude a case (non-conforming layers) the precondition already excludes by hypothesis — the "imagines a case the precondition already excludes" / "explains why needed rather than what it says" drift patterns. The first sentence is a defensive note (residue of the resolved precondition restructuring); the second restates "conforming layers preserve invariants" as a scope argument.

**Required**: State the precondition once and proceed. Drop the self-referential "makes the assumption explicit" sentence and compress the out-of-scope re-argument to at most the single fact the proof uses (conforming ⟹ L12/L12a/L-fin/S0/S1 hold at each step).

### Issue 6: Duplicated import of the same ASN-0093 facts
**ASN-0086, "The Two Foundational Sets"** ("Globally `s_C`-resident content (from ASN-0093 L0)" and "Subspace identifier distinctness (from ASN-0093 SC-NEQ)") **and R4 proof**.

**Problem**: The `s_C`-residency (L0) and `s_C ≠ s_L` (SC-NEQ) facts are each imported with an equivalence-to-ASN-0036-notation gloss in the intro, then re-derived again in R4 ("SD ... a direct consequence of L0 ... together with SC-NEQ ... and T7"), and again inside FreshLinkKeyDisjointness. These are "two paragraphs saying the same thing in different words." Each restatement is short, but they compound.

**Required**: Import L0 and SC-NEQ once; have R4 and FreshLinkKeyDisjointness cite that import rather than re-narrating the L0 + SC-NEQ + T7 chain.

## OUT_OF_SCOPE

### Topic 1: Higher-arity retraction tuples bypassing `nullified`
`nullified(Σ)` draws only from `L_R^Σ`, which by the `L_K` definition requires `|Σ.L(a)| = 3`. A substrate-conforming layer could emit an arity-`> 3` link with type coverage `= coverage(R)` that never registers in `nullified`. The note explicitly restricts to standard-triple links and lists multi-arity relations as an open question, so this is future territory, not an error here.

### Topic 2: Arrangement/`L_K` cross-invariants
Whether relational predicates that depend on from/to content being currently visible in some `Σ.M(d)` need new invariants is already the first listed open question; correctly deferred.

META: not applicable — the ASN defines genuine new state (typed relations, `nullified`, active subsets), operations, and invariants stated abstractly, and remains on-track despite R0–R5 being thin restatements of ASN-0043/0093.

VERDICT: REVISE
