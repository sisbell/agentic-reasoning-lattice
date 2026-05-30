# Review of ASN-0043

## REVISE

### Issue 1: CPP's "load-bearing precondition" note imagines a case the precondition already excludes
**ASN-0043, CPP — ChainPrefixPreservation**: "Note the precondition is load-bearing: a sibling advance at `#tᵢ₋₁ = p` would modify the terminal position `p` itself, which is *not* strictly beyond `p`."
**Problem**: The lemma's hypothesis is precisely `#tᵢ₋₁ > p` at every sibling-advance step. This sentence then steps outside that hypothesis to narrate what would happen at `#tᵢ₋₁ = p` — a case the precondition forbids. It explains *why the precondition is needed* rather than advancing the proof, and it imagines a scenario the carrier already excludes. This is exactly the accreted meta-prose the anti-bloat classifier targets (commit history shows this precondition was just churned). The proof is complete without it.
**Required**: Delete the sentence. The precondition stands on its own; the proof already uses `#tᵢ₋₁ > p` where needed.

### Issue 2: FSP→FSE bridge paragraph is organizational meta-prose with a forward reference
**ASN-0043, end of FSP / before FSE**: "FSP factors out the *conformance* half of a fresh-sibling extension but takes freshness (h1) and producibility (h2) as hypotheses. Several results below must also *exhibit* such a fresh sibling of an existing link. We establish that existence once."
**Problem**: This paragraph advances no reasoning. It narrates the document's factoring decision and enumerates downstream consumers ("several results below"), justifying why FSE is stated separately. FSE's own statement and proof carry all the content; the reader does not need the editorial framing. This is the "definition's introduction enumerates downstream consumers / justifies document ordering" pattern.
**Required**: Remove the paragraph; let FSE follow FSP directly with at most a one-clause lead ("We also need the existence of such a fresh sibling:").

### Issue 3: Repeated full-locator parentheticals for FSP/FSE
**ASN-0043, L9, L11b, Worked Example, and L9's formal statement**: e.g. "By FreshSiblingExistence (FSE, *A Shared Conformance Lemma* above)" (twice), "we appeal to FSP (FreshSiblingConformance, *A Shared Conformance Lemma* above)", and inside L9's formal claim "(preserved by FSP, FreshSiblingConformance, stated in *A Shared Conformance Lemma* above)".
**Problem**: The lemma names FSP/FSE are introduced once; repeating "(FreshSiblingConformance, *A Shared Conformance Lemma* above)" at each use is locator bloat. Worse, embedding such a parenthetical inside L9's *formal statement* puts proof-bookkeeping into a slot reserved for the claim itself.
**Required**: Cite as "FSP" / "FSE" after first introduction. Strip the parenthetical from L9's formal statement — preservation-by-FSP belongs in the proof, not the quantified claim.

### Issue 4: Worked example Step 4 and Step 6 restate the same L8 summary
**ASN-0043, Worked Example**: Step 4 closes "This is the structural counterpart to the earlier reflexivity check: same-coverage links match (...); disjoint-coverage links discriminate (...)." Step 6 closes "Together, Steps 4 and 6 exercise L8 in both discriminating directions: disjoint coverage forces distinct types (...); identical coverage under distinct span decompositions forces a shared type (...)."
**Problem**: Two paragraphs in the same section deliver the same match/discriminate summary of L8 in different words. The per-step `✓` verifications already establish each result; the dual prose summary is redundant.
**Required**: Keep one closing summary (Step 6's is the more complete) and drop the Step 4 counterpart sentence.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
