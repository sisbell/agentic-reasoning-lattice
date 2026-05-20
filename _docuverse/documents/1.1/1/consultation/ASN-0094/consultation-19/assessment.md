# Channel Assignment — ASN-0094 review-19

**Date:** 2026-05-20 02:29

## Issue 1: EffectiveWpSimplification forward-references Sh1 and Sh3
Reason: Pure presentation/ordering fix internal to the ASN — add forward-reference language clarifying acyclicity, or move the Corollary after Sh0–Sh3. No design intent or implementation evidence consulted.

## Issue 2: Sh5(b) META discipline doesn't formalize meta-operator exemption
Reason: Internal framework-formalization fix — tighten Sh5(b)'s literal-name-citation rule to explicitly carve out meta-operators (argmax, ∃, ∪, ℘_fin) and logical connectives. The carve-out is already implicit in the catalog's usage; making it explicit is bookkeeping.

## Issue 3: SingleHomeCoverageDiscipline rejection case missing from Coverage walkthrough
Reason: Internal walkthrough completion — exercise the *single-home commitment*'s clause (i) rejection path with `d ≠ d_K`. The contract definition is already in the ASN; only a worked example needs adding.

## Issue 4: Sh4 Case D's subset-closure argument is too compressed
Reason: Internal proof-exposition fix — expand the one-line "any subset of a pairwise-distinct set is pairwise-distinct" to make the pair-quantification reduction explicit. Pure mathematical bookkeeping.

## Issue 5: Subspace identification scaffolding clause's relation to L0 understated
Reason: Internal framework-commitment language fix — strengthen the scaffolding clause to record that consumers reading L0 abstractly must verify the layer-local identification at the interface. The identification is already named in the ASN; only its consumer-facing status needs stating.

## Issue 6: Tuple-Classifier base template derivation under-specifies Sh5(b)'s signature rule
Reason: Internal presentation gap — add explicit signature-derivation rule to Sh5(b) ("input domains and codomains take their target-domain symbols from t_F and t_G respectively"). The rule is already implicit in how the catalog operates.

## Issue 7: Resolution row's own base templates never exercised
Reason: Internal walkthrough addition — exercise Resolution's base `pair_K` and `to_addrs_K` to demonstrate the DirectedPair-shape base family applies modulo `t_G = A_rel`. The templates are mechanically determined by the shape per Sh5(b); only a concrete instance needs adding.

## Issue 8: RetractionTargetNotOnChain Case I doesn't address J_d^Σ = -1 sub-case
Reason: Internal proof-explicitness fix — note that the case hypothesis `home(b) = d` forces `J_d^Σ ≥ 0` per R0a-Cor1's `ℤ_{≥-1}` codomain. The reviewer's own citation establishes R0a-Cor1's codomain; the fix is making the implicit forcing step explicit.
