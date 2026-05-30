# Channel Assignment — ASN-0042 review-130

**Date:** 2026-05-30 06:04

## Issue 1: ω-conformance-gap paragraph defers downstream and inventories use-sites
Reason: Purely editorial compression. The load-bearing fact (`tumbleraccounteq` decides `owns`, not `ω`) is already established in the ASN's own evidence prose; collapsing to one sentence and dropping the inventory/pointer requires no design intent or new implementation evidence.

## Issue 2: the owns/ω distinction is stated twice
Reason: Internal deduplication. Both passages already exist in the ASN; deciding which slot keeps the distinction (the intro) is a structural edit needing no external input.

## Issue 3: O7(c) duplicated between postcondition prose and Formal Contract, with the same hedge twice
Reason: Internal restructuring. The discharge bookkeeping and entry-state caveat are already present and correct in the proof; relocating them out of the postcondition and Formal Contract is a presentation choice derivable from the ASN alone.

## Issue 4: trailing T3 non-sequiturs after proofs already concluded
Reason: Editorial deletion of unused proof tails. The derivations and their actual dependencies (including where T3 determinacy is genuinely consumed, O1's decidability postcondition) are all internal to the ASN.
