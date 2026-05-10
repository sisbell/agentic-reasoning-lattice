# Cone Review — ASN-0034/TA5a (cycle 6)

*2026-04-17 19:13*

### TA5a's closing paragraph claims every `inc(·, k)` with `k > 0` introduces a new hierarchical level, contradicting the case `k = 1` result and T4c's definition
**Foundation**: T4c (LevelDetermination) — Postconditions: on the T4-valid subdomain, the hierarchical level of a tumbler is defined by its zero count via the biconditionals `(zeros(t) = 0 ↔ node) ∧ (zeros(t) = 1 ↔ user) ∧ (zeros(t) = 2 ↔ document) ∧ (zeros(t) = 3 ↔ element)`. "Hierarchical structure" body prose (Gregory's confirmation): "When creating a same-type child (DOCUMENT creating DOCUMENT = versioning), `depth = 1`, and no zero separator is introduced."
**ASN**: TA5a, closing prose immediately preceding ∎:
> "The hierarchy enforces this naturally: each `inc(·, k)` with `k > 0` introduces one new hierarchical level, and the address format has exactly four fields with three separators, so at most three child-creation steps can be applied from a node address — three `inc(·, 2)` steps, with `zeros(t) = 0, 1, 2` respectively before each step, each satisfying `zeros(t) ≤ 2`."

And TA5a's own Case `k = 1`:
> "The range of separator positions `#t + 1` through `#t + k - 1 = #t` is empty, so no zero separators are introduced: `zeros(t') = zeros(t)`."

**Issue**: The claim "each `inc(·, k)` with `k > 0` introduces one new hierarchical level" is false for `k = 1` under the ASN's own definitions, and the paragraph then justifies only `inc(·, 2)` steps while still universally quantifying the opening clause over all `k > 0`. Three independent pieces of the ASN pin the contradiction:
  (1) Under T4c, hierarchical level is determined by `zeros(t)` on the T4-valid subdomain, and TA5a Case `k = 1` proves `zeros(t') = zeros(t)` — so `inc(·, 1)` preserves hierarchical level rather than introducing a new one.
  (2) The "Hierarchical structure" body identifies `depth = 1` as same-type child / versioning with no zero separator, i.e., no new level.
  (3) The paragraph's own concrete count — "three `inc(·, 2)` steps" — tallies only the `k = 2` branch; the `k = 1` branch is silently dropped from the enforcement mechanism, even though the opening clause asserted it does introduce a level.

The effect is that TA5a's motivating prose presents an incorrect semantic reading of the theorem's content: it conflates "the iff bound tightens as `k` grows" (true) with "every positive `k` introduces a level" (false at `k = 1`), and the conflation crosses the boundary between TA5a's T4-preservation guarantee and T4c's level-determination definition. A downstream reader asked to justify why `inc(·, 1)` is admissible under T4 for *any* `zeros(t) ≤ 3` would, following this paragraph, incorrectly conclude that `inc(·, 1)` consumes a hierarchical level and therefore should be constrained to `zeros(t) ≤ 2`, matching `inc(·, 2)`.

**What needs resolving**: TA5a's closing paragraph must either (a) distinguish the `k = 1` case (same-level, versioning, no new separator, `zeros(t') = zeros(t)`) from the `k = 2` case (new separator, new level, `zeros(t') = zeros(t) + 1`) so that the "introduces one new hierarchical level" claim is restricted to the branch where it actually holds, or (b) be restated in terms that do not reference hierarchical level at all — e.g., framing the tighter `zeros(t) ≤ 2` bound for `k = 2` as a consequence of introducing a new zero separator rather than of introducing a new level — so that the motivation does not cross into T4c's territory while asserting something T4c's definition refutes.
