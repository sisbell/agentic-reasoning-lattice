# Channel Assignment — ASN-0047 review-303

**Date:** 2026-06-01 23:48

## Issue 1: J4 fork is characterized by range equality, which is strictly weaker than the "whole arrangement copy" it claims to formalize
Reason: The fix (replace range equality with a position- and multiplicity-preserving bijection) is mathematical, but committing to *order* and *duplicate* preservation as the correct semantics needs grounding in both design intent and implementation behavior, since the ASN currently only asserts "whole arrangement" without confirming these two dimensions.
Nelson question: When CREATENEWVERSION creates a new version, must the new document's content begin byte-for-byte identical to the source — preserving both the relative order of content and any repeated/transcluded material — or only the set of included content?
Gregory question: Does `docreatenewversion` (via `doretrievedocvspanfoo`/`retrievedocumentpartofvspanpm`) reproduce the source's content-subspace POOM with V-positions in the same order and with duplicate I-addresses retained at distinct positions, or can it collapse or reorder entries?

## Issue 2: Temporal decomposition table omits K.δ as a transition that modifies M
Reason: This is an internal contradiction between the temporal-decomposition table, K.δ's Document-case frame/effect, and the J4 discharge — resolvable by reconciling the ASN's own statements without external input.

## Issue 3: Forward-reference deferral and meta-prose around classification (anti-bloat)
Reason: Purely editorial restructuring — inlining operative constraints and collapsing the repeated P4a temporal-scope explanation is derivable from the ASN's existing content.
