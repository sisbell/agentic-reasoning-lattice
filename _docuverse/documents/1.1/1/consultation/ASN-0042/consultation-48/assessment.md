# Channel Assignment — ASN-0042 review-48

**Date:** 2026-05-14 07:57

```
## Issue 1: O18 / DelegatorAllocatesPrefix freshness gap
Reason: Need design intent on whether delegation always materially baptizes a fresh prefix (vs. permitting pre-baptized sub-positions to become principal prefixes), and implementation evidence on whether the granfilade/allocator ever pre-baptizes addresses that later become principal prefixes.
Nelson question: Did the design require that a principal's ownership prefix come into existence *at* the moment of delegation (a fresh baptism), or did Nelson contemplate principals being assigned prefixes that had previously been allocated as ordinary sub-positions within the delegator's domain?
Gregory question: In udanax-green, when a new account is admitted (via findpreviousisagr / the granfilade insertion path), is the account's tumbler always a fresh slot baptized in that same operation, or can an account be bound to an address that was previously baptized as a non-account sub-position under the parent's prefix?
```

```
## Issue 2: Invalid Bop depth parameters in O10 worked example
Reason: Mechanical error — Bop(·, 3) violates ASN-0040 B6(ii) (d ∈ {1, 2}) and B6(iii). Fix is to change d=3 to d=2 in the two cited calls; derivable directly from the cited foundation ASN.
```
