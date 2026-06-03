# Review of ASN-0068

The mathematical content is strong: CV-MAX's existence/uniqueness proof is carefully cased (left/right walks, M-aux applications, lockstep-offset analysis with the δ=0 and δ>0 split), CV-IN-N's necessity argument is concrete and correct, and the four worked examples check out against the claims (including the product-bound-not-tight observation in Example 3 and the differing-depth lockstep in Example 4). I found no gap in the derivations. The REVISE items below are all forward-reference / recap accretion, consistent with the anti-bloat classifier on this note.

## REVISE

### Issue 1: CV-ATOM closing paragraphs restate the claim and re-narrate Example 2
**ASN-0068, Atomicity and Granularity**: The claim already states "The operation defines no minimum-quotation-length cutoff..., no merge-window heuristic..., and no block-alignment constraint." The derivation then proves this ("The operation does not consult a width threshold, merge window, or block-alignment offset because no clause... references such a quantity"). A third paragraph repeats it once more — "CV-ATOM rules these out by construction" — and a fourth paragraph, "A subtle consequence of CV-ATOM in the presence of self-transclusion... Example 2 above exhibits this phenomenon concretely," re-narrates what Example 2 and the M14 reference already establish.
**Problem**: The no-cutoff statement appears three times in different words, and the self-transclusion paragraph is a backward-pointer that restates a concrete example already given. This is the "two paragraphs say the same thing" and "relocated rather than removed" pattern.
**Required**: State the no-cutoff fact once (in the claim), let the derivation prove it, and delete the self-transclusion recap paragraph (Example 2 already carries it). The Nelson "word for word" grounding may stay as one sentence; the conventional-diff analogy is legitimate motivation and may stay.

### Issue 2: "What the Result Cannot Express" recaps existing claims without advancing reasoning
**ASN-0068, What the Result Cannot Express**: Item (i) ("compareversions consults M, not R... Stale references in R cannot generate phantom correspondences") is CV-DETERM's state-dependence plus CV-IDENT in new words; item (ii) ("Independent textual matches without I-address identity are invisible") is CV-IDENT restated; item (iii) is a bare pointer to CV-PROV-FORGOTTEN.
**Problem**: The section is a recap whose content is already established by CV-IDENT, CV-PROV-FORGOTTEN, and CV-DETERM. It does not introduce a new guarantee.
**Required**: Either delete the section or reduce it to a one-line cross-reference. If the "M not R" connection to the provenance relation is the one genuinely new observation, fold that single sentence into CV-DETERM's state-dependence paragraph.

### Issue 3: Paragraph trailing CV-PROV-FORGOTTEN restates the claim
**ASN-0068, The Correspondence Relation**: Immediately after CV-PROV-FORGOTTEN, the paragraph "The pair (d_a, d_b) may be unrelated to each other — siblings forked from a common ancestor, ancestor and descendant, or wholly independent documents... The operation reports the present-state overlap; it does not reconstruct the history" repeats the claim's content (lineage is not recoverable / present-state only).
**Problem**: Restatement of the claim just made; the enumerated relationship list does not add a derivation step.
**Required**: Remove the paragraph, or keep only the concrete "siblings / ancestor-descendant / independent" enumeration if it is judged to add reader orientation, dropping the "reports overlap, not history" restatement.

## OUT_OF_SCOPE

### Topic 1: Concurrent-modification invariants and replication consistency
**Why out of scope**: The first two Open Questions (mid-comparison arrangement modification; identical results across replicated copies) are genuinely new territory belonging to future ASNs, not defects here. CV-RO and CV-DETERM correctly scope the present operation as a read-only snapshot.

### Topic 2: Counterpart links and value-level (textual) correspondence
**Why out of scope**: "What the Result Cannot Express" (ii) gestures at counterpart links in dom(L); link semantics are explicitly out of scope per the scope directive. The structural exclusion (correspondence is I-address identity, not value equality) is correctly stated by CV-IDENT and need not be elaborated further here.

VERDICT: REVISE
