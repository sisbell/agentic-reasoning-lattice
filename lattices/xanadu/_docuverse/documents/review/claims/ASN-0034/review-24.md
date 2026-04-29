# Cone Review — ASN-0034/D1 (cycle 2)

*2026-04-13 20:55*

### TumblerSub formal contract omits T-membership preconditions on its operands
**Foundation**: (internal — foundation ASN)
**ASN**: TumblerSub formal contract: "*Preconditions:* a ≥ w (when a ≠ w: if zpd(a, w) exists, aₖ ≥ wₖ at k = zpd(a, w); if zpd(a, w) does not exist, the condition holds vacuously)"
**Issue**: TumblerAdd's formal contract explicitly lists `a ∈ T, w ∈ T` among its preconditions. TumblerSub's formal contract lists only `a ≥ w`. The body text says "Given two tumblers `a` (minuend) and `w` (subtrahend)," implying T-membership, but the formal contract does not state it. This matters at two points: (1) TumblerSub's own body proof of T-membership of the result appeals to "since `a, w ∈ T` requires `#a ≥ 1` and `#w ≥ 1`" — citing a fact the contract never required; and (2) D1's proof says "TumblerSub's precondition is satisfied for minuend b and subtrahend a" and checks only `b ≥ a`, because that is all the contract demands. If a formalizer translates the contract literally, the operator accepts arguments outside T and the result-membership proof has an ungrounded premise.
**What needs resolving**: TumblerSub's formal contract should explicitly require `a ∈ T` and `w ∈ T` as preconditions, parallel to TumblerAdd's contract.

---

### zpd is load-bearing in formal contracts and proofs but has no formal definition
**Foundation**: (internal — foundation ASN)
**ASN**: TumblerSub formal contract (uses `k = zpd(a, w)` in both preconditions and definition); D1 proof (establishes `zpd(b, a) = divergence(a, b)` as a bridge step)
**Issue**: The closely analogous concept Divergence receives a standalone formal definition: domain (`a, b ∈ T` with `a ≠ b`), exhaustive case analysis, exactness claim ("exactly one case applies"), and a formal contract. zpd receives only an inline description within TumblerSub's prose: "the first position at which the padded sequences disagree." Yet zpd is partial — it is undefined when the padded sequences agree everywhere — and this partiality is consequential: TumblerSub's precondition contract branches on whether zpd exists, and D1's proof must argue that zpd and Divergence coincide under specific conditions. A formalizer must extract zpd's definition (domain, codomain, partiality, relationship to zero-padding conventions, distinction from Divergence) from narrative text rather than from a citable formal definition. The D1 bridge argument ("Under our preconditions these coincide…") is well-argued but is essentially re-deriving zpd's properties from scratch because there is no definition to cite.
**What needs resolving**: zpd needs a standalone formal definition parallel to Divergence — specifying its domain (pairs of tumblers), the zero-padding convention it uses, its partiality (undefined when padded sequences agree everywhere), and its relationship to Divergence. TumblerSub's formal contract and D1's proof should then cite this definition rather than reconstructing zpd's behavior inline.
