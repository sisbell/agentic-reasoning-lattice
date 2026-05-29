# Review of ASN-0040

## REVISE

### Issue 1: Use-site inventory in B_fin
**ASN-0040, B_fin (after the proof)**: "B_fin discharges the finiteness premise that surfaces wherever a proof appeals to max(children(Σ.B, p, d))... Concretely it is invoked at: next's preconditions..., Bop's well-definedness proof..., B10's Case 2..., and B7, B8, B9..."
**Problem**: This is a downstream-consumer inventory, not reasoning. It enumerates who cites B_fin rather than advancing what B_fin says. It rots as soon as any consumer changes and is exactly the meta-prose the anti-bloat pass targets.
**Required**: Delete the paragraph. The invariant and its proof stand alone; consumers cite it where they need it.

### Issue 2: Unnecessary "joint induction" framing for B_fin/B_type
**ASN-0040, B_type proof**: "By joint induction with B_fin... The two invariants are coupled by Case 2... Forward references from B_type's case analysis to B_fin therefore refer to a hypothesis the joint inductive frame supplies at the same step, not to a separately established theorem."
**Problem**: B_fin's own proof appeals to nothing from B_type — it is a standalone induction over B0a's partition. The dependency is one-directional (B_type needs finiteness; B_fin does not need typing). Presenting them as a single joint induction, then re-presenting B_fin "as a standalone derivation," generates defensive non-circularity prose for a coupling that does not exist.
**Required**: Prove B_fin first as the independent invariant it is; have B_type cite it as an established theorem. Drop the joint-induction scaffolding and the non-circularity justification.

### Issue 3: Label-vs-corollary justification prose for B0
**ASN-0040, before the B0 statement**: "We list B0 as a primitive label rather than as a labelled corollary of B0a for two reasons. First... Second... The Properties Introduced table accordingly records B0 as derivable from B0a within ASN-0040 but retained as a primitive label for proof legibility."
**Problem**: Several paragraphs justify a document-organization choice (whether B0 is "primitive" or "corollary"). This advances no reasoning about baptism; it argues with an imagined editor. The "two corollary routes" discussion (T8 chain vs. B0a) compounds it.
**Required**: State B0, note in one clause that it follows from B0a, cite it where used. Remove the dual-route comparison and the "two reasons" justification.

### Issue 4: B0★ redundancy disclaimer
**ASN-0040, after B0★ proof**: "B0★ is not stronger than B0 in content... but the labelled corollary makes the multi-step reading citable at use sites... Subsequent proofs cite B0★ when their reasoning spans more than one transition... they cite B0 when the reasoning is local to one step."
**Problem**: Meta-prose explaining the bookkeeping distinction between two labels rather than the mathematics. The single sentence "B0★ extends B0 to finite transition sequences by induction" is the entire content.
**Required**: Keep the statement and proof; delete the citation-discipline commentary.

### Issue 5: B4 "event model subsumed" prose
**ASN-0040, B4**: "This recasts what an 'event model' with read/commit events and a precedence relation ≺ would express... The vocabulary 'commit(β₁) ≺ read(β₂)' used in earlier exposition is therefore subsumed: it says, in event terms, what 'β₁ precedes β₂ in the transition sequence' says in transition terms. We adopt the transition phrasing throughout..."
**Problem**: This narrates the history of a prior formulation that no longer appears in the note. A reader has no "earlier exposition" to reconcile against — the reference is to a deleted draft. Pure reviser-drift residue.
**Required**: State B4 in transition terms directly. Remove all reference to the superseded event vocabulary.

### Issue 6: Duplicated S(p,1) = S(p′,2) stream-identity proof
**ASN-0040, B1 proof sub-case (C)** and **B6 necessity sub-case (b), d = 1**: Both derive `S(p, 1) = S(p′, 2)` via first-element component comparison (`c₁ = [p₁,…,p_{#p−1},0,1]`) plus the shared deterministic recurrence.
**Problem**: The same multi-step argument is written out twice, in full, in two sections. Two paragraphs saying the same thing in different words.
**Required**: Prove the stream-identity lemma once (it is a property of the stream construction, not of either invariant) and cite it from both B1 and B6.

### Issue 7: Repeated "B4 ensures…" across wp derivations
**ASN-0040, wp analysis**: "B4 ensures children(B, p, d) is evaluated against the same precondition state B..." appears in near-identical form closing each of the three wp derivations, then again in "Both derivations reason about a single baptism... B4 (Atomic Baptism) discharges the serialization assumption..." and again in "The single-step B0 inside one wp derivation and the multi-step B0★... are not redundant."
**Problem**: The atomicity caveat is restated four-plus times. The last sentence defends against a redundancy charge rather than computing a wp.
**Required**: State the B4 evaluation-against-precondition-state point once for the section. Delete the per-derivation repetitions and the B0/B0★ non-redundancy paragraph.

### Issue 8: S0 citation-choice sentence
**ASN-0040, S0 proof**: "We cite T10a.7 rather than reprove the gap induction it already discharges."
**Problem**: Editorial justification of a citation decision, not reasoning. The citation itself already conveys this.
**Required**: Delete the sentence; the proof ends at the re-indexing step.

### Issue 9: B9 summary-table entry contradicts its own statement
**ASN-0040, Properties Introduced**: B9 row reads "`(A p, d, M : (E B' reachable : hwm(B', p, d) ≥ M))`".
**Problem**: Two defects. (a) The table drops the `B6(p, d)` guard that the formal statement carries — and the note explicitly argues the quantifier "matches Bop's precondition exactly... no more and no less," so the unguarded table form is wrong. (b) The table uses "`B' reachable`," the exact phrasing the B9 section deprecates as "loose in two ways" and replaces with state-level `Σ →* Σ'`. The summary retains the rejected formulation.
**Required**: Restore the `B6(p, d)` guard and the `Σ →* Σ'` state-level phrasing in the table to match the corrected statement.

### Issue 10: "Relationship to ASN-0034's allocated set" carries excess reconciliation prose
**ASN-0040, Σ.B section**: The subsection introduces Bridge1/Bridge2 (legitimate forward requirements) but surrounds them with extended prose on notation re-lettering ("ASN-0034 writes Σ for the transition vocabulary and s for individual states, whereas this ASN writes Op..."), the conditional reverse inclusion, and "The lenses differ in emphasis regardless of which inclusion is in force..."
**Problem**: The two bridge obligations are the load-bearing content; the surrounding lens/notation essay is commentary that a precise reader must skip past. The notation re-lettering is restated again at Bop's frame.
**Required**: Keep Bridge1, Bridge2, and the one inclusion they license. Compress the notation reconciliation to a single clause and remove the duplicate at Bop.

## OUT_OF_SCOPE

### Topic 1: Parent-prerequisite enforcement
**Why out of scope**: The note correctly defers "must a parent be baptized before children" to Tumbler Ownership and the Open Questions. The reverse inclusion `Σ.B ⊆ allocated(Σ)` depending on it is properly left conditional. No revision needed — flagged only to confirm this deferral is appropriate, not a gap.

META: Not applicable — the ASN defines state (Σ.B), an operation (baptize), and abstract invariants (B0–B10) that any conforming implementation must satisfy; the implementation references are evidence, not specification, so it has not drifted.

VERDICT: REVISE
