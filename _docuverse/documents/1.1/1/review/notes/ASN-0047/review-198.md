# Review of ASN-0047

## REVISE

### Issue 1: Essay-length cells contradict the matrix's stated "navigational index" purpose
**ASN-0047, Class (a) verification matrix preamble and K.μ~ column**: The preamble declares "The matrix is a navigational index; each cell summarises the load-bearing argument." Yet the K.μ~ cells for `S8a, S8-depth, S8-fin`, `D-CTG★ / D-MIN★`, `D-SEQ★`, and `S8★` each contain multi-sentence derivations — e.g. the S8-fin/K.μ~ cell runs to a full paragraph ("S8-fin(Σ') discharged independently of K.μ~-FIX through the K.μ⁻ + K.μ⁺ decomposition: K.μ⁻ restricts dom(M(d))...finite + finite = finite...").
**Problem**: A table cell carrying a paragraph-length argument is essay content in a structural slot. It defeats the navigational-index purpose the preamble asserts and forces the reader to parse prose inside a grid. This is distinct from cell *terseness* — these cells are over-long, not under-specified.
**Required**: Reduce each K.μ~ cell to a one-line pointer to the corresponding per-invariant prose (which already exists for S8★, D-SEQ★, the K.μ~ rows), and move the derivation text there. Either the cells summarise or they prove; pick one convention and apply it uniformly.

### Issue 2: Meta-prose deciding which rows receive prose
**ASN-0047, after the Class (a) matrix**: "For frame- or precondition-only invariants (S7a, S7b, C1b, L1, L1a, L3, L-fin, and the like) the matrix cell *is* the discharge — no prose follows, to avoid restating the cell. The per-invariant prose below is reserved for invariants whose discharge mechanism is non-trivial (e.g. S8★, D-SEQ★, the K.μ~ rows, L1b, L1c)."
**Problem**: This is prose about the document's own prose-allocation policy. It advances no part of the verification; a reader following the proof gains nothing from being told which rows were judged trivial enough to omit. It is exactly the "essay content in a structural slot" the anti-bloat classifier targets.
**Required**: Delete. If a row's discharge is the matrix cell, simply let the prose omit it; no announcement is needed.

### Issue 3: Single-home navigation prose in the K.δ catalogue
**ASN-0047, K.δ case (ii)**: "...are discharged in §*K.δ case (ii) discharge and parent-allocator activation*; that section is the single home of the activation argument, and every other site in this ASN cites this K.δ case (ii) definition rather than re-pointing there."
**Problem**: The second clause justifies document organization ("single home... every other site cites this rather than re-pointing"), not the claim. This is the "prose justifies document ordering / multiple paragraphs defer to the same downstream location" pattern. The bare forward pointer suffices.
**Required**: Reduce to the pointer alone ("...discharged in §K.δ case (ii) discharge and parent-allocator activation"). Drop the self-description of the citation convention.

### Issue 4: Deferral redundancy around S4 and the distinctness corollaries
**ASN-0047, S4 paragraph and "Derived distinctness corollaries"**: The S4 paragraph states "...are discharged separately under 'Entity distinctness' and 'Link distinctness' below," and the corollaries block restates "the S4 paragraph defers to them." Two paragraphs in adjacent sections announce the same hand-off.
**Problem**: Reciprocal deferral prose ("defers to them" / "discharged separately below") is bidirectional pointer noise — the same routing fact stated twice from both ends. It is content the precise reader must read past.
**Required**: State the scoping once (S4 is content-only; entity/link distinctness handled in the corollaries) and remove the back-reference in the corollaries block.

### Issue 5: The identity dom(M) = E_doc is load-bearing but not enrolled as a tracked invariant
**ASN-0047, Bridging lemma (M–E_doc)**: "`dom(M) = E_doc` (†)" is asserted with an inline two-direction justification and then used pervasively (preconditions phrase document existence interchangeably as `d ∈ E_doc` and as allocation in M).
**Problem**: (†) functions as a standing per-state invariant — every `d ∈ E_doc`/`d ∈ dom(M)` substitution depends on it — yet it appears in neither the ExtendedReachableStateInvariants conjunction nor the verification matrix, and the proof's induction never checks its preservation per transition. A load-bearing identity threaded through the whole induction should be tracked through the induction, not relegated to a bridging note.
**Required**: Either add (†) to the per-state invariant set with a one-line preservation entry (only K.δ/IsDocument grows both sides in lockstep; all other transitions frame both), or explicitly state that (†) is a definitional consequence of K.δ's effect and the default-value convention requiring no separate preservation obligation. As written it sits between the two.

## OUT_OF_SCOPE

### Topic 1: Concurrent link/content allocation under a shared home document
The ASN's SequentialTransitionAxiom assumes totally-ordered atomic transitions; coordination-free concurrent allocation is named in the Open Questions and excluded by the Scope section (concurrency). No revision needed here.

VERDICT: REVISE
