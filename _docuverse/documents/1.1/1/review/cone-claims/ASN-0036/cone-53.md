Reading through the ASN as a whole system — tracing each precondition chain across claim boundaries and checking the inductive structure end-to-end.

**S1 proof.** One-step derivation from S0: S0's consequent `a ∈ dom(Σ'.C)` is the first conjunct needed, and universalizing over `a ∈ dom(Σ.C)` gives subset inclusion directly. Sound.

**S3 base case.** AX-1 gives `dom(Σ₀.M(d)) = ∅` for every `d`, so the quantifier range is empty and the invariant holds vacuously. ✓

**S3 inductive step.** Fix `d` and `v ∈ dom(Σ'.M(d))`. The case split on "inherited unchanged vs. not" is an exhaustive binary partition by excluded middle. Inherited case: `v ∈ dom(Σ.M(d))` is in scope for the IH, S0's consequent gives `Σ.M(d)(v) ∈ dom(Σ.C)`, S1 lifts to `dom(Σ'.C)`. New/redirected case: the disjunctive condition matches AX-2's range guard exactly (with `v ∈ dom(Σ'.M(d))` established before the case split), so AX-2 yields `Σ'.M(d)(v) ∈ dom(Σ'.C)` directly. Both cases close. ✓

**AX-2 well-definedness argument.** The domain guard `v ∈ dom(Σ.M(d))` in the second disjunct prevents `Σ.M(d)(v)` from being evaluated outside its domain under the strict partial-function reading. The note that "classically the guard adds nothing" is accurate — in classical logic the first disjunct already handles `v ∉ dom(Σ.M(d))`; the guard is there for the tool-level obligation. ✓

**Dependency graph.** AX-1, AX-2, S0 are axioms with no dependencies. S1 depends only on S0. S3 depends on AX-1, AX-2, and S1 (which in turn depends on S0). No cycles, no missing links between cited dependencies and the proof steps that invoke them.

---

### S1 Forward References entry misclassifies an external prose citation

**Class**: OBSERVE
**Foundation**: N/A (foundation ASN, internal consistency only)
**ASN**: S1 (StoreMonotonicity), Formal Contract — Forward References: *"GlobalUniqueness (GlobalUniqueness, ASN-0034) — cited as the consolidated guarantee that each fresh address allocated in a new transition is unique across the system, the same uniqueness fact S4 and S7 invoke; not used in S1's proof, whose single step is S0"*
**Issue**: The Forward References slot in a Formal Contract is the place to record downstream intra-ASN claims that depend on this claim's result. GlobalUniqueness belongs to ASN-0034, which is a *declared upstream dependency* of this ASN — it is not a forward reference at all under either the intra-ASN or temporal reading. What the entry actually documents is that S1's preamble prose cites GlobalUniqueness but the proof does not; that is a prose-citation disclaimer, not a forward dependency pointer. The actual downstream claim that depends on S1 (S3, which cites S1 in both its Depends list and its inductive step) is absent from this section. A tool that walks Forward References as a dependency graph would either add a spurious S1 → GlobalUniqueness arc or miss the S1 → S3 arc entirely.
**What needs resolving**: Move the GlobalUniqueness prose-citation note out of Forward References (or annotate it explicitly as a prose-only citation not constituting a structural dependency) and add S3 — and any other intra-ASN claims that depend on S1's result — to the Forward References list.

---

VERDICT: OBSERVE