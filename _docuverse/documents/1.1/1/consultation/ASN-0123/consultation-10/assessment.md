# Channel Assignment — ASN-0123 review-10

**Date:** 2026-06-13 01:09

## Issue 1: the cross-owner branch's realizability rests on `pfx(π) ∈ E`, which PS does not deliver
Reason: Internal. The gap is a formalization bridge between ASN-0042's principal structure (its PrefixBaptismCoupling already yields `pfx(π) ∈ Σ.B`) and ASN-0047's entity set `E` — either extend the B=E identification past document level or state `pfx(π) ∈ E` as an explicit cross-owner precondition; both options draw only on cited foundations, and the implementation's non-enforcement is already recorded as deviation 4, so neither design intent nor fresh code evidence bears on whether the abstract model carries account prefixes into `E`.

## Issue 2: V7's downward navigation claims to enumerate "the versions of d" but excludes cross-owner versions
Reason: Internal. This is a pure scoping fix — the ASN already proves severance (V9, `¬(d_src ≼ v)`), defines `derives`, and flags the consequence in Open Question 2, so narrowing V7's "the versions of d" to the owned/address-discoverable versions is fully derivable from content already present.
