# Review of ASN-0084

The technical core is sound: the bijection proofs (R-PPERM, R-SPERM), coverage arguments (R-PIV, R-SWP), R-COMM, and the phased R-BLK transformation hold up, and the six worked examples genuinely cover distinct sub-cases (forward/fixed/backward μ, empty exterior, non-S pass-through). My findings are concentrated in accreted meta-prose (the anti-bloat directive) plus one citation imprecision.

## REVISE

### Issue 1: The "B′ is not maximal" caveat is restated five times
**ASN-0084, Correspondence-Run Decomposition / R-BLK statement / R-BLK body / R-BLK closing / Properties table**:
- preamble: "Note this is plain partition-ness; it is strictly weaker than S8's uniqueness postcondition (c)... R-BLK below establishes only that B′ is *a* run partition (disjoint and covering), not that B′ is the maximal one."
- statement: "yielding a run partition B′ ... maximality not claimed"
- body: "This is partition-ness only; it does **not** establish that B′ is the maximal (canonical) decomposition."
- closing: "B' need not itself coincide with the maximal (canonical) partition — the 4-cut worked example below exhibits a B' containing a mergeable pair..."
- table row R-BLK: "maximality not claimed"

**Problem**: The same load-bearing distinction (B′ is a partition, not the canonical/maximal one) is asserted five times in different words. This is the "two paragraphs say the same thing" pattern, compounded. A reader tracking the argument must re-confirm at each restatement that nothing new is being claimed.

**Required**: State the caveat once — at the R-BLK statement, where it scopes the postcondition. Remove the preamble forward-reference and the body/closing restatements; the worked-example demonstration of a mergeable B′ can stand on its own without re-announcing the caveat.

### Issue 2: Use-site framing and forward-defense in place of plain statements
**ASN-0084, Correspondence-Run Decomposition preamble**: "We apply S8's consistency clause per-position and label it mnemonically *S8-cons*... Separately, we use the partition property of S8's runs — every v ∈ dom(M(d)) lies in exactly one run — which we call *run-partition*..."
**ASN-0084, EXT-VAC**: "the one fact downstream reasoning consumes is the implication: when c_{n−1} ∉ V_S(d), the right-exterior subset {v ∈ V_S(d) : v ≥ c_{n−1}} is empty and c_{n−1} ∉ dom(M(d))."

**Problem**: Both passages describe what downstream reasoning *consumes* rather than asserting the fact and using it. "the one fact downstream reasoning consumes is the implication" is a use-site inventory wrapped around a one-line implication. The S8-cons / run-partition paragraph is terminology bookkeeping plus a forward pointer to R-BLK; the labels do real work but the framing ("Separately, we use...", "which we call...") is meta-prose.

**Required**: State the EXT-VAC right-exterior fact directly as a lemma-style implication without the "downstream reasoning consumes" preamble. Keep the S8-cons / run-partition labels but drop the use-site narration and the forward reference to R-BLK.

### Issue 3: EXT-VAC right-exterior cites the wrong premise
**ASN-0084, EXT-VAC**: "a depth-2 subspace-S cut c_{n−1} outside V_S(d) lies — by R-PRE(iv), which forbids gaps within [c₀, c_{n−1}) — strictly above the maximum [S, N]"

**Problem**: R-PRE(iv) is not the operative premise. The conclusion "c_{n−1} ∉ V_S(d) ⟹ ord(c_{n−1}) > N" follows from D-SEQ alone: D-SEQ gives V_S(d) = {[S, k] : 1 ≤ k ≤ N}, so any depth-2 subspace-S cut [S, q] with 1 ≤ q ≤ N would already lie in V_S(d); being outside forces q > N. R-PRE(iv) governs positions *inside* [c₀, c_{n−1}) and says nothing about where c_{n−1} sits relative to max(V_S(d)).

**Required**: Replace the parenthetical "by R-PRE(iv), which forbids gaps within [c₀, c_{n−1})" with the D-SEQ premise (V_S(d) is exactly {[S, 1], ..., [S, N]}).

## OUT_OF_SCOPE

### Topic 1: Generalization beyond the depth-2 (m₁ = 2) restriction
**Why out of scope**: The ASN restricts the text subspace to m₁ = 2 and leans on it to identify singleton ordinals [k] with k. By D-MIN/D-SEQ, V-positions at any depth m share components 1..m−1 and vary only in the last component, on which `shift` acts — so the displacement/width arithmetic would carry via a last-component projection. Generalizing the "Identification" machinery to m₁ > 2 is real rework (not new mathematics) and is appropriately deferred; I flag only that the restriction is presented as enabling the arithmetic when it is closer to a convenience than a necessity.

### Topic 2: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: Already correctly listed under Open Questions; the natural permutation class for k > 4 and the closure of rearrangement composition are new territory.

VERDICT: REVISE
