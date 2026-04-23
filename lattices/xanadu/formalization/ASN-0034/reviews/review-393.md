# Regional Review — ASN-0034/Divergence (cycle 1)

*2026-04-23 00:04*

### Meta-prose in NAT-order body about axiom-slot structure
**Class**: OBSERVE
**Foundation**: (internal — NAT-order body)
**ASN**: NAT-order body: "The axiom slot introduces `<` before constraining it: the first clause `< ⊆ ℕ × ℕ` posits `<` as a binary relation on ℕ, and the three strict-total-order clauses that follow then constrain that relation. NAT-closure follows the same register for the arithmetic primitive, opening its axiom slot with the signature `+ : ℕ × ℕ → ℕ` before the unit-membership and left-identity clauses."
**Issue**: This paragraph explains the *presentation style* of the axiom slot and cross-references NAT-closure's register; it does not state anything about `<`. It is the reviser-drift pattern "prose around an axiom explains why the axiom is structured as it is rather than what it says." The same form appears in NAT-closure's body ("The axiom slot introduces `+` before constraining it…") and in NAT-wellorder's body ("The axiom body invokes the non-strict companion `≤`, which is not a primitive…"). A precise reader must skip past these paragraphs to reach axiom content.

### Defensive prose in Divergence about NAT-wellorder's role
**Class**: OBSERVE
**Foundation**: (internal — Divergence body)
**ASN**: Divergence body: "Case (i)'s value `k` is unique from the characterization alone, without appeal to NAT-wellorder… NAT-wellorder plays a distinct role — not in uniqueness, but in *existence* of a witness: when case (i) is entered from the weaker hypothesis that `S := {…}` is nonempty, NAT-wellorder supplies `min S`, whose minimality automatically discharges the `(A i : 1 ≤ i < min S : aᵢ = bᵢ)` conjunct…"
**Issue**: This paragraph is a defensive justification of *why* NAT-wellorder sits in the Depends list given that uniqueness does not need it. The `S`-nonempty hypothesis is logically equivalent to case (i)'s own existence clause, so the "weaker hypothesis" framing is a tautology dressed as an alternative entry point. The content belongs to the revision rationale, not to the definition of `divergence`.

### Use-site inventory in Divergence's NAT-order Depends entry
**Class**: OBSERVE
**Foundation**: (internal — Divergence *Depends*)
**ASN**: Divergence Depends: "NAT-order (NatStrictTotalOrder) — trichotomy at length pair `(#a, #b)` splits case (ii) into sub-cases (ii-a)/(ii-b); trichotomy at candidate pair `(k, k')` discharges case (i)'s uniqueness argument."
**Issue**: The Depends slot is being used to enumerate every call site of NAT-order's trichotomy within the definition body, which is the "use-site inventory" noise pattern. A structural declaration should name the supplied fact, not catalog its invocations. The same slot for NAT-wellorder and NAT-closure in Divergence is terser; NAT-order's entry stands out as drift.

### Case-(ii) entry condition understated in Divergence definition
**Class**: OBSERVE
**Foundation**: (internal — Divergence definition)
**ASN**: Divergence definition clause: "(ii) If `#a ≠ #b`, NAT-order's trichotomy applied to `(#a, #b)` rules out the `#a = #b` branch and leaves exactly one of `#a < #b` or `#b < #a`. In sub-case (ii-a), `#a < #b` and `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`, whence …"
**Issue**: The case-(ii) guard is written as `#a ≠ #b`, but the sub-cases additionally require shared-position agreement. When `#a ≠ #b` *and* a shared-position mismatch exists, the correct case is (i), not (ii) — agreement is needed, not just a length difference. The function is still well-defined because the exhaustiveness/mutual-exclusivity argument downstream reconciles this, but a reader parsing the definition linearly will expect `#a ≠ #b` alone to select (ii). Stating the case-(ii) guard as "no shared-position mismatch and `#a ≠ #b`" (or folding the shared-position agreement up from the sub-cases into the case header) would make the dispatch read correctly on first pass.

### Implicit NAT-discrete use in transitivity branch `k₂ < k₁`
**Class**: OBSERVE
**Foundation**: (internal — T1 proof, part (c))
**ASN**: T1 transitivity, Case `k₂ < k₁`: "Since `k₂ < k₁` and `a` has components below `k₁`, `k₂ ≤ m`."
**Issue**: The informal phrase "a has components below `k₁`" conflates two sub-situations: when `a < b` via T1(i) the bound `k₁ ≤ m` makes `k₂ < k₁ ≤ m` direct, but when `a < b` via T1(ii) the bound is `k₁ = m + 1`, so `k₂ < m + 1` requires NAT-discrete to yield `k₂ ≤ m`. The T1 Depends entry for NAT-discrete does name this site, but the proof body itself papers over which of the two derivations is in use. A single clause distinguishing the two forms would make the step discharge visibly from the cited axiom.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 265s*
