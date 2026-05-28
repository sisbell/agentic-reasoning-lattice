# Review of ASN-0077

I worked through O0–O12 plus the corollaries, the two wp's, the operation specification, and the worked example. Key checks:

**O0 (Origin extended to dom(L)):** The three-piece composition for clause (b) — L1c (chain seed = `origin(ℓ)`) + K.λ's `origin(ℓ) = d` precondition + closure of `dom(L)` under K.λ — is correctly load-bearing. The closure argument enumerates K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ, K.σ and identifies K.λ as the unique L-modifier via inspection of effect/frame clauses. The K.σ reference is routed through LP8 of ASN-0098 (a foundation), so no direct ASN-0093 citation. Sound.

**O1/O2 (origin partition and block uniformity):** O1(c) correctly traces the equivalence class to outputs of `A_C(d)` via S7d + L0 + SubAllocatorAxiom (a) and (e). O2's case split is exhaustive by S3★-aux; the link case correctly uses CL-OWN bridged by M-sub(a) (which requires #v ≥ 2 from S8a). Both branches discharged.

**F1 ≡ F2 ≡ F3:** The (F2) = (F3) collapse explicitly cites O2 (not M16a alone), correctly noting M16a applies only to dom(C) blocks while O2 handles both. (F1) ⊆ (F3) and (F3) ⊆ (F1) use B1/B3 of ASN-0058. Sound.

**O3 (structural derivation):** Correctly notes origin reads only the component sequence; S3★ discharges well-definedness of `origin(M(d)(v))`. The lifts inherit purity.

**O5/O5★, O6/O6★:** P3 + O3 for permanence; P0 + O5 for monotonic growth. Induction structures explicit.

**O11 (V-span preservation under K.μ⁺):** The cross-state depth identification (`m' = m` at Σ') correctly invokes the state-independence of `subspace(v) = v_1` and `#v` as structural projections to bridge V_{s_C}(d) at Σ ⊆ V_{s_C}(d) at Σ'. Sub-case (a) uses precondition (vi) to derive contradiction; sub-case (b) uses C0a + SC-NEQ. Both branches give the impossibility of new positions falling in ⟦σ⟧.

**O11' (K.μ⁺_L):** LinkVPositionDepthAxiom universality fixes m_L = 2 at both states; precondition (iii) of SHOWORIGIN_V forces V_{s_L}(d) non-empty when subspace(u) = s_L. Strict containment in K.μ⁺_L's effect (`⊃`) explicitly forces freshness of v_ℓ. Both sub-cases correctly handled.

**Edge cases:** The singleton I-span argument's `#b > #a` case correctly chains S7b/L0/SubAllocatorAxiom(a,e) + K.α's emission algorithm (first emission `[d.0.s_C.1]` of length `#d + 3`, subsequent via length-preserving inc(·, 0)) to derive `#b = #d + 3 = #a`. The "empty-restriction within a non-empty document" is correctly excluded via TA-strict + precondition (vi) at u.

**Worked example:** Verifies O5–O12 against concrete transitions, including K.μ~ (showing inclusion failure) and K.μ⁻ (showing admissibility loss). Both failure modes match the formal claims and absences.

**Open Questions:** All six are legitimately downstream — cross-subspace I-span behavior, transitive chain surfacing, native/transcluded distinction, unreachable-home behavior, historical containment, intra-document sharing report. None reflect REVISE-level gaps in the current ASN.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Behavior of SHOWORIGIN over I-spans crossing subspaces such that link addresses also report origins
**Why out of scope**: The ASN's I-span lift definitionally restricts to `⟦σ⟧ ∩ dom(C)`; reporting link origins from an I-span is recorded as the first open question and is appropriately a future ASN extending the lift's domain.

### Topic 2: Historical containment operation
**Why out of scope**: The ASN explicitly excludes this in the "What SHOWORIGIN does not promise" section — it belongs to a separate operation over Σ.R, recorded as the fifth open question.

### Topic 3: Surfacing the intermediate transclusion chain
**Why out of scope**: SHOWORIGIN reports direct origin (one document tumbler per address), not the chain of intermediate documents. The ASN correctly delegates this to a separate operation (second open question).

### Topic 4: Native vs transcluded content distinction within a document's arrangement
**Why out of scope**: A separate operation, recorded as the third open question.

VERDICT: CONVERGED
