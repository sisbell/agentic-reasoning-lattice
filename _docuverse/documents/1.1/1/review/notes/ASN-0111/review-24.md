# Review of ASN-0111

This ASN specifies READLINK as a pure store lookup. The claims (RL0–RL8, RL-WF/ARITY/GEN/REP) are technically sound, the worked read checks the load-bearing postconditions against a concrete arity-3 link plus a nested and an orphaned instance, and the foundation citations (ASN-0034/0036/0043/0047/0093/0098, all verified) are used rather than reinvented. The remaining issues are residual bloat of the kind this note's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Back-reference inventory residue in "What the read reveals that the endpoints do not"
**ASN-0111, §"What the read reveals…"**: "The type, the direction, and the whole-structure-at-once are all recoverable only from the link object — but these are precisely the guarantees already formalised at their slots (the type by RL5, the from/to asymmetry and the simultaneous grouping by RL2 and RL1)."
**Problem**: This parenthetical inventories claims already stated (RL1, RL2, RL5) without advancing the argument — it is the residue of a collapsed list (the prior cycle reduced a four-item "what's missing" list to ownership-only, and this sentence is what the collapse left behind). The rhetorical lead-in ("What would still be missing? Everything that makes the relationship a relationship. The bytes at the two ends announce neither why they are connected nor by whom.") is essay framing the reader must skip to reach the one new point, ownership.
**Required**: Delete the back-reference inventory and the rhetorical lead; open the section directly on the ownership point that RL4 carries.

### Issue 2: RL4 is slotted as an operation postcondition but is a fact about the key
**ASN-0111, RL4**: "The read does not output the home — `readlink(a, Σ)` returns endsets only. Rather, the key that names the read already encodes it…"
**Problem**: RL4 is listed among the readlink output-property claims, yet its own prose disclaims that the read produces or establishes the home — `home(a) = N(a).0.U(a).0.D(a)` is derivable by T4 projection on `a` whether or not `readlink` is ever invoked. The disclaiming clause is the tell that the claim is mis-slotted: a reader is walked through what the operation does *not* do, in a sequence of output-postconditions. (This flags the framing, not the decision to keep ownership content.)
**Required**: Restate RL4 as a remark on the read *key* — ownership is recoverable from the address a caller already holds — rather than as a numbered postcondition alongside RL1–RL3/RL5 that describe the returned value, so the "the read does not output the home" disclaimer becomes unnecessary.

## OUT_OF_SCOPE

### Topic 1: Distinguishing two links with identical recorded structure
The third Open Question (identity carried by address, not value) correctly notes that two distinct links with equal `Σ.L` values yield identical `readlink` output, since the read returns endsets only. This is properly deferred — it concerns a guarantee about the read interface's identity surface, not a defect in the present claims.

VERDICT: REVISE
