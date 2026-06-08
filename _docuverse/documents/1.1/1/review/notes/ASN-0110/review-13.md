# Review of ASN-0110

This is a careful, thorough specification. The touching semantics, role separation, the touch-by-coverage/return-by-value asymmetry, anonymity, survivability, and the weakest-precondition analysis are all handled with real rigour, and the worked instance correctly exercises RE-full and RE-role. I verified the example computation, the RE-add distribution, the RE-wp case split, and the RE-mono persistence chain; all hold. Two genuine issues remain.

## REVISE

### Issue 1: Open Question 4 is already answered by RE-anon
**ASN-0110, Open Questions / RE-anon**: OQ4 asks "What must the system guarantee about the relationship between the endsets a region-search returns and the count of distinct links anchored to that region?"
**Problem**: RE-anon already resolves exactly this. It establishes (a) the sound lower bound `max_i |Eᵢ(I, Σ)|` on the number of distinct contributing links, and (b) that the exact count is undetermined (via the L11b duplication construction). That *is* the guaranteed relationship between the returned endsets and the link count. The scope explicitly excludes the counting operations (FINDNUMOFLINKS), so OQ4 cannot be deferring to a separate operation — it concerns this operation's own result, which RE-anon answers. An open question should not pose as open something the claims body resolves.
**Required**: Either remove OQ4, or sharpen it to state precisely what remains open *beyond* RE-anon's lower bound (e.g., conditions under which a tighter bound or exact count is recoverable), so it does not duplicate an established claim.

### Issue 2: RE-surv mis-types the composite K.μ~ as a single-step transition
**ASN-0110, RE-surv**: "Let `Σ → Σ'` be any arrangement edit — a K.μ-family transition (`K.μ⁺`, `K.μ⁻`, `K.μ⁺_L`, or the composite `K.μ~`)..."
**Problem**: K.μ~ is a named composite (`K.μ⁻ + K.μ⁺`), so its transition is `Σ →* Σ'`, not the single step `Σ → Σ'`. A1a itself distinguishes "single-step `Σ → Σ'` for the atomic operations, the two-step composite `Σ →* Σ'` for K.μ~." Listing the composite under a single-arrow quantifier is a type imprecision in the lemma statement. The conclusion is unaffected (L' = L holds across both constituents, so RE-det gives equality), but the statement as written is not well-typed.
**Required**: State the transition as `Σ → Σ'` for the atomic K.μ edits and `Σ →* Σ'` for the composite K.μ~, mirroring A1a, so the survivability claim covers K.μ~ by composition rather than by mislabeling it atomic.

## OUT_OF_SCOPE

(none beyond the topics the ASN already defers to its own Open Questions 1, 2, 3, 5, which are correctly identified as future territory)

VERDICT: REVISE
