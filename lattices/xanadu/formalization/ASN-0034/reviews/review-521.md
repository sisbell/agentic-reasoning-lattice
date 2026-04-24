# Regional Review — ASN-0034/TA-Pos (cycle 4)

*2026-04-24 11:35*

### T0 Depends glosses cite only one of several use sites for each NAT-* import
**Class**: OBSERVE
**Foundation**: (foundation ASN; internal)
**ASN**: T0 *Depends:* — "NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the lower bound of the nonemptiness clause `1 ≤ #a`." and "NAT-order (NatStrictTotalOrder) — supplies the non-strict relation `≤` on ℕ appearing in the nonemptiness clause `1 ≤ #a`."
**Issue**: Both glosses narrow the import to a single use site (the nonemptiness clause `1 ≤ #a`), but `1` and `≤` each appear at two additional axiom sites in T0: inside the component-projection clause's index-domain set-builder `{j ∈ ℕ : 1 ≤ j ≤ #a}`, and inside extensionality's inner quantifier `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. The peer dependency glosses in TA-Pos (e.g., NAT-closure "supplies `1 ∈ ℕ` for the numeral bounding that range") cover their single bounded-quantifier site without omission; T0's glosses invite a reader to verify coverage only at the nonemptiness clause and to wonder whether the typing and extensionality clauses rely on a different source for `1` and `≤`. Soundness is untouched — the imports are present — but the pointer-prose undersells the scope of each NAT-* reliance compared to T0's actual axiom content.

VERDICT: OBSERVE

## Result

Regional review converged after 4 cycles.

*Elapsed: 912s*
