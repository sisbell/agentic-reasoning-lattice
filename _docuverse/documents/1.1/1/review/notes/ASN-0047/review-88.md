# Review of ASN-0047

## REVISE

### Issue 1: K.λ missing from "Properties Introduced" table
**ASN-0047, Properties Introduced**: The "New properties introduced by this ASN" table lists K.δ, K.ρ, K.μ⁺_L, K.μ~-FIX, etc., but omits K.λ.
**Problem**: K.λ (LinkAllocation) is introduced as a new elementary transition in this ASN (in the "Link allocation" section). It is a transition kind, not an inherited one from ASN-0043, and belongs in the table.
**Required**: Add a row for K.λ with its statement, preconditions, effect, and frame.

### Issue 2: L1c not explicitly verified or listed in ExtendedReachableStateInvariants
**ASN-0047, Extended reachable-state invariants**: "ExtendedReachableStateInvariants (per-state). Every state reachable from Σ₀... satisfies: S2 ∧ S3★ ∧ ... ∧ L0 ∧ L1 ∧ L1a ∧ L1b ∧ L3 ∧ L14 ∧ L-fin ∧ CL-OWN ∧ CL-UNIQ"
**Problem**: L1c (LinkAllocatorConformance, ASN-0043) is a foundation axiom requiring every `a ∈ dom(L)` to derive from a T4-valid document-level seed via a structural inc chain with `k₁ = 2`. The ASN's K.λ construction preserves L1c by its allocation discipline (first emission via SubAllocatorAxiom; subsequent emissions via inc(·, 0)), but this preservation is neither listed in the invariant set nor explicitly verified.
**Required**: Either add L1c to ExtendedReachableStateInvariants with derivation, or explicitly note "L1c preserved by K.λ's allocation discipline" in the K.λ discharge paragraph.

### Issue 3: "K.δ discharge table" referred to but does not exist as a table
**ASN-0047, Worked example: ghost-base document versioning**: "the K.δ discharge table's k = 1 ghost-base row" and "the K.δ discharge table"
**Problem**: The phrase "discharge table" appears multiple times in the ghost-base worked example, but there is no actual table in the K.δ definition. The structure is a "Per-sub-case additional requirements" bulleted list. Referring to a bulleted list as a "table" is confusing.
**Required**: Either render the per-sub-case requirements as a table, or change the reference to "the K.δ k = 1 ghost-base sub-case" or "the K.δ per-sub-case requirements."

### Issue 4: "Path 0/1/2" terminology used in worked examples but not defined in the K.δ definition
**ASN-0047, Worked example: ghost-base document versioning**: "This is Path 2 (K.δ precondition + TA5 determinism at the tumbler layer)" and "T10a's GlobalUniqueness on `A_v(1.0.1.0.5)` is *not* available here..."
**Problem**: The terms "Path 1" (T10a route) and "Path 2" (direct inspection route) appear in the worked example without prior definition in the K.δ section. The K.δ *Freshness discharge* paragraph describes three routes (NodeUniqueAllocation, T10a GlobalUniqueness, direct inspection) but does not label them.
**Required**: Name the three discharge paths explicitly in the K.δ *Freshness discharge* paragraph (e.g., "Path 0 (NodeUniqueAllocation, case i)," "Path 1 (T10a, case ii live operand)," "Path 2 (direct inspection, case ii ghost operand)"), so the worked example's references resolve.

### Issue 5: P3★ entry references "ASN-0036's P0/P1/P2"
**ASN-0047, Properties Introduced, Local extensions table**: "P3★ | ... | Synthesises ASN-0036's P0/P1/P2 + ASN-0043's L12 with the qualitative mode-enumeration..."
**Problem**: ASN-0036 does not have properties labeled P0/P1/P2. The labels P0, P1, P2 are introduced in this ASN (P0 subsumes ASN-0036's S0+S1; P1 specialises ASN-0034's T8 to the entity set; P2 is introduced fresh). The "Foundation source" attribution is incorrect.
**Required**: Change "ASN-0036's P0/P1/P2" to "this ASN's P0 (subsuming ASN-0036's S0/S1), P1 (specialising ASN-0034's T8), and P2."

### Issue 6: wp derivation phrasing "substituting R for R'" is non-standard
**ASN-0047, Coupling and isolation, J1 derivation**: "Computing the wp of K.μ⁺ alone, substituting R for R': wp(K.μ⁺, Contains(Σ') ⊆ R) = (A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R)"
**Problem**: Standard wp semantics evaluates the post-condition at the post-state. The phrasing "substituting R for R'" suggests a textual substitution of variable names, which is not how wp works. The correct framing is: since K.μ⁺ frames R (i.e., R' = R), evaluating `Contains(Σ') ⊆ R` at the post-state reduces to `Contains(K.μ⁺(Σ)) ⊆ R = R'`.
**Required**: Rephrase to "Since K.μ⁺ frames R (R' = R), Contains(Σ') ⊆ R' at the post-state reduces to..." or similar standard wp phrasing.

### Issue 7: L14 entry claims "no L14 label in the foundation"
**ASN-0047, Properties Introduced, New properties table**: "L14 | StoreDisjointness: `dom(C) ∩ dom(L) = ∅` — derived from L0 and SC-NEQ via T7 (new derivation; no L14 label in the foundation)"
**Problem**: ASN-0043 does have an L14 label — "L14 (DualPrimitive)" — with the scoped statement `dom(L) ∩ dom(C)|_{s_C} = ∅`. This ASN's L14 (StoreDisjointness, unscoped) is a strengthening of ASN-0043's L14 (DualPrimitive, scoped under `s_C`-resident content). Claiming no foundation L14 exists is factually incorrect.
**Required**: Move L14 to the "Local extensions and strengthenings" table with attribution: "Strengthens ASN-0043's L14 (DualPrimitive, scoped) to the unscoped form by deriving from L0 (with C-clause) and SC-NEQ via T7."

## OUT_OF_SCOPE

### Topic 1: Node sub-hierarchy structure within E_node
**Why out of scope**: NodeLineage requires `n₀ ≼ e` for all nodes, but does not enforce a parent-of-node relationship inside E_node (no analog of P8 for nodes). Whether [1, 2] must be in E when [1, 2, 3] is in E_node is left unconstrained. Specifying intra-node hierarchy belongs to a future node-management ASN.

### Topic 2: Concurrency semantics for K.δ Path 2 freshness
**Why out of scope**: Already flagged in Open Questions ("Under what discipline can K.δ's Path 2 freshness discharge remain sound when concurrent or multi-protocol entity allocations may emit candidates between the inspection and the commit").

### Topic 3: Version contract and lineage acyclicity
**Why out of scope**: Explicitly deferred ("The richer version contract — including arrangement invariants, provenance flow, and lineage acyclicity — is deferred to a subsequent version-management ASN").

### Topic 4: Link withdrawal mechanism reconciling tombstoning with D-CTG★/D-MIN★
**Why out of scope**: Already flagged in *Link-withdrawal gap* section and Open Questions; specifying the withdrawal mechanism requires status flags, tombstones, or retraction links outside this ASN.

VERDICT: REVISE
