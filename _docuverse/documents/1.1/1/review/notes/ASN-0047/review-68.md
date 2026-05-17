# Review of ASN-0047

## REVISE

### Issue 1: K.μ⁺_L's "S8" verification incorrectly extends ASN-0036's S8 to the link subspace

**ASN-0047, "Per-subspace arrangement invariants under K.μ⁺_L"**: "S8 (SpanDecomposition): S8's quantifier `v₁ ≥ 1` captures all V-positions in the extended state — since both `s_C ≥ 1` and `s_L ≥ 1` (established above for S8a) — extending coverage to the link subspace. S8 is derived from S8-fin, S8a, S2, and S8-depth (ASN-0036), all verified above."

**Problem**: ASN-0036's S8 lists `referential integrity (S3)`, `zeros(a) = 3 (S7b)`, and `#E(a) ≥ 2 (S7c)` as preconditions — all content-store-specific. Link-subspace V-positions target dom(L), violating S3 directly. The "derived from S8-fin, S8a, S2, and S8-depth" enumeration silently omits the missing S3/S7b/S7c. The correct treatment appears later in the "S8-scope in the extended state" note inside ExtendedReachableStateInvariants, where S8 is restricted to the content-subspace projection and the link-subspace analog is established separately via D-CTG★/D-MIN★/D-SEQ★. The K.μ⁺_L section's claim contradicts that scoping.

**Required**: Rewrite the K.μ⁺_L S8 verification to either (a) cite only the projection-to-content-subspace version of S8 plus the per-subspace D-SEQ★ for the link subspace, matching the treatment in "S8-scope in the extended state", or (b) explicitly justify why S3/S7b/S7c can be dropped when projecting to the link subspace (which would require articulating the link-subspace analog `S3★-link → dom(L)`).

### Issue 2: K.δ effect for IsNode case lacks explicit M-clause

**ASN-0047, "K.δ (Entity creation)"**: "When IsDocument(e): M'(e) = ∅ (empty arrangement)."

**Problem**: The effect is stated only for the IsDocument case. For IsNode(e) and IsAccount(e), the prose is silent on M. The reader must infer from the frame clause `(A d' :: M'(d') = M(d'))` plus the totality convention `M(e) = ∅ for e ∉ E_doc` that M is unchanged. This is correct but requires the reader to reconstruct the argument from two scattered facts. K.δ for nodes and accounts could leave the question "does M get a new empty entry at the new e?" unanswered; the frame says no, but the IsDocument-only effect clause invites confusion.

**Required**: State explicitly in the effect that for IsNode(e) and IsAccount(e), M is unchanged (frame), and explain why the IsDocument case needs separate mention (because totality+frame would also give M(e)=∅ for documents, but the *semantic activation* of e as a document-arrangement target is what the effect clause records).

### Issue 3: ExtendedReachableStateInvariants per-state list omits P4a

**ASN-0047, "ExtendedReachableStateInvariants (per-state)"**: The conjunction lists S2 ∧ S3★ ∧ ... ∧ P4★ ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ NodeLineage ∧ ... but does not list P4a (HistoricalFidelity).

**Problem**: P4a is introduced in the body as a per-state property ("Every entry in R reflects an actual past content-subspace containment event") and is given a full inductive derivation. It belongs in the per-state invariant catalogue alongside P4★/P7/P7a. Omitting it from the ExtendedReachableStateInvariants conjunct list leaves it as an unstated theorem floating in the body — its preservation under each transition is implicit but not enumerated, and a future ASN that builds on this one cannot cite it as part of the named invariant set.

**Required**: Add P4a to the ExtendedReachableStateInvariants per-state conjunction, and add a one-paragraph elementary case analysis in the proof showing each transition preserves it (or invoke the existing derivation that uses P2 + J1'★).

### Issue 4: "Per-state arrangement shape (D-SEQ★)" forward pointer relies on a circularity disclaimer that doesn't fully discharge

**ASN-0047, "Per-state arrangement shape (D-SEQ★)"**: "D-SEQ★ is the per-state invariant stated in *Per-state arrangement shape (D-SEQ★)* immediately above and derived in full below... The K.μ⁻ case analysis treats the D-SEQ★-shaped pre-state as a structural input assumption discharged by D-SEQ★'s per-state guarantee."

**Problem**: D-SEQ★ is forward-referenced in the K.μ⁻ admissibility precondition before being derived in the "Amendments" section. The disclaimer says "the D-SEQ★ derivation below reads its hypotheses from invariants K.μ⁻ either preserves or has frame on" — but D-SEQ★'s derivation uses D-CTG★ and D-MIN★, which K.μ⁻ is itself responsible for preserving via the postcondition. The induction structure is: at the pre-state Σ, D-SEQ★ holds (by inductive hypothesis); K.μ⁻ uses D-SEQ★ at Σ in its admissibility precondition; the post-state must satisfy D-CTG★/D-MIN★ which (via D-SEQ★'s derivation) gives D-SEQ★ at Σ'. This is the standard pattern, but the disclaimer doesn't explicitly note the inductive structure that breaks circularity.

**Required**: Rewrite the disclaimer to explicitly invoke the inductive structure: "D-SEQ★ at the pre-state Σ holds by the ExtendedReachableStateInvariants inductive hypothesis at the prior step; K.μ⁻'s admissibility precondition consumes this pre-state shape; K.μ⁻'s D-CTG★/D-MIN★ postcondition (together with S8-fin/S8-depth/S8a frame-preserved or postconditioned) then re-derives D-SEQ★ at the post-state via the same Step 1/Step 2 argument of the Amendments section."

### Issue 5: K.μ~ contract's "subspace-preserving" admissibility constraint is asserted but not derived

**ASN-0047, "K.μ~ — contract"**: "*Admissibility constraints.* π is subspace-preserving — `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))`..."

**Problem**: Subspace-preservation is stated as an admissibility constraint imposed externally on K.μ~. But it should be derivable from the bijection equation + S3★ + L14, similarly to how link-subspace identity is derived. If `M'(d)(π(v)) = M(d)(v)` and v is content-subspace (so M(d)(v) ∈ dom(C) by S3★), then M'(d)(π(v)) ∈ dom(C). By S3★ at the post-state, this means subspace(π(v)) = s_C. Symmetrically for link-subspace v. So subspace-preservation follows from the bijection equation + pre/post-state S3★ + L14.

If subspace-preservation is truly an independent admissibility constraint (not derivable), the proof of invariant preservation cannot use the bijection equation alone — it needs both. The current text takes subspace-preservation as primitive without explaining why it isn't derived; the link-subspace fixity derivation that follows uses S3★+L14+CL-UNIQ in a similar style, raising the question of why subspace-preservation gets axiomatic status while link-fixity gets derived.

**Required**: Either (a) derive subspace-preservation as a consequence of the bijection equation + pre-state and post-state S3★ + L14 (matching the link-fixity derivation pattern), removing it from the admissibility constraint list; or (b) explain why subspace-preservation must be imposed as a constraint while link-fixity can be derived (the asymmetric treatment is suspicious without justification).

### Issue 6: Bootstrap node n₀'s structural specification has minor inconsistency

**ASN-0047, "Definition (Initial state)" and "Structural form of n₀"**: "E₀ = {n₀} where n₀ = `[1]`... The bootstrap node is fixed as the single-component tumbler `[1]`."

**Problem**: The "Structural form of n₀" paragraph spends substantial prose justifying `n₀ = [1]` via Nelson and Gregory. But then K.δ case (i) (Node baptism) admits multi-component nodes like `[1, 2]` via NodeUniqueAllocation+NodeLineage. The relationship between "the bootstrap is `[1]` specifically" and "all subsequent nodes descend from `[1]` by prefix" is correctly stated, but the load-bearing role of the specific choice `[1]` (vs. any single-component positive tumbler `[c]` with c ≥ 1) is overstated. Any single-component positive tumbler would serve as `n₀` equivalently for the formal model; the consultation evidence pins it to `[1]` by convention, not by formal necessity. The "single-component" structural property is what matters; the value `1` is conventional.

**Required**: Clarify that `n₀ = [1]` is a convention pinning a specific value (per Nelson LM 4/28 and Gregory's granfilade), and that the formal model would admit any single-component positive `n₀` provided NodeLineage's `n₀ ≼ e` is interpreted consistently. Or: tighten the argument to explain why specifically `[1]` (not `[5]` or `[42]`) is structurally load-bearing — perhaps via the "first allocator from nothing" pattern.

### Issue 7: P3 vs P3★ historical separation is unclear

**ASN-0047, "P3 (Arrangement as sole locus of destructive change)" and "P3★ (ArrangementMutabilityOnly, extended)"**: P3 is stated qualitatively without value-preservation; P3★ adds value-preservation conjuncts and L.

**Problem**: P3 as introduced in the four-component-state section is a "qualitative claim about which components admit which mutability modes" — but the prose for P3 also says C, E, R "admit only extensions" which sounds like a quantitative claim. The split between qualitative P3 and quantitative P3★ is hard to read because P3 itself seems to claim more than "names of modes." The P3★ definition is then a strengthening that adds explicit value-preservation. The asymmetry between P3 ("qualitative") and P3★ ("synthesizes P0 ∧ L12 ∧ P1 ∧ P2") suggests P3 is doing less work than its statement implies.

**Required**: Either (a) tighten P3 to be genuinely qualitative (just naming the three mutability modes available to M, without claiming domain-inclusion or value-preservation for other components — those go to P0/P1/P2), or (b) drop P3 entirely and let P3★ stand as the single statement, since P3 alone is never cited downstream as load-bearing. Currently P3 floats as a half-formal claim that P3★ supersedes.

### Issue 8: K.δ k=1 ghost-base discussion is excessively long and obscures the proof structure

**ASN-0047, "*Scope, base-liveness, and discharge of `e ∉ E` in the ghost-operand case*"**: This subsection runs approximately 1000 words and includes multiple cross-references, implementation citations, and meta-commentary about deferred semantics.

**Problem**: The technical content (admit ghost-base k=1 versioning; require live-base for k=0; freshness discharge routes through K.δ precondition + TA5) is buried under extensive design-rationale prose, implementation-evidence citations, and discussion of position (a)/(b)/(c) choices. The key formal claim — `e ∉ E` is discharged by inspection of E plus TA5 determinism on the candidate — is correct but appears as one sentence amid pages of justification.

**Required**: Tighten to the formal content: (i) precondition list including `IsDocument(t)` for k=1 without requiring `t ∈ E`; (ii) discharge mechanism (K.δ precondition + TA5); (iii) one-paragraph justification citing Nelson LM 4/23. Move the implementation-evidence discussion (Gregory's `docreatenewversion` ordering bug, leaked granfilade slots) to either a separate "Implementation correspondence" note or to consultation answers. Move the "three positions" meta-discussion to a deferred-questions cross-reference. The current prose density risks burying the technical claim.

### Issue 9: Worked examples are useful but their cross-referencing is fragmentary

**ASN-0047, three worked examples**: "Worked example: fork with subsequent insertion", "Worked example: interior content replacement", "Worked example: link allocation and arrangement", "Worked example: ghost-base document versioning", "Worked example: node baptism under the bootstrap root".

**Problem**: The five worked examples exercise different transitions and invariants but lack a coordinating map showing which example covers which invariant. The verification lines within each example name many invariants but it's unclear from outside any given example which are exercised non-vacuously vs. frame-preserved. The link allocation example includes a coverage statement ("Invariants exercised *directly*... Invariants exercised *only as frame-preserved*...") but the other examples do not. Result: a reader checking whether invariant X has been concretely exercised must scan all five examples.

**Required**: Add a coordinating table at the top of the worked-examples section listing (rows: invariants; columns: examples; cells: directly-exercised / frame-preserved / vacuous / not-covered). Or: add the same "Invariants exercised directly / Invariants exercised only as frame-preserved" coverage statement to each worked example, matching the link-allocation example's format.

## OUT_OF_SCOPE

### Topic 1: Withdrawal mechanism for interior link-subspace positions
The ASN correctly identifies (Issue F in "Structural sufficiency and known gaps") that tombstone-style link withdrawal at interior positions is not expressible under D-CTG★/D-MIN★. The mechanism requires a state-model extension (status flag, tombstone marker, retraction link). This is deferred to a future ASN.

**Why out of scope**: The ASN explicitly identifies this as a named gap and defers it to a withdrawal-invariants ASN. The current model's constraints are correctly stated; expanding the state model to support tombstoning is a different scope.

### Topic 2: Version-management semantics beyond the K.δ k=1 structural admissibility
The ASN admits ghost-base versioning at the K.δ elementary level but defers version-lineage semantics (arrangement-transition invariants between versions, content-allocator linkage, provenance flow, acyclicity).

**Why out of scope**: This is correctly listed in Open Questions; comprehensive version semantics belongs to a subsequent version-management ASN.

### Topic 3: Account-level k=1 (depth-1 tumbler extension at the account level)
The ASN excludes IsAccount(t) from the k=1 sub-case of K.δ, citing absent design semantics for "account versions."

**Why out of scope**: This is a deliberate scope exclusion correctly justified by the absence of documented design intent. Admitting it would require new "account version" semantics, which belong to a separate design proposal.

### Topic 4: Non-T10a allocators
The elementary set assumes T10a-conforming allocation for content, links, and non-node entities, with NodeUniqueAllocation as the named protocol exception for nodes.

**Why out of scope**: Correctly deferred; admitting non-T10a allocators requires extending the freshness-discharge framework, which is a substantial new ASN.

VERDICT: REVISE
