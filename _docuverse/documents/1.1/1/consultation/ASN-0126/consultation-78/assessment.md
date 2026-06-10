# Channel Assignment — ASN-0126 review-78

**Date:** 2026-06-10 01:12

## Issue 1: ASN-0086's state-indexed functions `L_K`, `A_K`, `nullified` are used on the four-component state without a lifting convention
Reason: Internal fix. The registry is the only added component, and ASN-0086's functions are defined over three-component states that predate it, so they trivially read only C/M/L — the note's own B1 already runs exactly this argument for `a_emit` and `A_rel`; generalizing it to all five functions reuses reasoning already present, requiring no design intent or implementation evidence.

## Issue 2: The Binary wrapper's `→_sh`-step is asserted before its existence is established (P5 forward-dependency)
Reason: Internal fix. Both repair options — forward-citing P5 (GateRealizability) or discharging the gate inline via `Sh-conf(R, {r}, {(a, δ(1, #a))}) = ⊤` from R's Binary registration and `|F| = |G| = 1` — use only results and definitions already in the note; this is a citation/ordering adjustment, not a question of intent or implementation.

## Issue 3: The retraction proof re-explains B2's transferability scope already fixed in the bridge section
Reason: Internal fix. The repair deletes a redundant restatement of B2's carrying conditions, which "The projection bridge" already fixes, replacing it with a citation; pure prose trimming derivable from the ASN's own structure.
