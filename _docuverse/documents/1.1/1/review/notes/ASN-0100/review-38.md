# Review of ASN-0100

## REVISE

### Issue 1: The step-2 "forced vs. canonical-decomposition choice" taxonomy is decomposition-justifying meta-prose

**ASN-0100, Substrate Decomposition, step 2**: cases *(i.a) — Forced by precondition*, *(i.b) — Forced omission*, *(ii) — Canonical-decomposition choice (both sub-cases)*, e.g. "The omission of K.μ⁻ in case (ii) is therefore a canonical-decomposition parsimony choice in both sub-cases — the alternative decomposition is admissible under K.μ⁻ + K.μ⁺ for both — rather than a forced consequence of either sub-case."

**Problem**: This is multi-paragraph prose justifying *why* a decomposition step is omitted and whether the omission is "forced" or a "parsimony choice." It does not advance the operation's reasoning. The operative condition is single-line: K.μ⁻ fires iff the content-subspace Right region `{v ∈ V_{s_C}(d) : v ≥ p}` is non-empty (equivalently, strict `s_C` contraction is both needed and admissible while preserving `s_L`). The forced/choice distinction, the per-sub-case `n'_{s_L}` bookkeeping ("the `V_{s_L}(d) = ∅` sub-case sets `n'_{s_L} = n_{s_L} = 0` trivially, and the `V_{s_L}(d) ≠ ∅` sub-case sets `n'_{s_L} = n_{s_L}`"), and the cross-deferring among (i.a)/(i.b)/(ii) ("matching case (i.a)'s forced omission, with the same effect as case (ii)'s reduction") are exactly the reviser-drift patterns the anti-bloat classifier targets.

**Required**: Collapse to the operative condition: K.μ⁻ appears iff the pre-state content-subspace Right region is non-empty; otherwise omitted. Delete the forced/choice taxonomy and the per-sub-case retention enumeration.

### Issue 2: Case (ii)'s "alternative decomposition" contradicts step 3's own contract constraint

**ASN-0100, Substrate Decomposition step 3**: "INSERT's contract restricts this freedom by mandating that step 3's K.μ⁺ firing add *precisely* the Insertion and Shifted-right V-positions and no additional `s_C` positions."
**vs. step 2 case (ii)**: "an alternative decomposition could fire K.μ⁻ with `n'_{s_C} < N` ... A subsequent K.μ⁺ then re-adds the discarded `s_C` positions before adding Insertion ... reaching the same Σ'."
**vs. Atomicity section**: "The subsequent K.μ⁺ may re-add the full sequential run `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}` ... Such alternative decompositions are admissible and reach the same Σ'."

**Problem**: Step 3 imposes a "contract-level constraint" that K.μ⁺ adds *no additional `s_C` positions* beyond Insertion ∪ Shifted-right, and INS.M-exhaustive is "derived" from this mandate. But case (ii) and the uniqueness/atomicity section explicitly describe admissible decompositions whose K.μ⁺ re-adds discarded Left positions — i.e., adds `s_C` positions outside Insertion ∪ Shifted-right. A clause cannot be both a binding contract on step 3 and routinely violated by admissible decompositions. The intended meaning is "no `s_C` positions outside Left ∪ Insertion ∪ Shifted-right *in the post-state*," which is a property of Σ', not a stipulation on one K.μ⁺ firing.

**Required**: Derive INS.M-exhaustive as a property of the post-state `V_{s_C}(d')` — established via the uniqueness-of-Σ' argument the ASN already gives — rather than as a mandate on the canonical K.μ⁺ firing. Then either drop the "contract-level constraint" framing or restrict it explicitly to the canonical decomposition while stating that exhaustiveness is decomposition-independent.

### Issue 3: Composite-atomicity exposition is restated across three sections

**ASN-0100**: the same content appears in (a) Environmental Assumptions ("Composite atomicity. No elementary transition of any other composite interleaves..."), (b) Atomicity and Canonical Order ("*Composite-level atomicity* ... is *not* entailed by SequentialTransitionAxiom; it is a stronger property..."), and (c) the closing paragraph ("The composite-atomicity precondition is therefore part of INSERT's specification, not an implementation footnote.").

**Problem**: Three passages in different sections make the same point — elementary atomicity is supplied by SequentialTransitionAxiom, composite atomicity is a stronger environmental precondition the substrate must provide, violation makes Σ' a joint product. This is the "two paragraphs say the same thing in different words" pattern, multiplied to three.

**Required**: State the composite-atomicity precondition once (it belongs in the contract under INS.pre), and reference it from the Atomicity section without re-deriving the elementary-vs-composite distinction or re-arguing the concurrent-INSERT failure mode.

### Issue 4: The "I3 covers the shift-only regions, Insertion verified separately" explanation is repeated four times

**ASN-0100**: the partition explanation recurs in (a) the "Scope of ASN-0082's I3 against INSERT's post-state" paragraph, (b) §Arrangement functionality ("I3-S2 ... does *not* cover the Insertion region ... verified by the explicit pairwise-disjointness argument above"), (c) §Referential integrity ("I3-S3 ... the Insertion region's contribution is verified explicitly above"), and (d) §Post-state V-position well-formedness ("They do not cover INSERT's Insertion region ... verified explicitly below").

**Problem**: The per-invariant verification work is legitimate, but the surrounding meta-prose explaining *that* I3 covers Left + Shifted-right + cross-subspace while Insertion is handled separately is restated verbatim-in-substance four times. Stating the partition once and then doing the per-invariant work suffices.

**Required**: State the I3-coverage/Insertion-gap partition once (the dedicated "Scope of ASN-0082's I3" paragraph), then let each invariant subsection do its verification without re-explaining the partition.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion semantics
**Why out of scope**: The ASN correctly restricts to the content subspace and names `K.μ⁺_L` / `K.λ` as a structurally different operation; a future ASN.

### Topic 2: Minimum substrate machinery to secure composite atomicity
**Why out of scope**: Raised in Open Questions; this is the substrate environment's concern, not a gap in INSERT's per-state specification.

VERDICT: REVISE
