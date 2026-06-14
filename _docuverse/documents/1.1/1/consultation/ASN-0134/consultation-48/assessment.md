# Channel Assignment — ASN-0134 review-48

**Date:** 2026-06-14 16:52

## Issue 1: §4 opening previews and duplicates the H3 conditional-`K.σ` rationale
Reason: Pure deduplication — the "why the carry-over is conditional" rationale (committed stack carries no `A_doc`-conformance over `E`, so `K.σ`'s frontier status is realization-conditional) appears in full at both the §4 opening and H3, so collapsing one to a pointer is fully determined by the note's own content. No design intent or implementation evidence is at stake.

## Issue 2: A6's representative invariant list uses labels overloaded across the note's own foundations
Reason: The disambiguation is forced by A6's own scoping — "every per-state invariant of the `→_sh` stack" — plus the note's repeated statement that the stack carries no entity set `E` ("an entity set E that 𝔼's K.σ does not carry"), which together exclude ASN-0047's `P6` (over `E_doc`) and ASN-0128's SurfaceDiscipline (a derivation predicate) and select ASN-0126's ReachableConformance and ASN-0093's StoreDisjointness. The cross-ASN label facts are already supplied in the finding and verifiable by reading the sibling specs directly — neither of which is a Nelson or Gregory channel.

## Issue 3: Section-closing paragraphs recap results their sections already establish
Reason: The fix trims closers that restate the V1 soundness/durability bullets (§8) and the two-families instance analyses (§4) already present in the note, preserving only the genuinely new taxonomic-closure and termination-hand-off sentences. This is internal editing derivable from the note's own structure.
