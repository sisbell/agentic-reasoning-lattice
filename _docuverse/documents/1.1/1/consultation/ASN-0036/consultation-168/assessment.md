# Channel Assignment — ASN-0036 review-168

**Date:** 2026-05-29 05:01

## Issue 1: Numbering gaps break self-containedness
Reason: Purely editorial — the fix is either contiguous renumbering or a one-line retirement note, both derivable from the ASN's own structure. Neither design intent nor implementation evidence bears on numbering hygiene.

## Issue 2: S5 treats transition invariants as vacuously satisfiable by an isolated state
Reason: The fix is a formal rephrasing — S0/S1 are already defined in this ASN as transition invariants (`Σ → Σ'`), so restating that they impose no condition on an isolated state is derivable from the ASN's own definitions.

## Issue 3: Editorializing meta-prose in the S8 proof and worked example
Reason: Purely a prose-editing fix — relabel the lemma directly and drop self-descriptive framing. No design or implementation question is involved.
