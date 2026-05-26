# Review of ASN-0098

I traced each proof, verified foundation citations, checked boundary cases, and worked through the concrete trace.

## What I checked

**Stored-link invariants (LP2, LP3 and ★ versions, Store Monotonicity★):** Inductive proofs are explicit; base case (reflexive closure) and inductive step are both stated. L12 of ASN-0043 is applied correctly.

**Frame lemmas (LP4–LP8, LP14):** LP4's intersection form `dom(Σ.M) ∩ dom(Σ'.M)` is correctly motivated, with M1 of ASN-0093 supplying the lift for downstream uses. LP8 unifies K.σ and K.δ-IsDocument under a shared document-registration hypothesis, with both parts (pre-state preservation and newly-registered emptiness) discharged.

**Operation effects (LP9, LP10, LP11):** Exact set-difference characterisations are given with both inclusions proved. LP9's freshness re-derivation for K.μ⁺_L via S3★-aux + SC-NEQ + TS4 is sound and self-contained even though ASN-0047 already states `⊃`. LP10's boundary case (`n'_{s_C} = n'_{s_L} = 0`) is addressed. LP11's range-equality second postcondition is derived rigorously.

**LP-Fin's bound-then-finiteness argument:** Verified the case structure on `#d`:
- Sub-cases (i) `d_0 ≼ d` and (ii) disagreement at `j ≤ #d_0` are jointly exhaustive on `#d > #d_0`.
- For `#d ≤ #d_0`: prefix-of-d_0 derivation is sound; admissible range `{z_2+1, …, #d_0}` excludes `#d ≤ z_2` (needs both zeros) and `#d = z_2` (T4 endpoint).
- Sub-case A (`z_2 < #d < #d_0`): position `#d+1` past both zeros forces `d_0[#d+1] ≥ 1`, divergence at `#d+1` gives `a < s`, contradiction.
- Sub-case B (`#d = #d_0`): subspace-component analysis at position `#d_0 + 2` plus chain-index analysis at `#s` yields exactly `n` candidates.
- Non-canonical remark: within-chain construction at action point `k_ℓ < #s` shows `|F ∩ [s, s ⊕ ℓ)| = ℵ₀` for `#ℓ < #s`. Ground (ii) of definitional non-tightness correctly covers `#ℓ > #s` and `#ℓ = #s` with non-ordinal `ℓ`.

**LP12b proof:** Chain dom(Σ.L) ⊆ F → LP-Fin Corollary at X = s_C → coverage ∩ dom(Σ.L) = ∅ → no link-subspace V-position in projection (via S3★ contradiction) → wp evaluates to false. Each step is licensed by stated foundations.

**Tightness achievability (four cross-chain cases):** Same-document cross-subspace direction flip is correctly handled — for `A_C(d_0)`-spans interferers excluded above, for `A_L(d_0)`-spans excluded below. Descendant case via zero-count balance giving `x_1 ≥ 1` at position `#d_0 + 1`. Ancestor case symmetric via `y_1 ≥ 1`. Non-nesting case via Divergence case (i). Each T1 case-(i) application has comparison-range obligations discharged.

**LP19a/LP19 separation:** Clean. LP19a is a state-independent freshness statement about `a_new`; LP19 chains it to the projection consequence via the coverage definition being state-free.

**Worked trace:** Verified arithmetic. For slot 2 with `e₂ = {(i₁, δ(1, #i₁))}` and coverage `{t : i₁ ≼ t}`, sibling chain elements `i₂, i₃, i₄` are correctly excluded from coverage (equal length, distinct → no prefix relation). K.μ~ branch from Σ_1 with `π(v₁) = v₃, π(v₂) = v₂, π(v₃) = v₁` yields slot-2 projection moving from `{v₁}` at Σ_1 to `{v₃} = π({v₁})` at Σ_3, consistent with LP11.

**Citations:** All references are to foundation ASNs (0034, 0036, 0040, 0043, 0047, 0053, 0058, 0093). No drift outside the foundation set.

**Boundary cases handled:** Empty endset (project = ∅), empty arrangement, K.μ⁻ to empty post-state, empty slots 1/2 with non-empty type, R = ∅ in LP12a, unit-width spans, n = 1 in LP-Fin.

VERDICT: CONVERGED
