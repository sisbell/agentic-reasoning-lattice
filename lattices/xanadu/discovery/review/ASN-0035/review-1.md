# Review of ASN-0035

## REVISE

### Issue 1: N2 quantifies over N, but the definition of N does not support the claim

**ASN-0035, "The node as position" / N2**: "Every node `n ∈ N` with `n ≠ r` satisfies `r ≼ n`."

**Problem**: `N` is defined as `{n ∈ T : n > 0 ∧ zeros(n) = 0}`. The tumbler `[2]` satisfies both conditions — it is positive and has no zero components — so `[2] ∈ N`. But `[1] ⋠ [2]`, since `[1]` is not a prefix of `[2]`. The universal claim over `N` is false under the given definition.

The *intended* claim holds for `Σ.nodes` and is derivable: the root `[1]` is in `Σ.nodes` (N3(a)), BAPTIZE only creates children of existing nodes (preserving the parent's prefix), so by induction every element of `Σ.nodes` has `[1]` as prefix. But the formal statement quantifies over the syntactic set `N`, which includes addresses like `[2]`, `[3, 5]`, `[42]` that no chain of baptisms from `[1]` can produce.

**Required**: Either (a) redefine `N` to include the root-prefix constraint: `N = {n ∈ T : n > 0 ∧ zeros(n) = 0 ∧ n₁ = 1}`, or (b) restrict N2's quantifier to `Σ.nodes` and provide the inductive derivation from N3 + BAPTIZE + the initial state. Option (b) is cleaner — it keeps `N` as the syntactic set (useful for N7's forward-reference principle) and makes N2 a theorem about reachable states rather than a constraint on syntax. Either way, the current statement is formally false and must be fixed.

This inconsistency propagates: N7 says references "may target any address in `N`" — if `N` includes `[2, 3]`, that's a reference to an address permanently outside the docuverse. The ASN should clarify whether that is intended (harmless but permanently empty) or an artifact of the definitional mismatch.

### Issue 2: Initial state of Σ.nodes underspecified

**ASN-0035, "The node as position"**: "At genesis, `Σ.nodes` contains at least the root node."

**Problem**: "At least" admits initial states like `{[1], [1, 3]}` (skipping `[1, 1]` and `[1, 2]`), which would violate N5 (Sequential Children) from the start. It also admits `{[1], [2]}`, which would violate the intended constraint that all baptized nodes are under `[1]`. The inductive arguments for N2 (over `Σ.nodes`), N5, and N8 all depend on the initial state satisfying the invariants, but the initial state is left ambiguous.

**Required**: Specify `Σ.nodes = {r}` at genesis (exactly the root, nothing else). This gives a clean inductive base: N3 holds (trivially a one-element tree), N5 holds (no children, so gap-free vacuously), and the derivation of N2 for `Σ.nodes` starts from a state where only `[1]` is present.

### Issue 3: N8 claims all invariants preserved but verifies only N3

**ASN-0035, "Gradual admission" / N8**: "At every point during a node's lifecycle... the system state satisfies all node invariants."

**Problem**: The ASN explicitly verifies that BAPTIZE preserves N3 (tree closure). Preservation of N4 is argued separately ("BAPTIZE only adds"), and N5 is argued from the `inc(·, 0)` construction. But N8 makes a blanket claim about *all* node invariants without collecting these arguments or identifying which invariants are state-dependent (require preservation proofs) versus structural (hold unconditionally from the tumbler algebra). The reader must reconstruct the verification by scanning the entire document.

**Required**: The N8 section should enumerate the state-dependent invariants (N3, N4, N5) and either show preservation inline or give forward/backward references to where it is shown. For the structural properties (N9, N10 from T5/T10; N16 from TA5), state that they hold unconditionally and cite the foundation property. This turns the claim from assertion into verified enumeration.

### Issue 4: No concrete example verifying BAPTIZE postconditions

**ASN-0035, "Baptism"**: The BAPTIZE operation is defined with preconditions, postconditions, and frame conditions, but no specific scenario is traced.

**Problem**: The ASN has informal examples (the `[1,1] < [1,1,1] < [1,2]` ordering example in N6) but never runs BAPTIZE through a concrete sequence with postcondition checks. The review standards require at least one specific scenario verifying key postconditions.

**Required**: Trace a sequence such as: start with `Σ.nodes = {[1]}`. (1) BAPTIZE(`[1]`): `C = ∅`, `n = inc([1], 1) = [1, 1]`. Check: `[1, 1] ∈ N`, `parent([1, 1]) = [1] ∈ Σ.nodes`, `Σ.nodes = {[1], [1, 1]}`, N3/N4/N5 hold. (2) BAPTIZE(`[1]`): `C = {[1, 1]}`, `n = inc([1, 1], 0) = [1, 2]`. Check: `parent([1, 2]) = [1]`, `[1, 1] < [1, 2]`, last components 1 and 2 differ by 1 (N5). (3) BAPTIZE(`[1, 1]`): `C = ∅`, `n = inc([1, 1], 1) = [1, 1, 1]`. Check: `parent([1, 1, 1]) = [1, 1] ∈ Σ.nodes`, depth increases, N3(b) satisfied. This grounds the postconditions in a verifiable instance.

### Issue 5: N0 asserts link validity without formal grounding

**ASN-0035, "The node as position" / N0**: "A node address `n ∈ N` is a valid target for spanning and linking regardless of whether any content has been allocated under `n`."

**Problem**: The spanning claim is grounded in T12 (SpanWellDefined, ASN-0034) — span well-formedness depends only on the arithmetic of start and length, not on content existence. The linking claim lacks equivalent grounding. Links are defined in the vocabulary as having endsets that are sets of spans, which suggests link well-formedness reduces to span well-formedness. But this reduction is not stated or derived. The ASN cannot assert properties of links when no foundation defines link well-formedness formally.

**Required**: Either (a) make the reduction explicit — endsets are sets of spans (vocabulary), span well-formedness is arithmetic (T12), therefore link endset well-formedness is arithmetic — or (b) restrict N0 to spanning and defer the linking claim to the ASN that formalizes link structure. Option (a) is a two-line derivation; option (b) is a scope trim.

## OUT_OF_SCOPE

### Topic 1: Authorization model formalization
N15 introduces allocation authority informally — "an agent authorized by the parent node's owner." The terms *agent*, *owner*, and *authorized* have no formal definitions. A formal authorization model (delegation, transfer, revocation) belongs in a future ASN, likely alongside account ontology. The open questions already acknowledge this gap.

**Why out of scope**: N15 establishes the *principle* that allocation authority flows downward at baptism. Formalizing the authorization mechanism is new territory requiring its own state model and operations — not an error in the node ontology.

### Topic 2: Node decommissioning semantics
N4 guarantees that baptized nodes are permanent, and the ASN discusses content migration ("Upon notice of cancellation... orderly transition"). But the operational semantics when a node's operator permanently ceases function — resolution behavior for references, content retrieval guarantees, effect on subtree allocation — are not specified.

**Why out of scope**: This requires the replication and inter-server protocol (BEBE), which the ASN explicitly excludes. The open questions acknowledge it.

VERDICT: REVISE
