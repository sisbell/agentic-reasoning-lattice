# Channel Assignment — ASN-0051 review-31

**Date:** 2026-05-15 23:53

## Issue 1: SV2 and SV3 statements cover π but proofs additionally establish locate
Reason: Purely a structural/symmetry fix to the formal statements. The locate content already lives in the proofs; the question is presentation — expand statements or split into named claims. Derivable from the ASN's own content.

## Issue 2: SV6 sub-lemma elides a needed agreement step
Reason: Proof-level gap; the missing transitivity step (t↔s on 1..j−1 and s⊕ℓ↔s on 1..k−1 ⇒ t↔s⊕ℓ on 1..j−1) is mechanical and already implicit in the surrounding facts. Fix is internal to the proof.

## Issue 3: SV6 precondition is embedded inside a paragraph
Reason: Pure formatting — convert prose precondition to a structured bullet list. All content is already stated; only the presentation needs restructuring. Internal.

## Issue 4: Two-span worked example asserts "this is the maximally merged decomposition" without verifying merge condition fails
Reason: M7's merge condition (V-adjacency and I-adjacency) is defined in ASN-0058 and the necessary check is mechanical — verify v₆ relative to v₅ and a₂ relative to a₁+5. Derivable from cited ASN-0058 machinery.

## Issue 5: SV13 part (e) — K.μ⁺_L placement relative to M-frame list
Reason: Resolution requires checking K.μ⁺_L's frame condition against ASN-0047's operational closure (K.μ⁺_L modifies M; K.λ is M-frame). All transition semantics are settled in ASN-0047. Internal taxonomy fix.

## Issue 6: SV11's "exactly m · p decomposition terms" — indexed positions vs distinct sets
Reason: Pure clarification — distinguish Cartesian-product index count from distinct-set count. The mathematical content is already correct; only the count semantics need disambiguating in one sentence. Internal.
