# Review of ASN-0075

This ASN defines an observational operation cleanly: the three-state classification is sound, the necessity argument (D-DISCR) constructs a genuine pair of indistinguishable-on-`(C,L,E,M)` states, and the worked example concretely verifies D-EXH/D-IDENT/D-ORIG/D-SYM. I found no correctness defects in the proofs. The findings below are all accretion/meta-prose — which this note's classifier asks be surfaced at source.

## REVISE

### Issue 1: D-BOUND axiom carries rationale-prose, not statement-prose
**ASN-0075, "The SHOWDELETIONS Operation" (D-BOUND)**: "The per-state invariants preserved by every elementary transition (S2, S3★, …) do not entail P4★ ... at an intermediate state inside a composite P4★ may fail ... Restricting invocation to composite boundaries is what makes P4★ and P4a available wherever the proofs in this note invoke them."
**Problem**: This paragraph explains *why the axiom is needed* (to make P4★/P4a available) rather than *what it says*, and closes with a use-site inventory ("wherever the proofs in this note invoke them"). This is the flagged "new prose around an axiom explains why it is needed" / use-site-enumeration pattern. The axiom is fully carried by its first sentence (invocation occurs at a composite boundary).
**Required**: Reduce to the axiom statement. The P4★-availability motivation, if kept at all, belongs as a one-clause note at the single point P4★ is first invoked, not as standing rationale around the axiom.

### Issue 2: D-EXH proof is announced before it is given
**ASN-0075, Lemma D-EXH**: "The proof invokes P4★ (Contains_C(Σ) ⊆ R) to exclude the impossible row; P4★ is available at the composite boundary by D-BOUND."
**Problem**: This sentence sits between the lemma statement and the `*Proof.*` marker, previewing the proof's mechanism and forward-referencing D-BOUND. The proof body itself both invokes P4★ and is already gated by the lemma's own "composite-boundary state" hypothesis. The sentence advances no reasoning the proof does not immediately repeat.
**Required**: Delete the preview sentence; let the proof body cite P4★ where it actually uses it.

### Issue 3: The L14 + S3★-aux + S3★-contrapositive + P4★ chain is unpacked three times
**ASN-0075, D-EXH proof; supplementary lemma Group 1; D-SUBSP justification**: D-EXH unpacks "a ∈ dom(C) ⟹ a ∉ dom(L) (L14); witness v must have subspace(v)=s_C (S3★-aux + S3★ link-clause contrapositive); hence (a,d) ∈ Contains_C(Σ) ⊆ R (P4★)." Group 1 then re-applies it ("by the same L14 + S3★-aux + S3★-contrapositive chain unpacked in the proof of D-EXH above"), and D-SUBSP re-unpacks the same structure again ("mirroring the chain unpacked in D-EXH").
**Problem**: The identical inference structure is spelled out at length in three locations. The conclusions differ (exclude impossible row / exclude CURRENT(a,d_B) / exclude ℓ∈ran(M(d_B))), but the mechanical chain is one argument. This is the relocated/duplicated-prose pattern that compounds across cycles.
**Required**: State the chain once as a named sub-lemma ("a content-store address witnessed in `ran(M(d))` occupies an `s_C` V-position, so P4★ forces `(a,d) ∈ R`") and cite it at the other two sites instead of re-deriving.

## OUT_OF_SCOPE

### Topic 1: Multi-document (>2) deletion families and third-document witnesses
**Why out of scope**: The binary witness structure is what this ASN specifies; generalizing to n-document families and the "deleted from both, current in a third" case (Open Questions 3, 5) is new operation territory, not a defect here.

### Topic 2: Restoration/recovery operation consuming SHOWDELETIONS output
**Why out of scope**: D-ACT establishes the output is consumable; the actual restoration operation and its origin/link-preservation guarantees (Open Question 9) are a separate operation ASN.

VERDICT: REVISE
