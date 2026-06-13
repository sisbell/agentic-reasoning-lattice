# Review of ASN-0130

This is a carefully built note. The substitution lemma (PR3a), the acyclicity argument (PR2), the wp partitions (PR0/PR5a), and the lint-exactness derivation (PR5) are all genuine proofs with their cases worked. The findings below are two precision gaps and one scoping note.

## REVISE

### Issue 1: ST⁺'s aggregate-threshold extension is broader than its soundness argument

**ASN-0130, PR5 (*Parameters* qualification)**: "The parameter reading extends that threshold position from 'ℕ literal' to any *bound* ℕ value, the parameter included" — justified by "Soundness ... consumes only the *fixity* of bound values across a step: ... a count's threshold stays put whether literal or parameter."

**Problem**: The definition admits **any bound ℕ value** in a `count(D) ≥ c` threshold; the soundness argument establishes the required cross-step fixity for exactly two cases — literals and environment-bound parameters. These do not exhaust "bound ℕ value." A value introduced by a PC2 binder guard (`if f(Σ) is some y then count(D) ≥ y …`) is recomputed at each state and is *not* fixed across a step. For such a threshold, ⊤-stability fails: at Σ, `count(D)_Σ ≥ y_Σ`; at Σ′, `count(D)_{Σ'} ≥ count(D)_Σ ≥ y_Σ` (D grow-only), but if `y_{Σ'} > y_Σ` the count may not have grown to match, so `count(D)_{Σ'} ≥ y_{Σ'}` can be false. The note neither narrows the phrasing nor argues such a value cannot occupy a threshold position. The saving fact — PD0 admits no binder-guard rule, so a guard-bound ℕ value can never sit inside an ST⁺-classified term, leaving only parameters and literals (both fixed) reachable in threshold position — is true (quantifier domains are address/tuple/class-valued, never ℕ, so the only ℕ binders are parameters and guards) but is left unstated, which is precisely what makes the soundness proof incomplete for the stated definition.

**Required**: Either restrict the extension to "an ℕ literal or environment-bound parameter," or add the missing clause — that PD0's grammar admits no binder-guard form, so the only bound ℕ values reaching an aggregate threshold in an ST⁺-classifiable term are parameters and literals, both fixed across every step.

### Issue 2: PR1 mis-cites the class governing pdef de-registration

**ASN-0130, PR1**: "a `Nullify_Binary` on a referent's `pdef` tuple de-registers it (PS2), falsifying (iv) for a standing definition *with no content change whatsoever*."

**Problem**: De-registering a `pdef` tuple is a `pdef`-class matter, which is **PS1** (PredicateDefinition). **PS2** is `pd_stable` (StabilityCertificate), which has nothing to do with the cited fact. The de-registration mechanism is stated in the "Retraction interacts" paragraph of the Standard registrations section. In a permanence argument whose whole point is to separate the content/signature-intrinsic conjuncts from the endorsement conjunct (iv), an incorrect class label on the very mechanism that falsifies (iv) is a precision defect.

**Required**: Cite PS1 (or the "Retraction interacts" paragraph), not PS2.

## OUT_OF_SCOPE

### Topic 1: Expansion size / sharing

PR3's `expand(a)` inlines each applied reference with no sharing, so a definition that references a common sub-definition along k paths produces k inlined copies, and `expand(a)` can be exponential in the reference-DAG depth. PR2/PR3a establish *termination and finiteness*, which is all the abstract spec needs. Bounding or sharing the expansion (DAG-structured evaluation, memoized referents) is an implementation/efficiency concern.

**Why out of scope**: The note correctly proves the spec-level property (the result is a finite, pure, well-typed PL term); efficient evaluation of that term is downstream of this note's guarantees.

### Topic 2: Atomic allocation of a contiguous run

PR0 (i) rejects any `A_def` that is not one contiguous chain segment, so a run split by an interleaved same-document K.α at allocation time would fail registration. The note acknowledges this (the worked-composition caveat "with no other K.α scoped to `d_b` interleaved" and the udanax-green parenthetical), but provides no primitive guaranteeing a definition's run is allocated as one uninterrupted segment.

**Why out of scope**: Allocation is ASN-0093's K.α; ensuring run contiguity before registration is an upstream caller discipline, and PR0 (i) already rejects the failure mode. This is a future allocation-protocol concern, not an error here.

VERDICT: REVISE
