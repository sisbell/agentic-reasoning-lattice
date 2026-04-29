# Cone Review — ASN-0034/Span (cycle 1)

*2026-04-25 22:21*

### Meta-prose introducing the three properties of ⊕
**Class**: OBSERVE
**ASN**: TumblerAdd, immediately after the proof: "Three properties of this definition — characterizations of what ⊕ does rather than postconditions to discharge — require explicit statement."
**Issue**: The three properties themselves (no carry, tail replacement, many-to-one) are concrete operational descriptions that belong in the body. The framing sentence, however, is defensive justification — it argues for inclusion rather than stating the property. A reader has to parse past it to reach content.

### Defensive use-site inventory in ActionPoint proof
**Class**: OBSERVE
**ASN**: ActionPoint derivation: "to conclude `i ∈ S` we must also establish the three remaining membership clauses `i ∈ ℕ`, `1 ≤ i`, and `i ≤ #w`; the carrier `i ∈ ℕ` holds by the universal's domain restriction, the bound `1 ≤ i` holds by hypothesis, so only `i ≤ #w` needs discharge."
**Issue**: The inventory enumerates membership obligations that the surrounding quantification already discharges trivially, then walks through them to identify the one that needs work. The walk-through pattern reads as defensive accounting rather than reasoning that advances the proof. A direct treatment ("`i ≤ #w` follows because…") would suffice.

### NAT-order not declared in TA0 and Span Depends despite precondition use
**Class**: OBSERVE
**ASN**: TA0's *Preconditions:* `a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a` — and Span's `actionPoint(ℓ) ≤ #s` — both use NAT-order's `≤` directly. Neither contract lists NAT-order in *Depends*. TumblerAdd, with the identical precondition, does list NAT-order.
**Issue**: The `≤` between two naturals (`actionPoint(·)` and `#·`) is NAT-order's defined non-strict companion. The convention elsewhere in this ASN is to declare direct uses (TumblerAdd lists T1 separately from NAT-order even though T1 depends on NAT-order). The omission is reachable transitively through ActionPoint, so no downstream consumer fails — but it is inconsistent with the citation discipline used elsewhere.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 673s*
