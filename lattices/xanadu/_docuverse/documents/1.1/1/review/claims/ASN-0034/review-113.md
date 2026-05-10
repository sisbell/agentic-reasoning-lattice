# Cross-cutting Review — ASN-0034 (cycle 1)

*2026-04-17 00:53*

### Systematic miscitation: NAT-* axioms not referenced by Depends lists
**Foundation**: T0 (CarrierSetDefinition) — "The standard properties of ℕ that downstream proofs cite — closure under successor and addition, strict total order, discreteness, order compatibility of addition, and well-ordering — are stated as separate axioms (NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder). Each proof cites only the ℕ facts it actually uses."
**ASN**: Throughout — ActionPoint, TA-Pos, TumblerAdd, TA1, TA5, T10a-N, Prefix, T1, T10, T0(a), TumblerSub, and others. Representative quotes: ActionPoint's Depends says "invokes T0's well-ordering of ℕ"; TA-Pos's Depends says "T0's discreteness axiom"; TumblerAdd's Depends says "T0's order-compatibility of `+`" and "T0's strict successor inequality"; TA5's Depends cites "T0's closure of ℕ under successor", "T0's discreteness", "T0's order-compatibility"; T10a-N's Depends cites "T0's discreteness", "T0's order-compatibility of addition", "T0's strict successor inequality", "T0's defining clause `m ≤ n ⟺ m < n ∨ m = n`"; T1's Depends cites "irreflexivity … trichotomy … transitivity" of `<` on ℕ "that T0 enumerates" and "T0's well-ordering of ℕ".
**Issue**: T0 explicitly delegates these facts to NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder. The Depends lists should cite the NAT-* axiom that actually supplies each step, but every citation currently attributes the step to T0. A precondition chain that says "from T0" is broken if T0 itself denies ownership and points elsewhere. This affects nearly every proof that uses successor, addition, `≤`, discreteness, or well-ordering of ℕ.
**What needs resolving**: Rewrite Depends clauses so each ℕ-level step names the NAT-* axiom that supplies it. T0 should be cited only for the carrier-set characterisation (T, `#·`, `·ᵢ`, `#a ≥ 1`, `aᵢ ∈ ℕ`).

### D2 has no Depends clause
**Foundation**: n/a — internal consistency. Every other theorem in this ASN (D0, D1, T1, T3, TA0, TumblerAdd, TumblerSub, etc.) lists a Depends clause that enumerates the facts its proof consumes.
**ASN**: D2 (DisplacementUnique), Formal Contract — only "*Preconditions*" and "*Postconditions*" are listed.
**Issue**: D2's proof invokes D1 (for the second witness), TA-LC (for cancellation), TA0 (for well-definedness of both additions), TumblerSub (for the explicit form of `b ⊖ a`), T1 (for the strict inequality at the divergence point), and ActionPoint/TA-Pos (to certify `b ⊖ a`'s action point and positivity). None are cited.
**What needs resolving**: Add a Depends clause to D2 that enumerates the properties its proof actually consumes.

### Definition (Span) and T12 omit Depends
**Foundation**: n/a — internal consistency.
**ASN**: "Definition (Span)" — contract lists only Preconditions and Definition. T12 (SpanWellDefinedness) — contract lists Preconditions, Definition, Postconditions.
**Issue**: Both contracts invoke `Pos(ℓ)` (TA-Pos), `actionPoint(ℓ)` (ActionPoint), and `s ⊕ ℓ` (TumblerAdd); T12 additionally cites TA0 for endpoint existence, TA-strict for non-emptiness, and T1 case (ii) / T3 for the prefix cases in the convexity proof. None of these are in a Depends list.
**What needs resolving**: Add Depends clauses naming the properties each contract rests on (at minimum TA-Pos, ActionPoint, TumblerAdd, TA0 for the definition; plus TA-strict, T1 for T12).

## Result

Not converged after 1 cycles.

*Elapsed: 120s*
