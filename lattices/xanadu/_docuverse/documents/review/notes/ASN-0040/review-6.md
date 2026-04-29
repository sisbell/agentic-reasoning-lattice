# Review of ASN-0040

## REVISE

### Issue 1: No consolidated formal definition of the baptize operation

**ASN-0040, throughout**: The baptism operation is described operationally ("queries the existing address space for the highest allocated position under a given parent prefix and increments to produce a candidate") and its output is named by B2, but baptize(p, d) is never formally defined as an operation with explicit preconditions, postcondition, and frame condition.

**Problem**: The wp section reasons about `wp(baptize(p, d), B1)` and `wp(baptize(p, d), a ∉ B)`, but "baptize(p, d)" has no prior formal definition. The postcondition `B' = B ∪ {next(B, p, d)}` appears only inside the wp derivation. Preconditions are scattered: B6 (depth validity), B4 (serialization), and the implicit constraint that baptism produces exactly one element. The frame condition (only Σ.B changes) is never stated.

This also obscures B2's logical role. B2 is presented as a "powerful consequence" of B1, but B1's proof relies on the same mechanism B2 names — "queries B for the maximum element of S(p, d) — which is cₘ — and increments by one to produce c_{m+1}." The dependency runs: operation definition → B1 theorem → B2 reformulation (hwm as sufficient statistic). The current order reverses the first two steps.

**Required**: Define baptize(p, d) as a formal operation before B1:
- PRE: B6(p, d); B4 (serialized within namespace); [parent prerequisite deferred per Open Questions]
- POST: Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}
- FRAME: only Σ.B is modified

Then prove B1 as a theorem from this definition + B0 + B0a. Then present B2 as the simplification that B1 enables: since children is always a contiguous prefix, the "query max, increment" mechanism reduces to c_{hwm+1}.

---

### Issue 2: B4 dependency missing from B1 induction and B8 proof

**ASN-0040, B1 section**: "The next baptism in this namespace queries B for the maximum element of S(p, d) — which is cₘ — and increments by one to produce c_{m+1}."

**ASN-0040, B8 section**: "Within the same namespace, B1 ensures sequential, gap-free allocation — the n-th and m-th elements of a sibling stream are distinct for n ≠ m (by S0). Across namespaces, B7 ensures non-overlapping ranges."

**Problem**: B1's inductive step assumes the baptism reads cₘ as the maximum and produces c_{m+1} — this requires that no concurrent same-namespace baptism has altered the state between read and commit. That is precisely B4's guarantee. B4 is not cited in the B1 proof. The wp section later correctly identifies B4 as a dependency (`wp(baptize(p, d), B1) — environmental: B0a, B4`), but the proof that establishes B1 omits it.

Similarly, B8's same-namespace argument claims uniqueness from B1 + S0 without citing B4. Without B4, two concurrent baptisms in the same namespace could both observe hwm = m and both attempt to produce c_{m+1} — the same address, violating B8. B1's maintenance prevents this only because B4 prevents the concurrent observation.

**Required**: Cite B4 explicitly in the B1 induction step (the serialization guarantee that each baptism observes the complete state left by the previous one). Cite B4 in B8's same-namespace case (serialization ensures distinct baptisms observe distinct hwm values, producing distinct stream indices, which S0 maps to distinct addresses).

---

### Issue 3: B5a precondition not discharged for stream elements

**ASN-0040, B5a section**: "Combined with B5, every element of S(p, d) inherits the zeros count established at c₁: `(A n ≥ 1 : zeros(cₙ) = zeros(p) + (d − 1))`"

**Problem**: This universal claim applies B5a inductively to every cₙ in the stream, but B5a has the precondition `t_{sig(t)} > 0`. The ASN never discharges this precondition for stream elements. The argument is straightforward but absent: c₁ = inc(p, d) has final component 1 (from TA5(d)), so sig(c₁) = #c₁ and c₁_{sig(c₁)} = 1 > 0. Each cₙ₊₁ = inc(cₙ, 0) advances the value at sig(cₙ) by 1 (TA5(c)), preserving positivity. By induction, every cₙ satisfies the precondition.

**Required**: State that all stream elements satisfy B5a's precondition, with the brief inductive argument (one or two sentences).

---

### Issue 4: Trace does not verify B₀ conformance

**ASN-0040, "A baptism traced" section**: "Begin with B₀ = {[1]} — a single root node."

**Problem**: The trace asserts B₀ = {[1]} without verifying it satisfies B₀ conformance. The concrete example is meant to ground the formal development; the base case of the B1 induction requires a conforming seed. The verification is simple — [1] is not in any sibling stream (no tumbler p with #p + d = 1 for d ∈ {1, 2} exists), so children(B₀, p, d) = ∅ for all (p, d), which is trivially a contiguous prefix of length 0; and [1] satisfies T4 (single positive component, no zeros) — but it should be stated explicitly to complete the trace's role as a worked base case.

**Required**: Add explicit verification that {[1]} satisfies B₀ conformance before the first baptism step.


## OUT_OF_SCOPE

### Topic 1: Parent prerequisite chain
**Why out of scope**: Whether p must be baptized (p ∈ Σ.B) before children can be baptized beneath it is explicitly deferred to Tumbler Ownership. The ASN acknowledges this as an open question and separates syntactic validity (T4, enforced by B6) from baptismal status.

### Topic 2: Distributed consensus for B4
**Why out of scope**: B4 is a specification-level serialization requirement. How distributed replicas enforce it (consensus protocols, partition handling) is an implementation concern acknowledged in the Open Questions.

### Topic 3: Bulk allocation
**Why out of scope**: Whether a single operation may baptize a contiguous range of k positions atomically is acknowledged as an open question. The current ASN specifies single-element baptism; bulk allocation is a future extension.

VERDICT: REVISE
