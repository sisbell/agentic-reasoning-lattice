# Review of ASN-0075

## REVISE

### Issue 1: The "P4★ is a composite-boundary property, not a per-state invariant" rationale is restated three times in three sections

**ASN-0075, D-EXH lemma paragraph**: "The reachability hypothesis is load-bearing for the proof: it activates `P4★` (`Contains_C(Σ) ⊆ R`), which ASN-0047 establishes as a composite-boundary property — not as a per-state invariant preserved by every elementary transition. At intermediate states inside a composite, `P4★` may fail..."

**ASN-0075, D-BOUND section**: "Both `P4★` (`Contains_C(Σ) ⊆ R`) and `P4a` (historical fidelity) are composite-boundary properties of ASN-0047, not per-state invariants preserved by every elementary transition: at an intermediate state inside a composite, `P4★` may fail..."

**ASN-0075, D-RECONS section**: "P4a holds only at composite-boundary states, which is exactly where D-BOUND restricts SHOWDELETIONS to be invoked."

**Problem**: The same load-bearing fact — that `P4★`/`P4a` hold only at composite boundaries and may fail at intermediate states — is stated in near-identical words in the D-EXH paragraph and the D-BOUND section, then echoed a third time in D-RECONS. This is the "multiple paragraphs in different sections say the same thing" pattern. A reader following the D-EXH proof must re-read in D-BOUND what was already established two paragraphs earlier.

**Required**: State the fact once, at the axiom that owns it (D-BOUND). Have the D-EXH lemma simply note that its reachability hypothesis is discharged by D-BOUND, and drop the duplicated intermediate-state explanation from the D-EXH paragraph and the redundant clause in D-RECONS.

### Issue 2: D-BOUND's body is a use-site inventory / "why the axiom is needed," not a statement of what the axiom says

**ASN-0075, D-BOUND section**: "The boundary axiom discharges both at every invocation. It supplies D-EXH's `P4★` hypothesis (excluding the impossible `a ∈ ran(M(d)) ∧ (a, d) ∉ R` row), and it licenses P4a's reading of `DELETED(a, d)` as '`a` was once in `d`'s arrangement'..."

**Problem**: The axiom itself is one sentence (SHOWDELETIONS is invoked at a composite boundary). The remaining prose enumerates the axiom's downstream consumers (D-EXH's hypothesis, P4a's reading) — the flagged "definition's introduction enumerates downstream consumers" / "explains why the axiom is needed rather than what it says" pattern. The places that depend on the boundary hypothesis already invoke it locally (D-EXH's proof, the supplementary lemma, D-RECONS), so the inventory here is redundant with those call sites.

**Required**: Reduce D-BOUND to the axiom statement plus, if needed, the single observation that the per-state invariants (S2, S3★, etc.) are insufficient for `P4★`. Let the consuming proofs cite D-BOUND at their own use sites rather than pre-listing them at the axiom.

## OUT_OF_SCOPE

### Topic 1: Multi-document SHOWDELETIONS and restoration operations
The Open Questions raise families of >2 documents, witness structure, and a restoration operation that reintroduces deleted content. These are genuinely new operations/state and belong in future ASNs, not this one.

### Topic 2: Span-based finite presentation of the deletion set
The question of when the deletion set admits a finite span-set presentation (vs. singleton enumeration) is a packaging/representation concern the ASN correctly defers (D-ACT notes packaging is a representation choice). Future work.

VERDICT: REVISE
