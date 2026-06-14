# Channel Assignment — ASN-0131 review-47

**Date:** 2026-06-14 01:34

## Issue 1: The intersection ⊇ direction is *refuted* in the body but recorded as "open"
Reason: Neither channel is needed — the counterexample refuting universal ⊇ is already fully constructed in the body (the non-injective `Σ.M(d)` witness with shared I-address `a` carried by positions outside `W₁ ∩ W₂`). Promoting that negative result to a stated claim and reframing OQ4 to the genuinely unresolved refinement (which arrangement restriction recovers equality) is bookkeeping over reasoning the ASN already contains.

## Issue 2: The insert/delete `L`/`E`/`R` frame is asserted from a model that has no such stores
Reason: Neither channel is needed — the fix is purely to relabel the `L'=L ∧ E'=E ∧ R'=R` frame as *this* ASN's modeling assumption (the natural lift of ASN-0082's `(C,M)` primitive) rather than a derivation inherited from a foundation whose state has no `L`/`E`/`R`. That ASN-0082 cannot determine the lifted operation's write-set over those stores is evident from the cited foundation's own structure; the downstream argument is unchanged, so only the frame's status needs honest labeling.

## Issue 3: Transclusion section re-argues a foundation design choice without advancing RE's reasoning
Reason: Neither channel is needed — this is an editorial compression. The load-bearing content (surfacing by content identity; coverage permanence) is already carried by RE-TRANS and RE-IDENT, both present in the ASN, and the redundant paragraph only re-justifies an ASN-0043 design choice the note depends on rather than establishes. Removing or compressing it to a one-line pointer requires no design intent or implementation evidence.
