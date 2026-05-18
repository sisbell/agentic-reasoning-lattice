# Review of ASN-0047

## REVISE

### Issue 1: SequentialTransitionAxiom contains use-site inventory

**ASN-0047, *The state model***: "SequentialTransitionAxiom (Axiom, SequentialAtomicTransitions). The transition relation `Σ → Σ'` is single-event sequential: ... Every per-state invariant and every precondition-discharge argument in this ASN — including K.δ's freshness discharge against `e ∉ E`, K.α's freshness against `dom(C)`, K.λ's freshness against `dom(L)`, and every K.μ⁺/K.μ⁻/K.μ~ precondition evaluated against the pre-state arrangement — operates within this sequential-atomic semantics."

**Problem**: The third sentence enumerates downstream consumers of the axiom rather than advancing its meaning. This is the reviser drift pattern "definition's introduction enumerates downstream consumers." The axiom statement and equivalent form are content; the enumeration is meta.

**Required**: Remove the use-site enumeration. The axiom's statement and equivalent restatement are sufficient; consumers cite the axiom at their use sites.

### Issue 2: Ghost-base versioning paragraph in K.δ is essay content

**ASN-0047, *Elementary transitions* (K.δ)**: The "*Ghost-base versioning (k = 1).*" paragraph runs ~150 words explaining why the relaxation is invariant-safe, citing Gregory's `docreatenewversion`, justifying the structural-only operand requirement, and noting "The relaxation applies only to the *initial* version step."

**Problem**: The precondition list (specifically the "k = 1 (version)" sub-case) already states the relaxation. The paragraph is justification: *why* the relaxation works, implementation evidence, and scope limitation prose. This is essay content in a structural slot.

**Required**: Condense to one sentence stating that the k = 1 sub-case admits `t ∉ E_doc`, with the structural-only check and ghost-routing chain consequence stated in K.δ's freshness discharge paragraph (which already covers this).

### Issue 3: K.δ effect on M is described three times

**ASN-0047, *Elementary transitions* (K.δ)**: The K.δ definition contains:
- Effect statement: "`E' = E ∪ {e}` where `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`"
- "*Effect on M, per case.*" paragraph: per-case M behavior with collective form
- "*Frame:*" paragraph: "The M-effect is per-case (above): IsNode and IsAccount frame M entirely ... IsDocument frames M on every d' ≠ e and initialises `M'(e) = ∅` (which equals `M(e)` by the totality convention, so the *value* of M' on every address coincides with M, but e enters E_doc, so the *typing* of M' changes). The per-case M-statements above are the effect; this frame summary lists only the components on which all three cases agree uniformly (C, L, R)."

**Problem**: The Frame paragraph restates the Effect-on-M paragraph's content and adds interpretive prose about typing-vs-value distinctions. This is duplication.

**Required**: State M's effect once, in the Effect or Frame paragraph (not both). The typing-vs-value observation belongs in a single line, not a paragraph.

### Issue 4: P5 retirement paragraph is meta-prose about claim relationships

**ASN-0047, *Extended monotonicity invariants***: "P3★ supersedes P5 in the extended state by extending the monotonicity statement to L. **Once the link store enters the state model, P3★ is the canonical per-transition monotonicity invariant and P5 is no longer separately stated — P5's three conjuncts (dom(C) growth with value preservation, E growth, R growth) survive intact as conjuncts of P3★, joined by the new dom(L) growth with value preservation. The ExtendedTransitionInvariants synthesis below cites P3★ rather than P5; readers applying invariants in the extended state should treat P3★ as the unique per-transition monotonicity claim, with P5 retired.**"

**Problem**: The bolded sentences are essay content explaining how claims relate, addressed to readers ("readers applying invariants ... should treat ..."). This is reviser drift.

**Required**: One sentence: "P3★ supersedes P5 in the extended state, extending P5's monotonicity to L." Drop the reader address and the retirement narrative.

### Issue 5: K.μ⁻ has overlapping explanatory paragraphs

**ASN-0047, *Elementary transitions* (K.μ⁻)**: After the precondition list, K.μ⁻ contains:
- A "verification" paragraph: "The case analysis below is a *verification* that this admissible-pattern precondition is exactly what the D-CTG★ and D-MIN★ postconditions admit..."
- A paragraph on what contraction preserves
- The Exhaustiveness lemma with proof
- A post-lemma summary: "Only case (a) is consistent ... Case (b) violates D-CTG★ ... Case (c) violates D-MIN★ ..."
- A closing paragraph: "Contraction is pure removal — the domain shrinks, and no surviving value is altered. Without the value-preservation clause, K.μ⁻ could modify values at remaining positions, conflating contraction with rewriting. Nelson: 'the owner of a document may delete bytes...'"

**Problem**: Five paragraphs surrounding one lemma. The "verification" preamble and post-lemma summary together restate what the lemma proves. The closing paragraph with Nelson quote is design-intent narrative.

**Required**: Reduce to: precondition list, the exhaustiveness lemma (which already contains the case-by-case admissibility argument), and one short closing paragraph on the invariants preserved. Drop the verification preamble and the Nelson-quoted contraction-as-pure-removal essay.

### Issue 6: Decomposition of K.μ~ restates the bijection equation

**ASN-0047, *Elementary transitions***: "K.μ~ realises the *bijection equation* `(E π : π is a bijection dom(M(d)) → dom(M'(d)) : (A v ∈ dom(M(d)) :: M'(d)(π(v)) = M(d)(v)))` together with the admissibility constraints and derived frame catalogued in §*Decomposition of K.μ~* below."

**ASN-0047, *Decomposition of K.μ~***: "K.μ~ realises the bijection equation stated in §*Elementary transitions* above. π is admissible iff..."

**Problem**: Deferral-and-restate pattern. The first site defers to the second; the second refers back. Both restate the equation.

**Required**: State the bijection equation once at the §*Decomposition of K.μ~* site (where the admissibility constraints follow). At the elementary transitions site, state only that K.μ~ is a named composite of K.μ⁻ + K.μ⁺ and point to the decomposition section.

### Issue 7: Worked example preamble is use-site inventory

**ASN-0047, *Worked example: interior content replacement***: "We trace the interior-position case of the content-replacement decomposition (K.μ⁻ + K.μ⁺ with `n'_{s_C} = k₀ − 1` rather than the single-position pair at `k₀ = n_{s_C}`) introduced in the *Elementary transitions* section. The example exercises the multi-position K.μ⁻ + K.μ⁺ pair, the intermediate-state admissibility verification at M_int, the K.μ⁺ amendment's content-subspace restriction on the rebuild, and the asymmetric coupling of J1★ and J1'★ to new versus re-added addresses at the composite boundary."

**Problem**: The second sentence enumerates what the example exercises — a use-site inventory. The example itself will demonstrate these. Inconsistent across the document: the link allocation worked example has no comparable preamble.

**Required**: One sentence stating the scenario. The exercised features will be visible in the example.

### Issue 8: Invariant verification convention paragraph is reader guidance

**ASN-0047, *Invariant verification convention (worked examples)***: The entire section explains how to read the worked examples (what gets verified at each step, what's skipped, what's a deviation).

**Problem**: Reader guidance, not content. It documents an internal review convention rather than the spec.

**Required**: Drop the convention paragraph. The worked examples should be self-contained — if a verification is omitted, the reason (frame condition, vacuity) is local to that step, not a convention.

### Issue 9: K.α cross-document distinctness not addressed in S4 proof

**ASN-0047, *Extended reachable-state invariants*, Foundation invariants**: For K.λ, S4 explicitly cites the Cross-document disjointness chain lemma (T10a.{2,5} → T10) for cross-document distinctness. For K.α the proof states only: "Each K.α produces `a` via the T10a allocator under origin(a) (S7a, ASN-0036), so GlobalUniqueness (T10a) gives `a ∉ dom(C)`."

**Problem**: GlobalUniqueness within a single sub-allocator gives freshness within that chain, not cross-document distinctness. Two K.α events under distinct documents need the same Cross-document disjointness chain (with `b_C` in place of `b_L`) to establish distinctness of their outputs.

**Required**: Add one sentence to the K.α treatment in S4: cross-document distinctness for content allocations follows from the Cross-document disjointness chain lemma applied at `b_C(d₁)` and `b_C(d₂)`.

### Issue 10: L14a amendment is mentioned in prose but not in summary table

**ASN-0047, *Amendments to existing transitions***: "L14a amendment. In the extended state, S3★ + CL-OWN supersede ASN-0043's L14a."

**Problem**: This is a substantive supersession of an ASN-0043 invariant (NonTranscludability). The "Local extensions and strengthenings" summary table at the end lists every other foundation supersession but omits L14a.

**Required**: Add an L14a row to the Local extensions table, noting the supersession by S3★ + CL-OWN.

### Issue 11: Lemma (Permanence from elementary frames) has interpretive sentence

**ASN-0047, *Coupling and isolation***: "The L12 clause is vacuous in the four-component state (where L is not yet a state component); in the extended state it provides the link-store analog of P0, completing the structural symmetry between the content store and the link store."

**Problem**: "completing the structural symmetry between the content store and the link store" is interpretive essay content.

**Required**: Drop the trailing clause; the vacuity-vs-extended-state observation is sufficient.

### Issue 12: Permanence section's "P3★ below" forward reference accretion

**ASN-0047, *Permanence***: "The quantitative monotonicity content — domain growth plus value preservation across C, L, E, R — is supplied by P0, P1, P2, and L12 individually, and consolidated under P3★ in *Extended monotonicity invariants* below."

Combined with §*Extended monotonicity invariants*: "P3★ synthesises P0 ∧ L12 ∧ P1 ∧ P2 into one named monotonicity predicate over `Σ → Σ'`."

**Problem**: Two paragraphs deferring to/back from the consolidation. The Permanence section states the four primitives; the consolidation site introduces P3★. The forward-pointer prose adds no content.

**Required**: Drop the forward reference. The Permanence section can stand on its own; the §*Extended monotonicity invariants* synthesis can cite the four primitives directly when introducing P3★.

## OUT_OF_SCOPE

No additional out-of-scope items beyond those the ASN's own Open Questions section already catalogues.

VERDICT: REVISE
