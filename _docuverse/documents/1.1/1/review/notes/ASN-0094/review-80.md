# Review of ASN-0094

## REVISE

### Issue 1: Sh-conf's "iff" success condition contradicts per-K discipline gating

**ASN-0094, The Conformance Axiom**: "Combined success condition: `Emit_K(Σ, d, F, G)` succeeds iff `d ∈ dom(Σ.M)` *and* `K ∈ T_cat` *and* `conf_K^Σ(F, G)`. On any failure, `Emit_K` returns `⊥` and leaves state unchanged... Per-K discipline contracts (Sh4, FDD, SHCD) also return `⊥` on suppression."

**Problem**: The axiom asserts an "iff" success condition, but per-K disciplines (Sh4 clause (ii), FDD clause (ii), SHCD clause (i)) can suppress emissions when Sh-conf's three conjuncts all hold. The "iff" is therefore false: success requires Sh-conf admission *and* per-K non-suppression. EffectiveWpSimplification's `wp_eff` correctly captures this with `... ∧ Π_K`, but Sh-conf's axiomatic statement isn't reconciled.

**Required**: Either restate Sh-conf as "necessary condition" or "Sh-conf admits iff", with the combined success condition deferred to the framework's gate stack (and explicitly named as the per-K-discipline-aware effective condition).

### Issue 2: "FDD subsumes Sh4" claim not formalized

**ASN-0094, DirectedPair / FunctionalDependencyDiscipline**: "FDD subsumes Sh4 at FDD-registered K. At FDD-registered K the layer runs only the FDD clauses (i)–(iii), with Sh4's clauses dormant. The Sh4 conclusion still holds on `A_K^Σ` by direct argument on the relation..."

**Problem**: Sh4's preservation theorem is *contract-discharged*: its inductive Case B explicitly invokes the *Sh4 idempotency contract* clause (iii). At FDD-registered K the Sh4 contract is dormant, so Sh4's preservation theorem doesn't directly apply. The "direct argument on the relation" is correct (FDD's from-slot uniqueness + R1 yields slot-pair distinctness) but sits as an informal paragraph rather than a named lemma. Downstream consumers that cite Sh4 at FDD-registered K have no formal hook.

**Required**: A named corollary "Sh4 holds at FDD-registered K via FDD" with the explicit derivation (FDD property → from₁ distinct on distinct active tuples → slot-pair distinct), so that consumers can cite the corollary rather than the prose aside.

### Issue 3: Missing concrete walkthrough for Provenance shape

**ASN-0094, Provenance — `(1, 0|1, A, A, ⊤)`**: The section defines the template family using the partial accessor `to₁⁻` and explicitly filters `to₁⁻(τ) ≠ ⊥` in `to_addrs_K`.

**Problem**: Provenance is the only shape with `c_G = 0|1` (partial to-slot) and the only one with unrestricted target domain `A` on both sides. The section defines six templates with `⊥`-handling but provides no worked example exhibiting (i) an emission with `|slot_addrs(G)| = 0` (agent-attribution-only), (ii) an emission with `|slot_addrs(G)| = 1`, (iii) `to_K(b)` correctly excluding `to₁⁻(τ) = ⊥` tuples, (iv) `pair_K(a, b)` returning false for empty-G tuples. The reader cannot ground the framework's behavior at this shape's distinguishing features against a concrete scenario.

**Required**: A worked example exhibiting both `|slot_addrs(G)|` regimes, with template evaluation at the final state distinguishing the two cases.

### Issue 4: Missing concrete walkthrough for SHCD single-home rejection

**ASN-0094, SingleHomeCoverageDiscipline**: The section defines the *single-home commitment* (gate 1) with literal-equality test `d = d_K`, distinct from FDD's Observe-based gate 3.

**Problem**: SHCD is the only discipline that fires at gate 1, and the only one with a non-Observe protocol. No worked example exhibits (i) an emission at `d = d_K` admitted, (ii) an emission at `d ≠ d_K` rejected with `⊥` at gate 1 before gates 2–5 fire, (iii) `latest_K_for_addr(d)` exercising `emission_order` over a homed-set with multiple entries. The Comment worked example uses NonIdempotentDirectedPair but explicitly does not opt into SHCD.

**Required**: A walkthrough exhibiting an SHCD-registered K with two emissions at `d_K` (showing chain-index ordering) and at least one rejected emission at `d ≠ d_K`.

### Issue 5: Reviser drift in Sh4's "Universal scope" paragraph

**ASN-0094, Sh4 — IdempotencyDiscipline**: "The two bound variables `τ` and `τ'` range independently over `A_K^Σ`, including the diagonal `τ = τ'`. On the diagonal the conclusion `addr(τ) = addr(τ')` reads `addr(τ) = addr(τ)`, satisfied by reflexivity of equality, so the diagonal contributes no constraint. The substantive content is off-diagonal..."

**Problem**: The paragraph imagines the diagonal case the universal-quantifier reading already trivially satisfies, then dispatches to the off-diagonal "substantive content". A standard universal quantifier reader reads this dispatch implicitly. The paragraph reads as a relocated prior finding rather than as content the proof requires.

**Required**: Delete the paragraph or condense its content into a one-line parenthetical at the lemma statement.

### Issue 6: Reviser drift in BundledDirectedPair's "Coverage class disjointness from R"

**ASN-0094, BundledDirectedPair**: "The BundledDirectedPair shape tuple `(1, *, A_doc, A_doc, ⊤)` differs from Retraction's `(*, 1, A, A_rel, ⊤)` on four components... Per-class constancy of `shape(·)` gives the contrapositive: `shape(K) ≠ shape(K') ⟹ K ≁ K'`. Hence every K registered at the BundledDirectedPair shape satisfies `K ≁ R`. In EffectiveWpSimplification's Step 2... the first disjunct's arm holds directly..."

**Problem**: The one-line argument (different shape tuples → different ~-classes → K ≁ R) is elaborated into a multi-sentence paragraph that re-walks EffectiveWpSimplification's Step 2 dispatch. The same `K ≁ R via shape-tuple inequality` argument applies to every non-Retraction catalog row but is exhibited only here, suggesting relocation rather than substantive content.

**Required**: Either tighten to one sentence, or move the argument to a general note ("at every non-R catalog row, K ≁ R by shape-tuple inequality + per-class constancy") at the catalog or Sh-conf section.

### Issue 7: Missing concrete walkthroughs for Tuple-Classifier and Resolution shapes

**ASN-0094, Tuple-Classifier section**: "Structurally identical to Classifier; the only difference is the target domain." No worked example.

**ASN-0094, Resolution section**: "Standalone admissibility. Resolution's base templates depend only on shape components and Sh0–Sh4; standalone registrations work identically to consumed registrations." No standalone worked example (Resolution appears only as `K_res` in Comment).

**Problem**: While both shapes share structure with neighbors, the framework's claim that "templates work identically" is unverified for these shapes. Tuple-Classifier's distinguishing G-target rejection pattern (G targeting `A_doc` instead of `A_rel`) isn't exhibited. Resolution's standalone behavior outside the `_via` consumption pattern is asserted but not shown.

**Required**: Add at least a brief walkthrough for each — Tuple-Classifier exhibiting the G-side partition rejection mirror of Classifier's, and Resolution exhibiting standalone admission and template evaluation.

### Issue 8: Sh4 contract correctness paragraph contains internal expository redundancy

**ASN-0094, Sh4 — IdempotencyDiscipline / contract clause (i.a)**: The "Contract correctness" and "AllocatedAddressAntichain citation" sub-paragraphs argue first that the contract is correct *regardless of clause (d)*, then add a tightening result *under clause (d)*. The second result is then re-cited by FDD's contract paragraph as "the same AllocatedAddressAntichain argument used in Sh4's contract".

**Problem**: The expository two-tier structure (correct without clause (d), tighter under clause (d)) is presented as load-bearing, but the framework's argument needs only the post-filter exact-equality correctness — the tightening is an optimization observation that doesn't affect any preservation theorem. The cross-reference from FDD adds another layer of forwarding. This reads as accumulated meta-prose around the contract's well-foundedness.

**Required**: Drop the tightening sub-paragraph or move it to an aside; keep only the correctness statement (post-filter exact-equality decides) that the framework's arguments actually need.

## OUT_OF_SCOPE

### Topic 1: Multi-process atomicity for Sh4/FDD contracts

**Why out of scope**: The Open Questions section explicitly tags this as a *scope boundary* — porting to multi-process substrates with racing emitters at coverage-equivalent K's would require coordination protocols outside the framework. The framework's commitment to single-process substrates is honest and explicit.

### Topic 2: Non-empty initial link store baseline relaxation

**Why out of scope**: Open Questions flags this as a *scope boundary*. Extending Sh4/FDD/SHCD's preservation theorems to non-empty initial L_K would require per-K baseline verification at registration — a separate framework extension, not a defect in this ASN.

### Topic 3: A_M symbol for document-container targeting

**Why out of scope**: Open Questions flags this as a *scope boundary*. The framework restricts target domains to `A_doc`, `A_rel`, `A` per the substrate's convention; metalink-style container targeting belongs to a future shape catalog extension.

VERDICT: REVISE
