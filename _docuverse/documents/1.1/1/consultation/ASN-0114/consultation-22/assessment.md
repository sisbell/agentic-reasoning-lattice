# Channel Assignment — ASN-0114 review-22

**Date:** 2026-06-10 00:18

## Issue 1: A relation-reading convention forward-referenced into the collapses paragraph
Reason: Pure exposition fix — cut a prematurely-placed, duplicate sentence and let the relation reading live solely in "Status of the result," which already develops it fully. No design intent or implementation evidence is in question; the relocation is derivable from the ASN's own structure.

## Issue 2: F4's frame restates itself
Reason: Redundancy removal whose justification is already internal to the ASN — the dropped clause's content is entailed by "`Σ.L` identical" (write-side) and by `Σ.M`/`Σ.C` (documents), with read-side confinement assigned to F6. Nothing turns on what the system was meant to do or what the code does.

## Issue 3: The `coverage(R) := ⟦R⟧` bridge over-justifies a definitional synonym
Reason: A stylistic exposition choice between two stated options; the load-bearing fact — that `⟦R⟧ = coverage(eᵢ)` is already well-typed and the two unions coincide immediately — rests on ASN-0053's span-set denotation, which the ASN already cites. No external channel needed.
