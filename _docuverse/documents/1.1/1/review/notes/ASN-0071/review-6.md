# Review of ASN-0071

## REVISE

(none)

## OUT_OF_SCOPE

(none — the ASN's "What we do not specify" section and "Open Questions" appropriately defer visibility filtering, replica consistency, presentation order, historical-containment queries via R, and the relationship to operations that mutate state)

## Analysis notes

I checked the load-bearing arguments and found them sound:

**Subspace confinement** (`t₁ = u₁ = s_C` for `t ∈ ⟦σ⟧`): The proof correctly invokes `actionPoint(ℓ) ≥ 2` to place position 1 in TumblerAdd's prefix-copy region, then uses T1 case (i) at k=1 (vacuous-agreement-before-k, length bounds `≥ 1` from T0) twice to rule out `t₁ < u₁` and `t₁ > u₁`, closing via NAT-order trichotomy on ℕ. The argument holds for `t` of any length, including longer extensions, because it depends only on position 1.

**Subset claim** `iaddrs(Q)(Σ) ⊆ dom(Σ.C)`: Sound. The state-explicit reading is correctly flagged. The counter-example `u = [1, 5]`, `ℓ = [2, 0]` justifies the `actionPoint(ℓ) ≥ 2` precondition — I verified that `[2, 1] ∈ ⟦σ⟧` and `subspace([2, 1]) = s_L`.

**Worked scenario**: All ASN-0047 preconditions discharge cleanly (K.δ entity creation, K.α first emission, K.μ⁺ first-position binding with ValidFirstInsertionPosition at m=2, K.ρ provenance, transclusion via second K.μ⁺ binding `a₁` in `d_B`). The reach computation `v_A ⊕ δ(1, 2) = [s_C, 2]` and the membership verifications for `[s_C, 1, 5] ∈ ⟦σ_A⟧` (T1 case ii for left, case i at k=2 for right) check out. F-SHARE, F-DIST, F-PART, F-FILT, F-CUR are verified concretely.

**Finiteness**: The three-step proof (Σ₀ has empty E_doc since n₀ is a node; each elementary transition adds ≤1 to E_doc with K.δ being the only modifier; reachable states have finite ancestry by ExtendedReachableStateInvariants) is rigorous. The orthogonality of SequentialTransitionAxiom (atomicity) versus reachability (finite ancestry) is correctly attributed.

**Definitional consequences** (F-COMP, F-SOUND, F-PART, F-DIST, F-SHARE, F-EMPTY, F-FILT, F-LOC): Each unfolds directly from F-find or F-iaddrs as claimed. The "obligations on implementations" framing correctly characterizes F-COMP and F-SOUND as the two halves of the defining iff.

**Foundation citations**: All cross-references go to foundation ASNs (34, 36, 47, 53, 58); no non-foundation ASN references. Notation reuses foundation definitions (`⟦σ⟧`, `subspace`, `origin`, S3★, S7, P0–P2, L0) without reinvention.

**Currency vs. permanence**: The reconciliation through versioning is appropriately hedged as "convention, not a structural guarantee," and the operation's commitment to current-state semantics versus R-based historical semantics is correctly framed.

VERDICT: CONVERGED
