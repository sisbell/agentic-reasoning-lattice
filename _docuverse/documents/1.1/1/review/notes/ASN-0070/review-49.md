# Review of ASN-0070

## REVISE

### Issue 1: The "denotation, not representation" disclaimer is restated in three separate sections

**ASN-0070, Canonical Form / Computation via Decomposition / F-det**:

- Canonical Form (closing): *"We do not commit the operation's postcondition to canonical form: the abstract specification fixes only `⟦Σ_V^S⟧_V = R(d, e)|_S`. An implementation may return any representationally equivalent form. The canonical form is the derivation that callers apply when representational identity matters."*
- Computation via Decomposition: *"This is *one* admissible computation (the postcondition fixes denotation, not decomposition strategy — see Canonical Form)."*
- F-det postcondition: *"The representations `Σ_V` and `Σ_V'` may differ; after canonical-form derivation, they coincide."*

**Problem**: Three sites carry the same point (the postcondition pins V-restricted denotation, not span-set representation; canonical form is an optional downstream derivation). One of them additionally carries a back-pointer ("see Canonical Form"). This is the cross-section-deferral / same-claim-in-different-words accretion pattern: a reader following the argument has to re-absorb the identical caveat each time it recurs.
**Required**: State the denotation-vs-representation contract once — naturally in the Canonical Form section where canonical form is defined — and delete the restatements in "Computation via Decomposition" and in the F-det postcondition (F-det can simply assert that `⟦Σ_V^S⟧_V` is uniquely determined, which is its actual content).

### Issue 2: Scene-setting essay lines in The Setting

**ASN-0070, The Setting**: *"By the permanence invariants (P0, P1, L12 of ASN-0047), the stored material persists; only the arrangement varies. The arrangement is the variable; storage is the constant."* and *"Resolution is the inverse problem: given I-addresses (from an endset), find the V-positions in `d` that currently hold them."*

**Problem**: The aphoristic closers ("The arrangement is the variable; storage is the constant") restate the immediately preceding sentence in epigram form without adding a claim. The "inverse problem" sentence then re-announces what F0 defines two paragraphs later. This is essay content in a setup slot — the reader must skip it to reach the load-bearing material.
**Required**: Drop the epigram and the pre-announcement; let F0's definition carry the inverse-image framing. Retain only the factual permanence citation.

## OUT_OF_SCOPE

### Topic 1: Multi-home endset resolution, concurrency semantics, transclusion-lineage relationships
**Why out of scope**: The three Open Questions (resolution against documents transcluding from different home subsets; concurrent-modification semantics; `follow(ℓ,d,i)` vs `follow(ℓ,d',i)` under shared transclusion lineage) are correctly posed as future work. They are not defects in this note's query semantics, which is fully specified for the single-state, single-document case.

VERDICT: REVISE
