# Regional Review — ASN-0034/NAT-sub (cycle 1)

*2026-04-24 11:48*

### "Unique natural number characterised by" overstates axiom content
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: NAT-sub opening: "whenever `m, n ∈ ℕ` satisfy `m ≥ n`, the difference `m − n` is the unique natural number characterised by `(m − n) + n = m`."
**Issue**: "Characterised by" reads as a uniqueness claim over solutions to `x + n = m` (i.e., cancellation). The axiom establishes only that the function value satisfies the equation; uniqueness-of-solution is not derived — it would require cancellation, which is not available from what is in scope. The signature's single-valuedness gives uniqueness of the function's *output*, not uniqueness of *solutions*.

### Defensive justifications for Consequence-vs-Axiom placement
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: NAT-sub body: "Retaining it as an axiom clause would launder that derivation through a non-minimal clause, the same concern that kept NAT-order's disjointness form `m < n ⟹ m ≠ n` from being separately exported…" and the parallel paragraph for strict positivity.
**Issue**: These paragraphs defend the choice to export results as Consequences rather than axiom clauses, and cross-reference an unrelated omitted derivation in NAT-order. That is meta-commentary about axiomatization discipline, not content that advances the derivations. The derivations themselves already show the relevant content is derivable; the justificatory framing is noise the reader must skip past.

### Use-site inventory paragraph at end of NAT-sub body
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: NAT-sub final body paragraph beginning "The axiom body invokes symbols beyond ℕ's primitive membership."
**Issue**: This paragraph enumerates where `<`, `≤`, `≥`, `>`, and `+` are cited across the axiom clauses and Consequences, and reiterates which dependency supplies each. The Depends slot already records these citations with their instantiations. The paragraph is a use-site inventory that duplicates the Depends bullets in prose form rather than advancing a claim.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 145s*
