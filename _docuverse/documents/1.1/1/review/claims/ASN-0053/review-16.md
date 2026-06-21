Reading the ASN as a system, the per-claim algebra is largely sound and the precondition chains into ASN-0034 (WF→D1/TumblerSub, S5→TA-assoc/TA-LC, S4→T12/WF) hold up. I found one correctness/consistency defect and two framing observations.

### S7 main-body grounds infinitude in T0(b), contradicting its own canonical block
**Class**: REVISE
**Foundation**: T0(b) (UnboundedLength) — postcondition is purely existential: "For every n ∈ ℕ with n ≥ 1, there exists t ∈ T with #t ≥ n." T0 (CarrierSetDefinition) — comprehension supplies membership of every finite ℕ-sequence of length ≥ 1.
**ASN**: S7 (CoveringExistence). The running-prose proof states: "Thus every extension lies in [s, reach(s, ℓ)) = ⟦(s, ℓ)⟧, and **by T0(b) there are infinitely many of them**." The formal-contract block for the same claim states the opposite: "writing s.0ⁿ ... each s.0ⁿ ... lies in T **by T0's comprehension axiom** ... (The membership of each extension is what is load-bearing here; the existential UnboundedLength claim T0(b) ... is **not what we invoke**.)"
**Issue**: T0(b) asserts only that *some* tumbler of length ≥ n exists; it says nothing about the specific extensions s.0ⁿ of this s, nor that they lie in T, nor that there are infinitely many of them. The infinitude of {s.0ⁿ} is grounded only by T0's comprehension (each s.0ⁿ ∈ T, lengths #s+n pairwise distinct). The main prose therefore cites the wrong foundation, and the two copies of S7 in the document directly contradict each other on which axiom is invoked. A downstream consumer reading the running prose gets an unsound justification and a spurious T0(b) edge.
**What needs resolving**: Reconcile the running-prose S7 with its formal-contract block — replace the "by T0(b)" citation with the T0-comprehension + ℕ-infinitude argument (s.0ⁿ ∈ T for all n, pairwise distinct lengths), and remove the dependence on T0(b) for infinitude.

### S1/S3 invoke the total order directly but omit T1 from their dependency lists
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder) — supplies `<`, `≤`, and the totality that makes max/min over tumblers well-defined.
**ASN**: S1 (IntersectionClosure) depends only on S6, WF; S3 (MergeEquivalence) depends only on S6, WF. Both proofs reason "by the total order alone," define `s' = max(start(α), start(β))` / `r' = min(reach(α), reach(β))`, and case-split on `<`/`=` of boundary tumblers.
**Issue**: The order relation and the max/min these proofs manipulate are T1's, yet T1 is not in either depends list (S0, by contrast, lists T1 directly). T1 is reachable transitively via WF, so soundness is not at risk, but the dependency DAG is incomplete for claims that invoke the order in their own right.
**What needs resolving**: n/a (OBSERVE) — optionally add the direct T1 edge for S1/S3 to match S0's treatment.

### S11d table labels the containment bound "2 spans" while the difference column reads "at most 2"
**Class**: OBSERVE
**Foundation**: n/a.
**ASN**: S11d (GeneralDifferenceBound), table row "(iv) Containment (⟦β⟧ ⊂ ⟦α⟧) | at most 2 spans | **2 spans** | S11".
**Issue**: The "Difference" cell correctly says "at most 2 spans" (cases (a)/(b)/(c) of S11 yield 0/1/2), but the "Bound" cell says "2 spans," which reads as exactly-2 rather than the tight upper bound. The surrounding text ("achieved only in the containment case") clarifies intent, so this is cosmetic.
**What needs resolving**: n/a (OBSERVE).

VERDICT: REVISE