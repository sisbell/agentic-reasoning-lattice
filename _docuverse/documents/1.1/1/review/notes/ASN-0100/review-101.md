# Review of ASN-0100

This is a thorough, multi-cycle ASN; its invariant coverage against ASN-0047's `ExtendedReachableStateInvariants` is essentially complete, the edge cases (j=0, append, empty document, re-insertion after clearance) are worked, and the wp analysis is genuinely non-trivial. The findings below are residual anti-bloat items, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Duplicated defensive gloss explaining an excluded K.δ mechanism

**ASN-0100, Frame Conditions (INS.frame.E) and §Post-state … (P6)**:

> `E' = E`. The entity set is unchanged … (`dom(M)` is extended only by K.δ's Document-case arrangement frame, which adds `e` with `M'(e) = ∅`; ASN-0047)

and verbatim again in the P6 paragraph:

> `dom(M)` is extended only by K.δ's Document-case arrangement frame, which adds `e` with `M'(e) = ∅`; ASN-0047

**Problem**: The same clause appears in two sections, and in both it explains how `dom(M)` *would* grow if K.δ fired — a mechanism INSERT's decomposition explicitly excludes (no K.δ fires). It is a defensive justification of a foundation mechanic that does not advance INSERT's argument; the only fact INSERT needs is `E' = E` (hence `dom(M') = dom(M)`, `E'_doc = E_doc`). This is the reviser-drift pattern: a paragraph imagining a case the precondition already excludes, repeated across sections. The further parenthetical "whose prose states `dom(M) = E_doc`" compounds it.

**Required**: In both sites, state only `E' = E` (no K.δ in the decomposition), hence `E'_doc = E_doc`. Drop the "dom(M) is extended only by K.δ's Document-case…" gloss in both places; INSERT never invokes K.δ.

### Issue 2: INS.proj closing paragraph re-narrates the formal derivation

**ASN-0100, §Coverage and link discoverability (after the Step 0–4 derivation)**: "The K.μ⁻ step's 'temporary retraction' of `P_0^R` … is *cancelled* by K.μ⁺'s reintroduction of those V-positions at shifted addresses: the Right contributions disappear at `Σ_μ⁻` … and reappear at `Σ_μ⁺` …"

**Problem**: Steps 2 and 3 of the immediately-preceding derivation already establish this exactly — Step 2 gives `project = P_0^L ∪ P_0^{s_L}` (P_0^R removed), Step 3 adds `{shift(v,n) : v ∈ P_0^R}`. The prose paragraph restates the same algebra in words ("two paragraphs say the same thing in different words").

**Required**: Either keep the formal steps and drop the prose re-narration, or compress to a single clause noting the retraction/reintroduction is exact. Not both.

## OUT_OF_SCOPE

None. The Open Questions correctly defer link-subspace insertion, COPY, concurrency, and composition to future ASNs rather than asserting claims about them.

VERDICT: REVISE
