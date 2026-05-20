# Review of ASN-0094

## REVISE

### Issue 1: Departure from ASN-0086's Nullify-as-sole-R-producer discipline is undocumented
**ASN-0094, "Attributed Retraction" walkthrough (Emission AR1) and Retraction catalog row**: `Emit_R(Σ_0, d_retr, F_AR1, G_AR1)` with `F_AR1 = {(d_attr1, δ(1, #d_attr1))}` — a direct `Emit_R` call with non-empty F.
**Problem**: ASN-0086's relational layer commitment states "callers may invoke `Emit_K` only at type indices `K` satisfying `K ≁ R`; every `R`-typed emission is routed through the `Nullify` alias" (Relational layer — RelationalLayer commitment). `Nullify` is the fixed alias with `F = ∅`. ASN-0094's Retraction shape `c_F = *` admits attributed retractions (`F ≠ ∅`), which the "Attributed Retraction" walkthrough exercises. The framework's "Interaction with Nullify" paragraph addresses only Nullify-shaped calls and even states "Since ASN-0086 commits the relational layer to routing every class-(iii) `R`-emission through `Emit_R` (via Nullify)..." — phrasing that suggests the framework upholds ASN-0086's discipline while the catalog and walkthrough silently relax it.
**Required**: An explicit statement of the framework's stance on ASN-0086's Nullify-as-sole-R-producer discipline. Either: (a) state that the framework supersedes ASN-0086's relational layer's restriction at R-emissions, preserving only the substrate-level unit-depth retraction discipline via `c_G = 1` + canonical-slot; or (b) restrict the Retraction shape to `c_F = 0` and remove the "Attributed Retraction" walkthrough.

### Issue 2: "Or, equivalently" baseline relaxation doesn't cover Sh4
**ASN-0094, Sh-conf section, "Initial-state baseline for preservation proofs"**: "A substrate that wants the framework's guarantees from a given starting point must verify `L_K^{Σ_init} = ∅` (or, equivalently, that every prior `L_K`-tuple satisfies `conf_K^{Σ_init}`) at that point."
**Problem**: `conf_K^Σ` is a per-tuple predicate (Sh-conf clauses (a)–(d)). Sh0–Sh3 quantify over individual tuples, so the per-tuple equivalence discharges their base cases. Sh4 quantifies over *pairs* of tuples in `A_K^Σ`. A state where every L_K-tuple satisfies `conf_K^{Σ_init}` can still contain two distinct A_K-tuples sharing a slot-pair, falsifying Sh4 at the base case. The Sh4 proof's actual base case relies on `L_K^{Σ_0} = A_K^{Σ_0} = ∅`, not on the weaker per-tuple alternative.
**Required**: Either strengthen the equivalence to add "and no two A_K-tuples in A_K^{Σ_init} share a slot-pair under Sh4" (and analogously for FDD's from-slot-uniqueness and SHCD's homed-set), or explicitly state that the equivalence covers Sh0–Sh3 only and that Sh4/FDD/SHCD require the stricter empty-baseline.

### Issue 3: Case I of RetractionTargetNotOnChain conflates first- and subsequent-emission branches
**ASN-0094, Lemma — RetractionTargetNotOnChain, Case I**: "`a_emit(Σ, d)` lies on the same chain by FreshEmissionAddress (ASN-0086) at chain index `J_d^Σ + 1` (whether first-emission or subsequent-emission branch fires, both branches deposit the next chain element)."
**Problem**: The Case I hypothesis `home(b) = d` places `b` in `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}`, forcing this set non-empty. By FreshEmissionAddress, this is exactly the predicate that *blocks* the first-emission branch. Only the subsequent-emission branch can fire under Case I's hypothesis. The "whether first-emission or subsequent-emission" phrasing is therefore imprecise — first-emission is structurally excluded in Case I.
**Required**: State that Case I's hypothesis forces subsequent-emission; remove the disjunctive phrasing. Alternatively, prove the chain-index calculation independently of which branch fires (the framework's intent), but at minimum justify why both branches deposit "the next chain element" when only one can fire.

### Issue 4: `T_cat / ~` finiteness is asserted but per-class accessibility for the framework's catalog operations is not derived
**ASN-0094, TypedRelationCatalog definition**: "Fix a distinguished set `T_cat ⊆ T_admissible` *finite up to `~`*... Concretely, `T_cat` is specified by listing one representative per class, with closure under `~` implicit."
**Problem**: Sh-conf's first conjunct is the literal membership test `K ∈ T_cat`. Because each `~`-equivalence class is infinite as a set of endsets (an endset and any coverage-equivalent endset are distinct values), a literal-equality test against `T_cat`'s representative list cannot decide membership of an arbitrary `K`. The framework needs `T_cat`-membership to be decidable on endset inputs, which requires testing `[K] ∈ T_cat / ~`, i.e., that the *coverage class* of K matches some registered representative's coverage class. The Definition asserts the quotient is finite but does not characterize the membership-decision procedure that Sh-conf's gate consumes.
**Required**: Either (a) state the membership test as `K ∈ T_cat` modulo `~` (a coverage-equality test against a finite representative list), or (b) record that `K ∈ T_cat` is a literal-equality test against an enumerated endset list and document the consequence (only the specific endset values listed at `Σ_init` are admitted; coverage-equivalent endsets at other values are rejected).

### Issue 5: The Sh5(b) discipline's "literal name-citation" rule has no formal verification mechanism in the framework
**ASN-0094, Sh5 — TemplateCatalog, (b) META discipline**: "The criterion is *literal name-citation for data symbols*: a data-symbol reference in a template body must either be one of the shape-component slots, K itself, a scaffolding clause name..."
**Problem**: The discipline is stated as a META commitment about how the catalog is constructed, but the framework provides no mechanism for verifying that a given template body satisfies it. The "Worked check at `latest_K_for_addr`" paragraph walks one template through the discipline by hand, but the catalog has eight other rows whose templates are not similarly verified. For Sh5(b) to be falsifiable per the discipline's own intent, the framework needs either (a) a verification procedure that runs over each catalog row's templates, or (b) an explicit per-template citation of which data symbols each template uses and under which category (i)–(iv).
**Required**: Either spot-check each catalog row's templates against the discipline (as done for `latest_K_for_addr`), or supply a per-template citation table. The current single worked check leaves the rest of the catalog implicitly trusted.

## OUT_OF_SCOPE

### Topic 1: Cross-process consistency under the Sh4 / FDD / single-home contracts
**Why out of scope**: The framework explicitly restricts to single-process substrates in the "Scope: single-process substrate" clause and lists multi-process coordination as an open question. A multi-process treatment would require a coordination protocol distinct from this framework's within-call-sequentiality assumption.

### Topic 2: Composite shapes (relations whose F or G is constrained by another relation's content)
**Why out of scope**: Already flagged in Open Questions. Composite-shape semantics would require either new restriction axes or a derivation that composites reduce to existing primitives, neither of which is settled.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: Sh-conf clause (d) rejects ghost addresses in slot positions by design (only `A^Σ`-allocated addresses are admitted). Whether a future shape family should admit ghost-targeting under a state-dependent conformance rule is in the Open Questions list; the current framework's slot-allocated-only stance is internally consistent.

### Topic 4: Bipartite catalog rows for shapes not yet present (e.g., `(1, 1, A_rel, A_rel, _)`, `(1, 0|1, A_doc, A_doc, ⊤)`)
**Why out of scope**: The catalog is described as enumerating rows demanded by present-day predicate templates, with extension by hand-design recorded as the Sh5(a) META observation. Adding bipartite halves not yet exercised by any template family is future catalog work, not a defect of this ASN.

VERDICT: REVISE
