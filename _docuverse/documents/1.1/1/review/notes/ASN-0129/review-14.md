# Review of ASN-0129

The technical core checks out. I verified the four-state trace step by step (gate verdicts, dedup branches, frontier addresses a₁–a₄, the active-view sequence ⊥,⊤,⊥,⊥ and default-view ⊥,⊤,⊥,⊤, the `ever_res` lock), the PD0 polarity rules (the filter/witness/count arguments are each sound, and `count(D) = c` correctly lives in neither class), the QD-fin induction, the V-IDX vacuity argument (R-C1 plus S3's empty behavior set does force a family-free class into every constructible registry), PC6's converse at its one non-trivial leaf (the Observe_K pattern query normalizes exactly to the exhibited QD filter, and V-TUP is genuinely load-bearing there), and the C-reach demotion (the out-degree-≤1 observation in count (i) is correct — the determinate walk does traverse a full cycle once before stopping, so `is_in_chain` is `reach` on those families). I also stress-tested whether QD's tuple-valued bases plus V-TUP silently void ASN-0128's D4 ("reverse access is opt-in") — they reconstruct `sources_to` for every K, but raw `Observe_K` always carried target-side patterns, so the capability was never absent and the reconstruction is unremarkable; not a finding. The remaining issues are anti-bloat findings under this note's classifier.

## REVISE

### Issue 1: Open Question 1 re-argues PC3's resolution instead of posing the question
**ASN-0129, Open questions §1**: "PC3 fixes one view per top-level term as a naming convention, and cross-view mixing is already derivable through the fixed-view slices — an audit-view domain filtered by an active-view body is a well-formed QD expression whose same-Σ semantics this note already fixes (PC3)."
**Problem**: This is PC3's own closing paragraph restated in different words — same example (the audit-view domain with active-view filter body), same conclusion ("surface design, not capability" / "surface syntax … not the semantic capability"). PC3 already says: "Cross-view readings are derivable now, inside a term of any view, through the fixed-view slices: … `{x ∈ L_K : P_active(x)}` — an audit-view domain filtered by an active-view body — is a well-formed QD expression whose semantics is already fixed … what is deferred (Open Question 1) is first-class surface syntax (`P[v]`) and its pragmatics, not the semantic capability." Two paragraphs in the same document saying the same thing; the reader of the open-questions list re-litigates a settled point before reaching the actual question.
**Required**: Trim Open Question 1 to the open half only — should the view become a first-class parameter `P[v]` with per-constituent binding, and which mixed-view idioms deserve named, checkable syntax — citing PC3 for the settled part rather than restating it.

### Issue 2: UV states its warrant three times in two adjacent paragraphs
**ASN-0129, UV**: (a) opener: "…left the behavior surfaces open (its Open Question 1); UV closes the question by extending the committed rule per codomain…"; (b) reconciliation paragraph: "…their default-view readings deferred to its Open Question 1, the question UV closes"; (c) same paragraph, closing sentence: "…the behavior surfaces are not on that list, being exactly what Open Question 1 held open."
**Problem**: The fact "ASN-0128's Open Question 1 left the behavior surfaces' default-view readings open and UV closes it" is stated three times inside UV (a fourth instance, in V, is the fence at introduction and can stand). The reconciliation paragraph itself is necessary — the readings of BH2's "BH1 filtering does not rewrite the walk" and BH1's "Nothing else is rewritten" must be explicit to avoid a silent override — but its two restatements of the warrant add nothing beyond the opener. This is the same-thing-in-different-words pattern compounding within one section.
**Required**: State the warrant once (the opener already does); let the BH2 and BH1 reconciliation sentences cite it ("the surface Open Question 1 held open") without re-deriving it, cutting instances (b)'s and (c)'s restatements to references.

### Issue 3: A per-view semantic derivation is embedded in V-PRIM's `elems` admission
**ASN-0129, V-PRIM, second bullet**: "(on `chain`'s output it loses no count — the returned sequence's elements are pairwise distinct, the walk's being so by BH2 and UV's rewrite only deleting — so `count(elems(chain(t)))` is the *returned sequence's* length: the walk's length at term views `audit` and `active`, but at `default` the rewritten sequence's length, strictly shorter whenever a traversed element is filtered, UV)"
**Problem**: Placement, not existence — the content is correct and useful (it is the only route to walk length, `Seq_fin(T)` having no length atom). But a three-clause derivation with per-view case analysis sits inside a vocabulary-admission parenthetical, and its per-view half is UV-owned semantics (chain's default rewrite) restated in compressed form. The reader must parse a proof to get past the admission of an order-forgetting projection.
**Required**: Keep the one-clause faithfulness fact at V-PRIM (elements pairwise distinct, so `count(elems(·))` is the sequence's length); move the per-view instantiation into UV's Collections clause, where chain's default rewrite is owned — or drop it there, since UV already fixes the rewritten sequence.

## OUT_OF_SCOPE

### Topic 1: Per-home link reads
PL cannot group or select link addresses by home document: no `home` projection is admitted, no homed-set base exists, and PC6 itself records that prefix testing is no substitute (`d ≼ a` does not characterize `home(a) = d`). BH4 consumes home-chain arithmetic strictly internally. A protocol wanting a per-home census ("active K-tuples homed at d") has no term.
**Why out of scope**: This is a vocabulary absence consistent with the note's minimality stance, and PC6's paired-admission discipline already prices how such an extension would land (atom and base move together). New admission, future ASN — not an error here.

### Topic 2: Frontier exposure and the full P-tgt
Only the residence disjunct of Nullify's P-tgt is PL-expressible (QD-audit correctly claims exactly the residence clause, as membership in the reflected `L_dom`); the self-emit disjunct `a = a_emit(Σ, d_retr)` would need a frontier-reading atom PL does not ship. A gating discipline that must state the surface's complete admission condition cannot.
**Why out of scope**: The note never claims full P-tgt expressibility, and whether any protocol needs to gate on the next emission address is a design question for the protocol layer, with the extension again governed by PC6's paired-admission discipline.

### Topic 3: Sequence vocabulary beyond `elems`
`Seq_fin(T)` is introduced by `chain` and eliminated only by `elems` (plus `tip`'s verdict): position, predecessor, and order queries on walks are inexpressible.
**Why out of scope**: Deliberate minimality — the walk's order is consumed at agent time today; richer sequence operations, if a protocol forces them, are a named future admission rather than a gap in this note's claims.

VERDICT: REVISE
