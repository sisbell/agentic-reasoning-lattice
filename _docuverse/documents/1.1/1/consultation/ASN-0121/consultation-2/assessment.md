# Channel Assignment — ASN-0121 review-2

**Date:** 2026-06-09 01:09

## Issue 1: FL-REACH(d) overstates the relation to ASN-0098's discoverable union
Reason: The fix is internal — the correct claim (restrict to *satisfying* links) is already stated in the ASN's own closing sentence and follows from FL-EMP and FL-DEF. No design intent or implementation evidence is needed; this is a logical correction to the heading/table wording to match the proof already present.

## Issue 2: "I-address request" is used as a load-bearing qualifier but never defined
Reason: The fix is internal — the request grammar in FL-DEF admits exactly one kind of request (every component an Endset or `∗`), so the qualifier either drops (claims hold for all `q`) or must be formalized, both decidable from the ASN's own grammar. No external channel can supply a formal referent the ASN itself has not defined.
