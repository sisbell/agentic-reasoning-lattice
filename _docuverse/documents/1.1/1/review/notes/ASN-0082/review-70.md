# Review of ASN-0082

## REVISE

### Issue 1: Weakest-precondition analysis recomputes a postcondition already discharged trivially by I3-VP

**ASN-0082, "Weakest-precondition analysis (I3-VP backwards through the shift)"**: the section derives the S8a obligation on `shift(v, n)` component-by-component (conjuncts 1–3) using TumblerAdd's piecewise behavior, NAT-addcompat, and NAT-order.

**Problem**: I3-VP already establishes exactly this — its shifted-region bullet reads "OrdShiftHom (b) ... gives directly that shift(v, n) satisfies S8a." So the wp target here is the case whose answer is *already trivially true* (a single OrdShiftHom citation). Per the review standard, a wp computed only for a postcondition that holds trivially is not analysis; it duplicates I3-VP in different words. If a wp pass is wanted, target a non-trivial postcondition where the shift interacts with something OrdShiftHom does not hand you wholesale (e.g., I3-S3 referential integrity through the shift, or the I3-CS/I3-V domain-closure interaction at the gap boundary).

**Required**: Either retarget the wp analysis to a non-trivial postcondition, or remove it and let I3-VP's one-line OrdShiftHom discharge stand.

### Issue 2: Defensive negative meta-prose in the wp conjunct on ordinal positivity

**ASN-0082, wp conjunct 2 (`vₘ + n > 0`)**: "The obligation is strict positivity only, so `n ≥ 1` discharges it on its own; **S8a's `vₘ ≥ 1` is not consumed here, and no left-operand comparison (`vₘ` versus `1`, which would require commutativity) is invoked.**"

**Problem**: The bolded clause advances no reasoning — it inventories what is *not* used and pre-empts a hypothetical commutativity objection that the claim's premises already exclude. This is the "explains around the step rather than performing it" pattern the anti-bloat classifier targets. The positive content (`n ≥ 1` gives `vₘ + n ≥ vₘ + 1 > 0`) is complete on its own.

**Required**: Delete the "is not consumed / no left-operand comparison ... is invoked" clause.

## OUT_OF_SCOPE

### Topic 1: NAT-comm introduced as a local axiom

The ASN introduces `NAT-comm` ("ℕ addition is commutative") as a *local axiom*, used in I3-S(a) and D-S(a). It is genuinely not derivable from the cited foundation: ASN-0034 supplies NAT-addcompat, NAT-closure, NAT-order, NAT-discrete, NAT-wellorder — none of which yields commutativity, and depth-1 `⊕`-commutativity is equivalent to it, not a route to it.

**Why out of scope**: The local introduction is correct and correctly labeled. But a primitive ℕ arithmetic fact belongs alongside the other NAT-* axioms in ASN-0034, not re-introduced ad hoc in a downstream ASN. Promoting it to the foundation is a foundation-edit task, not a correction to ASN-0082.

VERDICT: REVISE
