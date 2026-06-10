# Channel Assignment — ASN-0126 review-70

**Date:** 2026-06-09 22:11

## Issue 1: The projection-bridge introduction is a use-site inventory plus structural justification
Reason: Purely an editorial restructure — deleting redundant consumer-inventory and "establish once" rationale prose, since the bridge and its B1/B2 consequences are already stated and each result is re-cited at its own use-site. No design intent or implementation evidence is at stake.

## Issue 2: "Single-source" reasons about `→_sh` before `→_sh` exists
Reason: A placement fix that relocates an already-legitimate consequence to the section where `→_sh` is defined; the claim itself is unchanged and derivable from the note's own definitions. Neither channel is needed.

## Issue 3: The gate is stated before the registry it gates on is defined
Reason: A reordering of material already present in the note (the `Σ.registry` component, coverage-class keying, C0, and well-definedness of `shape(·)` on `[K]`) so the registry precedes the gate that reads it. This is internal presentation/logical-dependency hygiene, not a question of intent or implementation.

## Issue 4: The gated-wp guard uses the partial predicate `Sh-conf` in a flat conjunction
Reason: A formal-hygiene fix internal to the note — the note already defines `Sh-conf` as partial and already resolves this in the gate by ordering (i) before (ii); applying the same conditional-conjunction or totalization choice to the wp guard is derivable from the ASN's own content.
