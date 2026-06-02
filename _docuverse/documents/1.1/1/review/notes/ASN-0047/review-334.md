# Review of ASN-0047

## REVISE

### Issue 1: Verification-matrix preamble carries a downstream-discharge inventory, not reasoning
**ASN-0047, *Extended reachable-state invariants*, Class (a) matrix preamble**: "The named composite K.μ~ carries no column here, and the per-invariant prose below does not repeat this routing: every intermediate state of a K.μ~ instance is a K.μ⁻ then a K.μ⁺ step, already discharged by those two columns, and *all* of K.μ~'s composite-boundary specifics — LRP, K.μ~-S3★, K.μ~-FIX, and its S3★, CL-OWN, and CL-UNIQ preservation — are discharged once in the *Decomposition of K.μ~* section, not as per-elementary-step obligations."
**Problem**: This is a use-site inventory plus deferral — it enumerates which named results live in which downstream section, telling the reader where *not* to expect a column. It advances no part of the invariant argument; a reader following the matrix must skip it. This is exactly the forward-reference accretion pattern (a paragraph deferring to a downstream location while listing its named consumers).
**Required**: Reduce to a single clause stating that K.μ~ is a K.μ⁻+K.μ⁺ composite and therefore inherits both columns. Drop the enumeration of LRP / K.μ~-S3★ / K.μ~-FIX / CL-OWN / CL-UNIQ discharge sites.

### Issue 2: "full-clearance realisation claim" framing includes document-organization meta-prose
**ASN-0047, *Decomposition of K.μ~***: "We record this as the **full-clearance realisation claim** — *the full-clearance form realises every admissible π* — and establish it once in Steps (A)–(B) below; subsequent passages cite it by name rather than restate it."
**Problem**: The clause "establish it once in Steps (A)–(B) below; subsequent passages cite it by name rather than restate it" is prose about how the document is organized, not about the claim. Naming a claim and proving it is legitimate; narrating the citation discipline is not. The claim statement itself ("the full-clearance form realises every admissible π") suffices.
**Required**: Delete the "establish it once … cite it by name rather than restate it" clause; keep the named claim and its Steps (A)–(B) proof.

### Issue 3: Worked examples defer repeatedly to "J4 step (ii)" for the same grounding
**ASN-0047, *Worked example: fork of a duplicate-I-address source***: "the implementation behaviour grounding this is stated once at J4 step (ii)." Compare *Worked example: subsequent-version fork (k = 0)*, which also routes its CREATENEWVERSION grounding through J4 step (ii).
**Problem**: Multiple worked examples in different sections defer to the same downstream location for the implementation grounding. Each deferral is a sentence the reader must follow elsewhere rather than a check performed in place; the pattern "multiple paragraphs in different sections defer to the same downstream location" applies. The φ-bijection postcondition the example checks (`|dom(M'(d_new))| = 2`) is self-contained and needs no deferral pointer.
**Required**: Remove the "stated once at J4 step (ii)" deferral sentences from the worked examples; the φ-injectivity check stands on its own. State the implementation grounding once, at J4, without back-pointers from the examples.

### Issue 4: SubAllocatorBundle re-exports foundation lemmas under local names
**ASN-0047, *Allocator hierarchy under documents*, SubAllocatorBundle**: "Each sub-clause below is proved by a named ASN-0093 lemma. … The five sub-clauses, each with its discharging ASN-0093 lemma" — followed by five sub-clauses each terminating in "*Discharge:* [lemma] (ASN-0093)."
**Problem**: Each sub-clause restates an ASN-0093 result (DisjointSubAllocatorChains, FirstEmission/FirstEmissionFreshness, ChainElementT4Validity, ChainDiscipline/ChainEnumerationInjectivity, CrossDocumentDisjointness) under a new local label, with the body of each sub-clause being the discharge pointer. Since ASN-0093 is a foundation, these can be cited at point of use; bundling them into five renamed sub-clauses is a use-site inventory that adds a naming layer without adding reasoning. The genuinely new content (the *Disjointness* sub-clause's cross-subspace fourth-clause delta dispatched by CrossDocDisjoint) is buried among four re-exports.
**Required**: Cite the four foundation lemmas inline where consumed (e.g. at the K.α/K.λ first-emission freshness steps) and retain only the cross-subspace delta as local content, rather than mirroring all five ASN-0093 lemmas under SubAllocatorBundle.* names.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
**Why out of scope**: The final open question correctly identifies that K.μ⁻ models suffix-only contraction while the implementation's interior `DELETEVSPAN` compacts-and-renumbers. This is a future operation-modeling question, not a defect in the current K.μ⁻ specification — the suffix-removal K.μ⁻ is internally consistent with D-CTG★/D-MIN★.

### Topic 2: Type-only / one-sided links (K.λ endset emptiness)
**Why out of scope**: Whether K.λ should require `e₁ ∪ e₂ ≠ ∅` is a link-semantics design choice raised in the open questions; L3 already fixes the structural floor (`N ≥ 3`, `e₃ ≠ ∅`), and the present invariants are sound without resolving it.

VERDICT: REVISE
