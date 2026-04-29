# Review of ASN-0047

## REVISE

### Issue 1: K.δ entity hierarchy — prose and formalization diverge

**ASN-0047, K.δ (Entity creation)**: "The address is allocated via inc(·, k) (TA5, ASN-0034) under the parent's prefix."

**Problem**: K.δ's formal definition is `E' = E ∪ {e} where e ∉ E` — no parent entity is required to exist. But the mechanism description says addresses are allocated "under the parent's prefix" via inc, which presupposes a parent. This creates three concrete gaps:

**(a) Bootstrapping.** P4's proof introduces Σ₀ = (∅, ∅, λd.⊥, ∅) with E₀ = ∅. The inc mechanism needs an input tumbler from an existing entity, so K.δ *as described* cannot produce the first node. The formal definition (any fresh `e ∉ E`) permits it, but the mechanism description contradicts this. The ASN should either define the initial state with a bootstrap entity, carve out root creation as a special case, or clarify that the inc description is typical usage, not a precondition.

**(b) Missing hierarchy invariant.** P6 establishes existential coherence for content: `origin(a) ∈ E_doc` for all `a ∈ dom(C)`. No analogous invariant ensures the entity hierarchy is well-formed — that every `d ∈ E_doc` has its parent account in `E_account`, and every account has its parent node in `E_node`. The formal definition of K.δ permits creating document `1.0.1.0.2` without account `1.0.1` existing. The worked example happens to show a consistent hierarchy (E₁ = {1, 1.0.1, 1.0.1.0.1}), but no property enforces this. Downstream ASNs that build on K.δ need to know whether orphan entities are permissible.

**(c) Initial state undefined.** The state model defines Σ = (C, E, M, R) but never formally specifies the initial state. P4's proof introduces Σ₀ inline — it should be part of the state model definition. The choice of initial state determines what states are reachable: with E₀ = ∅ and K.δ requiring inc, nothing is reachable beyond Σ₀ itself.

**Required**: Either (i) formalize the parent requirement as a precondition of K.δ for non-root entities, add a hierarchy invariant (e.g., every entity at level k > 0 has its level-(k−1) prefix in E), define the initial state with at least one root node, and verify P4/P6/P7 base cases against it; or (ii) remove the "parent's prefix" language from K.δ, acknowledge that E is a flat set of valid addresses with no enforced hierarchy, and note that inc is a typical mechanism, not a constraint.

## OUT_OF_SCOPE

### Topic 1: Composite transition atomicity
**Why out of scope**: The ASN defines composite transitions as ordered sequences with invariants required only at the final state. What happens if a composite transition is interrupted mid-sequence (e.g., K.μ⁺ fires but K.ρ does not) is explicitly deferred — "operation atomicity and concurrency" is listed as out of scope.

### Topic 2: Provenance under transitive sharing
**Why out of scope**: The open question about chains of transclusion (document A transcludes from B which transcluded from C) and their provenance implications requires link semantics and transclusion mechanics not yet specified. This is new territory.

### Topic 3: Fork arrangement constraints
**Why out of scope**: J4 constrains ran(M'(d\_new)) ⊆ ran(M(d\_src)) but leaves open whether the fork must copy the entire arrangement or may be a proper subset. This is an operation-specification decision, not a state-transition property.

### Topic 4: Subspace boundaries in reordering
**Why out of scope**: Whether K.μ\~ must respect subspace boundaries (text vs. link subspaces) depends on subspace semantics not yet specified. Acknowledged as an open question.

VERDICT: REVISE
