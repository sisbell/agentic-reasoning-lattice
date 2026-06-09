# Review of ASN-0117

This is a strong, thorough note: the operation is cleanly defined, the case split on `R = ∅` vs `R ≠ ∅` is handled correctly, edge cases (leading-span, suffix, delete-everything, within-document sharing, cross-document transclusion, multi-position shift) are all exercised with concrete worked examples, the wp analysis is non-trivial and per-link-existential (correct), and the displacement is correctly inherited from ASN-0082 with the `s_C = 1` bridge made explicit. The technical content holds. The findings below are about uneven invariant coverage and accreted prose.

## REVISE

### Issue 1: P4a (a composite-boundary invariant) is never addressed

**ASN-0117, "Effect" and "The document remains one coherent sequence"**: The note invokes ExtendedReachableStateInvariants only for "the per-state invariant package" ("...satisfies the per-state invariant package of ExtendedReachableStateInvariants"), then hand-derives the composite-boundary properties **P4★** and **P7a** in the Effect section.

**Problem**: ExtendedReachableStateInvariants lists the composite-boundary properties as exactly `P4★ ∧ P4a ∧ P7a`. The note derives two of the three manually and never mentions **P4a (TraceWitnessing)** at all. Because the note deliberately cites only the *per-state* half of the theorem, P4a's preservation at DELETE's post-state (a composite boundary) is established nowhere — neither cited nor derived. The treatment of the boundary half is uneven: two clauses hand-proved, one silently dropped.

**Required**: Either (a) cite the composite-boundary half of ExtendedReachableStateInvariants once — which uniformly supplies P4★, P4a, and P7a for any valid composite from a reachable state, making the manual P4★/P7a derivations redundant — or (b) address P4a explicitly alongside P4★ and P7a (it holds trivially: `R' = R` and the trace to `Σ` is a prefix of the trace to `Σ'`, so every existing record keeps its witness). As written, the note hand-derives the easy two and omits the one that actually involves the trace.

### Issue 2: Duplicated "blanket `ran ⊆ dom(C)` would be false" argument

**ASN-0117, "The document remains one coherent sequence"**: "Stating the whole range as `ran(M'(d)) ⊆ dom(C')` would be false for any document containing a link, since its preserved link positions map into `dom(L)`..."

**ASN-0117, "P5 (DocumentIsolation)"**: "...a single `M'(d')(v') ∈ dom(C')` clause cannot be stated for *every* `v'`, because link positions resolve into `dom(L)`. The per-subspace split here is the same one S3★ forces on `M'(d)` above (§'The document remains one coherent sequence')..."

**Problem**: The same observation — a blanket content-store containment is wrong because link-subspace positions resolve into `dom(L)` — is made twice in different sections, with the second instance explicitly back-referencing the first. This is the redundant-deferral pattern: two paragraphs saying the same thing, one pointing at the other. The reader re-reads a point already made.

**Required**: State the per-subspace S3★ split once (at first use) and let the later section cite the established split without restating the negative ("would be false") justification.

### Issue 3: Defensive comparative prose in DEL-LIMM and boundary examples

**ASN-0117, DEL-LIMM frame clause**: "This is *stronger* than L12 (LinkImmutability, ASN-0043), which fixes only the values of links already present and would still permit `dom(Σ'.L) ⊋ dom(Σ.L)`..."

**ASN-0117, "Boundary — suffix delete" and "Boundary — delete everything"**: Both worked examples re-run the identical J2-supplied frame discharge (`Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, link store fixed, S3★, P4★, P7a) in nearly the same words.

**Problem**: The DEL-LIMM comparison spends a sentence on *what L12 would otherwise permit* — a hypothetical the clause's own statement already forecloses; this is the "imagines a case the claim already excludes" pattern. The two `R = ∅` boundary examples discharge the same elementary-K.μ⁻ frame package twice with no new structure exercised between them (delete-everything is just suffix-delete with `n'_{s_C} = 0`).

**Required**: For DEL-LIMM, state the strict-frame guarantee (`Σ'.L = Σ.L`) and drop the counterfactual about L12. For the boundary examples, collapse the two `R = ∅` cases into one (noting delete-everything as the `n'_{s_C} = 0` specialization) rather than repeating the frame discharge.

## OUT_OF_SCOPE

### Topic 1: Deletion in the link subspace (`subspace(p) = s_L`)
**Why out of scope**: The precondition fixes `S = s_C`; removal of link-subspace arrangement entries is a distinct operation tied to link lifecycle, properly a future note alongside MAKELINK.

### Topic 2: General-depth deletion (`m > 2`)
**Why out of scope**: The precondition fixes `m = #p = 2`, inheriting ASN-0082's depth-2 contraction. Extending past depth 2 requires extending the foundation displacement first; the note honestly states the restriction.

### Topic 3: Backtrack reconstruction, concurrent un-serialized deletion, content-index invariants, orphaned-link obligations
**Why out of scope**: All four are correctly deferred to the Open Questions as future territory — they presume backtrack machinery, concurrency model, or discovery-index state this note does not introduce.

VERDICT: REVISE
