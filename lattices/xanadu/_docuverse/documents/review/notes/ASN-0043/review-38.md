# Review of ASN-0043

## REVISE

### Issue 1: Link store finiteness axiom missing — L9 and L11b proofs unsound without it

**ASN-0043, L9 (TypeGhostPermission) and L11b (NonInjectivity)**: Both proofs construct a conforming extension Σ' by allocating a fresh link address.

**Problem**: The axioms (L0, L1, L1a, L1b, L3, L5, L6, L12, L14) do not constrain `dom(Σ.L)` to be finite. The set of valid link addresses — element-level tumblers with `fields(a).E₁ = s_L` and `#fields(a).element ≥ 2` — is countably infinite. A conforming state can map *every* valid link address to a link value (each axiom is either a universal over `dom(Σ.L)` that holds regardless, or a transition invariant that is vacuous absent transitions). In such a state, no fresh link address exists, and both proofs fail.

Concrete counterexample for L9: define `Σ.L(a) = (∅, ∅)` for every valid link address `a`. This satisfies L0 (subspace), L1/L1a/L1b (structural), L3 (arity 2 ≥ 2), L5/L6 (definitional), L12/L14 (no transitions, disjointness). Every valid link address is occupied with a binary link. No fresh address can be allocated; no existing entry can be modified (L12); no binary link can become a standard triple. L9's universal-extension claim fails.

Concrete counterexample for L11b: define `Σ.L` as an *injective* mapping from all valid link addresses to distinct link values. Then for any `a ∈ dom(Σ.L)`, no other `a'` satisfies `Σ.L(a') = Σ.L(a)`, and no fresh address exists for extension. L11b's universal-extension claim fails.

**Required**: Add an axiom paralleling S8-fin (ASN-0036):

> **L-fin.** For each reachable system state, `dom(Σ.L)` is finite.

This ensures the set of occupied link addresses is always a finite subset of the countably infinite valid address space, guaranteeing fresh addresses exist. Both L9 and L11b proofs then go through as written — the phrase "prefixes beyond any finite allocation history" (L9) becomes justified, and L11b's allocation of a fresh `a'` succeeds.

The L9 proof itself has a secondary reliance: "by T0(a), node-field components are unbounded, providing prefixes beyond any finite allocation history." With L-fin, "finite allocation history" is guaranteed rather than assumed. Without L-fin, the proof explicitly appeals to finiteness while the axioms permit infinity — a gap between the proof's assumption and the model's constraints.

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage as a general span algebra result

PrefixSpanCoverage — `coverage({(x, δ(1, #x))}) = {t : x ≼ t}` — is a general property of the tumbler arithmetic (it uses only T1, T12, TA-strict, OrdinalShift, and PrefixRelation). It is used here by L9, L10, and L13, but it will also be needed by any future ASN reasoning about span queries over hierarchical address structure. It may belong in a span algebra foundation ASN rather than the link ontology.

**Why out of scope**: This is an organizational question about where to house a general utility lemma, not an error in this ASN. The proof is rigorous and complete here.

### Topic 2: Endset equivalence under coverage

The ASN correctly notes that coverage is a lossy projection: distinct endsets (different span decompositions) may cover the same address set. The open questions list already identifies this: "Under what conditions should two endsets with different span decompositions but identical coverage be treated as equivalent for query purposes?" This is a query-semantics question belonging to a future search/retrieval ASN.

**Why out of scope**: L8 (TypeByAddress) defines type matching via span-set equality, which is well-defined and sufficient for the ontology. Whether a coarser equivalence (coverage equality) should be supported is a query-interface decision.

VERDICT: REVISE
