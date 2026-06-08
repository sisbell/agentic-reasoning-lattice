# Review of ASN-0111

## REVISE

### Issue 1: RL-REP is downstream use-site inventory, not a guarantee about the read
**ASN-0111, "Invariants governing the returned structure" / Claims table**: "RL-REP (Pointer). Downstream coverage-based uses of an endset (specified elsewhere) consume the returned spans only via `coverage`, under which equal-coverage endsets are interchangeable (LP21 of ASN-0098)."
**Problem**: This is forward-reference accretion of exactly the kind the anti-bloat classifier targets. The section is titled "invariants governing the returned structure," but RL-REP states nothing about what `readlink` returns — it describes what *other, unspecified downstream operations* do with the result, deferring to "specified elsewhere." `readlink` returns the exact endsets (RL1), not coverage; equal-coverage interchangeability (LP21) is a consumer-side property that places no constraint on the read's output. The substantive coverage-interpretation content is already carried by RL5 (type-by-address via L8). RL-REP advances no claim about the read.
**Required**: Remove RL-REP from the claims and the invariant section (the downstream consumption discipline belongs to FOLLOWLINK/RETRIEVEENDSETS, not READLINK). If a returned-structure invariant about coverage is wanted, state one that constrains `readlink`'s output directly rather than its downstream consumers.

VERDICT: REVISE
