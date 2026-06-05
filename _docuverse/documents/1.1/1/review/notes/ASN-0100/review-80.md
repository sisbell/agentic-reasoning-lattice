# Review of ASN-0100

## REVISE

### Issue 1: Atomicity over-claims that intermediate states are unobservable

**ASN-0100, Atomicity and Canonical Order**: "External observers see the composite boundary; the intermediate states are not externally observable."

**Problem**: The proof establishes — correctly and at length — that every intermediate of the decomposition is a *reachable state satisfying the per-state invariants*, and that boundary properties hold at the boundary. That is the abstract guarantee, and it is complete on its own. The added claim that intermediates are "not externally observable" is asserted, not proven, and is in direct tension with the ASN's own Open Question: "What must [an implementation] guarantee to recover canonical order after a partial failure *during* the substrate composite?" — which presumes intermediates are real, exposable states. Unobservability is an implementation-level property the abstract spec neither needs nor can discharge.

**Required**: Drop the unobservability assertion (and the parallel "the intermediate states are not externally observable" framing). State only what is proven: each intermediate is invariant-preserving; boundary couplings discharge at the boundary. Whether a runtime exposes intermediates is the partial-failure open question, not a fact this ASN establishes.

### Issue 2: INS.C1a-app claim entry is a use-site inventory

**ASN-0100, Claims Introduced (INS.C1a-app) and §S8★**: "...yielding a unique maximally-merged decomposition; **instantiated at each S8★ discharge site**." The §S8★ heading likewise frames the lemma by where it is "instantiated."

**Problem**: This is the flagged anti-bloat pattern of a definition introduction enumerating downstream consumers rather than advancing its content. The lemma's meaning is "preconditions S2 ∧ S8-fin ∧ S8-depth ⇒ unique maximally-merged decomposition of the single-subspace restriction." Where it gets used is the verification's business, not the claim's.

**Required**: State INS.C1a-app as the precondition→conclusion lemma it is; remove "instantiated at each S8★ discharge site" from the claim statement.

### Issue 3: Implementation-mechanism enumeration in an abstract slot

**ASN-0100, Atomicity and Canonical Order**: "Implementations realise the composite via transactional sequencing, locking, copy-on-write, or log-and-commit..."

**Problem**: A bare enumeration of implementation mechanisms. It is bracketed as "below the level of abstraction," so it does not constitute drift, but the list itself advances no reasoning — the point ("the decomposition choice is unspecified") is already made by the uniqueness-of-Σ' argument.

**Required**: Replace the mechanism list with the abstract point: the post-state Σ' is determined, the realizing decomposition is not. No catalog of techniques needed.

## OUT_OF_SCOPE

The ASN bounds link-subspace insertion, COPY, DELETE, REARRANGE, versioning, and replication correctly in §Bounding the Scope. The INSERT-vs-COPY contrast stays in scope: its claims (INS.identity, .crossdoc, .tightsurv) are about INSERT's identity-by-allocation, not COPY mechanics, and they are legitimately derived consequences.

VERDICT: REVISE
