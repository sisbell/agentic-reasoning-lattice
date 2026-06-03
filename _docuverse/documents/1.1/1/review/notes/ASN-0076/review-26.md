# Review of ASN-0076

## REVISE

### Issue 1: Citation of a nonexistent foundation claim "S9"
**ASN-0076, E0 (Invariant inheritance)**: "ASN-0036's S0 and S1 are subsumed by P0 and discharged with it (and S9 follows from P0 unconditionally)."
**Problem**: There is no claim S9 in ASN-0036 (its claims are S0–S5, S7/S7a/S7b/S7d, S8/S8-fin/S8a/S8-depth, D-CTG/D-MIN/D-CTG-depth/D-SEQ, and the two insertion-position predicates). "S9 follows from P0" therefore discharges nothing — it references a claim that does not exist in the foundation. Either the label is wrong or the clause is spurious.
**Required**: Remove the S9 clause, or correct it to the intended foundation claim and show the derivation.

### Issue 2: Sub-case (a) freshness is asserted at the wrong state
**ASN-0076, E0 (Successor step, sub-case (a))**: "SubAllocatorBundle (ASN-0047) certifies that this first emission satisfies `ℓ_new ∉ dom(Σ.C) ∪ dom(Σ.L)` at the state of allocation (freshness)."
**Problem**: SubAllocatorBundle establishes first-emission freshness *at the activating entity-allocation event* (when `d_new` enters `E_doc`), which is generally far earlier than the state `Σ` at which EDITLINK fires. Freshness at `Σ` does not follow directly from SubAllocatorBundle; it follows from the sub-case condition `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new} = ∅` together with the fact that only `A_L(d_new)` emits the first-emission address. The parallel sub-case (b) derives current-state freshness carefully (via L11a + the subspace argument); sub-case (a) omits the analogous derivation and leans on a freshness claim asserted at a different state.
**Required**: Derive `ℓ_new ∉ dom(Σ.C) ∪ dom(Σ.L)` *at `Σ`* from the sub-case-(a) emptiness condition, matching the rigor of sub-case (b).

### Issue 3: Incorrect description of coverage as "having no extensions"
**ASN-0076, The Composite**: "`coverage(E_from) = {t : ℓ_old ≼ t}` (the singleton `{ℓ_old}` plus its extensions, of which there are none until subsequent allocations may add them)".
**Problem**: Coverage is purely combinatorial over `T` and consults no state component (Definition — Coverage, ASN-0098). `{t ∈ T : ℓ_old ≼ t}` is the full prefix-closure of `ℓ_old` — an infinite set of tumblers — independent of what is allocated. The parenthetical "of which there are none" conflates the abstract coverage set with the (possibly empty) set of *allocated* extensions. The downstream proofs (E4, E7) need only `ℓ_old ∈ coverage(E_from)`, so the error is in the prose, not the result, but the statement as written is false.
**Required**: Drop or correct the parenthetical; coverage contains all prefix-extensions of `ℓ_old` in `T` regardless of allocation.

### Issue 4: Foundation coupling claims cited under altered names
**ASN-0076, The Composite / E5**: J0 is named "AllocationRequiresPlacement", J1★ "ExtensionRecordsProvenanceContentSubspace", J1'★ "ProvenanceRequiresExtensionContentSubspace".
**Problem**: ASN-0047 names these J0 = AllocationPlacementCoupling, J1★ = ExtensionRecordsProvenance, J1'★ = ProvenanceRequiresExtension. The label symbols match, so the references are traceable, but the descriptive names diverge from the foundation. Per the self-contained-with-foundation discipline, use the foundation's names rather than introducing variants.
**Required**: Align the descriptive names with ASN-0047.

## OUT_OF_SCOPE

### Topic 1: Supersession-type address convention (`τ_sup`)
**Why out of scope**: The ASN correctly declines to fix which tumbler designates "supersession" and defers it to a future ASN on type-endset conventions. E4 is honestly stated as a *structural* witness rather than a semantic identification, and the Open Questions enumerate the deferred conventions. This deferral is appropriate, not a gap in this ASN.

### Topic 2: Supersession-chain acyclicity and reader resolution policy
**Why out of scope**: Termination and acyclicity of supersession chains, and the policy for choosing among divergent successors (E5), are correctly flagged as unresolved in the Appendix and Open Questions. These belong to a future link-search / authorization ASN.

VERDICT: REVISE
