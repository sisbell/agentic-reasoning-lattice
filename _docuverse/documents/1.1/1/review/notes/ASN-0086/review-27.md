# Review of ASN-0086

## REVISE

### Issue 1: R7 is half-stipulation, not a lemma
**ASN-0086, R7 — NullifyIsEmit, Step 3**: "*Stipulated half — adopted, not derived:* every relational-layer-initiated class-(iii) step is an Emit_K call... The stipulation is *definitional*... is not extractable from L12, L12a, or the Frame conditions."
**Problem**: A claim labeled `LEMMA` should be derivable from premises. R7's conclusion ("relational-layer state change reduces to Emit_K") rests on a definitional commitment of which substrate-primitive deposits the relational layer commits to. This is a definition dressed as a theorem. The honest framing in Step 3 contradicts the LEMMA label in the property table.
**Required**: Reclassify R7 as `DEF` or `HYP+THM` (a definition that becomes a theorem under the named stipulation). Alternatively, split R7 into R7a (proven: no Σ.L-affecting transition exists outside class (iii)) and R7b (stipulated: every class-(iii) step is Emit_K). The current single-lemma framing obscures the proven/stipulated boundary.

### Issue 2: Frame conditions are stipulated but read as derived
**ASN-0086, Frame conditions on the primitive transitions**: "These commitments are at the substrate-model interface and constrain only the visible values..."
**Problem**: Classes (i), (ii), (iii) are *defined* by their frame conditions, not characterized by them. But downstream uses (e.g., R6c-Corollary Step 4, R0 Step 4's "by class-(iii) Frame, Σ'.C = Σ.C") read as if the frame conditions follow from ASN-0034/0036/0043. The ASN tries to derive Σ'.C = Σ.C for arrangement modifications from S9 and the Σ.L=Σ.L case from L12+L12a, but for the class-(iii) emission itself, the frame is a *new commitment* of ASN-0086.
**Required**: Add a clear statement at the Frame conditions section that classes (i)/(ii)/(iii) are *definitions of the abstract substrate model* introduced here, not consequences of the underlying ASNs. The substrate model's adequacy to ASN-0034/0036/0043 is a separate claim that should be flagged.

### Issue 3: R0a's discipline-conditionality should be in its claim statement
**ASN-0086, R0a — FlatLinkDomain**: The `*[Setup-free, discipline-conditional]*` tag flags the qualifier, but the antichain conclusion `(A a, a' ∈ dom(Σ.L) :: a ≼ a' ⟹ a = a')` reads as unconditional.
**Problem**: R0a's claim text presents the antichain as a property of "every state Σ reachable from an initial Σ_0 with dom(Σ_0.L) = ∅". But the reachability is *via discipline-respecting transitions*, not arbitrary `→` transitions. A reader skimming R0a may miss that the substrate primitive in isolation falsifies it.
**Required**: Restate R0a's universal as: `(A Σ : reachable via discipline-respecting → transitions :: (A a, a' ∈ dom(Σ.L) :: a ≼ a' ⟹ a = a'))`. Make the discipline-respecting qualifier part of the quantifier range, not a separate hypothesis stated paragraphs away.

### Issue 4: Worked Sketch Step 3 does not verify Nullify's preconditions
**ASN-0086, Worked Sketch Step 3 (concrete)**: "`Σ_2 → Σ_3` via `Nullify(Σ_2, d', a₂) = Emit_R(Σ_2, d', ∅, {(a₂, δ(1, 8))})`."
**Problem**: Nullify has four preconditions (P0–P3). Step 3 introduces a cross-document retraction but jumps straight to the emission without checking the preconditions. In particular, P3 (no strict prefix-extension of a₂ in dom(Σ_2.L)) must be verified — and the verification of *why* it holds (R0a's antichain at Σ_2 under the discipline) should be made explicit. The verification of P0 (`d' ∈ dom(Σ_2.M)`) is also skipped.
**Required**: Add precondition-check bullets to Step 3 parallel to the L-invariant bullets at Steps 1 and 2. Each P0–P3 should have a one-line discharge with its substrate witness.

### Issue 5: R6b is asserted but not concretely exercised
**ASN-0086, R6b — SingleDepthRetraction**: Justification is structural (existential quantifies over L_R, not A_R), but the worked sketch never tests it directly.
**Problem**: R6b's substantive consequence is "nullifying a retraction tuple does *not* restore the original assertion." This is the property a skeptical reader most needs to see concretely. The Worked Sketch does Step 2 (restoration-by-re-emission) but not the contrasting case (attempted-restoration-by-retracting-the-retraction).
**Required**: Add a Step 6 to the Worked Sketch: `Nullify(Σ_5, d_retr, b₁)` (retract the retraction of a₁). Compute that nullified(Σ_6) still contains a₁ because the original (b₁, ∅, {(a₁, δ(1, 8))}) ∈ L_R^{Σ_6} (by R3, audit preservation), and the witness check for a₁ ∈ nullified(Σ_6) does not consult b₁'s active-subset status.

### Issue 6: R5's META label conflicts with its content
**ASN-0086, R5 — TupleSelfTargeting**: Labeled META in the properties table, but presented as a permission claim with explicit construction.
**Problem**: META in the existing vocabulary (e.g., L4 in ASN-0043) is a meta-statement *about* the model, not a claim *within* it. R5 has a constructive witness (the unit-depth self-targeting span) and an invariant-preservation argument. This is closer to a LEMMA or DEF — specifically, an existence/permission lemma.
**Required**: Reclassify R5 as LEMMA (with content: "the construction is admissible") or split into a DEF (the canonical self-targeting span) and a LEMMA (R0 extended to span-targets in A_rel preserves invariants). The "Stage 2" exhaustive enumeration of orthogonal invariants is defensive and could be replaced by a single sentence: "All L-invariants are preserved by R0 Step 4 since none restricts span-target subspace."

### Issue 7: `↦` and `⊑̂` notation introduced just before use
**ASN-0086, R6c-Corollary**: "Let `↦` denote the union of dom-extending `→` with ASN-0036's arrangement-modifying transitions..."
**Problem**: The broader transition relation is introduced inside R6c-Corollary's statement, after the entire R0–R6c chain has been proved using the narrower `→`. A reader following the proofs sequentially encounters the corollary's relation as a surprise.
**Required**: Introduce `↦` and `⊑̂` alongside `→` and `⊑` in the "State transition relation" definition at the top, with the note that R0–R6c are stated against `→` and that R6c-Corollary lifts the conclusion to `⊑̂`. This makes the dual-transition-vocabulary explicit from the start.

### Issue 8: Setup hypothesis has no maintenance protocol
**ASN-0086, Setup hypothesis**: "We additionally assume globally s_C-resident content: `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`."
**Problem**: The hypothesis must hold *for every state* in the system. But ASN-0086 doesn't restrict the content-emission protocol (class (ii) in `→`). So the hypothesis is a hope, not a derived invariant. R0 requires the hypothesis at *every* invocation; without a maintenance argument, R0 is conditional on an external commitment.
**Required**: Either (a) state explicitly that the Setup hypothesis is an external constraint on the content-emission protocol, parallel to the sibling-frontier discipline being an external constraint on the link-emission protocol; or (b) add a Frame-condition variant for class (ii) requiring `subspace_I(c) = s_C`. The current treatment leaves the Setup hypothesis structurally floating.

### Issue 9: Properties table is internally inconsistent
**ASN-0086, Properties Introduced table**: R7 is labeled `LEMMA`, but R7's body labels half the proof as stipulated. R5 is labeled `META`, but R5's body presents it as a permission claim with constructive proof. R6 is `LEMMA`, but its body says "R6 itself, stated below as `A_K^Σ`'s well-definedness, is a definitional check."
**Problem**: The labels in the table do not match the labels and proof structures in the body. A reader using the table as a summary gets a misleading map of which claims are derivable theorems versus which are definitions or stipulations.
**Required**: Reconcile the table labels with the proof structures. Specifically: R6 → DEF (or LEMMA with note that it's a definitional check); R7 → DEF + LEMMA (or relabel as in Issue 1); R5 → LEMMA (or rename META category to PERMISSION).

### Issue 10: R6c's user-facing reading does not match its formal scope
**ASN-0086, R6c — RestorationByReemission**: "Once retracted, a tuple stays out of every future active subset reachable through dom-extending transitions"
**Problem**: The user-facing reading of R6c is "every future active subset" — without qualification. The formal claim restricts to `⊑`-reachability (dom-extending). The user reading is recovered only by R6c-Corollary, which is introduced separately. A reader who absorbs R6c as the headline claim may miss that R6c alone does not establish the user-facing reading.
**Required**: Either (a) state R6c against `⊑̂` directly (with the proof composing R6c-Corollary's argument into the main proof), or (b) rephrase R6c's headline to "every future state reachable via dom-extending transitions" so that the formal scope is visible.

## OUT_OF_SCOPE

### Topic 1: Multi-arity active subsets
**Why out of scope**: The note explicitly scopes A_K to standard-triple links (`|Σ.L(a)| = 3`). Generalizing to A_K^{(n)} for higher arities requires defining slot semantics for n > 3 and is named in Open Questions.

### Topic 2: L14's native scoped form
**Why out of scope**: Lifting the Setup hypothesis to admit s_L-resident content is a substantive reformulation of R0/R4/R5 that is correctly deferred to a future revision.

### Topic 3: Substrate-level elevation of the sibling-frontier discipline
**Why out of scope**: Tightening the substrate emission primitive to forbid prefix-extension emissions would discharge R0a's conditionality but is a design choice about the substrate, not an error in ASN-0086.

### Topic 4: Atomicity model for concurrent Emit and Observe
**Why out of scope**: The note treats `→` as a sequential transition relation; concurrency semantics is a separate concern.

### Topic 5: Type catalog evolution and collision discipline
**Why out of scope**: The Open Question on dynamic type-catalog extension across uncoordinated layers is a substantive policy question for a higher layer.

VERDICT: REVISE
