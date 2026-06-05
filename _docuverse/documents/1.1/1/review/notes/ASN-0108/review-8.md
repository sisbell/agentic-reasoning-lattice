# Review of ASN-0108

## REVISE

### Issue 1: The offset-cursor "weakest precondition" is over-claimed — it is sufficient but not weakest

**ASN-0108, W2 (CursorByIdentity)**: "`wp(resume_offset, R) ≡ |{a ∈ Match(q, Σ') : κ(a) ≤_K κ(c)}| = j` ... **This is the genuine weakest precondition**" (and again: "Even net-count invariance, the genuine weakest").

**Problem**: The condition `j' = j` (writing `j' = |{a : κ(a) ≤_K κ(c)}|`) is not the weakest precondition of `R`. It is too *strong*: it excludes reachable post-states that nonetheless satisfy `R`. Concretely, take the boundary where the cursor's delivered-count exceeds the current match size — reachable under (M-mut) by heavy orphaning. Window 1 delivers `{a_1, a_2}`, so `j = 2`. Between calls `a_1, a_3, a_4, a_5` all orphan, leaving `Match(q, Σ') = {a_2}`, so `m' = 1`. Then:
- `resume_offset` delivers ranks `[3, 4]` of a 1-element set = `∅`.
- `After(a_2, Σ') = ∅` (the cursor `a_2` is the `≺`-max element), so `R`'s target is also `∅`. **R holds.**
- Yet `j' = |{a ∈ Match(Σ') : κ(a) ≤_K κ(a_2)}| = |{a_2}| = 1 ≠ 2 = j`.

So a state satisfying `R` violates the stated condition; the true weakest precondition is the strictly weaker `j' = j ∨ (j ≥ m' ∧ j' ≥ m')` (the past-the-end corner, where both windows are empty). Since a weakest precondition must admit *every* `R`-satisfying state, "`j' = j`" cannot be it. By contrast the identity wp ("`κ(c)` recoverable") *is* exact, because `resume_id` is defined to compute `R`'s target directly — so the asymmetry the section advertises is real, but the offset side is mislabeled.

**Required**: Either restate the offset wp as the genuinely weakest condition including the past-the-end corner, or relabel "`j' = j`" as a *sufficient* (frozen-prefix) precondition rather than "the genuine weakest." The narrative ("offset is hard to discharge over a mutable set") survives either way.

### Issue 2: W5's concrete walk demonstrates the cut-point clause, not the tail-pair-order clause it is labeled as exercising

**ASN-0108, W5 (OrderStability)**: the formal statement gives two independent conditions — (1) cursor discrimination unchanged: "`κ_{Σ'}(c) <_K κ_{Σ'}(a) ⟺ κ_Σ(c) <_K κ_Σ(a)`"; and (2) tail-pair order unchanged: "for every pair `a, b` lying in the tail ... `κ_{Σ'}(a) <_K κ_{Σ'}(b) ⟺ κ_Σ(a) <_K κ_Σ(b)`". The "concrete walk of the tail-order hazard" then relocates `L_2` from key 20 to key 5, and states: "This is exactly a tail-order violation."

**Problem**: In that walk `L_1` (key 10) is the *cursor*, and `L_2` crosses from above to below `κ(L_1)`. Per the formal decomposition this is a violation of clause (1) (cursor discrimination of `L_2` flips: `10 <_K 20` becomes `10 <_K 5` false) — as the walk itself then admits ("crossed below the cursor's cut-point"). It does **not** exercise clause (2), which concerns two links *both remaining in the tail* whose mutual order swaps. That clause is independently necessary and a distinct skip mechanism: with tail `{y, z, w}`, `κ(y) < κ(w) < κ(z)`, delivering `{y, z}` in one window makes the next cursor the batch `≺`-max; if `y, z` swap between calls the next cursor changes from `z` to `y`, and `After(z)` excludes `w` while `After(y)` includes it — `w` is skipped purely from a tail-pair reorder, with no link crossing below a *delivered* cursor in the violating step. The walk asserting it covers "tail-order" therefore leaves clause (2)'s necessity un-illustrated while appearing to discharge it.

**Required**: Either provide a separate concrete walk that isolates clause (2) (two tail links swapping, causing a third link to be skipped), or relabel the existing walk as demonstrating the cut-point/discrimination clause and state clause (2)'s necessity with its own argument.

## OUT_OF_SCOPE

### Topic 1: Multi-document global ordering, mutating-set completeness, cursor-invalidation vs exhaustion disambiguation
**Why out of scope**: These are correctly carried as Open Questions, not as claims. The ASN does not assert guarantees it has not earned (W4 is explicitly conditioned on a fixed `(Match, κ)`; W9/W9a flag the recoverability proviso). No in-ASN claim improperly reaches into count-only or full-set retrieval territory.

VERDICT: REVISE
