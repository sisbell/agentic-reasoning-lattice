# Review: M1 — Address & Span Algebra (Detailed Design)

I checked the design against ASN-0034/0045/0053, the decomposition's M1 boundary, and the composition contract. M1 is a foundation (no upstream API to mis-call), so the interface-fidelity axis reduces to "leans only on ℕ" — satisfied via `num-bigint`. I traced every owned capability, the arithmetic, both span constructors, the whole span-set engine, and every named seam consumer.

The design is unusually complete and self-aware. I verified the subtle correctness points specifically — and they hold:
- **`subtree_of` width = `shift(p,1)` (advance position `#p`), not `inc(p,0)` (advance `sig(p)`)**: I confirmed `[p, p⊕δ(1,#p))` denotes *exactly* the extensions of `p` (T5), and that `inc(p,0)` over-captures on trailing-zero prefixes — the design's distinction is correct and load-bearing.
- **`merge` guard `separated ⟺ max start > min reach`** and **`intersect` self-guard via `WF`'s `s<r`**: both verified across all five SC cases including the adjacency boundary (equality → merge proceeds / intersect → None).
- **Field-absence ⇒ NO** (T6 b/c/d), **`zeros` as unbounded `usize`** (avoids the count-wrap mis-classification), **`Nat = BigUint`** (T0(a)), **flat zero-agnostic order** (T1/TA-PosDom): all faithful.
- **`parent` as a single structural peel** (not level-coarsening) vs **`document_of` as level-coarsening**: the worked examples are internally consistent and the peel provably preserves T4-validity.

No `[DEFECT]` found: a competent Rust engineer could implement M1 from this document correctly. The items below are genuine but non-load-bearing.

## Revision list

1. **`[SHARPENING]`** In §6's `split` prose, state explicitly that **σ itself must be level-uniform** (S4's precondition — needed so `reach⊖p` shares length `L`), not only `level_compat(start, p)`. The general level gate (§6/Invariants lists `split`) already mandates it, so the document read whole is correct; the split-specific line just abbreviates and could mislead a builder gating in isolation.

2. **`[SHARPENING]`** In §6's `difference` dispatch table, change the Containment(β⊂α) count from "2" to "**1 or 2**" and note that a complement failing `WF` (zero-width, when a boundary coincides) is dropped — matching the "≤2 (S11d)" prose and the `SpanSet` return. As written the table reads as "always 2."

3. **`[SHARPENING]`** Clarify `CanonicalForm`'s serialization story. It's omitted from the serde-required list (`Tumbler/Address/Span/SpanSet/Level`). It works as M7's in-memory dedup key via derived `Hash + Eq` (M7 can hash it into an opaque `LockKey`, and lock collisions are safe since the dedup *decision* uses `Eq`). But if M7 needs an exact/collision-free coverage-class `LockKey` or ever journals it, it must derive `Serialize/Deserialize`. State which.

4. **`[SHARPENING]`** Package the S7 unit-span cover as a function (e.g. `cover(points: &[Tumbler]) -> SpanSet`). The decomposition lists "coverage" as M1-owned; the design gives `hull` plus a *documented recipe* (`union` of `from_endpoints(t, inc(t,0))`). The recipe is concrete and correct, but exposing it spares M6/M8 from re-deriving it.

5. **`[SHARPENING]`** Note that `ElemPos { doc, subspace, ordinal }` models only a **2-component element field**; T4b allows `E(t) ∈ ℕ⁺` of any length ≥ 1. The design already routes the general case through raw `shift`/`validate`, but one line preventing a builder from assuming `elem_addr` is the *only* element-construction path would help.

6. **`[SHARPENING]`** `depth(a) -> Level` returns the hierarchical *level* (an enum), but "depth" conventionally connotes a numeric nesting count. Either rename (`level_of`) or annotate that it aliases `a.level()`.

7. **`[SHARPENING]`** Specify `Tumbler::get(i: Pos)` out-of-range behavior (1-based; `i = 0` or `i > #t`). A panic contract is fine for a low-level accessor, but it should be stated rather than left implicit.

8. **`[SHARPENING]`** `validate(t: Tumbler) -> Result<Address, T4Error>` consumes `t` on the error path (`T4Error` carries only clauses). Note that a caller needing the rejected tumbler back must clone first, or have `T4Error` carry it.

VERDICT: CONVERGED
