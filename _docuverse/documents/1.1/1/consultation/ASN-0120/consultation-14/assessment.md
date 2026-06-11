# Channel Assignment — ASN-0120 review-14

**Date:** 2026-06-11 03:39

## Issue 1: `wf` does not enforce the depth its own gloss asserts
Reason: The fix requires choosing between tightening the precondition (depth-match required) and loosening the prose (mismatch admitted), and that choice should follow the behavioral ground truth: what the implementation actually accepts and resolves when a spec's depth disagrees with the document's content depth. This is an evidence question, not a design-intent one — the confinement math survives either way.
Gregory question: When CREATELINK's `vspanset2sporglset`/`permute` walks a source arrangement, does it require or assume the supplied V-span's depth matches the document's content V-position depth, and if a mismatched-depth span is supplied, what I-regions does it actually emit?

## Issue 2: Elementary precondition discharge gaps (K.μ⁺_L and K.λ)
Reason: Both gaps are closable from facts the ASN already cites — FirstEmissionFreshness/SubsequentEmissionFreshness (or L0's subspace argument) for the content branch, and S8-fin for finiteness of `ρ`. The fix is writing the missing proof steps; no external input changes them.

## Issue 3: ML10's frame omits E and R, and J1'★'s vacuity is misgrounded
Reason: The missing clauses `E' = E ∧ R' = R` are the stated frames of K.λ and K.μ⁺_L in the substrate ASNs (ASN-0047, ASN-0093), and regrounding J1'★'s vacuity on `R' \ R = ∅` is a purely formal correction. Derivable from the ASN's own dependency content.

## Issue 4: Worked example — the type spec is not concrete, and the contiguity remark contradicts the example's own data
Reason: Constructing a concrete type source document with an active V-position, and either picking genuinely non-adjacent addresses or applying M7's two-sided (I-adjacency and V-adjacency) merge condition, uses only machinery the ASN already cites (ML6's precondition, ASN-0058's M7). Internal fix.

## Issue 5: Meta-prose accretion
Reason: Purely editorial — deleting defensive framing, deduplicating the confinement derivation, and moving the Gregory parenthetical into a blockquoted implementation note require no external knowledge.

## Issue 6: "The consultation" — dangling referent grounding ML5's directionality claim
Reason: The review prescribes regrounding on the Nelson quotation plus ML9's endset symmetry, but that quotation's provenance was the dangling consultation itself; Nelson should confirm the design intent and supply a citable source so the replacement grounding is solid rather than secondhand.
Nelson question: Does Literary Machines (or the concept notes) support that a link's from/to ordering is a semantic labeling whose meaning depends on the link type — with the link followable from either end — rather than a traversal restriction, and what is the citable passage?
