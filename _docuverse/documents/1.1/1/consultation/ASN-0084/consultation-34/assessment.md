# Channel Assignment — ASN-0084 review-34

**Date:** 2026-05-15 15:15

## Issue 1: R-WP citation error for V-position subspace preservation
Reason: Internal citation fix. The correct citation (OrdShiftHom (b) of ASN-0036) is already established and used in R-BLK's Scope note within this ASN; R-WP just needs to be aligned to that usage. No design intent or implementation evidence required.

## Issue 2: R-WP title misrepresents what is proved
Reason: Internal terminological/rigor issue. The fix is a choice between retitling (to match what is actually proved) or strengthening the proof with a necessity argument; both alternatives are derivable from the ASN's own definitions and Dijkstra-voice conventions. No external evidence needed.

## Issue 3: Undefined notation "subspace_V"
Reason: Pure notation cleanup. ASN-0036 already supplies `subspace` for V-position projection; replacing `subspace_V` with `subspace` is a mechanical edit within the ASN's vocabulary. No channels needed.

## Issue 4: Missing worked example for the w_α = w_β sub-case
Reason: Internal exposition gap. The formulas in R-DISP and R-SPERM already determine the Δ_μ = 0 sub-case; constructing the example requires only instantiating those formulas on a concrete document. No design intent or implementation evidence needed.
