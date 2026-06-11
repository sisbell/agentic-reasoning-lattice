# Channel Assignment — ASN-0129 review-1

**Date:** 2026-06-11 11:23

## Issue 1: Tuple-valued and class-valued bound variables have no vocabulary to act on them
Reason: Internal — the choice between admitting per-tuple primitives and restating PD0 over address-valued domains is a language-design decision for PL, the project's own construction; the tuple structure and V-STAT static-expansion machinery needed for either repair are already in the note and its cited deps (ASN-0086/0128). Neither design intent nor implementation evidence bears on it.

## Issue 2: PC6's converse is false as argued — `Observe_K` pattern queries exceed the atoms
Reason: Internal — the counterexample and both repair paths turn entirely on `Observe_K`'s already-specified signature (ASN-0086) and PL's own definition; choosing between extending the vocabulary and downgrading PC6 to a definition is the note's architectural call, not a question answerable from Literary Machines or udanax-green.

## Issue 3: PC6a's proof sketch cites a result for a strictly weaker logic than PL
Reason: Internal — the unmet obligation is a model-theoretic inexpressibility proof (counting, built-in orders, walk atoms), which no channel can supply; the fallback demotion to a design stance is already grounded by ASN-0128's recorded both-authorities basis for withholding multi-hop traversal, so no re-consultation is needed.

## Issue 4: PD0's class, as written, contains non-monotone terms
Reason: Internal — pure proof repair: an inductive, polarity-typed definition of the PD0 class using the witness-persistence ground (L12/L12a) already cited in the note.

## Issue 5: PD2's "only exception is retraction" is false when BH4 is attached
Reason: Internal — the falsifying fact (BH4's `age` reads home-wide chain traffic, not K-slices) is already quoted from ASN-0128; the fix is carving out or scoping PD2's active-slice clause, requiring no new evidence.

## Issue 6: View semantics are inconsistent — audit enumeration atoms undefined, QD's view binding contradicts PC3
Reason: Internal — defining audit readings of the enumeration atoms and settling QD's view binding are spec-consistency decisions within the note's own view machinery; the audit/active/default lenses are project-substrate constructs (ASN-0128), not surfaces Nelson or udanax-green speak to, and the review already identifies that the note must own the new definition.

## Issue 7: UV is under-specified off set/sequence codomains
Reason: Internal — the per-codomain rules are presentation-layer design decisions, and the governing principle (verdicts are never presentation-rewritten) is already exhibited by the note's own `tip` carve-out; it needs stating and applying per atom, not external grounding.

## Issue 8: `age`'s partiality is exactly the silent kind PC2 bans, and it breaks PC5's universal claims
Reason: Internal — re-typing `age` as ℕ ∪ {⊥} (or adding an activeness guard primitive) is a mechanical type repair within the note's own COD and PC2 guard machinery.

## Issue 9: PC2a's aggregation cannot reach set-valued terms, and the "meta-level sum" has no defined status
Reason: Internal — closing QD under finite set-valued PL terms and deciding ℕ-addition's admission are expressiveness-boundary decisions for the project's own language; the finiteness arguments required (AD bounds, QD-fin) are already present in the note.

## Issue 10: `dom(Σ.M)` membership is silently absent, while PC4 overstates dependence on Σ.M
Reason: Internal — whether to admit an `M_dom` base is a layer-boundary decision the note already has the apparatus to make (the structural-reads fence and the ASN-0127 boundary supply the rationale either way), and tightening PC4's dependency tuple is mechanical; the substrate's read surface is fixed by the cited deps.

## Issue 11: Constants and literals are leaf forms the vocabulary never admits
Reason: Internal — admitting constants, ℕ literals, and optional-equality (or a definedness test) to V-PRIM is a mechanical vocabulary repair fully determined by the note's own terms and COD.

## Issue 12: Minor rigor defects
Reason: Internal — fixing a dangling citation, settling the `M_K(active)` notation (jointly with Issue 6's decision), and stating the induction base (Σ_init.C finite via R-VAL's verbatim ASN-0086 components, already cited) are mechanical edits from content in the note and its cone.
