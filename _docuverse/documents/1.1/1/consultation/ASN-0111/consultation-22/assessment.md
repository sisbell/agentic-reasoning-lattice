# Channel Assignment — ASN-0111 review-22

**Date:** 2026-06-08 12:05

## Issue 1: "link store empty" is false in the orphaned worked example
Reason: Pure internal consistency fix — the correct premise (`coverage(F) ∩ dom(Σ.L) = ∅`) was derived one sentence earlier and the parallel Slot 3 argument already uses it. No design intent or implementation evidence is involved.

## Issue 2: Defensive parentheticals accrete around RL1/RL2 boundary
Reason: Editorial trim of defensive justification; RL2 stands on its own structural content (arity equality + L6 positional accessor) already present in the ASN. No external channel needed.
