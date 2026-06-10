# Channel Assignment — ASN-0127 review-4

**Date:** 2026-06-10 00:23

## Issue 1: The distinctive discovery-rise is asserted, never witnessed
Reason: Internal — the construction uses only primitives already in the note: F-IMG-MONO (image grows under K.μ⁺), F-INERT (store-fixed result invariance), and the content-sharing/arrangement-extension semantics already cited from ASN-0047/0058. K.μ⁺ mapping a V-position to a pre-existing content address `a_2 ∈ dom(C)` is licensed by the abstract model (M13/M14 permit non-injective `Σ.M(d)`), so witnessing the store-fixed rise needs no design-intent or implementation evidence.

## Issue 2: No weakest-precondition computed — all of it deferred to the open questions
Reason: Internal — the K.μ⁻ wp is a direct algebraic computation from F-UDIST and F-INERT, both already proved in the note, and the review supplies the full derivation skeleton (`findlinks(Δ, Σ) ⊆ findlinks(image(W, d_q, Σ'), Σ)`). No external channel is involved.

## Issue 3: E-INV lacks an explicit derivation and cites an incomplete premise
Reason: Internal — full link-value persistence `Σ'.L(a) = Σ.L(a)` is already available from L12 (immutable link values, cited in the note's State section) and the sibling foundation LP13 in ASN-0098 (already relied on here for LP3★/LP11/Store Monotonicity); the arity step from value equality is the L6 reasoning the note already runs in F-CIL. Verifying LP13's statement is reading a cited sibling ASN, not consulting Nelson or Gregory.
