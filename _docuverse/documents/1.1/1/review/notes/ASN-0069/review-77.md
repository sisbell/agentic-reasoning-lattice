# Review of ASN-0069

## REVISE

### Issue 1: Transitive correspondence across the version (sibling) stream is left underived, while the structurally identical chain-fork case (V11) is fully derived

**ASN-0069, §"Structural Correspondence", V8 remark**: "For versions past the second, `d_prev` is itself a subsequent emission whose content operand is the version *before* `d_prev`, not `d_src`; V8 at `d_prev`'s fork then yields `(version-before-d_prev) ↔ d_prev`, and the two-step composition does not reach `d_src`. The general transitive correspondence in that case would require an induction along the entire emission sequence of `A_v(d_src)` with every consecutive pair unedited, which we do not derive here."

**Problem**: The natural reading of "versions of a document" is the sibling stream of `A_v(d_src)` — version 1 = `inc(d_src,1)`, version 2 = `inc(v1,0)`, version 3 = `inc(v2,0)`, etc. The operand chain is `d_src → v1 → v2 → …`, with each adjacent pair linked by V8. This is the exact structure Nelson's intercomparison promise ("word for word, what parts of two versions are the same" [LM 2/20]) is invoked to cover. Yet the transitive claim "unedited version 1 and version 3 of `d_src` fully correspond" is punted in one sentence — while V11 derives the *chain-fork* analogue (`dⁱ_new = inc(dⁱ⁻¹_new, 1)`) in full, with a complete induction. The two inductions are structurally identical (V8 adjacent correspondence + per-step unedited premise + composition); the only difference is the operand being the prior sibling (`inc(·,0)`) rather than the prior chain-link (`inc(·,1)`). Deriving the less-central chain case in full and dropping the central version-stream case is an unjustified asymmetry of depth on this ASN's headline deliverable.

**Required**: Either (a) supply the sibling-stream induction — a V11-analogue establishing that for an unedited version sequence `d_src, v1, …, v_k` produced by `A_v(d_src)`'s `inc(·,0)` chain, the I-addresses inherited by `v_k` equal those of `d_src` at fork-time — or (b) give an explicit justification for why the sibling case is scoped out while the chain case is derived, rather than the bare "which we do not derive here."

### Issue 2: V5a re-derives a transition-vocabulary frame theorem that exceeds what the fork operation needs

**ASN-0069, §"Frame: Source Isolation", V5a**: per-step clause (a) walks the entire arrangement-modifying vocabulary `K_M` plus K.α, K.λ, K.δ, K.ρ and the K.μ~ composite; clause (b) adds a full induction on sequence length.

**Problem**: V5 (source isolation) and the two corollaries (source–fork isolation, pairwise independence) are what V10 and V12 actually consume. The general universal theorem — "any `d*`, any sequence, every member of ASN-0047's vocabulary, K.μ~ by decomposition" — is a property of the transition system as a whole, not of CREATENEWVERSION. Proving it here (with the exhaustive vocabulary enumeration and the length induction) is composition of per-transition frames that ASN-0047 already states; the fork ASN needs only "these per-transition frames compose to preserve `M(d*)` when no step targets `d*`." This is drift toward ASN-0047 territory dressed as a fork-specific lemma.

**Required**: Reduce V5a to the two corollaries the ASN uses, justified by one-line composition of ASN-0047's per-transition frame conditions; drop the universal-theorem framing and the full induction, or relocate the general statement to where the transition vocabulary is defined.

### Issue 3: Meta-prose around claim statements that justifies framing rather than advancing reasoning

**ASN-0069, §"Composability", V11 "Anchoring at Σ" paragraph**: "To keep the conclusion well-defined under that scope, V11 anchors `V_{s_C}(d_src)` and `M(d_src)(v)` at `Σ` — the immutable historical state at the chain's start — rather than at any later state. Arrangement edits M-targeted elsewhere … are discharged operationally by V5a Corollary 2."

**ASN-0069, §"Frame: Source Isolation", V5a**: "`K_M` lists only the three elementary kinds; the named composite K.μ~ is handled by decomposition in clause (a)" and the closing "Thus every member of ASN-0047's arrangement-modifying vocabulary — the three elementary kinds and the one composite — is covered."

**Problem**: The "Anchoring at Σ" paragraph explains *why the claim is stated the way it is* rather than advancing the proof — the precise reader must skip it to follow the induction. The V5a sentences are a defensive exhaustiveness/coverage claim of the same kind the anti-bloat classifier names. Neither passage carries object-level content; both are reviser-style accretion around the formal statement.

**Required**: Remove the "Anchoring at Σ" rationale paragraph (the anchoring is already fixed by the formula `M(d_src)(v) at Σ` in V11's statement and the base-case derivation). Drop the V5a exhaustiveness asides; if K.μ~ decomposition matters it belongs inline in the one step that uses it, not as a standing coverage claim.

## OUT_OF_SCOPE

### Topic 1: Snapshot vs. living forks, concurrent modification, descendant enumeration
**Why out of scope**: The ASN already lists these as Open Questions and makes no claims about them; they are future-ASN territory, not errors here.

VERDICT: REVISE
