ASN-0096 written to `lattices/xanadu/discovery/notes/ASN-0096-link-projection-displacement.md` (318 lines).

The ASN develops the projection function `proj(e, d, Σ)` as the bridge between durable I-address coverage (stored in the link) and dynamic V-position presentation (computed from current arrangement). Eighteen claims organized into:

- **Still point** (LP-IMM, LP-COV, LP-CON, LP-MON, LP-SLOT, LP-TYPE) — what survives every transition
- **Moving frame** (LP-REARR, LP-CONTR, LP-EXT, LP-CROSS) — displacement modes under each K.μ family transition
- **Derived guarantees** (LP-SURV, LP-DISC) — the survival condition and discoverability criterion
- **Non-invariants** (LP-NOV, LP-NOC, LP-NOD) — what changes
- **Frame** (LP-FRAME) — arrangement transitions never touch L

Each displacement claim is derived calculationally from the projection definition plus the relevant K.μ transition semantics. Boundary cases (empty projection, boundary insertion, cross-version, cross-owner, reverse-orphan, split coverage) are worked through against the framework. Ten open questions probe directions outside the asserted guarantees — projection ordering, rendering equivalence, fork correspondence, projection composition, S5-sharing effects on cardinality.