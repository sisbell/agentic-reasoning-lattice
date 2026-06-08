# Channel Assignment — ASN-0112 review-40

**Date:** 2026-06-08 11:47

## Issue 1: Type confusion — span equated with span-set in V12
Reason: Pure type-consistency fix derivable from the ASN's own definitions (V0/V11 fix the result type as `SpanSet` and the wp section already states "there is no `σ_d`" on the empty result). No design intent or implementation evidence is at stake.

## Issue 2: Forward-referencing restatement in the Vstream section
Reason: Editorial deletion of a restatement and a forward teaser; the reasoning being trimmed (V2, V4, V5) is already present in the ASN, so no external channel is needed.
