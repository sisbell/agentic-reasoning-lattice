# Channel Assignment — ASN-0087 review-56

**Date:** 2026-06-04 01:43

## Issue 1: S8★ verification omits the content-subspace half
Reason: The fix is internal — the ASN already establishes K.μ⁺_L's frame on the content subspace (`Σ'.M(d)(v) = Σ.M(d)(v)` for prior positions) and the inheritance pattern for frame-fixed invariants, so the content-subspace decomposition with condition (c) carries to `Σ'` by the same reasoning already deployed throughout *Invariant Preservation*.

## Issue 2: M-Effect claim states "depth per M-DepthConv" for the subsequent-link case, where it does not apply
Reason: The fix is internal — the body's Effect section already states the correct depth attribution ("depth `m_L(d)`, the existing link-subspace depth") for the non-empty case, and M-DepthConv's own scope clause confines `m = 2` to first-link placement, so the table can be corrected to match the body without external input.
