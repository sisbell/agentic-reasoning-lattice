# Cone Review — ASN-0034/D1 (cycle 3)

*2026-04-13 21:23*

### Divergence exhaustiveness claim depends on T3 but neither cites it nor argues it

**Foundation**: (internal — foundation ASN)
**ASN**: Divergence definition: "Exactly one case applies for any `a ≠ b`."
**Issue**: The definition asserts that its two cases are exhaustive and mutually exclusive but provides no argument. Mutual exclusivity is straightforward: if case (i) holds, some `aₖ ≠ bₖ` within shared positions exists, which falsifies case (ii)'s universal agreement. But exhaustiveness requires: if case (i) does not apply — all shared components agree — and `a ≠ b`, then `#a ≠ #b` so that case (ii) applies. The contrapositive of this step is: all shared components agree AND `#a = #b` implies `a = b`. That is exactly T3's forward direction. Without citing T3 or reproducing its argument, the exhaustiveness claim is ungrounded. The definition says the two cases "correspond to the two cases of T1," suggesting T1 provides the case structure, but T1 does not establish that every pair of distinct tumblers falls into one of these two cases — ruling out the possibility of distinct tumblers with identical lengths and components is T3's job. This matters for formalization: a TLA+ proof of Divergence's totality on `{(a, b) ∈ T × T : a ≠ b}` requires the T3 lemma in the proof obligation.
**What needs resolving**: The Divergence definition should either cite T3 when claiming exhaustiveness, or provide an inline argument (even one sentence: "If neither case holds, all shared components agree and `#a = #b`, so `a = b` by T3 — contradicting `a ≠ b`"). The dependency on T3 should be visible in the definition's citation structure.
