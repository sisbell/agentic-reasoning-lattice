# Review of ASN-0071

I checked the three substantive proofs (subspace confinement, the `resolve` equivalence, and finiteness), the worked scenario against its claimed postconditions, and the boundary cases (empty query, unresolvable positions, infinite span reach, self-reference of `d_s`).

## Verification notes

**Subspace confinement (the one non-trivial proof).** The argument that every `t ∈ ⟦σ⟧` has `t₁ = u₁` is complete: `(u ⊕ ℓ)₁ = u₁` holds because `actionPoint(ℓ) ≥ 2` forces `ℓ₁ = 0` and places position 1 in TumblerAdd's prefix-copy region; the T1 interval squeeze (ruling out `t₁ < u₁` via `u ≤ t`, and `t₁ > (u⊕ℓ)₁` via `t < u⊕ℓ`) correctly leaves `t₁ = u₁ = s_C`. The `actionPoint(ℓ) ≥ 2` precondition is genuinely load-bearing, and the `u=[1,5], ℓ=[2,0]` counterexample correctly exhibits a straddling span when it is dropped. S3★ then routes `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` with both sides read state-dependent — stated honestly.

**`resolve` equivalence.** `{a_j + k} = {M(d_s)(v) : v ∈ dom(f)} = iaddrs_one` via B1 (coverage) + B3 (consistency) is correct, and the set-flattening dedup argument under M14 is sound. The relaxation boundary (positions outside `dom(M(d_s))`) is handled.

**Worked scenario.** F-SHARE, F-DIST, F-PART, F-FILT, F-CUR, and home/transcluding recovery each check against the concrete `{d_A, d_B}` result. The infinite-`⟦σ_A⟧` / finite-intersection point (F-FILT) is verified explicitly.

**Finiteness.** The three-step induction (`Σ₀.E_doc = ∅`; K.δ adds ≤ 1 and only it touches `E`; finite elementary ancestry of reachable states) is complete, including the correct note that the bound is against the elementary count, not the composite count.

**Definitional honesty.** F-COMP/F-SOUND are correctly framed as the two halves of the defining biconditional (obligations on implementations), not as independent theorems — avoiding a proof-by-definition trap. The superset-oracle failure mode is a useful, correctly-derived conformance observation.

No cross-ASN references outside the foundation set (0047/0053/0058); `actionPoint`, `Pos`, `⊕`, T1 are all base/foundation vocabulary.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-state `find` and historical `R`
The "Permanence and currency reconciled" section correctly defers the `R`-based ever-containing query to a separate mechanism; the open question is properly future territory, not a gap here.

### Topic 2: Distributed replica freshness and visibility filtering
Both are explicitly listed under "What we do not specify" with deferral rationale — correctly out of scope.

VERDICT: CONVERGED
