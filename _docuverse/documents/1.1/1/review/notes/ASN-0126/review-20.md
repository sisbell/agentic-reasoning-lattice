# Review of ASN-0126

## REVISE

### Issue 1: "register against" contradicts the immutable registry
**ASN-0126, intro / Registry permanence / Open questions #4**: intro promises "a finite shape catalog they can register against"; Open questions #4 asks "whether every app registers all of its own types"; yet Registry permanence states "the registry is fixed at the moment Σ_init is defined" and "There is no notion of altering the registry within a single substrate's evolution."
**Problem**: The note never reconciles *apps registering their types* with an *immutable registry*. If registration is a runtime act, P1 forbids it; if it is a construction-time act baked into `Σ_init.registry`, the note never says so, and "register against" reads as runtime mutation. As written, the central use-case ("apps register against the catalog") has no defined mechanism.
**Required**: State explicitly that all registrations are fixed at substrate construction (entries present in `Σ_init.registry`), and disambiguate "register against" (conformance-check) from "register" (add an entry, which the model does not permit post-init).

### Issue 2: `|·|` overloaded between arity and span count
**ASN-0126, Single-source / The shape-gated emit**: the note writes `|F| = 1` (span count of an endset) and `|value| = 3` (arity of a link value), while ASN-0043 already fixes `|Σ.L(a)|`/`|L|` as *arity* (endset count).
**Problem**: `|·|` now means arity on a `Link` and span-count on an `Endset`. Disambiguation rests entirely on the operand's type, which is not always locally obvious (e.g. `|value| = 3` sits two clauses from `|G| < ∞`). A reader tracking the gate's preconditions must re-derive which measure is in play at each site.
**Required**: Use a distinct notation for span count (the note already coins "span count `|e|`" — pick a non-colliding symbol, or qualify every site), so arity and span count are never both written `|·|` in the same clause.

### Issue 3 (anti-bloat): retraction re-expression is buried under stacked authority rationale
**ASN-0126, Single-source, ¶2**: the structural content is exactly "R is registered Binary; the attributed form `Emit_R(Σ, d_retr, [r], {(a, δ(1,#a))})` has `|F|=1, |G|=1`." Surrounding it: "The single-target form is not a narrowing we impose for convenience; it is what retraction *is*. Nelson confirms retraction 'was designed as a single-target...' his DELETEVSPAN command takes 'the given span' (singular), in pointed contrast to COPY, MAKELINK, and REARRANGE... Gregory confirms the implementation carries a single span at every layer..."
**Problem**: This is essay-length design justification by appeal to authority, not reasoning that advances the claim. The reader must skip three to four sentences of provenance to recover the one-line shape commitment.
**Required**: Reduce to the structural statement plus at most one citation. Move design-intent narrative to a provenance sidecar.

### Issue 4 (anti-bloat): Binary-≠-unit-depth restated four-plus times
**ASN-0126, Single-source, ¶2**: "Binary registration alone, however, does **not** entail ASN-0086's UnitDepthRetractionDiscipline" / "Binary is thus strictly weaker than the discipline's unit-depth requirement" / "Binary registration is therefore *compatible* with the discipline... but does not by itself enforce it" / "the discipline remains exactly where ASN-0086 placed it."
**Problem**: One point — Binary admits non-unit Binary G, so registration does not enforce unit-depth — is asserted four times in different words within a single paragraph.
**Required**: State once, with the single load-bearing reason (a length-`δ(2,#t)` span is Binary-conformant), and delete the restatements.

### Issue 5 (anti-bloat): span-count-vs-coverage divergence duplicated for F then G
**ASN-0126, Shape-conformance, ¶2**: the F-coalescing argument ("a source presenting one contiguous extent as two abutting spans... Gregory confirms udanax-green performs *no* endset coalescing... `spanf1.c`... `orglinks.c`") is then re-run nearly verbatim for Binary's G ("Binary's to-span is therefore subject to the identical span-count-vs-coverage divergence... exactly as for F, and for the same implementation reason: udanax-green stores spans per-emit with no coalescing").
**Problem**: The same divergence, the same app-side coalescing burden, and the same udanax-green justification are stated twice. The second pass adds no new content beyond "this also applies to Binary's G."
**Required**: State the divergence and coalescing rule once over "any single-span shape slot," note that it binds F (all shapes) and Binary's G, and drop the second full restatement and its repeated implementation citation.

### Issue 6 (anti-bloat): meta-prose justifying the wp artifact and the gate/landing split
**ASN-0126, The shape-gated emit**: "The refinement lives in the emit's *precondition*, so the proper depth artifact is the weakest precondition of the gated emit against a non-trivial postcondition — not the assertion that it deposits no non-conforming tuple (that is P4, a corollary)." Also P4: "P4 is the *enablement* half of the gate (enablement vs landing is drawn once in The shape-gated emit)."
**Problem**: The first explains *why* a wp is the right artifact rather than computing it; the second is a cross-reference about where a distinction "is drawn." Both are commentary on the document's own structure, not steps in the argument.
**Required**: Open directly with the wp derivation. Drop the "proper depth artifact" framing and the "drawn once in X" pointer; let the wp and P4 carry the distinction.

### Issue 7 (anti-bloat): repeated deferral to Open questions #4 and duplicated "no free-floating materials" quote
**ASN-0126, Single-source**: the R-standardization question defers to "Open questions #4" in ¶2 and again in the "Two qualifications" paragraph, where Open questions #4 then restates it a third time. Separately, Nelson's "no free-floating materials. No free-floating materials exist" rule is quoted in ¶2 and again at "that exclusion is precisely what Nelson's 'no free-floating materials' rule already forbids."
**Problem**: Multiple sections defer to the same downstream location for the same open point, and the same authority quote is used twice to discharge the same `F = ∅` exclusion.
**Required**: Defer to Open questions #4 once; cite "no free-floating materials" once at the point of first use.

### Issue 8 (anti-bloat): defensive preamble before C0
**ASN-0126, Registration entries**: "We must be careful that well-formedness is not merely a *definition* we could vacuously satisfy by an ill-formed registry. P1... freezes an ill-formed registry... exactly as faithfully as a well-formed one. P1 alone therefore does not make `shape(·)` single-valued..."
**Problem**: A paragraph rehearsing why C0 is needed (rather than what it states) before stating C0. The single necessary observation — P1 freezes contents but does not constrain `Σ_init`'s well-formedness, so single-valuedness needs a separate construction-time commitment — is stretched across several sentences of "we must be careful."
**Required**: Compress to one sentence motivating C0, then state C0.

## OUT_OF_SCOPE

### Topic 1: idem semantics, behavior catalog, predicate composition
**Why out of scope**: Open questions #1–#3, #5 correctly defer operational semantics (idem at emit, behaviors, default/composed predicates) to a successor. This note commits only to structural presence and state-independence of the idem flag, which is appropriate.

### Topic 2: multi-source / higher-arity relations
**Why out of scope**: Open questions #6. The note explicitly scopes itself to `|F| = 1`, `N = 3`, and routes multi-source needs to the ungated ASN-0086 link store. Extending the framework is a supplemental note, not a defect here.

VERDICT: REVISE
