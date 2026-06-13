# Review of ASN-0122

I checked every claim X0–X12, the worked example by full recomputation, and the foundation citations. The mathematics is sound: the correspondence relation is correctly derived as the kernel of `res` (X1/X2 cleanly separate certification from resemblance), the maximal-chain decomposition (X11) properly establishes succ as an acyclic partial injection via TS2/TS4, the clipping geometry (X4c) is genuinely worked through TS4/TS5 + T12(c) convexity, the transport lemma (X-T) is instantiated correctly across the full edit vocabulary (X7), and the six-element worked example exercises fan-out, the tie-break, clipping, and the self-comparison boundary with every count forced by the definitions. Edge cases (empty spec-set, empty document, null clip, self/disjoint/overlap windows, depth-mismatched operands) are handled. No correctness defects found.

The note carries the `review-mode.anti-bloat` classifier, and that is where the remaining issues sit: rationale that was correct at one site has been re-derived at a second.

## REVISE

### Issue 1: X12 precondition re-derives the content-subspace-clip rationale already established at its definition site
**ASN-0122, X12 (COMPARE) — Precondition**: "This last is operand hygiene marking the operand as a content query; it is *not* the content-only guarantee. `subspace(start) = s_C` constrains only the start tumbler, and a low-action-point span can still denote link-subspace positions, so content-only regions are delivered unconditionally by the region's `∩ V_{s_C}(d_i)` clip (see *State, Instances, and Spec-Sets*)."

**Problem**: This is a three-sentence restatement — plus a back-reference to the very section it restates — of the *State, Instances, and Spec-Sets* paragraph, which already establishes the identical point with a concrete example: "The `∩ V_{s_C}(d_i)` discards every such position before it becomes an instance, so a content-only region is delivered whatever the operand spans denote; `subspace(start) = s_C` is operand hygiene, not the guarantee." Each of the three X12 clauses ("operand hygiene not the guarantee," "constrains only the start tumbler / low-action-point spans still denote link positions," "delivered by the clip") is a verbatim-in-substance copy of that paragraph. A precondition slot should state the precondition crisply; here it carries the full re-derivation as essay content, and the "(see …)" pointer confirms the duplication rather than removing it.

**Required**: Reduce the X12 precondition to the precondition and a one-clause pointer, e.g. "every span a content-subspace span (`subspace(start) = s_C`) — operand hygiene, not the content-only guarantee; the guarantee is the region's `∩ V_{s_C}` clip (X9, *State, Instances, and Spec-Sets*)." Drop the re-derivation.

### Issue 2: the "value-matching over-reports / unreadable as the same part" gloss is delivered twice
**ASN-0122, *What "Correspond" Must Mean***: "A value-based relation cannot distinguish genuine sharing from coincidence, and the conflation is unrecoverable downstream: a reader of the report cannot tell 'the same part' from 'a part that happened to look the same the day someone typed it.'"

**ASN-0122, X2 discussion**: "An implementation that matched by value would over-report, and its pairs could no longer be read as 'the same part.'"

**Problem**: Both passages assert the same normative claim — value-matching conflates coincidence with sharing (over-reports), so its pairs cannot be read as "the same part." The derivation section makes it forward (to reject value-equality before X2 proves the construction); the X2 discussion makes it backward (to gloss the proven lemma). Each passage has unique surrounding material that should stay — the prose's locality/S4 angle, X2's human-asserted-equivalence boundary ("translation, parallel passage … a human act," which is a legitimate does-not-do statement) — but the shared over-report gloss is stated in full at both sites.

**Required**: Carry the over-report/"same part" gloss at one site (X2's discussion is the natural anchor, since X2 is its formal witness) and let the derivation section reference it rather than restate it, or vice versa. Keep each passage's distinct content.

## OUT_OF_SCOPE

The note's Open Questions correctly defer the genuinely new territory (n-way alignment composed from pairwise reports, the consistency contract for a derived/cached correspondence index, correspondence to content arranged in neither operand, and subspace-vocabulary extension) to future work rather than smuggling claims about them into this ASN. No improper inclusion to flag — the operation stays within "compare two spec-sets," and the retired/relocated neighbors (version creation, document discovery, deletion comparison, etc.) are absent as expected.

VERDICT: REVISE
