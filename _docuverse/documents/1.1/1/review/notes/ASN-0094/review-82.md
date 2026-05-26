# Review of ASN-0094

## REVISE

### Issue 1: Document size — review-30's three-way split recommendation still pending
**ASN-0094, full document**: 43K words.
**Problem**: A single ASN this size cannot be reviewed as a coherent whole. Review-30 already recommended a three-way split; the reviser punted to operator (per project memory `project_asn94_apex_and_split`). The pre-protocol-docs window is the cheap time to act. Five distinct logical layers are bundled: (1) substrate scaffolding + AllocatedAddressAntichain + CoverageEqualityDecidability, (2) Sh-conf axiom + Sh0–Sh3 preservation, (3) Sh4 + per-K discipline contracts (FDD, SHCD), (4) catalog + per-shape templates, (5) extensive walkthroughs. Layers (4) and (5) alone exceed 20K words.
**Required**: Split into framework axioms / per-K disciplines / catalog walkthroughs as three ASNs. Each becomes independently review-able and the cross-dependency graph (which depends on what) becomes explicit.

### Issue 2: CoverageEqualityDecidability — polynomial-time claim is imprecise
**ASN-0094, Lemma — CoverageEqualityDecidability**: "decidable in polynomial time in the total span count `n + n'`".
**Problem**: T1 comparisons on tumblers are not constant time — T2 (IntrinsicComparison) bounds each comparison by `min(#a, #b)` component pairs. Under T0(b) (UnboundedLength), tumbler depth is unbounded, so step (2)'s sort and step (3)'s membership tests are not polynomial in `n + n'` alone. The decidability conclusion is correct; the complexity claim conflates input span count with input bit-length.
**Required**: Either restrict the complexity claim to "polynomial in the total input size (span count plus tumbler depths)" or drop the complexity assertion and keep decidability only — decidability is all `T_cat` membership actually needs.

### Issue 3: R-registration status as ambient framework requirement
**ASN-0094, Nullify Compatibility section**: "R-registration is mandatory."
**Problem**: This is stated in prose, not elevated to a framework-level axiom. Three load-bearing artifacts depend on it as Precondition 2 (Lemma — RetractionSelfFreshness, Corollary — EffectiveWpSimplification, NullifyActiveSubsetCompatibility). The framework has no enforcement mechanism — a layer can instantiate it without R-registration and the substrate would proceed with `Nullify` calls failing Sh-conf's `K ∈ T_cat` gate. Worse, ASN-0086's `nullified(Σ)` Definition reads `L_R^Σ` directly regardless of registration, so a layer that emits R-typed tuples bypassing `Emit_K` produces nullifications the framework cannot reason about.
**Required**: Either elevate "R ∈ T_cat" to a framework axiom alongside the *Emit_K routing commitment*, or explicitly scope the framework as "applies to layers that register R" and state which guarantees degrade when R is unregistered.

### Issue 4: Forward-reference and scope-flag meta-prose accretion
**ASN-0094, multiple sections**:
- Opening section's "this is flagged here because it affects every downstream consumer of `L_R^Σ` reading audit-slice multiplicity" justifies placement of a flag.
- Sh4 contract's "Multi-process consistency is flagged in Open Questions" defers to a later section.
- Open Questions' three `[scope boundary]` items contain "this item is listed here to flag the boundary, not as an unresolved internal question" — meta-prose explaining why the entries exist where they do.
- Catalog Curation Discipline noted as "stated once globally at *The Canonical Shape Catalog* above; signatures mechanical, bodies hand-curated against shape-mates" — meta-prose about document structure repeated across walkthroughs.
- "primary consumption" column in Retraction "flags this active-subset machinery as the principal consumer rather than enumerating the inherited base family a second time" — meta-prose justifying what the column omits.
**Problem**: These are essay content in structural slots. Each forces the reader to skip past meta-prose to follow the substantive claim.
**Required**: Strip the justifications-for-placement; let the structure speak for itself. If a flag belongs in the opening section, it doesn't need a sentence explaining why it's there. If Open Questions distinguishes scope-boundaries from open questions, do so by tag alone, not by repeating the distinction in each entry's prose.

### Issue 5: Catalog Curation Discipline is referenced throughout but labeled NOTE (non-load-bearing)
**ASN-0094, Properties Introduced table**: Catalog Curation Discipline is `NOTE`, not `LEMMA` or `AXIOM`.
**Problem**: Per-shape template families (catalog rows + walkthroughs) consume this discipline implicitly — readers see five-template bodies converging across shape-mate rows and could reasonably infer the framework guarantees the convergence. The Consequences (a) paragraph acknowledges the gap, but it is buried after the catalog. A consumer reading the catalog top-down meets the templates first and the disclaimer last.
**Required**: Either elevate the discipline's three conventions (per-shape uniformity, Signature derivation, Citation) to a load-bearing layer-commitment with its own preservation argument, or hoist Consequences (a)'s caveat into the catalog header so readers see "template bodies are author-curated" before the templates themselves.

## OUT_OF_SCOPE

### Topic 1: Empty initial-state baseline assumption
**Why out of scope**: Already noted as `[scope boundary]` in Open Questions; the framework explicitly scopes itself to the empty-`L_K^{Σ_init}` setting. Lifting this requires per-K baseline checks that are correctly flagged as out of framework scope.

### Topic 2: Multi-process consistency
**Why out of scope**: Sh4/FDD contracts explicitly commit to single-process substrate. Multi-process coordination is a different protocol-layer concern.

### Topic 3: `A_M` (container-level addressing) in target-domain vocabulary
**Why out of scope**: Correctly flagged as a future-extension scope boundary; udanax-green doesn't support container-level link targeting.

### Topic 4: Composite shapes (relations whose F or G is constrained by another relation's content)
**Why out of scope**: Open Question's refinement candidate; new shape axis, not an error in current framework.

VERDICT: REVISE
