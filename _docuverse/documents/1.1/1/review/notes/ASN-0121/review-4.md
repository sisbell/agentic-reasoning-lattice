# Review of ASN-0121

## REVISE

### Issue 1: nullified-monotonicity argument leaves K.δ uncovered

**ASN-0121, "The answer is forced" (the two monotonicity facts)**: "Second, `nullified` is non-decreasing across `→`. R6a (ASN-0086, RetractionStability) establishes this across ASN-0086's allocation-only relation `K.σ ∪ K.α ∪ K.λ`; the editing and provenance operations lie outside that relation, but each leaves `Σ.L` literally unchanged (K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~ rewrite only `Σ.M`; K.ρ writes only `Σ.R`) ... So `nullified` is constant across every editing/provenance step and monotone (R6a) across every allocation step, hence non-decreasing across all of `→`."

**Problem**: The ASN fixes `→` as the ASN-0047 vocabulary `{K.α, K.λ, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ}` — which contains **K.δ** (document/entity registration) and contains **no K.σ** (ASN-0047 registers documents via K.δ, not K.σ). The monotonicity argument then sorts operations into exactly two buckets: those R6a covers (R6a is stated over `K.σ ∪ K.α ∪ K.λ`, so within ASN-0121's vocabulary it reaches only K.α and K.λ), and the editing/provenance ops K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~/K.ρ. **K.δ falls in neither bucket.** It is not K.α or K.λ (so R6a does not apply to it — R6a's relation has K.σ, not K.δ), and it is not named among the editing/provenance ops whose "leaves `Σ.L` unchanged" justification is given. The conclusion "non-decreasing across all of `→`" is therefore not discharged for every member of `→`. The same hole recurs in FL-RET ("non-decrease of `nullified` across the full transition vocabulary — R6a ... for allocation steps, and constancy ... across the editing and provenance operations") and is relied on by FL-MON, FL-RET, and FL-REACH's permanence reasoning.

(Note the companion link-store fact does *not* have this hole: "only K.λ touches the link store ... with **every other operation** framing `Σ.L` fixed" is a genuine catch-all that covers K.δ. Only the `nullified` argument enumerates buckets and omits K.δ.)

**Required**: Add explicit handling of K.δ: document/entity registration extends `Σ.E`/`Σ.M`/`Σ.C`/`Σ.R` but leaves `Σ.L` (hence `L_R^Σ` and `nullified`) literally unchanged, so `nullified` is constant across every K.δ step. Equivalently, restate the argument structurally — `nullified` is a function of `Σ.L` via `L_R^Σ`; `Σ.L` changes only under K.λ; R6a gives monotonicity there; every other operation in `→` (including K.δ) frames `Σ.L` fixed — which closes the gap uniformly without per-bucket enumeration.

## OUT_OF_SCOPE

### Topic 1: Version- and time-qualified link inquiry
**Why out of scope**: The behaviour of a retracted link under a prior-version or time-qualified inquiry is correctly deferred to an Open Question; the current operation inquires against the current state only. No claim is made, so nothing to fix here.

### Topic 2: V-spec (arrangement-mediated) request phrasing and its agreement with the I-address regime
**Why out of scope**: The ASN treats V-spec phrasing as a separable front-end convenience and raises the I-address/V-spec agreement invariant as an Open Question rather than a claim. Appropriate.

VERDICT: REVISE
