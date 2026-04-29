# Review of ASN-0006

## REVISE

### Issue 1: Position notation reinvents ASN-0001's subspace arithmetic
**ASN-0006, "The state we need"**: "A position `q = (s, k)` pairs a subspace `s` with an offset `k`... the within-subspace shift `(s, k) ⊕ w = (s, k + w)`"
**Problem**: The ASN introduces `(s, k)` pair notation, `text_subspace(d)`, `link_subspace(d)`, `size(poom(d))`, and a custom `⊕` operator — all of which reinvent ASN-0001's subspace handling. TA7a defines the canonical representation as ordinal-only `[x]` with subspace held as structural context; TA7b defines the subspace frame condition; T7 defines SubspaceDisjointness. The custom notation also creates a type conflict: TC2's `p ⊕ i` for `i = 0` is natural-number addition on pairs, while ASN-0001's `⊕` requires a positive displacement (`w > 0`). The two `⊕` symbols mean different things.
**Required**: Restate positions using ASN-0001's ordinal-only formulation. Subspace is structural context, not an arithmetic operand. Replace `text_subspace(d)`, `link_subspace(d)`, `size(poom(d))` with definitions grounded in T4's field extraction and T7's subspace disjointness. Use span notation from T12 where appropriate (e.g., the copied range `[p, p ⊕ w)` rather than pointwise iteration from 0).

### Issue 2: Transclusion independence theorem assumes B ≠ D without stating it
**ASN-0006, "Independence of transclusions"**: "D's DELETE modifies at most D's POOM (by AX1). Since B ≠ D, `poom'(B) = poom(B)`."
**Problem**: The theorem says "If document B transcludes content at I-addresses A from document D, and subsequently D deletes that content from its POOM, then B's mapping to A is unaffected." The proof uses `B ≠ D`, but this condition appears nowhere in the theorem statement. For self-transclusion (B = D), the theorem is false: D's DELETE modifies D's POOM, which IS B's POOM, and may remove the very V→I entries that constitute the transclusion. A document that self-transcludes and then deletes all V-positions mapping to those I-addresses loses the mapping entirely.

The INSERT isolation corollary has the same gap: "If document B transcludes content from document A" — the proof uses `B ≠ A` without stating it.
**Required**: Add `B ≠ D` (resp. `B ≠ A`) as an explicit condition in both statements. Note that self-transclusion within a single document does not enjoy cross-document isolation — the document's own subsequent operations may displace or remove the transcluded mappings.

### Issue 3: `a↓doc` extraction assumes single-component fields
**ASN-0006, "The state we need"**: "We write `a↓doc` for the document-level prefix of address `a` — the first five components `Node.0.User.0.Document`"
**Problem**: "The first five components" is correct only when Node, User, and Document fields each have exactly one component (α = β = γ = 1 in ASN-0001 T4's notation). T4 allows multi-component fields: `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ`. The document-level prefix has α + β + γ + 2 components in general. The concrete trace uses single-component fields (`1.0.1.0.1`), which masks the issue.
**Required**: Define `a↓doc` using ASN-0001's `fields(t)` function: `a↓doc` is the concatenation of `node(a)`, `0`, `user(a)`, `0`, `doc(a)` as extracted by `fields`. This works for any component count and is computable from the address alone (T4 guarantees this).

### Issue 4: AX1 claims universality beyond its evidence
**ASN-0006, "Independence of transclusions"**: "AX1 (POOM isolation). Every operation modifies the POOM of at most one document"
**Problem**: The statement quantifies over *every* operation, but the evidence is an enumeration of currently-known operations (INSERT, DELETE, COPY, CREATENEWVERSION, MAKELINK, plus read-only operations). If the enumeration is complete, the universal claim follows — but the ASN does not close the set. A future operation could violate AX1, making proofs that cite it unsound. Additionally, the MAKELINK verification relies entirely on implementation evidence ("Gregory confirms the mechanism") rather than a formal argument about the operation's specification.
**Required**: Either (a) close the operation set — state explicitly that these are all the mutating operations the system provides — and verify AX1 for each, or (b) restate AX1 as a design constraint that all operations must satisfy, distinguishing it from a derived property. The MAKELINK case should get at least a brief formal argument (MAKELINK writes to one document's link subspace; other documents are read-only inputs for V→I resolution).

### Issue 5: Self-transclusion has no concrete trace
**ASN-0006, "A concrete trace"**: The trace covers cross-document COPY (A's content into B).
**Problem**: TC4 explicitly discusses self-transclusion ("When `source_doc = target`... the addresses extracted are those from before the modification"), but no concrete trace verifies the interaction of TC4 (read-before-write) with TC7 (shift). The interesting case is when the source span overlaps the insertion point: COPY from `[0, 3)` to position 2 within the same document. Before the operation, positions 0, 1, 2 map to addresses a₀, a₁, a₂. TC4 says extract {a₀, a₁, a₂} from the pre-state. TC2 deposits them at positions 2, 3, 4. TC7 shifts old positions ≥ 2 forward by 3 — so old position 2 goes to position 5. Show this scenario end-to-end and verify that all postconditions are consistent.
**Required**: Add a self-transclusion trace with overlapping source and insertion point, verifying TC2, TC4, and TC7 step by step.

### Issue 6: Target POOM post-state domain not explicitly characterized
**ASN-0006, TC2 + TC7**: TC7 states what happens to positions before and after p. TC2 states what positions p through p+w−1 map to.
**Problem**: These clauses state necessary conditions on specific positions but do not characterize `dom(poom'(target))`. An implementation that satisfies TC2 and TC7 while also adding spurious entries (e.g., a phantom mapping at position `size + w + 42`) would not violate any stated postcondition. The frame conditions (TC5, TC6, TC8, TC12) constrain other documents, ispace, links, and the link subspace — but nothing constrains the target's text-subspace domain to be exactly the union of preserved, new, and shifted entries.
**Required**: State the domain explicitly: `dom(poom'(target))` restricted to the text subspace equals `{q : q < p ∧ q ∈ text_subspace(target)} ∪ {p ⊕ i : 0 ≤ i < w} ∪ {q ⊕ w : q ∈ text_subspace(target) ∧ q ≥ p}`, and prove the three sets are pairwise disjoint. This closes the frame on the target's own POOM.

## OUT_OF_SCOPE

### Topic 1: Multi-document, multi-span COPY
**Why out of scope**: The ASN explicitly defers this ("the multi-document generalization is deferred"). The single-span, single-source formalization is the correct first step; the generalization is a future ASN.

### Topic 2: COPY into the link subspace
**Why out of scope**: The precondition restricts `p` to a text-subspace offset (`0 ≤ p ≤ size(poom(target))`). TC3 says COPY doesn't filter content type, but the formal specification only covers text-subspace insertion. Link-subspace insertion (placing content at link positions) is a distinct operation mode that needs its own analysis — particularly the interaction between link-subspace shifts and text-subspace stability.

### Topic 3: Permission model and COPY precondition
**Why out of scope**: TC19 (publication grants transclusion) establishes a permission policy, but the COPY precondition contains no permission check. The relationship between TC19 and the operation's formal precondition — who may invoke COPY on which content — belongs in a permissions ASN, not here.

### Topic 4: Atomicity and concurrency
**Why out of scope**: The open questions ask about COPY atomicity with non-contiguous spans and concurrent source modification. These are concurrency concerns that require a consistency model not yet defined.

VERDICT: REVISE
