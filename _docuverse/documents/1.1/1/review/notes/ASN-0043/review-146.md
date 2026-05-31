# Review of ASN-0043

I checked the proofs of L1c (CPP-based home identification), FSP/FSE (fresh-sibling conformance and existence), PrefixSpanCoverage (both inclusion directions, including the `k = m` tail sub-case), L9 (Case A constructive chain and Case B via FSE), and the full worked example including the six-step extension. The tumbler arithmetic in every step is correct: `inc(d,2)` and the sibling sweep produce the claimed element fields, the `zeros`-count transitions respect TA5a's bounds, the `#tᵢ > #s` and `k₁ = 2` conjuncts are discharged from the seed-equals-home constraint, and the coverage-equality computation in Step 6 (`[g,g') ∪ [g',h) = [g,h)`) holds.

Boundary cases are covered: empty from/to endsets (L9 witness), arity > 3 (Step 3), type discrimination across disjoint cones (Step 4), multi-span order-irrelevance (Step 5), and distinct decompositions with equal coverage (Step 6) — each exercises a property singletons cannot witness. The state-local invariant set is preserved completely by FSP, with `Σ'.C = Σ.C` / `Σ'.M = Σ.M` legitimately discharging the ASN-0036 obligations verbatim. The ASN defines state (`Σ.L`), invariants (L0–L14a), and stays clear of operations; it has not drifted into implementation mechanics, and citations to ASN-0034/0036 are foundation references. No surviving forward-reference accretion: the most recent prose factors repeated arguments through named lemmas (CPP, FSP, FSE, the subspace-disjointness discharge) rather than duplicating them, and the per-step "fresh sibling" factoring legitimately avoids restating L12/L12a six times.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Global content-subspace constant
**Why out of scope**: The Open Questions already flag that content-side disjointness is scoped to the `s_C`-resident slice rather than all of `dom(Σ.C)`. Fixing a global content-subspace invariant is a strengthening for a future content-side ASN, not a defect here — this ASN correctly states L14/L14a under the explicit `s_C`-residence hypothesis.

VERDICT: CONVERGED
