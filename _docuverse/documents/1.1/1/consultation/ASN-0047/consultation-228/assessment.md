# Channel Assignment — ASN-0047 review-228

**Date:** 2026-06-01 07:17

## Issue 1: S3★ listed as both an admissibility hypothesis and a derived consequence for K.μ~
Reason: Internal. The ASN's Step (B) already derives S3★(Σ') from the K.μ⁻ restriction + K.μ⁺ amendment cells, and the ASN explicitly classifies CL-OWN/CL-UNIQ/S2/S8★ as derived consequences; resolving S3★'s status to match is a pure consistency fix from the ASN's own proof structure.

## Issue 2: Body asserts empty-endset consumer semantics that the matching Open Question marks as undecided, and references an undefined term
Reason: Internal. The contradiction is between the body's assertion and the ASN's own Open Question, and "discovery-set unions" has no referent in the state model; aligning the body to the existing OQ (downgrade/defer) and dropping the undefined term is editorial consistency derivable from the ASN alone.

## Issue 3: Dead derivation of a fact already fixed by axiom
Reason: Internal. SubspaceConventionAxiom in the same ASN fixes s_C = 1 ∧ s_L = 2, making the s_C ≥ 1 / s_L ≥ 1 re-derivation trivially redundant; deletion requires no external input.

## Issue 4: K.δ k=0 fork sub-case carries an unstated precondition
Reason: Internal. The per-sub-case activation conditions (k=1 when A_v(d_src) has no prior emission; k=0 when it already has a frontier) are already established by the ASN's K.δ case analysis and FrontierEquivalence; making the fork precondition explicit is derivable from the ASN's own definitions.
