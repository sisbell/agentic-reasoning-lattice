# Review of ASN-0094

## REVISE

### Issue 1: Sh4 contract is described as "registered" but is actually automatic for idem=⊤

**ASN-0094, EffectiveWpSimplification Corollary**: "At a K registered under exactly one of SHCD, Sh4, or FDD, `Π_K` reduces to the single corresponding conjunct" and "At a K registered under no per-K discipline (i.e., K's row of the catalog lists no opt-in entries...), `Π_K` reduces vacuously to `⊤`".

**Problem**: The Sh4 idempotency contract is automatic for any K with shape(K).idem = ⊤ — there is no opt-in registration step. But the Π_K prose treats Sh4 as one of three "registered" disciplines alongside SHCD and FDD (which are genuine opt-ins). This conflates the idem flag with discipline registration. Under a literal reading of "no opt-in entries", an idem=⊤ K with no FDD would have Π_K reduce vacuously to ⊤, dropping the C = ∅ conjunct entirely — which contradicts the framework's preservation argument for Sh4.

**Required**: Clarify that "K under the Sh4 idempotency contract" means "shape(K).idem = ⊤ AND K not registered under FDD", and that this is structurally determined by the shape, not an opt-in. The four-case Π_K reduction in the corollary should explicitly be: (idem=⊤, no FDD) ⇒ Sh4 conjunct; (idem=⊤, FDD) ⇒ FDD conjunct; (idem=⊥, no SHCD) ⇒ vacuous; (idem=⊥, SHCD) ⇒ SHCD conjunct.

### Issue 2: SubstrateConsumerActiveSubsetCompatibility Lemma is heavy for its substantive content

**ASN-0094, Nullify Compatibility section**: The Lemma's statement, proof, "Consumed by" enumeration, "Compatibility envelope" scope statement, and per-row table reference span several pages.

**Problem**: The substantive content reduces to: "if your postcondition can be evaluated at the unchanged Σ on the rejection branch, it's preserved across Sh-conf's ⊥-extension". The (α)/(β) split is useful as a framework note, but elevating it to a numbered Lemma with formal proof creates the appearance of independent depth where the result is nearly tautological — rejection branches preserve state pointwise by construction (no `↦`-step fires), and "preservation" follows.

**Required**: Either condense the Lemma into an explanatory paragraph at the end of the Nullify Compatibility section (the substantive (α)/(β) checklist for downstream consumers is worth keeping), or strengthen the Lemma's content with a genuine claim — e.g., establishing that the envelope is *exhaustive* (no compatible surface exists outside the envelope characterization), which is currently asserted but not proved.

### Issue 3: LinkAddressNotPrefixOfEmit's general additivity argument is preserved but trivial under current scaffolding

**ASN-0094, LinkAddressNotPrefixOfEmit Step II.1**: The preamble explicitly states "the preamble's `zeros(a) = zeros(b) = 3` forces `zeros(w) = 0` (Step II.1's NAT-card additivity at every substrate-reachable `b, a`), so the substantive contradiction at substrate-reachable inputs surfaces at Step II.2 or II.3, not at Step II.1."

**Problem**: The framework preserves the general NAT-card additivity argument "for citation purity" against hypothetical future scaffoldings that admit deeper K.λ emissions. But the present ASN supplies neither (a) a scaffolding clause admitting such depths nor (b) a worked example exercising `#w ≥ 2 ∧ zeros(w) ≥ 1`. The result is a load-bearing-looking derivation that under current substrate commitments is structurally tight at `#w ≤ 1` and degenerate at `zeros(w) = 0`. The general argument is correct but its inclusion implies a reach the current framework does not exercise.

**Required**: Either (a) commit explicitly to a scaffolding extension that exercises the general additivity, or (b) inline the trivial discharge at the current scaffolding and note the general argument as an aside for future extension. The current formulation reads as if the general additivity is needed when it isn't.

### Issue 4: The Π_K conjunct's necessity argument needs tightening

**ASN-0094, EffectiveWpSimplification Corollary**: "Without the `Π_K` conjunct, the prior wp_eff form `d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)` would be necessary but not sufficient for the postcondition `(a, F, G) ∈ A_K^{Σ'}`".

**Problem**: The argument that Π_K is *necessary* assumes the postcondition requires a *new* tuple to be deposited. But the corollary statement names the postcondition simply as `(a, F, G) ∈ A_K^{Σ'}`, which on a contract-suppressed call could be satisfied by a *pre-existing* tuple (the one whose presence caused suppression). The Sh4 contract suppresses precisely because such a pre-existing tuple already witnesses the slot-pair. So the postcondition holds at Σ' = Σ via the existing witness, even though no new tuple was added — making the prior wp_eff form sufficient *for the postcondition as written*, just not for the strengthened reading "a new tuple satisfying (F, G) was deposited".

**Required**: Either weaken the necessity argument to apply specifically to the "new tuple deposited" reading (and label this postcondition variant explicitly), or strengthen the postcondition statement to require new-tuple deposition. The current formulation conflates the two readings.

### Issue 5: Resolution row's "standalone admissibility" verification could be tighter

**ASN-0094, Resolution catalog row and standalone walkthrough**: The catalog row states "Standalone admissibility (settled and exhibited)" and the "Resolution base templates at a standalone K (no `_via` consumer in scope)" walkthrough exercises K = approved_by.

**Problem**: The walkthrough exhibits Emissions AB1, AB2, AB3 and tabulates base templates — but the "standalone" claim hinges on whether Sh5(b)'s discipline admits the base templates at a Resolution-registered K with no parametric consumer. The walkthrough demonstrates the templates evaluate correctly, but doesn't explicitly walk the Sh5(b) audit checklist (steps 0-3) at the standalone registration. The audit table lists Resolution under "Accepted" with body convergence flagged as hand-curated, but the standalone path's admissibility under Sh5(b) is asserted rather than verified against the audit procedure.

**Required**: Add a brief Sh5(b) audit walk for the standalone Resolution registration: confirm that each base template body cites only data symbols in categories (i)-(iv), with no parametric K_res argument in scope. This would make the "settled and exhibited" claim mechanically falsifiable in the same form as other audit table entries.

### Issue 6: Catalog audit table density limits extension feasibility

**ASN-0094, Sh5(b) section**: The catalog-wide citation audit table has 11 rows with dense per-symbol classifications; only one worked check (`latest_K_for_addr`) is presented in detail.

**Problem**: For an extension author registering a new catalog row, the Sh5(b) discipline requires per-symbol classification against six categories. The minimal review checklist (steps 0-3) describes the procedure but the audit table's terse cell format makes the classification logic opaque. Without additional worked checks for rows with non-trivial body shapes (Retraction's set-equality F-side; Provenance's partial G-handling; BundledDirectedPair's c_G = * empty-G admission), an extension author lacks worked examples for the harder classification cases.

**Required**: Add worked checks for at least two more representative rows beyond `latest_K_for_addr` — Retraction's `pair_K(F̂, b)` and Provenance's `to_K(b)` are good candidates because they exhibit non-standard body shapes (set-equality on F; ⊥-filtering on G). The walks should mirror the `latest_K_for_addr` format with explicit symbol-by-symbol classification.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate coordination
**Why out of scope**: The framework explicitly commits to single-process substrate scope. Cross-process atomicity for the Sh4/FDD contracts requires a coordination protocol outside the framework. This is acknowledged in Open Questions [scope boundary].

### Topic 2: Mechanical body-shape derivation at shape-mate rows
**Why out of scope**: Sh5(a) explicitly downgrades per-shape body-shape uniformity from commitment to aspiration. Sharpening this to a procedural derivation recipe is recorded as an open work item that a future draft may undertake.

### Topic 3: Bypassed emissions for K ∈ T_cat at K.λ
**Why out of scope**: The framework requires all K ∈ T_cat class-(iii) emissions to route through Emit_K (the *Emit_K routing commitment*). Layers wanting to host bypassed emissions for migration scenarios are explicitly outside scope.

VERDICT: REVISE
