# Channel Assignment — ASN-0118 review-11

**Date:** 2026-06-08 23:59

## Issue 1: CP0(a) rests on an asserted "coincidence" whose one-line proof is omitted
Reason: The missing step is a formal equality between `expand(resolve(R))` and the per-position ascending reading, derivable entirely from premises the ASN already cites — ASN-0058's maximal-run lockstep (`M(d_s)(vⱼ+k) = aⱼ+k`) and C1b's V-start run ordering. No design intent or implementation evidence is at stake; the bridge is pure substrate algebra already present in the ASN.
