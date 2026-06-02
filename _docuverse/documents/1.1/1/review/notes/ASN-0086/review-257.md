# Review of ASN-0086

## REVISE

### Issue 1: SliceUniqueness claims "exactly one slice" but higher-arity addresses index zero
**ASN-0086, Lemma — SliceUniqueness**: "Each tuple address `a ∈ dom(Σ.L)` indexes exactly one slice `L_K^Σ`. *Proof.* ... a single coverage class `[Σ.L(a).e₃]`; thus `a` lies in no two slices. ∎"

**Problem**: The proof establishes *at most one* ("lies in no two slices"), not *exactly one*. The statement "exactly one" is false for any address with `|Σ.L(a)| ≠ 3`: every `L_K^Σ` carries the conjunct `|Σ.L(a)| = 3`, so a higher-arity link indexes **zero** slices. The note states this directly one paragraph earlier ("higher-arity links (`|Σ.L(a)| > 3`) ... inhabit `A_rel^Σ = dom(Σ.L)` but index no tuple of any `L_K`") and again in *Definition — TupleAddress* ("image the arity-3 slice `{a : |Σ.L(a)| = 3}`", i.e. `addr` is not onto `A_rel`). So SliceUniqueness contradicts both its own proof and two adjacent claims.

**Required**: Restate as "indexes **at most one** slice" (which is exactly what the proof gives and all the disjoint-union claim needs), or scope the quantifier to `{a ∈ dom(Σ.L) : |Σ.L(a)| = 3}` where "exactly one" is then correct.

### Issue 2: Corollary R5.1 asserts "any slot position," but R5 only proves slots 1 and 2
**ASN-0086, Corollary R5.1 — SelfTargetingEmission**: "For any `a ∈ A_rel^Σ`, **any slot position**, and any caller-supplied home `d`, R0 emits ... carrying the unit-depth span `(a, δ(1, #a))` in the chosen slot (by Steps 2–3 ...)."

**Problem**: R5's proof establishes the from-set case (Step 4) and to-set case (Step 3) — slots 1 and 2. It does *not* treat slot 3 (the type slot). Placing `(a, δ(1, #a))` in slot 3 changes the link's type endset (and its coverage class), which is a materially different claim than placing it in a content slot; the cited "Steps 2–3" cover only the to-set. The corollary's "any slot position" therefore overreaches the proof, and the corollary otherwise restates Steps 3–4 without adding argument.

**Required**: Either restrict R5.1 to the from/to slots actually proved (slots 1–2), or add the slot-3 case explicitly (noting the type-class consequence). If R5.1 adds nothing beyond R5's Steps 3–4, fold it back rather than carrying a separate labeled corollary.

### Issue 3: wp Case 2 is the weakest precondition only over a sub-domain of where Emit_K is defined
**ASN-0086, Weakest-Precondition Analysis, Case 2**: "Over the layer-reachable states ..., the weakest precondition is `d ∈ dom(Σ.M) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`."

**Problem**: `Emit_K` is defined with "Σ ranges over the `→*`-reachable states," but the wp formula is the weakest precondition only on the strictly smaller *layer-reachable* domain. The derivation's no-pre-existing-retraction-covers-`a` step depends on the unit-depth discipline, which holds only for layer-reachable states. On a `→*`-reachable-but-not-layer-reachable state a pre-existing wide retraction to-span can already cover the fresh `a`, so the stated formula is *not* the wp there. Calling it "the weakest precondition" without flagging that it fails over the operation's full domain is imprecise.

**Required**: State explicitly that the formula is the wp relative to the layer-reachable domain only and does not characterize `wp` on `→*`-reachable-but-undisciplined states, or restrict `Emit_K`'s stated domain to layer-reachable states.

### Issue 4: Pure-alias catalog entries and defensive "load-bearing" prose (anti-bloat)
**ASN-0086, R2/R4 and the wp derivations**: R2 ("definitional alias of L12"), R4 ("definitional alias of SD"); and wp prose such as "`d ∈ dom(Σ.M)` ... is load-bearing: dropping it leaves K.λ's home-precondition undischarged, so no post-state Σ' is produced" (appears in both Case 1 and Case 2).

**Problem**: R2 and R4 rename a foundation result into the R-catalog with no new content; the "dropping X leaves Y undischarged, so no post-state is produced" construction is repeated verbatim-in-structure across both wp cases. These are the "use-site inventory / defensive justification" patterns the anti-bloat classifier targets. The execution-precondition observation is the same sentence twice.

**Required**: Either drop R2/R4 as standalone catalog rows (cite L12/SD inline where used) or mark them once as vocabulary aliases without proof-prose; state the home-precondition's necessity once and reference it.

## OUT_OF_SCOPE

### Topic 1: Cardinality/ratio bound on `nullified(Σ)` relative to `dom(Σ.L)`
This is raised in the note's own Open Questions and is genuinely new territory (a quantitative substrate guarantee), not a defect in the present relational vocabulary.

### Topic 2: Multi-arity typed relations `L_K^{(n)}`
Generalizing slices beyond arity-3 (also an Open Question) is future work; the arity-3 restriction here is internally consistent once Issue 1 is fixed.

VERDICT: REVISE
