# Channel Assignment — ASN-0036 review-180

**Date:** 2026-05-29 06:18

## Issue 1: S8a restates the domain-restriction axiom and carries defensive meta-prose
Reason: Purely editorial — the fix folds the per-component form into the existing domain-restriction axiom or strips the "not an independent claim"/"is equivalently" framing. Both the axiom and the T0/T4 equivalence are already present in the ASN, so no design intent or implementation evidence is required.

## Issue 2: S2 duplicates the `Σ.M(d)` partial-function axiom
Reason: Editorial deduplication — the `Σ.M(d) : T ⇀ T` partial-function declaration already carries single-valuedness, and S2's role as a citable name for the S8 proof is internal to the document. Removing the redundant declaration and justification essay needs no external channel.

## Issue 3: Under-cited promotion step in the S8 within-subspace lemma
Reason: Internal proof-citation fix — both NAT-discrete and NAT-order are foundation claims already in ASN-0034's dependency set referenced by this ASN; adding NAT-order to the promotion step is derivable from the existing proof structure and ASN-0034's own conventions.
