# Channel Assignment — ASN-0096 review-1

**Date:** 2026-05-24 07:54

## Issue 1: Claim count mismatch
Reason: Internal accounting issue. The ASN itself has the claims; reconciling 16 vs 18 requires re-reading the ASN content, not external consultation.

## Issue 2: Moving frame may not cover all transition families
Reason: Needs Nelson for the intended K.μ family taxonomy and how operations like FORK and MAKELINK relate to displacement semantics; needs Gregory to confirm which operations exist and what state transitions they produce.
Nelson question: What is the complete enumeration of K.μ operation families, and which were intended to displace existing link projections versus create new structure?
Gregory question: Which udanax-green operations modify existing I-address coverage in a way that would change projection output (vs. operations that only create fresh addresses or new links)?

## Issue 3: Projection signature underspecified
Reason: Needs Nelson because the type signature of `proj` reflects design intent about what projection operates over (endset, span, address); Gregory can confirm whether the implementation distinguishes these operands.
Nelson question: Was projection designed as a single operation over endsets, or as distinct operations over endsets, spans, and individual I-addresses with different cardinality semantics?
Gregory question: Does udanax-green implement projection as a uniform function, or are there separate code paths for endset-level vs. span-level vs. address-level projection?

## Issue 4: Derived guarantees lack visible derivation chains
Reason: Internal. The premise sets for LP-SURV and LP-DISC are composed from claims already in the ASN; surfacing the derivation is an exposition task using existing content.

## Issue 5: Boundary cases omit standard hard cases
Reason: Needs Gregory for concrete implementation behavior on zero-width spans, empty endsets, exact-coverage DELETE, and INSERT-inside-coverage; Nelson for whether these cases were intended to be defined or undefined.
Nelson question: Was projection of zero-width spans and empty endsets designed as vacuously defined, undefined, or a vanishing operation?
Gregory question: How does udanax-green handle DELETE of the exact coverage range and INSERT strictly inside a coverage range — does it produce one projection cluster or split into multiple?

## Issue 6: No concrete example
Reason: Internal. A worked example for LP-CONTR or LP-EXT can be constructed from the projection definition and transition semantics already in the ASN without external evidence.

## Issue 7: Weakest precondition analysis not evident
Reason: Internal. The wp computation for LP-SURV derives from the projection definition plus the moving-frame claims, all already present in the ASN.

## Issue 8: Non-invariants need precise statement of what changes
Reason: Needs Gregory to exhibit concrete K.μ transitions that demonstrably violate LP-NOV, LP-NOC, LP-NOD; the witnesses must come from actual implementation behavior to be constructive.
Gregory question: For each non-invariant (novelty, cardinality, document-identity), which specific udanax-green operation produces an observable change in that property, and what is the minimal trace exhibiting the change?
