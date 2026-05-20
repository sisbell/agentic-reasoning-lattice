# Review of ASN-0094

## REVISE

### Issue 1: Coverage cardinality formulation is mathematically broken
**ASN-0094, Definition — Conformance**: "`match(|coverage(F)|, c_F) ∧ match(|coverage(G)|, c_G) ∧ coverage(F) ⊆ t_F ∧ coverage(G) ⊆ t_G`"

**Problem**: By ASN-0043's coverage definition together with PrefixSpanCoverage, `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`. By T0(a) and T0(b) (ASN-0034), this set is infinite. So `|coverage(F)|` is infinite for every non-empty canonical-form F, and `match(|coverage(F)|, 1)` is never satisfied. Identically, `coverage(F) ⊆ A_doc` is unsatisfiable because `coverage(F)` contains infinitely many tumblers that are not document addresses.

The Convention CanonicalSlotForm tries to repair this by redefining `|coverage(F)|` to mean "the count of allocated addresses denoted." But the formal statements of Sh0–Sh3 and Sh-conf use the standard set-cardinality operator. Quietly re-interpreting `|·|` in prose, while the formal definitions read mathematically, is fragile.

**Required**: Either (a) introduce an explicit operator like `cov_allocated(F, Σ) := coverage(F) ∩ A^Σ` and restate Sh-conf, Sh0–Sh3, and the slot-accessor definitions in terms of `|cov_allocated(F, Σ)|`; or (b) check conformance syntactically against F's span structure (single-canonical-span form) rather than against coverage cardinality. Whichever is chosen, address the state-dependence introduced: under (a), conformance may become a moving target as allocation grows; under (b), the relationship between syntactic conformance and the address-set guarantees needs explicit proof.

### Issue 2: Nullify under Retraction shape fails Sh-conf
**ASN-0094, Canonical Shape Catalog, Retraction row**: `t_G = A_rel`

**Problem**: ASN-0086 defines `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`. Under the formal definitions, `coverage({(a, δ(1, #a))}) = {t : a ≼ t}` includes every tumbler extending `a`, the vast majority of which lie outside `dom(Σ.L) = A_rel`. So `coverage(G) ⊆ A_rel` fails on the very call that ASN-0086 specifies as the only producer of R-tuples under the relational-layer commitment. The conformance axiom rejects the substrate's own retraction primitive.

**Required**: This is the same root cause as Issue 1, but worth flagging specifically: any fix to coverage interpretation must demonstrably admit Nullify. Show that under the chosen interpretation, the canonical Nullify call is conformant for the Retraction shape.

### Issue 3: Sh0–Sh3 induction handles only `→`, not `↦`
**ASN-0094, Proof of Sh0**: "By induction on the state Σ. ... Inductive step. Suppose the property holds at Σ, and let `Σ → Σ'` be a state transition."

**Problem**: ASN-0086 defines two transition relations: `→` (dom-extending) and `↦` (broader, including arrangement-modifying steps). Reachable states are reachable under `↦*`, not just `→*`. The induction as written says nothing about arrangement-modifying transitions in `↦ \ →`. The conclusion "holds at every reachable Σ" therefore does not follow directly.

The remedy is one extra inductive case citing LinkStoreInvarianceUnderArrangement (`Σ'.L = Σ.L`, hence `L_K^{Σ'} = L_K^Σ`, hence preservation is trivial). But the proof must show this step explicitly; "by similar reasoning" is not adequate.

**Required**: Extend each of Sh0–Sh3's inductive step to cover both transition classes, with the arrangement-modifying case discharged via LinkStoreInvarianceUnderArrangement.

### Issue 4: Coverage template's `emission_order` is not defined cross-allocator
**ASN-0094, Coverage walkthrough**: "`latest_K_for_addr(d) ≡ argmax_{τ ∈ S_d} emission_order(τ)` ... depends on a total ordering on tuples — typically by tuple-address allocation order, which is monotone in emission time under T9 (ForwardAllocation, ASN-0034)."

**Problem**: T9 establishes ordering only within a single allocator's chain (`same_allocator(a, b) ∧ allocated_before(a, b) ⟹ a < b`). A Coverage tuple `τ` with `to₁(τ) = d` has `addr(τ)` in `A_L(home(τ))`'s chain. Two Coverage tuples targeting the same `d` typically have different `home(τ)` values (the layer emitting Coverage need not always emit from the same home document). Their tuple addresses then belong to different sub-allocators (with prefix-incomparable bases by CrossDocDisjointness), so T9 does not order them. The template's `argmax` is undefined when `S_d` spans multiple allocators.

T1 (LexicographicOrder) supplies a total order on all tumblers, but T1's order is unrelated to emission time across allocators — a smaller T1-address could be allocated later in wall-clock time.

**Required**: Either (a) define `emission_order` explicitly with cross-allocator semantics (e.g., a substrate-level global counter, or a partial order that admits ties), and prove its existence; (b) restrict Coverage relations to single-home emission and document the constraint; or (c) acknowledge that Coverage requires layer-supplied ordering and state Sh5's mechanical-derivability claim only modulo that.

### Issue 5: Sh4 is policy but K_sidecar_of's totality depends on it
**ASN-0094, Sh4**: "*Status.* Sh4 is a policy, not a substrate-enforced axiom."

**ASN-0094, Attribute walkthrough**: "`K_sidecar_of(d) ≡ to₁(τ)` where τ is the unique element of `{τ ∈ A_K^Σ : from₁(τ) = d}` (uniqueness by Sh4)"

**Problem**: `K_sidecar_of` is presented as a value-returning predicate, but its definition uses "the unique element," which presupposes a singleton candidate set. The singleton property is established only by Sh4. If Sh4 is a non-enforced policy, then `K_sidecar_of` is not a substrate-level function; it is a function only on layers that happen to enforce Sh4 correctly. The same issue affects any template using a Sh4-uniqueness argument (this is the only one in the catalog, but Sh5's generation of new Attribute-shape templates would carry the same defect).

The walkthrough then claims "*Slot accessors are total on the relevant slots*." For point accessors on `(1, 1)` shapes, totality follows from Sh0/Sh1. But for "the unique active tuple at d," totality depends on Sh4, which is not enforced.

**Required**: Either (a) elevate Sh4 to a substrate-enforced axiom (Emit_K rejects a coverage-duplicate emission for idempotent K); or (b) restate `K_sidecar_of` as `arbitrary_K_sidecar_of(d)` returning some element of the candidate set, or as a set-valued accessor returning the candidate set itself; or (c) make every template that consumes Sh4 explicitly conditional on the policy holding, and acknowledge that template behavior under policy violation is layer-defined.

### Issue 6: `T_cat` is referenced but never defined
**ASN-0094, Definition — ShapeRegistry**: "`shape : T_cat → Shape`"

**Problem**: `T_cat` appears in the registry signature and in every per-type universal quantifier (Sh0–Sh3) but is never defined. Possible readings: (i) `T_cat = T_admissible` (every admissible type has a shape); (ii) `T_cat = T_admissible / ~` (one shape per coverage class); (iii) `T_cat ⊊ T_admissible` is the registered subset (relations the substrate admits via shape); (iv) `T_cat` is a finite indexing set with type-names. Each reading affects what Sh-conf rejects (an unregistered type? a non-conformant type?) and what Sh0–Sh3 quantify over.

**Required**: Define `T_cat` explicitly. State its relationship to `T_admissible` and `T_admissible / ~`. State what happens when `Emit_K` is called with a `K ∉ T_cat` (rejected? admitted with a default shape?).

### Issue 7: Shape registry mutability is unspecified
**ASN-0094, Open Questions**: "What guarantees the shape registry stays consistent across processes?"

**Problem**: The ASN treats shape registration as a one-time act ("Registering a new K in T_cat requires registering its shape") but does not say whether the registry can change at runtime. If `shape(K)` is mutable, then a prior-emitted tuple of type K that satisfied `shape(K) = Σ_1` may not satisfy `shape(K) = Σ_2` after re-registration. Sh-conf's inductive preservation argument tacitly assumes the registry is constant on the timeline of state transitions; this should be axiomatic, not implicit. The Open Questions raise this but do not resolve it.

**Required**: State explicitly that `shape` is constant across the system's lifetime (or, if mutable, the conditions under which re-registration is permitted and the obligations on prior tuples). Strengthen the inductive arguments of Sh0–Sh3 to cite registry constancy as a premise.

### Issue 8: `K_is_fresh` violates Sh5's mechanical-derivability claim
**ASN-0094, Sh5**: "the predicates `{tpl[K] : tpl ∈ Tpl(Σ_canon)}` are mechanically derivable from K's shape and name alone."

**ASN-0094, Attribute walkthrough**: "`K_is_fresh(d) ≡ has_K(d) ∧ mtime(K_sidecar_of(d)) ≥ mtime(d)` ... It is the only template here that depends on data outside the relational structure, and its instantiation requires the user-specified `mtime` accessor in addition to K's name."

**Problem**: Sh5 claims templates derive from K's shape and name alone. `K_is_fresh` requires an external `mtime` accessor. The ASN acknowledges the discrepancy in prose but does not amend Sh5. Either `K_is_fresh` is in the Attribute template family (and Sh5's claim is wrong) or it isn't (and the walkthrough is misleading about what Sh5 generates).

**Required**: Pick one: (a) remove `K_is_fresh` from the Attribute family and present it as a layer-level composite atop the substrate templates; or (b) generalize Sh5 to allow templates parameterized by externally registered accessors, list `mtime` as one such accessor, and update the derivability claim accordingly.

### Issue 9: `latest_K_for_addr(d)` is partial on empty `S_d`
**ASN-0094, Coverage walkthrough**: "`latest_K_for_addr(d) ≡ argmax_{τ ∈ S_d} emission_order(τ)` where `S_d = {τ ∈ A_K^Σ : to₁(τ) = d}`"

**Problem**: When `S_d = ∅` (no Coverage tuple has yet targeted `d`), `argmax` over the empty set is undefined. The template offers no convention for this case. Predicates of "what's the latest coverage of d?" returning `⊥` is the only sensible answer, but the template should say so. The same gap also exists for other partial-template scenarios (e.g., `to₁⁻` is acknowledged optional, but `latest_K_for_addr` is presented as if total).

**Required**: Make the optionality explicit: `latest_K_for_addr : A_doc → A_rel ∪ {⊥}` with the empty-`S_d` case returning `⊥`. Audit other templates for similar gaps.

### Issue 10: The "typical case" of no allocated descendants is a load-bearing theorem, not a remark
**ASN-0094, Convention CanonicalSlotForm**: "For element-level addresses with no allocated descendants (the typical case), the intersection is the singleton `{x}`."

**Problem**: The entire cardinality framework rests on the property that an element-level address `x` has at most one allocated address in `{t : x ≼ t}` — namely `x` itself. This is a consequence of antichain properties (R0a for links, the analogous content-side property from ASN-0093's chain enumeration). Calling it "the typical case" suggests it is sometimes false, in which case Sh-conf preservation is in jeopardy. If it is always true (modulo subspace), it is a theorem and should be stated and proved.

**Required**: State the property as a lemma — "For every `Σ` and every element-level `x ∈ A^Σ`, `coverage({(x, δ(1, #x))}) ∩ A^Σ = {x}`" — and prove it from R0a together with the corresponding content-side antichain (cited from foundations or from this ASN's substrate-conformance discipline). Cite this lemma at the point Sh0/Sh1 needs it.

### Issue 11: Sh5 is a proof sketch with no derivation procedure
**ASN-0094, Sh5 Proof sketch**: "Each template body is expressed in terms of (i) slot accessors ... (ii) target-domain typing ... (iii) the active-subset view ... (iv) the existential and universal quantifiers ..."

**Problem**: Sh5 claims templates are "mechanically derivable." A mechanical derivation is an algorithm — input a shape, output a template family. The proof sketch enumerates the ingredients but does not exhibit the algorithm. The walkthrough catalog shows templates per shape, but it is unclear whether the catalog is generated by a procedure or hand-curated to match observed need. The bipartite-coverage discussion ("further bipartite entries can be added without changing the framework") suggests hand-curation.

**Required**: Either (a) exhibit the derivation procedure (templates as functions of shape components — "if `c_F = 1` and `c_G = 1`, generate `cites_K(a, b) ≡ ...`"); or (b) downgrade Sh5 from LEMMA to META, stating that "templates are written by hand against the canonical shape catalog" rather than claiming mechanical derivability.

### Issue 12: No concrete worked example
**ASN-0094 overall**

**Problem**: The standards in this review process require a concrete example. The ASN exhibits canonical shapes and templates abstractly but never picks a specific K, registers its shape, and walks through Sh-conf, Sh0–Sh3, and a predicate evaluation against a specific Σ. Without an example, the framework's edge cases (empty store, post-retraction state, cross-allocator emission, ghost-address targeting) are not verified.

**Required**: Add a worked example — pick `K = comment` with the Comment shape, exhibit two specific tuples `τ_1, τ_2` in `L_K^Σ`, verify Sh0–Sh3 hold by direct check, evaluate `unresolved_K_comments(d)` against a specific `d`, and verify `all_K_resolved(d)` flips when a Resolution tuple is emitted.

### Issue 13: Open Questions include items that are this ASN's responsibility
**ASN-0094, Open Questions, items 6 and 8**: "must `emission_order` be a substrate-level guarantee...?" and "Do shape constraints commute with retraction?"

**Problem**: Item 6 is Issue 4 of this review — the Coverage template uses `emission_order` without defining it cross-allocator. Item 8 is closely tied to Issue 3 and Sh-conf's preservation properties — if retraction can change `A_K^Σ`, does conformance still hold for the post-retraction active subset? These are not future ASNs' problems; they affect whether the templates exhibited in this ASN evaluate correctly.

**Required**: Resolve items 6 and 8 in this ASN. Future-work items in the Open Questions list should be ones that the present framework demonstrably works without — composite shapes, `(0, 0)` admissibility, idempotency-independence are legitimate future questions; the two flagged here are not.

## OUT_OF_SCOPE

### Topic 1: Composite shapes (relations whose F or G is constrained by another relation's content)
**Why out of scope**: Open Question 5 raises whether composite shapes need a new axis. This is genuinely future territory — the present framework expresses primitive shapes only, and composition through predicates is described as adequate for current needs. A future ASN can introduce composite shapes when a concrete use case demands them.

### Topic 2: Admission of `(0, 0)` shapes
**Why out of scope**: Open Question 1. Whether single-tuple existence flags warrant a canonical shape is genuinely a future design question. No template family currently demands it.

### Topic 3: Whether idempotency is derivable from cardinality and target-domain
**Why out of scope**: Open Question 3. The empirical catalog gives shapes with identical (cardinality, target-domain) and different idempotency (Comment vs Citation), so independence is the working hypothesis. A future ASN may revisit if a structural reason for the choice emerges.

VERDICT: REVISE
