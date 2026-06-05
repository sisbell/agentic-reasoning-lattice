# Review of ASN-0108

I checked the load-bearing proofs independently — the W2 weakest-precondition nesting, the W4 partition induction (including the variable-`N` generalization), the W9a termination argument, and the four termination walks plus the four W5/W6/W8 hazard walks. I also verified the cut-point-only sufficiency claim in W9a (the point the prior review-14 flagged) holds: with clause-1 preserved at each cursor, every delivered link stays permanently below all later cursors by transitivity, so the finite consumable supply depletes regardless of clause-2 tail reordering. The closed-form count `⌈m/N⌉ + [N divides m]` checks against all four boundary regimes (`m=0`, `N>m`, exact multiple, non-divisible), including `[N divides 0]` firing for the empty set.

The cross-ASN references (ASN-0034 T1/T8/T9, ASN-0043 L-fin/L12/L12a, ASN-0093 K.λ, ASN-0098 LP13/LP17) are all to foundation ASNs and are used, not reinvented. The matching set `Match` is cleanly parameterized as an abstract interface, importing only M-fin (derivable) and M-mut (explicitly conditioned on the discoverability reading, with the monotone alternative flagged) — a legitimate abstraction boundary, not a hand-wave.

The claims W0–W11 are stated as properties of windowed retrieval parameterized by abstract key-properties (injective, allocation-monotone, state-stable, recoverable); the address-key vs. content-position-key discussion is motivation that derives which property each guarantee needs, not implementation mechanics. The ASN stays on the system-guarantee side.

Edge cases I specifically checked and found covered: empty matching set (`m=0`, next cursor `⊥` unchanged), first-window-short (`N>m`), exact-multiple terminal empty window, orphaned cursor survival, new-link blind spot, empty-window-iff-empty-After (so a short window under a recoverable key genuinely means exhaustion), and the bounded-instantaneous-tail-but-infinite-cumulative-inflow non-termination case.

I could not find a skipped case, an unproven conjunct, or a proof-by-similarly. The Open Questions appropriately defer multi-document allocation-monotonicity, cross-state W4 preservation, and the orphan/exhaustion ambiguity to future ASNs rather than leaving them as gaps here.

## REVISE

(none)

## OUT_OF_SCOPE

The Open Questions correctly defer future territory (multi-document global key ordering, guaranteed delivery of links created behind a non-monotone cursor, cross-state completeness, cursor-orphan disambiguation, progress/delivery correspondence). These are new ASNs, not defects in this one.

VERDICT: CONVERGED
