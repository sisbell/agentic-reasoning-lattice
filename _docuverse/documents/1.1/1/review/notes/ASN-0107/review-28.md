# Review of ASN-0107

## REVISE

### Issue 1: D3 conflates the existence count with the discovery count — as written it contradicts E1/E2

**ASN-0107, "Two Anchorings" / D3 (ZeroIsPresentNotHistorical)**: "`num(Q, Σ) = 0` asserts that no link in `dom(Σ.L)` satisfies `Q` *at `Σ`*. It does not assert that no such link ever existed, nor that none is discoverable from another document or another arrangement."

**Problem**: D3's formal subject is `num(Q, Σ)`, which by the State section's definition is the **existence** count against a fixed permanent request `Q`. But for that count the claim "does not assert that no such link ever existed" is **false**. By E1 satisfaction against fixed `Q` is time-invariant per link, and by E2 `num(Q, ·)` is monotone non-decreasing; so if `num(Q, Σ) = 0` then `num(Q, Σ₀) ≤ num(Q, Σ) = 0` along every path `Σ₀ →* Σ`, i.e. no link satisfying `Q` was *ever* created. For the existence anchoring, a zero **does** assert historical absence in the store. The qualifier "nor that none is discoverable from another document or another arrangement" is meaningless for existence anchoring, which consults no arrangement at all.

The body's prose ("consulted arrangement," "leaves the discovery count," "reachable through it") and the Claims-Introduced table ("absence in the present *view*, not in the historical archive") both make clear D3 is meant about the **discovery** count `num_disc` / the state-resolved request `Q(Σ)` — where non-monotonicity (D2) genuinely lets a once-matching link drop out. But the claim as stated over `num(Q, Σ)` overreaches to the existence reading where it is contradicted by the note's own E1/E2.

**Required**: Scope D3 to the discovery count. State it over `num_disc(d_q, W, Σ)` (equivalently over the resolved request `Q(Σ)`), and note explicitly that the existence count `num(Q, Σ) = 0`, by contrast, *does* certify historical absence in the store (E1 + E2). The "ever existed / discoverable from another arrangement" disclaimers belong only to the discovery reading.

### Issue 2: Claim label `P0a` is introduced before `P0`

**ASN-0107, "State and the Counting Request" (P0a) vs "What Is Counted" (P0)**: P0a (RequestRepresentationInvariance) is stated in the State section; P0 (CountIsCardinality) is stated in the following section.

**Problem**: The `a` suffix conventionally marks a sub-claim of its parent, yet P0a appears textually before P0 is defined, and the two are in fact independent claims (one about request representation, one about the counting unit). The ordering invites the reader to look for a parent P0 that has not yet appeared.

**Required**: Either renumber so the subordinating label follows its parent, or give the request-representation claim a non-subordinate label so it does not read as a sub-claim of an undefined P0.

## OUT_OF_SCOPE

None. The deferrals the note makes (multi-document-anchored request parts; coincidence of discovery and existence counts; count-versus-retrieval staleness) are correctly routed to the Open Questions rather than asserted here.

VERDICT: REVISE
