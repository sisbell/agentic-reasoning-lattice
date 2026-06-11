# Channel Assignment — ASN-0128 review-18

**Date:** 2026-06-11 04:31

## Issue 1: SD's definiens has an unbound state variable and an unstated relation to I1a's notion
Reason: The fix is internal — binding the quantifier over reachable states, recording SD's relation to I1a's surface-emitted notion, and dropping the forward pointer are all derivable from the note's own definitions; DR's derivation already shows the all-reachable-states reading is the intended one, and I1a supplies the template.

## Issue 2: The view-selection mechanism for the enumeration surfaces is unspecified
Reason: The fix is internal — the note already commits both views, names one "default" (deciding which the unmarked call returns), establishes the active-view escape hatch in Denotation and views, and supplies the call-form precedent in `Observe_K`'s `{hist, oper}` selector; specifying the mechanism is surface syntax, not a new semantic choice requiring design intent or implementation evidence.

## Issue 3: Forward-deferral and duplicated content in the Denotation block (anti-bloat)
Reason: The fix is internal — pure deletion and consolidation of prose the note states elsewhere (I0's criterion, D3's `targets_under`), with no semantic content added or changed, so neither channel has anything to contribute.
