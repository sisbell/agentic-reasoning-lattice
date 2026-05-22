# Review of ASN-0094

## REVISE

### Issue 1: Lemma — RetractionTargetNotOnChain Case II is dense and under-structured

**ASN-0094, RetractionTargetNotOnChain Case II**: The cross-home case is approximately 60 lines of inline derivation covering local suffix definition, zero-count additivity via NAT-card, strictly-increasing-concatenation construction, T4b position-range agreement at three positional ranges, and Prefix-based componentwise reasoning. All within a single proof case.

**Problem**: A reader must track multiple interleaved steps without breakdown — the "well-formedness of `w` under `#w := #a - #b`", the bijection `Z_w^shift ↔ Z_w` re-indexing, the disposition of the `#a = #b` boundary sub-case via T3 ("follows by analogous argument"), and the explicit derivation of `home(a) = home(b)` via three N/U/D range-agreement arguments. The equal-length sub-case is hand-waved at the end.

**Required**: Either factor zero-count additivity over prefix decomposition into a separate named lemma (it's used in one place but is general), or restructure Case II into explicitly numbered sub-steps mirroring AllocatedAddressAntichain's Case 3 structure (Step II.1 zero-position sharing, Step II.2 N/U/D agreement, Step II.3 home contradiction).

### Issue 2: AllocatedAddressAntichain Case 3 sub-case presentation is inconsistent with its worked example

**ASN-0094, AllocatedAddressAntichain Case 3**: The formal proof walks Sub-case 3a (`x ∈ dom(Σ.L), a ∈ dom(Σ.C)`) explicitly at Step 3.3a, and discharges Sub-case 3b "by symmetry under the side-label swap." The worked example then walks Sub-case 3b only.

**Problem**: The formal proof and the worked example walk different sub-cases. A reader verifying the worked example against the formal proof must perform the symmetry swap mentally and re-derive Step 3.3b's component values. The proof's Case-symmetry argument is sound but the asymmetric exposition is jarring.

**Required**: Either walk both sub-cases formally in parallel (factoring the shared Steps 3.1, 3.2 and noting which clause of the subspace-partition scaffolding fires in each), or have the worked example match the formally-walked sub-case (3a), with 3b as a brief mirror.

### Issue 3: Sh-conf's return-type signature change has incomplete callsite analysis

**ASN-0094, Sh-conf**: "The framework extends ASN-0086's `Emit_K` return type from `Σ' × A_rel^{Σ'}` to `(Σ' × A_rel^{Σ'}) ∪ {⊥}`."

**Problem**: Changing the substrate primitive's return type silently breaks ASN-0086 callers. The framework handles Nullify via the NullifyActiveSubsetCompatibility corollary, but other callers (direct `Emit_K` invocations from layer code, any composite operation in ASN-0086 that consumes `Emit_K`'s return tuple) are addressed only via the candidate-set queries `C_K`/`C_fd_K`. The exposition does not enumerate which ASN-0086 surface is affected and what the compatibility commitment is for each.

**Required**: Add a brief enumeration table in the Nullify Compatibility section listing ASN-0086's `Emit_K` consumers (Nullify, direct callers, downstream operations) and the framework's compatibility commitment for each. Currently a reader must reconstruct this from scattered remarks.

### Issue 4: Emit_K routing commitment is load-bearing but its violation mode is not consolidated

**ASN-0094, Scope and Substrate Scaffolding**: The *Emit_K routing commitment* is cited inside Case B of Sh0, Sh1, Sh2, Sh3 (four sites) and inside Step 1 of EffectiveWpSimplification. It is the layer-level assumption that every class-(iii) emission of `K ∈ T_cat` routes through `Emit_K`.

**Problem**: If a layer bypasses `Emit_K` by directly invoking K.λ, the preservation theorems Sh0-Sh4 fail silently — the substrate primitive K.λ remains permissive at the substrate level and admits arbitrary `(F, G, K)` triples. The framework provides no detection mechanism. The "outside scope" framing is acknowledged in pieces (Sh-conf's "Scope" paragraph, Sh0's Case B citation) but the failure mode is not consolidated.

**Required**: Add a single paragraph (either under Sh-conf or as a new "Routing Failure Modes" sub-section) stating: (a) which preservation theorems lose their guarantees under routing violation, (b) which templates become ill-defined, (c) which contracts (Sh4, FDD, single-home) lose their preservation under routing violation.

### Issue 5: Single-home commitment specification is buried inside the Coverage walkthrough

**ASN-0094, Coverage instantiation**: The *single-home commitment* — the framework's third per-K layer-discipline contract — is defined within the "Coverage instantiation (opt-in via SingleHomeCoverageDiscipline)" sub-section of NonIdempotentDirectedPair.

**Problem**: The framework introduces three distinct layer-discipline contracts: the *Sh4 idempotency contract* (in its own Idempotency section), the *FDD functional-dependency contract* (in its own FunctionalDependencyDiscipline sub-section), and the *single-home commitment*. The first two have dedicated structural placement; the third is embedded within a per-shape walkthrough, making its contract clauses (i)-(ii), preservation theorem, base/Case A/B/C structure, status, and failure modes harder to locate. The framework's naming convention paragraph treats all three as parallel commitments.

**Required**: Promote the *single-home commitment* and the SingleHomeCoverageDiscipline definition to a dedicated section parallel to Idempotency (Sh4) and FunctionalDependencyDiscipline, or consolidate all three contracts into a single "Layer-Discipline Contracts" section.

### Issue 6: Gate ordering with multiple disciplines is not documented in one place

**ASN-0094, Sh4 contract Ordering with Sh-conf / FDD contract Ordering with Sh-conf**: Each per-K discipline contract describes its ordering with Sh-conf locally. The Sh4 contract states canonical-form gate first, Sh4 contract second, cardinality/target-domain gates third. The FDD contract restates the identical structure. The single-home commitment's ordering relative to Sh-conf and other contracts is not explicitly specified.

**Problem**: At a K registered with multiple disciplines (in practice the disciplines are mutually exclusive, but the framework should document this), the full call-site gate ordering is reconstructible only by reading all three contract sections. A reader needs: (1) single-home check first (literal equality, no Observe); (2) Sh-conf canonical-form gate (clauses a, b); (3) Sh4 *or* FDD contract clauses (i)-(iii) (mutually exclusive at the registered K); (4) Sh-conf cardinality/target-domain gates (clauses c, d); (5) K.λ.

**Required**: Add a "Gate Ordering" sub-section under Sh-conf consolidating the per-K call-site gate ordering, including the mutual-exclusion argument for the disciplines (FDD requires idem=⊤, SHCD requires idem=⊥) and the single-home commitment's literal-equality semantics.

### Issue 7: Per-class constancy is asserted as a registry property without specifying the registration interface

**ASN-0094, ShapeRegistry Definition**: "Per-class constancy. For K, K' ∈ T_cat with K ~ K': shape(K) = shape(K'). The function shape factors through T_cat / ~."

**Problem**: Per-class constancy is required for Sh0-Sh4's inductive arguments (where the new tuple's type K' may be `~`-equivalent to the K being examined, and the proof appeals to `shape(K') = shape(K)`). The constancy property is asserted but the registration mechanism — how a layer ensures all coverage-equivalent endsets receive the same shape value — is unspecified. Decidable membership (via coverage-equivalence against a representative list) is specified for T_cat, but the symmetric specification for `shape` is missing.

**Required**: Add a brief paragraph specifying the registration interface: the layer registers a representative K_rep from each ~-class together with shape(K_rep); `shape` extends to the rest of the class by per-class constancy. This makes per-class constancy a consequence of the registration interface, not an independent property to verify.

### Issue 8: Worked examples have partial template coverage

**ASN-0094, "Resolution base templates exercised directly" / Provenance walkthrough / Coverage walkthrough**: Resolution exercises 2 of 5 base templates (`pair_K`, `to_addrs_K`). Coverage walks `latest_K_for_addr` but not the four base templates. Provenance shows partial-G admission via `to₁⁻` but does not exercise Sh4 suppression at this shape.

**Problem**: The framework's central claim is shape-determined template uniformity. A reader verifying this claim against the worked examples finds that the verification is split unevenly: some shapes are fully exercised (Comment via the long walkthrough plus Tuple-Classifier and Attributed Retraction), others only partially. The remaining cases are dispatched as "compute analogously and are omitted." The cumulative gap is significant for the framework's verification claim.

**Required**: Add a brief verification table per worked example listing all base templates evaluated at the example's state. Even one-line evaluations ("`from_K(d_2) = {τ_2}`") would close the verification cycle. The current per-template "omitted by analogy" claims are reasonable in isolation but inconsistent in aggregate.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate consistency

**Why out of scope**: The framework's atomicity contracts are explicitly scoped to single-process substrates (Sh4 contract "Scope: single-process substrate" clause, Open Questions). Multi-process scenarios require distributed coordination protocols at the `~`-equivalence class scope, which would extend the framework's scope rather than fill a current gap.

### Topic 2: T_cat runtime extension and substrate evolution

**Why out of scope**: The framework forbids runtime extension of T_cat. Substrates needing to add typed relations mid-life face a re-initialization path. The migration story is acknowledged as outside scope (TypedRelationCatalog Definition's "Lifetime constancy of T_cat" paragraph).

### Topic 3: Ghost-targeting slot semantics

**Why out of scope**: L9 (ASN-0043) admits ghost addresses in endsets; Sh-conf clause (d) rejects them in slot positions. Whether future shape families should admit state-dependent conformance for ghost slots is an open design question, not a current framework defect (acknowledged in Open Questions).

### Topic 4: Mechanical derivation of template families

**Why out of scope**: Sh5(a) explicitly states templates are hand-curated. Whether a future framework could derive templates mechanically from shapes is an open META question.

### Topic 5: Predicate composition closure

**Why out of scope**: The framework provides atomic per-shape templates and notes that composition into composite predicates is a layer-level concern. Whether composition can express predicates strictly beyond atomic templates is acknowledged as not addressed.

VERDICT: REVISE
