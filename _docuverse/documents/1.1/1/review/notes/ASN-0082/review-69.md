# Review of ASN-0082

## REVISE

### Issue 1: Provenance narration around the foundation shift properties
**ASN-0082, "The Ordinal Shift"**: "We need two properties of this shift. Both are established in the foundation." … "Additionally, shift preserves structural properties, and both facts are established in the foundation rather than re-derived here."
**Problem**: The citations themselves (TS1, TS2, OrdShiftHom, all tagged ASN-0034/0036) already carry the "established in the foundation, not re-derived here" provenance. The surrounding narration ("Both are established…", "is likewise guaranteed", "both facts are established in the foundation rather than re-derived here") is meta-prose about where the facts live, not about what they say. The reader must skip past it to reach the actual property statements.
**Required**: Delete the provenance framing; state each property with its citation (e.g., "shift is order-preserving: shift(v₁,n) < shift(v₂,n) for #v₁=#v₂ (TS1)") and stop narrating that the foundation owns it.

### Issue 2: wp-analysis method-explanation and self-assessment essay
**ASN-0082, "Weakest-precondition analysis (I3-VP…)"**: "The wp computation propagates the post-state predicate backwards through the assignment to yield the pre-state obligation. Reading these obligations against the I3 contract makes explicit which preconditions the contract supplies…" and the closing "The wp surfaces *what the assignment requires* from the pre-state… confirming that the contract's preconditions are exactly the wp-derived constraints, with no slack."
**Problem**: The substance is the three discharged conjuncts (positivity 1..m−1, vₘ+n>0, m≥2). The opening paragraph explains the wp *method* and the closing paragraph editorializes about the result ("with no slack"). Both are scaffolding around the computation, not the computation.
**Required**: Drop the method preamble and the closing self-assessment; keep the substitution, the three conjuncts, and their one-line discharges.

### Issue 3: Editorial justification of non-preservation
**ASN-0082, "Arrangement invariants not preserved," Case S = 1**: "These violations are inherent to the shift's purpose: the gap is opened for new content, and the contiguity invariants are re-validated only once that content is placed."
**Problem**: The factual content — which of D-CTG/D-SEQ/D-MIN the gap violates, with the worked-example witness — is already fully stated. The quoted sentence is reassurance prose that does not advance any claim.
**Required**: Remove the sentence. The violation statements plus the worked example stand on their own.

### Issue 4: Allocation-invariant lemmas padding the preservation battery
**ASN-0082, I3-S7 and S7-post**: "S7a, S7b are predicates over `dom(C)`; since this set is unchanged and the pre-state satisfies both, the post-state satisfies them identically. S7d is a predicate over the document set…"
**Problem**: Both sub-operations provably leave the content store and document set untouched (I3-C / D-I, I3-D / D-CD). S7a/S7b/S7d/S7 are functions solely of those unchanged sets, so their preservation is vacuous — they are not arrangement invariants and lie outside the V-layer this ASN governs. Promoting them to named derived lemmas with a paragraph of argument each inflates the lemma count without exercising any shift property.
**Required**: Collapse I3-S7/S7-post to a single sentence noting that all dom(C)- and document-set-scoped invariants (S7a/b/d, S7) carry trivially because I3-C/D-I fix dom(C) and I3-D/D-CD fix the document set. Drop the per-predicate restatement.

### Issue 5: I3-V listed as an operation postcondition but admitted to be a corollary
**ASN-0082, I3 / I3-V**: "I3-V (the vacating clause) is a one-line corollary of I3-CS: any pre-state v … satisfies neither I3-CS disjunct … so v ∉ dom(M'(d))."
**Problem**: If I3-V follows in one line from I3-CS, it is a consequence of the domain-closure clause, not an independent postcondition of the operation. Listing it among the operation's postconditions (and in the registry as an "introduced" postcondition) overstates the contract's primitive content.
**Required**: Either derive I3-V once as a remark under I3-CS, or keep it as a postcondition and drop the "one-line corollary of I3-CS" derivation — not both.

## OUT_OF_SCOPE

### Topic 1: ℕ commutativity as a local axiom
The NAT-comm local axiom (`m + n = n + m`) is genuinely absent from ASN-0034's NAT-* family, so introducing it here is not a reinvention of an existing foundation definition. But ℕ commutativity belongs with NAT-addcompat/NAT-closure in the foundation, not re-declared per consuming ASN. Promoting it to ASN-0034 is a foundation extension, not a defect in this ASN.

### Topic 2: Depth > 1 generalization of gap-closure
The collision between TA4's zero-prefix precondition and S8a's componentwise positivity at intermediate components (already noted in Open Questions) is new territory for a future ASN, not a gap in the depth-2 result proved here.

VERDICT: REVISE
