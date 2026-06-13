# Review of ASN-0125

## What I verified

**Core impossibility and the two-act structure.** EL0's reading of L12/LP13 as a weakest precondition is sound: `J ≡ a ∈ dom(L) ∧ L(a) = ℓ₀` holds at every reachable state of every schedule from `Σ₀`, `J ⟹ ¬R_mut`, so `wp(S, R_mut)` at `Σ₀` is `false` — correct. EL1's collapse of "edit" and "independent creation" to the same transition instance `K.λ(d_s, a_emit(Σ,d_s), ℓ')` with the same post-state is a genuine state-indistinguishability result, and it correctly forces the second act.

**EL2(c) closure (the most error-prone elimination).** Verified: first emission `[d.0.s_L.1]` has `#E = 2`, `inc(·,0)` preserves length (TA5(c)), a nested version-of-link would need `#E ≥ 3`, and R0a makes `dom(Σ.L)` a prefix antichain — so address structure carries only same-home (T6) and per-home order (T9), neither semantic. Sound.

**EL4 single-target.** `coverage({(x,δ(1,#x))}) = {t : x ≼ t}` (PrefixSpanCoverage) intersected with `dom(Σ.L)` collapses to `{x}` by R0a. The claim that this is per-claim (no whole-state discipline needed) is correct, and it is what makes `old`/`new`/`addr` total on `Ŝ^Σ` at every reachable state.

**The operation contracts.** I checked the active-at-birth and full-frame arguments in EL6(iv) and EL7(iv)/(vi), including the genuinely tricky retraction-class successor case: when `ℓ'` is `[R]`, step 1 nullifies its target `t` and `Σ₁` stays edit-disciplined (unit-depth retraction schema satisfied, `t ∈ dom(Σ.L) ⊆ dom(Σ₁.L)`), so EL6(iii)'s wp Case 2 premise holds at step 2; the fresh `b` escapes every pre-existing unit-depth `[R]` coverage by R0a antichain at `Σ₂`. The DC precondition pins witnesses at the pre-state `Σ` and the `dom(Σ.L) ⊆ dom(Σ₁.L)` transfer is correctly invoked. The "`a' ∉ dom(Σ.L)` so neither witness is `a'`" remark is right.

**EL11(a) discovery biconditional.** The "no content address extends `old(e)`" step checks out: `t ≽ y` agrees with `y` on `y`'s three separator positions, `zeros(t)=3` (C1) forces `E(t)₁ = E(y)₁ = s_L`, contradicting `E(t)₁ = s_C` (L0/SC-NEQ); link extensions collapse by R0a; CL-OWN pins listing to `home`. Symmetric from-side is genuinely the same argument with renamed endpoints (not a differing case), so "symmetrically" is legitimate.

**EL13 commutation** computed in both interleavings — `a_emit` depends only on the same-home subset, cross-home appends commute at distinct fresh keys, enabledness independent — yields identical `Σ_ab = Σ_ba`. Correct, and the per-home/per-asserter "latest" nuance is accurate.

**EL10 and EL14(c)** constructions verified arithmetically (`shift([s_L,1],1) = [s_L,2]` rebind; 2-cycle `succ_o` has no sink, `current = ∅`). **Worked example** addresses all trace correctly (`ℓ₁=H.0.s_L.2`, `c₁=.3`, `ℓ₂=P.0.s_L.1`, `c₂=.2`, `r₁=.4`, `c₃=.5`, `r₂=.6`), and the standoff→repair sequence resolves as claimed.

## REVISE

None.

I specifically examined the meta-prose the anti-bloat classifier targets. The three candidates — "Layer transfer," "Vocabulary fact V," "K.λ-only composites are valid" — are each load-bearing soundness obligations, not accretion: ASN-0086's contracts are proved at restricted-vocabulary "layer-reachable" states, and citing them at full ASN-0047-vocabulary states genuinely requires the transfer argument (the cited facts depend only on `Σ.L` and `dom(M)`, both evolved identically). A rigorous reviewer would want that bridge explicit, not elided. The closing hedge "without claiming anything of ASN-0086 results this note does not use" is a trivial defensive clause and the 6-fact list is a use-site inventory, but trimming them is cosmetic — below the threshold for a revision cycle, and the kind of style-churn the project's no-style-rewrites principle warns against. The aphoristic flourishes ("undo is just another statement," "the current view forgets; the record cannot") are statements of what the system does, which the directive explicitly classifies as not meta-prose. No forward-reference deferral accretes to a shared downstream location; no paragraph re-proves another (EL7(iv) cites EL6(iv) rather than restating it); no axiom-rationale sub-paragraphs are present.

## OUT_OF_SCOPE

The eight Open Questions are correctly future work, not gaps in this ASN — each names a *layer* obligation the substrate-level note cannot and should not settle:

### Authority for cross-principal retraction (OQ1)
The worked example has `H` nullify `P`'s claim `c₂`; Nullify's P-tgt admits any `a ∈ A_rel^Σ`, so the substrate imposes no asserter-authority constraint. Correctly deferred — authority is an ASN-0042 ownership-overlay concern, and the substrate state carries no principal (EL8b).

### Span-level endset correspondence under reshaping (OQ6)
This ASN treats the edit atomically (successor gets a fresh value `ℓ'`; the claim relates whole addresses). When an edit narrows or reshapes a single endset, span-level old↔new correspondence is new territory, not an omission here.

### Meta-claim currency stratification (OQ3)
EL8(d) permits claims targeting claims; whether `current` resolution must stratify such meta-claims to stay well-founded is a genuine future question, not a defect in the present (acyclic-or-cyclic) `succ_o` treatment.

VERDICT: CONVERGED
