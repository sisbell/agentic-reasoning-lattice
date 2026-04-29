# Review of ASN-0026

## REVISE

### Issue 1: P7 quantifier admits CREATENEWVERSION violation
**ASN-0026, P7 — Cross-Document V-Independence**: `[op applied to d ==> (A d' : d' =/= d : Sigma'.V(d') = Sigma.V(d'))]`

**Problem**: The quantifier ranges over all `d' ≠ d`, including documents that do not yet exist. CREATENEWVERSION applied to `d` creates a new document `d'` whose V-space transitions from undefined (not in `Sigma.D`) to defined. The equality `Sigma'.V(d') = Sigma.V(d')` compares a defined value to an undefined one — the property is violated by construction. The REF-STABILITY proof depends on P7 and inherits this defect, though it would be sound under the corrected formulation.

**Required**: Restrict the quantifier to pre-state documents: `(A d' : d' ∈ Sigma.D ∧ d' ≠ d : Sigma'.V(d') = Sigma.V(d'))`. This protects every document that existed before the operation while permitting CREATENEWVERSION to initialize V-space for the newly created document.

### Issue 2: P7 "applied to" is ambiguous for COPY
**ASN-0026, P7**: "An operation on document `d` does not modify `Sigma.V(d')` for any `d' ≠ d`"

**Problem**: COPY involves two documents — a source (read) and a target (written). Under the reading "COPY applied to the source," P7 would assert the target's V-space is unchanged, which is false (COPY writes to the target). Under the reading "COPY applied to the target," P7 correctly protects the source and all other documents. The phrase "applied to" is undefined and the intended reading must be guessed. The REF-STABILITY theorem ("After any operation on `d_s`") inherits this ambiguity — does "operation on `d_s`" mean an operation that reads `d_s` or writes `d_s`?

**Required**: Define the convention. A clean restatement: "Each text-content operation modifies the V-space of at most one document in `Sigma.D`. For every `d' ∈ Sigma.D` whose V-space is not the write target of the operation, `Sigma'.V(d') = Sigma.V(d')`." This handles INSERT (writes `d`), COPY (writes target), CREATENEWVERSION (writes no existing document), and avoids the "applied to" ambiguity.

### Issue 3: P4 derivation misses nesting-prefix case
**ASN-0026, P4 — Creation-Based Identity**: "Two cases. If `a` and `b` were produced by the same allocator (same ownership prefix), T9 gives... If `a` and `b` were produced by different allocators (distinct, non-nesting prefixes), T10 gives `a ≠ b` directly."

**Problem**: T10 requires `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` — neither prefix is a prefix of the other. But parent and child allocators have nesting prefixes by construction (T10a: the parent spawns the child by `inc(·, k')`, giving the child a prefix that extends the parent's). The parenthetical "distinct, non-nesting prefixes" is presented as exhaustive of the different-allocator case, but it is not — it silently excludes parent/child pairs. ASN-0001 provides GlobalUniqueness as a lemma that handles all cases (same allocator, different allocators with non-nesting prefixes, AND parent/child with nesting prefixes). The same gap appears in the freshness derivation under "I-Space Extension Classification."

**Required**: Replace the two-case derivation with a direct citation of GlobalUniqueness from ASN-0001, which is the exact statement P4 restates in semantic terms.

### Issue 4: P9 does not require injective mapping for new positions
**ASN-0026, P9 — Mapping Preservation Under INSERT**: `(A j : p <= j < p + k : Sigma'.V(d)(j) in fresh)`

**Problem**: `fresh` is defined as a set of `k` elements, and the clause says each of the `k` new positions maps to *some* member of `fresh`. This permits non-injective mappings — two new positions could map to the same fresh address, leaving some fresh address unreferenced at birth. This contradicts the ASN's own observation that "every content-creation operation (INSERT) simultaneously creates a V-space mapping to the new I-content" — if some fresh addresses are unmapped, they are born with `refs(a) = ∅`. It also conflicts with P4: INSERT creates `k` distinct bytes at `k` distinct addresses, and each byte should appear at exactly one new position.

**Required**: State that the mapping from new positions to fresh addresses is injective: `(A j₁, j₂ : p ≤ j₁ < j₂ < p + k : Sigma'.V(d)(j₁) ≠ Sigma'.V(d)(j₂))`. With `|fresh| = k` and injectivity, the mapping is a bijection, ensuring every fresh address appears exactly once.

## OUT_OF_SCOPE

### Topic 1: Document creation and bootstrap
The five operations presuppose `d ∈ Sigma.D`, but no operation creates the first document. CREATENEWVERSION forks an existing document. The system cannot reach a non-empty state from `Sigma_0` without a creation mechanism.
**Why out of scope**: Document lifecycle is a separate concern; the ASN correctly defers it.

### Topic 2: Version DAG structure and immutability
The vocabulary defines versions as "immutable snapshots" but the state model permits `Sigma.V(d)` mutation for any `d ∈ Sigma.D`. The relationship between the mutable current state and the immutable version history is not formalized.
**Why out of scope**: Version semantics requires its own ASN with a formal DAG model.

### Topic 3: Atomicity of compound operations
INSERT requires both I-allocation and V-mapping. The ASN does not specify whether partial failure is possible or what state it would leave. The Open Questions section acknowledges this.
**Why out of scope**: Atomicity is an operational concern that depends on the execution model, which is not yet specified.

### Topic 4: Empty document well-formedness
The Open Questions section asks whether `n_d = 0` is a valid state. P2 and P9 handle it correctly (vacuous satisfaction), but the model neither requires nor forbids empty documents.
**Why out of scope**: This is a design choice that belongs in a document lifecycle ASN, not a defect in the two-space model.

VERDICT: REVISE
