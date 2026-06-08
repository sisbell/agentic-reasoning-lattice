# Channel Assignment — ASN-0112 review-38

**Date:** 2026-06-08 11:21

## Issue 1: Depth-divergence / reach-tightness prose is distributed redundantly across five sites
Reason: Pure deduplication — consolidating the reach-attainment statement at the named V-ReachTight claim and trimming pointer sentences. All content is already present in the ASN; no design intent or implementation evidence is at stake.

## Issue 2: V3's "tightest bound" reads as a property of the returned span but characterizes only the constructed intermediate `reach_d`
Reason: Reframing for clarity — making explicit that V3 bounds `reach_d`, with the delivered span's reach governed by V-ReachTight. The distinction is already derived in V2/V-ReachTight; this is internal rewording.

## Issue 3: Residual rhetorical meta-prose in a structural slot
Reason: Deletion of motivational framing that restates the section header. Purely editorial, derivable from the ASN's own structure.
