# Cross-cutting Review — ASN-0034 (cycle 4)

*2026-04-17 08:46*

Reading the ASN for cross-cutting issues not in Previous Findings.

### TA1-strict's strict-addition promotion is unsourced
**Foundation**: N/A (foundation ASN — internal consistency)
**ASN**: TA1-strict (StrictOrderPreservation), Case 1 (`k = j`). The proof writes: *"At position `k = j`: TumblerAdd gives `(a ⊕ w)ₖ = aₖ + wₖ` and `(b ⊕ w)ₖ = bₖ + wₖ`. Since `aₖ < bₖ` (the divergence inequality) and natural-number addition preserves strict inequality, `aₖ + wₖ < bₖ + wₖ`."* TA1-strict's Depends lists NAT-addcompat as the sole NAT-* citation for this step.
**Issue**: "Natural-number addition preserves strict inequality" is not a single NAT-* axiom in the stated ℕ signature. NAT-addcompat axiomatises only *non-strict* order-compatibility (`n ≥ p ⟹ m + n ≥ m + p` and the right form). Promoting the strict `aₖ < bₖ` through the shared summand `wₖ` to `aₖ + wₖ < bₖ + wₖ` requires three steps under the per-step citation convention T0 establishes: NAT-order's `≤`-from-`<` clause to weaken `aₖ < bₖ` into `aₖ ≤ bₖ`; NAT-addcompat's right order-compatibility to lift to `aₖ + wₖ ≤ bₖ + wₖ`; NAT-cancel's right cancellation to rule out the equality `aₖ + wₖ = bₖ + wₖ` (which would give `aₖ = bₖ`, contradicting `aₖ < bₖ` via NAT-order's irreflexivity); NAT-order's `≤`-with-non-equality clause to convert the non-strict ≤ into the strict <. This is exactly the four-step chain GlobalUniqueness Case 5's length-collision argument spells out explicitly ("sharpens to strict because NAT-cancel's right cancellation rules out the equality... NAT-order's defining clause then converts non-strict ≤ together with non-equality into the strict"). TA1-strict elides the chain into a single phrase and cites only NAT-addcompat, violating the citation policy that both NAT-order and NAT-cancel are load-bearing for the strict promotion. The sibling property TA1 exhibits the same elision more carefully — its sub-case `j = k` cites NAT-addcompat + NAT-order but still omits NAT-cancel, which is what actually discharges the equality-rule-out step.
**What needs resolving**: Either expand TA1-strict's Case 1 step (and TA1's sub-case `j = k` step) into the full NAT-order + NAT-addcompat + NAT-cancel chain and add the missing citations to the respective Depends lists, or introduce a standalone NAT-* axiom for strict monotonicity of `+` on ℕ (parallel to NAT-sub's explicit strict-monotonicity clause) that both properties can cite directly.

## Result

Converged after 5 cycles.

*Elapsed: 3287s*
