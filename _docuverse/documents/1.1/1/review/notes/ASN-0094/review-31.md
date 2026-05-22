# Review of ASN-0094

I worked through the major proofs and verified case-exhaustiveness, boundary coverage, and consistency with the cited foundations.

**Verifications:**

1. **Sh0–Sh4 inductions** are case-exhaustive (A: no change to L_K/A_K; B: K.λ adds at K with K≁R; C: Emit_R contracts A_K with K≁R; D: K~R simultaneous add-and-contract). Case D's structural bound `|leaving| ≤ 1` is correctly derived from R0a + R1 + PrefixSpanCoverage. The empty-baseline asymmetry between Sh0–Sh3 (per-tuple-relaxable) and Sh4/per-K disciplines (require full empty-baseline) is explicitly scoped in *Initial-State Baseline*.

2. **RetractionTargetNotOnChain** generalizes to arbitrary `b ∈ dom(Σ.L)`, which is what makes both EffectiveWpSimplification consumption sites (prior-R-tuple discharge in Step 1, new-emission discharge in Step 2's K~R case) reachable. Case II's NAT-card additivity argument is sound; Sub-case II.A's T3-collapse at equal lengths and II.B's suffix construction at strictly shorter `b` are both worked out.

3. **AllocatedAddressAntichain's Sub-case 3b "by symmetry"** is sound: Steps 3.1 (zero-position enumeration via NAT-card) and 3.2 (E-field first-position agreement via T4b) are domain-independent; only Step 3.3 differs across sub-cases, and the swap is mechanically described.

4. **EffectiveWpSimplification's** conditional-on-substrate-reach framing correctly carries the "calls Sh-conf would reject never reach K.λ, so wp_086 is moot there" caveat, while the effective-wp form holds at every call site.

5. **NullifyActiveSubsetCompatibility** preserves ASN-0086's active-subset content (single-tuple scope + R6a stability) across clause (iii) and clause (ii). The audit-slice multiplicity loss is documented as a deliberate set-semantics commitment of `shape(R) = (*, 1, A, A_rel, ⊤)` with `idem = ⊤`; layers needing multiset are directed to attributed retraction.

6. **Cross-ASN references**: only foundation (ASN-0034, ASN-0043, ASN-0086). ASN-0093 references are confined to ASN-0086's catalog imports.

7. **Boundary cases**: empty L_K at Σ_init; empty F (c_F = 0 boundary of c_F = *); empty G (c_G = 0|1 of Provenance); first emissions; concurrent retraction (Case D); cross-domain prefix attempts (rejection 2 + AR3); K ∉ T_cat (rejection 4); duplicate-Nullify suppression — all exhibited.

8. **No hand-waves**: ✓ used as closure markers backed by explicit text; "mirrors"/"by symmetry" backed by elaboration of what is and isn't shared.

9. **Gate ordering** at Sh-conf is fully specified (SHCD → canonical-form → Sh4/FDD → cardinality/target-domain → K.λ), with mutual exclusion of FDD and SHCD justified by `shape(K).idem` value-fixing.

## REVISE

(No items identified.)

## OUT_OF_SCOPE

The Open Questions section appropriately enumerates scope boundaries (cross-process consistency, (0,0) shapes, ghost-targeting slot semantics, composite shapes, per-K opt-in as a sixth shape component). Each is tagged with kind (design choice / refinement candidate / scope boundary).

VERDICT: CONVERGED
