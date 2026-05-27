# Channel Assignment — ASN-0099 review-23

**Date:** 2026-05-27 00:33

## Issue 1: A1 introduced as applications-level axiom but is substrate-scope
Reason: The resolution choice depends on whether design intent supports promoting A1 to substrate (Nelson) and whether implementation evidence rules out incidental link allocation by K.μ⁺/K.μ⁻/K.ρ at a structural rather than behavioral level (Gregory). Both channels were already consulted to ground A1; the revision question is whether their evidence is strong enough to justify substrate promotion versus permanent applications-level placement versus weakening to monotonicity.
Nelson question: Should ASN-0047's frame clauses for K.μ⁺, K.μ⁻, and K.ρ be amended to explicitly state `L' = L`, thereby promoting A1 to a derived substrate consequence — or is there a design-intent reason these three frames should remain silent on L?
Gregory question: Does the udanax-green implementation contain any code path — present or historically — where content-extension (K.μ⁺ analogue), content-contraction (K.μ⁻ analogue), or provenance-recording (K.ρ analogue) routines could write to the LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN regions of the spanfilade, even via indirect calls or shared helpers?

## Issue 2: F4 weakening direction proof is brief and load-bearing
Reason: The fix is a one-sentence clarification at point-of-use citing the meta-level fixing of F1 already established in F4's framing paragraph. Purely internal proof restructuring.

## Issue 3: F10's chronological reading needs sharper boundary
Reason: The fix connects ChainMembershipForOrigin's contiguous-prefix claim with ChainEnumerationInjectivity's strict-increase property — both substrate claims already cited in this ASN. Derivable from the ASN's own citations.

## Issue 4: F15/F16/F17/F18/F19-filt/F19-sco derivations lean on "same structural argument"
Reason: The fix adds one-sentence verifications that the universal-quantifier structure carries the per-slot equality argument the same way the existential does. The verification reduces to L6's component-wise tuple equality and LP13's value preservation, both already cited.

## Issue 5: Empty endset and arity-out-of-range conjuncts together can deceive
Reason: The fix adds explanatory prose distinguishing two short-circuit paths through the already-stated conjunct `i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅`. Purely internal exposition.

## Issue 6: Worked example Query 10's d_b chain-position assumption
Reason: The fix is a setup-side choice — either tighten the worked-example to assume `d_b = inc(d_a, 0)` or introduce a fresh K.σ at Query 10's start to obtain a chain-frontier document. Both options are derivable from K.δ/K.σ semantics already in the ASN's substrate dependencies.

## Issue 7: "Without appreciable delay" cited from Nelson without ASN-internal grounding
Reason: The fix depends on whether "without appreciable delay" has a textual foundation source in Literary Machines or Nelson's concept notes, or whether it is paraphrased design intent without an attributable phrase. Nelson can resolve whether the quotation is sourced and whether it carries any timing-bound force or is purely motivational.
Nelson question: Is "without appreciable delay" a quoted phrase from Literary Machines or another Nelson source — and if so, does it carry any timing commitment beyond "the next query after K.λ commitment reflects the link," or is it purely motivational framing for the reader experience?
