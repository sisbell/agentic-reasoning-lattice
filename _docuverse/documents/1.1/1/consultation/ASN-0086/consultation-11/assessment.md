# Channel Assignment — ASN-0086 review-11

**Date:** 2026-05-16 19:53

## Issue 1: R0a's induction uses an implicit stronger invariant than the stated antichain
Reason: This is a proof-restructuring task that uses only material already present in the ASN — the substrate facts (T10a.2, T10a.7, T10a.8, zero-count additivity) and the named sibling-frontier discipline are all in scope. The auxiliary invariant can be stated and proved with the existing toolset; the reviewer's two reformulation options are both internally derivable.

## Issue 2: Open Questions cross-reference is unfulfilled
Reason: Purely editorial — either add an Open Question stating the slice-wise question or remove the dangling cross-reference. Open Questions need only be posed, not answered, so neither design intent nor implementation evidence is needed.

## Issue 3: R6c's reach excludes arrangement-modifying transitions
Reason: The Scoping note already establishes that arrangement-modifying transitions leave `Σ.L` untouched and therefore preserve every L-invariant trivially. Both fixes proposed by the reviewer (extending `⊑` or adding a parenthetical) follow directly from this fact and require no further channel input.
