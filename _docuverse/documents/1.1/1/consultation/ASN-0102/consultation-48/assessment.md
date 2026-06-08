# Channel Assignment — ASN-0102 review-48

**Date:** 2026-06-08 00:10

## Issue 1: The "standalone composite" restriction on COPY is stipulated without justification, yet the entire coupling discharge depends on it
Reason: Deciding between (a) justifying the standalone rule and (b) dropping it requires knowing whether the restriction reflects a real constraint — Nelson can say whether COPY was meant to combine atomically with other edits, and Gregory can say whether docopy ever runs inside a multi-operation transaction. The coupling/wp mechanics for the "compose freely" rework would be internal to ASN-0047, but the choice of branch is not derivable from the ASN alone.
Nelson question: Was COPY intended to be combinable with other operations (e.g. a single COPY-then-DELETE) into one atomic transaction, or is it by design an isolated editing primitive that always stands alone?
Gregory question: In udanax-green, is docopy ever committed as part of a larger multi-operation transaction, or is each docopy always its own atomic unit bracketed by its own POOM/spanfilade writes?
