# Review of ASN-0120

## REVISE

### Issue 1: The ρ = ∅ boundary is settled twice, with twin deferrals to the same Open Question
**ASN-0120, "What the endset arguments name…" (final paragraph) and "Three endsets…" (ML5 paragraph)**: The resolution section ends with: "the empty slot is benign at each point downstream. `K.λ`'s value precondition constrains only slot 3 … so `(∅, e₂, e₃)` and `(e₁, ∅, e₃)` are legal link values. And the slot is *inert* in ML9's discoverability test … This is the degenerate *one-sided* link whose slot convention ML5 records below. Its definedness is settled here; what the empty non-type endset *means* for the link's connection is deferred to the Open Questions." The ML5 paragraph then restates the identical facts: "ρ(R_j, Σ) = ∅ forces `e_j = ∅`, the operation is defined on the input, the record is L3-legal, and the empty slot is inert in discovery. What the empty non-type slot *means* for the link's connection we defer to the first Open Question."
**Problem**: This is the flagged accretion pattern in both of its forms: two paragraphs in different sections saying the same thing in different words (defined / L3-legal / inert-in-ML9 appears verbatim-equivalent in both), and two paragraphs deferring to the same downstream location (the first Open Question is pointed at twice). The connective scaffolding compounds it: "we return to this boundary below" (recovery-equation paragraph), "whose slot convention ML5 records below," "walked at the recovery equation," "settled here … deferred to the Open Questions" — four pieces of document-navigation prose orbiting one boundary case. The reader following ML5's directionality argument must skip past a re-derivation of facts already established two sections earlier.
**Required**: Settle the boundary once — the natural home is the resolution section, where the recovery equation forces `e_j = ∅`. Fold the one-sided-link slot convention (the Nelson LM 4/48 material) into that single treatment, and let ML5 cite it in one clause rather than re-deriving it. Keep exactly one deferral to the Open Question.

### Issue 2: The "equivalently" gloss on the ordinal-displacement precondition is false as stated
**ASN-0120, "What the endset arguments name…"**: "carries an *ordinal displacement* `ℓ_j = δ(n_j, m)` — equivalently `actionPoint(ℓ_j) = #u_j`, the tight half of T12's `actionPoint(ℓ_j) ≤ #u_j`"
**Problem**: `ℓ_j = δ(n_j, #u_j)` is strictly stronger than `actionPoint(ℓ_j) = #u_j`. Counterexample: `ℓ = [0, …, 0, 3, 0, 5]` of length `#u_j + 2` has `actionPoint(ℓ) = #u_j` and `Pos(ℓ)`, but is not an ordinal displacement — and with such an `ℓ` the identity `u_j ⊕ ℓ_j = shift(u_j, n_j)` that the confinement argument invokes from OrdinalShift fails (the sum has length `#u_j + 2`). The missing conjunct is the length condition: the δ-form is equivalent to `#ℓ_j = #u_j ∧ actionPoint(ℓ_j) = #u_j` (then positions below the action point are zero and the action point is the last component, recovering `δ(ℓ_m, m)`). The normative `wf` clause is correct; the gloss misstates it, and a reader taking the gloss as the precondition would admit spans the rest of ML1's machinery cannot handle.
**Required**: Either drop "equivalently" or complete it: "equivalently `#ℓ_j = #u_j ∧ actionPoint(ℓ_j) = #u_j`."

### Issue 3: ML7's parenthetical hedges against the invariant it just proved
**ASN-0120, "The invariants MAKELINK preserves," ML7**: "(Whether a link's *owner* may delete it is a separate operation outside this ASN; MAKELINK guarantees that no one *else's* edit can break it.)"
**Problem**: ML7's body establishes, via L12, that *no* transition removes the address or alters the value — the guarantee is unconditional, not "no one else's." The parenthetical imagines an owner-deletion case that L12, cited two sentences earlier as the carrier of the claim, excludes from the transition vocabulary entirely. As written it silently weakens the theorem with a sociological disclaimer. Link editing is already named in the Scope exclusions; the hedge adds nothing the scope list doesn't.
**Required**: Delete the parenthetical, or replace it with a statement consistent with L12 (e.g., that any future link-retirement operation is a model extension outside the present transition vocabulary, per the EDITLINK scope exclusion).

### Issue 4: ML4's paragraph states the no-coupling fact three times in two sentences
**ASN-0120, "Residence, and its independence…"**: "MAKELINK admits a home `d` together with endsets whose coverage is *disjoint* from everything under `d`'s prefix … Formally, the precondition imposes no constraint relating `d` to `ρ(R_j, Σ)`: … — nothing relates any `ρ(R_j, Σ)` to `d`, and in particular all three may be disjoint from everything under `d`'s prefix."
**Problem**: "imposes no constraint relating `d` to `ρ(R_j, Σ)`" and "nothing relates any `ρ(R_j, Σ)` to `d`" are the same clause twice within one sentence, and "disjoint from everything under `d`'s prefix" appears twice in the paragraph. Sentence-level duplication of the kind the anti-bloat classifier targets.
**Required**: One formal statement of the non-coupling (the precondition relates `d` to no `ρ(R_j, Σ)`) followed by the one substantive consequence (all three resolved sets may be disjoint from `d`'s subtree).

## OUT_OF_SCOPE

### Topic 1: Endset arguments supplied as raw I-addresses or spans (ghost and foreign endsets)
**Why out of scope**: The ASN correctly restricts MAKELINK-via-V-specs to content-backed endsets (`ρ ⊆ dom(Σ.C)`) and notes that reaching L4/L9's full generality requires a distinct argument shape. That is a different operation surface, properly a future ASN, and the body already marks it as such.

### Topic 2: Endset arguments resolving through the link subspace (links to links), and the assertional meaning of an empty non-type endset
**Why out of scope**: Both are recorded as Open Questions. The definedness of the empty-slot boundary is settled in-model here; what remains open is semantics, which is new territory rather than an error.

### Topic 3: Link retirement/editing semantics under ownership
**Why out of scope**: EDITLINK (ASN-0076) is explicitly excluded by the scope list; this ASN need only stay consistent with L12 (see Issue 3).

The technical core is sound and was checked in detail: the T5 confinement argument discharging `ρ(R, Σ) ⊆ dom(Σ.C)` is correct including the depth-mismatch case; the recovery equation's `F`-trace (with the frontier counterexample motivating it), the TS3/S3 merge induction, the extensional coverage form, and tightness/LP19a stability all hold as cited; ML6's necessity-and-sufficiency for L3's type clause is exact; ML9's wp argument (Facts (a) and (b), including the `d' = d` boundary where the home's range gains `a`) is complete, with the `s_C`/`s_L` subspace exclusion correctly disposing of the link-store half at every future state; the worked example exercises the claims it cites. The remaining items are prose precision and accretion, not gaps in the mathematics.

META: (not applicable — the ASN defines an operation by preconditions, postconditions, frame, and preserved invariants, squarely in specification territory)

VERDICT: REVISE
