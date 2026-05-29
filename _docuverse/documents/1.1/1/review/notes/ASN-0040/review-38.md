# Review of ASN-0040

## REVISE

### Issue 1: Same deferral repeated across four sites
**ASN-0040, B0a / Bop / allocated-set / B9**: The "parent prerequisite" open question is deferred verbatim in at least four places — B0a ("Whether p must itself be baptized... is deliberately deferred to the Open Questions"), Bop PRE ("[parent prerequisite deferred to Open Questions]"), the allocated-set section ("The reverse inclusion... is deferred to the Open Questions"), and B9 ("whether the parent must itself be baptized is the open question deferred above").
**Problem**: This is the flagged pattern of multiple paragraphs deferring to the same downstream location. The reader re-encounters the identical non-answer four times.
**Required**: State the deferral once (Open Questions is the natural home) and remove the in-line restatements.

### Issue 2: B₀ non-emptiness explanation stated twice
**ASN-0040, Σ.B introduction and B₀ conf.**: The Σ.B intro argues "any activation discipline conforming to ASN-0034 forces t₀ ∈ B₀ and hence B₀ ≠ ∅"; B₀ conf. then repeats "Non-emptiness is *not* a separate clause... it is forced externally by the composition of Bridge2... and ASN-0034's `allocated(s₀) = {t₀}`."
**Problem**: Two paragraphs in different sections say the same thing in different words.
**Required**: Keep the statement at B₀ conf. (where the seed conditions live) and delete it from the Σ.B intro.

### Issue 3: TA5a "bridging restatement" note repeated nearly verbatim
**ASN-0040, B6 sufficiency, B10 Case 1, Bop B10-preservation**: The parenthetical "(B6(iii)'s uniform form `zeros(p) + (d − 1) ≤ 3` is ASN-0040's own bridging restatement, collapsing TA5a's two d-cases...)" appears three times with essentially identical wording.
**Problem**: Repeated explanatory aside; advances no new reasoning after the first occurrence.
**Required**: State the bridging relationship once (at B6, where the condition is defined) and cite it elsewhere.

### Issue 4: B1 sub-case (B) re-derives B6's necessity propagation
**ASN-0040, B1 "all other namespaces"**: The paragraph "Sub-case (B)'s propagation mechanisms differ across its configurations..." re-proves, for each failure mode (leading zero, interior adjacency, zero-budget, d≥3, trailing-zero+d=2), that every stream element violates T4 — exactly the propagation already established in B6's necessity proof.
**Problem**: Duplicated multi-paragraph argument across sections.
**Required**: In B1, cite B6's necessity result ("every element of S(p,d) violates T4 for these configurations") and drop the re-derivation.

### Issue 5: Non-circularity / document-ordering meta-prose
**ASN-0040, B_type proof, B_fin proof, Bop correctness**: B_type opens by noting B_fin is "proved independently below as a standalone induction... that appeals to nothing from B_type"; B_fin states "The argument is self-contained — it appeals to nothing from B_type"; Bop's correctness proof spends a paragraph arguing "the cross-references... are jointly inductive rather than circular."
**Problem**: Prose that justifies document ordering and non-circularity rather than advancing the argument — the flagged accretion pattern.
**Required**: Remove the self-referential circularity commentary; a simultaneous induction needs no defense of its own legitimacy.

### Issue 6: B9 critique of a prior formulation
**ASN-0040, B9 quantifier discussion**: "The earlier formulation 'B' reachable from Σ.B by a finite sequence of baptisms' was loose in two ways: it elided the state-level transition structure... and it left the registry growth ungrounded..."
**Problem**: Reviser drift — the paragraph critiques a superseded draft of this same note rather than stating the current claim. A reader of the final note has no "earlier formulation" to compare against.
**Required**: Delete the comparison; state the quantifier and its meaning directly.

### Issue 7: Idempotence stated twice
**ASN-0040, end of high-water-mark section**: "We observe that next is *idempotent in evaluation*... a second evaluation against the same B returns the same answer" is immediately followed by "Gregory's implementation confirms this precisely... both invocations would return the same address."
**Problem**: Two adjacent paragraphs assert the identical fact (query without commit leaves the registry unchanged); the same query/write distinction was already made in the introduction.
**Required**: Collapse to one statement.

### Issue 8: Use-site inventories in structural slots
**ASN-0040, Properties Introduced table and B0 commentary**: The table's Status column carries "cited by B1, B10" (B0), "cited by B8 (Case 1) and by the Bridge1 commentary and wp-analysis lift" (B0★); B0's prose adds "cited as such by the inductive proofs of B1 and B10."
**Problem**: Definition/property introductions enumerating downstream consumers rather than stating content — flagged accretion.
**Required**: Drop the consumer lists; provenance ("from B0a") is sufficient in the table.

### Issue 9: Definitions enumerating downstream consumers
**ASN-0040, B_type closing and S2 introduction**: B_type closes "B_type is the typing skeleton on which B10 builds..."; S2 opens "One structural identity... will be needed in two later arguments (B1 and B6)."
**Problem**: Same enumerate-the-consumers pattern at the definition site.
**Required**: Remove the forward inventories; let B1/B6/B10 cite S2/B_type where used.

### Issue 10: Defensive justification in the allocated-set bridge section
**ASN-0040, Relationship to ASN-0034's allocated set**: "each an obligation across the two ASNs rather than a theorem of either alone... parallel in status to B3's forward requirement..." and "Without either bridge requirement, the inclusion is unjustified."
**Problem**: Defensive prose explaining the *status* of the forward requirements rather than advancing the inclusion argument.
**Required**: Trim to the inclusion statement, the two bridge requirements, and the one-line preservation argument.

## OUT_OF_SCOPE

### Topic 1: Reverse inclusion Σ.B ⊆ allocated(Σ)
**Why out of scope**: Depends on the parent-prerequisite/ownership model, correctly deferred to Tumbler Ownership and Open Questions; not an error here.

### Topic 2: Content/Occupied predicate (B3)
**Why out of scope**: B3 is properly stated as a parametric forward requirement on a future content-storage ASN; defining Occupied now would overreach.

### Topic 3: Bulk allocation, cross-replica ordering, per-subspace contiguity
**Why out of scope**: Raised in Open Questions; new territory for future ASNs, not gaps in this one.

VERDICT: REVISE
