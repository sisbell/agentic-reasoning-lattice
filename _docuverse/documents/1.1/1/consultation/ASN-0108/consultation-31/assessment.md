# Channel Assignment — ASN-0108 review-31

**Date:** 2026-06-13 03:38

## Issue 1: The matched-content key's state-stability is grounded on an assumption the key's own definition violates
Reason: Resolving the inconsistency requires knowing what the spanfilade insertion-sort actually keys on for a link whose matched endset spans several I-addresses — a fixed/canonical function of the endset (reading (a), state-stable) or the specific endpoint matched in that traversal (reading (b), not state-stable). The note can only commit to (a) honestly, or downgrade to (b), if the implementation's actual sort key is established; this is the matched-content (Gregory) key, so Nelson's link-address intent does not bear on it. (W8's separate computability-vs-value-invariance clarification is internally derivable, but the central W5 resolution needs the evidence.)
Gregory question: In the udanax-green link search, when a matching link's endset spans multiple content I-addresses, does the insertion-sort that builds the result list key on the specific I-address through which discoverability was established in that traversal (so the key differs if a later traversal matches the link via a different endpoint), or on a fixed/canonical I-address derived from the endset alone (e.g., the least covered I-address, independent of which endpoint currently matches)?

## Issue 2: The "concretely" section pre-states the W5/W6/W8 verdicts before those claims exist
Reason: Purely an organizational fix — the three keys' definitions and the non-injectivity caveat stay, and the pre-stated downstream conclusions are already re-stated in W5/W6/W8; cutting the use-site inventory is internal editing requiring no external evidence.

## Issue 3: The "two permanent keys differ only at W6 / W5 and W8 vacuous for both" thesis is restated at five sites
Reason: Consolidating one comparative fact to its natural home (W6) with citations elsewhere is editorial deduplication; the fact itself is already established in the note, so no channel is needed.

## Issue 4: The allocation-orthogonality argument is duplicated across W5 and W8 with mutual cross-deferral
Reason: Stating the orthogonality argument once (W5) and citing it from W8 without restating the conclusion is internal restructuring of content already present in the ASN; no external evidence is required.
