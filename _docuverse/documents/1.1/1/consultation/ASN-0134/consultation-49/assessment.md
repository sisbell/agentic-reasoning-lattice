# Channel Assignment — ASN-0134 review-49

**Date:** 2026-06-14 17:15

## Issue 1: "Not sequential consistency" does not follow from the stated premises; the client model is load-bearing and unstated
Reason: Internal — the note's intro already scopes the contract to "concurrent clients" ("the weakest discipline... so that the sequential semantics is faithfully presented to concurrent clients"), and G0 already states agents must self-serialize their own cross-home operations if they want ordering, so the pipelined/non-sequential client model is present in the note. The fix surfaces that model in G0/§3 and replaces the "we don't model program order" non-sequitur with "concurrent invocation ⟹ program order ≠ real-time order ⟹ linearizability ≠ SC"; no external definition or evidence is required.

## Issue 2: Duplicate paragraph + forward-pointer on K.σ frontier status (§4)
Reason: Internal — pure deletion of a redundant paragraph whose only content (realization-conditionality plus an H3 forward-pointer) is already stated in Paragraph A and restated in clause 2, the Claims table, and SAFE(c); nothing is lost by removing it.

## Issue 3: Residual meta-prose (exhaustiveness assertion, use-site inventory)
Reason: Internal — pure deletion of meta-prose (a closure/exhaustiveness assertion and a downstream use-site inventory) that advances no reasoning; the two families and the §1 stack commitment stand without it.
