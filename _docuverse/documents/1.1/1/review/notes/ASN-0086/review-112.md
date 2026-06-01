# Review of ASN-0086

## REVISE

### Issue 1: R0 cross-home freshness asserts a false intermediate — distinct documents are *not* generally prefix-incomparable

**ASN-0086, R0 proof, subsequent-emission branch, *Cross-home freshness***: "the document-level prefixes `d, d'` are distinct T4-valid document tumblers (S7d, GlobalUniqueness, ASN-0034), hence prefix-incomparable; since `d ≼ a` and `d' ≼ ℓ'`, T10 (PartitionIndependence, ASN-0034) yields `a ≠ ℓ'`."

**Problem**: GlobalUniqueness gives `d ≠ d'`, not prefix-incomparability. Two distinct document-level tumblers can stand in a prefix relation: `d = 1.0.1.0.1` and `d' = 1.0.1.0.1.5` both have `zeros = 2`, are T4-valid, and satisfy `d ≼ d'` (a version-extension of a document — exactly the "accidental extension of the document number" the vocabulary describes, and an admissible `dom(M)` pair under K.σ). T10's precondition `d ⋠ d' ∧ d' ⋠ d` therefore does not hold, so the cited T10 step is unlicensed. The *conclusion* `a ≠ ℓ'` is still true, but via the field-separator zero at position `#d + 1` (where `a` carries the `0` of `b_L(d)` while `ℓ'` carries a nonzero document-extension component), not via T10. Notably, R0a Case 1 derives the cross-home result *correctly* by the zeros/home-equality argument — R0 takes a shortcut that contradicts the note's own careful treatment.

**Required**: Replace the "hence prefix-incomparable + T10" step with either (a) a direct citation of ASN-0093's CrossDocumentDisjointness lemma (which is conformance-free — it establishes anchor incomparability and `a ≠ b` for addresses extending `b_·(d₁)`, `b_·(d₂)`, exactly R0's situation, and preserves R0's stated goal of covering non-`→*`-reachable states), or (b) the explicit field-separator argument used in R0a Case 1.

### Issue 2: Same scope-justification prose restated three times with a self-referential forward pointer

**ASN-0086, Definition — Categorical reachability / Definition — Emit_K / WP Case 1**:
- Categorical reachability: "**The bare operations … range over the full (`↝*`-reachable) state space** … (the consequence of this scope choice — dischargeability of conformance conjuncts — is stated once at the Definition — Emit_K)."
- Emit_K: "ranging over it rather than the conforming sub-space is what makes conformance conjuncts such as P2c genuinely dischargeable rather than vacuous standing invariants."
- WP Case 1 *Domain of quantification*: re-explains that the bare operation can run from a non-conforming pre-state so "P2c is therefore a genuine, dischargeable conjunct."

**Problem**: This is the flagged anti-bloat pattern — the identical point ("operations range over the full state space, which is what makes conformance conjuncts dischargeable rather than vacuous") appears in three sections, and one instance carries an explicit forward pointer to another ("stated once at the Definition — Emit_K"), which the forward-reference-accretion guidance names directly ("multiple paragraphs in different sections defer to the same downstream location"). The reader must reconcile three near-duplicate statements to confirm they say the same thing.

**Required**: State the scope choice and its consequence once (at the Definition — Emit_K, which the others point to), and delete the restatements and the self-referential parenthetical from Categorical reachability and WP Case 1.

### Issue 3: Two full worked examples embedded inside the R7a proof body

**ASN-0086, R7a**: "*Worked example — composite create-two-fresh-documents-each-with-initial-link (length-4 decomposition)*" and "*Worked example — composite emitting two links at one existing home (subsequent-emission replay)*", both interposed between the end of the R7a proof (`∎`) and the Definition — relational layer.

**Problem**: Concrete examples are legitimate content, but their *placement* inside a lemma's proof region — in addition to the standalone four-step Worked Sketch section that already exercises first- and subsequent-emission branches — interrupts the structural argument and duplicates illustrative coverage. The second example explicitly re-derives the subsequent-emission `ℓ_prev` tracking that the Worked Sketch's Steps 1–3 already walk through.

**Required**: Move both worked examples into the Worked Sketch section (or a dedicated examples appendix) and consolidate the overlapping subsequent-emission illustration, leaving R7a's proof to carry only the case discharges.

### Issue 4: R7a leans on "substrate-conforming layer" / clause (b) frontier-emission as a definitional assumption, but the decomposition's address-reconstruction is only as strong as that assumption

**ASN-0086, R7a, discharge (4)(iii) and ConformingHomedContiguity clause (b)**: "clause (b) requires the `r` fresh keys homed at `d` to occupy exactly chain indices `J+1, …, J+r` … no index skipped."

**Problem**: The claim that the replay reconstructs *the same* addresses `a_k` that `Σ'` holds (rather than merely *some* fresh conforming addresses) rests entirely on clause (b) of the conforming-layer definition. The note states this conditionality but never exhibits that any substrate mechanism *forces* a composite `↝`-step to deposit at contiguous frontier indices — clause (b) is asserted as part of "conforming," so R7a is "conforming layers decompose as claimed" with conformance doing all the work. This is fine as a conditional lemma, but the lemma's strength (and what a downstream consumer may rely on) is materially weaker than the unqualified table entry "NoExtraClassAffectsL" suggests.

**Required**: Either (a) state R7a's conclusion as explicitly contingent on clause (b) in the summary table and at the point of use, so consumers do not read it as an unconditional substrate guarantee, or (b) show that the substrate's K-op vocabulary (not the layer's discipline) already forces frontier-contiguous deposition, discharging clause (b) rather than assuming it.

## OUT_OF_SCOPE

### Topic 1: Atomicity / consistency model for concurrent Observe vs Emit
**Why out of scope**: The Open Questions ("Must Emit be atomic with respect to concurrent Observe…", "what is the consistency model under which `A_K` transitions are observed?") concern a concurrency semantics the substrate has not yet specified. This is new territory for a future ASN, not a defect in the present single-trajectory development.

### Topic 2: Dynamic, uncoordinated introduction of new admissible types and type-address collision
**Why out of scope**: Whether two layers independently choosing colliding type ghost addresses creates a problem is a multi-layer coordination question. The present ASN correctly models types as coverage classes over ghost-permissible addresses; collision semantics belong to a layer-interaction ASN.

VERDICT: REVISE
