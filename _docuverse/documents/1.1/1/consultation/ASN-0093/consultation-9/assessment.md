# Channel Assignment — ASN-0093 review-9

**Date:** 2026-05-18 19:02

## Issue 1: T10a.8 application to non-tree-embedded chains is meta-argued, not formally derived
Reason: The fix is to extract the existing meta-argument from the Remark into a named lemma with explicit preconditions and a self-contained proof. The substantive content (FirstEmission's T4-valid base + TA5a propagation + T10a.8's proof structure) is already inspected in the ASN; restructuring is purely formal.

## Issue 2: Chain-element T4-validity is established only in a Remark, not as a named lemma
Reason: The proof (FirstEmission base + TA5a per-step under k=0 unconditional preservation) is already stated inline in the ASN. The fix is to elevate this inline argument to a first-class named lemma with explicit preconditions and induction, and add it to the Properties Introduced table.

## Issue 3: SubAllocatorAxiom mixes axiom and derived content
Reason: The ASN itself acknowledges that Disjoint and FirstEmission's freshness conclusion are derivable, and the derivations are already exhibited in the *Remark — derivable clauses*. The fix is to strip these clauses from the axiom and restate them as named lemmas using the existing derivations.

## Issue 4: ChainMembershipForOrigin's T10a.7 contrapositive argument is muddled
Reason: This is a presentational clarity issue on a logical step (instantiating universal-quantified strict monotonicity in the correct direction). The substantive argument is correct; the fix is to rewrite it as a clean two-line derivation.

## Issue 5: Discharge matrix omits lemma preservation across transitions
Reason: All lemma-preservation arguments already exist elsewhere in the ASN (ChainMembershipForOrigin's proof section, ChainPrefixExtension's chain induction, StoreT4Validity's frame argument). The fix is presentational — either extend the matrix or add a preamble pointing to where each lemma's discharge resides.

## Issue 6: Base case verification doesn't address derived lemmas
Reason: The base cases for the derived lemmas are trivially vacuous over empty stores / empty dom(M), directly derivable from `Σ₀ = (∅, ∅, ∅)`. The fix is to add an explicit sentence stating this.

## Issue 7: Cross-document disjointness Case A's zero-count argument assumes more than M0 alone
Reason: The proof needs M0 at both `d₁` and `d₂` (currently only `d₂` is invoked in prose). The fix is purely a clarification of an already-correct argument using premises already available from M0's universal statement.

## Issue 8: ChainPrefixExtension's step case uses TA5-SigValid without first asserting chain-element T4-validity
Reason: This is a structural fix dependent on Issue 2's resolution. Once chain-element T4-validity is its own lemma, ChainPrefixExtension's induction cites it cleanly without nesting. No external input needed.

## Issue 9: K.σ does not state that the address space outside dom(C) ∪ dom(L) ∪ dom(M) is admissible
Reason: The cross-anchor freshness argument (anchors have `zeros = 3`, K.σ pins `zeros(d) = 2`, so collision impossible) uses only premises already present in the ASN. The fix is to add the one-sentence note the review itself proposes.

## Issue 10: The "T10a-discipline-satisfying chains" notion is informal
Reason: The intended structural definition (inc(·, 0)-extension chain with T4-valid first element) and the lemmas inherited (T10a.1, T10a.7, T10a.8) are all already discussed in the ASN. The fix is to separate the definition from the inherited-lemma claim, which is purely a definitional reorganization.
