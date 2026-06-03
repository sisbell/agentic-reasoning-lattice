# Channel Assignment — ASN-0071 review-20

**Date:** 2026-06-02 23:49

## Issue 1: PC proof omits the case where `t` is shorter than `#u`
Reason: The fix is internal — the missing T1 case-(ii) step is the same proper-prefix argument the ASN already uses elsewhere (e.g. the F-FILT span reasoning), requiring no design intent or implementation evidence.

## Issue 2: `find` typed as a total function but is partial
Reason: The fix is internal — the prose and companion F-iaddrs signature already establish `find` is partial, so correcting `→` to `⇀` is a self-contained consistency edit needing no external channel.
