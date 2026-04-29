# Regional Review — ASN-0034/TA-Pos (cycle 6)

*2026-04-24 03:22*

Reading through the full ASN against the previous findings and scanning for new structural issues.

All previously flagged items appear addressed:
- "Complementarity" slot relabeled to `*Consequence:*`
- TA-Pos opening defensive/inventory passages removed
- Slot-signposting meta-prose removed from NAT-zero, NAT-order, NAT-closure bodies
- "a separate consequence" / "not an independent exportable consequence" framing removed
- NAT-order Depends slot reduced to `(none).`
- "export ... as a Consequence" and "the exactly-one trichotomy bullet" phrasings removed
- Notation note uses the generic form without committing to `0 < 1 in 0.0` counterexample
- NAT-closure body has genuine semantic unpacking (totality, closure, distinctness) without axiom paraphrase, typo, commutativity paragraph, or "callers need" trailers
- NAT-closure Depends now names the exactly-one trichotomy Consequence
- NAT-zero's em-dash aside about indiscernibility removed
- NAT-order's "familiar implicational form" trailer removed

One new item:

### Redundant English paraphrase of the complementarity equivalence
**Class**: REVISE
**Foundation**: n/a (meta-prose / paraphrase drift)
**ASN**: TA-Pos, body: "The two predicates are complementary: `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`. Every tumbler in `T` is either positive or a zero tumbler, and none is both. This equivalence rests on logic alone: …"
**Issue**: The sentence "Every tumbler in `T` is either positive or a zero tumbler, and none is both." is a third English restatement of material already expressed by the label "complementary" and the formal biconditional `Pos(t) ⟺ ¬Zero(t)` on the preceding line. It advances no reasoning — the element-level partition reading is an immediate instantiation of the predicate-level equivalence that precedes it. The following sentence ("This equivalence rests on logic alone…") then does the derivational work via bounded-quantifier DeMorgan. The middle sentence sits between the formal claim and its proof, restating the claim in words. This is the paraphrase-drift pattern prior cycles have been trimming systematically across this ASN; leaving it in signals accretion.
**What needs resolving**: Remove the "Every tumbler in `T` is either positive or a zero tumbler, and none is both." sentence. The lead-in "The two predicates are complementary:" plus the formal biconditional plus the DeMorgan derivation constitute the complete statement-and-proof; no English gloss of the biconditional is needed between them.

VERDICT: REVISE
