# Review of ASN-0126

## REVISE

### Issue 1: Dangling forward reference "the front end (below)"
**ASN-0126, Single-source**: "discontiguous multi-target retraction falls to the front end (below), never to a gated `→_sh`-step" and "Only *discontiguous* multi-target retraction falls to the front end."
**Problem**: "(below)" promises a section describing what "the front end" does with discontiguous multi-target retraction. No such section exists in this note — the Open questions do not cover it, and no front-end mechanism is defined. The reader is sent to content that isn't there. This is the forward-reference accretion pattern: a deferral to a downstream location that doesn't resolve.
**Required**: Either drop the "(below)" pointer and state plainly that discontiguous multi-target retraction is the app's responsibility (outside `→_sh`), or remove the claim if it is not load-bearing.

### Issue 2: P6's induction is fragmented across two sections
**ASN-0126, Single-source**: "The 'only conforming tuples' conclusion below is inductive, so it needs a base case the gate cannot supply: we commit that the framework's base state carries an empty link store, `Σ_init.L = ∅` … induction over `→_sh`-steps gives … the reachable-state conformance invariant P6 (Properties established)."
**Problem**: This paragraph previews P6's proof and lodges P6's base-state commitment (`Σ_init.L = ∅`) inside the Single-source section. P6 (Properties established) then points *back*: "the base `Σ_init.L = ∅` (Single-source)." The base-state fact and the induction sketch live apart from P6's actual statement, and the two sections cross-reference each other for one argument. `Σ_init.L = ∅` is a base-state commitment that belongs with the other `Σ_init` setup (Registry permanence, where `Σ_init` is defined), not buried in a prose section about F-cardinality.
**Required**: State `Σ_init.L = ∅` once where `Σ_init` is constructed, and give P6 its complete induction in one place. Remove the preview from Single-source.

### Issue 3: wp derivation does not discharge L3 (`K ∈ T_admissible`)
**ASN-0126, The shape-gated emit (Weakest precondition)**: "With added guard `g_sh ≡ K registered ∧ Sh-conf(K, F, G)` and `wp(S, R)` ASN-0086's Case-2 right-hand side … The first two conjuncts are this note's contribution; the remaining three are inherited verbatim."
**Problem**: The underlying `K.λ` step is enabled only when L3 holds, i.e. the type slot is non-empty (`K ∈ T_admissible`). ASN-0086's wp Case 2 presupposes this as `Emit_K`'s operation precondition; it is not one of the three listed conjuncts. The gated wp adds exactly `K registered ∧ Sh-conf` and inherits the three landing conjuncts — but never shows that `K registered ⟹ K ∈ T_admissible`, so the formula silently assumes the type slot is non-empty. That step (registry stores non-empty `K_j`, `coverage(K) = coverage(K_j) ≠ ∅`) is only made later, inside P5's proof. The wp section is not self-contained without it.
**Required**: In the wp section, note inline that "K registered" absorbs `K ∈ T_admissible` (via C0's non-empty stored representative), so no separate conjunct is needed — or list it. As written, the claim "the remaining three are inherited verbatim" understates what enablement requires.

### Issue 4: Coalescing guidance names only "abutting" spans
**ASN-0126, Shape-conformance**: "coalescing abutting spans to that canonical form before emit is the app's responsibility."
**Problem**: A single-span slot rejects every `|F| ≥ 2` value, including *overlapping* or *nested* spans (e.g. `(a, δ(1,#a))` together with `(a, δ(2,#a))`) whose coverage is also contiguous. The app-side coalescing guidance is stated only for "abutting" spans, leaving the overlapping/nested contiguous case unmentioned even though it is rejected identically. The rule `|F| = 1` is unambiguous, but the guidance enumerates an incomplete subset of the cases an app must canonicalize.
**Required**: Generalize the guidance to "any multi-span presentation of a single contiguous extent (abutting *or* overlapping)" so the app obligation matches what the gate actually rejects.

## OUT_OF_SCOPE

### Topic 1: Operational semantics of `idem`, behavior catalog, default predicates
**Why out of scope**: The note's Open questions explicitly defer these to a successor note layering operational semantics. They are new territory (what the substrate *does* with conforming tuples), not defects in the structural framework defined here.

### Topic 2: Whether `Σ_init.registry` ships standard pre-registrations
**Why out of scope**: Open question 4 leaves the standard-registration policy to the successor; the framework correctly treats the registry as a parameter individuating substrates, so this is a future content decision, not an error.

VERDICT: REVISE
