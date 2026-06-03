# Review of ASN-0098

I read the note as a self-contained account of link-projection displacement and checked each lemma's proof, the boundary cases, and the anti-bloat patterns the classifier flags.

## REVISE

(none)

I traced the load-bearing proofs and found them sound:

- **Closure schema (★)** and its instantiations (LP3★, LP13, Store Monotonicity★) are valid: each target is a conjunction of membership-persistence and value-preservation clauses, and the single-step guarantees (L12, C0/L12 of ASN-0093) are genuine instances. The induction discharges base and step correctly.
- **LP9/LP10** correctly isolate the two structural facts (strict domain change + prior-domain agreement) shared by K.μ⁺ and K.μ⁺_L (resp. K.μ⁻), and the exact-difference formulas are proved by mutual inclusion, not asserted.
- **LP10 / LP12a boundary cases** (R = ∅, full clearance) are handled explicitly, and the wp correctly degenerates to `false`.
- **LP11** uses K.μ~-FIX to justify π permuting a fixed domain; the biconditional and reverse inclusion (via π⁻¹) are both shown.
- **LP12a** is a correct weakest precondition: `enabled ∧` the pullback `project(a,i,d,Σ) ∩ R ≠ ∅`, with `dom(Σ'.M(d)) = R` justified from `R ⊆ dom(Σ.M(d))` via D-SEQ★ prefixes.
- **LP-Fin** is the most demanding proof and it holds: the prefix-agreement claim, the `#d ≤ #d_0` bound, sub-case A (separator-zero divergence excludes shorter prefixes), and sub-case B's four-way split on the chain index all close, yielding exactly `n` candidates.
- **LP12b / LP19a / LP19** correctly chain LP-Sub + LP-Fin Corollary + L0 + SC-NEQ to confine canonical-content coverage to subspace `s_C`, and the freshness contradiction is clean.

Edge cases the standard checklist demands are all addressed: empty endset and empty arrangement (degenerate configurations), full-document delete (LP10/LP12a R=∅), partial-span delete (LP10 partial-deletion paragraph), boundary insertion (LP19), transclusion/copy-to-self (LP16), reordering (LP11), and empty from/to with non-empty type (L3 degenerate case).

Anti-bloat pass: the previously-declined "self-restating bullets + roadmap" finding is confirmed already removed — the two input-bullets are directly followed by the degenerate-configuration paragraph with no restating sentence. The remaining forward references (LP12a → LP18, the K.ρ-elision parenthetical in the worked trace) are single, reading-aiding pointers, not the multi-site deferral or downstream-consumer-inventory patterns. The LP6/LP7/LP14 template-consolidation paragraph is the opposite of accretion. No essay-in-structural-slot, no axiom-rationale sub-paragraphs, no duplicated paragraphs found.

## OUT_OF_SCOPE

The Open Questions (reverse-discovery primitive, contiguity-of-projection under K.μ~, V-order/I-order reflection, link-to-link induced discovery, cross-document operation comparability, fork without link-subspace transclusion, link-canonical contraction survival) are correctly deferred — each defines new state or new operations beyond projection displacement and belongs in a successor ASN.

VERDICT: CONVERGED
