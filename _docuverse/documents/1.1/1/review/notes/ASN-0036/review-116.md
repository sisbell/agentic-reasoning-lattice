# Review of ASN-0036

## REVISE

### Issue 1: S5 states both constructions twice
**ASN-0036, Sharing**: The prose paragraph ("To see this, fix any `N`. Construct state `Σ_N`... The same holds within a single document: for any `N`, construct `Σ'_N`...") gives both the cross-document and within-document constructions in full, including the S0/S2/S3 verifications and the `N+1 > N` conclusion. The subsequent *Proof* ("**Cross-document construction.** Fix `N ∈ ℕ`...") restates the identical constructions with the identical invariant checks.
**Problem**: Two passages in the same property say the same thing in different words — the carrier of the anti-bloat classifier. The reader must reconcile two near-identical accounts to confirm they match.
**Required**: Keep one. Either let the prose motivate and the Proof discharge, or fold the construction into a single statement; do not enumerate both constructions twice.

### Issue 2: S7 well-definedness paragraph justifies its dependency list instead of arguing
**ASN-0036, S7 proof, "Well-definedness"**: "Two distinct contributions establish that `a` is a well-formed T4 tumbler... *First,* by S7b... *Second,* by T10a.4... T10a.4 preserves the surrounding T4-validity stated at S7b... but does *not* itself fix the exact value `zeros = 3`. Combining the two: S7b pins the zero-count at exactly 3, T10a.4 supplies the structural well-formedness..."
**Problem**: This is defensive prose explaining *why both citations are needed* (and what each does not do), not a step in establishing well-definedness. The actual content reduces to "by S7b, `zeros(a) = 3`, and by T10a.4, `a` is T4-valid; hence T4b applies." The remainder is dependency bookkeeping that compounds across cycles.
**Required**: Replace with the one-sentence statement; drop the "does not itself fix" commentary.

### Issue 3: `subspace_I` and `subspace` introductions narrate document structure
**ASN-0036, subspace_I block**: "With S7c in hand, the projection `subspace_I(a) = E(a)₁` named in the prose above receives a standalone Formal Contract, paralleling the `subspace` block below for V-positions."
**ASN-0036, subspace block**: "This is the definitional shorthand named in the prose under S7c (`subspace_I(a) = E(a)₁`), here given a standalone Formal Contract for V-positions."
**Problem**: A definition's introduction should advance its meaning, not announce its placement relative to sibling blocks ("paralleling the ... block below," "here given a standalone Formal Contract"). This is cross-reference scaffolding, not content.
**Required**: State the definition (`subspace_I(a) = E(a)₁`) and its precondition directly; remove the placement narration.

### Issue 4: Hypothetical future-subspace justification before D-CTG
**ASN-0036, Arrangement contiguity**: "The underlying reasoning is parametric in S — should the constraints be extended to another subspace in future work, the proofs would apply with the obvious substitution `1 ↦ S` — but the formal contracts here are written for `S = 1`."
**Problem**: This imagines work the ASN does not do and asserts, without proof, that future proofs "would apply." It does not advance any `S = 1` claim. Stating that D-CTG/D-MIN/D-SEQ are bound to `S = 1` is sufficient; the parametricity speculation is noise.
**Required**: Delete the parametric-extension sentence; retain only the binding to `S = 1`.

### Issue 5: ValidInsertionPosition split-rationale is design commentary
**ASN-0036, Valid insertion position**: "We split the valid-insertion-position predicate by document state. The non-empty case has its depth determined by state via S8-depth, so the predicate is binary; the empty case takes the depth as an operational input... Splitting eliminates the ambiguous third argument from the non-empty case while keeping the empty case's depth input explicit."
**Problem**: This paragraph justifies the authoring decision to use two predicates rather than stating system behavior. The two Formal Contracts that follow already make the binary/ternary distinction self-evident.
**Required**: Remove the meta-justification; let the two definitions stand on their own.

### Issue 6: S8a invokes T4 on a bare element field that is not a T4 address
**ASN-0036, S8a proof and contract**: Preconditions/Depends list "T4 (HierarchicalParsing, ASN-0034)" and the proof states "T4... constrains the structure of every field." But a V-position (`zeros(v) = 0`) is a standalone element-field tumbler, not a valid four-field T4 address (under T4c, `zeros = 0` would read as a *node* address).
**Problem**: T4 governs full N.0.U.0.D.0.E addresses; applying it to an isolated field is unjustified. Moreover the derivation does not need T4 — the proof itself derives componentwise positivity "directly from `zeros(v) = 0` together with T0's ℕ-valued carrier." The T4 citation is both imprecise and unused for the derived conjuncts.
**Required**: Drop T4 from the derivation of the `zeros(v) = 0` / positivity conjuncts (cite only the element-field definitional commitment plus T0/NAT-discrete), or explicitly justify treating a bare element field under T4's field-segment constraint.

### Issue 7: S9 restates S0 with no formal content
**ASN-0036, S9 / Properties table**: The table records S9 as a "named directional reading of S0 (no formal content beyond S0)," and the *Corollary of S0* confirms S9's consequent is discharged directly by S0.
**Problem**: Given the anti-bloat classifier, a property whose entire content is a re-reading of S0 plus a one-way-dependency diagram is restatement. The diagram and the "S0 is the mechanism; S9 is the consequence" gloss repeat the asymmetry already established under S3 and the persistence-independence section.
**Required**: Either give S9 content S0 lacks (e.g., a precise statement quantifying over the *family* of arrangements that S0 alone does not phrase), or demote it to a one-line corollary of S0 rather than a full property block with proof, contract, and diagram.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contiguity semantics
**Why out of scope**: The ASN correctly defers link-subspace (`S = 2`) tombstone/append-only semantics to a future ASN and binds D-CTG/D-MIN/D-SEQ to `S = 1`. This deferral is appropriate, not an error here — flagging only to confirm no coverage gap is implied.

META: The ASN remains squarely within specification territory — it defines the two state components (C, M), their invariants (S0–S9), and arrangement well-formedness abstractly enough to bind any implementation; it has not drifted to implementation mechanics.

VERDICT: REVISE
