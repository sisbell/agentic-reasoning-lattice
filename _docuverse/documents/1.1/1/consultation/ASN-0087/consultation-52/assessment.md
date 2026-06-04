# Channel Assignment — ASN-0087 review-52

**Date:** 2026-06-04 01:15

## Issue 1: Use-site inventory and downstream-naming around M-FreshExcl
Reason: Pure editorial trim — state the generic exclusion and its derivation, drop the consumer inventory and citation announcement. The mathematical content stands on its own; no design intent or implementation evidence needed.

## Issue 2: "Why the definition is shaped this way" prose around StandardAuthoring
Reason: Internal — the StandardAuthoring definition and its `F`-intersection are already present; the fix is to state the definition directly and compress the finiteness rationale. No external channel needed.

## Issue 3: Defensive exclusion of a wrong derivation route
Reason: Internal — the structural derivation (`ℓ` is an `A_L(d)` emission → form `[d,0,s_L,k]` → F's definition) is already in the text and self-sufficient; only the LP-Sub refutation needs cutting.

## Issue 4: Protocol-rationale essay in Atomicity
Reason: Internal — the load-bearing non-atomicity guarantee and `Σ_mid` characterization are already proven; the fix only removes protocol-layer speculation. No substrate evidence or design intent required.

## Issue 5: Reachability-justification prose in Atomicity
Reason: Internal — the substantive content (K.λ commits to `Σ_mid` before K.μ⁺_L is evaluated, via SequentialTransitionAxiom) is already cited; only the "not a transitional artifact" defensive framing is removed.
