# Review of ASN-0070

The technical core is sound. I checked the two substantial proofs — F-canonical (Steps 1, 2, 2a, the consecutivity Characterisation, both gap-closure arguments) and the F-contig contiguity claim — and they hold: the case analysis is exhaustive, both inclusions are shown where set equality is claimed, and the boundary cases (`s_m = 1` left-closure, `j = 1` vacuity, undefined `m_S(d)`) are handled. The five worked configurations exercise F-sound, F-complete, F-multi, F-empty, F-state, and the cross-subspace `⊎`. No correctness gaps found.

The findings below are all of the anti-bloat kind the note's classifier targets: prose that restates established results rather than advancing them.

## REVISE

### Issue 1: The "two halves of the postcondition" fact is stated three times

**ASN-0070, Derived Properties intro / F-sound / F-complete**: The intro already assigns each lemma its inclusion direction — "F-sound is the `⟦Σ_V^S⟧_V ⊆ R...` inclusion; F-complete is the reverse inclusion." F-sound's closing then repeats "This is the `⟦Σ_V^S⟧_V ⊆ R(d, L(ℓ).eᵢ)|_S` direction of the postcondition," and F-complete's closing repeats the reverse plus "F-sound and F-complete together unpack the set equality."
**Problem**: The same decomposition fact is asserted in three locations; a reader following the postcondition must read past two redundant restatements.
**Required**: State the split once (the intro is the natural place) and delete the two closing restatements. The verifier-decomposition remark in F-sound's closing is itself a fourth way of saying the same thing — fold or cut it.

### Issue 2: Claims Introduced table re-derives proofs instead of indexing them

**ASN-0070, Claims Introduced table**: Entries for F-canonical, F-det, F-multi, and F-subspace carry full derivation chains — e.g., F-det's entry reproduces "chain S2 → unique inverse image → unique partition (S3★-aux) → unique V-restricted denotation → unique canonical form (F-canonical/S9)," which is verbatim the body derivation; F-canonical's entry restates the entire existence/uniqueness argument.
**Problem**: A claims index should let a reader locate a claim, not re-prove it. These entries duplicate the lemma bodies in different words — the exact "two paragraphs saying the same thing" pattern.
**Required**: Reduce each entry to its statement and kind. The derivation belongs in the lemma body only.

### Issue 3: Directive meta-prose in the V-restricted denotation section

**ASN-0070, V-Restricted Denotation**: "The V-restricted denotation is what the postcondition fixes. The raw denotation `⟦Σ_V^S⟧` is correspondingly larger; the discrepancy is the irrelevant deeper-depth and cross-subspace tumblers in the lexicographic interval. Implementations and downstream consumers must compare results via `⟦·⟧_V`, not `⟦·⟧`."
**Problem**: This paragraph instructs implementers and re-characterises a definition already given precisely by the displayed formula. It advances no reasoning beyond the definition. The "what makes the filter an *admissible-V-position* filter rather than a bare depth-and-subspace filter" sub-paragraph is similarly a rationale-for-the-clause rather than a statement of the clause.
**Required**: The formula plus the one-line positivity justification (citing S8a) suffices. Cut the directive and the "what makes the filter" framing.

### Issue 4: The "Reachability" section restates F-empty in prose

**ASN-0070, Reachability**: "Coverage may reach the arrangement fully... partially... or not at all... All three are uniform outcomes with no error condition — the empty set is regular (formalised as F-empty). Whether an unreached portion is observable elsewhere... is irrelevant to resolution against `d` in the current state."
**Problem**: This section establishes nothing not already fixed by F0's inverse-image definition and discharged formally by F-empty; it is an essayistic preview that defers to a downstream lemma.
**Required**: Either delete the section or compress to a single sentence at F0's definition noting that partial/empty reach is uniform (the formal content lives in F-empty).

### Issue 5: Interpretive Nelson closers placed inside lemma slots

**ASN-0070, F-det / F-origin / F-state / F-multidoc**: Each derived-property lemma closes with motivational essay prose — "Nelson's commitment... is the structural consequence of working with functions"; "This is the structural reading of Nelson's 'a link to one version is a link to all versions'"; etc.
**Problem**: These are interpretive commentary occupying the postcondition/derivation slots of formal lemmas. They are not statements of what the operation does; they motivate. Placement in the lemma body forces the reader past them to reach the next claim.
**Required**: If retained, gather the system-guarantee interpretations into a single closing discussion section rather than appending one to each lemma. The lemma bodies should end at their derivations.

## OUT_OF_SCOPE

### Topic 1: Coverage members that are non-element-level addresses
**Why out of scope**: L4 permits endset spans over any tumbler, so `coverage(e)` may include node/account/document-level addresses. These never intersect `ran(M(d)) ⊆ dom(C) ∪ dom(L)`, so they contribute nothing — handled uniformly by F0. Making this explicit is a clarity nicety, not a correctness gap, and the Open Questions already gesture at related cross-home resolution semantics.

### Topic 2: Concurrency semantics of `follow` against a concurrently-modified document
**Why out of scope**: Correctly deferred by the note's own Open Questions; belongs to a transition-scheduling ASN, not this query specification.

VERDICT: REVISE
