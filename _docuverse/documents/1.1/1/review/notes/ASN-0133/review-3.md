# Review of ASN-0133

This note is ambitious and, in most places, admirably precise about where each hypothesis lives. The recognizability/absorption results (Q0, Q1) are clean, Q5's injectivity bound is carefully argued, and Q-EXT's composition of X-DEF with PD0 ⊥-stability is sound, including the domain re-entry case (SF tracks the predicate's truth, not domain membership). The problems below are concentrated in the *discharge* story for H-W and in one over-strong enumeration.

## REVISE

### Issue 1: "H-W reduces to bounded domain growth" is false — what reduces is the real-fire count, not H-W

**ASN-0133, Q5a / commit bullet / Q6 discussion**: Q5a says "For an all-SF registry … *H-W reduces to bounded domain growth*: real fires number at most `Σ_ρ |⋃_k [D_ρ]_{Σ_k}|` … the only unbounded-work route is unbounded new arguments." The commit bullet repeats it ("the cheapest way to discharge H-W, through the SF case (Q5a), which needs only domain-growth bounds"), as does Q6 ("discharge the meta-level H-W by a registration-checkable bound … plus bounded domain growth, Q5a").

**Problem**: H-W is defined as `|W(σ)| < ∞ for every σ`, with `W(σ)` the **index-stamped** triples `(ρ, x, k)` where a trigger is true. Bounded domain growth (even with all-SF) does **not** imply this. Concrete counterexample: one rule ρ, domain `D = {t1, t2}` (both permanently in `[D_ρ]`, so domain growth is bounded at 2), SF trigger `T(t) ≡ ¬(∃ c ∈ L_cmt :: t ∈ coverage_G(c))`. At Σ₀ let `t2` already carry a covering comment (`T(t2)=⊥`) and `t1` not (`T(t1)=⊤`). Take the unfair infinite sequence that fires `(ρ, t2)` forever — each a no-op by RG (`Σ'=Σ`). Then `t1` is never fired, `T(t1)=⊤` at every `Σ_k` (the audit slice never gains a `t1`-covering tuple), so `(ρ, t1, k) ∈ W(σ)` for all `k` and `|W(σ)| = ∞`. The registry is all-SF with bounded domain growth, yet **H-W fails**. (Real fires over this σ number 0 — bounded.) Extinction discipline does not rescue this: X-DEF falsifies a trigger only *when fired*, and an unfired argument stays true. So all-SF + bounded domain ⇏ H-W; only fairness closes the gap, which would couple H-W to H-FAIR and contradict the note's own "genuinely separable, neither derivable from the other."

What bounded domain growth actually discharges is the **real-fire count** — exactly Q5a's formula — which is all Q6 uses (after the last real fire every fire is a no-op). The note has conflated "bounded real fires" with "H-W (`|W|<∞`)," and these differ precisely on unfair, no-op-padded sequences.

**Required**: Stop claiming Q5a discharges H-W. State the lever as *finitely many real fires*, with two independent sufficient conditions for it: H-W (via Q5) and all-SF + bounded domain growth (via Q5a + Q-EXT). Re-state Q6 to depend on "finitely many real fires + H-FAIR" rather than "H-W + H-FAIR." Then "the only unbounded-work route is unbounded new arguments" must also go — unfair starvation of a persistently-true argument is a second route to `|W|=∞`.

### Issue 2: Q-FLIP's "exactly ASN-0129's falsifier inventory" omits deposit-driven re-arming

**ASN-0133, Q-FLIP**: "what can re-arm a trigger is not 'retraction' but **exactly** ASN-0129's falsifier inventory … read off FP and PD1/PD2: a retraction shrinking an active slice the trigger reads; a BH1-type emission moving a default-view result; a BH4-footprint change from any deposit in a watched home."

**Problem**: The cited PD1 states the opposite-polarity re-armer the list drops: "(∃ x ∈ M_K :: P(x)) at view active flips ⊥→⊤ **on a K-deposit**." A bare deposit re-arms active-view triggers, and this is not "retraction," "BH1," or "BH4." It bites even on ¬-shaped (extinguishable) triggers via BH3: let `T(s) ≡ ¬def(target_of(s, K))` for a BH3-attached Binary K. With zero K-tuples from `s`, `target_of=⊥`, `T(s)=⊤`; firing emits one tuple `s→y`, giving `target_of=y`, `T(s)=⊥` (extinguished, no retraction). Depositing a **second** active K-tuple `s→y'` flips `target_of` to `⊥` ("several," ASN-0128 BH3), re-arming `T(s)=⊤` — with no retraction, no BH1, no BH4. This is exactly PD2's "A term containing `targets_keyed` is perturbed by deposits of every BH3-attached Binary type," which the inventory cites but does not include. So "exactly the inventory" overclaims relative to its own source.

**Required**: Add deposit-driven re-arming to the inventory (active-slice growth flipping `∃`-shaped or non-monotone-verdict triggers such as `target_of`/`targets_keyed`), or soften "exactly" to "in particular" and drop the completeness claim. The note's real point — folklore "no retraction ⟹ flips at most once" is unsound — survives either way, but the enumeration must match PD1/PD2.

### Issue 3: `Post_ρ` is called "PL-expressible" over a sort PL does not have

**ASN-0133, RG**: "an *emission contract* `Post_ρ` — a PL-expressible predicate over (argument, state, **emitted call set**) constraining what any fire of ρ must emit." But Q3 says the registration check "ranges over PL-typed objects **and** the surface's emission forms."

**Problem**: PL (ASN-0129, COD = `{Bool, T, ℘_fin(T), T∪{⊥}, Seq_fin(T), Map_fin, ℕ, ℕ∪{⊥}}`) has no sort for "emitted call sets," so a predicate whose third argument is a call set is not well-formed PL. Q3 implicitly concedes this by listing "emission forms" *alongside* (not within) PL-typed objects. The two passages are inconsistent, and the choice matters: a contract phrased over the **post-state** `Σ'` *is* PL but only constrains emissions up to their state effect (it cannot distinguish "emitted a covering tuple" from "one already existed"); a contract over the **call set** constrains emissions but is not PL. In a note that stakes whole theorems (PC6/PC6a, C-reach, C-emit) on precisely what PL can and cannot express, this looseness is out of character.

**Required**: Pick one. Either define `Post_ρ` as a PL predicate over `(x, Σ, Σ')` and accept that it constrains emissions only via their post-state effect (sufficient for every use here — Q3, the worked example), or state plainly that `Post_ρ` is a *meta-level* contract over `(x, Σ, emission-set)` using surface emission forms (as Q3 already treats it) and drop "PL-expressible" from RG.

### Issue 4: Q6 misattributes why post-bound fires are no-ops

**ASN-0133, Q6 proof**: "After Q5's bound is exhausted every fire is a no-op and the state is constant **(Q1's argument applies pointwise)**."

**Problem**: Q1's argument begins from *quiescence* ("quiescent ⟹ every fire a no-op"), which is exactly what Q6 is trying to prove and cannot assume here. The actual reason every post-bound fire is a no-op is Q5's bound: a trigger-true fire would be a real fire and exceed `|W(σ)|`, so every fire after the last real one is on a trigger-false argument, hence a no-op, hence `Σ'=Σ`. Citing Q1 inverts the dependency.

**Required**: Replace the parenthetical with the Q5-bound reasoning (no further real fires possible ⟹ every subsequent fire is trigger-false ⟹ no-op ⟹ state constant). While there, make the finite-σ case explicit: a *fair* finite sequence cannot end at a non-quiescent state, since a trigger-true tail argument left unfired and unremoved violates H-FAIR.

## OUT_OF_SCOPE

### Topic 1: Quiescence under a mutating registry
RG fixes `R` as a static finite set, and "what registers them … is the protocol layer above." Whether recognizability and conditional termination survive *dynamic* registration/de-registration of rules during operation (the pdef-trigger machinery makes this concrete) is a real question but belongs to a future activation-binding note, not a correction here.

### Topic 2: Concurrency and detection consistency
The fire sequence `σ` is sequential and interleaved. Racing writers (ASN-0128 I4, first-commit) and whether quiescence detection stays observer-uniform under concurrent firing are deferred by the note's own "concurrency reconciliation … left to the implementation layer." Legitimately future.

VERDICT: REVISE
