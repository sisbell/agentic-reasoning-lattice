# Review of ASN-0047

## REVISE

### Issue 1: K.δ k=1 sub-case presentation conflates structural relaxation with freshness discharge

**ASN-0047, Elementary transitions (K.δ)**: The k=1 case is presented as two sub-cases:
- "k = 1 (version, live): IsDocument(t) ∧ t ∈ E_doc"
- "k = 1 (version, ghost-base): IsDocument(t) only"

**Problem**: These are not distinct transitions with different effects. The structural relaxation (admitting t ∉ E_doc) and the resulting effect are identical; what differs is the freshness discharge route (T10a GlobalUniqueness vs direct E-inspection), which is determined by InEntityAllocatorDomain(t), not by which "sub-case" the caller selects. Presenting them as alternatives is misleading — any live operand t ∈ E_doc also satisfies the ghost-base precondition, so the "live" sub-case is structurally a special case of "ghost-base." The freshness-discharge table compounds this by listing "k = 1 ghost-base" as one discharge route, even though the same route applies to subsequent k = 0 chain steps in ghost-rooted chains (as the worked example demonstrates).

**Required**: Present k=1 as a single sub-case with precondition IsDocument(t), and route the freshness discharge by InEntityAllocatorDomain(t) (with the table entry generalized accordingly).

### Issue 2: K.μ⁻ definition forward-references concepts introduced later

**ASN-0047, Elementary transitions (K.μ⁻)**: "The shape is the per-state D-SEQ★ invariant derived in *Amendments to existing transitions* below"
**Problem**: K.μ⁻'s definition uses D-CTG★, D-MIN★, and D-SEQ★ before they are introduced in the *Amendments to existing transitions* section. Forces the reader to skip forward or proceed without grounding.
**Required**: Move the amendments section before K.μ⁻, or define K.μ⁻ in terms of the unamended D-CTG/D-MIN and strengthen later.

### Issue 3: L1b verification elides zeros preservation citation

**ASN-0047, ExtendedReachableStateInvariants proof (L1b case)**: "In the *subsequent-link case*, K.λ produces `ℓ = inc(prev, 0)` (TA5(c)), which is a sibling extension preserving the element-field length: TA5(c)'s length-preservation clause gives `#E(ℓ) = #E(prev)`"
**Problem**: TA5(c) preserves tumbler length (#ℓ = #prev), not element-field length #E. The element-field length is preserved only because zeros are also preserved across inc(·, 0) on T4-valid input, which requires T10a.8 (UniformSiblingZeroCount). The proof skips this step.
**Required**: Cite T10a.8 explicitly: same length + same zeros count → same element-field length.

### Issue 4: Use-site inventory after D-SEQ★ derivation

**ASN-0047, Amendments to existing transitions (D-SEQ★)**: "This per-subspace D-SEQ★ underwrites all subsequent appeals to a "V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}" structure in this ASN — including the K.μ⁻ amendment, the K.μ~-FIX domain-fixity argument, the link-subspace fixity proof, and the ExtendedReachableStateInvariants induction."
**Problem**: Use-site inventory enumerating downstream consumers — exactly the pattern flagged in the review-mode classifier. The derivation's content is what matters; future consumption is irrelevant to its meaning.
**Required**: Remove the sentence.

### Issue 5: Document-ordering justification in worked example

**ASN-0047, Worked example: fork with subsequent insertion (Notation)**: "This example is part of the extended-state discussion (placed after the K.λ, K.μ⁺_L, S3★, P3★, P4★, J1★, J1'★, D-CTG★, D-MIN★, D-SEQ★, Contains_C, CL-OWN, CL-UNIQ apparatus has been introduced)..."
**Problem**: Document-ordering justification combined with a use-site inventory. The reduction note is useful; the catalogue of prerequisites is noise.
**Required**: Reduce to "Verification lines use extended-state labels (P4★, J1★, etc.); since the example's arrangement is content-subspace-only, each starred form reduces here to its four-component ancestor."

### Issue 6: Defensive paragraphs around amendments and catalogue

**ASN-0047, multiple sections**: 
- "Trade-off acknowledgement. D-CTG★/D-MIN★ trade interior link-withdrawal expressibility..." (D-CTG★/D-MIN★ section)
- "Known gaps from the catalogue. The sufficiency claim is bounded by the per-component enumeration above..." (Elementary transitions section)
- "Asymmetry derivation. No invariant of the extended state requires every ℓ ∈ dom(L)..." (Orphan links section)
**Problem**: Each is a defensive justification that points forward to a treatment elsewhere ("treated in *Link-withdrawal gap* below", "contrast with J0"). The gaps themselves are addressed in their proper sections; these forward-pointing paragraphs only restate that something is incomplete.
**Required**: Remove or fold into the section that actually treats the gap.

### Issue 7: Freshness-discharge table entry too narrow

**ASN-0047, Freshness-discharge summary**: Table lists "K.δ k = 1 ghost-base (¬InEntityAllocatorDomain(t))" as a separate discharge route.
**Problem**: The worked example explicitly notes "the *displacement* of the freshness discharge from T10a-GlobalUniqueness to direct E-inspection propagates chain-wide" for subsequent k=0 steps. The table's narrow scoping to "k=1 ghost-base" conflicts with this propagation.
**Required**: Generalize the entry to "K.δ ¬IsNode(e), ¬InEntityAllocatorDomain(t)" so it covers k=0 and k=1 ghost-rooted steps uniformly.

### Issue 8: S4 verification's first-link case characterization includes irrelevant conjunct

**ASN-0047, ExtendedReachableStateInvariants proof (S4 case, K.λ first-link)**: "The first-link case is identified by the K.λ precondition `V_{s_L}(d) = ∅` together with `dom(L) ∩ {a : origin(a) = d} = ∅`"
**Problem**: V_{s_L}(d) = ∅ is not the criterion — orphan links (allocated but never arranged, or arranged then K.μ⁻'d off) can leave V_{s_L}(d) empty while dom(L) ∩ {a : origin(a) = d} ≠ ∅. SubAllocatorAxiom.FirstEmission applies only when the sub-allocator has not yet emitted, which is the second condition alone.
**Required**: Strike the first conjunct.

### Issue 9: Meta-commentary in worked example

**ASN-0047, Worked example: interior content replacement (composite verification)**: "The asymmetry between J1★'s and J1'★'s handling of re-added addresses is what this example demonstrates: K.μ⁻ + K.μ⁺ on a previously-arranged address is *transparent* to provenance coupling, because the provenance bookkeeping is tied to content novelty in the range rather than to V-position movement in the domain."
**Problem**: Meta-commentary stating what the example demonstrates. The verification lines already establish the asymmetry; an additional summary sentence narrating "what the example shows" is noise.
**Required**: Remove the sentence; the verification itself does the work.

### Issue 10: Meta-remark on proof structure

**ASN-0047, Allocator hierarchy under documents (Cross-document disjointness chain)**: "*Remark on case exhaustiveness.* The split into A and B is by trichotomy on the prefix relation between `d₁` and `d₂`; T10a is not consumed in the case split itself. T10a's role is in justifying that distinct documents can in fact land in Case B..."
**Problem**: Meta-prose about how the proof is structured, not advancing the proof. The reader does not need to be told that T10a is used elsewhere.
**Required**: Remove the remark.

### Issue 11: K.μ⁻ case (c) explanation has redundant commentary

**ASN-0047, K.μ⁻ exhaustiveness lemma**: Case (c) is described with two long paragraphs explaining the contiguity clause via a worked example (K' = {2, 4}) and re-explaining the routing.
**Problem**: The case (c) statement plus the partition proof body already establish the routing. The auxiliary explanation duplicates content.
**Required**: Tighten case (c) to its definition plus a brief contiguity-clause note; remove the {2, 4} worked example since case-(b) routing is established in the partition proof.

### Issue 12: Repeated deferral to "Open Questions"

**ASN-0047, multiple locations**: At least six paragraphs defer to "Open Questions" (concurrency discipline, ghost-base concurrency under multi-protocol allocation, withdrawal mechanism, account-level depth-1 extension, fork V-position correspondence, NodeAllocationRegistry protocol).
**Problem**: Accumulated forward references to the same downstream location — exactly the pattern flagged in review-mode.anti-bloat. Each deferral is individually defensible, but the accumulation makes the body feel scaffolded around what's *not* in scope.
**Required**: Consider whether all six need explicit body-text deferrals, or whether the Open Questions section can stand alone with the body restricting itself to in-scope material. Several of the body-text deferrals could be removed entirely.

## OUT_OF_SCOPE

The Open Questions section appropriately catalogues deferrals to future ASNs:
- Forking with arrangement-preservation invariants
- Version graph / lineage acyclicity
- Cross-document link discoverability after contraction
- Link subspace capacity bounds and ordering invariants
- Concurrency discipline for ghost-base freshness discharge
- Withdrawal mechanism reconciling tombstoning with D-CTG★/D-MIN★
- Account-level depth-1 extension

These are properly out of scope and correctly marked.

VERDICT: REVISE
