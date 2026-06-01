# Channel Assignment — ASN-0047 review-167

**Date:** 2026-05-31 20:22

## Issue 1: M is silently re-typed from partial (foundation) to total, forcing reinterpretation of inherited preconditions
Reason: The choice between keeping M partial (foundation-matching) or total is a formal-modeling decision fully specified by the ASN's own state definition and the cited foundation typing; no design intent or implementation evidence is required to pick one and state the override explicitly.

## Issue 2: J1, J1', and P4 are introduced only to be immediately superseded by J1★, J1'★, P4★, with forward "see below" deferrals
Reason: Purely editorial restructuring — the ASN already proves J1/J1'/P4 are the `dom(L) = ∅` specialisations of the starred forms, so collapsing them to one line each is derivable from the ASN's own content.

## Issue 3: The (a')/(b') sub-allocator parent-dispatch argument is restated in full in three sections
Reason: The dispatch logic is one argument already fully stated in the ASN; extracting it into a named sub-lemma and replacing the duplicates with citations requires no external input.

## Issue 4: Prose around inherited/new axioms explains why the axiom is wanted rather than what it states
Reason: Trimming rationale sub-paragraphs and reducing axiom restatements to content-plus-citation is internal editorial work; the surfaced totality friction is Issue 1's consequence, also internal.

## Issue 5: FrontierEquivalence reverse direction mislabels the producing allocator
Reason: The ASN's own Sub-allocator names and T10a framing already establish that `inc(t, 0)` is the sibling on the parent allocator's chain (t's sub-allocators produce `inc(t, k')` with `k' > 0`), so the naming correction is derivable internally.
