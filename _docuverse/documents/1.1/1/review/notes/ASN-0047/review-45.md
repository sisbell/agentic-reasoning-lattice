# Review of ASN-0047

## REVISE

### Issue 1: Node addresses claimed to be single-component
**ASN-0047, K.δ definition**: "a node address is a single-component tumbler (zeros(e) = 0) drawn from a flat node-identifier namespace by an external allocator"
**Problem**: This contradicts ASN-0045's T4c (LevelDetermination), under which `IsNode(t) ≡ T4-valid(t) ∧ zeros(t) = 0`. T4-validity with zeros = 0 admits multi-component tumblers like [1, 2, 3] — the parenthetical "(zeros(e) = 0)" is offered as a definition of single-component but does not entail single-component. The formal precondition states only `ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E`, which permits multi-component nodes. The prose adds an unstated restriction.
**Required**: Either acknowledge that T4c admits multi-component nodes and adjust prose, or add a formal invariant `(A e ∈ E : IsNode(e) :: #e = 1)` to make the single-component restriction load-bearing.

### Issue 2: TA5 cross-reference error in K.δ descent case
**ASN-0047, K.δ definition**: "*Descent case (k ∈ {1, 2}, TA5(b)/TA5(a)).* ... k = 1 (TA5(b)) appends `.1` ... k = 2 (TA5(a)) appends `.0.1`"
**Problem**: TA5(a) is the strict-monotonicity postcondition (`t' > t`), which holds for any k > 0 and does not specify what gets appended. The postcondition that gives the appended content "`.0.1` for k = 2" is TA5(d): `#t' = #t + k`, positions `#t+1 ... #t+k-1` are `0`, position `#t+k` is `1`. The citation should be TA5(b)+(d), not TA5(b)/(a) — TA5(b) supplies preservation of existing positions, TA5(d) supplies the length extension and zero-separator/terminal-1 structure.
**Required**: Replace "TA5(b)/TA5(a)" with "TA5(b)/TA5(d)" and correct the inline citations `k = 1 (TA5(b)+(d))` and `k = 2 (TA5(b)+(d))`.

### Issue 3: "origin(t) = parent(e)" overloads origin notation
**ASN-0047, K.δ sibling case**: "*Sibling case (k = 0, TA5(c)).* t is a previously allocated address at the same level as e under parent(e), so origin(t) = parent(e) and `zeros(t) = zeros(e)`. ... The condition origin(t) = parent(e) here means t is a child of parent(e) at the same level as the new entity."
**Problem**: `origin(·)` is defined in ASN-0036 (S7) as `N(a).0.U(a).0.D(a)` — applicable only to element-level addresses (zeros = 3) where all four T4b projections are defined. For an entity t with zeros ≤ 2, origin(t) is not defined by S7. The ASN attempts to repurpose origin by paraphrase ("here means t is a child of parent(e)"), but this is definition-by-prose rather than a formal definition. A reader cannot mechanically check this clause against S7.
**Required**: Either introduce a distinct entity-level notation (e.g., `entityParent(t)` or `parentOf(t)`) and define it formally, or restrict the sibling case to use only `parent` terminology (e.g., "parent(t) = parent(e)" with parent generalised to non-node entities, already defined in this ASN).

### Issue 4: T7 misapplied in K.μ⁺_L verification
**ASN-0047, K.μ⁺_L verification of v_ℓ ∉ dom(M(d))**: "`subspace(v_ℓ) = s_L` and `s_L ≠ s_C` (SC-NEQ) ensures no collision with text-subspace positions (T7)."
**Problem**: T7 (FirstElementFieldDistinction, ASN-0034) is stated for "T4-valid element-level tumblers" — its preconditions require `zeros(a) = zeros(b) = 3`. V-positions have `zeros(v) = 0` (S8a), so T7 does not directly apply. The intended argument is far simpler: distinct first components imply distinct tumblers by T3 (CanonicalRepresentation) — if `v.1 = s_L ≠ s_C = w.1`, then by extensionality v ≠ w.
**Required**: Replace the T7 citation with T3 (or with extensionality directly).

### Issue 5: K.α lacks formal inc-conformance precondition
**ASN-0047, K.α definition**: Precondition states only `IsElement(a) ∧ origin(a) ∈ E_doc`. Prose mentions: "the allocation mechanism inc(·, k) (TA5, ASN-0034) operates within an ownership domain... By GlobalUniqueness (ASN-0034), a is distinct from every previously allocated address."
**Problem**: K.λ's precondition explicitly requires "ℓ is produced by a T10a-conforming allocation event (TA5, ASN-0034) on the link allocator's current frontier under d's link prefix" — the explicit structural requirement is what closes T10a's GlobalUniqueness chain. K.α's prose claim that "a is distinct from every previously allocated address" by GlobalUniqueness rests on the same inc-conformance, but the precondition does not formalize it. Without explicit inc-conformance, `a ∉ dom(C)` alone does not exclude collisions with non-content addresses or non-inc-produced collisions. The asymmetry between K.α and K.λ obscures that both rely on the same T10a chain.
**Required**: Add to K.α's precondition: "a is produced by a T10a-conforming allocation event (TA5, ASN-0034) under origin(a)'s content allocator", parallel to K.λ's wording.

### Issue 6: K.δ identity criterion for nodes is incompletely formalized
**ASN-0047, K.δ root node case**: "the address is allocated outside the inc(·, k) discipline ... subject only to ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E ... node uniqueness is enforced by the external allocator rather than by T10a, since inc(·, k) is defined to extend an existing tumbler rather than to mint a top-level identifier. ... any allocator satisfying e ∉ E suffices"
**Problem**: For root nodes, the GlobalUniqueness chain that T10a closes for inc-produced addresses is delegated to "the external allocator's external uniqueness guarantee." But the abstract specification gives no formal property that "the external allocator" must satisfy beyond `e ∉ E`. In a distributed system, ensuring `e ∉ E` across nodes without coordination is precisely the problem T10a solves for content/link allocation; punting it to an unspecified mechanism leaves the soundness of root-node creation ungrounded at the abstract level. Either the abstract specification should state the contract this external allocator must satisfy (e.g., "node addresses are drawn from a globally unique identifier space"), or it should derive uniqueness from a stated property of n₀'s address space.
**Required**: Add a concrete contract for root-node uniqueness as an axiom (e.g., "Axiom (NodeUniqueAllocation): for every K.δ root-node event producing e, e is distinct from all previously allocated entities in any reachable state"), or state explicitly that node uniqueness is a property of the underlying namespace and out of scope for the transition model.

### Issue 7: K.μ~ link-subspace identity is both precondition and derived consequence
**ASN-0047, K.μ~ definition vs S3★ analysis**: K.μ~'s precondition asserts "π is the identity on the link subspace — `(A v ∈ dom(M(d)) : subspace(v) = s_L : π(v) = v)`". The Generalized referential integrity section then derives the same fact: "Link-subspace fixity under K.μ~. Since K.μ⁺ (amended) requires `subspace(v) = s_C` for new V-positions, K.μ⁺ cannot create link-subspace V-positions... Each surviving link-subspace mapping retains its value in dom(L)."
**Problem**: The ASN states this is intentional ("Stating it at the definition site makes K.μ~'s contract explicit and removes the indirection through the decomposition... so the strengthening is consistent rather than restrictive"), but the resulting structure is unclear: if the precondition holds by stipulation, the derivation is vacuous; if the precondition is "consistent with" a derived theorem, then either the precondition is decorative or the precondition forces something stronger than the derivation establishes (e.g., the precondition forbids cardinality-preserving swaps within a duplicate-mapping case that the derivation alone would admit). The reader cannot tell which clauses are independent and which are equivalent.
**Required**: Resolve this either by (a) keeping the precondition and demoting the derivation to a redundancy-check remark, or (b) keeping the derivation and weakening the precondition to subspace-preservation only, deriving the pointwise-identity from S3★ + the K.μ⁺ amendment.

### Issue 8: ReachableStateInvariants self-reference suggests dual-presentation drift
**ASN-0047, Extended reachable-state invariants section**: "This supersedes the ReachableStateInvariants theorem (ASN-0047) by replacing S3 with S3★...", and similarly "ValidComposite★ ... supersedes ValidComposite (ASN-0047)", "P4 (ASN-0047)", etc.
**Problem**: The ASN cites itself by number multiple times, signalling that the extended-state portion was layered onto a pre-existing four-component model. The result is two versions of nearly every invariant (S3 vs S3★, P3 vs P3★, P4 vs P4★, P5 vs P5★, ValidComposite vs ValidComposite★, ReachableStateInvariants vs ExtendedReachableStateInvariants) and a reader who must track which version applies in which section. This is structurally awkward and creates confusion about which form is normative.
**Required**: Either (a) restructure so that the five-component state is presented from the start, with the four-component theorems removed entirely; or (b) explicitly mark the four-component sections as "Pre-Link Model" and the five-component sections as "Final Model", so the reader can see the layering. Remove the self-citations "(ASN-0047)".

### Issue 9: K.δ k = 1 descent semantics undeveloped
**ASN-0047, K.δ descent case**: For k = 1, "inc adds `.1`" without a new zero separator, and `zeros(e) = zeros(t)`. So k = 1 descent from a document [N, 0, U, 0, D] yields [N, 0, U, 0, D, 1] — still zeros = 2, still IsDocument by T4c, but with a multi-component D-projection.
**Problem**: The ASN admits k = 1 descent for documents (producing what would conventionally be a version or sub-document) but does not explain what this corresponds to semantically. The worked example covers sibling creation (k = 0) and account/document descent (implicitly k = 2 in the initial state setup), but not the k = 1 case. The reader is left to infer whether [N, 0, U, 0, D, 1] is intended as a version of document D, a sub-document, or something else, and whether the transition model treats it specially.
**Required**: Either add a worked example exercising the k = 1 descent case (showing what entity is produced and that K.δ's preconditions are satisfied), or explicitly state that the k = 1 case is out of scope for this ASN and defer to a future version-management ASN.

### Issue 10: K.μ⁻ admissibility tied to D-SEQ★ but D-SEQ★ is derived later
**ASN-0047, K.μ⁻ admissibility precondition**: "for each non-empty subspace S in M(d), there exists `n_S ≥ 1` such that `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` (a contiguous range from the per-subspace minimum, of uniform inner depth — a structural property established for the four-component state in ASN-0036's D-SEQ derivation, here applied per subspace)"
**Problem**: The structural form K.μ⁻ relies on is exactly D-SEQ★ (derived later in the Amendments section). The parenthetical justification — "ASN-0036's D-SEQ derivation, here applied per subspace" — is hand-waved; the per-subspace generalization is itself a derivation, not an inheritance. Strictly, K.μ⁻'s precondition is forward-referencing material that the ASN derives below.
**Required**: Either move the D-SEQ★ derivation earlier in the ASN (before K.μ⁻'s amendment), or explicitly cite "by D-SEQ★ (derived below)" so the forward reference is visible, or restate K.μ⁻'s precondition as a self-contained suffix-removal condition that does not assume the indexed-tuple form.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism
**Why out of scope**: The ASN explicitly flags this as an open question. The amended D-CTG★/D-MIN★ disallows interior link removal via K.μ⁻, but Nelson's tombstoning design (where withdrawn links retain their position with an "inactive" status flag) requires either a status-flag mechanism on link entries or a tombstone marker in M(d). Both are new state components or new transitions, outside this ASN.

### Topic 2: Link inheritance under forking
**Why out of scope**: J4 fork as defined creates a new document populated only from the source's content subspace. Whether the forked document should inherit the source's links is a design question for a future fork-specification ASN, as the ASN itself notes.

### Topic 3: Tombstoning semantics
**Why out of scope**: The ASN trades ASN-0036's tombstoning provision for uniform D-CTG★/D-MIN★. Reintroducing tombstoning (for deleted text or withdrawn links) requires explicit state structure beyond what M(d) currently captures.

### Topic 4: Concurrent allocation discipline
**Why out of scope**: K.α and K.λ both rely on T10a's GlobalUniqueness, which assumes serialization of allocation events. Concurrent allocation (whether across nodes, across users within a node, or within a single document) requires a coordination model outside this ASN.

### Topic 5: Version chain semantics
**Why out of scope**: K.δ k = 1 descent permits multi-component document addresses (which conventionally denote versions), but version-graph semantics (DAG of forking, version comparison, version-resolved transclusion) belongs to a version-management ASN.

VERDICT: REVISE
