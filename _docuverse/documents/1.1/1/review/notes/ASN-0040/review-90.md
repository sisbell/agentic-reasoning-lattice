# Review of ASN-0040

This ASN is mathematically solid — the inductive invariants (B1, B10, B_fin), the case analyses (B6, B7), and the uniqueness/extent arguments (B8, B9) are complete and check out against the foundation. My findings are almost entirely accretion: meta-prose that has settled around the foundation references and forward pointers, exactly the pattern the anti-bloat classifier flags.

## REVISE

### Issue 1: Defensive non-citation paragraph in S(p,d)
**ASN-0040, The sibling stream**: "We deliberately derive the stream's properties (uniform length, strict ordering below) directly from the primitives TA5 and T1 rather than citing T10a.1 (UniformSiblingLength) and T10a.7 (EnumerationInjectivity), because identifying a baptismal stream with a T10a allocator domain presupposes that baptism *is* the T10a allocation discipline — which remains an open question of this ASN... the re-derivation is independent grounding, not redundant restatement."
**Problem**: This is "why the derivation is done this way" meta-prose, not reasoning that advances the stream's meaning. It is also self-contradicting at the surface: the preceding sentence states "Structurally this is the foundation's allocator domain `dom(A)` (T10a) with base `inc(p, d)`: the same... recurrence." If the object *is* `dom(A)`, then S(p,d)'s uniform-length postcondition and S0 duplicate T10a.1 and T10a.7. Either the identification holds (cite the foundation) or it is genuinely open (then asserting "structurally this is dom(A)" is the over-claim). The reader must work past two paragraphs to reach the one-line definition.
**Required**: Reduce to the definition plus its postconditions. If the open-question hedge is load-bearing, state it once in Open Questions (where the `allocated(s) ⊆ s.B` question already lives), not inline as a citation-policy defense.

### Issue 2: B7 specialization claim stated twice
**ASN-0040, Namespace disjointness**: intro — "The disjointness conclusion itself specializes the foundation's T10a.6 (DomainDisjointness)... What is ASN-local — and what the proof below supplies — is the case analysis... together with the B6(i)/aliasing necessity argument." And again in *Depends*: "The disjointness conclusion specializes T10a.6 (DomainDisjointness) to baptismal namespaces; the case analysis and the B6(i)/aliasing necessity argument are the ASN-local content."
**Problem**: Two paragraphs in the same property say the same thing in different words — a relationship/use-site inventory duplicated across the prose slot and the Depends slot.
**Required**: Keep the relationship statement in one place (Depends is the natural home); delete the intro restatement.

### Issue 3: Multiple deferrals to the same open question
**ASN-0040, S(p,d) paragraph and Open Questions**: the S(p,d) meta-paragraph defers to "an open question of this ASN (under what activation discipline `allocated(s) ⊆ s.B` holds)"; the Open Questions section restates "Under what activation discipline does `allocated(s) ⊆ s.B` hold..."
**Problem**: Two locations defer to the identical downstream concern; the inline deferral compounds Issue 1's bloat.
**Required**: Single deferral in Open Questions; remove the inline forward pointer.

### Issue 4: Re-explanation of B0★ at its use site
**ASN-0040, B8 proof, Case 1**: "B0★ (Multi-step Irrevocability), the labelled corollary of B0 covering finite transition sequences, gives s₁'.B ⊆ s₂.B".
**Problem**: B0★ is fully stated two sections earlier; re-describing it as "the labelled corollary of B0 covering finite transition sequences" at the call site is restatement that does not advance the proof.
**Required**: Cite "B0★" by label alone.

## OUT_OF_SCOPE

### Topic 1: The Occupied predicate (B3)
**Why out of scope**: B3 reaches into content storage, which is explicitly deferred. It is correctly framed as a *forward requirement* on a future ASN rather than defining `Occupied` here, so no revision is needed — noting only to confirm the framing is the right one and should stay a requirement, not grow into a content-storage definition.

VERDICT: REVISE
