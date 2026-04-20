# Cone Review — ASN-0034/PositiveTumbler (cycle 2)

*2026-04-16 21:53*

### Dangling citation to TA-Pos in T1's Depends clause
**Foundation**: n/a (foundation ASN, internal)
**ASN**: T1 (LexicographicOrder), *Depends* clause: "…so the least-element claim is discharged from T0 rather than left implicit, matching the per-step citation convention established for `ActionPoint` and `TA-Pos`."
**Issue**: The justification note appeals to a convention "established for `ActionPoint` and `TA-Pos`" as a template that T1 is following. Neither `ActionPoint` nor `TA-Pos` is stated anywhere in the visible ASN content, and the ASN declares no external dependencies. Previous findings already note ActionPoint's absence in the context of TA0's proof, but T1's Depends clause introduces a second undefined handle, `TA-Pos`, that has no counterpart in the text — no property, no definition, no forward section. A reader auditing T1's dependency chain cannot resolve what convention is being matched.
**What needs resolving**: Either define TA-Pos (and ActionPoint) as properties within this ASN so the convention reference has a live target, drop the comparison to those two properties from T1's Depends clause if they are not part of this ASN's scope, or, if the intent is to defer their definitions to a rename/promotion that has not yet landed, annotate the reference as forward-looking and state where those properties will be defined.
