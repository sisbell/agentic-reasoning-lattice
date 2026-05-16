# Channel Assignment — ASN-0051 review-43

**Date:** 2026-05-16 04:03

## Issue 1: K.μ~ listed as "elementary transition" in SV7
Reason: Pure terminological fix — ASN-0047's distinction between elementary transitions and distinguished composites is already established and cited within this ASN. No external channel needed.

## Issue 2: SV11 biconditional proof wording omits "overlap"
Reason: One-line proof completion. The overlap case follows directly from the S0 convexity argument already established in the SV11 proof — overlapping contiguous regions within I(β_k) share an extremum and coalesce by the same ordinal-contiguity reasoning. Internal.

## Issue 3: discover_through_s(d) lacks a formal SV claim
Reason: The required SV claims for discover_through_s follow mechanically from SV2–SV5 applied per-link to coverage(Σ.L(a).s); the document-derived caveat already lays out the argument. Internal derivation.

## Issue 4: SV5 worked example is degenerate
Reason: Pedagogical extension only — the non-degenerate witness in the SV5 proof's discussion provides the mathematical content, and constructing a parallel worked-example case from the post-removal state M'(d) is mechanical. Internal.

## Issue 5: "Resolution" used informally throughout without definition
Reason: Terminological fix — the intent ("Resolution gives the positions a reader would see") is already informally pinned to locate(e, d) in the body. Adding a definition formalising this tie requires no external input.

## Issue 6: SV6 proof's "Restricting to element-level t" step lacks an explicit boundary check
Reason: One-line clarification that the ordering k > p₃ > p₂ > p₁ rules out two of three boundary cases. The inequality chain follows from T4-validity of s (already established in the proof). Internal.

## Issue 7: K.μ~-induced intermediate states not addressed in projection invariance claim
Reason: Clarification draws only on K.μ~'s distinguished-composite decomposition into K.μ⁻ + K.μ⁺ (specified in ASN-0047 and already cited via K.μ~-FIX in this ASN) plus the already-proved SV3 and SV2. Internal.

## Issue 8: NewLinkEvaluationDefinedness corollary lacks an explicit proof
Reason: The four well-definedness steps cite K.λ's effect (ASN-0047) and L3/L4 (ASN-0043), both already cited in this ASN. The derivation is mechanical from established facts. Internal.
