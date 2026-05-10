# Review of ASN-0035

## REVISE

### Issue 1: N8 preservation verification omits N6
**ASN-0035, N8 (Always-Valid Intermediate States)**: "We verify this by enumerating the state-dependent and structural invariants separately."
**Problem**: The enumeration covers N2–N5 (state-dependent) and N9, N10, N16 (structural), but N6 (Structural Ordering) is absent. N6 depends on `Σ.nodes` and the `parent` relation — both modified by BAPTIZE — so it is state-dependent and must be addressed. The DFS-equivalence derivation in the N6 section is structural induction on the tree, meaning N6 holds for *any* finite tree satisfying N3 and N5. Preserving N3 and N5 therefore suffices to preserve N6, but this reasoning must be stated.
**Required**: Add to the N8 verification: "N6 (Structural Ordering): N6 is derived by structural induction on the tree, assuming N3 and N5. Since BAPTIZE preserves both, N6 holds in the post-state without independent verification."

### Issue 2: BAPTIZE freshness postcondition stated without derivation
**ASN-0035, BAPTIZE**: "`n ∉ pre(Σ.nodes)` — the address is fresh"
**Problem**: The text following the postcondition block argues *determinism* ("the new address is uniquely determined") and cites T10a and T9, but does not derive freshness. The derivation requires two steps that are not shown: (a) `n > max(C)` by TA-strict, so `n` is not any existing child of `p`; (b) any `m ∈ Σ.nodes` with `m = n` would have `parent(m) = [n₁, ..., n_{a}] = p`, making `m` a child of `p` and hence in `C` — contradicting (a). Step (b) in particular is needed to rule out collision with nodes under *other* parents. The concrete trace verifies freshness by example but example is not proof.
**Required**: Add the two-step derivation after the postcondition block: (a) `n > max(C)` by TA-strict ⟹ `n ∉ C`; (b) any node equal to `n` is a child of `p` by the definition of `parent` and T3 (CanonicalRepresentation), hence in `C` — contradiction. These two steps close the argument.

## OUT_OF_SCOPE

### Topic 1: Resolution semantics for forward references to unbaptized addresses
N7 establishes that references to addresses like `[2, 3]` are well-formed. What an operation *does* when it encounters such a permanently-empty reference (e.g., COPY from `[2, 3]`) belongs in the operations ASN, not here.
**Why out of scope**: N7 defines syntactic admissibility; operational semantics on empty references is new territory.

### Topic 2: Bootstrap authority for the root node
The genesis state has `Σ.nodes = {[1]}`, but `authorized(actor, [1])` is undefined — no actor is specified as initially authorized for the root. If no actor satisfies the predicate, no BAPTIZE can ever fire and the node tree cannot grow beyond `{[1]}`. The account ontology must ensure at least one actor is initially authorized for `r`.
**Why out of scope**: This is a constraint on the account ontology's definition of `authorized`, not on the node ontology's definition of BAPTIZE.

VERDICT: REVISE
