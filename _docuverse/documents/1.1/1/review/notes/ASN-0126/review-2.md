# Review of ASN-0126

## REVISE

### Issue 1: Single-source `|F| = 1` blocks ASN-0086's Nullify and contradicts the "rejects nothing" claim

**ASN-0126, Single-source / Shape-conformance**: "The single-source commitment captures every observed pattern and rejects nothing the substrate is asked to express" — and the pattern list includes "retractions."

**Problem**: ASN-0086 defines `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` — the retraction tuple has **empty from-set** (`F = ∅`, `|F| = 0`) with the target in `G`. RetractionDirectionality explicitly permits an empty from-set ("left empty for unattributed retractions"). Every shape here requires `|F| = 1`, so `Sh-conf(R, ∅, {(a, δ)})` fails for all three shapes. Under `→_sh`, the only `L_R`-growing step `K.λ_sh` is therefore **disabled for Nullify**: P4 silently makes ASN-0086's retraction mechanism non-emittable. The note both lists "retractions" as single-source-captured and disables the substrate's actual retraction operation. The universal claim is false against the substrate's own vocabulary.

**Required**: Reconcile explicitly. Either (a) acknowledge retraction is being re-modeled from a G-targeting Nullify into an F=1 Unary marker (then state that ASN-0086's literal Nullify/`L_R`/`nullified` machinery is no longer expressible under `→_sh`, and how `nullified` is redefined), or (b) admit a zero-source case for the retraction type. As written, "rejects nothing the substrate is asked to express" must be retracted or qualified.

### Issue 2: `Sh-conf` is undefined for unregistered types — P4 is ill-defined for them

**ASN-0126, Shape-gated emit / P4**: "`K.λ_sh` is `K.λ` with the added precondition `Sh-conf(K, F, G)`" and `Sh-conf` "depends only on the tuple's span counts ... and the shape recorded for K in the registry."

**Problem**: In ASN-0086 the type slot ranges over all of `T_admissible` (any non-empty endset), but the registry records only finitely many. For a `K` with no registry entry, `shape(K)` is undefined, so `Sh-conf(K, F, G)` is undefined and `K.λ_sh`'s precondition has no truth value. The note never says emits are restricted to registered types. P4 ("No `→_sh`-step extends `dom(Σ.L)` with a tuple for which `Sh-conf` fails") is therefore ill-defined precisely on the unregistered case — does an unregistered emit fail, succeed unchecked, or is it inadmissible?

**Required**: State the precondition for unregistered `K` — most likely add "K is registered" to `K.λ_sh` (every emit must name a registered type), and adjust P4/the worked illustration accordingly. Without this the refined relation is not fully defined.

### Issue 3: Registry keyed by raw endset vs. coverage class — conflicts with ASN-0086 TypeEquivalence

**ASN-0126, Registry permanence / P2**: "A type K's shape is a function of K alone — `shape(K)` is well-defined without reference to state ... the same K cannot carry one shape at Σ and another at Σ'."

**Problem**: ASN-0086's TypeEquivalence (lifting L8) identifies types by coverage: `K ~ K' ≡ coverage(K) = coverage(K')`, and ASN-0086 treats the type subscript as a coverage-class index (`L_K = L_{K'}` for `K ~ K'`). This note keys the registry on "K" without saying whether the key is a raw endset or a coverage class. If raw endsets, two coverage-equal endsets `K ~ K'` could be registered with *different* shapes, so `shape(·)` is not a function of the type (the coverage class) and contradicts ASN-0086's identification — at emit, lookup by which `K`? The well-definedness P2 asserts is not established.

**Required**: State that registration is keyed by coverage class `[K]` (or that the registry must assign `~`-equal endsets identical entries), and that `shape`/`idem`/`Sh-conf` respect `~`. This is required for P2/P3 to be true rather than asserted.

### Issue 4: ASN-0086 lemmas are imported into `→_sh` without establishing the reachability inclusion

**ASN-0126, Shape-gated emit / Worked illustration**: "All reachability in this note is with respect to `→_sh`," yet the illustration relies on a "fresh address" (ASN-0086 R0/`a_emit`) and PrefixSpanCoverage, all proven over `→*`-reachable states.

**Problem**: ASN-0086's structural lemmas (R0, a_emit totality, L-ContiguousPrefix, etc.) are quantified over `→*`-reachable states. The note works in `→_sh`-reachable states without observing that `→_sh ⊆ →` (each `K.λ_sh` step is a `K.λ` step plus a precondition), hence `→_sh`-reachable ⊆ `→`-reachable, which is what licenses importing those lemmas. The transfer is sound but unstated; a rigorous note must show the inclusion before using `→`-domain results.

**Required**: Add one line establishing `→_sh ⊆ →` and therefore `→_sh*`-reachable ⊆ `→*`-reachable, so ASN-0086 properties apply at every state this note reasons about.

### Issue 5: Cross-ASN reference by number to a non-foundation ASN

**ASN-0126, Open questions 5**: "Retired ASN-0095's territory."

**Problem**: Standard 7 — ASNs are self-contained; references by number to non-foundation ASNs are flagged. ASN-0095 is not a foundation ASN.

**Required**: Remove the numbered reference or describe the territory ("predicate-composition rules") without citing the retired ASN by number.

## OUT_OF_SCOPE

### Topic 1: idem-flag operational semantics
The flag's role in well-formedness, nullification, and re-emission is explicitly deferred to a successor note. Committing only to its structural presence and state-independence (P3) is legitimate here; the semantics are correctly future territory.

### Topic 2: multi-source (`|F| ≥ 2`) and richer arity
Deferred to a supplemental note. Narrowing to `|F| = 1` now and loosening later is a reasonable scoping decision, not an error — provided Issue 1 (the `|F| = 0` retraction case) is resolved, since that is not "richer arity" but an existing substrate operation.

META: (none — the note defines abstract state, a refined transition, and state-independent invariants; it is incomplete and mis-reconciled with ASN-0086's retraction, not drifted from specification territory.)

VERDICT: REVISE
