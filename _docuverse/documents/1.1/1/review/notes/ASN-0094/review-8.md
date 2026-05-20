# Review of ASN-0094

## REVISE

### Issue 1: ShapeWellFormedness commentary contains misleading qualifier

**ASN-0094, Definition — ShapeWellFormedness, *Behavior at `c_F = 0|1`***: "Neither `c_F = 0` nor (typically) `t_F = -` fires at a `c_F = 0|1` row, so both implications on the F-side are vacuously satisfied"

**Problem**: The "(typically)" suggests `t_F = -` might sometimes fire at a `c_F = 0|1` row. But the immediately preceding well-formedness rule `t_F = - ⟹ c_F = 0` excludes `(c_F = 0|1, t_F = -)` outright (since `0|1 ≠ 0`). Mathematically, `t_F = -` *never* fires at `c_F = 0|1` — the registry rejects it. The hedging undermines the very rule being commented on.

**Required**: Remove "(typically)" or restate as "`t_F = -` is excluded at `c_F = 0|1` rows by the well-formedness implication `t_F = - ⟹ c_F = 0`."

### Issue 2: T_cat "finite distinguished set" terminology is incorrect

**ASN-0094, Definition — TypedRelationCatalog**: "Fix a finite distinguished set `T_cat ⊆ T_admissible` that is *closed under coverage-equivalence*"

**Problem**: T_cat closed under `~` cannot be finite if it contains any non-empty equivalence class, because `~`-classes are infinite (many endsets share the same coverage by L5). The clarifying sentence ("Equivalently, `T_cat` is a union of `~`-equivalence classes; concretely it is specified by listing one representative per class") concedes this but lets the misnomer stand.

**Required**: Replace "finite distinguished set" with "set finite up to `~`" or "set whose quotient `T_cat / ~` is finite", or state directly that T_cat is the union of finitely many `~`-classes (each infinite as endset sets, finite in count of classes).

### Issue 3: Sh-conf's effective weakest-precondition is not composed with ASN-0086's wp

**ASN-0094, Sh-conf — ShapeConformanceAxiom**: "The framework restricts ASN-0086's `Emit_K` (the relational-layer operation) by adding two preconditions"

**Problem**: ASN-0086 defines `wp(Emit_K(...), (a, F, G) ∈ A_K^{Σ'})` explicitly. Sh-conf adds `K ∈ T_cat ∧ conf_K^Σ(F, G)` as additional preconditions, but the framework never states the composed wp. Readers must derive that the effective wp is the conjunction of ASN-0086's wp with Sh-conf's predicates, with `K ∈ T_admissible` absorbing into `K ∈ T_cat` via `T_cat ⊆ T_admissible`. This composition is straightforward but should be exhibited explicitly so the framework's contract with ASN-0086 is unambiguous.

**Required**: State the effective wp for Emit_K under Sh-conf as a single formula, derived from ASN-0086's wp + Sh-conf's added conjuncts. Show the `⊥` rejection corresponds to wp failure on either source.

### Issue 4: home_R introduced in worked example without allocation

**ASN-0094, Worked Example: K = comment, Emission 3**: "Emission 3 (resolution). `ρ_1 := Emit_{K_res}(Σ_2, home_R, F_ρ, G_ρ)`"

**Problem**: The worked example's Σ_0 setup says "with two pre-allocated documents `d_1, d_2 ∈ A_doc^{Σ_0}` and a home document `home_K ∈ dom(Σ_0.M)`". home_R is introduced for the first time at Emission 3, but its allocation step is never shown. The Sh-conf check at Σ_2 implicitly requires `home_R ∈ dom(Σ_2.M)`, which is not established.

**Required**: Add `home_R ∈ dom(Σ_0.M)` to the Σ_0 setup, or insert a K.σ step registering home_R before Emission 3.

### Issue 5: "Sh5's mechanical-derivability claim degrades" overstates Sh5

**ASN-0094, Coverage instantiation, *Without SingleHomeCoverageDiscipline***: "Without SingleHomeCoverageDiscipline: the Coverage instantiation must layer-supply an `emission_order` total order on `S_d`. Sh5's mechanical-derivability claim degrades at this point"

**Problem**: Sh5 is explicitly labeled META and the framework states "Sh5 is a META commitment about how this framework constructs and maintains its canonical shape catalog, not a mechanical-derivation theorem". Sh5 doesn't claim mechanical derivability for any shape — that's precisely what the META observation (a) disclaims. Saying Sh5's claim "degrades" misrepresents Sh5's status.

**Required**: Reword to reflect Sh5's actual scope. E.g., "Without SingleHomeCoverageDiscipline, the Coverage instantiation's `latest_K_for_addr` is no longer determined by shape + substrate alone; the layer must supply a per-K `emission_order` accessor, which the catalog row records as a per-K registration obligation rather than a derived template."

### Issue 6: AllocatedAddressAntichain Case 3 — implicit use of `n_3 < #x`

**ASN-0094, Lemma — AllocatedAddressAntichain, Case 3, Step 3.2**: "the E-field of `x` occupies positions `n_3 + 1 .. #x`"

**Problem**: For this range to be non-empty (E-field has at least one position), the proof needs `n_3 + 1 ≤ #x`, equivalently `n_3 < #x`. This is justified by L1b (`#E(x) ≥ 2`) and T4(iv) (`x_{#x} ≠ 0`), but the proof never names either. A reader checking the boundary case `n_3 = #x` would have to derive this gap independently.

**Required**: Add a one-line justification before Step 3.2 establishing `n_3 < #x` from L1b/`#E ≥ 2` (link side) or the content-side scaffolding's `#E ≥ 2` (content side), with T4(iv) excluding `n_3 = #x`.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link shape extensions
**Why out of scope**: The framework explicitly restricts to the arity-3 standard-triple slice (Scope and Substrate Scaffolding, *Arity scope*). Extending to L3's higher-arity links would require per-extra-slot shape components and is genuinely new design territory.

### Topic 2: Dynamic T_cat registration after Σ_init
**Why out of scope**: The framework asserts T_cat is fixed at Σ_init for the inductive proofs to fire. Dynamic registration (adding new K's at later states) is a separable design problem and not an error in the present formulation.

### Topic 3: Composite shapes (relations constrained by other relations' content)
**Why out of scope**: Listed in Open Questions; would require a new restriction axis beyond the five-tuple shape, structurally new territory.

### Topic 4: Cross-process shape registry consistency
**Why out of scope**: Listed in Open Questions. The single-process lifetime-constancy commitment is sufficient for the framework's stated guarantees; distributed extensions are future work.

### Topic 5: Mechanical procedure for deriving Sh5 templates from arbitrary shapes
**Why out of scope**: Sh5(a) explicitly disclaims this as a META observation. The hand-curated catalog discipline (Sh5(b)) is the framework's actual commitment.

VERDICT: REVISE
