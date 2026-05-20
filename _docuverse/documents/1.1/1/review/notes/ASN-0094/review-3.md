# Review of ASN-0094

## REVISE

### Issue 1: Restatement of foundation definitions
**ASN-0094, "Definition — ZeroCountDepth" through "Definition — WeakestPreconditionEmitK"**: ASN-0094 restates twelve definitions (ZeroCountDepth, AllocatorTreeDepth, Extension, BroadExtension, RetractionType, RetractionDirectionality, SubstrateConformingLayer, EmitKFunctionNess, FreshEmissionAddress, NoCraftedSpanReachesD, WeakestPreconditionNullify, WeakestPreconditionEmitK) verbatim from ASN-0086's vocabulary.
**Problem**: The review rule says "ASNs may use foundation definitions without restating them." Many of these (RetractionType, RetractionDirectionality, EmitKFunctionNess, FreshEmissionAddress, NoCraftedSpanReachesD, WeakestPreconditionNullify, WeakestPreconditionEmitK, ZeroCountDepth, AllocatorTreeDepth) are also never invoked in ASN-0094's body. They are dead in this ASN's context.
**Required**: Delete the unused definition restatements. For SubstrateConformingLayer, Extension, BroadExtension (which ARE used), reference them by name as foundation imports rather than restating their bodies.

### Issue 2: Foreign ASN references in restated SubstrateConformingLayer body
**ASN-0094, "Definition — SubstrateConformingLayer"**: "*(a) Invariant Catalog.* The full L/S/M/C invariant list of ASN-0036, ASN-0043, and ASN-0093: ... *ASN-0036 content/arrangement invariants*: S0, S1, S2, S3, ... *ASN-0093 substrate invariants*: M0, M1, C0, C1, ..."
**Problem**: The restated definition references ASN-0036 and ASN-0093 by number. These are not in the foundation list (ASN-0034, ASN-0043, ASN-0086). Even if the original ASN-0086 definition contains these references as part of its foundation contract, ASN-0094 restating them surfaces non-foundation cross-references in this ASN.
**Required**: Remove the restatement entirely (per Issue 1). When ASN-0094 needs the substrate-conforming-layer contract, cite it as "the SubstrateConformingLayer contract of ASN-0086" without re-enumerating the inherited content.

### Issue 3: Sh0-Sh3 proof Case A conflates two sub-cases
**ASN-0094, "Sh0 Proof, Inductive step, Case A"**: "K.σ and K.α leave `Σ.L` unchanged, so `L_K^{Σ'} = L_K^Σ` for every K; the property is inherited. The only sub-class affecting `dom(Σ.L)` is K.λ. By the layer commitment ... every K.λ-step producing a tuple in `L_K^Σ` for `K ∈ T_cat` originates as an `Emit_K` call..."
**Problem**: Case A purports to cover all "dom-extending steps (K.σ, K.α, K.λ)" but the argument splits the K.λ class into (i) K.λ emitting a tuple of type K (handled by layer commitment + Sh-conf) and (ii) K.λ emitting a tuple of type K' ≠ K (which leaves `L_K` unchanged). Sub-case (ii) is never explicitly handled. The K.λ branch is then absorbed into the "by layer commitment" argument without first ruling out K.λ steps for other types. The same elision appears in Sh1, Sh2, Sh3 proofs.
**Required**: Split Case A explicitly: (A1) step does not change `L_K` (K.σ, K.α, K.λ emitting non-K tuples, and arrangement steps for the broader `↦`); (A2) step is a K.λ for type K admitted by Emit_K. Or broaden Case A to "any step that leaves `L_K^Σ = L_K^{Σ'}`" and treat the K-emission case separately.

### Issue 4: Sh4 proof case structure incomplete
**ASN-0094, "Sh4 Preservation under the contract"**: "*Step (Case A: `Σ → Σ'` is K.σ or K.α).* `Σ.L` is preserved pointwise..."
**Problem**: Case A names only K.σ and K.α as the "doesn't change A_K" class. K.λ steps emitting tuples of types K' ≠ K (and K' ≠ R) also leave `A_K` unchanged but are unhandled. Case B narrows to "K.λ-step admitting a new K-tuple" without mentioning other K.λ steps; Case C only covers retraction and arrangement-modifying steps. K.λ for K' ∉ {K, R} falls through the cracks.
**Required**: Add the missing branch explicitly (either to Case A or as a new sub-case) and note that under such a step `L_K^{Σ'} = L_K^Σ` and `nullified(Σ') = nullified(Σ)` (since `L_R` is unchanged when K' ≠ R), so `A_K` is unchanged.

### Issue 5: Opaque notation `slot_addrs(F)(τ)`
**ASN-0094, "Sh4 contract clause (i)"**: "`C(F, G, Σ) := {τ ∈ A_K^Σ : slot_addrs(F)(τ) = slot_addrs(F) ∧ slot_addrs(G)(τ) = slot_addrs(G)}`"
**Problem**: `slot_addrs(F)(τ)` does not parse cleanly. `slot_addrs` is defined as a function on endsets (`slot_addrs(F) = X_F`), not as a slot-of-tuple accessor. The intent appears to be "the slot-addresses of τ's F-slot," but as written it reads as `slot_addrs(F)` applied to τ. The same opaque notation appears in the proof's contradiction step.
**Required**: Use an explicit accessor. For example: let `F_τ, G_τ` denote the F-slot and G-slot endsets of `τ`; then `C(F, G, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)}`. Or use the substrate's slot accessors directly: `from_K^Σ(τ) = slot_addrs(F)`.

### Issue 6: Notational collision Σ_K for shape vs Σ for state
**ASN-0094, "Definition — Shape"**: "A *shape* is a tuple `Σ_K = (c_F, c_G, t_F, t_G, idem)`"
**Problem**: Σ is used throughout the ASN as the system state. Reusing Σ as the shape constructor (even with a K subscript) creates a notational collision in expressions like `Σ_K = shape(K) at state Σ`. The body works around this by writing `shape(K)` everywhere, but the Shape definition itself unnecessarily introduces the collision.
**Required**: Rename the shape tuple — e.g., `S_K`, `Sh_K`, or just drop the named-tuple notation and refer to `shape(K) = (c_F, c_G, t_F, t_G, idem)` directly.

### Issue 7: T_cat closure under ~ ambiguous
**ASN-0094, "Definition — TypedRelationCatalog"**: "By coverage-equivalence (ASN-0086, `~` definition), `T_cat` is treated up to `~`: if `K ∈ T_cat` and `K ~ K'`, then `K'` inherits `K`'s shape (equivalently, the registry operates on the quotient `T_cat / ~`)."
**Problem**: The status of `K'` is left ambiguous: is `K' ∈ T_cat`, or just `shape(K') = shape(K)`? Sh-conf rejects "unregistered types" — does this mean types whose class `[K]` lacks a registered representative, or types `K` not literally in the catalog? The downstream layer-commitment argument ("every class-(iii) emission of a type `K ∈ T_cat`") doesn't say whether this is membership or class-membership.
**Required**: Choose one formal reading. Either define `T_cat ⊆ T_admissible / ~` as a set of classes (and `K ∈ T_cat` means `[K] ∈ T_cat`), or define `T_cat ⊆ T_admissible` to be ~-closed (so `K ∈ T_cat ∧ K ~ K' ⟹ K' ∈ T_cat`). Sh-conf's clause "K ∈ T_cat" then becomes unambiguous.

### Issue 8: Tpl referenced in properties table but not defined
**ASN-0094, "Properties Introduced" table**: "Tpl | DEF | Map from canonical shape to its predicate template family"
**Problem**: The body never formally defines `Tpl` as a function. It exhibits template families per shape in "Per-Shape Template Walkthroughs" but does not assemble these into a typed function `Tpl : Shape → TemplateFamily` with a precise codomain.
**Required**: Either (a) drop the row from the table since templates are hand-curated per shape and not packaged as a single function, or (b) define `Tpl` with explicit signature and enumerate the catalog entries.

### Issue 9: AllocatedAddressAntichain Case 3 "vice versa" not made explicit
**ASN-0094, "Lemma — AllocatedAddressAntichain, Proof, Case 3"**: "(`x ∈ dom(Σ.L), a ∈ dom(Σ.C)`, or vice versa)"
**Problem**: The proof works through the case `x ∈ dom(Σ.L), a ∈ dom(Σ.C)` and concludes "Contradiction; this case is vacuous." The symmetric case `x ∈ dom(Σ.C), a ∈ dom(Σ.L)` is dispatched only by "or vice versa." For symmetric arguments this is acceptable, but here the argument turns on which side carries `s_L` versus `s_C`. The vice-versa direction needs at least one sentence noting that swapping x and a yields `E(x).1 = s_C` and `E(a).1 = s_L`, again contradicting `s_C ≠ s_L`.
**Required**: Add the symmetric step explicitly, or replace "or vice versa" with "WLOG x ∈ dom(Σ.L), a ∈ dom(Σ.C); the case x ∈ dom(Σ.C), a ∈ dom(Σ.L) yields the same s_C ≠ s_L contradiction by swapping roles."

### Issue 10: emission_order monotonicity claim lacks derivation
**ASN-0094, "Coverage walkthrough"**: "We define: `emission_order(τ) := the chain-index of addr(τ) within the link sub-allocator chain at d_K` ... The `argmax` in `latest_K_for_addr` is then well-defined under T1."
**Problem**: The argument that `argmax` is well-defined requires (i) `S_d` is finite (yes, from L-fin), (ii) `emission_order` is a total order on `S_d` (claimed via T9), and (iii) the order is monotone in emission time. T9 establishes that within a single allocator's chain, `allocated_before(a, b) ⟹ a < b` under T1. The chain-index ordering and emission-time ordering are claimed to coincide, but this requires a one-line argument: T9 + T10a.7 (EnumerationInjectivity) give that chain index n strictly increases with allocation time, and the address at index n+1 is strictly above the address at index n under T1.
**Required**: State the derivation explicitly: under SingleHomeCoverageDiscipline, all K-tuples have addresses on `A_L(d_K)`'s chain; T10a.7 makes chain indices unique; T9 makes the chain-index → tumbler map strictly increasing. The `argmax` picks the unique chain element of maximal index in `S_d`.

### Issue 11: Worked example covers only Comment shape
**ASN-0094, "Worked Example: K = comment"**: only Comment is walked through.
**Problem**: The framework's most subtle template — Coverage's `latest_K_for_addr` under SingleHomeCoverageDiscipline — has no concrete verification. Provenance's partial accessor `to₁⁻` semantics has no example. The bipartite Classifier/Tuple-Classifier distinction has no example to show the substitution `d ↝ τ` working out.
**Required**: Add at least one worked example for Coverage (showing `emission_order` over 2–3 emissions, verifying `latest_K_for_addr(d)` returns the most recent). Brief examples for Provenance and Tuple-Classifier would also strengthen the catalog walkthrough.

### Issue 12: Worked example omits cardinality-violation rejection
**ASN-0094, "Worked Example, Rejection cases"**: covers non-canonical form (clause (a) violation) and unallocated address (clause (d) violation).
**Problem**: Clause (c) — cardinality mismatch via `match(|X_F|, c_F)` — is never exercised. An emission with `|X_F| = 2` against `c_F = 1`, or with empty F-slot against `c_F = 1`, would test the cardinality branch of Sh-conf.
**Required**: Add a rejection case where `slot_addrs(F)` has the wrong cardinality (e.g., 2 addresses with `c_F = 1`), showing Sh-conf clause (c) rejecting the emission.

### Issue 13: Sh5 expressive-ceiling claim unsupported
**ASN-0094, "Consequences (b)"**: "Composite predicates extend within the ceiling, not beyond it. ... Composition does not raise it. Capability beyond the ceiling requires a new canonical shape, not a new relation in an existing shape."
**Problem**: "Composition does not raise" the ceiling is stated as a fact but has no supporting argument. The framework offers Boolean operators and quantification over T_cat; whether these can express predicates beyond per-shape templates depends on which composition primitives are admitted. The claim needs either a proof sketch or downgrading to a META observation.
**Required**: Either prove the closure claim (define what "composition" admits and show templates closed under it), or rephrase as a design observation rather than a structural property.

### Issue 14: `-^Σ` (absent-slot expansion) not formally specified
**ASN-0094, "Definition — Shape"**: "At each state Σ the symbol expands to the corresponding allocated set: `A_doc ↦ A_doc^Σ = dom(Σ.C)`, `A_rel ↦ A_rel^Σ = dom(Σ.L)`, `A ↦ A^Σ = A_doc^Σ ∪ A_rel^Σ`."
**Problem**: The expansion table omits `-`. The conformance definition says "When `t_F = -` ... the F-side of (d) is vacuously satisfied since `X_F = ∅`" — but this leaves `-^Σ` undefined as a set. A reader cannot mechanically check clause (d) without knowing how to interpret `-^Σ`.
**Required**: Specify `-^Σ = ∅` (or some other convention) so clause (d) becomes uniformly checkable: `X_F ⊆ -^Σ ⟺ X_F = ∅`, which holds by the c_F = 0 constraint.

### Issue 15: Set-vs-bag semantics distinction informal
**ASN-0094, "Sh4 Justification of the policy"**: "For idempotent relations the predicate template uses *set semantics* ... For non-idempotent relations ... the predicate template uses *bag semantics* — multiplicities are preserved."
**Problem**: Templates return either Booleans or sets of tuples (subsets of A_K^Σ). The "bag" character — that two distinct tuples in A_K^Σ can have identical `(F, G)` slot pairs — is structural and not a separate "semantics." The set/bag dichotomy reads as if templates somehow choose how to interpret A_K, but A_K is always a set of (distinct-address) tuples.
**Required**: Rephrase to drop the bag-semantics framing. The point is that idempotent relations admit existence-vs-count distinction predicates because Sh4 collapses `(F, G)`-duplicates in A_K; non-idempotent relations support count predicates because such duplicates can persist.

## OUT_OF_SCOPE

### Topic 1: Cross-process / distributed shape registry consistency
**Why out of scope**: Mentioned in Open Questions. Distributed coordination of the lifetime-constant `shape` registry across substrate processes is a deployment concern, not a framework-level invariant.

### Topic 2: New canonical shapes beyond the current catalog
**Why out of scope**: The catalog is enumerated as the current set; new shapes (e.g., the hypothetical Tuple-Attribute or `(0, 0)` shapes mentioned in Open Questions) are future additions, not gaps in this ASN.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: The framework's current discipline forbids ghost addresses in slot positions. Whether to admit shape-conformant ghost-targeting (with a state-dependent conformance rule) is noted as an Open Question and would require a new shape axis.

### Topic 4: Composite shapes (relations whose F or G is constrained by another relation's content)
**Why out of scope**: Noted in Open Questions. Adding a meta-shape language to compose shapes is a separate framework extension.

VERDICT: REVISE
