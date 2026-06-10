# Channel Assignment — ASN-0126 review-84

**Date:** 2026-06-10 02:52

## Issue 1: "stays inert until an app registers a type" contradicts the immutable-registry thesis (P1)
Reason: Internal fix. The note's own P1 (RegistryInvariance), the statement that "the registry is fixed when Σ_init is defined," and the frame conditions showing no step in `{K.σ, K.α, K.λ_sh}` touches the registry already establish that registration is construction-time-only with no runtime primitive. Aligning the prose with these existing results requires no external channel — the reviewer is not asking whether runtime registration *should* exist (a design-intent question), but pointing out the math already forecloses it and the word "until" contradicts that.
