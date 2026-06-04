# Channel Assignment — ASN-0087 review-63

**Date:** 2026-06-04 02:34

## Issue 1: D-CTG★ proof discharges a case the operation's own convention excludes
Reason: Internal. The ASN already commits to fork (a) via M-DepthConv: MAKELINK is the only operation invoking K.μ⁺_L, so every first link is placed at `m = 2` and S8-depth pins `m_L(d) = 2` thereafter — `m_L(d) > 2` is unreachable within the spec's own operation set. Reducing the discharge to the one-line depth-2 initial-segment argument requires no external evidence or design intent; the convention that excludes the interior case is stated in the ASN itself.

## Issue 2: S2 cross-subspace exclusion cites the wrong source for `v₁ = s_C`
Reason: Internal. The correct justification is purely definitional — `V_{s_C}(d) = {v : subspace(v) = s_C}` together with `subspace(v) = v₁` (SubspaceProjection, ASN-0036) — both already available in the ASN's referenced foundations. Swapping the citation from S8a to the subspace definition and projection is a self-contained fix.
