# Review of ASN-0070

## REVISE

### Issue 1: Forward-reference justification embedded in a definition

**ASN-0070, F-canon-form (CanonicalForm), clause (i)**: "...whose width is an ordinal displacement `δ(c, m_S(d)) = [0, ..., 0, c]` of depth `m_S(d)` with `c ≥ 1`. (F-canonical Step 1 shows no other level-uniform span has a finite, subspace-confined `⟦σ⟧_V` matching a component of `R(d, e)|_S`.)"

**Problem**: The parenthetical is a justification for the width restriction that forward-references a proof appearing *after* the definition. A reader working through the definition cannot follow the cited argument yet and must skip past it. The clause's job is to state the canonical shape; *why* no other shape qualifies is precisely what F-canonical Step 1 proves. This is meta-prose in a structural (DEF) slot — it explains why the restriction is needed rather than stating what the shape is.

**Required**: Delete the parenthetical. The definition states the shape; F-canonical Step 1 already supplies the justification at the point where it is provable.

### Issue 2: F-det attributes V-restricted uniqueness to S9, which governs full-T denotation

**ASN-0070, F-det (DenotationalDeterminism), Derivation step 4**: "...a canonical form exists ... and S9 (NormalizationUniqueness, ASN-0053) yields a unique normalised form per component."

**Problem**: S9 establishes that two *normalised, full-denotation-equivalent* span-sets (`⟦Σ̂₁⟧ = ⟦Σ̂₂⟧` over all of `T`) are equal. But the postcondition of `follow` fixes only the *V-restricted* denotation `⟦Σ_V^S⟧_V`, not the full `⟦Σ_V^S⟧`. S9 alone does not bridge V-restricted equality to the per-component uniqueness F-det asserts. The bridge that actually licenses this — recovering `(s_j, c_j)` from `⟦σ_j⟧_V` so that V-restricted equality implies full equality — is established inside F-canonical (Step 4, "Bridge"). F-det skips this step and cites S9 directly, leaving the chain underspecified.

**Required**: Cite F-canonical (its Step 4 bridge + run-reconstruction) as the source of per-component uniqueness from the fixed V-restricted denotation, rather than citing S9 as if it applied directly to `⟦·⟧_V`. If S9 is retained, name the bridge step that converts V-restricted equivalence to full-denotation equivalence first.

## OUT_OF_SCOPE

### Topic 1: Cross-home consistency obligations between `follow(ℓ, d, i)` and `follow(ℓ, d', i)`
**Why out of scope**: The note correctly raises this in Open Questions. Relating resolutions across documents transcluding shared homes is a new query-composition obligation, not a defect in the single-document inverse-image specification.

### Topic 2: Concurrent / multi-server (BEBE) link traversal consistency
**Why out of scope**: SequentialTransitionAxiom (ASN-0047) makes `follow` a pure query against one serialized state; replication consistency belongs to a future model.

VERDICT: REVISE
