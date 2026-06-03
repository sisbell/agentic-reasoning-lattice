# Review of ASN-0070

## REVISE

### Issue 1: Dangling/inconsistent label "F-canon-form"
**ASN-0070, Canonical Form / Theorem (F-canonical)**: "there exists exactly one per-subspace family satisfying the canonical-form shape of F-canon-form."
**Problem**: The body defines the canonical-form shape under the heading **Definition (CanonicalForm)**, but the F-canonical theorem (and F-det step 5, F-empty's Depends) refer to it as **F-canon-form** — a label that appears only in the Claims table, never as a labeled claim in the body. A reader following "the canonical-form shape of F-canon-form" cannot locate that label in the proof text.
**Required**: Use a single consistent label. Either rename the body definition to F-canon-form, or change the references to point at "Definition (CanonicalForm)".

### Issue 2: Duplicated depth prose in The Setting
**ASN-0070, The Setting**: "The two subspace depths `m_{s_C}(d)` and `m_{s_L}(d)` need not coincide. Neither is a fixed constant: each is `≥ 2`, pinned per document while its subspace is non-empty and undefined otherwise."
**Problem**: This paragraph restates, in summary form, exactly what the two preceding bullet points already establish (each `m_S(d) ≥ 2`, pinned by first insertion, undefined when the subspace is empty). It advances no new claim — it re-says the bullets. This is the "two paragraphs say the same thing" accretion pattern flagged by the anti-bloat classifier.
**Required**: Delete the restating paragraph; the bullets are sufficient. If the "need not coincide" fact is load-bearing downstream, keep only that half-sentence.

### Issue 3: S5-vs-K.μ⁺ disambiguation is meta-prose
**ASN-0070, F-multi, "Structural admissibility"**: "S5 is a model-existence claim about arbitrary cardinality, not a reachability claim in ASN-0047's transition system, and the reachability of the binary hypothesis here rests on K.μ⁺'s non-injectivity rather than on S5."
**Problem**: This sentence does not advance the lemma; it adjudicates *which cited dependency is the right justification* for reachability — the "new prose explains why a dependency is/isn't load-bearing" accretion pattern. The substantive point (the binary hypothesis is reachable via K.μ⁺ non-injectivity) is already made in the sentence before it. The S5 caveat is editorial commentary on the dependency list.
**Required**: State the reachability fact (K.μ⁺ imposes no content-side injectivity, so `v₁ ≠ v₂` mapping to the same `a` is reachable) and stop. If S5 is retained in Depends as the abstract-cardinality witness, let the Depends line carry that role without an in-prose disclaimer about what S5 "is not."

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics of follow against a concurrently-modified document
**Why out of scope**: Raised in Open Questions; concurrency model is new territory not part of specifying the inverse-image query, and F-frame already fixes the single-state reading.

### Topic 2: Cross-document resolution relationships under shared transclusion lineage
**Why out of scope**: Raised in Open Questions; relating `follow(ℓ, d, i)` to `follow(ℓ, d', i)` across lineage requires version-graph machinery beyond this note's per-document query.

VERDICT: REVISE
