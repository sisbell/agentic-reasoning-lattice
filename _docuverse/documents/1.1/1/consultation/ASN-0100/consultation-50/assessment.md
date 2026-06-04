# Channel Assignment — ASN-0100 review-50

**Date:** 2026-06-04 15:18

## Issue 1: Counterfactual reasoning about a case INSERT excludes
Reason: Pure deletion — the fix removes a retracted counterfactual and cites the existing frame INS.frame.subspace, which already establishes link-subspace isolation within the ASN. No design intent or implementation evidence is at stake.

## Issue 2: "Composite atomicity" stated in multiple slots
Reason: Deduplication of an already-stated claim — consolidate the definitional-atomicity statement into §Atomicity and reference it elsewhere. The claim and its justification are entirely internal to the ASN.

## Issue 3: Repeated deferral to §Provenance for the same discharge
Reason: Structural cleanup — collapse four forward pointers to §Provenance into one. The discharge content already exists in the ASN; only the redundant pointers change.

## Issue 4: Use-site inventory attached to a precondition
Reason: Editorial trim — drop the per-step consumer enumeration from the precondition, leaving `d ∈ dom(M)`. The per-step discharge already lives in §Atomicity; nothing external is needed.
