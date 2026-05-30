# Channel Assignment — ASN-0042 review-140

**Date:** 2026-05-30 09:32

## Issue 1: Factoring narration in StrictLongestCover preamble
Reason: Pure editorial fix — deleting meta-prose and opening with the general-form statement requires no design intent or implementation evidence; the lemma's content and citations are already present in the ASN.

## Issue 2: Content-model deferral repeated, duplicating the Scope declaration
Reason: De-duplication of three identical out-of-scope deferrals against the ASN's own Scope declaration; entirely internal, derivable from the ASN's existing structure.

## Issue 3: O17's statement omits the reachability qualifier its derivation requires
Reason: Internal consistency fix — the derivation already routes through RegistryReachability (reachable-only), and other claims (O4, O6, O9) use the inline "Σ reachable from Σ₀" convention; the corrected quantifier is derivable from the ASN alone.
