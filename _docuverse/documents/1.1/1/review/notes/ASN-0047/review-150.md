# Review of ASN-0047

## REVISE

### Issue 1: Step (B) of the K.μ~ dependency chain names its goal as "realising S3★(Σ')" — but S3★(Σ') is an admissibility *input*, making the argument read as circular

**ASN-0047, *Decomposition of K.μ~*, Step (A)/Step (B)**: Step (A) derives subspace preservation "from admissibility (i)'s stipulated S3★(Σ')"; Step (B) is titled "Mechanical realisation of admissibility (i)'s stipulated S3★(Σ') by the K.μ⁻ + K.μ⁺ decomposition," consuming Step (A).

**Problem**: As written, S3★(Σ') is both the assumption that drives Step (A) (subspace preservation) and the conclusion Step (B) claims to "realise." A reader following the chain sees S3★(Σ') used to prove subspace preservation, then subspace preservation used to "realise" S3★(Σ') — i.e., S3★ from S3★. The intended (and defensible) content is different: admissibility *filters* π so that S3★(Σ') holds by construction, and Step (B) actually establishes *realisability of the admissible π by the decomposition*, not S3★ itself. The structural-slot naming obscures which proposition is input and which is output.

**Required**: Retitle Step (B) to state its real obligation ("the K.μ⁻ + K.μ⁺ full-clearance decomposition realises any admissible π"), and state once, plainly, that S3★(Σ') for K.μ~ holds *by the admissibility filter* (so the matrix cell is true by definition), with Steps (A)/(B) supplying only the realisability that K.μ~ is a non-vacuous operation. Remove the framing that presents S3★(Σ') as a derived output of the decomposition.

### Issue 2: Asymmetric, unjustified permanence of link-subspace depth versus content-subspace depth

**ASN-0047, LinkVPositionDepthAxiom**: "each document `d` has a fixed link-subspace V-position depth `m_L(d) ≥ 2` ... determined at the first link-subspace insertion and unchanged thereafter."

**Problem**: The content subspace gets no analogous permanence axiom — content depth is supplied per-insertion by ValidFirstInsertionPosition (ASN-0036), which admits any `m ≥ 2` and does not fix it across an empty interval. After K.μ⁻ empties `V_{s_C}(d)` and K.μ⁺ re-inserts, content depth may change; link depth may not. No stated per-state invariant (S8-depth is per-state; CL-OWN/CL-UNIQ/D-* do not mention depth) requires `m_L(d)` to persist across an empty link subspace, so the "unchanged thereafter" clause is either over-specification or it conceals a load-bearing requirement that content equally needs. The ASN does not explain why links require cross-state depth fixity and content does not.

**Required**: Either (a) justify the asymmetry by naming the invariant that forces link-depth permanence but exempts content, or (b) weaken the axiom to per-non-empty-interval fixity matching the content treatment (parallel to ValidFirstInsertionPosition), or (c) add the content analog if permanence is genuinely intended for both.

### Issue 3: Axiom prose explains *why the axiom is needed* rather than *what it says*

**ASN-0047, LinkVPositionDepthAxiom, NodeUniqueAllocation, NodeRegistryBootstrap**: e.g. LinkVPositionDepthAxiom carries "The axiom resolves the genuine underdetermination S8-depth leaves open ... is otherwise unconstrained ... The axiom does not fix `m_L(d)` to any particular value ..."; NodeRegistryBootstrap carries "The node-allocation registry is external to `Σ`; `n₀` enters at `Σ₀` rather than via a prior K.δ event."

**Problem**: This is exactly the anti-bloat pattern the note flags — sub-paragraphs of motivation/scope/rationale accreted around axiom statements. The motivation does not advance the axiom's content; a reader must skip past it to find the normative claim.

**Required**: Reduce each axiom to its statement plus at most one sentence of necessary scoping. Move the "why needed" essay content out of the axiom slot (or delete it — the necessity surfaces where the axiom is consumed).

### Issue 4: Definition enumerates downstream consumers (use-site inventory)

**ASN-0047, *Allocator hierarchy under documents*, "Sub-allocator names"**: "`A_doc(·)` is the family member named in the case-(a') discussion of `A_v(d)`'s parent allocator"; "`A_account(·)` is the family member cited in the K.δ case (ii) k = 2 sub-case A discharge below."

**Problem**: A definition's body inventories where the defined object is later used. This is meta-prose that rots as sections move and does not advance the definition's meaning; per the anti-bloat note, use-site inventories in definitional slots are a finding.

**Required**: State each sub-allocator's structure (anchor, first emission, emission rule, output level) and stop. Drop the "is the family member cited in X below" clauses.

### Issue 5: "Temporal scoping of J0" paragraph duplicates the composite-boundary matrix and re-derives by analogy

**ASN-0047, *Coupling and isolation*, "Temporal scoping of J0"**: "This transient failure is admissible under ValidComposite★, exactly parallel to P4★'s transient violation between K.μ⁺ and K.ρ in the analogous J1★ case ... The composite-boundary verification matrix in *Class (b)* below catalogues J0 in this scoping uniformly with J1★."

**Problem**: The same scoping fact is stated here and again in the Class (b) composite-boundary matrix and surrounding prose. Two locations in different sections assert the same content and cross-defer to each other ("catalogues J0 ... below"), the deferral pattern the note flags.

**Required**: State J0's composite-boundary scoping once (the matrix is the natural home) and delete the duplicate paragraph, or reduce it to a one-line pointer without re-deriving the J1★ analogy.

### Issue 6: Repeated forward deferrals for L / K.λ / K.μ⁺_L in *The state model*

**ASN-0047, *The state model***: `L` is named in Σ but its "substantive characterisation deferred to" *Link store and extended system state*; the same section is forward-referenced for K.λ, K.μ⁺_L, and the L-invariants in multiple separate sentences ("introduced later under...", "Sections preceding the link store's introduction read Σ with `L = ∅`").

**Problem**: Multiple paragraphs in the state-model section defer to the same single downstream location for the same object. The accumulated "introduced below / read with L = ∅ for now" scaffolding is forward-reference accretion.

**Required**: Introduce `L` and its dependents once at a single site; replace the scattered "deferred / introduced later / read with L = ∅" sentences with one statement of staging.

### Issue 7: K.μ⁺ precondition cites ASN-0036 D-CTG/D-MIN but describes the strengthened per-subspace form

**ASN-0047, K.μ⁺ (Elementary transitions), precondition**: "the resulting arrangement satisfies D-CTG (contiguity within each subspace, ASN-0036) and D-MIN (minimum position in each non-empty subspace, ASN-0036)."

**Problem**: ASN-0036's D-CTG/D-MIN are content-subspace (`V_1(d)`) forms with a link-subspace exemption; "within each subspace" / "each non-empty subspace" is the D-CTG★/D-MIN★ strengthening introduced *in this ASN*, not the ASN-0036 property cited. The citation attributes a per-subspace guarantee to a foundation that does not provide it at the elementary-definition site.

**Required**: Cite the local D-CTG★/D-MIN★ (or, if the unamended K.μ⁺ definition predates them, cite ASN-0036's content-subspace D-CTG/D-MIN without the "each subspace" wording and defer the per-subspace strengthening to the amendment).

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: The fork composite (J4) explicitly leaves a forked document's link subspace empty and notes that link inheritance "would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is correctly deferred and is new territory, not a defect.

### Topic 2: Concrete node-allocation registry protocol
**Why out of scope**: NodeUniqueAllocation/NodeRegistryBootstrap deliberately treat the registry as external to Σ; specifying its issuing protocol, persistence, and concurrency discipline belongs to a future ASN (the ASN's Open Questions already records this as the abstraction boundary).

VERDICT: REVISE
