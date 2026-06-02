# Review of ASN-0047

I checked the transition model against its foundations and traced the technical core (K.δ entity discipline, the K.μ⁻/K.μ⁺/K.μ~ arrangement transitions, J4 fork, the J0/J1★/J1'★ couplings, and the Class (a)/(b) inductive verification). The mathematical content holds up: the SSGU scoping of GlobalUniqueness, the per-subspace D-SEQ★ derivation (both `m = 2` and `m ≥ 3` cases), the K.μ~-FIX/RANGE arguments, and the multiplicity-preserving fork all check out, and the worked examples exercise the right boundaries (duplicate-I-address source, interior replacement, orphan link, full link-subspace clearance). I could not find a hard correctness gap.

Because this note carries `review-mode.anti-bloat`, the findings below are meta-prose patterns the precise reader must work around. I deliberately avoid the previously-declined territory (ASN splitting, matrix-cell expansion).

## REVISE

### Issue 1: Temporal-scope framing restated across four locations
**ASN-0047, multiple**: The per-state vs. composite-boundary distinction is laid out in (a) the §Extended reachable-state invariants preamble (two paragraphs), (b) the ExtendedReachableStateInvariants definition's two labeled groups, (c) the proof's "Class (a)/Class (b)" preamble, and (d) the P4a definition box — and the worked-example conventions then say "the per-state / composite-boundary temporal-scope distinction is established once, in the *Extended reachable-state invariants* preamble."
**Problem**: A sentence that asserts the distinction is "established once" while itself re-invoking it is the reviser-drift signature for relocated framing. The reader meets the same dichotomy four times before reaching the proof that uses it.
**Required**: State the temporal-scope dichotomy once (the §preamble), and have (b)/(c)/(d) cite it by name without re-explaining what per-state vs. composite-boundary means.

### Issue 2: S3★ definition slot carries use-site compositional reasoning
**ASN-0047, §Generalized referential integrity**: "S3★ alone yields only store *membership*, not equality of subspace identifiers; L0 supplies the second step... the per-branch equality promotes to the universal correspondence over all `v ∈ dom(M(d))` only via S3★-aux (SubspaceExhaustiveness)."
**Problem**: This is a paragraph enumerating which invariant supplies which conjunct of a downstream correspondence — reasoning about how S3★/L0/S3★-aux combine, sitting in the slot where S3★ is defined. It does not advance the meaning of S3★ itself; the reader must skip it to reach the invariant.
**Required**: Move the "subspace-position correspondence" derivation to the single site that consumes it (the S3★ Class (a) discharge already re-derives the same combination), leaving the S3★ definition to state the invariant.

### Issue 3: Defensive "why the guard is needed" clauses on preconditions
**ASN-0047, K.δ case (ii) k = 0**: "No additional freshness conjunct is imposed here — the case-level `e ∉ E` ... reads the current frontier index... which nothing forces, since a sibling of an already-allocated `t` could otherwise collide with a previously advanced sibling."
**Problem**: The trailing "since ... could otherwise collide" is a justification of *why the guard exists* rather than a statement of the precondition. The same pattern appears in the K.μ~ necessity preamble and the J1★ derivation's "A domain-based formulation ... would fail for value replacement" aside. These defensive asides explain a design choice the precondition already encodes.
**Required**: State the guard (`e ∉ E` reads the frontier; FrontierEquivalence discharges it) and drop the collision-rationale clause, or relocate it to a single design-note rather than recurring at each precondition.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content withdrawal
The note's K.μ⁻ contracts only by per-subspace suffix removal; front/interior deletion with compaction (the implementation's `DELETEVSPAN`) is not modeled. This is correctly deferred — it is already an Open Question and DELETE-family operations are named-operation territory.

### Topic 2: One-sided / type-only links (`e₁ ∪ e₂ = ∅`)
Whether K.λ should admit type-only markers is raised as an Open Question; L3 currently requires only `e₃ ≠ ∅`, leaving the from/to endsets unconstrained. Belongs in a future link-semantics ASN, not a revision here.

VERDICT: REVISE
