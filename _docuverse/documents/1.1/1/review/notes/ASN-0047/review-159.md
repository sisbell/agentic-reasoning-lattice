# Review of ASN-0047

I checked the elementary transitions, the K.δ case analysis, the K.μ~ decomposition, D-SEQ★ derivation, the cross-document disjointness lemma, and the worked-example arithmetic. The core formal content is sound: the tumbler arithmetic in every worked example checks out (`b_C(d) = [d.0.1]`, first emissions, `inc(·,0)` advances, fork addresses), the per-subspace D-SEQ★ derivation handles both `m=2` and `m≥3`, the K.μ~ net-effect-vs-map-level distinction is correctly drawn against S5 transclusion, and no non-foundation ASN is referenced. The findings below are the meta-prose / forward-reference accretion patterns the review mode flags at source.

## REVISE

### Issue 1: Non-normative remark is essay content explaining an axiom's motivation
**ASN-0047, Link-subspace extension (after LinkVPositionDepthAxiom)**: "*Remark (non-normative).* The asymmetry tracks the V/I separation: content identity lives in the I-address, leaving the V-position depth free to churn, whereas a link's address is its own identity, so its arrangement depth is pinned to keep references to it stable."
**Problem**: This is prose around an axiom that explains *why* the asymmetry is desirable rather than *what* the axiom states. It advances no claim — the asymmetry's normative content is already fully given by LinkVPositionDepthAxiom ("unchanged thereafter") and the preceding "Asymmetry with content-subspace depth (intentional)" paragraph, which already states the operational difference. The reader must skip it to reach the K.μ⁺_L definition.
**Required**: Delete the non-normative remark. If the V/I-separation rationale is needed anywhere, it belongs in the consultation record, not adjacent to the axiom.

### Issue 2: Three paragraphs in three sections defer to the same K.μ~ necessity/sufficiency proof
**ASN-0047, Decomposition of K.μ~ / ValidComposite★**:
- *Preconditions of K.μ~*: "The necessity and sufficiency of this precondition are proved at *Necessity and sufficiency of the precondition* below..."
- *Decomposition*: "The necessary-and-sufficient existence condition ... is established by the *Necessity* and *Sufficiency* arguments at *Necessity and sufficiency of the precondition* above..."
- *ValidComposite★* clause (1): "whose necessary-and-sufficient existence condition ... is stated and derived at *Preconditions of K.μ~* above."
**Problem**: Three separate locations point at the same proof, each restating the existence condition ("takes at least two distinct values") with its sufficiency caveat. This is the "multiple paragraphs in different sections defer to the same downstream location" pattern — it forces the reader to navigate a cycle of cross-references to find where the argument actually lives.
**Required**: State the existence condition and its proof once (at *Necessity and sufficiency of the precondition*), and let the other two sites cite it by name with no restatement of the condition or its caveat.

### Issue 3: Properties-Introduced J0 cell carries rationale and use-site inventory in place of the statement
**ASN-0047, Properties Introduced (J0 row)**: "**Axiomatic** (alongside SubspaceConventionAxiom, NodeUniqueAllocation, SubAllocatorAxiom, NoDeallocation, S0): content allocation (K.α) always co-occurs with arrangement extension (K.μ⁺); not derived from foundation. P7a depends on it. J0 and J1 are independent couplings — J0 couples K.α with K.μ⁺ (placement requirement); J1 is *derived* by wp from the requirement to preserve P4..."
**Problem**: A Properties-Introduced cell should give the statement. This cell instead inventories which other axioms J0 sits "alongside," names a downstream consumer ("P7a depends on it"), and re-litigates the J0-vs-J1 independence already argued in *Coupling and isolation*. The downstream-consumer note and the independence essay are the "enumerates downstream consumers" and relocated-prose patterns.
**Required**: Reduce the cell to J0's statement and its axiomatic status. Drop the alongside-list, the "P7a depends on it" pointer, and the J0/J1 independence recap (which belongs only at the derivation site).

### Issue 4: Forward dependence of J1's derivation on P4, which is later scoped away
**ASN-0047, Coupling and isolation (J1)** vs **P4 (Provenance bounds, link-free fragment)**: J1's derivation rests on "preserving a design choice — namely the invariant `Contains(Σ) ⊆ R` (P4 below)." P4 is then defined as a property "of the four-component scaffold ... no K.λ and no K.μ⁺_L," superseded by P4★ in the full state.
**Problem**: J1 is derived to preserve P4, but P4 holds only on a fragment that the extended state leaves behind; the load-bearing coupling in the extended state is J1★ (derived from P4★). The forward reference "(P4 below)" sends the reader to a property that is immediately qualified as non-extended-state. The reader cannot tell, at the J1 site, that this whole derivation is scaffold-only until reaching P4 and then J1★. This is the document-ordering forward-pointer pattern.
**Required**: At the J1 site, state up front that J1/P4 are the link-free scaffold form and that the extended-state coupling is J1★/P4★ (a one-clause signpost), so the reader is not led to treat J1's P4-preservation as the operative result.

## OUT_OF_SCOPE

### Topic 1: Node-allocation registry protocol, link inheritance under fork, link-withdrawal/tombstoning mechanism, account-level depth-1 extension
**Why out of scope**: These are correctly parked in Open Questions. The registry mechanism is explicitly bounded by NodeUniqueAllocation as the abstraction boundary; link inheritance and tombstoning require new transitions (K.μ⁺_L variants, retraction primitives) that are future-ASN territory; account-level depth-1 extension is a deliberate precondition exclusion with documented justification. No revision needed here.

VERDICT: REVISE
