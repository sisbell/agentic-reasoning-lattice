# Review of ASN-0047

I read the ASN in full. The core argument — the five-component state model, the seven elementary transitions plus K.μ~, the per-state vs composite-boundary invariant split, and the per-subspace D-★ strengthenings — is rigorous. The hard proofs I spot-checked (D-SEQ★ Step-1 infinite-family argument, K.μ~ domain-fixity and link-subspace fixity, FrontierEquivalence, GlobalLineage clause (iii)) hold up, and the depth requirements (concrete worked examples, explicit wp derivations for J1★/J1'★) are met. My findings are confined to accreted prose, which the active anti-bloat classifier directs me to surface.

## REVISE

### Issue 1: Fork section explains the same excluded case twice
**ASN-0047, §Coupling and isolation (J4 / Definition (Fork))**: The Fork *precondition* already states `d_src ∈ E_doc ∧ V_{s_C}(d_src) ≠ ∅`. Two later paragraphs then independently re-litigate the case that precondition excludes:
- "The weaker condition M(d_src) ≠ ∅ is insufficient: a document with only link-subspace positions ... has ran(M(d_src)) ⊆ dom(L), and no address in dom(L) can serve as the target of a content-subspace V-position."
- "When the source's content subspace is empty — whether because M(d_src) = ∅ or because dom_C(M(d_src)) = ∅ — the fork definition does not apply; creation from such a source is ex nihilo (K.δ alone), not a fork."

**Problem**: Both paragraphs imagine the empty-content / link-only source that `V_{s_C}(d_src) ≠ ∅` already forbids, and both reach the same conclusion (link-only source → not forkable → ex nihilo). This is precondition-justification prose duplicated across the section; a reader must read past one to confirm the other says nothing new.

**Required**: State the precondition rationale once (a single clause noting why `V_{s_C}(d_src) ≠ ∅` is required rather than `M(d_src) ≠ ∅`) and delete the redundant restatement.

### Issue 2: "K.μ~ is a named composite, not a primitive transition" restated across slots
**ASN-0047, multiple sections**: The same fact is asserted in at least four locations — closing paragraph of *Elementary transitions* ("K.μ~ ... is a named composite of K.μ⁻ + K.μ⁺ (analogous to J4), not a primitive transition"), J3 ("The named composite K.μ~ is likewise self-sufficient"), the *Properties Introduced* table ("named composite K.μ⁻ + K.μ⁺ (not a primitive transition)"), and the *Temporal decomposition* table ("K.μ~ (named composite, K.μ⁻ + K.μ⁺)").

**Problem**: The compositional status is load-bearing once (at the defining site, *Decomposition of K.μ~*); the repeated "not a primitive" disclaimers add no information and are the kind of restated qualifier the reviser-drift check names.

**Required**: Fix the status at the definition site and let the table entries reference it by name without re-asserting "not a primitive transition."

## OUT_OF_SCOPE

### Topic 1: J0 permits fresh content to be displayed only in a non-origin document
J0 quantifies the placement document existentially (`(E d : d ∈ E'_doc ...)`), so a freshly allocated `a` with `origin(a) = d` may, by transclusion, be placed only in some `d' ≠ d` and never displayed in its own origin document. No stated invariant breaks (P6, P7a remain satisfied via the placement document), so this is not an error in ASN-0047.

**Why out of scope**: Whether fresh content must appear in its origin document is a new invariant question (it pairs naturally with the existing open question on transclusion-chain provenance), not a defect in the current coupling.

VERDICT: REVISE
