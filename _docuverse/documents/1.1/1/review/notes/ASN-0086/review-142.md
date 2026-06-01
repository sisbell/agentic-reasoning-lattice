# Review of ASN-0086

## REVISE

### Issue 1: R0 first-emission L1c chain — per-step zero-count bound misattributed to the seed

**ASN-0086, R0 proof, "L-invariant preservation… L1c (LinkAllocatorConformance), First branch"**: "Each step satisfies T10a's per-step admissibility (the `k ∈ {1, 2}` steps within TA5a's zero-count bounds at the document-level seed `d`, where `zeros(d) = 2`)…"

**Problem**: The exhibited chain is `d → inc(d,2) → inc(·,0) → inc(·,1)`. The two `k > 0` steps do **not** both act on `d`. The `k = 2` step acts on `d` (`zeros(d) = 2 ≤ 2`, the tight TA5a bound for `k = 2`), but the `k = 1` step acts on `b_L(d)`, where `zeros(b_L(d)) = 3` (B5: `zeros(inc(d,2)) = 2 + 1 = 3`, preserved by `inc(·,0)`). Its admissibility rests on the *other* tight TA5a bound, `k = 1 ∧ zeros(·) ≤ 3` — evaluated at `b_L(d)`, not at the seed. The justification "at the document-level seed `d`, where `zeros(d) = 2`" cannot discharge the `k = 1` step; both `k > 0` steps sit exactly on their respective TA5a boundaries, so the per-input zero-count is load-bearing and cannot be collapsed onto `zeros(d)`.

**Required**: Discharge each `k > 0` step against its own input's zero-count: `k = 2` at `d` (`zeros = 2 ≤ 2`), `k = 1` at `b_L(d)` (`zeros = 3 ≤ 3`).

### Issue 2: Duplicated T12-well-formedness argument in the Nullify definition

**ASN-0086, Definition — Nullify**: Para 1 — "the to-span `(a, δ(1, #a))` is T12-well-formed for *any* tumbler `a` (since `#a ≥ 1` by T0 and `actionPoint(δ(1, #a)) = #a ≤ #a`), so the underlying Emit_R executes…even when `a ∉ A_rel^Σ`…" Para 2 — "The to-span `(a, δ(1, #a))` is T12-well-formed for *any* tumbler `a` (`#a ≥ 1` by T0, `actionPoint(δ(1, #a)) = #a ≤ #a`), so R0 at `d_retr` emits the retraction triple…regardless of whether `a ∈ A_rel^Σ`…"

**Problem**: Two consecutive paragraphs state the identical claim (T12-well-formedness for any `a`, with the same parenthetical and the same "regardless of `a ∈ A_rel^Σ`" conclusion). The reader works past the repetition to confirm nothing new is said.

**Required**: State the well-formedness-and-execution fact once.

### Issue 3: Arity-3 scope rationale stated twice

**ASN-0086, Definition — Nullify**: "(P2) `|Σ.L(a)| = 3` scopes the downstream active-subset effect to standard-triple addresses (only arity-3 addresses populate some `A_K`), placing higher-arity targets outside Nullify's intended scope." Later: "The arity-3 restriction matches this note's scope. `A_K^Σ` is defined only over standard-triple links…so the active-subset effect of Nullify is meaningful only on arity-3 addresses. Nullifying a higher-arity address…would deposit `a` into `nullified(Σ')`, but no `A_K^{Σ'}` would feel the effect…"

**Problem**: The same scoping rationale (arity-3 because only arity-3 populates `A_K`; higher-arity nullification deposits into `nullified` but has no `A_K` effect) is given twice within one definition.

**Required**: Keep the explicit "higher-arity deposits but no `A_K` effect" account in one slot; let P2 just state the predicate.

### Issue 4: "(b) disambiguates (c)" explanation duplicated between definition and proof

**ASN-0086, Definition — substrate-conforming state** vs. **L-ContiguousPrefix proof**: The definition reads "(b) makes 'the fresh key at `d`' singular, so (c)'s 'occupies exactly chain index `J+1`' is unambiguous rather than open between several keys seeing the same pre-step frontier `J`." The proof restates "clause (b) guarantees a single step deposits at most one fresh key per home — making 'extends the prefix by one chain index' coherent rather than ambiguous between two keys both seeing the same pre-step frontier `J`."

**Problem**: The same load-bearing observation (clause (b) disambiguates clause (c); two keys at one frontier `J` would otherwise be ambiguous) appears in both places in near-identical words. The proof should consume the clauses, not re-derive their interplay.

**Required**: Keep the (b)-disambiguates-(c) rationale at the definition; have the proof cite the clauses without re-explaining them.

### Issue 5: Roadmap inventory in the introduction

**ASN-0086, opening**: "R0–R5 are derived lemmas from ASN-0043 + ASN-0093; R6a/R6b/R6c are the substantive lemmas carrying the *active/audit distinction*… On top of these we define three operations… and prove R7a…; the relational layer's state-affecting behavior is then fixed by its operation set (Definition — relational layer, below)."

**Problem**: A use-site inventory of every downstream label, forward-pointing to where each is proved. It advances no reasoning; the labels are defined in place below.

**Required**: Trim to the one-sentence thesis (relations compose more cleanly than endsets); drop the label-by-label forward inventory.

## OUT_OF_SCOPE

### Topic 1: Substrate-level enforcement of the unit-depth retraction discipline
The note's own Open Questions raise whether `L_R` to-span shape should become a substrate guarantee (a dedicated retraction K-operation). The wp Case 2 result's dependence on the layer-level discipline is correctly scoped here; promoting it to the substrate is a separate ASN.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
The restriction to standard-triple links is deliberate and stated. Defining `L_K^{(n)} ⊆ A_rel × ℘(A)^n` is new territory, not a defect of this note.

VERDICT: REVISE
