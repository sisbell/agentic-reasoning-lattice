# Review of ASN-0036

## REVISE

### Issue 1: Foundation properties referenced under invented names

**ASN-0036, multiple Depends/proof sites**: D-CTG, D-MIN, D-CTG-depth, D-SEQ, and S8 all cite "T1 (TumblerOrdering, ASN-0034)"; OrdShiftHom cites "TumblerAdd (PositionAdvance, ASN-0034)".

**Problem**: The foundation defines these as **T1 — LexicographicOrder** and **TumblerAdd — TumblerAdd**. "TumblerOrdering" and "PositionAdvance" are not the canonical names; "position-advance" appears only in TumblerAdd's prose description. Per the self-containment convention (use the foundation's name, don't reinvent), a reader cross-checking the dependency table against the foundation will not find these labels.

**Required**: Rename every "T1 (TumblerOrdering)" to "T1 (LexicographicOrder)" and "TumblerAdd (PositionAdvance)" to "TumblerAdd". (TS2/TS3/TS4, T0(a), GlobalUniqueness, OrdinalShift, etc. are already cited under their correct foundation names — only these two drift.)

### Issue 2: S8's I-side "structural shape" claim is restated four times and pulls in dependencies it never uses

**ASN-0036, S8 (statement conjunct (b), proof "succ stays within a subspace…" and "Chains are runs…", postcondition (a))**: the assertion that each lockstep image `shift(aⱼ, k)` "is a structurally valid element-level I-address (`zeros = 3` by S7b)…T4-valid (T10a.4)" appears in the run definition, twice in the proof, and again in the postcondition, and is the sole reason S7b and T10a.4 enter S8's Depends.

**Problem**: The partition theorem is established entirely on the V-side via the lockstep-successor (`succ` injective by TS2, acyclic by TS4, chain-decomposed on the finite set by S8-fin, confined to a subspace by OrdShiftHom). The *membership* `shift(aⱼ, k) ∈ dom(Σ.C)` (from S3) is used; the further elaboration into `zeros = 3` / T4-validity is consumed by nothing in the existence, lockstep-identity, maximality, or uniqueness arguments. Applying `shift` to an I-address (`a ⊕ δ(k, #a)`, action point `#a ≤ #a`) needs no structural hypothesis. This is accreted decoration repeated across four structural slots — exactly the anti-bloat pattern flagged for this note.

**Required**: State `shift(aⱼ, k) ∈ dom(Σ.C)` once (via S3) and remove the `zeros = 3` / T4-validity elaboration from the statement, both proof occurrences, and the postcondition; drop S7b and T10a.4 from S8's Depends unless a load-bearing use is identified. If the I-side structural shape is genuinely a wanted corollary, assert it exactly once as a separate remark, not inline at every mention of `shift(a, k)`.

### Issue 3: S2 postcondition adds nothing beyond the partial-function axiom

**ASN-0036, S2**: "Each V-position maps to exactly one I-address, by the `Σ.M(d) : T ⇀ T` partial-function declaration"; the only Formal Contract postcondition is "`ran(Σ.M(d)) = {…}` is a well-defined set."

**Problem**: Functionality is already entailed by the `T ⇀ T` axiom declared in the Σ.M(d) contract. S2's postcondition restates that the range is a set — a consequence of any function — so the property carries no content distinct from the axiom it cites. It reads as a named placeholder so downstream proofs can write "(S2)".

**Required**: Either give S2 a postcondition that is not an immediate restatement of the partial-function declaration (e.g., the single-image property in the explicit quantified form, derived from the declaration), or fold S2 into the Σ.M(d) axiom and cite that axiom directly where S8/run-labels currently cite S2.

## OUT_OF_SCOPE

### Topic 1: Contiguity for the link subspace (S = 2)

**Why out of scope**: D-CTG, D-MIN, D-SEQ are deliberately stated only for the text subspace (S = 1), per Nelson's character-position evidence. Whether the link subspace satisfies an analogous contiguity is link-layer territory, which the Scope section excludes.

### Topic 2: Which operations preserve D-CTG/D-MIN/S2 and establish subspace alignment

**Why out of scope**: The Open Questions correctly defer INSERT/DELETE/COPY/REARRANGE frame conditions and the V-position/I-address subspace-alignment obligation to the operations layer; these are not defects in the strand model's state-level invariants.

VERDICT: REVISE
