# Channel Assignment — ASN-0126 review-50

**Date:** 2026-06-09 12:15

## Issue 1: "single point" overstates `→_sh`'s compatibility with ASN-0086
Reason: The rewording only needs two ASN-0086 facts — that `Emit_K` is total over `Endset × Endset` and that R5(c) constructs an empty from-set — both supplied verbatim by the review and both matters of ASN-0086's own spec content, not design intent or the C implementation. The `|F| = 1` decision itself is already settled in the note; only the scope-characterization prose changes. Internal.

## Issue 2: the Σ_init-construction sentence is stated twice, verbatim
Reason: Pure deduplication — the construction statement is already present in both sites; the fix states it once and cross-references. Derivable from the note alone.

## Issue 3: P1–P6 are forward-referenced before they are stated, then restated
Reason: Structural reorganization — move each property's statement to its derivation site and reduce the summary entries (P1, P5) to derivation pointers. All content is already in the note. Internal.

## Issue 4: "domain-discharge ordering" is meta-prose around the gate
Reason: Compression of accreted prose; the review supplies the target sentence, and the well-definedness point is already entailed by the gate's own definition in the note. Internal.

## Issue 5: `|e|` is defined twice, once with a self-satisfying forward reference
Reason: Editorial deduplication — define `|e|` once at first use, drop the redundant forward pointer, and remove one of the two state-independence statements. All present in the note. Internal.
