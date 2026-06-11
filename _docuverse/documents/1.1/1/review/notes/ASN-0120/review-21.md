# Review of ASN-0120

This ASN is in strong shape. The core technical apparatus — the `wf` predicate, the confinement argument via T5, the recovery equation on `F` rather than the store, the merge legality argument via TA5-SigValid/TS3/S3, the K.μ⁺_L precondition discharge at the intermediate state, and the two-fact wp derivation for ML9 — is carried through with the per-step citations the foundations demand, and I verified each chain against the cited contracts (the T5 prefix-confinement instantiation, the LP-Fin Corollary traces at `n = 1` and `n > 1`, the `aₖ = shift(a₁, k−1)` induction including its `k = 1, 2` base cases, the J0/J1★/J1'★ vacuity arguments, and both branches of Fact (b) including the `d' = d` boundary). The worked example genuinely exercises ML0, ML1, ML2, ML5/ML9 symmetry, and the negative home case. Two gaps remain.

## REVISE

### Issue 1: ML9's future-state consequence cites only half its premises
**ASN-0120, "The invariants MAKELINK preserves," closing sentence of ML9**: "And by ML1's stable store trace, the link can become discoverable from a new document only by that document's arrangement reaching the *originally resolved* content."

**Problem**: This quantifies over all later states `Σ''`, but the named premise — ML1's stable *content*-store trace (`coverage(e_j) ∩ dom(Σ''.C) = ρ(R_j, Σ)`, via LP19a) — covers only half the test. By LP12 at `Σ''`, discoverability consults `coverage(eᵢ) ∩ ran(Σ''.M(d''))`, and by S3★ the range lies in `dom(Σ''.C) ∪ dom(Σ''.L)`. The claim therefore also needs `coverage(eᵢ) ∩ dom(Σ''.L) = ∅` *at every later state*. Fact (a) establishes that exclusion only at the immediate post-state `Σ'` ("LP-Sub at Σ'", "every element of dom(Σ'.L)…"). The materials for the lift are all present — `dom(Σ''.L)` decomposes into `dom(Σ'.L)` (excluded by Fact (a)) plus later fresh K.λ allocations (excluded by LP19a, which the ASN's own stability sentence already states for "any address freshly allocated at any later state" without drawing the link-store conclusion) — but the chain is never assembled, and as cited the consequence does not follow from "ML1's stable store trace" alone.

**Required**: Either state the link-store exclusion uniformly — one or two sentences noting that every `F`-address in `coverage(eᵢ)` carries `subspace_I = s_C` (a property of the fixed endset value, LP-Fin Corollary) while every element of `dom(Σ''.L)` is an `s_L`-subspace `F`-address (LP-Sub and L0, both per-reachable-state invariants), with later allocations independently excluded by LP19a — and cite that exclusion alongside the stable content trace in the closing sentence; or restrict the closing sentence to the immediate post-state.

### Issue 2: the empty from/to-resolution boundary is determined by the contract but never stated, and the body is in tension with itself about it
**ASN-0120, "What the endset arguments name…" (postcondition and `wf`), "Three endsets…" (ML5 paragraph: "The degenerate one-sided case is consistent — when there is no meaningful from, the first endset alone designates what is pointed at"), and Open Questions ("Under what conditions, if any, may the resolution ρ(R, Σ) legitimately recover an empty set for the from or to endset…")**

**Problem**: `enabled(makelink) ≡ d ∈ dom(Σ.M) ∧ (A i : wf(R_i, Σ)) ∧ ρ(R₃, Σ) ≠ ∅` does not exclude `ρ(R₁, Σ) = ∅` or `ρ(R₂, Σ) = ∅` — a case that arises on any well-formed spec over deleted or vacuous positions, and one the mandatory boundary list (MAKELINK with empty endsets) requires the ASN to walk. The contract in fact fully determines the behavior: with `ρ(R_j, Σ) = ∅`, no canonical span can be rooted in the resolved set, so the recovery equation forces `e_j = ∅` as the unique admissible record; K.λ's L3 precondition still holds (only slot 3 is constrained non-empty); and the slot contributes nothing to ML9's existential. None of this is stated. Worse, the body points in two directions: the ML5 paragraph asserts the one-sided case "is consistent," while the first Open Question asks whether empty resolution "may legitimately" occur at all — leaving the reader unable to tell whether the operation is defined on such input. Relatedly, the discharge of K.λ's `e₃ ≠ ∅` from the ML6 precondition is left implicit; the one-step chain (`coverage(e₃) ∩ F = ρ(R₃, Σ) ≠ ∅`, and `coverage(∅) = ∅`, hence `e₃ ≠ ∅`) is never written down, though it is what makes the precondition sufficient rather than merely necessary.

**Required**: Add the boundary case to the body: state explicitly that empty from/to resolution is admitted (or strengthen `enabled` to exclude it — pick one), that the recovery equation then forces `e_j = ∅`, that L3 is satisfied because only the type slot is constrained, and that the empty slot is inert in ML9's wp; include the explicit one-step discharge `ρ(R₃, Σ) ≠ ∅ ⟹ e₃ ≠ ∅`. Then rephrase the first Open Question so it concerns only the *meaning* of an empty non-type endset, not the operation's definedness, and reconcile it with the ML5 "degenerate one-sided case" sentence.

## OUT_OF_SCOPE

### Topic 1: Endset arguments referencing the link subspace (link-to-link endsets)
**Why out of scope**: `wf` deliberately confines specs to `subspace(u_j) = s_C`, and the ASN's second Open Question already reserves the link-subspace case; specifying resolution through link-subspace arrangement positions (CL-OWN/CL-UNIQ territory) is new machinery for a future ASN, not an error here.

### Topic 2: Direct I-address endset arguments (ghost and foreign endsets)
**Why out of scope**: The ASN correctly notes that reaching addresses outside the content store requires a different argument shape that bypasses V-span resolution (the full generality of L4/L9). That argument shape is a distinct operation surface, properly deferred.

### Topic 3: Link deletion by the owner
**Why out of scope**: ML7's parenthetical correctly scopes MAKELINK's guarantee to "no one else's edit can break it"; whether and how an owner withdraws a link is a separate operation (cf. retraction machinery in ASN-0086) and belongs to its own ASN.

VERDICT: REVISE
