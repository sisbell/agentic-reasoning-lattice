# Review of ASN-0099

## REVISE

### Issue 1: A1/A1a and the "Arrangement Independence" intro triple-state the same fact
**ASN-0099, "Arrangement Independence" / A1a / A1**: The intro says "operations other than K.λ preserve Σ.L"; A1a says every atomic op of V∖{K.λ} "publishes L' = L ... hence preserves the link store"; A1 says "K.λ is therefore the unique operation of V that modifies the link store."
**Problem**: Three statements of one fact. F9's derivation consumes the *per-op* preservation (A1a: `Σ.L = Σ'.L` across each V∖{K.λ} step), not the uniqueness *summary*. A1's "K.λ is the unique modifier" is an inventory-style restatement that no downstream claim consumes; F9 even cites A1 where it actually uses A1a's per-op content. This is forward-reference/restatement accretion.
**Required**: Keep A1a (with K.μ~ composition folded into its scope) as the single load-bearing lemma; delete A1's uniqueness summary and the intro sentence that pre-announces it. Have F9 cite A1a directly.

### Issue 2: Defensive and motivational prose in the two-phase factoring
**ASN-0099, "A Two-Phase Factoring"**: "the caller has no pre-validation obligation beyond establishing d ∈ dom(Σ.M)" and "The factoring matters because the two phases have different stability properties. Σ.M is mutable ...; Σ.L is monotonic ...."
**Problem**: The first is API-ergonomics justification, not a property of the operation. The second is motivational essay restating facts already carried by K.μ-family frames and L12, sitting in a definition slot. Neither advances the definition of `image` or `findlinks_V`.
**Required**: Drop the pre-validation sentence (the undefined-on-`d ∉ dom(Σ.M)` clause already states the contract). Either delete the "factoring matters because" paragraph or reduce it to a single forward pointer to F9/F11 where the stability distinction is actually used.

### Issue 3: F4 repeats per-witness L3 caveats already covered by the global realizability claim
**ASN-0099, F4 (MatchIndividuation)**: A global "*Realizability.* Each witness is realizable ... arises by a K.λ allocation under any document" precedes the witnesses, yet each witness re-parenthesizes "(the mandatory non-empty type-endset slot per L3)" and "(permitted by L3 for non-type slots)".
**Problem**: The realizability/L3-admissibility of empty non-type slots is established once globally; repeating it inside Strengthening 2, Strengthening 3, and the Weakening witnesses is redundant padding around the actual disagreement computation.
**Required**: State the L3 endset-shape admissibility once (in the Realizability paragraph) and strip the per-witness repetitions, leaving each witness to carry only its query `I` and the slot-by-slot disagreement.

### Issue 4: Worked-example narration justifies example construction
**ASN-0099, "A Worked Example," Query 6**: "Query 5's chain stays in V ∖ {K.λ}, so it cannot exercise F11's load-bearing case — the case where dom(Σ.L) grows under the persistence claim. We extend Σ_5 with one K.λ step to surface that case explicitly."
**Problem**: This is meta-prose about why the example is arranged as it is, not content the reader needs to verify the claim. The Query itself already exhibits the K.λ growth case.
**Required**: Delete the design-rationale sentences; let Query 6 state its state and evaluate F11/F9-λ/F19 directly.

### Issue 5: "Local Atomicity" section restates foundation + F2
**ASN-0099, "Local Atomicity and the Single-State Setting"**: "By SequentialTransitionAxiom (ASN-0093), every state transition is atomic ...; Σ is well-defined at every query point. A K.λ commits a to dom(Σ.L) atomically: by the time the K.λ ... returns, a is in dom(Σ.L) and the next query ... must include a if a matches."
**Problem**: The first sentence restates a foundation axiom; the second restates it again ("commits ... atomically") and then re-derives completeness (F2). Two sentences saying the same thing, neither adding a new guarantee.
**Required**: Either remove the section or compress to one sentence pointing at SequentialTransitionAxiom for the single-state reading; drop the F2 restatement.

## OUT_OF_SCOPE

None. The ASN's own "What We Have Not Specified" and "Open Questions" correctly fence procedure, replication/BEBE, caching, and the inverse (FOLLOWLINK) direction.

VERDICT: REVISE
