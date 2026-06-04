# Channel Assignment — ASN-0091 review-61

**Date:** 2026-06-04 00:58

## Issue 1: Collapse-case realiser claim conflates an operation invocation with the empty transition
Reason: Choosing between fix (a) and (b) needs design intent on whether REARRANGE_K is meant to be total over R-PRE (Nelson), and evidence on whether the unbundled K.μ⁻/K.μ⁺ steps are independently valid with clause (ii) attaching only to the named bundle (Gregory).
Nelson question: Was REARRANGE_K intended to be defined on every input satisfying R-PRE — including ones that yield M'(d) = M(d) — or should identity-producing invocations lie outside its domain?
Gregory question: In the collapse case, are the elementary steps K.μ⁻ and K.μ⁺ each independently valid (their own preconditions met), with the non-trivial-net-effect clause (ii) borne solely by the named composite K.μ~ and not by the elementary steps?

## Issue 2: RA-adm discharged twice over for the same invariants
Reason: The fix is a clean partition of which invariants depend only on frame-fixed components versus the arrangement; this is determinable from the ASN's own dependency statements and needs no external channel.

## Issue 3: S2 derived twice with explicit cross-deferral
Reason: Purely an editorial deduplication — derive S2 once and cite by label; fully internal to the ASN.
