# Regional Review — ASN-0034/Divergence (cycle 6)

*2026-04-24 06:10*

Reading the ASN carefully, checking what was fixed and looking for new issues the prior cycle did not flag.

Most prior findings are resolved: T3's floating `n` is gone, the "symbol-provenance" paragraphs around NAT-addcompat/NAT-cancel/NAT-discrete/NAT-wellorder are removed, NAT-cancel's "recorded as consequence because…" framing is gone, Divergence's Postconditions "tight bounds" gloss is gone, the NAT-order Depends citation no longer claims a candidate-pair uniqueness use, and Divergence case (i) is now a designating description over "least."

One new issue remains.

### Divergence Definition case (ii) carries derivation walk in a structural slot
**Class**: REVISE
**Foundation**: (internal)
**ASN**: Divergence, *Formal Contract → Definition*: "(ii) if `#a ≠ #b ∧ (A i : 1 ≤ i ≤ #a ∧ i ≤ #b : aᵢ = bᵢ)`, **NAT-order's trichotomy on `(#a, #b)` rules out `#a = #b` and splits on which length is shorter**: (ii-a) `#a < #b`, **whence the shared-position range reduces to `1 ≤ i ≤ #a`** and `divergence(a, b) = #a + 1`; or (ii-b) `#b < #a`, **whence the shared-position range reduces to `1 ≤ i ≤ #b`** and `divergence(a, b) = #b + 1`."
**Issue**: The Definition slot should designate the value `divergence(a, b)` in each sub-case; it should not walk the derivation. The bolded fragments are derivation content: "trichotomy rules out `#a = #b` and splits on which length is shorter" is reasoning over the entry condition, and "whence the shared-position range reduces to `1 ≤ i ≤ #a` [/`#b`]" is a derived fact about the precondition that is irrelevant to the returned value. The sibling axioms NAT-addcompat, NAT-cancel, NAT-discrete hold derivations in the body prose and keep their Axiom/Consequence slots clean; the main-body prose above the Formal Contract already walks the exact same trichotomy-and-range-reduction steps, so the Definition slot is duplicating that walk. Case (i) was cleaned up in the prior cycle by collapsing to a designating description; case (ii) still carries the pre-cleanup structure. The pattern (derivation content inside a structural slot) is the same pattern previously flagged around axiom-bookkeeping and symbol-provenance.
**What needs resolving**: Collapse case (ii) to just the sub-case condition and the value. A form like "case (ii): `#a ≠ #b ∧ (A i : 1 ≤ i ≤ #a ∧ i ≤ #b : aᵢ = bᵢ)`, with value `#a + 1` when `#a < #b` (sub-case (ii-a)) and `#b + 1` when `#b < #a` (sub-case (ii-b))" states the Definition without the trichotomy walk or the range-reduction gloss. The derivation stays in the body prose where it already sits.

VERDICT: REVISE
