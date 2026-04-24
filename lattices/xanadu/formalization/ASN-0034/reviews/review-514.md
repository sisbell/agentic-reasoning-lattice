# Regional Review — ASN-0034/Span (cycle 3)

*2026-04-24 10:29*

### Presentation order: T1 and T3 used in proofs that precede their statements
**Class**: OBSERVE
**Foundation**: (foundation ASN; internal)
**ASN**: TumblerAdd proof — "so `r = w` by T3" (dominance equality branch) and "T1 case (i) at divergence position `k` yields `a ⊕ w > a`" (strict advancement); T1 proof — "The argument relies on `<` on ℕ (NAT-order) and on T3 (CanonicalRepresentation)".
**Issue**: TumblerAdd (section "Tumbler arithmetic") cites T1 and T3 in its proof, but both T1 and T3 appear later in the ASN. T1 in turn cites T3 which appears after it. The dependency graph is consistent, but the presentation inverts it. A precise reader following TumblerAdd's dominance proof must jump forward to read T3's biconditional before they can confirm that the "every component agrees and `#r = #w`, so `r = w` by T3" step is legitimate. Soundness is unaffected.

### "Length" terminology overload between T0's `#` and Span's `ℓ`
**Class**: OBSERVE
**Foundation**: (foundation ASN; internal)
**ASN**: Span — "where `s ∈ T` is a start address and `ℓ ∈ T` is a length — a positive tumbler used as a displacement whose action point satisfies `actionPoint(ℓ) ≤ #s`."
**Issue**: T0 introduces `#· : T → ℕ` as "length" (a natural number: cardinality of the component sequence). Span calls `ℓ` a "length" but `ℓ ∈ T` is a tumbler, not a natural number. The same prose then calls `ℓ` a "displacement." Two different notions of "length" are now in scope (`#a` as component count, and `ℓ` as a span-length tumbler), and the precise reader must distinguish them by context rather than by vocabulary. Soundness is unaffected but the reader must do extra bookkeeping.

VERDICT: OBSERVE

## Result

Regional review converged after 3 cycles.

*Elapsed: 2308s*
