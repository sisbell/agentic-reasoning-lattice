# Review of ASN-0086

## REVISE

### Issue 1: Load-bearing citations to foundation claims that do not exist in the cited foundations
**ASN-0086, multiple sites**: e.g. "By ChainUniformLength (ASN-0093), `#a = #t_i = #t_1 = #a'`" (R0a, Case 2); "ChainUniformLength (ASN-0093) gives `#t_n = #t_1`" (R0a-Cor2); "By ChainUniformZeroCount (ASN-0093)" (R0a-Cor2, Step 1 verifications); "ASN-0093's SubAllocatorAxiom directly axiomatizes the sub-allocator structure" (Allocator Structure), with sub-references `SubAllocatorAxiom.Exists`, `.FirstEmission`, `.ChainDiscipline` throughout.

**Problem**: The provided ASN-0093 claim statements contain **no** `SubAllocatorAxiom`, no `ChainUniformLength`, and no `ChainUniformZeroCount`. ASN-0093 axiomatizes allocation through `K.σ/K.α/K.λ` plus the lemmas `ChainDiscipline`, `FirstEmission`, `ChainMembershipForOrigin`, `ChainEnumerationInjectivity`, etc. The uniform-length / uniform-zero-count facts this note needs trace to ASN-0040's `S(p,d)` postconditions (`#cₙ = #p + d`, `sig(cₙ) = #p + d`) routed through `ChainDiscipline` — but the note invents ASN-0093 lemma names instead of citing what the foundation actually provides. R0a-Cor2 (a headline result, `#E = 2` strictly) and R0's subsequent-emission freshness both rest on these phantom citations. A precise reader cannot discharge them.

**Required**: Replace every `ChainUniformLength`/`ChainUniformZeroCount`/`SubAllocatorAxiom.*` citation with the actual ASN-0093 lemma (`ChainDiscipline`, `FirstEmission`, `ChainMembershipForOrigin`) or the ASN-0040 `S(p,d)` postcondition it derives from. If the note intends a "SubAllocatorAxiom," it must name the ASN-0093 construct that exists (`ChainDiscipline` is a LEMMA, not an axiom; ASN-0093's only axioms are `SubspaceConventionAxiom` and `SequentialTransitionAxiom`).

### Issue 2: Citations to ASN-0034 / ASN-0036 claims that do not exist
**ASN-0086, R0a-Cor2**: "incrementing a non-zero ℕ-value stays non-zero — established locally by NAT-zero + NAT-discrete + NAT-addcompat … identically to the chain in ASN-0034 T10a.8" and "the T10a.8 mechanism (TA5(c) modifies only the terminal position…)".
**ASN-0086, `↦` definition**: "holds `Σ'.C = Σ.C` by ASN-0036's S9 (TwoStreamSeparation)".
**ASN-0086, R0 and substrate-conforming catalog**: "S0, S1, S2, S3, S7a, S7b, S7c, S7d, …" / "S7a–c (content-attribution invariants)".

**Problem**: ASN-0034 has `NAT-closure/discrete/order/wellorder/addcompat` — there is **no `NAT-zero`**. ASN-0034 has `T10a.1`–`T10a.7`, `T10a`, `T10a-N` — there is **no `T10a.8`**. ASN-0036 has `S7, S7a, S7b, S7d` — there is **no `S7c`** and **no `S9 (TwoStreamSeparation)`**. The `↦`-frame argument (`Σ'.C = Σ.C` under arrangement modification) depends critically on the nonexistent S9; `LinkStoreInvarianceUnderArrangement` and R6c-Corollary inherit this gap.

**Required**: Either cite the real foundation claim that establishes each fact (e.g., for `Σ.C` invariance under `Σ.M`-modification, point to the actual ASN-0036 mechanism, not "S9"), or supply the argument inline. Remove `NAT-zero`, `T10a.8`, `S7c`.

### Issue 3: Foundation claims cited under the wrong label
**ASN-0086, R4**: "T7 (FirstElementFieldDistinction, ASN-0034)".
**ASN-0086, AddressUniverse / R4 / R0**: "ASN-0093 L14 (StoreDisjointness) — equivalently ASN-0043 L14 (DualPrimitive)".

**Problem**: ASN-0034's T7 is **SubspaceDisjointness**, not "FirstElementFieldDistinction" (the note itself uses the correct name elsewhere, e.g. in the R5 area and Setup). ASN-0093's store-disjointness claim is labeled **SD**, not "L14" — ASN-0093 has no claim labeled L14. The inconsistent labels make verification fail at the citation site and contradict the note's own usage.

**Required**: Use `T7 (SubspaceDisjointness, ASN-0034)` and `SD (StoreDisjointness, ASN-0093)` uniformly.

### Issue 4: Meta-prose around definitions and forward references (anti-bloat)
**ASN-0086, multiple structural slots**:
- Allocator Structure: "The descriptive lemma below is retained because subsequent claims (especially in the Worked Sketch) refer to the *shared depth-one allocator*…" — justifies the lemma's inclusion rather than advancing it.
- R6b: "We name R6b as a DEF-Consequence because the choice of quantification range, rather than being a derived theorem, is the substantive design commitment whose flatness and non-fixpoint consequences govern the rest of this development…" — prose explaining why the label was chosen.
- Definition — substrate-conforming layer, "Status note on L5/L6/L8" and "Alignment with substrate and implementation": the L5/L6/L8 paragraph explains *why the catalog bundles them* rather than stating an obligation; the alignment paragraph is essay content ("Nelson's broader design intent, expressed in Literary Machines, does not require chain-discipline emission per se — his substrate invariants are permanent addressing, span-attached link survivability, link ownership by home, type openness, and search efficiency").
- Definition — substrate-conforming layer: "R7a (below) cites this Definition by name in its precondition; the proof's *Per-step substrate-invariant discharge* block enumerates how each entry in (a) and (b) is preserved…" — a definition enumerating its downstream consumer.
- Multiple sections defer to the same downstream location: R6c Consequence (d), the unit-depth-discipline "Consumption" paragraph, and the Nullify discussion all forward to "WP Case 2 (Weakest-Precondition Analysis, below)."
- R5 proof: "(proved below from R0's verification structure, independent of the specific endset content used here — no circular dependency)" and R5-Cor's "Scope distinction" paragraph distinguishing R5 from R5-Cor.

**Problem**: This note carries the `review-mode.anti-bloat` classifier. Each item above is meta-prose: inclusion justifications, label rationale, use-site inventories, repeated downstream deferrals, and essay content in structural slots. A reader following the argument must skip past them.

**Required**: Delete the inclusion/label justifications (state the lemma and its dependencies; the label table already records status). Collapse the repeated "see WP Case 2" deferrals to a single pointer at the earliest site. Move the implementation/Nelson essay content out of the substrate-conforming-layer Definition (the catalog needs the invariant list, not the motivation). State L5/L6/L8's discharge mechanism in one line without the "why the catalog bundles them" paragraph.

### Issue 5: R0 re-derives a freshness result the foundation already names
**ASN-0086, R0 subsequent-emission branch**: the three-part sub-claims (a)/(b)/(c) re-derive "fresh against same-home chain / cross-home links / content."

**Problem**: ASN-0093 supplies `SubsequentEmissionFreshness`, which establishes exactly this three-way split as a foundation lemma, yet R0 reconstructs it from `ChainEnumerationInjectivity + CrossDocDisjointness + DisjointSubAllocatorChains + L0 + SC-NEQ + T10` rather than citing it. This is duplicated reasoning the foundation already carries (and is the kind of accretion the anti-bloat classifier targets).

**Required**: Cite `SubsequentEmissionFreshness (ASN-0093)` for the subsequent-emission branch and drop the re-derivation, or state explicitly why the foundation lemma is insufficient here.

## OUT_OF_SCOPE

### Topic 1: Concurrency / atomicity of Emit vs. Observe
The Open Questions raise whether Emit is atomic w.r.t. concurrent Observe and the consistency model for `A_K` transitions. These are genuine but belong to a future ASN; this note correctly works under `SequentialTransitionAxiom` (ASN-0093) and need not resolve them.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
Multi-arity links are explicitly deferred ("which we do not pursue here"). The active-subset machinery's extension to `|Σ.L(a)| > 3` is future territory, not a defect of the standard-triple development.

### Topic 3: Whether L1b should be tightened to `#E = 2` at the foundation
R0a-Cor2 establishes `#E = 2` for this note's links; whether ASN-0043's L1b admission should itself be narrowed is a foundation-design question for a future ASN, not a fix to ASN-0086.

VERDICT: REVISE
