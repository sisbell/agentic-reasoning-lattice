# Review of ASN-0086

## REVISE

### Issue 1: Sloppy `℘(A)` notation in R6a's proof

**ASN-0086, R6a proof**: "Recall that `coverage : Endset → ℘(A)` is a pure function on endset values, fixed by the substrate model (ASN-0043, Definition of coverage)"

**Problem**: ASN-0043's coverage definition has codomain `℘(T)` (the full tumbler space), not `℘(A)` where `A` would be the state-dependent address universe `A^Σ = dom(Σ.C) ∪ dom(Σ.L)`. This matters because L9 (TypeGhostPermission) explicitly permits endsets to reference ghost addresses outside `A^Σ`. The proof's logic is correct (coverage is state-independent), but the notation conflates the state-independent `T` with the state-dependent `A`.

**Required**: Replace `℘(A)` with `℘(T)`. Or, if `A` is intended as a shorthand for `T` here, define this explicitly.

### Issue 2: R0a's introductory paragraph reference is cross-cutting

**ASN-0086, R0a proof**: "The induction does not go through directly on the antichain property: in Case 1, sub-case B (below), the existing `a' ∈ dom(Σ.L)` with `home(a') = d` must be placed in the same sibling stream..."

**Problem**: The proof structure has three layers — the sibling-stream invariant (the strengthened claim), the antichain corollary (with Case 1: same home, Case 2: different home), and the induction (with Sub-case A and Sub-case B for the step). "Case 1, sub-case B" mixes these layers; it refers to the antichain corollary's Case 1 needing information from the induction's Sub-case B. A first-time reader has no way to parse this reference until reading the entire proof.

**Required**: Restructure the explanatory paragraph to either reference only the proof structure that has been introduced at that point, or defer this motivation to after the structure is laid out.

### Issue 3: R5's consequence (d) treats provenance as substrate-derivable when it requires convention

**ASN-0086, R5 Consequences (d)**: "*Higher-order predicates.* 'Has τ been retracted?', 'who emitted τ?', 'what tuples target τ?' — all are ordinary observations over `L_K`, evaluated by the same machinery as predicates over documents."

**Problem**: "Has τ been retracted?" is substrate-derivable (check `τ ∈ nullified(Σ)`). "What tuples target τ?" is substrate-derivable (find tuples with τ in coverage of from/to). But "who emitted τ?" is *not* substrate-derivable without a convention — the emitter must have included its own address in `F` at emission time. Emit_K writes `(F, G, K)` to a fresh address with no implicit emitter field; provenance is conventional, not structural. Grouping these three questions as uniformly answerable conflates substrate machinery with caller conventions.

**Required**: Distinguish substrate-derivable predicates from conventionally-derivable ones, or specify what convention "agent provenance" requires.

### Issue 4: Worked Sketch concrete instantiation does not verify Step 1's R5 instantiation against L-invariants

**ASN-0086, Worked Sketch Step 1 (concrete)**: Verifies coverage and prefix-relationships explicitly, but does not walk through L-invariant preservation for the emission of `b₁`.

**Problem**: The schematic Step 1 invokes R0, which itself comes with a 4-step proof verifying every L-invariant. The concrete instantiation could verify L1 (`zeros(b₁) = 3`), L1a (`home(b₁) ∈ dom(Σ_1.M)`), L1b (`#E(b₁) ≥ 2`), L14 (`{b₁} ∩ dom(Σ.C)|_{s_C} = ∅`), and L14a (`{b₁} ∩ ran(Σ.M) = ∅`) at the actual tumbler value `1.0.1.0.1.0.2.2`. Without this, the worked sketch demonstrates the structural cycle but not the invariant-preservation rigor. The note explicitly proves R0 Step 4 with each L-invariant; the example should exercise this concretely.

**Required**: Add invariant-by-invariant verification at the concrete tumbler `b₁`, or state explicitly that the concrete instantiation verifies only set-theoretic claims and defers L-invariant verification to R0's abstract proof.

### Issue 5: The single-tuple-scope argument in Nullify's Definition restricts to `A_rel^{Σ'}` but the unrestricted coverage is wider

**ASN-0086, Nullify Definition, single-tuple scope argument**: "The to-span's coverage `{t : a ≼ t}` is in principle the entire prefix-subtree of `a` within `T`; restricted to `A_rel^Σ = dom(Σ.L)`, however, P3 gives that the only link address with `a` as a prefix is `a` itself..."

**Problem**: The argument is correct that `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`. But the note never addresses what happens at *content* addresses sitting under `a` in tumbler order. If for some implementation reason a content address `c ∈ A_doc^{Σ'}` satisfies `a ≼ c`, that content address would lie in `coverage(G')`. Under Setup, `c` is `s_C`-resident, and `a` is `s_L`-resident, so `a ≼ c` would require `subspace_I(c) = s_L` somewhere — impossible by subspace-distinctness. The note should make this argument explicit (or note it as a corollary of R4) rather than appearing to dismiss content addresses without justification.

**Required**: Either add a sentence noting that `a ≼ c` for `c ∈ A_doc^{Σ'}` is precluded by subspace-distinctness, or generalize the argument to all of `T`, not just `A_rel^{Σ'}`.

### Issue 6: R6c's broader-scope extension argument relies on an unstated invariance of `L_R`/`nullified`/`A_K` under arrangement modifications

**ASN-0086, R6c parenthetical**: "arrangement modifications leave `Σ.L` and `dom(Σ.M)` untouched, so they preserve `L_R`, `nullified`, and `A_K` pointwise"

**Problem**: This is asserted without explicit justification. The invariance does hold — `L_R^Σ`, `nullified(Σ)`, and `A_K^Σ` are functions of `Σ.L` and the state-independent `coverage` function — but the parenthetical does not state this derivation explicitly. A Dijkstra reviewer would want to see: "`L_R^Σ` depends only on `Σ.L`; arrangement modifications preserve `Σ.L`; therefore `L_R^{Σ_arr} = L_R^Σ`" and similar for `nullified` and `A_K`. Three lines, but the chain should be visible.

**Required**: Make the dependency chain explicit in the parenthetical, even if briefly.

## OUT_OF_SCOPE

### Topic 1: Higher-arity links and `L_K^{(n),Σ}`
The note explicitly defers higher-arity (`|Σ.L(a)| > 3`) tuples to future work, with the typed-relation construction restricted to standard triples. The Open Questions section names this. Out of scope here.

### Topic 2: Elevating the sibling-frontier discipline to a substrate-level guarantee
The note acknowledges R0a is discipline-conditional and discusses what tightening Emit_K's specification or the substrate primitive would achieve. The Open Questions section traces the design tradeoffs. This is genuine future work, not a flaw in the present ASN.

### Topic 3: Self-loops via emitter address prediction
A caller who knows the next-available address could construct `F` to self-reference. The substrate doesn't forbid this. Not addressed in the note but is a minor edge case that doesn't affect any of the claims as stated.

### Topic 4: Slice-wise statement of R0, R4, R5 under L14's native scoped form
The Open Questions section poses this explicitly. Reformulating R0/R4/R5 without the Setup hypothesis is genuine future work.

### Topic 5: Concurrent emission, ordering of Observe results, atomicity model
The Open Questions section lists these. Not the scope of the abstract relational substrate.

### Topic 6: Type catalog growth and collision policy
Coordination-free type extension via L9's ghost permissions is identified as an open question.

VERDICT: REVISE
