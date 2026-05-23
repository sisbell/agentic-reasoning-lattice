# Patch Review of ASN-0094

## REVISE

### Issue 1: No catalog row added for `c_G = *`
**ASN-0094, The Canonical Shape Catalog table**: The patch states "The Sh5 catalog has no row supporting cardinality `*` on G... Sh-conf cannot admit bundled `citation.depends` emissions under the current registration."
**Problem**: The catalog still has no row with `c_G = *`. Existing rows enumerate only `c_G ∈ {0, 1, 0|1}`. The patch's central requirement (admit bundled multi-target emissions) is not implemented.
**Required**: Add a canonical shape row with `c_G = *` (e.g., `(1, *, A_doc, A_doc, ⊤)` or similar) with a stated `t_G` partition and `idem` flag, plus template family.

### Issue 2: No template family for `c_G = *`
**ASN-0094, Per-Shape Template Walkthroughs**: Existing base templates use `to₁` (SlotAccessorTotality at `c_G = 1`). At `c_G = *`, `to₁` is undefined.
**Problem**: Templates `pair_K`, `to_K`, `from_addrs_K`, `to_addrs_K` cannot be mechanically derived for `c_G = *` without re-formulating bodies to use `slot_addrs(G_τ)` as a set (parallel to how Retraction re-formulates F-side templates at `c_F = *`). No such re-formulation is provided.
**Required**: Re-formulated base template family for the new shape, with G-side accessors using membership (`b ∈ slot_addrs(G_τ)`) or set-equality (`slot_addrs(G_τ) = Ĝ`) per the role-specific pattern Retraction's catalog row establishes.

### Issue 3: Backward compatibility for legacy single-target `citation.depends` unaddressed
**ASN-0094, ShapeRegistry Definition**: "Lifetime constancy. `shape` is fixed across the substrate's lifetime; it does not change as states evolve."
**Problem**: Patch requires "Legacy single-target `citation.depends` emissions must remain conformant." Under per-class constancy + lifetime constancy of `shape(·)`, a single registered K has one fixed shape. If `citation.depends` is re-registered at `c_G = *`, legacy single-target tuples (with `|slot_addrs(G)| = 1`) remain conformant only because `match(1, *)` succeeds — but the patch doesn't state this explicitly nor verify Sh1 at the migrated shape against pre-existing tuples emitted under `c_G = 1`.
**Required**: Either explicit argument that `match(1, *)` admits legacy tuples (one sentence), or a migration discipline if pre-patch and post-patch shapes differ.

### Issue 4: Sh1, Sh3, Sh4 preservation arguments not extended
**ASN-0094, Cardinality / Target Domain / Idempotency sections**: Sh1's clause-(c) discharge cites `match(|slot_addrs(G)|, c_G)`; Sh3's clause-(d) discharge cites `slot_addrs(G) ⊆ t_G^Σ`; Sh4's contract clause (i.a) uses Observe_K with a finite G-pattern.
**Problem**: At `c_G = *`, the Observe-then-post-filter procedure in Sh4's contract clause (i.a)/(i.b) needs the same multi-slot over-approximation argument Retraction's `c_F = *` requires (per-element AllocatedAddressAntichain firing across each `y ∈ slot_addrs(G)`). Patch does not state this.
**Required**: Explicit confirmation that the existing multi-slot generalization paragraph in Sh4's contract clause (i.a) — currently written for F-side `c_F = *` — applies symmetrically to G-side `c_G = *`, or a parallel paragraph for G.

### Issue 5: EffectiveWpSimplification interaction with the new shape
**ASN-0094, Corollary — EffectiveWpSimplification**: Step 1 cites Sh1 at `K := R` to pin every prior R-tuple's G-endset to a single unit-depth span (`shape(R).c_G = 1`); Step 2's `K ~ R` case relies on the same `c_G = 1` constraint to force the new emission's G to one span. The corollary's argument is load-bearing for the framework's wp-simplification at Retraction-typed emissions and is consumed by Sh4's induction.
**Problem**: A new shape with `c_G = *` does not modify Retraction itself, but if any K registered at the new shape were `~`-equivalent to R, the corollary would break: Step 2's `K ~ R` case would see `shape(K).c_G = *` instead of `c_G = 1`, and the unit-depth-discipline witness no longer follows from Sh1 + Sh3 alone. The patch's stated registration (`citation.depends` at the new shape) is unlikely to satisfy `~ R`, but no statement excludes it, and the framework's per-class constancy of `shape(·)` makes the coverage-class disjointness a registry-time obligation rather than a runtime check.
**Required**: An explicit statement that the new shape's coverage class is disjoint from `[R]` (`citation.depends` is registered at `c_G = *` only because no R-equivalent K shares the row), preserving EffectiveWpSimplification. Alternatively, a strengthened corollary that holds at every catalog shape with `c_G ∈ {1, *}` by reading Sh1/Sh3 symmetrically on the multi-element G case.

VERDICT: REVISE
