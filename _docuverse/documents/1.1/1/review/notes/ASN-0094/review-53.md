# Review of ASN-0094

## REVISE

### Issue 1: Sh5(b) discipline's category (i) literal wording excludes the derived slot accessors the audit table treats as category (i)

**ASN-0094, Template Catalog (Sh5), META discipline (b)**: Category (i) is defined as "the shape components (cardinality, target-domain typing, idempotency flag)" — literally the five-tuple symbols `c_F`, `c_G`, `t_F`, `t_G`, `idem`. Category (vi) enumerates exactly four base-machinery accessors: `A_K^Σ`, `addr(τ)`, `slot_addrs(·)`, `δ(1, #·)`. The audit table then assigns `from₁`, `to₁`, `to₁⁻`, `from_K`, `to_K`, etc. to category (i) with qualifier "shape-component-derived under `c_F = 1`" (or similar).

**Problem**: These slot accessors are not literally shape components — they are derived functions defined in the Slot Accessors section, with existence conditional on cardinality. The audit table extends category (i) implicitly via the "shape-component-derived" qualifier, but the discipline's text does not formally license this extension. The framework's own "Mechanical falsifiability without mechanical derivation" claim asserts that "the literal name-citation check against the six categories is a finite, decidable per-symbol classification" — but `from₁` falls in neither (i) (literally) nor (vi) (not enumerated), so the per-symbol classification is not mechanically decidable without recourse to the audit table's implicit extension. An auditor walking the discipline alone would face ambiguity at every catalog row.

**Required**: Either update category (i) wording to "the shape components and their uniquely-derived slot accessors (`from₁`, `to₁`, `from₁⁻`, `to₁⁻`, `from_K^Σ`, `to_K^Σ`)", or extend category (vi)'s base-machinery enumeration to include these derived accessors. Either fix removes the implicit extension currently embedded in the audit table.

### Issue 2: Sh4 Case D's "Step D.0" derivation of `τ_new ∈ A_R^{Σ'}` is load-bearing but its placement within Case D is unconventional

**ASN-0094, Idempotency (Sh4), Case D**: "Step D.0 — τ_new ∈ A_R^{Σ'}. The case description above presupposes that τ_new actually joins `A_R^{Σ'}`; this is *not* a definitional move and requires its own discharge..."

**Problem**: Step D.0 is a non-trivial discharge (two Lemma applications: self-nullification + cross-nullification) that establishes the case's structural precondition. It sits *inside* Case D's analysis rather than as a separate sub-lemma. This makes Case D's argument harder to audit — the reader must recognize that "A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving" is a *consequence* (proved at D.0) rather than the case's definitional setup. The text correctly calls it out ("a theorem at this point, not a stipulation"), but the integration is awkward.

**Required**: Promote Step D.0 to a named sub-lemma (e.g., "Lemma — RetractionSelfFreshness") stated before Case D and cited at Case D's case-description. This separates the structural establishment (what enters A_R^{Σ'}) from the pairwise-distinctness preservation (Sh4's body on the established A_R^{Σ'}).

### Issue 3: The "audit-slice multiplicity is not preserved" commitment in NullifyActiveSubsetCompatibility shifts ASN-0086's Nullify postcondition in a way downstream consumers may not anticipate from ASN-0086's text alone

**ASN-0094, Nullify Compatibility, Audit-slice set-semantics commitment**: "two consecutive bare-form `Nullify(Σ, d_retr, a)` calls at the same target `a` produce *only one* tuple in `L_R^Σ` — not two."

**Problem**: ASN-0086's `Nullify` contract specifies a postcondition that assumes a fresh `(Σ', _)` pair is produced. ASN-0094's framework changes the operational semantics for the duplicate case: the second call returns `⊥` and `L_R` is not extended. While the NullifyActiveSubsetCompatibility Corollary formally records that the *active-subset* content is preserved, downstream consumers relying on ASN-0086's audit-slice multiplicity (e.g., for event reconstruction) silently lose audit events. The framework calls this "deliberate" but does not record an explicit migration discipline for ASN-0086 consumers that previously assumed multiset semantics — only the recommendation to "use attributed retraction" with no concrete migration steps.

**Required**: Add a "Migration discipline for bare-Nullify multiset consumers" sub-clause to the Nullify Compatibility section, naming the operational pattern that recovers per-event audit multiplicity (e.g., "every duplicate bare-Nullify call site must be replaced with an attributed-form `Emit_R(Σ, d_retr, {(d_caller, δ(1, #d_caller))}, {(a, δ(1, #a))})` where `d_caller` records the calling context to distinguish the second event from the first"). Without this, the commitment is documented as a deliberate semantic shift but not actionable.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate concurrency

**Why out of scope**: The framework's *Sh4 idempotency contract*, *FDD functional-dependency contract*, and *single-home commitment* all presuppose single-process substrate sequencing. The Open Questions section explicitly flags this as a scope boundary, not an unresolved internal question; extending the framework to multi-process substrates would require a coordination protocol at the `~`-equivalence class scope, which is a separate research effort.

### Topic 2: Mechanical catalog extension procedure

**Why out of scope**: Sh5(b)'s minimal review checklist is procedural (manual auditor walks per-symbol classification) rather than algorithmic. The framework explicitly acknowledges this cost as part of Sh5's META status. Sharpening to a mechanical derivation procedure is recorded as future work.

VERDICT: REVISE
