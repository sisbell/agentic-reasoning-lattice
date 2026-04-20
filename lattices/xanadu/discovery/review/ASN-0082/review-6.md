# Review of ASN-0082

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Straddling spans — spans whose denotation crosses the insertion boundary
**Why out of scope**: A span σ with start(σ) < p < reach(σ) would be split by the insertion: the left portion preserved by I3-L, the right portion shifted by I3 (with width preserved by I3-S). The split-then-shift interaction is a corollary of I3 + I3-L + S4 (SplitPartition), not a gap in I3-S's proof. Natural follow-up for a span-level INSERT ASN.

### Topic 2: VD/VP invariant preservation across insertion
**Why out of scope**: The ASN establishes VD and VP as local axioms on M(d) and uses them to ground I3. Whether VD and VP hold for M'(d) depends on the gap region's content placement (deferred to a future INSERT ASN). Shifted positions preserve both properties — depth is maintained by TumblerAdd's result-length identity; positivity by the T4 argument in the body — but full invariant preservation requires the gap positions to also comply, which is an operation-level concern.

### Topic 3: Complete INSERT specification
**Why out of scope**: I3 is a partial specification — it constrains how existing content repositions but deliberately leaves the gap [p, shift(p, n)) unaddressed. The content-placement postcondition (mapping gap positions to freshly appended I-addresses) and the exact characterization of dom(M'(d)) belong in the INSERT operation ASN that this property feeds into.

### Topic 4: External V-position reference update mechanism
**Why out of scope**: The ASN's own open question. This is an interface concern about how systems that record V-positions (e.g., link endsets, cursors, bookmarks) track positions through shifts. It belongs in the link/reference-tracking layer, not the span algebra.

VERDICT: CONVERGED
