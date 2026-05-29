# Review of ASN-0053

## REVISE

### Issue 1: WR follow-up paragraph restates the proof's conclusion
**ASN-0053, WR (after the proof)**: "The width is recoverable from the endpoints. Conversely, start(σ) ⊕ width(σ) = reach(σ) by definition. So start ⊕ width determines reach (by definition of ⊕), and start and reach determine width (by D2, via reach ⊖ start)."
**Problem**: This paragraph re-derives in prose exactly what the proof just established (reach ⊖ start = width). The "start ⊕ width = reach by definition" half is the literal definition of reach already stated in the reach-function section. It is restatement, not advancement — the reader must read it to confirm it adds nothing.
**Required**: Delete the paragraph, or compress to the single new content (the bidirectional determination), without re-quoting both directions.

### Issue 2: S0 proof carries trailing essay/defensive prose
**ASN-0053, S0 (paragraph after the proof)**: "In topological terms, half-open intervals on a total order are convex. The hierarchical structure of tumbler addresses does not affect this... because `tumblercmp` compares tumblers lexicographically without treating zero-separators specially (Gregory, Q11). The ordering is flat even though the addresses are hierarchical."
**Problem**: The one-line proof already discharges convexity from T1 totality. "In topological terms... are convex" restates the conclusion; "The hierarchical structure... does not affect this" / "The ordering is flat even though..." is a defensive justification against a confusion the lexicographic order (T1) already excludes by construction. The `[1,3,0,5]` example is legitimate (concrete), but its surrounding framing is meta-prose. This is the anti-bloat pattern: prose imagining a case the carrier already excludes.
**Required**: Keep the concrete `[1,3,0,5]` instance if it aids the reader; drop the topology restatement and the "flat even though hierarchical" defensive sentences.

### Issue 3: Forward-reference restatement of TA-LC before S5
**ASN-0053, before S5**: "The composition property below depends on left cancellation of TumblerAdd: if a ⊕ x = a ⊕ y with both sides well-defined, then x = y (TA-LC, ASN-0034)."
**Problem**: This is a forward pointer ("the composition property below") that pre-states a foundation property already listed in the Properties table and re-discharged inside S5's own precondition list. The standalone announcement adds nothing the S5 proof does not state at point of use — it is the "definition's introduction enumerates downstream consumers / defers to a downstream location" pattern.
**Required**: Remove the sentence; cite TA-LC directly where S5 uses it (it already does).

### Issue 4: Ritual dual-citation accretion at property closings
**ASN-0053, S1 / S3 / S4 / S7 / S9 / S11**: e.g. S1 closes with both "Gregory confirms this from the implementation: intersecting two spans yields at most one output span (Q10)" and "Nelson confirms it from design intent..." (Q1); the pattern (one Gregory + one Nelson grounding) recurs at nearly every property.
**Problem**: Evidence grounding is appropriate for this ASN, but the uniform two-quote coda after every property has become formulaic. Where the second quote restates the first's content in the other author's words (S1, S9 "confirms both existence and uniqueness"), it is the "two paragraphs say the same thing in different words" pattern.
**Required**: Retain one grounding citation per property where the evidence is load-bearing; drop the second where it only re-affirms the same claim.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound
**Why out of scope**: The final Open Question ("Does the general difference bound extend to span-set difference?") is correctly deferred — S11d bounds single-span difference; the n-span case is genuinely new territory, not a gap in this ASN.

### Topic 2: Span behavior under address allocation / cross-level intersection
**Why out of scope**: The Open Questions on normalized-form stability under allocation and cross-level intersection touch operations and allocation dynamics, which this ASN correctly scopes out.

Note on rigor: the mathematical content is sound. WR, WF, S1–S5, S4a, S3b, S8, S9, S11–S11d all discharge their foundation preconditions explicitly, cover the boundary/containment sub-cases, and carry worked instances. S9's case split is exhaustive (the same-start-same-reach configuration is correctly excluded via TA-LC before the split). S7's negative result (no finite exact representation) is properly grounded in T0(b). No correctness or coverage defects found — the REVISE items are residual meta-prose accretion flagged under the anti-bloat classifier.

VERDICT: REVISE
