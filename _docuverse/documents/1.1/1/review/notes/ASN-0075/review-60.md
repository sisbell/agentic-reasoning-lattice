# Review of ASN-0075

## REVISE

### Issue 1: P4★/P4a boundary-availability caveat restated at every use site
**ASN-0075, D-WIT / D-DISJ / D-RECONS**:
- D-WIT: "`Contains_C(Σ) ⊆ R` by P4★ — a composite-boundary property of ASN-0047, available here by the composite-boundary hypothesis."
- D-DISJ: "The argument invokes `P4★`, available by D-BOUND."
- D-RECONS: "P4a (historical fidelity, ASN-0047; available by D-BOUND)."

**Problem**: The same defensive caveat — that the invoked provenance property is boundary-scoped and therefore licensed — is reasserted at three separate sites. D-BOUND already establishes once that every invocation occurs at a composite boundary; each restatement is the "defer to the same justification" pattern the anti-bloat pass targets. The D-DISJ instance is worse: it is a use-site preview placed *before* the proof, announcing what the proof will cite.
**Required**: State the boundary-availability fact once (D-BOUND carries it) and let bare citations `(P4★, ASN-0047)` / `(P4a, ASN-0047)` stand at the use sites. Delete the "available by …" clauses and the D-DISJ preview sentence.

### Issue 2: "Documents with no shared content" edge case is a pure back-reference
**ASN-0075, Edge Cases**: "Disjoint content-subspace `R`-projections is the case of 'no shared content'; it yields `Q0` (both halves empty) by D-DISJ. See 'Vacuity of both report halves,' where the general `wp(SHOWDELETIONS, Q0)` condition and the D-DISJ sufficient condition are both established."
**Problem**: The entry establishes nothing new — it relabels D-DISJ's hypothesis as "no shared content" and points the reader back to two earlier locations. This is the cross-section deferral pattern; the precise reader gains nothing by visiting this paragraph.
**Required**: Either delete the entry (D-DISJ already covers it) or reduce to a one-line cross-reference without re-deriving the relabeling.

### Issue 3: D-NEED meta-bridge to D-DISCR
**ASN-0075, D-NEED argument**: "The increment over D-DISCR is the *scope* of the discrimination."
**Problem**: This sentence describes how D-NEED relates to the preceding lemma rather than advancing D-NEED's own claim. The substantive content — that `R`-membership distinguishes the predicates at every reachable state, not only at boundaries — is carried by the surrounding sentences. The bridge clause is reviser meta-prose.
**Required**: Remove the sentence; the next sentence ("`DELETED` and `NEVER_INCLUDED` differ on `R`-membership by their very definitions, and that difference does not depend on `Σ` being a composite boundary") states the scope point directly.

### Issue 4: Redundant "content-subspace" qualifier on R-projections
**ASN-0075, D-DISJ**: "documents with disjoint `R`-projections on the content subspace — `{a : (a, d_A) ∈ R} ∩ {a : (a, d_B) ∈ R} = ∅`".
**Problem**: Every pair in `R` already references content (K.ρ requires `a ∈ dom(C)`, and `dom(C)` is wholly `s_C`), so "on the content subspace" qualifies a set that has no other elements. The qualifier reads as defensive precision that the foundation already guarantees.
**Required**: Drop "on the content subspace" (and the matching phrase in the edge-case entry of Issue 2); `R`-projection is unambiguous.

## OUT_OF_SCOPE

### Topic 1: Multi-document and third-witness generalization
The Open Questions raise reporting against a third document and families of more than two documents. These are genuinely new territory (witness-structure beyond the binary asymmetric pair), correctly deferred, not errors here.

VERDICT: REVISE
