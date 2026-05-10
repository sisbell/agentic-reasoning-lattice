# Regional Review — ASN-0034/TA-Pos (cycle 1)

*2026-04-23 14:38*

Reading the foundation ASNs and TA-Pos for internal consistency.

### NAT-zero Depends embeds proof derivation
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: NAT-zero Depends — "NAT-order (NatStrictTotalOrder) — supplies the strict-order primitive `<` used in the second axiom clause; under the hypothesis `n < 0`, transitivity `m < n ∧ n < p ⟹ m < p` reduces the `0 < n` branch of the disjunction to `0 < 0`, and indiscernibility of `=` rewrites `n < 0` under `0 = n` to the same `0 < 0` in the equality branch; irreflexivity `¬(n < n)` then contradicts `0 < 0` in both branches, lifting the disjunction `0 < n ∨ 0 = n` to the *Consequence:* bullet `¬(n < 0)`."
**Issue**: The derivation of the Consequence is reproduced in full inside the Depends slot. The prose body above already walks the same argument. Depends should name what is used; the proof walk belongs in the body. Distinct variant of the pattern flagged for TumblerSub in Previous Findings (use-site inventories) — here the inventory is replaced by a mini-proof.

### Authoring-register cross-references are meta-prose
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: NAT-order body — "NAT-closure follows the same register for the arithmetic primitive, opening its axiom slot with the signature `+ : ℕ × ℕ → ℕ` before the unit-membership and left-identity clauses." Mirrored in NAT-closure body ("the same register NAT-order uses to posit `<` (with its axiom opening `< ⊆ ℕ × ℕ` before the strict-total-order clauses)") and again in NAT-closure's Depends ("posited directly by this axiom's first clause, in the same register NAT-order uses to posit `<`").
**Issue**: These sentences comment on how sibling axioms are structurally authored rather than on the claim at hand. They advance no obligation. The reader must parse cross-file stylistic notes to reach content. Three occurrences across two ASNs suggest reviser drift — structural-convention defense migrating into claim bodies.

### TA-Pos partition consequence lives only in prose
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: TA-Pos — "A separate consequence concerns the content of the partition: T0's clause `(A a ∈ T :: 1 ≤ #a)` guarantees that every `t ∈ T` has at least one index in range, so `Pos(t)` exhibits a nonzero component and `Zero(t)` makes every component equal to `0`."
**Issue**: The paragraph is explicitly framed as a "separate consequence" yet has no formal-contract bullet. Either it is a genuine exported fact (lift to *Consequence:*) or it is a gloss on the definitions (drop the "separate consequence" framing). The hybrid placement leaves a downstream claim citing this fact no label to cite.

### Custom slot label "Complementarity"
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: TA-Pos Formal Contract — "*Complementarity:* `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`."
**Issue**: Sibling ASNs (NAT-zero, NAT-order) use the standard label *Consequence:* for facts lifted from definitions/axioms. TA-Pos introduces a bespoke slot name for what is structurally a Consequence bullet. Inconsistent header vocabulary across foundation ASNs.

### NAT-closure prose documents a non-claim
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: NAT-closure body — "The mirrored clause `n + 0 = n` is not axiomatized here; commutativity of `+` is not enumerated, so the right-identity form is not derivable from this axiom alone."
**Issue**: The sentence exists to forestall a misread, not to advance any claim. Useful as a reader warning, but it is defensive prose around the axiom (explaining what the axiom is *not*). Flag at source before it compounds into a pattern of scoping-exclusion paragraphs in every contract.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 98s*
