# Review of ASN-0047

## REVISE

### Issue 1: J1'★ derivation asserted "in the same manner," never shown
**ASN-0047, *Scoped coupling constraints* (J1★ derivation paragraph)**: J1★ is derived by an explicit weakest-precondition computation: "wp(K.μ⁺ (amended), Contains_C(Σ') ⊆ R') = (A a : a ∈ ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C}) : (a, d) ∈ R)". The converse is then dispatched in one sentence: "Symmetrically, J1'★ is the converse coupling … derived in the same manner from the requirement that R have no extraneous entries unanchored in content-subspace arrangement."

**Problem**: J1★ and J1'★ are not symmetric. J1★ forces K.ρ from a content-range extension (wp target: P4★, `Contains_C ⊆ R`). J1'★ forces a content-range change from an R-extension — the wp runs backward from a *different* invariant (the historical-fidelity / no-unanchored-entries property, i.e. P4a), and the text never names that invariant nor computes the wp against it. "Derived in the same manner" is a proof-by-similarly for a coupling whose direction and target invariant genuinely differ. This is the load-bearing premise of the P4a extended-state derivation.

**Required**: State the invariant J1'★ is the wp-preserving coupling *for* (presumably P4a), and show the backward wp computation explicitly, as is done for J1★/P4★ — or, if the derivation is truly mechanical, give the one or two steps that make it so rather than asserting symmetry.

### Issue 2: Duplicated "T4b cannot identify the frontier" prose
**ASN-0047, K.δ *Rationale (k = 0 conjuncts)*** and **Properties Introduced, FrontierEquivalence row**:
- K.δ rationale: "T4b's `parent`/`zeros`/length stratification cannot in general identify t as the frontier of the allocator whose tracked chain contains it, so the direct freshness predicate `inc(t, 0) ∉ E` is the load-bearing operand selector."
- Properties table: "Counterexample to T4b-based identification: T4b's `parent`/`zeros`/length stratification does not in general identify t as the frontier of the allocator whose tracked chain contains it."

**Problem**: Near-verbatim restatement of the same claim in two slots (the "two paragraphs say the same thing in different words" pattern flagged by the anti-bloat classifier). The Properties table is an index; carrying the rationale a second time is accretion.

**Required**: Keep the statement at its load-bearing site (the K.δ rationale) and reduce the Properties-table row to the lemma statement plus a pointer, dropping the duplicated counterexample sentence.

### Issue 3: SubAllocFresh "single carrier" sentence is use-site inventory
**ASN-0047, *Allocator hierarchy under documents*, SubAllocatorFreshness lemma**: "We abbreviate this **SubAllocFresh**. It is the single carrier of the first-vs-subsequent freshness argument; the operations and derived obligations below cite it by name rather than re-derive it."

**Problem**: The second sentence enumerates downstream consumers and the citation discipline rather than advancing the lemma's content — the "definition's introduction enumerates downstream consumers" pattern. The lemma's three discharge parts already stand on their own.

**Required**: Drop the meta-sentence; the abbreviation alone suffices, and call-sites already cite it.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**ASN-0047, J4 fork composite**: The fork definition deliberately starts the forked document's link subspace empty and notes "A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope."

**Why out of scope**: This is correctly deferred — it is new territory (a compound operation over the link subspace), not a defect in the present transition taxonomy. The Open Questions list already records it.

### Topic 2: Node-allocation registry protocol
**ASN-0047, NodeUniqueAllocation / NodeRegistryBootstrap**: The registry that discharges node freshness/lineage is treated as an external axiom.

**Why out of scope**: Whether to specify the registry's issuing/persistence/concurrency protocol is a future-ASN question (already in Open Questions); NodeUniqueAllocation is a legitimate abstraction boundary for the docuverse-layer transition model.

VERDICT: REVISE
