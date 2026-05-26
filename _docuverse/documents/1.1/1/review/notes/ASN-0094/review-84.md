# Review of ASN-0094

## REVISE

### Issue 1: Dead definitions referencing non-foundation ASN

**ASN-0094, top of Scope and Substrate Scaffolding**: "Definition — ZeroCountDepth" and "Definition — AllocatorTreeDepth"

**Problem**: Both definitions reference ASN-0093 ("child-spawn `(d, k')`...", "ASN-0093's structural chain from `d` to A's base address"). ASN-0093 is not in the foundation set listed at the head of the review (foundation is ASN-0034, ASN-0043, ASN-0086). Worse, after careful search neither `ZeroCountDepth` nor `AllocatorTreeDepth` is referenced anywhere else in ASN-0094 — they are dead text. The framework's actual chain-discipline access goes through the locally defined "Per-document link sub-allocator chains" and "Link sub-allocator chain-index function" scaffolding clauses, which avoid naming ASN-0093 directly.

**Required**: Delete both definitions, or — if a downstream consumer is intended — invoke them at a load-bearing site and route the ASN-0093 dependency through a scaffolding clause rather than a direct citation.

### Issue 2: Defensive paragraph imagines a case the framework already routes

**ASN-0094, paragraph after EffectiveWpSimplification's proof**: "*Coverage-class disjointness from R at every non-R catalog row.* ... For a row whose shape tuple is componentwise equal to R's, the registry's hand-curation requires its representative to register `K_rep ~ R`; otherwise the row is a divergent coverage class at R's shape and is rejected by the catalog author at registration. Either way, Step 2 lands in Case A (`K ≁ R`) and the wp simplification holds uniformly at every non-R catalog row."

**Problem**: This is exactly the *forward-reference accretion* pattern the review-mode classifier flags ("a paragraph imagines a case the claim's carrier or precondition already excludes"). EffectiveWpSimplification's Step 2 routes on `K ≁ R` vs `K ~ R`, not on shape mismatch. A "divergent coverage class at R's shape" still routes via `K ≁ R`, so the framework handles it whether or not the hand-curation gate fires. The "hand-curation" claim is not framework-enforced (per-class constancy gives `K ~ K' ⟹ shape(K) = shape(K')`, not the converse), and the paragraph admits no value beyond what the simpler "shape ≠ R's shape ⟹ K ≁ R by contrapositive" sentence already provides.

**Required**: Delete the "For a row whose shape tuple is componentwise equal to R's..." sub-clause and the "Either way" coda. The shape-difference contrapositive alone discharges Step 2's K ≁ R case.

### Issue 3: K ∈ T_cat check is implicit in gate ordering

**ASN-0094, "Gate Ordering" enumeration in the Conformance Axiom section**

**Problem**: The five-gate enumeration (SHCD, Sh-conf canonical-form, Per-K Observe-then-Emit, Sh-conf cardinality/target, K.λ) does not name where `K ∈ T_cat` is checked, despite this being a load-bearing Sh-conf admission conjunct. Gates 2, 3, 4 all consult `shape(K)` which is only defined for `K ∈ T_cat`. Pattern 4 in the Sh-conf Rejection Patterns section says "`K ∉ T_cat` fails Sh-conf's first conjunct," but the gate ordering numbers Sh-conf canonical-form as gate 2 with no explicit `K ∈ T_cat` gate. Symmetric remark for `d ∈ dom(Σ.M)` — the gate ordering checks this implicitly at K.λ (gate 5) rather than as a named Sh-conf gate. Readers tracing why a particular `⊥` returned cannot identify the rejecting gate when the failure is `K ∉ T_cat`.

**Required**: Either add an explicit gate 0 ("Catalog membership: test `K ∈ T_cat`; on failure return `⊥` before any other gate fires") or fold the check into gate 2 with text "test `K ∈ T_cat`, then `F` and `G` canonical-slot form." Same for `d ∈ dom(Σ.M)`.

### Issue 4: FDD Case B carries a redundant qualifier

**ASN-0094, FDD preservation theorem, Case B**: "*Step (Case B: `A_K^{Σ'} = A_K^Σ ∪ {τ_new}`, a K.λ-step at type K with no concurrent nullification of any τ ∈ A_K^Σ).*"

**Problem**: FDD's shape `(1, 1, A_doc, A_doc, ⊤)` differs componentwise from R's `(*, 1, A, A_rel, ⊤)`, so per-class constancy forces `K ≁ R` for every FDD-registered K. A K.λ-step at type K (with `K ≁ R`) cannot extend `L_R^Σ` and therefore cannot expand `nullified(Σ)`. The "with no concurrent nullification" qualifier is structurally impossible to violate at any FDD-registered K — it is dead verbiage copied from Sh4's Case B, where the qualifier is load-bearing for the K ~ R sub-case routed to Case D. FDD has no Case D (excluded by shape mismatch, as the theorem's preamble already notes).

**Required**: Drop the qualifier. Case B's description should read "a K.λ-step at type K" simpliciter.

### Issue 5: Sh-conf admission "iff" framing conflicts with gate ordering

**ASN-0094, Sh-conf section**: "*Sh-conf admission condition (necessary, not sufficient):* `Emit_K(Σ, d, F, G)` is *Sh-conf-admissible* iff `d ∈ dom(Σ.M)` *and* `K ∈ T_cat` *and* `conf_K^Σ(F, G)`."

**Problem**: The "iff" claims complete characterization, but the gate ordering shows SHCD (gate 1) and per-K-discipline (gate 3) can reject before any Sh-conf clause fires. So a call rejected by gate 1 was never "checked for Sh-conf admission" — yet the iff form suggests Sh-conf is the complete success condition. The text tries to patch this with "(necessary, not sufficient)" but the iff biconditional contradicts the patch. Either Sh-conf admission is the full success criterion (it isn't — Π_K must also hold), or it's a necessary sub-condition (then drop the iff). The wp_eff form below resolves this correctly by listing all conjuncts; the Sh-conf statement should match.

**Required**: Restate as a one-direction implication: "If Sh-conf admits, then `d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)`. For overall success, additionally `Π_K(d, F, G, Σ)` must hold (per Gate Ordering)." Keep the iff form only within the substrate's actual definition of Sh-conf admissibility, not for the framework's success condition.

### Issue 6: "Three independently-checked structural gates" terminology drifts from the five-gate ordering

**ASN-0094, Conformance Axiom section, paragraph beginning "*Structural gates.*"** and **Sh-conf Rejection Patterns paragraph**: "Three independent gates, each rejecting independently. When the worked examples below refer to 'Sh-conf's three independently-checked structural gates'..."

**Problem**: The framework names "three structural gates" for canonical-form, cardinality, target-domain — but the Gate Ordering paragraph immediately below splits these into gates 2 and 4 (with cardinality and target-domain combined as gate 4). Worked examples then cite "three gates" while the gate ordering enumerates five. The numbering inconsistency creates confusion when a walkthrough says "Sh-conf clauses (a)/(b)/(c)/(d) all pass" — does this mean gate 2 passed, or gates 2 and 4?

**Required**: Either renumber the structural gates to match the five-gate ordering (canonical-form = gate 2, cardinality = gate 4a, target-domain = gate 4b), or commit to "three Sh-conf gates" and reshape the gate ordering to surface them individually. The current "three-vs-five" parallel structure is not consistent.

### Issue 7: Lemma — RetractionSelfFreshness preconditions overconstrain

**ASN-0094, RetractionSelfFreshness, Precondition 3**: "Every framework gate at an `Emit_R(Σ, d, F, G)` call site admits the call — Sh-conf clauses (a)–(d) all pass and the *Sh4 idempotency contract* clause (iii) fires..."

**Problem**: The Lemma is invoked at EffectiveWpSimplification Step 4(b), but at that point the corollary's hypothesis is "the framework's full gate stack admits the call (gates 1–4)," which is weaker than "the Sh4 contract clause (iii) explicitly fires." A call at K ~ R can be admitted by Sh4 clause (iii) when `C(F_{τ_new}, G_{τ_new}, Σ) = ∅` — this is automatic at clause (iii) — but the Lemma's precondition phrasing makes clause (iii) "firing" sound like an additional condition rather than a consequence of `C = ∅`. The cyclic-looking dependency is benign but the wording obscures it.

**Required**: Restate Precondition 3 as: "Gates 1–4 all admit the call; consequently, if Sh4 is registered at K (true for K ~ R since shape(R).idem = ⊤), Sh4's clause (i) check `C(F, G, Σ) = ∅` already passed at gate 3." This makes the inheritance explicit rather than appearing to require an additional layer-level commitment.

## OUT_OF_SCOPE

### Topic 1: Mid-lifetime catalog extension
The framework fixes `T_cat^rep` before `Σ_init` and asserts lifetime constancy. Real systems may want to add new relations as the substrate evolves. The framework's preservation theorems would need re-examination under a mutable catalog (the empty-baseline assumption fails for newly registered K). This is noted in Open Questions but is a substantial future ASN.

### Topic 2: Multi-process substrate races on Sh4/FDD candidate-set computation
The *Scope: single-process substrate* clause restricts the contracts. A distributed substrate would need a coordination protocol at the `~`-equivalence class. Treated correctly as a scope boundary; the coordination protocol design belongs in a future ASN.

### Topic 3: Document-container address targeting (`A_M` symbol)
Open question lists this as a scope boundary. Adding `A_M` would expand the target-domain vocabulary and require new template families (e.g., metalinks targeting containers, not content). Future ASN territory.

### Topic 4: `(0, 0)` shapes and other uncatalogued shape-tuples
The catalog lists eight canonical shapes. The shape-tuple space `{0, 1, *, 0|1}² × {A, A_doc, A_rel, -}² × {⊤, ⊥}` is much larger. Whether to admit `(0, 0)` existence-flag shapes, or reverse-Resolution `(1, 1, A_rel, A_doc, ⊤)`, etc., is a catalog-extension question outside this ASN's scope.

VERDICT: REVISE
