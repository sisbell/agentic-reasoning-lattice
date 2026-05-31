# Channel Assignment — ASN-0093 review-21

**Date:** 2026-05-31 04:36

## Issue 1: SubAllocatorAxiom.Exists is tautological given the definition of "active"
Reason: The fix is internal — the claim that the stream objects exist is already unconditional from ASN-0040's SiblingStream (any `B6`-valid parent) plus M0's discharge of `B6(b_·(d),1)`, both already cited in the note. Deleting or demoting Exists requires no design intent or implementation evidence.

## Issue 2: SubAllocatorAxiom.FirstEmission is derivable, not axiomatic
Reason: The fix is internal — FirstEmission's structural form follows from the ASN-0040 SiblingStream postcondition `cₙ = [p₁,…,p_{#p},0…0,n]` and its T4-validity from TA5a given M0, all of which the note already re-derives in the C1c/L1c exhibitions. Demotion to a lemma is a structural rearrangement.

## Issue 3: Use-site inventories and forward-reference meta-prose in structural slots
Reason: The fix is internal — removing enumerations of downstream consumers is pure prose deletion; the disciplines and lemmas stand on their stated content with no change to claims.

## Issue 4: Reviser-drift prose justifying definition-vs-consequence structure
Reason: The fix is internal — reducing the permanence commentary to the operative one-clause statement ("active at `Σ` iff `d ∈ dom(M)`; permanence follows from M1") is a self-contained edit using content already present.

## Issue 5: Duplicate prose
Reason: The fix is internal — collapsing the repeated E-projection parenthetical and the `E_doc → dom(M)` factoring to single statements is deduplication within the note, requiring no external input.
