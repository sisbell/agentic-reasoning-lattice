# Review of ASN-0070

This note's technical core — resolution as the inverse image `R(d, e) = M(d)⁻¹(coverage(e))` partitioned by subspace — is sound, and the F-canonical existence/uniqueness proof checks out against the worked configurations. My findings are concentrated in the area the `review-mode.anti-bloat` classifier flags: essay framing and rationale prose accreted around the definitions and forward references.

## REVISE

### Issue 1: Introduction enumerates a definition's downstream consumers
**ASN-0070, opening ("The argument begins...")**: "Every property of the operation — denotation-determinism, multiplicity, partial reach, empty admissibility, slot uniformity, origin symmetry — follows from that relation combined with the foundations. We shall develop it once and then read off consequences."
**Problem**: This is a use-site inventory for F0 placed before F0 is even stated. It advances no reasoning — it pre-announces the Derived Properties catalogue. Exactly the "definition's introduction enumerates downstream consumers" pattern.
**Required**: Reduce to a single sentence naming the inverse image as the operation's content; drop the consequence roster (the Claims Introduced table already lists them).

### Issue 2: Closing paragraph of Derived Properties duplicates the opening framing
**ASN-0070, end of "Derived Properties"**: "These properties are not independent axioms requiring separate verification. They are readings of the same definition: `R(d, e) = M(d)⁻¹(coverage(e))` partitioned by subspace..."
**Problem**: This restates the opening's "We shall develop it once and then read off consequences" in different words. Two paragraphs in the same document saying the same thing. One of them is redundant.
**Required**: Remove one. The closing restatement adds nothing the per-lemma Depends fields do not already establish.

### Issue 3: F-canonical clause (i) carries rationale prose explaining why the convention is needed
**ASN-0070, CanonicalForm clause (i)**: "The convention's role is to pin `(s, c)` uniquely from `⟦σ⟧_V` for the Step 2 reconstruction... Without the convention, distinct `(s, ℓ)` pairs would witness the same V-restricted point set and Step 2's `(s_j, c_j) = (min(run_j), |run_j|)` reconstruction would not be single-valued."
**Problem**: This is "why the convention is needed" prose embedded in a definition slot — it argues necessity rather than stating the convention. The necessity is already discharged operationally in Step 2's bridge argument (`s = min(⟦σ⟧_V)`), so the clause-(i) gloss is a relocated justification, not a definitional statement.
**Required**: State the positivity convention plainly in clause (i); move (or delete, since Step 2 already covers it) the "Without the convention..." necessity argument out of the definition.

### Issue 4: Defensive framing on the per-subspace decomposition
**ASN-0070, "Result Form and the Operation"**: "The per-subspace decomposition is structurally required, not a stylistic choice."
**Problem**: The substantive reason (differing subspace depths preclude a single level-uniform span-set) follows in the next sentences and stands on its own. The "structurally required, not a stylistic choice" lead is defensive meta-prose anticipating an objection.
**Required**: Delete the framing sentence; open directly with the depth-difference argument.

## OUT_OF_SCOPE

### Topic 1: Cross-home transclusion-lineage relationships between `follow(ℓ, d, i)` and `follow(ℓ, d', i)`
**Why out of scope**: The note correctly defers these to Open Questions; they concern multi-document resolution semantics not yet specified, not an error in this ASN's single-document resolution.

### Topic 2: Concurrency semantics during concurrent modification
**Why out of scope**: A genuine future concern (also listed in Open Questions); F-frame establishes state-purity, which is the most this query-level ASN can assert.

VERDICT: REVISE
