# Review of ASN-0069

## REVISE

### Issue 1: Reviser-drift defensive prose in V10(b) and V5a
**ASN-0069, V10(b) and V5a**: "the 'and symmetrically' in this clause refers to the second instantiation, not to a free swap of the labels within a single instantiation" and "(V5a Corollary 1 — source–fork isolation — does not apply to this pair, since neither sibling fork plays the source role with respect to the other; both are forks of `d_src`.)"

**Problem**: Both are defensive clarifications pre-empting a misreading rather than advancing the argument. The first explains how to read an earlier phrase; the second imagines a misapplication of Corollary 1 to a pair its premise already excludes. V5a(a) similarly dismisses a case its own hypothesis excludes ("If `d_target = d*`, the composite is M-targeted at `d*` and clause (a)'s hypothesis excludes it"). These are the reviser-drift patterns the anti-bloat classifier flags — prose a reader must skip to follow the claim.

**Required**: Delete the clarifying asides. State V10(b)'s two directions as two instantiations of Corollary 2 without the meta-commentary on what "symmetrically" means.

### Issue 2: V7 explains why the axiom is needed rather than what it states
**ASN-0069, §"The Empty-Source Case"**: "The alternative — rejecting the operation when the source is empty — is *inadmissible* under V7. Rejection would force the user to populate the source before forking... Rejection would also make the downstream property V11... implementation-dependent" and "V7's K.δ-alone composite is not a J4 composite... We frame V7 as an *extension* of J4..."

**Problem**: V7's normative content (empty source ⇒ K.δ-alone, succeeds with `M'(d_new) = ∅`, `R' = R`) is stated in one sentence; the surrounding two paragraphs argue *why this choice rather than rejection* and *how it relates to J4*. That is rationale prose around the claim, not the claim. The relationship-to-J4 framing is also restated a third time in V0's effects block.

**Required**: Keep the normative statement and the one-line dispatch rule. Cut the "inadmissible alternative" argument and collapse the J4-extension framing to a single citation.

### Issue 3: Deferral chains and forward "we turn to it next / follows / below" pointers
**ASN-0069, §"Identity by Sub-Allocation" and §"Sharing, Not Duplication"**: "content inheritance, source–fork correspondence, and source isolation follow"; "We pause to record what V1 and V2 do *not* yet claim"; "the arrangement-extension phase is what supplies the inheritance, and we turn to it next"; "We expand their consequences in §'Structural Correspondence' below."

**Problem**: Multiple paragraphs defer to the same downstream sections and narrate the document's own structure rather than advancing reasoning. "We pause to record what V1 and V2 do not yet claim" adds nothing the labeled claims do not already bound.

**Required**: Remove the narration-of-structure sentences; let the section headers and claim labels carry sequencing.

### Issue 4: V8b non-monotonicity claim asserted without derivation
**ASN-0069, V8b**: "every other elementary kind frames `M` at both and so fixes `Π_g`."

**Problem**: V8b's "Derivation" establishes only (i) the set bound and (ii) initial coverage. The positive non-monotonicity claim — that non-`d_op`/`d_new`-targeted steps fix `Π_g` — is stated without derivation, in a lemma that otherwise derives its conjuncts. The standard "claims labeled as facts require the chain shown" applies; the one-line discharge (V5a(a) at both `d_op` and `d_new` fixes `Corr_g`, hence `Π_g`) should be written.

**Required**: Add the one-line derivation citing V5a, or demote the sentence to an explicit "by V5a" pointer.

### Issue 5: V0 Effects block carries justification prose deferring to the verification
**ASN-0069, V0**: "The R' line is a set equality, not the inclusion... that V9 alone supplies; the equality is verified by the elementary decomposition in 'The Fork Composite' verification below" and the "State of `V_{s_C}(d_op)`... Either reading produces the same Effects" paragraph.

**Problem**: A formal effects block should state the effects; the inline justifications for why a line is an equality and which evaluation state is meant are meta-prose that belongs in (and is already discharged by) the verification section. The "Either reading produces the same Effects" paragraph defends a notational choice rather than specifying the operation.

**Required**: Reduce these to parenthetical citations (e.g., `R'` line: "(set equality; verified below)") and drop the evaluation-state defense, since the frame guarantee already pins the value.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork while source is being modified
**Why out of scope**: The first Open Question (concurrency beyond the sequential atomic axiom) is correctly deferred; concurrency semantics are new territory, not a gap in this operation's derivation.

### Topic 2: Snapshot vs. living fork, descendant enumeration, counterpart correspondence
**Why out of scope**: These Open Questions name future invariants (living-fork semantics, descendant discoverability, typed-counterpart correspondence) that the I-address-identity model deliberately does not address here.

VERDICT: REVISE
