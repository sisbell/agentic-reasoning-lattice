# Review of ASN-0076

## REVISE

### Issue 1: E0's composite precondition omits the reachability hypothesis the proof depends on

**ASN-0076, E0 (Precondition block + Invariant inheritance paragraph)**: The composite precondition lists only `ℓ_old ∈ dom(Σ.L)`, `d_new ∈ E_doc`, `N ≥ 3`, the endset conditions, and `τ_sup ∈ T`. The invariant-inheritance paragraph then concludes "by ExtendedReachableStateInvariants (ASN-0047) every per-state invariant ... continues to hold at the post-state."

**Problem**: ExtendedReachableStateInvariants applies only to states "reachable from Σ₀ by a finite sequence ... drawn from valid composites." To conclude `Σ'` satisfies the per-state invariants you need `Σ` reachable (then `Σ'` is reachable since EDITLINK is a valid composite). The precondition never asserts this. Worse, the K.λ precondition discharges *themselves* lean on per-state facts at `Σ` — SubAllocatorBundle presumes the entity-allocation event that activated `A_L(d_new)` actually occurred, and L0 ("every `a ∈ dom(Σ.C)` has `subspace_I(a) = s_C`," used to derive `ℓ_new ∉ dom(Σ.C)`) is a per-state invariant. Both presuppose `Σ` is a reachable/invariant-satisfying state. E5 correctly carries this as an explicit "outer hypothesis"; E0 does not, and the two are inconsistent.

**Required**: Add to E0's composite precondition that `Σ` is a reachable state of ASN-0047's extended reachable state (equivalently, satisfies the extended reachable-state invariants), matching E5's outer hypothesis — or state the invariant-inheritance conclusion as conditional on `Σ` reachable.

### Issue 2: τ_sup paragraph is deferral meta-prose

**ASN-0076, "The Composite" (τ_sup bullet)**: "Whether `τ_sup` lies in `dom(C)`, `dom(L)`, or neither — whether it is element-level, document-level, or in some dedicated subspace — is not constrained by the link model. EDITLINK simply records the caller's chosen address. The convention by which a reader recognizes `τ_sup` ... is external to the link model and deferred to a future ASN on type-endset conventions (Open Questions)."

**Problem**: This is meta-prose enumerating what is *not* constrained and forwarding to a future ASN. The single load-bearing fact — `τ_sup ∈ T` suffices for span well-formedness — is already stated in the preceding sentence and re-proved in E0. The remainder explains scope rather than advancing the argument, and the same convention is already listed in Open Questions.

**Required**: Reduce to the operative statement (`τ_sup ∈ T`; the span is well-formed by T12 via T0). Drop the not-constrained enumeration and the future-ASN deferral; Open Questions already carries it.

### Issue 3: E7's discoverability caveat is stated three times

**ASN-0076, E7 statement, "Reconciliation with ASN-0098's discoverability," and Claims Introduced table**: The caveat that `covers` is a structural witness and *not* ASN-0098 `discoverable_from` appears (a) parenthetically in E7's statement ("This is a structural-witness claim ... *not* a claim of discoverability"), (b) at length in the reconciliation paragraph ("The two run in opposite directions and rest on different state components ..."), and (c) again in the table row for E7.

**Problem**: Triplication of one distinction. The genuinely new content in the reconciliation paragraph is the *derived consequence* (absent arrangement, `ℓ_sup` is orphaned per LP17 and resurrectable per LP18, tied to E10). The opening half of the reconciliation merely restates the parenthetical already in E7's statement.

**Required**: Keep the orphaning/resurrection derivation (LP17/LP18 + E10 linkage) as the substantive content; collapse the repeated "structural-witness, not discoverability" framing to one location rather than three.

### Issue 4: E0's "First" ordering observation is design rationale, not reasoning

**ASN-0076, E0 ("We must observe two things about the order")**: "First, the composite definition fixes the successor step first; the chosen ordering makes the canonical unit-depth span `(ℓ_new, δ(1, #ℓ_new))` in `E_to` denote an *existing* link entity at the moment the supersession link is allocated, yielding a coherent reference rather than a forward declaration."

**Problem**: By L4 (endset spans may reference any tumbler, including not-yet-allocated ones), well-formedness does not require the referent to exist; the "First" point is therefore design rationale for an ordering convention, not a correctness step. Only the "Second" point (adjacency, used to identify `ℓ_sup = inc(ℓ_new, 0)`) is load-bearing.

**Required**: Drop or demote the "First" observation; retain the "Second" (adjacency) point, which the `ℓ_sup` identification actually consumes.

## OUT_OF_SCOPE

### Topic 1: Supersession chain/cycle invariants and "current successor" computation
**Why out of scope**: These are correctly placed in Open Questions; they concern a future supersession-semantics ASN, not a defect in EDITLINK's two-step composite.

### Topic 2: Authorization of who may select `d_new`
**Why out of scope**: E6's application-layer note correctly identifies this as belonging to a future authorization/capabilities ASN; the link model has no executor field.

VERDICT: REVISE
