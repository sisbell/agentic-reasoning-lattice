# Review of ASN-0130

## REVISE

### Issue 1: The merged-span F is not address-denoting — condition (iv), PR1's statement, and the PR5 lint all break on it

**ASN-0130, PR0/PS1**: "a Unary tuple whose F is the merged canonical span over the run, `{(a, δ(n, #a))}`" ... "(iv) every definitional reference in the term is the address of an already-registered definition — some `(b, F, ∅) ∈ A_pdef^Σ` ... with the referenced address in `addrs(F)`."

**Problem**: AD (ASN-0128) defines `addrs(e) = {x : (x, δ(1, #x)) ∈ e}` — it collects starts of *unit-depth* spans only. For a run of `n ≥ 2` values, the span `(a, δ(n, #a))` is not unit-depth, so `addrs(F) = ∅`. Consequences:

- Condition (iv) is vacuously false for every reference to a multi-value definition. No definition longer than one content value can ever be referenced. The note's central mechanism fails on the general case it defines.
- PR1's statement — "the run under `addrs(F)` held a valid encoding" — quantifies over the empty run for `n ≥ 2`.
- PR5's claim that the certification lint "is a one-quantifier PL term over `A_pdef^Σ` and `A_pd_stable^Σ`" is unestablished. The natural spelling `(∀ t ∈ M_pdef :: is_pd_stable(t))` evaluates `M_pdef = ⋃ addrs(F) = ∅` under merged spans — the lint is vacuously ⊤, a false-positive lint that passes while checking nothing. No alternative spelling exists in the vocabulary: `coverage(F)` is an infinite set (it contains all extensions), so it is not a QD domain and cannot be enumerated; V-TUP provides coverage *membership* tests for a given address but no coverage equality between two bound tuples' endsets; and `addr(x)` is the link address, not a run address.

Note also that all three shapes (Unary/Binary/Multi) force `|F| = 1` (ShapeConformance, ASN-0126), so an address-denoting F of n unit-depth spans conforms to no shape — the note cannot fix this by swapping the F encoding alone.

**Required**: Restructure the tuple so the run is recoverable by denotation — e.g., register `pdef` as Multi with `F = enc({a})` (the start, denoting identity) and `G = enc(A_def)` (the run) — or redefine condition (iv), PR1, and the lint on coverage with an explicit start-resolution rule (`referenced address = min(coverage(F))`), and re-derive the lint's PL-expressibility under whichever design is chosen.

### Issue 2: Identity-by-start is not well-defined — injectivity does not give prefix-freeness, and expansion's address-to-term resolution is never specified

**ASN-0130, PR-ENC/PR3**: "An *encoding* is an injective map from PL terms ... to finite content-value sequences, with a decidable parse" ... "identified by its start `a` — *the definition's address*."

**Problem**: Injectivity does not preclude one valid encoding being a proper *prefix* of another. If the encoding of term T₁ (length 3) is a prefix of the encoding of T₂ (length 5), both runs `[a, shift(a,3))` and `[a, shift(a,5))` satisfy conditions (i)–(iv) and both register — two active `pdef` tuples with the *same start address* and different extents (their coverages differ, so I0 dedup does not collapse them). A reference to `a` is then ambiguous between two definitions, and "identified by its start" fails. Separately, PR3's expansion — "replaces each reference by its referent's term" — requires resolving an address to a run extent, then to values, then to a term; the resolution procedure is never stated. It must specify: where the extent comes from (the tuple's span? a self-delimiting parse?), which slice is consulted (the note elsewhere says evaluation works for *de-registered* referents — "PR3 reads content, not registration" — so resolution must read the audit slice or the content itself, which contradicts PR3's own wording "expansion itself reads only *registered*, immutable content"), and how overlapping or mid-run-start registrations are disambiguated. Finally, PR-ENC defines the run via `shift(a, k)` while ASN-0093's K.α chain advances by `inc(·, 0)`; the identity `shift(x, 1) = inc(x, 0)` on T4-valid content addresses (TA5(c)/TA5-SigValid against OrdinalShift) is used silently and should be stated.

**Required**: Strengthen PR-ENC to a prefix-free (self-delimiting) encoding discipline, or have registration reject a run whose start already carries an active `pdef` tuple of different extent. State the expansion's resolution procedure explicitly, including its behavior for de-registered referents, and reconcile PR3's "registered ... content" wording with the de-registration stance. Add the one-line shift/inc identity.

### Issue 3: The emission route is unspecified and the idem=⊤ dedup claim has no operative mechanism

**ASN-0130, PS1**: "Idempotent: re-registering the same run dedups to the existing tuple (I0's coverage identity — the same run is the same definition)."

**Problem**: The exposed `Emit_K` emits canonical encodings only — `F = enc(X_F)`, unit-depth spans (AD, I5, ASN-0128) — so the merged span `{(a, δ(n, #a))}` cannot be presented through it. `register_pred` must therefore deposit via raw `K.λ_sh` (the gate admits it: `|F| = 1`, Unary). But then: (a) I1's dedup contract belongs to the surface operation `Emit_K` "and to it alone" — a raw `K.λ_sh` consults no dedup, so `idem = ⊤` in the registry does nothing for these deposits unless `register_pred` implements its own check, which is nowhere specified; (b) derivations containing `register_pred` deposits are not pdef-surface-emitted (I1a's premise requires every `L_K`-growing step to be an `Emit_K` deposit branch), so I1a's at-most-one-active-per-class uniqueness is unavailable, and PS1's definite article — "*the* existing tuple" — is unsupported. Citing I0 names an identity criterion, not an operation that enforces it. There is also a branch-order contradiction: PR0 says "validate, then classify," and condition (iv) is state-dependent — re-registering a still-active run whose referents were since de-registered fails (iv) under validate-first and is *rejected*, contradicting PS1's claim that re-registration dedups to the existing tuple.

**Required**: Pin `register_pred`'s full contract: the emission route (raw `K.λ_sh` wrapper, à la `Nullify_Binary`), where the dedup check sits relative to validation (and which validation conditions re-run on a potential hit), and the per-class uniqueness invariant the surface maintains, with its proof in place of the I1a citation.

### Issue 4: "Registered signature" and reference application are never defined

**ASN-0130, PR-ENC/PR3/Worked composition**: "a definitional reference types as its referent's registered signature" ... "`evaluate(a, args, view, Σ)`" ... "`gate ≡ quiescent_v1(t) ∧ under_cap(t, 3)`."

**Problem**: Nothing in the note registers a signature. The `pdef` tuple carries no typing data; whether the encoding records the term's context Γ, and in what parameter *order*, is unspecified — yet the worked composition *applies* a referenced definition to arguments (`quiescent_v1(t)`), an application form ASN-0129's PL does not have (PC2 is composition with binder guards; there is no lambda or application constructor). So the note's central syntactic extension — definitional references, possibly applied — has no typing rule (WT must be extended; the new rule and its decidability should be stated), no substitution discipline at expansion (capture/shadowing between the referent's binders and the referencing term's), and no account of how a free-variable term's parameter list is determined from an artifact. `evaluate`'s `args` is likewise never typed. A related precision point: PD0's ST/SF classes are defined on *pure* PL terms, so PR5's certificate strictly classifies the *expansion*, not the artifact's literal spelling — "the certified object and the classified object coincide exactly" needs that qualification (permanence survives, since the expansion is fixed by immutable content).

**Required**: Define the signature of a definition (sorted, ordered parameter context — recorded in the encoding or canonically inferable), state the WT extension rule for (applied) references and the substitution semantics of expansion, type `evaluate`'s arguments, and state that certification classifies the expansion.

### Issue 5: Registration's success postcondition ignores born-nullified deposits, and the note's operations get no wp analysis

**ASN-0130, PR0**: "On success, the surface emits the `pdef` classifier."

**Problem**: Success is implicitly "the definition is registered," and registration's meaning throughout the note is *active* membership — condition (iv) reads `A_pdef^Σ`. But a gate-clearing deposit lands active only when C3 holds (I3, ASN-0128): a pre-existing range retraction whose to-coverage includes `d`'s frontier slot makes the `pdef` tuple *born nullified* (RangeSterilization, ASN-0126) — validation passed, tuple deposited, definition never referenceable. The note neither assumes surface-disciplined derivations (under which DR discharges C3) nor states the caveat. More broadly, the note introduces two operations and derives a weakest precondition for neither — ASN-0126/0128 set the precedent (wp Case 1/2, WP, I6), and the non-trivial case here is exactly "wp(register_pred, the definition is referenceable at Σ')", whose C3 conjunct is the born-nullified condition above.

**Required**: Either scope PR0 to surface-disciplined derivations and cite DR, or add the born-nullified caveat to the postcondition; and supply the wp for `register_pred`'s referenceability postcondition (the `evaluate` precondition — what status the address must have — should be pinned in the same pass).

### Issue 6: PR1's transfer citation does not establish the claim as stated

**ASN-0130, PR1**: "the run's values are immutable (S0) and permanent (S1), both carried to the gated layer's states by ASN-0126's bridge (B2) and onward by RP (ASN-0128)."

**Problem**: B2 transfers *ASN-0086* results whose conclusions are single-state predicates; S0/S1 are ASN-0036 claims, and immutability is a *transition* property, which B2's own scope restriction says transfers only across genuine `→_sh`-steps, one step at a time. The citation as written is the wrong vehicle. The correct chain is short but different: the per-step content clauses of the substrate relation (K.α appends at a fresh key; K.σ and K.λ frame C — C0, ASN-0093, equivalently the restriction clauses in ASN-0086's Reachability definition), carried across gated and extended-record steps by B2's transition-invariant clause and RP-b, then inducted along the derivation from the registering state.

**Required**: Replace the S0/S1-via-B2 citation with the per-step argument plus induction; PR1 is the note's central permanence theorem and deserves the three lines.

### Issue 7: PR2's strict-precedence argument assumes one registration event per definition; the note's own de-registration semantics breaks that assumption

**ASN-0130, PR2**: "condition (iv) forces every definitional reference to name a definition whose registration *strictly precedes* the referencing one: the referent's tuple must be active at the referencing validation, and the referencing definition's own tuple does not yet exist during that validation."

**Problem**: The Standard registrations section permits de-registration, after which the same run can be re-registered (dedup consults the active slice, I2 — a nullified incumbent is invisible, so a fresh tuple deposits). "Registration order" is then a multi-event notion per definition, and PR2's argument — phrased as if each definition has exactly one registration event — no longer defines the order it appeals to. The conclusion survives: at *any* successful registration of D, each referent has *some* earlier successful registration, so reference edges strictly decrease first-registration time and a cycle yields infinite descent among finitely many events; self-reference stays excluded even at re-registration because the prior tuple is inactive and (iv) consults the active slice. But none of this is in the note — the proof must be restated to be robust to the feature the note itself ships.

**Required**: Restate PR2 via the earliest-successful-registration argument (or equivalent minimal-event induction), explicitly covering re-registration after de-registration.

## OUT_OF_SCOPE

### Topic 1: Run-assembly atomicity
A multi-value run is laid down by several K.α steps, each atomic but the sequence not: another writer's interleaved allocation on the same document's content chain fragments the run, and condition (i) then rejects the registration. Soundness is preserved by rejection; the authoring protocol that guarantees contiguity (reservation, single-writer discipline, retry) is operational territory for the protocol layer, not this note.

**Why out of scope**: the note's enforcement point (validation (i)) is correct; how authors avoid tripping it is a liveness concern outside the substrate spec.

### Topic 2: Signature compatibility across supersession lineages
PR4's tip-following consumer evaluates `tip(a₁)` with arguments shaped for v1; nothing constrains v2 to share v1's signature, so lineage-following evaluation can become ill-typed at a version boundary. Whether `supersedes` emissions between definitions should be signature-checked, or mismatch is the consumer's ⊥-analog to handle, is a real design question for a successor note.

**Why out of scope**: version-interface evolution is new machinery beyond the shipped S2 semantics this note deliberately reuses unchanged.

VERDICT: REVISE
