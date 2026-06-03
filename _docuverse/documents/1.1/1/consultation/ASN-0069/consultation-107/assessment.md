# Channel Assignment — ASN-0069 review-107

**Date:** 2026-06-03 02:58

## Issue 1: "owning document is implicit in M(d)(v)'s second argument" is incorrect
Reason: Derivable from the ASN alone — the substrate definition already states `M(d) : T ⇀ T` is the arrangement of each document, so the owning document is plainly the parameter `d`, and `M(d)(v)`'s two tumblers are `v` and `a`. The correction is a precise restatement of an object the ASN already defines.

## Issue 2: V9a's V9b carve-out is folded-in defensive prose
Reason: Purely editorial restructuring internal to the ASN — both V9a and V9b are already present, and the fix is to trim V9a's reconciliation prose and let V9b own the `origin(a) ≠ d_new` fact it already proves. No design intent or implementation evidence is at stake.
