# Review of ASN-0086

## REVISE

### Issue 1: Observe_K justifies match-decidability by a false finiteness claim

**ASN-0086, Definition — Observe_K, "Pattern domain" paragraph**: "the substrate-level match relation `F̂ ⊆ coverage(F)` remains decidable in `℘_fin(T)` because `coverage(F)` is itself a finite subset of `T` for every finite endset `F` (T12, ASN-0034 + finiteness of `F`)."

**Problem**: `coverage(F)` is **not** finite in general. A single well-formed span covers a lexicographic interval `{t : s ≤ t < s ⊕ ℓ}`, and this interval typically contains infinitely many tumblers. The note proves this itself: PrefixSpanCoverage gives `coverage({(x, δ(1, #x))}) = {t : x ≼ t}` — the entire prefix-subtree of `x`, which is infinite (`x.1`, `x.2`, `x.1.1`, …). R5 and R13 rely on exactly this infinite-subtree coverage. So the cited reason contradicts the note's own machinery. T12 supplies order-convexity and well-formedness, not finiteness; finiteness of `F` (a finite *set of spans*) does not make the *union of their coverages* finite.

The decidability *conclusion* survives, but for a different reason: `F̂` is finite, and each membership test `t ∈ coverage(F)` is decidable (intrinsic span containment via T2), so the finite conjunction `F̂ ⊆ coverage(F)` is decidable regardless of `coverage(F)`'s cardinality.

**Required**: Replace the justification. Decidability of `F̂ ⊆ coverage(F)` follows from `F̂ ∈ ℘_fin(T)` together with per-element decidability of `t ∈ coverage(F)` (T2 intrinsic comparison applied to each of the finitely many spans of `F`) — not from any finiteness of `coverage(F)`, which is generally infinite.

### Issue 2: Duplicated "catalog (a) alone is insufficient" with a deferral forward-reference

**ASN-0086, "Categorical transition relation `↝`"**: "…catalog (b), the chain-discipline catalog, which is the substantive hypothesis (catalog (a) alone is insufficient; see R7a's proof)."

**Problem**: The proposition "catalog (a) alone is insufficient" is asserted here with a forward pointer ("see R7a's proof"), and then established again inside R7a's proof (the `a* = [d.0.s_L.1.1]` argument). One paragraph defers to a downstream location for content that the downstream location then carries in full. This is the "multiple paragraphs defer to the same downstream location" / "prose justifies a hypothesis by a Y argument stated elsewhere" pattern. The `↝` definition should introduce `↝`; the sufficiency argument belongs solely in R7a.

**Required**: Remove the parenthetical rationale and forward pointer from the `↝` paragraph; state only that R7a quantifies over `↝` under the substrate-conformance precondition. Keep the insufficiency argument at its single home in R7a.

### Issue 3: substrate-conforming-layer Definition embeds use-site inventory and granularity rationale

**ASN-0086, Definition — substrate-conforming layer, clause (a)**: "preserved wholesale by any layer whose state-affecting operations compose the substrate's K-operations, since each K-op preserves the entire catalog by its own ASN-0093 contract (R7a discharges preservation at this granularity, not entry-by-entry). L5 (EndsetSetSemantics), L6 (SlotDistinction), and L8 (TypeByAddress) are value-shape commitments on the `Link` record, discharged at every K.λ-step by K.λ's value-shape precondition."

**Problem**: A catalog definition should enumerate *what* the catalog is. The trailing clause instead explains *why/where* it is discharged ("R7a discharges preservation at this granularity, not entry-by-entry") and inventories which specific invariants are discharged at which step — meta-prose that does not advance the definition's meaning and forces the reader past a parenthetical to find the definition itself.

**Required**: Reduce clause (a) to the catalog contents (the L/S/M/C invariant list). Move the discharge-granularity observation, if needed at all, into R7a where preservation is actually argued.

### Issue 4: "Unit-depth retraction discipline" Definition enumerates its downstream consumer

**ASN-0086, Definition — Unit-depth retraction discipline, "Consumption" sub-paragraph**: "The relational layer (defined below) satisfies the discipline by definitional commitment of its `Nullify` alias… this makes 'every `L_R^Σ` tuple was produced by a `Nullify` call' a definitional property of the relational layer…"

**Problem**: The "Consumption" sub-paragraph enumerates who downstream relies on the definition rather than advancing the definition's content — the "definition's introduction enumerates downstream consumers" pattern. The fact that the relational layer satisfies the discipline belongs at the relational-layer Definition (where it is, in fact, also stated), not as a sub-paragraph of the discipline's own introduction.

**Required**: Keep the "Scope" clarification (substrate does not enforce the shape constraint — that is genuine content about the definition). Delete the "Consumption" sub-paragraph; the relational-layer Definition already records the commitment.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs. Observe
**Why out of scope**: The Open Questions correctly defer the consistency model under which `A_K` transitions are observed concurrently with `Emit`. This requires an interleaving semantics the present single-step `→` model does not supply; it is new territory, not a defect here.

### Topic 2: Multi-arity active subsets `A_K^{(n)}`
**Why out of scope**: The note restricts `L_K`/`A_K` to standard-triple links and explicitly cordons higher-arity links off. Extending the active/audit machinery to `|Σ.L(a)| > 3` is future work, not a gap in the arity-3 development.

VERDICT: REVISE
