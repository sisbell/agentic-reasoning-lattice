Tracing the dependency graph and proof steps carefully before reporting.

**AX-2** — The domain guard on the second disjunct is correctly placed. The application `Σ.M(d)(v)` in the inequality is guarded by the explicit `v ∈ dom(Σ.M(d))` conjunct preceding it. The claim that "classically the guard adds nothing" is accurate: the first disjunct exhausts `v ∉ dom(Σ.M(d))`, so the OR can only be satisfied via the second disjunct when `v ∈ dom(Σ.M(d))` holds, making the guard redundant classically but load-bearing under the strict partial-function reading. The Formal Contract matches the formula.

**S0** — Axiom. The contract correctly names itself a root posit and identifies S1 and S3 (and S5, handled by the declined prior finding) as dependents. No issue.

**S1** — One-step proof: S0 gives `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` for any `a ∈ dom(Σ.C)`; the first conjunct delivers `dom(Σ.C) ⊆ dom(Σ'.C)` by universal instantiation. Correct. Forward reference to GlobalUniqueness is correctly classified as non-load-bearing in S1's proof chain.

**S3** — Induction on reachability from `Σ₀`. Base case: AX-1 empties `dom(Σ₀.M(d))`, so the quantifier range is empty and S3 holds vacuously. Inductive step: fix `d`, `v ∈ dom(Σ'.M(d))`, `a = Σ'.M(d)(v)`. The case split is exhaustive by excluded middle — either `v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v)` (inherited) or not (new/redirected). Inherited case: J0 yields `a ∈ dom(Σ.C)`, S1 carries it to `dom(Σ'.C)`. New/redirected case: AX-2's precondition is exactly `v ∈ dom(Σ'.M(d))` conjoined with the non-inherited disjunction, and its consequent is `Σ'.M(d)(v) ∈ dom(Σ'.C)`. Both cases close. The dependency declared in the Formal Contract (AX-1, AX-2, S1) matches what the proof actually uses. The closing remark on orphaned content correctly identifies itself as outside the proof.

---

### AX-1 body explains why the axiom is needed, not what it says

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: AX-1 (InitialEmpty), body paragraph — "We are not deriving this from anything; we are fixing the starting configuration. The point of naming it is methodological: an invariant on M proved by induction on transitions needs an explicit, citable anchor for its base case, and the empty base state is that anchor — the configuration on which every such invariant holds vacuously, there being no mapped position to witness a violation."
**Issue**: The paragraph explains the methodological role of AX-1 (why a named empty base state is needed for induction) rather than elaborating what the axiom states. The axiom's content is complete in the preceding formula. The Formal Contract already marks it as "a protocol design posit on the designated start state." The body paragraph is use-site inventory for an axiom — the specific reviser-drift pattern the review instructions flag.
**What needs resolving**: Condense or remove the methodological paragraph from the axiom body. The citable-anchor role is already evident from S3's Depends entry, which names AX-1 and states exactly the base-case function it serves.

VERDICT: OBSERVE