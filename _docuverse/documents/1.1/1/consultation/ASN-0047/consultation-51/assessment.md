# Channel Assignment — ASN-0047 review-51

**Date:** 2026-05-16 16:31

```
## Issue 1: CL-UNIQ is not preserved by K.μ⁺_L
Reason: The fix (add precondition `ℓ ∉ ran(M(d))`) is derivable from the ASN's own content — the ASN already cites Nelson's "permanent order of arrival" (LM 4/31) and Gregory's `findnextlinkvsa` + single `docopy` (do2.c:151–167) as the design and implementation evidence supporting one-position-per-link. Strengthening the precondition restores CL-UNIQ consistent with both cited sources.
```

```
## Issue 2: ASN-0047's L3 contradicts ASN-0043's L3 (foundation)
Reason: The evidence on both sides is already cited extensively in the ASN (Nelson LM 4/12 on type-as-optional-classifier; Gregory on udanax-green's empty-Θ storage admission). The remaining choice — revert ASN-0047's L3 to the foundation's non-empty form, or formally propose an ASN-0043 revision — is procedural/methodological and does not require new channel input.
```

```
## Issue 3: Worked example notational error in K.μ⁻ counterfactual
Reason: Pure notational/computational fix. At m_{s_L} = 2 the form `[S, 1, ..., 1, k]` collapses to `[S, k]`, so the corrected values are derivable directly from the example's pre-state without consultation.
```

```
## Issue 4: S0 and S1 are per-transition properties listed in the per-state theorem
Reason: Structural classification fix derivable from ASN-0036's own statement of S0/S1 as universally quantified over `Σ → Σ'`. Move them to ExtendedTransitionInvariants where the analogous per-transition properties (P0, P1, P2, P3★, P5★, L12) already live.
```

```
## Issue 5: P4a is not adapted to the extended state
Reason: Re-derivation is mechanical given the J1'★ statement already in the ASN. Since R ⊆ T_elem × E_doc and P7 constrains R to dom(C)-grounded entries, the witness state's V-position is necessarily content-subspace by S3★ — no new design or implementation evidence is required.
```

```
## Issue 6: NodeUniqueAllocation does not constrain node hierarchy structurally
Reason: The ASN's prose commits to "every node address descends from the single bootstrap root n₀" but does not formalize this as an axiom; deciding whether to elevate it (vs. defer to protocol level) requires design intent on whether node lineage is essential and implementation confirmation that lineage holds uniformly.
Nelson question: Does the Xanadu design require all node addresses to descend from a single bootstrap root as a structural property of the abstract model, or is node lineage a protocol-level concern that may admit disconnected ownership trees?
Gregory question: Does udanax-green enforce that every node address descends from a single root (e.g., via a single global granfilade), or do independent node-allocation trees occur in the implementation?
```

```
## Issue 7: Bootstrap node n₀ is underspecified
Reason: The ASN leaves n₀'s structural form open beyond `IsNode(n₀)`. Bounding it requires knowing whether the design designates a canonical form and what form the implementation actually uses for the root — both channel-specific facts not derivable from the ASN's existing text.
Nelson question: Does the design specify a canonical structural form for the bootstrap node (e.g., a single-component tumbler), or is any tumbler with `zeros = 0` admissible as n₀?
Gregory question: What is the structural form of the root node in udanax-green's granfilade — single-component, multi-component, or otherwise — and is there a single canonical root or multiple?
```

```
## Issue 8: K.μ~ frame is stated as "derived below" without inline derivation
Reason: Internal restructuring — either restate the frame as part of K.μ~'s contract (with explicit proof-from-decomposition reference) or note that K.μ~ inherits its frame entirely from its decomposition. The choice does not depend on external evidence.
```

```
## Issue 9: Decomposition of K.μ~ over-restricts the choice of intermediate state
Reason: Internal definitional choice — either prove existence of some admissible decomposition for every valid π (generalizing the proof) or commit K.μ~'s semantics to full clear-and-rebuild. K.μ~ is already defined abstractly via bijection π, so the decomposition is a proof artifact, not a semantic commitment requiring channel input.
```
