# Review of ASN-0047

After detailed analysis of this substantial specification, I find the ASN to be comprehensive and structurally sound. The proofs are detailed, the verification matrix is exhaustive, and the worked examples concretely exercise the abstract definitions. I traced the major dependency chains (K.μ~ decomposition Steps A-E, FrontierEquivalence, Cross-document disjointness chain, ExtendedReachableStateInvariants induction, K.δ case (ii) sub-cases) and found them logically complete.

That said, several items warrant revision before this can be considered fully converged.

## REVISE

### Issue 1: P4 → P4★ supersession status under "stale" usage in coupling section

**ASN-0047, "Coupling and isolation" section**: The derivation of J1 explicitly proves it from the *requirement to preserve P4* (`Contains(Σ) ⊆ R`), and the P4 proof appears in full in this section. But later, the *Content-scoped containment and provenance* section notes "P4 is unsatisfiable for the unscoped relation once link-subspace mappings exist" and supersedes P4 with P4★.

**Problem**: The J1 derivation is presented as if P4 holds, but it doesn't in the extended state. A reader following the J1 derivation forward cannot tell whether the wp-style derivation re-runs for P4★/J1★ or whether the original derivation transfers automatically. The text says "the same induction discharges P4a in the extended state, with J1'★ replacing J1' as the coupling" — but does NOT explicitly say the J1 wp derivation re-runs with Contains_C instead of Contains.

**Required**: Add an explicit paragraph in the *Scoped coupling constraints* section showing that the J1 wp computation, re-run with the design choice "preserve P4★", yields J1★ — analogous to how J1 was derived from "preserve P4". Otherwise J1★ reads as a posited coupling rather than a derived one.

### Issue 2: K.μ⁺_L's omitted strict-extension verification

**ASN-0047, K.μ⁺_L (LinkSubspaceExtension)**: The effect is `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`.

**Problem**: K.μ⁺ has explicit `dom(M'(d)) ⊃ dom(M(d))` (strict extension) in its effect clause. K.μ⁺_L's effect is stated as union with a singleton, but the strict-extension property is only derivable from `v_ℓ ∉ dom(M(d))`, which is *verified* (in the body prose) but not asserted as part of K.μ⁺_L's effect clause directly. The K.μ⁺_L effect statement leaves it implicit.

**Required**: Either state the strict-extension explicitly (`dom(M'(d)) = dom(M(d)) ∪ {v_ℓ} ⊃ dom(M(d))`), or cite the in-body verification (`v_ℓ ∉ dom(M(d))` — verified at K.μ⁺_L) at the effect clause itself.

### Issue 3: K.μ~ existence condition's circular-looking dependency

**ASN-0047, K.μ~ Decomposition**: The precondition `|dom_C(M(d))| ≥ 2` is derived (in the Decomposition section) via Step (D)'s pointwise link-subspace fixity, which consumes CL-UNIQ at the pre-state. CL-UNIQ at the pre-state is a Class (a) invariant of ExtendedReachableStateInvariants, which is proved by induction over valid composites — composites that include K.μ~ events.

**Problem**: This reads circularly. The argument is sound (CL-UNIQ at Σ is the *prior* induction state, used to prove CL-UNIQ at Σ'), but the prose doesn't make the inductive separation explicit at the K.μ~ definition site. A reader could read the existence-condition derivation as proving a precondition using a property whose preservation is itself being proved.

**Required**: At the K.μ~ definition, explicitly note that the precondition `|dom_C(M(d))| ≥ 2` is well-formed because the operation is intended for reachable states where CL-UNIQ holds by inductive hypothesis. The current "the inductive hypothesis ... is what closes Step (4)" appears deep in the proof body but should also be flagged at the definition.

### Issue 4: K.μ⁻ precondition `dom(M(d)) ≠ ∅` placement

**ASN-0047, K.μ⁻ definition in Elementary transitions**: K.μ⁻ lists `dom(M(d)) ≠ ∅` as a precondition. But the "*Per-subspace consequence of the strict-contraction clause*" paragraph in the K.μ⁻ amendment derives this same condition from "at least one S admitting strict contraction" + the empty-arrangement boundary discussion.

**Problem**: The precondition is stated twice — once explicitly at K.μ⁻'s definition, once as a derived consequence in the amendment. The relationship between these two statements isn't clear: is one a redundant restatement, or is the explicit statement load-bearing while the amendment's derivation is illustrative?

**Required**: Clarify that the explicit `dom(M(d)) ≠ ∅` precondition is the load-bearing form (verified at firing), and the amendment's "Per-subspace consequence" paragraph re-derives the same condition under the constructive shape characterization — not a separate obligation.

### Issue 5: J0 transient-failure handling vs J0's "design intent" framing

**ASN-0047, J0**: Stated as an axiom: "Content allocation K.α always co-occurs with arrangement extension K.μ⁺." The justification is design intent (Nelson, Gregory).

**Problem**: At an intermediate state after K.α but before K.μ⁺, J0 is genuinely violated (a is in dom(C) but no V-position maps to it). The composite-boundary discharge restores it. But unlike P4a (where the Class (b) treatment is explicit), J0's treatment in the verification matrix is implicit — J0 is listed as a coupling, but its temporal scoping (composite-boundary, not per-state) is not stated as crisply as P4★/P4a/P7a.

**Required**: Either (a) explicitly list J0 alongside J1★/J1'★ in the *composite-boundary* verification structure, with explicit transient-failure semantics; or (b) add a sentence at J0's definition clarifying that J0 binds initial-to-final states under ValidComposite★ rather than at each intermediate state.

### Issue 6: Worked example traces don't verify L11a explicitly

**ASN-0047, worked examples**: Multiple examples invoke K.λ but don't trace L11a (Link distinctness) discharge in the per-step verification, beyond noting "preserved by L12" or citing the matrix.

**Problem**: L11a (link-address uniqueness from distinct K.λ events) is a derived obligation listed in the verification matrix. The worked examples exercise K.λ in concrete cases (Step 1 of "link allocation and arrangement"; Step 4's second K.λ on ℓ₂), but the per-step verification doesn't explicitly check L11a's two routes (SubAllocatorAxiom.FirstEmission for first link, T10a GlobalUniqueness for subsequent). This is at odds with the matrix's treatment of distinctness obligations.

**Required**: In the "link allocation and arrangement" worked example, add an explicit L11a discharge for the first K.λ (citing FirstEmission) and the second K.λ on ℓ₂ (citing GlobalUniqueness on the inc chain).

### Issue 7: K.μ~ singleton case necessity argument leaves a gap

**ASN-0047, K.μ~ Decomposition, "Decomposition" paragraph**: The argument for necessity at `|dom_C(M(d))| = 1`: "The singleton case `|dom_C(M(d))| = 1` admits only the identity permutation on `dom_C`, and link-subspace fixity forces `π|_{dom_L} = id`, so π = id, violating (ii)."

**Problem**: This argument uses link-subspace fixity (Step D), which depends on CL-UNIQ at the pre-state — already noted in Issue 3. But more subtly: the necessity argument assumes link-subspace fixity *applies* to a candidate π. If `|dom_C(M(d))| = 1` and we hypothesize some π for K.μ~, must that π satisfy link-subspace fixity? Only if it's admissible. The "necessity" direction needs to show: for ANY admissible π, `|dom_C(M(d))| ≥ 2`. The argument is correct but the quantifier structure could be cleaner.

**Required**: Restructure the necessity argument as: "Suppose K.μ~ admits some π. Then π satisfies admissibility (i) and (ii). By Step (D)'s derivation (which requires CL-UNIQ at the inductive pre-state), π|_{dom_L} = id. With π ≠ id and subspace preservation, π must be a non-identity permutation on dom_C. Such a permutation exists only if |dom_C| ≥ 2."

## OUT_OF_SCOPE

### Topic 1: Concurrent K.α / K.λ on shared documents
Listed correctly as an Open Question.

### Topic 2: Node-allocation registry protocol mechanism
Correctly delegated to NodeUniqueAllocation/NodeRegistryBootstrap as axiomatic; mechanism is out of scope.

### Topic 3: Link withdrawal beyond suffix truncation (tombstoning reconciliation)
Listed correctly as an Open Question, with appropriate justification of the architectural cost.

### Topic 4: Account-level depth-1 tumbler extension
Correctly identified as an Open Question.

VERDICT: REVISE
