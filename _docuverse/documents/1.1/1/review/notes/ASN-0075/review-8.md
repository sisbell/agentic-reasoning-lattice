# Review of ASN-0075

## REVISE

### Issue 1: Confusing parenthetical about "adding L or E"
**ASN-0075, D-DISCR justification (end of section "Why the Provenance Relation Is Load-Bearing")**: "any system supporting SHOWDELETIONS must maintain state components C* beyond the four foundation components (C, L, E, M) collectively — adding L or E (or both) to the discriminating function does not suffice."
**Problem**: L and E are already part of (C, L, E, M). The clause "adding L or E (or both) to the discriminating function does not suffice" is logically vacuous as stated — they cannot be "added" because they are already counted. The reader cannot extract the intended meaning without reverse-engineering it. If the intent is "no projection of (C, L, E, M), including (C, L, E, M) itself, suffices — additional components are required," that should be said.
**Required**: Either delete the dash-clause (the preceding sentence is already complete and correct) or rephrase to name what additional component class is meant (e.g., "even consulting L and E as discriminators against C and M does not suffice; some component recording past arrangement state is required").

### Issue 2: Compressed gap argument in the witness run partition
**ASN-0075, D-ACT, partition argument**: "Within dom(C), every content address has element-field length 2 (each A_C(d) emits via inc(·, 0) from the length-2 first emission [d.0.s_C.1], and inc(·, 0) preserves length by TA5(c) of ASN-0034), so no element of dom(C) lies between consecutive emissions of one allocator under T1..."
**Problem**: The "so" collapses a multi-case argument into a single step. The conclusion "no element of dom(C) lies between consecutive emissions of one allocator under T1" requires excluding three classes of candidate intermediate t ∈ dom(C):
  - *Same length as a (= L_d + 3):* ruled out by T0 discreteness on the last component (k vs k+1).
  - *Length > L_d + 3:* would extend a's prefix [d.0.s_C.k], making origin(t) = d (via S7's prefix derivation), forcing t ∈ A_C(d) which emits only length-(L_d+3) — contradiction. This relies on the universality of #E = 2, not just within one allocator.
  - *Length < L_d + 3:* either a strict prefix of a (so t < a by T1 case (ii)) or in a different allocator's stream where T10 partitions T1-orderings (so t is < both or > both, not between).

The text states #E = 2 is universal in dom(C) but does not explicitly carry that fact into the gap argument's longer-length case. A reader cannot reconstruct the proof without supplying the cross-document origin reasoning and the T10 partition argument.
**Required**: Expand the gap argument to name at minimum the longer-length case explicitly — "any t ∈ dom(C) with #t > L_d + 3 starting with prefix [d.0.s_C.k] would have origin(t) = d (S7), but A_C(d) emits only at length L_d + 3 (#E = 2), contradiction" — and the cross-document case "any t ∈ dom(C) with origin(t) = d' ≠ d has document-level prefix d', and by T10 either all of d's content extensions T1-precede all of d''s or vice versa, so t cannot lie between a and shift(a, 1)."

## OUT_OF_SCOPE

(None to flag — the ASN's own Open Questions section appropriately deferred topics such as multi-document SHOWDELETIONS, concurrent transitions, deletion-from-all-witnesses, and presentation ordering to future ASNs.)

VERDICT: REVISE
