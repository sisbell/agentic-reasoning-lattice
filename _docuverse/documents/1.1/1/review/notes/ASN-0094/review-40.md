# Review of ASN-0094

## REVISE

### Issue 1: NAT-card and NAT-sub derivations are presentation overhead
**ASN-0094, "Locally derived NAT primitives (NAT-card, NAT-sub)"**: The Scope and Substrate Scaffolding section interleaves multi-paragraph local derivations of NAT-card (strictly-increasing enumeration of finite ℕ-subsets with additivity) and NAT-sub (uniqueness of partial subtraction), each requiring an "external well-founded measure" justification and a "background ℕ-arithmetic facts" caveat for commutativity and associativity.

**Problem**: The shape framework's substantive content is buried under primitives that belong upstream. The "background facts" caveat reveals the foundation does not supply ℕ-commutativity, ℕ-associativity, or strict-monotonicity-of-addition; the ASN compensates by deriving these locally with full induction structure. A reader trying to understand the shape framework wades through Peano-level arithmetic before reaching Sh-conf.

**Required**: Move NAT-card and NAT-sub to an appendix or a separate preliminaries ASN. Cite them by name in proof bodies. The foundation gap should be fixed at the foundation level, not papered over in every ASN that uses cardinality arithmetic.

### Issue 2: Elementary set-theoretic facts proved at full length
**ASN-0094, AllocatedAddressAntichain Step 3.1**: The "subset-with-equal-cardinality coincides with its containing set" inference (a 3-element subset of a 3-element set equals the set) is derived via NAT-card uniqueness over strictly-increasing enumerations, with explicit construction of `f_{Z_a}`, indices `j_i`, and a strict-monotonicity argument forcing `(j_1, j_2, j_3) = (1, 2, 3)`.

**Problem**: This level of justification for an elementary finite-set fact blurs the distinction between routine bookkeeping and load-bearing argument. The same pattern recurs throughout (e.g., RetractionTargetNotOnChain Step II.0 deriving `#a − #b ≥ 1` via NAT-sub's defining equation when `#b < #a`). The signal-to-noise ratio in the proofs degrades.

**Required**: Treat elementary set/arithmetic facts as background, with a single appendix note if needed. Reserve detailed construction for substantive shape-preservation claims.

### Issue 3: EffectiveWpSimplification's R-registration precondition is implicit
**ASN-0094, Corollary — EffectiveWpSimplification**: Step 1's discharge of `NoCraftedSpanReachesD(Σ, d)` cites "Sh1 at K := R" and "Sh3 at K := R" without listing `R ∈ T_cat` in the corollary's preconditions.

**Problem**: Sh1/Sh3 at K := R require R registration (the framework's mandatory baseline, stated in Nullify Compatibility). A consumer reading the corollary alone might miss that the conclusion fails for layers that decline R-registration. The dependency on a section several pages upstream is fragile.

**Required**: Add `R ∈ T_cat (baseline registration per Nullify Compatibility)` to the corollary's preconditions alongside the existing `Σ reachable from Σ_init under the Emit_K routing commitment`.

### Issue 4: K_res registration timing in Comment walkthrough is ambiguous
**ASN-0094, Worked Example: K = comment**: "K_res (a Resolution-shape relation, introduced by name when Emission 3 fires below — the layer registers it under shape (1, 1, A_doc, A_rel, ⊤) at Σ_0)"

**Problem**: The framework's lifetime constancy (TypedRelationCatalog Definition) fixes T_cat at Σ_init. The walkthrough's "registers it at Σ_0" reads as if registration is deferred to Σ_0, which would violate constancy. The intent is presumably "registered at Σ_init, narratively introduced when Emission 3 fires", but the prose is imprecise.

**Required**: Rephrase to "K_res registered at Σ_init per lifetime constancy; exercised first at Emission 3." Audit every walkthrough's "Registered catalog" paragraph for the same phrasing issue.

### Issue 5: Repetition of "Registered catalog for this walkthrough" paragraphs
**ASN-0094, all walkthrough sections**: Each walkthrough begins with a structurally-identical paragraph declaring T_cat = {...}, R registration baseline, lifetime constancy from Σ_init, and L_K^Σ_init = ∅.

**Problem**: The convention is uniform across walkthroughs and could be stated once at the framework level. Per-walkthrough restatement adds bulk without information.

**Required**: State the convention once (Initial-State Baseline section). Each walkthrough declares only the K's it exercises plus any per-walkthrough specifics.

### Issue 6: Σ-prefix convention is inconsistent across walkthroughs
**ASN-0094, Additional Worked Examples: Tuple-Classifier**: "we adopt the per-walkthrough prefix `Σ^TC`: the starting state is `Σ^TC_0 := Σ_4`"

**Problem**: All other walkthroughs use bare `Σ_0, Σ_1, ...` with implicit per-walkthrough scoping. Tuple-Classifier introduces an explicit prefix for scope-disjoint citation. The asymmetric treatment suggests indecision about the convention.

**Required**: Pick one convention (implicit scoping or explicit prefix) and apply uniformly across all walkthroughs.

### Issue 7: Sh5 audit table presented without catalog-growth procedure
**ASN-0094, Sh5(b) discipline and audit table**: The audit table enumerates 11 accepted catalog rows and references one rejected candidate. The ASN says auditor-side hand-review enforces template-body convergence at shape-mate rows.

**Problem**: The audit table is presented as a snapshot at the current catalog. The discipline is meant to apply to future extensions, but no procedure describes how a new row gets reviewed, who maintains the table, or what records an admission/rejection decision. "Auditor-side review" remains undefined.

**Required**: Either declare the audit table a snapshot (no growth commitment) or specify the registration procedure (review checklist, decision record, who maintains the table).

### Issue 8: Layer Composites section is over-engineered for one entry
**ASN-0094, Layer Composites**: A top-level section houses a single composite (K_is_fresh).

**Problem**: Section-level framing for one example adds structural overhead.

**Required**: Fold K_is_fresh into the DirectedPair + FDD walkthrough as an extension example, or remove the section header and discuss inline.

### Issue 9: Two near-duplicate paragraphs surface the same layer commitment
**ASN-0094, AllocatedAddressAntichain**: The *Framework-wide layer commitment* paragraph (Scope and Substrate Scaffolding) and the *Layer-commitment role in the proof* paragraph (AllocatedAddressAntichain preamble) both describe the `subspace_I(·) = E(·).1` identification's status as a framework-wide invariant.

**Problem**: The second paragraph repeats what the first establishes, then explicitly notes "the present paragraph is expository and points a reader at the named invariant rather than declaring an independent conditional." If it's purely expository and adds no new content, it should be cut.

**Required**: Remove the *Layer-commitment role in the proof* paragraph. The framework-wide commitment is sufficient.

## OUT_OF_SCOPE

### Topic 1: Multi-process consistency of the shape registry
**Why out of scope**: Already flagged in Open Questions under [scope boundary]. The framework explicitly commits to single-process substrates.

### Topic 2: Mechanical procedure for template family derivation
**Why out of scope**: Sh5 META observation (a) admits hand-curation; mechanical derivation is a separate research thread.

### Topic 3: Foundation gap for ℕ-commutativity and ℕ-associativity
**Why out of scope**: The gap is in the foundation NAT axioms, not in ASN-0094. Fixing it belongs in a foundation revision.

### Topic 4: Bipartite catalog rows for tuple-targeting DirectedPair variants
**Why out of scope**: The catalog explicitly enumerates rows demanded by present-day templates; extensions are incremental work.

VERDICT: REVISE
