# Review of ASN-0100

## REVISE

### Issue 1: Partition restatement contradicts its own "stated once" promise
**ASN-0100, §Effect Three ("Scope of ASN-0082's I3 against INSERT's post-state") and §§Arrangement functionality / Referential integrity / Post-state V-position well-formedness**: "We state the partition once here and apply it throughout the invariant verification below... The per-invariant subsections do not re-explain this partition."
**Problem**: The promise is false. §Arrangement functionality restates "I3-S2 ... discharges functionality on the Left + Shifted-right + cross-subspace portion ...; the Insertion region's contribution is the explicit pairwise-disjointness argument." §Referential integrity restates "I3-S3 ... discharges referential integrity over the Left + Shifted-right + cross-subspace portion ...; the Insertion region's contribution is the freshness ...." §Post-state V-position well-formedness restates it three more times with "(cf. I3-VD)", "(cf. I3-VP)", "(cf. I3-fin)" each carrying the same Left+Shifted-right+cross-subspace / Insertion-separate split. This is the "two paragraphs say the same thing in different words" pattern, repeated 4–5 times — and the meta-sentence promising it won't happen is itself document-structure noise.
**Required**: Either keep the partition statement once and delete the per-subsection restatements (citing the named I3 lemma per invariant suffices), or delete the "stated once / subsections do not re-explain" meta-prose and accept the local restatements. Not both.

### Issue 2: Circular / imprecise citation between INS.M-exhaustive and §Atomicity uniqueness
**ASN-0100, §Atomicity ("Arrangement of `d`")**: "At the boundary, `V_{s_C}(d')` equals Left ∪ Insertion ∪ Shifted-right by INS.M-left, INS.M-insert, INS.M-shift."
**Problem**: INS.M-left, INS.M-insert, and INS.M-shift are containment/existential clauses — they establish that each region's positions are present in `M'(d)` with the stated images (⊇), not that no other `s_C` position exists (⊆). The "equals" requires the ⊆ direction, which is precisely INS.M-exhaustive. But INS.M-exhaustive's own justification reads "Because the post-state Σ' is uniquely determined across all admissible decompositions (§Atomicity, uniqueness of Σ')..." — i.e., it leans on this very §Atomicity argument. As written the two cite each other for the missing direction. The substance is salvageable (the *canonical* decomposition establishes exhaustiveness directly by step-tracking, independent of uniqueness), but the citations form a loop.
**Required**: Attribute the "equals" in §Atomicity to the canonical decomposition's directly-established exhaustiveness (the step-tracking argument inside INS.M-exhaustive), and have INS.M-exhaustive's decomposition-independence step cite that direct result + uniqueness — breaking the apparent circle.

### Issue 3: Citation-practice prose in the K.σ disambiguation
**ASN-0100, §The Operation: Formal Contract**: "Where this ASN cites ASN-0093 (for ChainEnumerationInjectivity, FirstEmissionFreshness, DisjointSubAllocatorChains, etc.), it draws on ASN-0093's lemmas about allocator chains, not its standalone composite vocabulary."
**Problem**: This sentence explains the document's own citation conventions rather than advancing the argument — meta-prose of the "use-site disambiguation" kind the anti-bloat classifier targets. The substantive content (INSERT runs under ValidComposite★, fires no K.σ) is already carried by the surrounding two sentences and by INS.frame.dom; the enumerated-lemma aside adds bookkeeping, not reasoning.
**Required**: Delete the citation-practice sentence; retain only "The operative substrate is ValidComposite★ ... INSERT admits no K.σ firing."

## OUT_OF_SCOPE

(none — the "Bounding the Scope" section and Open Questions draw the boundaries correctly; link-subspace insertion, COPY, DELETE, version derivation, and replication are all properly deferred.)

VERDICT: REVISE
