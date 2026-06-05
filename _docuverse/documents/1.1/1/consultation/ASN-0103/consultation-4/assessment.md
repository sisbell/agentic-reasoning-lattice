# Channel Assignment — ASN-0103 review-4

**Date:** 2026-06-05 00:23

## Issue 1: The entity-set ↔ baptismal-registry coupling underlying CND.own is asserted, not derived
Reason: The fix is internal — it is a formal-architecture decision among the reviewer's three options (introduce an E↔B coupling invariant, lift to a combined state model carrying B, or weaken CND.own to structural ownership), all resolvable from the ASN's own content and the foundation ASNs (0040, 0042, 0047) already in scope. Design intent is not at issue: the ASN already quotes Nelson establishing that the owned-number tree *is* the ownership record (baptism = ownership), so the coupling's intended direction is given; what remains is to either cite/prove the E↔B agreement as a foundation result or retreat to the parent-prefix guarantees the ASN-0047 state alone supports. Implementation evidence cannot discharge a cross-model formal lemma, so Gregory is not needed.
