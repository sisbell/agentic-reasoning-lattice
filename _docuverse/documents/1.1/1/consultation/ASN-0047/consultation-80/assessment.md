# Channel Assignment — ASN-0047 review-80

**Date:** 2026-05-17 14:24

## Issue 1: Coordinating coverage table is pure navigational meta-prose
Reason: Structural deletion of a use-site inventory table. The fix is purely editorial — remove the table, no design or implementation evidence required.

## Issue 2: Design provenance section is "Why the axiom is needed" essay content
Reason: Structural decision to delete rationale prose; the formal axioms stand on their own. Consultation citations belong in an external provenance log, not in the ASN body.

## Issue 3: Cross-references to deferred questions duplicates the Open Questions section
Reason: Pure forward-reference deletion. Internal editorial fix.

## Issue 4: K.μ⁻ Precondition signpost paragraph is defensive justification
Reason: Stylistic deletion of meta-prose explaining what is about to be said. The precondition clauses suffice on their own.

## Issue 5: ValidComposite★ "identity composite (n = 0 case)" paragraph
Reason: Internal decision on quantifier semantics; the choice (`n ≥ 0` vs `n ≥ 1`) is technical and derivable from K.μ~'s π=id case already established in the ASN.

## Issue 6: K.μ~ "Other admissible decompositions" subsection is a use-site inventory
Reason: Illustrative variants belong outside the abstract spec once the existence claim is established. Pure editorial deletion.

## Issue 7: "Reconciliation with ASN-0043's L1c" is defensive justification
Reason: Compression of repeated prose into one sentence. Internal editorial fix.

## Issue 8: Ghost-base K.δ admissibility presumes an unmodeled allocator
Reason: Touches design intent for ghost addresses (Nelson's doctrine of whether ghosts are "allocated" in any sense) and implementation reality (whether udanax-green tracks any state for non-instantiated tumblers). Both perspectives shape whether to drop `t ∈ allocated(s)` or specify a ghost-emission mechanism.
Nelson question: Does the ghost-element doctrine (LM 4/23) treat ghost tumblers as "allocated" in any sense — i.e., does the design distinguish ghost addresses from merely-structurally-valid tumblers that have never been issued by any allocator?
Gregory question: Does udanax-green have any state representation (granfilade record, ISA reservation, or similar) for tumblers that are structurally valid but have never been instantiated by `docreatenewdocument`, `docreatenewversion`, or related procedures?

## Issue 9: J4 admits k=0, k=1, k=2 without distinguishing forking from sibling allocation
Reason: Requires resolving Nelson's terminology ("fork" as version creation vs new-document-with-transclusion) and Gregory's implementation distinction (separate procedures for `docreatenewdocument` vs `docreatenewversion`) to determine whether J4 should be restricted to a specific K.δ sub-case or split into named operations.
Nelson question: In Nelson's design, does "forking" (LM 4/29 "the new document's id will indicate its ancestry") refer specifically to version creation (k=1 in this ASN's terms), or does it cover all new-document-with-transclusion patterns including k=0 sibling and k=2 hierarchical descent?
Gregory question: Does udanax-green's procedural distinction between `docreatenewdocument` and `docreatenewversion` correspond to different K.δ sub-cases (k=0 vs k=1), and which procedure does the implementation characterize as "fork"?

## Issue 10: Three-discharge-paths paragraph is essay content surrounding the dispatch table
Reason: The table already encodes the three paths; the prose restatement is redundant. Internal editorial fix.

## Issue 11: Per-state vs per-transition theorem split is restated for four-component and extended states
Reason: Structural consolidation — keep only the extended theorems with a note that four-component is the L=∅ specialization. Internal editorial fix.

## Issue 12: SubspaceConventionAxiom subsumes SC-NEQ but both are stated as axioms
Reason: Internal decision on axiom layering. Both forms appeal to the same evidence already in the ASN; the choice is structural rather than evidential.

## Issue 13: K.μ⁻ exhaustiveness lemma duplicates content with subsequent case analysis
Reason: Pick one presentation (lemma or case analysis). Internal editorial decision.

## Issue 14: Multiple "load-bearing" / "operative" tagging throughout
Reason: Pure stylistic emphasis removal. Internal editorial fix.

## Issue 15: Notation section's "T" vs "allocated(s)" clarification
Reason: Meta-prose about terminology history; delete and use `allocated(s)` consistently. Internal editorial fix.
