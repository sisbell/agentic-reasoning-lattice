# Review of ASN-0047

## REVISE

### Issue 1: Citations to foundation lemmas absent from the foundation claim sets

**ASN-0047, L1b proof (subsequent-link case)**: "TA5(c) gives `#ℓ = #prev`, and T10a.8 (UniformSiblingZeroCount, ASN-0034) gives `zeros(ℓ) = zeros(prev) = 3`."

**ASN-0047, K.μ⁺_L precondition**: "OrdShiftHom (ASN-0036, clauses (b) and (c)) and OrdAddS8a (ASN-0036) are subspace-parametric in v₁..."

**Problem**: ASN-0034's `T10a` sub-lemmas are fully enumerated as T10a.1–T10a.7 plus T10a-N; there is no **T10a.8 (UniformSiblingZeroCount)**. Likewise ASN-0036 defines `OrdShiftHom`, `S8a`, `S8-depth`, etc., but no **OrdAddS8a**. These are load-bearing citations (zero-count preservation for L1b; S8a preservation for K.μ⁺_L) grounded in lemmas that do not exist in the cited foundations. Relatedly, the per-state invariant conjunction and the matrix cite **S7c** ("Element-field depth, `#E(a) ≥ 2`") as an ASN-0036 invariant, but ASN-0036's claim set contains S7, S7a, S7b, S7d only — no S7c. A reader cannot verify a proof step that rests on a non-existent lemma.

**Required**: Re-ground each step in an actual foundation property. The zero-count claim for `inc(prev, 0)` on a T4-valid `prev` follows from TA5(c) (modifies only `sig(prev)`) + TA5-SigValid (`sig(prev) = #prev`, last component nonzero, stays nonzero) — cite those. For S8a preservation under shift, cite the actual ASN-0036/ASN-0034 properties (TS-family + S8a). Either confirm S7c exists in ASN-0036 and correct the extraction, or replace S7c with the correct source (ASN-0093 C1b states `#E(a) ≥ 2`, but that is ASN-0093, not S7c).

### Issue 2: Definitions enumerate downstream consumers instead of advancing meaning

**ASN-0047, multiple definition sites**:
- FrontierEquivalence *Significance*: "Downstream K.δ case (ii) k = 0 discharge and the S4 row of the verification matrix cite this lemma rather than re-deriving the three-premise chain in place."
- K.δ-ID catalogue: "Downstream prose cites these identities by name (K.δ-ID.zeros-0/1, ...) rather than unpacking the TA5/T4b derivation chain at each invocation site."
- CrossDocDisjoint: "Downstream sites cite this lemma as CrossDocDisjoint."
- K.α inherited precondition: "Downstream sites in this ASN — verification matrix, body prose, and the Properties Introduced tables — cite this inherited precondition by name as K.α's `E(a)₁ = s_C` precondition."

**Problem**: This is the use-site-inventory pattern the anti-bloat note flags ("a definition's introduction enumerates downstream consumers rather than advancing the definition's meaning"). The citation handle is established by naming the lemma; listing which later sections invoke it adds no content and rots as sections move.

**Required**: Delete the consumer inventories. Keep the named handle (e.g., "We refer to this as CrossDocDisjoint") without enumerating invocation sites.

### Issue 3: Deferral-chain meta-prose in the K.μ~ section

**ASN-0047, Decomposition of K.μ~ and surrounding**: e.g. "Step (D)'s detailed treatment of this inductive separation appears in the body of *Link-subspace fixity* below; the present note flags the separation at the precondition site"; "proved at *K.μ⁻ admissible contraction shape* below"; "the full account is in ... below"; the *L14 premise convention (used throughout this section)* preamble; the *Dependency chain at a glance* block that then restates each step's consumes/produces a second time in the proof prose.

**Problem**: Multiple paragraphs in different slots defer to the same downstream location, and the dependency chain is stated twice (the "at a glance" block plus the per-step proofs (A)–(E)). The anti-bloat note flags both "multiple paragraphs defer to the same downstream location" and "two paragraphs say the same thing in different words." The reader must skip past navigation scaffolding to reach the argument.

**Required**: State the dependency chain once (either the compact "at a glance" form or the per-step proofs, not both). Replace forward-deferral paragraphs with a single inline derivation at the one site where the result is used.

### Issue 4: The necessity of `|dom_C(M(d))| ≥ 2` is argued three times

**ASN-0047, Preconditions of K.μ~ (*Necessity (sketch)*), Decomposition (*Necessity argument*), and *Note on the dispatch through specific configurations***: All three establish that admissibility (ii) (`π ≠ id`) plus link-subspace fixity forces a non-identity permutation of `dom_C(M(d))`, hence `|dom_C(M(d))| ≥ 2`, with the empty/singleton/mixed sub-cases dispatched in both the *Decomposition* and the *Note*.

**Problem**: Same claim, same argument, three locations — the "two paragraphs say the same thing" pattern, compounded. The *Note on the dispatch* explicitly re-runs the empty/singleton/mixed dispatch the *Decomposition* universal argument already subsumes ("The universal argument above subsumes the per-case treatments").

**Required**: Prove necessity once. If a sketch is wanted at the precondition site, make it a one-line pointer ("necessity is proved in *Decomposition* below"), and delete the *Note on the dispatch* paragraph, whose own text concedes it is subsumed.

### Issue 5: Axiom annotations explain why the axiom is needed rather than what it says

**ASN-0047, NodeRegistryBootstrap *Relationship to NodeUniqueAllocation clause (c)*** and **the *Direct vs derived T10a uniqueness across sub-cases (gloss)* paragraph**: The first is a multi-sentence sub-paragraph explaining that NodeRegistryBootstrap is "the base case" and clause (c) is "the inductive step" — i.e., why the axiom is needed. The second is a standalone "gloss" paragraph cataloguing which discharge route applies at k=0 vs k∈{1,2} before the case analysis that itself states the same routing.

**Problem**: These match the flagged pattern "new prose around an axiom explains why the axiom is needed rather than what it says (sub-paragraphs labeled 'Scope,' 'rationale,' 'Why the axiom is needed,' gloss, etc.)." The k-routing is stated in the gloss and then again in each sub-case's discharge.

**Required**: Reduce NodeRegistryBootstrap to its content (n₀ ∈ registry at Σ₀). State the base-case/inductive-step relationship once at the single discharge site (K.δ case (ii) k=2 sub-case C) that needs it. Fold the gloss's routing into the per-sub-case discharges rather than pre-stating it.

### Issue 6: K.μ⁻ empty-arrangement paragraph re-derives a condition the explicit precondition already carries

**ASN-0047, K.μ⁻ amendment, *Empty-arrangement boundary***: "The load-bearing form ... is K.μ⁻'s *explicit* precondition `dom(M(d)) ≠ ∅` ... The present paragraph's derivation re-establishes the same condition *under the constructive precondition shape* ... The two statements coincide — the explicit precondition is the load-bearing form, the constructive re-derivation is illustrative — and a caller verifying the explicit precondition need not also verify this paragraph's clause."

**Problem**: The paragraph derives `dom(M(d)) ≠ ∅` from the constructive form, then states the derivation is redundant with the explicit precondition and that no caller need check it. This is reviser-drift prose: it argues a case the precondition already excludes and then announces its own dispensability. It advances no reasoning.

**Required**: Delete the paragraph. The explicit precondition `dom(M(d)) ≠ ∅` at the K.μ⁻ definition site stands on its own.

## OUT_OF_SCOPE

### Topic 1: Link-withdrawal / tombstoning mechanism
The interior-link-withdrawal mechanism (status flag, retraction link, version-scoped membership) reconciling Nelson's LM 4/9 tombstoning with D-CTG★/D-MIN★ is correctly deferred. It is a separate state/operation design over `dom(L)`, not a fix to this ASN's arrangement invariants.

### Topic 2: Node-allocation registry protocol
The abstract specification of the external node-allocation registry (issuing protocol, persistence, concurrency) is legitimately a future ASN; NodeUniqueAllocation is a defensible abstraction boundary for the docuverse layer.

META: The ASN remains squarely in specification territory — it defines extended state, elementary transitions, coupling constraints, and reachable-state invariants abstractly; the findings are citation-grounding and accreted meta-prose, not drift into implementation mechanics.

VERDICT: REVISE
