# Review of ASN-0060

## REVISE

### Issue 1: Undefined "V-position" in OrdinalShift definition
**ASN-0060, Ordinal Shift**: "For a V-position v of depth m and natural number n ≥ 1"
**Problem**: "V-position" is not defined in this ASN or in ASN-0034. The term implies constraints (membership in the Vstream's position space) that are never specified. The lemmas I6, I7, I8 then quantify over unrestricted tumblers of length m — not V-positions — creating an inconsistency between the definition's domain and the lemmas' quantifiers. Either the operation is restricted to V-positions (in which case the lemmas need that restriction and V-position needs a definition), or the operation works for any tumbler of depth m (in which case drop the undefined term).
**Required**: Replace "V-position v" with "tumbler v" in the OrdinalShift definition, or define V-position formally. The former is simpler and matches the lemma statements.

## OUT_OF_SCOPE

### Topic 1: Reverse shift
**Why out of scope**: The natural companion — unshift(v, n) = v ⊖ δ(n, m), recovering v from shift(v, n) — belongs in a future extension. Its precondition (vₘ ≥ n) and the round-trip property via D1 are straightforward but outside this ASN's stated goal.

VERDICT: REVISE
