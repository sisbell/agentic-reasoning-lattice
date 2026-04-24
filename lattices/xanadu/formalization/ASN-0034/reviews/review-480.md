# Regional Review — ASN-0034/TA-Pos (cycle 7)

*2026-04-24 03:25*

Reading the ASN against previous findings and scanning for residual drift or new structural issues.

All previously flagged items appear addressed:
- TA-Pos body's "Every tumbler … and none is both" paraphrase removed
- Complementarity slot is `*Consequence:*`
- Defensive meta-prose around NAT-zero indiscernibility, NAT-order implicational-form trailer, NAT-closure "callers chain" trailer, NAT-closure "strict-above reading callers need" trailer all gone
- Notation note uses the generic warning without committing to an unverifiable `0 < 0.0` counterexample
- NAT-order Depends reduced to `(none).`
- NAT-closure Depends names the exactly-one trichotomy Consequence

One new item:

### Scope-defense trailer in the TA-Pos notation note
**Class**: REVISE
**Foundation**: n/a (meta-prose / scope defense)
**ASN**: TA-Pos, "Note on notation": "`>` is reserved for a separate tumbler ordering under which zero tumblers need not all be minimal, so writing `Pos(t)` as `t > 0` would conflate the two relations. This tumbler ordering is supplied by claims outside this region and enters no obligation of TA-Pos."
**Issue**: The closing sentence — "supplied by claims outside this region and enters no obligation of TA-Pos" — defends the absence of a Depends entry for the mentioned tumbler ordering. That the ordering is external is already implicit from the note sitting outside the formal contract and the ordering appearing in no formal-contract clause. The sentence is a scope-boundary defense (reassuring the reader no dependency was missed), matching the reviser-drift pattern of prose that justifies contract decisions rather than advancing the mathematical content. The preceding sentence ("`>` is reserved for a separate tumbler ordering … would conflate the two relations") already discharges the note's purpose — warning against writing `Pos(t)` as `t > 0`.
**What needs resolving**: Drop the "This tumbler ordering is supplied by claims outside this region and enters no obligation of TA-Pos." sentence. The warning about symbol conflation is complete without an explicit scope-defense trailer.

VERDICT: REVISE
