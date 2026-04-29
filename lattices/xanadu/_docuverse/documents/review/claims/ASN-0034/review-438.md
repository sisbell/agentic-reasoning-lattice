# Regional Review — ASN-0034/TumblerSub (cycle 1)

*2026-04-23 04:42*

### Phantom dependencies in TumblerSub for an unstated round-trip claim
**Class**: REVISE
**Foundation**: TumblerSub *Depends* slot
**ASN**: TumblerSub formal contract lists
> "TumblerAdd (TumblerAdd) — supplies tumbler addition `⊕` for the round-trip relationship `a ⊕ (b ⊖ a) = b` under `divergence(a, b) ≤ #a` and `#a ≤ #b`."
> "NAT-addcompat (NatAdditionOrderAndSuccessor) — monotonicity of addition with respect to order on ℕ, supporting the round-trip derivation via TumblerAdd."

**Issue**: Neither TumblerSub's body nor its Postconditions state or prove the round-trip `a ⊕ (b ⊖ a) = b`. Nothing in the definition, the derivation of `aₖ > wₖ`, the membership claim, the Pos-when-defined conclusion, or the `actionPoint` identity invokes `⊕` or addition monotonicity. The two Depends entries are tagged "for the round-trip relationship" / "supporting the round-trip derivation" — content that does not exist in the claim. This is reviser drift: dependencies relocated or retained from a prior draft that included the round-trip, now orphaned.

**What needs resolving**: Either (a) remove the TumblerAdd and NAT-addcompat dependency entries (plus any prose fragment that introduced them), or (b) if the round-trip is intended to be a postcondition of TumblerSub, add the explicit claim and proof so the declared dependencies have something to support.

---

### ZPD NAT-closure justification references expressions not in ZPD's own body
**Class**: OBSERVE
**ASN**: ZPD *Depends*:
> "NAT-closure ... places `#a + 1` and `#w + 1` in ℕ in the postcondition."

**Issue**: `#a + 1` and `#w + 1` appear in ZPD's contract only indirectly, via references to Divergence's case (ii) sub-cases; they are not literal terms in ZPD's Definition, Codomain, Partiality, or Postconditions. The justification is defensible through unfolding but is one step removed from where the reader looks for `#a + 1`. Not a correctness defect.

---

### "Consequence" placed inside Preconditions slot
**Class**: OBSERVE
**ASN**: TumblerSub *Formal Contract*:
> "Preconditions: a ∈ T, w ∈ T, a ≥ w (T1). Consequence: when zpd(a, w) is defined, aₖ > wₖ at k = zpd(a, w)."

**Issue**: The Preconditions slot should carry the caller's obligations, not a derived consequence used internally to license `aₖ − wₖ`. The derivation is sound (and the body does prove it), but attaching it to the Preconditions line conflates obligation with lemma.

---

VERDICT: REVISE
