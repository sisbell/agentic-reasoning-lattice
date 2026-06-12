# Review of ASN-0129

## REVISE

### Issue 1: The reserved symbol `S` is rebound twice after being globally declared
**ASN-0129, States and signatures / PD2 / PC6**: "Throughout, `S` is the class of reachable substrate states" — then PD2 states its non-interference clause as "a term reading only *audit* slices of types in S is invariant under every deposit of a type outside S," and PC6's Observe_K normalization writes "`{x ∈ S_view : …}` with `S_view` the selected slice."
**Problem**: The note makes exactly one global symbol reservation and then violates it in its own formal statements. PD2's `S` is a set of coverage classes, not the state class, and the collision sits inside the load-bearing sentence of the frame-stability theorem — the one a protocol author is told to apply mechanically ("Name the exceptions or be surprised by them"). Every atom signature in the note is `S`-indexed by the declared convention, so a reader unifying PD2's statement against the signatures gets a type error. The foundation models the required care explicitly: AllocatedSet introduces 𝒮 precisely "to keep the state-space symbol distinct from the unrelated symbol S." A note defining a typed language is held to at least that standard on its own symbols.
**Required**: Rename PD2's type-set variable (e.g., 𝒦 or `Ks`) throughout PD2's statement and discussion; rename or fence PC6's `S_view` (it is subscripted, but it is the same reserved letter in a formal display). Leave `ST`/`SF` as-is — compound names do not collide.

### Issue 2: The is_doc emit-surface provenance is stated three times; the PC5 instance is inert for the claim it decorates
**ASN-0129, PC5**: "`is_doc` is a single membership check — the residence test the emit surface itself performs on every `idem = ⊤` miss and every admitted `idem = ⊥` call (I1/I5, ASN-0128; home validation is branch-local — a dedup hit never reads `d`)."
**Problem**: PC5 is a termination proof. "A single membership check" discharges the obligation entirely; which upstream operations perform the same test, and on which branch of the dedup logic, has zero bearing on whether the check halts. The same fact appears in full at QD-audit ("performed on every `idem = ⊤` miss (I1: home validation is branch-local, a hit never reads `d`), every admitted `idem = ⊥` call (I5), and every `Nullify_Binary` call (P0, both branches, S3…)") — where it is genuinely load-bearing for the base audit — and a third time as a pointer at V-DOC ("performed per branch structure, QD-audit"). One upstream fact recited in three sections is the duplication pattern this note's classifier flags, and the PC5 recitation forces the reader through emit-side justification to reach a one-clause termination argument.
**Required**: Keep the full grounding once, at QD-audit. Reduce PC5's clause to "a single membership check on `dom(Σ.M)`" with at most a bare citation. V-DOC keeps its pointer.

### Issue 3: Two sections close by deferring to C-reach; the PC6 pointer sentence carries no content
**ASN-0129, PC6 (costs paragraph) and PC6a**: "what this loop entails against C-reach is recorded at C-reach." / "what the *semantics* can nonetheless express is the separate question C-reach addresses."
**Problem**: This is the flagged accretion pattern — multiple paragraphs in different sections deferring to the same downstream location. The PC6 sentence in particular is pure "see below": the feedback loop's exhibit is complete where it stands, and the polarity analysis it gestures at is stated in full at C-reach ("feedback evaluation over the base decides `reach` (PC6's loop), so a feedback-ceiling claim … would entail ¬C-reach"). A reader following PC6's argument must step over the pointer to get nothing they won't be given verbatim two sections later.
**Required**: Delete the PC6 sentence — the loop stands on its own, and C-reach already names it as "PC6's loop," which is the only cross-reference needed. PC6a's closing deferral may stay (it fences PC6a's scope), but it should then be the *only* forward pointer to C-reach.

### Issue 4: QD-audit buries a second topic inside a nested parenthetical of a ~110-word sentence
**ASN-0129, QD-audit**: "The document store contributes a membership atom, not a base: document-residence … — the one *arrangement-store*-domain test the upstream contracts perform (the link store carries its own checked domain test, `Nullify_Binary`'s P-tgt residence clause `a ∈ A_rel^Σ`, S3 — already PL-expressible as membership in the reflected `L_dom`, needing no atom of its own) — and a gating discipline written in PL must be able to state what the surface checks; V-DOC admits exactly that test, as `is_doc`."
**Problem**: The parenthetical's content is legitimate audit work — P-tgt's residence test is a surface-performed domain check, and the audit should account for why it needs no atom — but it is a distinct audit item (link-store residence) embedded as an aside inside the sentence auditing a different item (arrangement-store residence), behind two levels of nesting. The placement is the defect: a reader auditing the `is_doc` admission must parse and discard a complete second argument mid-sentence, then recover the main clause's spine across the interruption.
**Required**: Promote the P-tgt accounting to its own sentence ("The link store's analogous surface check, P-tgt's `a ∈ A_rel^Σ` (S3), needs no atom: it is already PL-expressible as membership in the reflected `L_dom`.") and let the `is_doc` sentence run unbroken.

## OUT_OF_SCOPE

### Topic 1: PL-term dynamics across the arrangement-editing transition family
**Why out of scope**: PD0–PD2 are proved against `→_sh` (K.σ ∪ K.α ∪ K.λ_sh) and are sound there. A deployed system composing this substrate with ASN-0127's layer also takes K.δ/K.μ⁺/K.μ⁻/K.μ~/K.ρ steps, and the stability classes need re-grounding against that larger relation (most claims survive — those steps preserve `Σ.L` per F-PRES, and contraction shrinks `Σ.M(d)`, not `dom(Σ.M)` — but the proof obligations are new). That is a bridging ASN between the two query layers, not an error in this one, which scopes its state class explicitly.

### Topic 2: Evaluation cost model
**Why out of scope**: PC5 proves termination and says nothing about cost — the default view evaluates `is_filtered_J` per result element per BH1 type, and every active-view read recomputes membership against `nullified(Σ)`. A complexity model and indexing discipline for PL evaluation is implementation-facing future work; nothing here depends on it.

### Topic 3: Admission criterion for the ℕ fragment and fold forms
**Why out of scope**: PC6's costs paragraph correctly prices the vocabulary axis (the `count(L_dom)`-parity candidate) and declares fold gaps deliberate, closable fold-by-fold. A principled criterion for *which* ℕ operations and fold accumulators to admit — why `+` and not `×`, what makes a fold form safe — is design work for the successor note that first needs one, not a gap in this note's closure theorem, which is exact for the vocabulary as fixed.

VERDICT: REVISE
