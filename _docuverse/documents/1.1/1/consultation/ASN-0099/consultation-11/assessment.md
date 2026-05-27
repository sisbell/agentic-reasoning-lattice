# Channel Assignment — ASN-0099 review-11

**Date:** 2026-05-26 19:27

## Issue 1: A1's "Propagation" clause forward-binds future revisions of other ASNs
Reason: Fix is internal — choice between narrowing A1's scope, reframing it as a transient discharge premise, or pursuing the OQ-identified ASN-0047 revision is a specification-framing decision derivable from the ASN's own dependency surface (F9 K.μ⁺/K.μ⁻ cases and F9-cor K.ρ case) and the explicit Open Question already drafted. No design intent or implementation evidence is needed.

## Issue 2: F19 monotonicity not extended to filtered/scoped variants
Reason: Fix is internal — the derivation is trivial composition of F19 with the per-constraint coverage stability supplied by LP13 (filtered) and intersection-preservation (scoped). Parallels the F15–F18 pattern already established in the ASN.

## Issue 3: F2/F3 formal claims missing for filtered/scoped variants
Reason: Fix is internal — the conformance contract pattern is already established by F2/F3 against `findlinks`; extending it to the filtered/scoped abstract operations is a mechanical restatement using the same `result(·) = abstract(·)` shape.

## Issue 4: F4 derivation lacks case-by-case treatment of enumerated strengthenings
Reason: Fix is internal — either enumerate witness pairs (e.g., for `coverage(eᵢ) ⊆ I`, take a coverage strictly larger than a singleton `I` that meets `I` in one address; for `|∩| ≥ k > 1`, take a singleton-intersection witness) or generalize the statement. Both options work from F1's structure alone.
