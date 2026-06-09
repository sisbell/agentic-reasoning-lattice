# Review of ASN-0126

## REVISE

### Issue 1: Retraction shape varies per-emit, contradicting one-shape-per-registration

**ASN-0126, Single-source**: "The framework re-expresses retraction as that attributed form: `Emit_R(Σ, d_retr, [r], {(a, δ(1, #a))})` where `[r]` is the single attributing source span (`|F| = 1`) and the targets stay in G — **Binary when one target, Multi when several**."

**Problem**: The note's own central commitment is that "a type K is registered once with one shape" and "The shapes therefore classify *registrations*, not tuples." A registered type R carries exactly one `shape(R)`, and `Sh-conf(R, F, G)` is checked against that single registered shape — not against whichever shape the emitted tuple happens to match. If R is registered Binary, a several-target retraction (`|G| = 2`) fails `Sh-conf` and is inadmissible under `K.λ_sh`. If R is registered Multi, single-target retractions also conform (Multi admits `|G| = 1`) but are not "Binary" in any operative sense. "Binary when one target, Multi when several" describes tuple-shape-matching, which the note elsewhere forbids as a way to determine conformance.

**Required**: State R's single registered shape. To admit variable target counts it must be Multi; then drop the per-emit "Binary/Multi" language and say single-target retraction conforms because Multi subsumes `|G| = 1`.

### Issue 2: Attributed retraction is claimed expressible, but R's registration is deferred to the successor

**ASN-0126, Single-source**: "With that single qualification, the single-source commitment rejects nothing the substrate is *legitimately* asked to express." **Open questions #4**: "Whether the substrate ships any types pre-registered ... or whether every app registers all of its own types."

**Problem**: Under `K.λ_sh`, *every* emit — including the re-expressed retraction `Emit_R(…)` — requires precondition (i): K is registered. The note asserts retraction is re-expressed into an admissible attributed form, but whether R is registered at all is left open in #4. If R is not registered, the framework rejects the `F = ∅` form (deliberately) and also cannot emit the attributed form (precondition (i) fails) — so retraction is not expressible under `→_sh`, contradicting the "rejects nothing legitimate" claim. The positive expressibility claim is therefore not established within this note.

**Required**: Either commit R as a standard registration here (e.g., R registered Multi), or weaken the claim to "the attributed form *is conformant when R is registered*, with R's registration deferred."

### Issue 3: `→_sh ⊆ →` and the import of ASN-0086 lemmas cross a state-arity mismatch left implicit

**ASN-0126, The shape-gated emit**: "Hence `→_sh ⊆ →`, and by induction on derivation length every `→_sh*`-reachable state is `→*`-reachable. ASN-0086's structural lemmas — R0 ... — are quantified over `→*`-reachable states, so they hold at every state this note reasons about."

**Problem**: This note redefines `Σ` to four components `(Σ.C, Σ.M, Σ.L, Σ.registry)` and rewrites every step's frame to carry the registry. ASN-0086's `→` is a relation on *three*-component states, and R0, `a_emit` totality, L-ContiguousPrefix are quantified over three-component `→*`-reachable Σ. A four-component-state relation cannot literally be `⊆` a three-component-state relation, and "every `→_sh*`-reachable state is `→*`-reachable" type-mismatches: the former are four-tuples, the latter three-tuples. The import of R0 (load-bearing for the worked example's "`K.λ_sh` is enabled" and for P4's positive emittability) silently relies on this.

**Required**: Make the projection explicit: define `π(Σ) = (Σ.C, Σ.M, Σ.L)`, show each `→_sh`-step projects to a `→`-step (registry framed, C/M/L identical to a `K.σ/K.α/K.λ` step), conclude `π` maps `→_sh*`-reachable states to `→*`-reachable states, and apply ASN-0086 lemmas to `π(Σ)`.

### Issue 4: Span-count measure rejects coverage-contiguous multi-span sources, unaddressed against the coverage-keyed registry

**ASN-0126, Shape-conformance**: "We count spans, deliberately, because ... a source span is *meant* to be able to cover a range or subtree." **Registration entries**: "Registration is keyed by *coverage class*, not by raw endset."

**Problem**: The note keys *types* by coverage (coverage-invariant, per L8) but measures *F-conformance* by raw span count (coverage-variant). Nelson's sanction is for "a single *span* [covering] a range/subtree" — but an app that presents the same contiguous coverage as two adjacent spans (e.g., a source built from content inserted in two pieces) has `|F| = 2` and is rejected by every shape, despite identical coverage to a conformant one-span F. The note defends span-count only against the `|coverage(F)| = 1` alternative; it never addresses the coverage-equal-but-multi-span case, which is the real edge created by mixing a coverage-keyed registry with a span-count F measure.

**Required**: Either state explicitly that single-source means single-span-as-emitted and the app must coalesce (acknowledging coverage-equal multi-span F is rejected), or make F-conformance coverage-based (single contiguous coverage) to match the coverage-invariant treatment of K. Address the edge rather than leaving it implicit.

### Issue 5: P5 quantifies "for any K" but `Sh-conf` is undefined for unregistered K

**ASN-0126, P5**: "For any K, F, G and any reachable Σ, Σ', `Sh-conf(K, F, G)` evaluated against Σ equals `Sh-conf(K, F, G)` evaluated against Σ'."

**Problem**: `Sh-conf` "is defined only for *registered* K ... For an unregistered K ... `Sh-conf(K, F, G)` carries no truth value." P5's unrestricted "for any K" then asserts equality of two undefined values. The intended content (definedness and verdict both coincide across states because registries are equal by P1) is correct but unstated.

**Required**: Restrict P5 to registered K, and note that registration-status itself is state-independent by P1 so definedness coincides at Σ and Σ'.

## OUT_OF_SCOPE

### Topic 1: Idem operational semantics, behavior catalog, default predicates, standard registrations, composition
**Why out of scope**: The note deliberately commits only the *structural presence* and state-independence of the idem flag and shapes, deferring emit-time idem behavior, predicate catalogs, and composition to a named successor. These are genuinely new territory, not gaps in the structural framework — provided Issue 2 (R as a needed standard registration) is resolved here rather than deferred.

### Topic 2: Multi-source (`|F| > 1`) and arity beyond N=3
**Why out of scope**: The note explicitly directs apps needing multi-source relations to the raw link store (ASN-0043) and flags loosening as a future supplemental note. Not narrowing these is a stated design boundary, not an error.

VERDICT: REVISE
