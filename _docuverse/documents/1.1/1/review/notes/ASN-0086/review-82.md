# Review of ASN-0086

This is a carefully constructed note and the technical core is largely sound: R0–R7a, the wp analysis, and the worked sketch hang together, the foundation citations are all to verified ASNs (ASN-0034/0036/0040/0043/0093), and the previously-declined SFD/Σ_D material is genuinely gone. The findings below are dominated by the meta-prose accretion the `review-mode.anti-bloat` classifier flags, plus one terminology-clarity item.

## REVISE

### Issue 1: R7a's table row is a full proof restated in a one-line slot
**ASN-0086, Properties Introduced (R7a row)**: "NoExtraClassAffectsL — for any state-affecting Σ ↝ Σ'… Substrate-conformance comprises two named clauses spelled out in *Definition — substrate-conforming layer*: catalog (a)… and catalog (b)… Catalog (b) is *strictly stronger*… The proof's *Per-step substrate-invariant discharge* block enumerates per replay step type…"
**Problem**: The "Properties Introduced" table is a structural index (every other row is one statement plus a parenthetical derivation). The R7a row instead re-derives catalog (a)/(b), the strict-strengthening argument, and the per-step discharge — several hundred words duplicating the body. Essay content in a structural slot.
**Required**: Reduce to the claim + the `(= …)` derivation chain, matching the other rows. The catalog and discharge live in the body already.

### Issue 2: Definitions and table rows carry use-site inventories
**ASN-0086, multiple sites**:
- R5-Cor row: "consumed by downstream Emit_K invocations at arbitrary endset shapes without per-call invariant re-verification"
- Unit-depth retraction discipline row: "Consumed by WP Case 2 regime (i) to discharge NoCraftedSpanReachesD(Σ, d) automatically"
- LinkStoreInvarianceUnderArrangement row: "Cited by R6c-Corollary's reduction and by the Worked Sketch's Σ_2 ↦ Σ_arr invariance argument"
- Definition — substrate-conforming layer: "R7a's discharge (4)(i)/(iii) consumes ChainMembershipForOrigin directly…"
**Problem**: A definition's meaning is not advanced by enumerating its downstream consumers; this is the "definition introduction enumerates downstream consumers" pattern named in the anti-bloat checklist. It rots as the consumer set changes.
**Required**: Delete the consumer enumerations. The consuming sites already cite the definitions they use.

### Issue 3: Forward-reference deferral clustering to "WP Case 2 / below"
**ASN-0086, R6c Consequence (d)**: "The regime distinction governing exactly when a class-(iii) Emit_K step contributes to A_K versus to L_K \ A_K is unpacked at its definitional home, WP Case 2 (Weakest-Precondition Analysis, below)."
**Problem**: Multiple sections defer to the same downstream location (this, plus R5-Cor "proved next," plus the regime discussion). The "multiple paragraphs defer to the same downstream location" pattern. The Consequence (d) sentence states a conclusion (non-monotonicity) and then points elsewhere for the actual content.
**Required**: Either state the regime distinction where it is first needed, or drop the pointer and let WP Case 2 stand on its own.

### Issue 4: Duplicated rationale and duplicated worked decomposition
**ASN-0086, Properties Introduced & Worked Sketch**:
- "Labeled COMMITMENT rather than DEF because it is a layer-level convention…" appears in both the Unit-depth row and the Relational layer row, after being explained once in the "Type labels" preamble.
- The Worked Sketch "Auxiliary pre-step" re-illustrates the K.σ-then-K.λ first-emission decomposition that R7a's "Worked example 1 (CreateDocAndLink)" already gives in full.
**Problem**: "Two paragraphs say the same thing in different words." The COMMITMENT-vs-DEF justification is taxonomy that belongs once (the preamble); the auxiliary pre-step duplicates a worked example from the R7a proof.
**Required**: State the COMMITMENT/DEF criterion once in the preamble and drop the per-row repeats. Collapse the auxiliary pre-step to a one-line cross-reference to R7a's Worked Example 1 (or remove it).

### Issue 5: "Strict-strengthening of (b) over (a)" justifies the definition's structure rather than stating it
**ASN-0086, Definition — substrate-conforming layer**: "*Strict-strengthening of (b) over (a).* Catalog (b) is *strictly stronger* than catalog (a): L1c… admits *any* T10a-conforming structural chain… but catalog (b) further restricts… Concretely, the tumbler a* = [d.0.s_L.1.1]… Catalog (b) closes this gap…"
**Problem**: This is prose explaining *why the definition has two catalogs* rather than what the definition is — the "new prose explains why X is needed rather than what it says" pattern. The `a*` counterexample is substantive (it shows the gap is real), but it belongs as a remark attached to R7a's load-bearing discharge step, not embedded in the definition that the discharge consumes.
**Required**: Keep the `a*` counterexample as a single remark at R7a discharge (4)(iii) (the one site that needs it); reduce the definition to the two catalogs themselves.

### Issue 6: "extends / extending" is overloaded across three distinct relations
**ASN-0086, R0 / Definition — Extension / ASN-0043 StateExtension**: R0 concludes "(E Σ' extending Σ, a : a ∉ dom(Σ.L) :: …)" where the witness is a single K.λ step; the note also defines `Σ ⊑ Σ' ≡ Σ →* Σ'` ("Extension"); and ASN-0043's `Σ' ⊒ Σ` ("StateExtension", store-wise growth-with-agreement) is cited in R5-Cor/R0 contexts.
**Problem**: "extends/extending" denotes (i) ASN-0043's ⊒, (ii) this note's ⊑ (reflexive-transitive closure of →), and (iii) an informal one-step transition, with no signposting. A precise reader must infer which is meant at each use.
**Required**: Reserve one verb per relation — e.g., "⊑-extends" for ⊑, cite ⊒ by name, and say "one →-step" for the single-step witnesses in R0/R5-Cor — so the existential witnesses are unambiguous.

## OUT_OF_SCOPE

### Topic 1: Active subsets over higher-arity links
The note restricts `L_K`/`A_K`/Nullify to arity-3 links and explicitly defers `A_K^{(n)}` to an open question. Correctly future territory, not an error here.

### Topic 2: Concurrency / atomicity of Emit vs. Observe
The open questions already park the consistency model for concurrent `A_K` transitions. Out of scope for a substrate that defines a sequential, totally-ordered transition relation.

VERDICT: REVISE
