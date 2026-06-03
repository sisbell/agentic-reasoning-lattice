# Review of ASN-0071

## REVISE

### Issue 1: `vspec`/`iaddrs` reinvent ASN-0058's content-reference machinery without acknowledging the relaxation

**ASN-0071, *The query* and *Resolution***: "A **vspec** is a pair `(d_s, σ)` where `d_s` is a document address... `σ = (u, ℓ)` is a level-uniform V-span confined to the content subspace" and `iaddrs_one(d_s, σ)(Σ) := { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`.

**Problem**: ASN-0058 (foundation) already defines `ContentReference (d_s, σ)` and `resolve(d_s, σ)`. The `vspec` is structurally `ContentReference` with two conditions dropped — (i) `V_{u₁}(d_s) ≠ ∅` and (iii) `#u = m` (depth-match) — and that very relaxation is what produces this ASN's cross-depth (PC-RANGE), empty-source, and deep-anchor (F-DEEP) cases. Similarly `iaddrs` is the set-valued, coverage-tolerant counterpart of `resolve` (which requires full coverage and yields ordered run/width sequences). The note silently introduces both from scratch. It cites ASN-0058 elsewhere (M13, M14, C0a) and even calls PC "the relaxed analogue of ASN-0058's C0a," so it is clearly building on that foundation — but a reader cannot tell whether dropping the well-formedness/depth-match conditions is intentional or an oversight.

**Required**: Define `vspec` explicitly as a relaxation of ASN-0058's `ContentReference` (naming which conditions are dropped and why search requires them dropped), and relate `iaddrs` to `resolve` (set-valued, coverage-tolerant). If the foundation's machinery genuinely cannot be reused, state that; do not present parallel notation as if the foundation did not exist.

### Issue 2: Currency deferral duplicates Open Question 1 (anti-bloat)

**ASN-0071, *Currency: state dependence*** (final sentence): "...the relationship between this current result and the ever-containing relation `R` is deferred (Open Questions)."

**Problem**: Open Question 1 states the identical deferral: "What relationship between FINDDOCSCONTAINING's current-state result and the historical containment relation `R` must the system guarantee?" Two passages defer the same question to the same downstream slot. This is the "multiple paragraphs defer to the same location / two paragraphs say the same thing" pattern.

**Required**: Keep the substantive Currency content (find reads only `E_doc`/`M`, reports current containment, does not consult `R`) and drop the trailing deferral sentence; the Open Question already carries it. One mention suffices.

## OUT_OF_SCOPE

### Topic 1: Relationship between current result and historical `R`; rejection vs. silent filtering; pre/post-contraction invariant

The three Open Questions correctly defer genuinely new territory (provenance-relation linkage, rejection policy, transition-coupling invariants) to future ASNs. No action — flagged only to confirm they are properly scoped out, not gaps in this ASN.

VERDICT: REVISE

The math is otherwise solid: PC, PC-RANGE, and F-DEEP are derived with explicit case splits (depth `#v ≥ #u` vs `#v < #u`, empty vs non-empty source subspace); boundary cases (empty query, partial coverage, cross-depth both directions) are covered with concrete worked scenarios; finiteness and currency are derived rather than asserted.
