The five claims (AX-1, AX-2, S0, S1, S3) form a tight dependency lattice. I read each claim's proof against its stated preconditions and then looked for issues that cross claim boundaries.

**Dependency chain.** S0 is the root axiom. S1 follows in one step (S0 gives both conjuncts; take the first). S3 is proved by induction: AX-1 pins the base state, the inherited case runs through S1 (hence S0), the new-or-redirected case runs through AX-2 directly. The Formal Contracts correctly reflect these at one level of indirection.

**AX-2 well-definedness.** The domain guard `v ∈ dom(Σ.M(d))` in the second disjunct is not logically redundant under the classical reading (the first disjunct already accounts for all `v ∉ dom(Σ.M(d))`), but it is necessary to keep `Σ.M(d)(v)` inside the function's domain before a strict partial-function evaluator reaches the inequality. The prose explanation is correct.

**S3 case split.** "Inherited unchanged" is defined as `v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v)`. Its complement is the disjunction AX-2's guard uses verbatim. The two cases are mutually exclusive and exhaustive over `dom(Σ'.M(d))`. Both are closed: the inherited case uses S1 (which lifts `a ∈ dom(Σ.C)` to `a ∈ dom(Σ'.C)`); the new-or-redirected case applies AX-2 directly, whose guard is satisfied by assumption. The induction is well-founded over finite transition sequences.

**Frame.** S3 quantifies over `dom(Σ'.M(d))`, so positions removed from M across a transition exit the invariant's scope without obligation. AX-2 places no constraint on removals; this is correct and consistent with S3's frame statement.

**S0 forward reference.** The reference to S5 in S0's Formal Contract was already examined and declined: S5 exists in the full ASN. Not re-raised.

One pattern worth flagging:

---

### Reviser-drift sentence in S3's closing paragraph
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S3 (ReferentialIntegrity), closing paragraph — "The earlier reading, that S1 alone forces `a ∈ dom(Σ'.C)` for any mapping established by a transition, conflated these: it assumed precisely the new-reference half that AX-2, not S1, supplies."
**Issue**: This sentence references a historical misreading rather than stating what the current proof says. The preceding sentences already establish the complete picture: S1 covers already-valid references; AX-2 covers new or redirected ones; the content-store invariants are silent on the new-reference half. The "earlier reading" sentence is entirely redundant and looks like a prior review finding's content relocated into the proof rather than removed — the canonical reviser-drift pattern. A fresh reader of the specification has no access to "the earlier reading" and gains nothing from the sentence that the preceding sentences do not already supply.
**What needs resolving**: Remove the sentence. The mathematical argument it was meant to support is already complete in the sentences that precede it.

---

VERDICT: OBSERVE