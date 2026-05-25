# Channel Assignment — ASN-0051 review-37

**Date:** 2026-05-16 02:03

## Issue 1: SV10 witness violates J0 (AllocationRequiresPlacement)
Reason: Fix is fully derivable from the ASN — drop K.α(i₁) and K.α(i₃) per the reviewer's prescription; span well-formedness under T12 (ASN-0034) and coverage definition do not require i₁, i₃ ∈ dom(C). Pure internal consistency repair.

## Issue 2: CrossDocumentDecoupling inherits SV10's J0 violation
Reason: Mechanical propagation of Issue 1's fix to the inherited witness chain. No new design or implementation question; fully derivable from the ASN.

## Issue 3: discover_s domain restriction A ⊆ dom(Σ.C) is unjustifiably narrow
Reason: Choice between (a) relax to A ⊆ T and (b) justify content-only restriction depends on whether discovery was *designed* as a general I-space query and whether the *implementation* admits link-address queries. Both channels inform the scope decision.
Nelson question: Was link discovery intended to operate over content addresses only, or as a general I-space query admitting link-address queries (reverse-link traversal, type-hierarchy lookup)?
Gregory question: Does udanax-green's link-discovery mechanism (the index/lookup structures querying link endsets) admit link addresses as query inputs, or is the query domain restricted to content addresses?
