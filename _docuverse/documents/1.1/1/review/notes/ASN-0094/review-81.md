# Review of ASN-0094

## REVISE

### Issue 1: Forward reference EffectiveWpSimplification → RetractionSelfFreshness

**ASN-0094, Section "Corollary — EffectiveWpSimplification", Step 3.5(b)**: "this is exactly Lemma — RetractionSelfFreshness part (i), applicable because all its preconditions hold"

**Problem**: RetractionSelfFreshness is stated *after* EffectiveWpSimplification in the ASN's section order, but EWS's Step 3.5(b) depends on it. RSF's proof has no upstream dependency on EWS (it uses only Sh-conf, Sh1, Sh3, and LinkAddressNotPrefixOfEmit — all stated earlier). The forward reference is acknowledged in EWS's proof text but creates ordering confusion: a reader encountering EWS naturally checks its cited dependencies, finds RSF unstated, and must skip ahead to verify the discharge.

**Required**: Move "Lemma — RetractionSelfFreshness" before "Corollary — EffectiveWpSimplification" so that EWS consumes a previously-established lemma rather than forward-referencing.

### Issue 2: Sh0–Sh4 lemma statements omit the empty-baseline precondition

**ASN-0094, Sections "Cardinality (Sh0, Sh1)", "Target Domain (Sh2, Sh3)", "Idempotency (Sh4)"**: Lemma statements quantify over "every reachable state Σ" without explicit baseline precondition.

**Problem**: The Initial-State Baseline section states "Sh0–Sh4 presuppose `L_K^{Σ_init} = ∅` for every `K ∈ T_cat`", and each preservation proof's base case discharges by this baseline ("at `Σ_init`, every `L_K^{Σ_init} = ∅`; the universal is vacuous"). But the lemma statements themselves don't carry this precondition. The Open Questions section flags non-empty initial link stores as a scope boundary, but a load-bearing precondition should be visible in the statement, not relegated to a separate section. A consumer reading Sh4 alone gets a stronger claim than the proof actually delivers.

**Required**: Add explicit precondition to each Sh0–Sh4 statement: "Under the baseline assumption `L_K^{Σ_init} = ∅` for every `K ∈ T_cat`, every reachable state Σ satisfies ...". Mirror in SHCD's and FDD's preservation theorems where the same baseline is consumed.

### Issue 3: Tuple-Classifier walkthrough setup contradicts Per-walkthrough convention

**ASN-0094, Tuple-Classifier walkthrough**: "Pre-allocate a home `home_K ∈ dom(Σ_0.M)` and a `K_neighbor`-tuple `σ ∈ A_rel^{Σ_0}` (the tuple to be endorsed) at a prior step from `Σ_init`"

**Problem**: The Initial-State Baseline section defines Σ_0 as "a pre-emission state reached from `Σ_init` by a finite sequence of K.σ/K.α steps (no K.λ-steps)". Creating σ ∈ A_rel^{Σ_0} requires a K.λ-step somewhere in the Σ_init → Σ_0 path (specifically, an Emit_{K_neighbor} step), contradicting the "no K.λ-steps" clause. Other walkthroughs honor the convention strictly; this one doesn't.

**Required**: Either (a) relax the convention to allow K.λ-steps at types other than the walkthrough's K-under-test, with explicit statement of which Ls are non-empty at Σ_0; or (b) restructure the Tuple-Classifier walkthrough to emit σ within its own emission sequence (Emission 0 creates σ via K_neighbor, Emission 1 endorses via K_tc) so the convention holds.

### Issue 4: CaseAClosureForLK lemma's proof is unusually terse

**ASN-0094, Section "Cardinality (Sh0, Sh1)"**: "*Proof.* Each sub-class's case-equation discharge is the direct citation given inline above; the Case B claim follows from R3 (ASN-0086) under the *Emit_K routing commitment*. ∎"

**Problem**: A separately-named lemma should have a structured proof body that explicitly discharges each enumerated sub-class. The current "proof" defers to inline citations within the statement text, conflating statement with proof. Sh0–Sh3 then invoke "by Lemma — CaseAClosureForLK at Case A", which forces verification to chase inline citations in the lemma's stated cases rather than reading a structured proof.

**Required**: Restructure so the three sub-classes are stated as a claim, then proved in a separate proof body with each sub-class discharged explicitly (e.g., "Sub-class 1 (K.σ/K.α): preserves `Σ.L` pointwise by ASN-0086's `→` Definition's frame conditions, hence `L_K^{Σ'} = L_K^Σ`. Sub-class 2: ... Sub-class 3: ... Case B: ...").

### Issue 5: "Audit-slice set-semantics commitment" referenced but not formally named

**ASN-0094, BundledDirectedPair walkthrough's "Empty-G admissibility" paragraph**: "Sh4 suppression and the audit-slice set-semantics commitment apply uniformly at `n = 0`"

**Problem**: The phrase "audit-slice set-semantics commitment" appears here but is not defined as a named commitment elsewhere. The Nullify Compatibility section discusses "set semantics at the bare Nullify alias" as a load-bearing departure from ASN-0086, but does not name it as a commitment. A reader chasing the term finds no formal definition.

**Required**: Either (a) introduce the named commitment formally in the Nullify Compatibility section ("**Commitment — AuditSliceSetSemantics.** Under the *Sh4 idempotency contract* at K with `shape(K).idem = ⊤`, two consecutive Emit_K calls with identical canonical slot-pairs produce one tuple in `L_K^Σ`, not two."), or (b) replace the BundledDirectedPair phrase with existing terminology ("Sh4 suppression applies uniformly at `n = 0`").

### Issue 6: EffectiveWpSimplification's Step 3.5 reads as inserted afterthought

**ASN-0094, Corollary — EffectiveWpSimplification proof**: Step labeled "*Step 3.5 — `addr(τ_new) ∉ nullified(Σ')` for the active-subset postcondition*" between Step 3 and Step 4.

**Problem**: The fractional numbering signals incomplete integration: Steps 1, 2, 3 derive the wp_086 simplification, Step 4 assembles wp_eff, and Step 3.5 establishes that τ_new actually reaches A_K^{Σ'} (not just L_K^{Σ'}). This is integral to the corollary's "fresh deposit in A_K^{Σ'}" postcondition, not a side remark. Fractional numbering is a reviser-drift fingerprint.

**Required**: Renumber to a clean 1–5 sequence with Step 4 being the active-subset extension and Step 5 the wp_eff assembly.

### Issue 7: SHCD preservation Case A omits the four-class enumeration that Sh4 and FDD perform

**ASN-0094, SHCD "Preservation under the single-home commitment", Step (Case A)**: "`L_K` is unchanged. The property is inherited tuple-by-tuple from the IH (no new τ to check; existing τ retain `home(addr(τ)) = d_K`)."

**Problem**: Sh4 and FDD enumerate four classes of `↦`-steps that produce the case-equation (K.σ/K.α, K.λ at K' ≁ K with K' ≁ R, K.λ at K' ~ R without τ leaving, arrangement-modifying steps). SHCD's Case A makes the assertion without the enumeration. The discharge is morally identical, but a reader verifying SHCD's preservation cannot confirm Case A's coverage without re-deriving the classification. Asymmetric proof structure across closely-related preservation theorems invites inconsistency on revision.

**Required**: Add the four-class enumeration to SHCD's Case A, citing the case-equation discharge for each, matching Sh4's and FDD's structure.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate atomicity for Sh4/FDD/SHCD contracts

**Why out of scope**: The framework explicitly commits to single-process substrates and flags multi-process as a scope boundary in Open Questions. Distributed atomicity protocols at the `~`-class scope are framework-extension work.

### Topic 2: Container-level link targeting via an A_M symbol

**Why out of scope**: Extending `t_F`/`t_G` to A_M (`dom(Σ.M)`) for metalink-style targeting would expand the shape vocabulary and Sh-conf clause (d). Flagged in Open Questions as a scope boundary, not a correction.

### Topic 3: Closure theorem for composite predicates

**Why out of scope**: The Consequences section explicitly states "The framework does not establish a closure theorem about these primitives." Characterizing the template language's expressive power belongs to a future ASN.

VERDICT: REVISE
