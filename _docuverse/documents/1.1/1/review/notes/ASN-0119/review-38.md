# Review of ASN-0119

I worked through the imports, the two worked transpositions (pivot `ABCDE → ACDEB` and swap `ABCDEF → AEFCDB`), the induced-permutation tables, the region displacements (pivot: β by −w_α, α by +w_β; swap: −(w_α+w_μ), w_β−w_α, w_β+w_μ), the four footprint configurations, and the two-move atomicity construction. All of the arithmetic checks out, and the derivations of RA0–RA9, S2, S3★, S8★, RA7a–c, and the boundary treatment (empty exterior, whole-document, degenerate sizes as partial-operation silence) are sound. The substance is correct. Two items remain.

## REVISE

### Issue 1: The P4a discharge invokes an induction whose measure, base, and hypothesis are never stated

**ASN-0119, "What is preserved: I-address correspondence" (P4a sub-argument)**: "...and so every reachable composite boundary — REARRANGE-interleaved or not — satisfies P4a, Σ'' among them."

**Problem**: P4a is the one invariant whose preservation is genuinely trace-relative, and the ASN handles it by case-splitting on the final composite. Both branches lean on the inductive hypothesis — Case 1 on "Σ is a composite boundary at which P4a held," Case 2 on "the hypothesis itself — P4a at Σ'' — is supplied ... by the combined induction." But the induction licensing those IH appeals is never set up. Its well-founded measure (the number of composites in the trace), its base case (Σ₀, where R₀ = ∅ makes P4a vacuous), and its step structure (case on the final composite, IH = P4a at the strictly-shorter pre-state) are all left implicit. As written, "the combined induction ... establishes ... and so every reachable composite boundary satisfies P4a, Σ'' among them" justifies a *premise* of the P4a argument (P4a at Σ'') by appeal to that argument's own *conclusion* — the textbook shape of a circularity that only an explicit measure resolves. For a note that elaborates every other invariant discharge step by step, collapsing the load-bearing induction into a one-sentence "and so" is exactly the "X follows from Y + Z is a claim, not a proof" pattern.

**Required**: State the induction: induct on the number `n` of valid composites in the trace; base `n = 0` (Σ₀, R₀ = ∅, vacuous); step on the final composite `C` with IH "P4a holds at the n-composite pre-state" — (i) `C = REARRANGE` (Case 1), (ii) `C` an ASN-0047 composite (Case 2). With the measure named, both IH appeals become legitimate, and the Case 2 conservativity remark collapses to one sentence (ASN-0047's per-composite arguments read only the pre-state, hence transfer to REARRANGE-interleaved traces).

### Issue 2: The RA1/RA2 citation cross-annotations do not line up and add parse overhead without advancing the argument

**ASN-0119, Claims table (RA1) and "The transposition as a permutation" / "What is preserved"**: RA1's source is listed as "ASN-0084 ArrangementRearrangement / R-PPERM / R-SPERM, **= RA2's source**," while RA2's own entry lists its source as "ASN-0084 R-PIV/R-SWP"; the body adds "the same source as RA2, not a result of R-RI but a hypothesis of it" and "its totality and bijectivity, together with the domain identity ..., are R-PIV and R-SWP."

**Problem**: The "= RA2's source" annotation asserts that RA1 and RA2 share a source, but the two entries name disjoint ASN-0084 lemma sets (ArrangementRearrangement / R-PPERM / R-SPERM versus R-PIV / R-SWP), so the cross-reference contradicts the table it annotates. The cross-annotations ("= RA2's source," "not a result of R-RI but a hypothesis of it") are citation bookkeeping a reader must stop and reconcile — I did, and the lemma sets do not match — without gaining any reasoning. In ASN-0084 the bijection equation `M'(d)(π(v)) = M(d)(v)` is ArrangementRearrangement plus the R-PPERM/R-SPERM correctness clauses; π's bijectivity is R-PPERM/R-SPERM; the domain identity `dom(M'(d)) = dom(M(d))` is R-PIV/R-SWP; the range equality is R-RI. The note's annotations blur these.

**Required**: Cite each result against the lemma that actually proves it (as just enumerated) and drop the "= RA2's source" / "hypothesis of it" cross-annotations; the four ASN-0084 citations stand on their own without the connective bookkeeping.

## OUT_OF_SCOPE

(none — the note stays within its declared scope of REARRANGE on the text subspace at depth 2; depth > 2, other subspaces, and the Open-Questions topics are appropriately deferred.)

VERDICT: REVISE
