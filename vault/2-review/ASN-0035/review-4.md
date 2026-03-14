# Review of ASN-0035

## REVISE

### Issue 1: N6 lacks formal statement, derivation, and demonstrative example

**ASN-0035, "Structural ordering"**: "The total order T1 restricted to `Σ.nodes` reflects the depth-first linearization of the node tree."

**Problem**: Three concerns.

(a) The property is stated informally. "Reflects the depth-first linearization" is not a formal predicate. A formal statement would be: for any `a, b ∈ Σ.nodes`, `a < b` under T1 iff `a` precedes `b` in the depth-first pre-order traversal of `(Σ.nodes, parent)` with siblings visited in T1 order. No such formalization is given.

(b) No derivation is provided. The property follows from T5 (contiguous subtrees) and N5 (sequential children) by induction on the tree: all descendants of sibling `i` form a contiguous interval (T5) that precedes sibling `i + 1` (because `[..., i, ...]` < `[..., i + 1]` by T1 at the divergence point). This multi-step argument is absent.

(c) The illustrative example describes baptism sequence `[1,1]`, `[1,1,1]`, `[1,2]` where temporal and tumbler orders coincide — both yield `[1,1] < [1,1,1] < [1,2]`. The text claims "`[1,2]` was baptized *after* `[1,1,1]` and yet follows it on the line," but "follows" holds in *both* temporal and structural senses here, so the example does not demonstrate the claimed divergence. The BAPTIZE concrete trace (steps 1–3) actually does demonstrate it: baptism order `[1,1], [1,2], [1,1,1]` vs. tumbler order `[1,1] < [1,1,1] < [1,2]`. N6 should reference that trace or use an example where the two orders genuinely differ.

**Required**: (a) A formal predicate for "depth-first linearization." (b) A derivation from T5 + N5. (c) Replace or supplement the example with one demonstrating temporal/structural order divergence — the concrete trace already provides one.

### Issue 2: N15 asserts permanence of an abstract, deferred predicate

**ASN-0035, "Allocation authority"**: "The authority is established at the moment of baptism and is permanent: once a subtree is delegated, the recipient's authority over it is irrevocable."

**Problem**: The predicate `authorized(actor, p)` is introduced as abstract and its refinement is explicitly deferred to the account ontology ("account ontology refines" in the properties table). Despite this, N15 asserts semantic properties — permanence and irrevocability — that cannot be verified without a definition. The supporting Nelson quote ("full control over its subdivision forevermore") describes *user accounts*, not the general authorization mechanism.

The BAPTIZE precondition `authorized(actor, p)` is well-defined as a slot for the account ontology to fill. But asserting that whatever fills that slot must be permanent is a *constraint on the future ASN*, not a property of this one. As written, N15 reads as a derived property, but no derivation is possible from the current formalization.

**Required**: Separate N15 into two parts: (a) the BAPTIZE precondition (keep as-is), and (b) the permanence requirement, reframed explicitly as a design constraint the account ontology must satisfy — e.g., "Design constraint: the account ontology must define `authorized` such that authority, once established, is irrevocable."

## OUT_OF_SCOPE

### Topic 1: Inter-node reference resolution semantics
N0 and N7 establish that spans and links may target ghost nodes (unbaptized or empty). What a query against such a reference returns — empty result, deferred promise, error — is unspecified here and belongs in a future content-resolution ASN.

**Why out of scope**: This ASN defines reference *admissibility*, not reference *resolution*. The two are independent concerns.

### Topic 2: Genesis bootstrap for authorization
The genesis state `Σ.nodes = {r}` is axiomatic, but no actor is established as `authorized(·, r)`. The concrete trace assumes authorization without grounding it. Whether genesis requires an explicit axiom for `authorized` belongs in the account ontology ASN.

**Why out of scope**: Authorization is explicitly deferred. The traces correctly test mechanical properties (N3, N5) by assuming the precondition holds.

VERDICT: REVISE
