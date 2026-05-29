# Channel Assignment — ASN-0036 review-151

**Date:** 2026-05-29 02:20

## Issue 1: D-CTG guard justification motivates with a configuration the model already excludes
Reason: Internal fix. The flagged configuration's unreachability follows from D-CTG-depth (already derived in the ASN from D-CTG + S8-fin), and the fact that all D-CTG intermediates have the form `[1,…,1,k]` with `zeros = 0` is established by D-SEQ — no design intent or implementation evidence is needed to trim the justification.

## Issue 2: S7d prose restates the S7a baptism principle
Reason: Internal fix. The required change is a prose trim removing a back-reference that re-narrates S7a's already-stated baptism principle; the object-level claim (documents allocated under the user prefix via T10a) is fully carried by S7d's axiom clause and Depends within the ASN.
