# Review of ASN-0047

## REVISE

### Issue 1: P4's inductive proof enumerates an incomplete transition set, then P4 is declared unsatisfiable in the full model
**ASN-0047, "Coupling and isolation" (P4 ProvenanceBounds)**: The proof states "In any reachable state where J1 has been satisfied for all prior transitions: Contains(Σ) ⊆ R" and discharges it by a per-elementary analysis listing only "K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~ (composite), K.ρ."
**Problem**: The enumeration omits K.λ and K.μ⁺_L. Under K.μ⁺_L, `Contains(Σ')` gains `(ℓ, d)` with `ℓ ∈ dom(L)`; since `dom(L) ∩ dom(C) = ∅` (L14) and provenance entries reference `dom(C)` (P7), `(ℓ, d) ∉ R`, so P4's case-(ii) inductive step (which would invoke J1 to require `(ℓ, d) ∈ R'`) actually fails. The later "Content-scoped containment" section concedes exactly this — "P4 is unsatisfiable for the unscoped relation once link-subspace mappings exist." So a theorem is given an unqualified base+inductive proof over a transition set that excludes the very transitions that break it, and only several sections later is it disclosed to be false in the full model. This is "showing the common case works does not establish the edge case": the proof never confronts K.μ⁺_L/K.λ.
**Required**: Scope P4's statement and proof explicitly to the link-free transition fragment (no K.λ, no K.μ⁺_L) at the point of proof — i.e., present P4 as a property of the four-component scaffold that P4★ supersedes — rather than as an unqualified reachable-state theorem whose proof silently omits the falsifying transitions.

### Issue 2: Essay-style rationale around LinkVPositionDepthAxiom
**ASN-0047, "Asymmetry with content-subspace depth (intentional)"**: The second half of this paragraph — "The distinction is the V/I separation applied consistently: stable identity must reside somewhere. A content byte's permanent identity lives in its I-address … a link, by contrast, has no separate I-space identity to fall back on: its address *is* its identity …" with the Nelson LM 4/11 quote.
**Problem**: This is "new prose around an axiom [that] explains why the axiom is needed rather than what it says." The substantive content — content-subspace depth may differ across re-populations, link-subspace depth is fixed per document — is a one-line formal fact already stated in the paragraph's first half. The philosophical V/I-identity justification adds no obligation a reader must discharge and sits in a structural slot immediately after the axiom.
**Required**: Reduce to the formal asymmetry statement (content depth free across re-populations via `ValidFirstInsertionPosition`; link depth pinned by the axiom). Drop the V/I-separation essay and Nelson quote, or move a single-sentence motivation to a non-normative remark.

### Issue 3: Intra-section circular deferrals in the K.μ~ decomposition
**ASN-0047, "Decomposition of K.μ~" / "Necessity and sufficiency of the precondition"**: The "Decomposition" paragraph defers upward ("established by the *Necessity* and *Sufficiency* arguments … above"); "Necessity and sufficiency" defers to "Steps (A), (C), (D), all derived in this section" and to "Step (A) … above"; Step (A)'s proof defers downward to "the *Case s_C → s_L* … paragraphs below"; the bijection-equation preamble defers to "Step (B.3) below," which defers back to "the admissibility filter (above)."
**Problem**: This matches "multiple paragraphs in different sections defer to the same downstream location" and reviser-drift. The reader cannot follow the argument linearly: each load-bearing step points at another step that points back. The forward/backward pointer web is restructuring residue, not advancing reasoning.
**Required**: Linearize. Prove Step (A) (subspace preservation), then Steps (C)/(D) (link fixity), then the necessity/sufficiency argument that consumes them, in dependency order, so each result is stated once before it is used and the cross-references collapse.

### Issue 4: Inherited foundation axiom restated and re-derived
**ASN-0047, "Allocator hierarchy under documents" (SubAllocatorAxiom)**: The section states the five sub-clauses are "inherited from ASN-0093 without modification," then elaborates each — e.g., SubAllocatorAxiom.Namespace re-derives "The first emission `[d.0.s_C.1]` is T4-valid by construction: the document d is T4-valid … appending one zero separator and the two-component element field `[s_C, 1]` … yields a T4-valid tumbler … subsequent `inc(·, 0)` emissions preserve T4-validity by TA5a."
**Problem**: Restating a foundation axiom is permitted, but re-deriving its content is not "restate the definitions needed" — it is re-proving a verified foundation guarantee. If the axiom is inherited verbatim, the T4-validity construction belongs to ASN-0093, not here.
**Required**: Cite the inherited clauses by name and source; drop the in-body re-derivations (Namespace T4-validity, T10aConformance frontier elaboration) unless ASN-0047 actually strengthens them.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: J4's fork leaves the forked document's link subspace empty, and the ASN already records that a link-inheritance mechanism "would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is correctly deferred; not an error here.

### Topic 2: Interior link withdrawal / tombstoning
**Why out of scope**: Withdrawing an interior link while retaining later links is acknowledged as requiring a mechanism outside K.μ⁻'s suffix-truncation contract and is listed in Open Questions. New territory, not a defect.

VERDICT: REVISE
