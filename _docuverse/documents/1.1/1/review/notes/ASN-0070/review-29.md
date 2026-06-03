# Review of ASN-0070

This note is mathematically sound on the points I checked closely — the F-canonical existence/uniqueness theorem (maximal-run partition, the consecutivity characterisation, the V-restricted↔full bridge lifting S9), the F-subspace biconditional via S3★-aux + L14, and the F-contig convexity argument all hold up. The seven worked configurations correctly exercise the named properties. My findings are about accumulated redundancy, which the `review-mode.anti-bloat` classifier asks me to surface, plus one structural-clarity note.

## REVISE

### Issue 1: The "denotation, not representation" disclaimer is repeated across five+ locations
**ASN-0070, multiple sections**: The same point — the postcondition fixes `⟦Σ_V^S⟧_V` and leaves representation/canonical form optional — appears in:
- Canonical Form: "We do not commit the operation's postcondition to canonical form: the abstract specification fixes only `⟦Σ_V^S⟧_V = R(d, e)|_S`."
- Computation via Decomposition: "This is *one* admissible computation. The abstract specification does not mandate the decomposition strategy."
- F-det: "Note: the operation's postcondition fixes V-restricted denotation, not representation; downstream callers needing representational identity must apply canonical-form derivation."
- F-empty: "An implementation may return any representation with empty V-restricted denotation; the canonical-form conclusion follows only after canonicalisation."
- Result Stability: "After canonical-form derivation, repeated queries also return identical representations."

**Problem**: This is the "multiple paragraphs in different sections defer to the same downstream point" pattern. The reader re-encounters the identical caveat five times.
**Required**: State it once (at Canonical Form, where it belongs) and delete the restatements; each later claim can carry at most a parenthetical pointer if truly needed.

### Issue 2: "Sub-cases as One Phenomenon" restates content already given three times
**ASN-0070, Sub-cases as One Phenomenon**: "The three results commonly distinguished — *multiple occurrences*, *fragmentation*, and *empty resolution* — are not three separate cases..."
**Problem**: Multiplicity, fragmentation, and empty result are already (a) developed in "Reachability" (total/partial/no reach), (b) exercised concretely in Configurations 2, 6, and 3, and (c) stated formally as F-multi and F-empty. This section adds no new claim — it is a fourth restatement in different words. The sixth worked configuration is even cited back into it ("The sixth worked configuration above exhibits this concretely"), confirming the overlap.
**Required**: Remove the section, or reduce it to a single cross-reference sentence; the formal lemmas and worked examples already carry the content.

### Issue 3: "Result Stability" duplicates F-det
**ASN-0070, Result Stability**: "For fixed `Σ`, repeated queries return identical denotations — by F-det below."
**Problem**: This section restates F-det (DenotationalDeterminism) and its three-part dependency (fixed state, unique inverse image, unique canonical form) in prose, then F-det restates it again with the same three-step chain. The forward reference "by F-det below" inside a section that itself precedes the lemma compounds the redundancy.
**Required**: Either fold the discursive reading into F-det's derivation or delete the standalone section.

### Issue 4: Open Questions 5, 6, and 8 orbit one question
**ASN-0070, Open Questions**:
- Q5: "must a downstream system-level contract... mandate canonical form so that the same query yields a bit-identical externally-quotable artifact?"
- Q6: "must the per-subspace family be in canonical form, or is any finite representation admissible regardless of redundancy?"
- Q8: "must the implementation expose a canonicalisation procedure, or may callers be required to derive it independently?"

**Problem**: All three are the same open question (who is responsible for canonicalisation / when is canonical form contractually required) phrased three ways.
**Required**: Consolidate into one open question.

### Issue 5: Result Form section carries two adjacent defensive justifications
**ASN-0070, Result Form and the Operation**: "The per-subspace decomposition is structurally required, not a stylistic choice." immediately followed two paragraphs later by "The representation choice is *natural and compact*, not derived from a stronger constraint."
**Problem**: Two back-to-back paragraphs justifying why the representation was chosen / how strong the requirement is. The first (per-subspace indexing forced by differing subspace depths) is load-bearing; the second is defensive meta-prose ("we adopt the span-set family because...") that the reader must work past.
**Required**: Keep the structural-necessity argument for per-subspace indexing; trim the "natural and compact, not derived from a stronger constraint" justification to the one sentence that names finiteness (M2/S8★) as the reason a span-set suffices.

## OUT_OF_SCOPE

### Topic 1: Partial-reach reporting and concurrency semantics
The first, third, and seventh Open Questions (what must be reported about unreached I-addresses; concurrency guarantees under concurrent modification; resolution-vs-content-retrieval coupling) are genuinely new territory for future ASNs, not defects here. Correctly parked.

VERDICT: REVISE
