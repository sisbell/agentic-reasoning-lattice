# Review of ASN-0047

## REVISE

### Issue 1: S8★ citation imprecision for link-subspace projection

**ASN-0047, *Amendments to existing transitions* / S8★ definition** and **verification matrix entry for K.μ⁺_L**: The matrix says S8★ is preserved by K.μ⁺_L via "per-subspace projection via ASN-0036's S8 on M(d')|_{V_{s_L}(d')}". The S8★ definition similarly says: "The decomposition is established by direct application of ASN-0036's S8 to the per-subspace projection."

**Problem**: ASN-0036's S8 lists S3 (range in dom(C)), S7b, and S7c as preconditions. For the link-subspace projection `M(d)|_{V_{s_L}(d)}`, the range is dom(L), so S3 strictly fails; S7b/S7c also do not apply (they constrain dom(C)). The text acknowledges this with "S3-style range containment in dom(L) via S3★'s link clause" — but "S3-style" is informal placeholder language, not a formal precondition substitution.

**Required**: Either (a) state explicitly that S8★ is discharged for the link subspace by the trivial length-1 decomposition (which the definition already mentions and which requires no S8 machinery), and update the matrix cell to read "trivial length-1 decomposition" rather than "ASN-0036's S8"; or (b) formalise a store-parametric variant ("Modified-S8" or similar) whose preconditions are stated abstractly in terms of "the relevant store" and explicitly derive both projections from this variant.

### Issue 2: NodeUniqueAllocation does not explicitly state registry-tracking closure

**ASN-0047, *Notation / The state model* (NodeUniqueAllocation)** and **K.δ case (ii) k = 2 discharge, sub-case B**: The K.δ k = 2 sub-case B discharge says: "the T2 spawnPt obligation here is therefore discharged ... by NodeUniqueAllocation's external commitment that every baptised node `t` was placed into the registry's tracked domain by a prior K.δ node-allocation event."

**Problem**: NodeUniqueAllocation as stated has two clauses — (a) Freshness `e ∉ Σ.E` and (b) Bootstrap lineage `n₀ ≼ e` — both of which constrain the *output* of a K.δ node-allocation event. The axiom does not contain an explicit clause asserting "every `t ∈ Σ.E_node` is in the external registry's tracked domain at every state Σ". The discharge in K.δ k = 2 sub-case B requires exactly this closure, but the chain (every E_node entry arrived via prior K.δ case (i) → that event obtained t from the registry → therefore t is in the registry) is left implicit. For an external/protocol-layer axiom, the registry-tracking closure is the substantive premise the docuverse layer relies on, and it should be stated alongside (a) and (b).

**Required**: Add an explicit clause (c) to NodeUniqueAllocation: "Registry tracking: for every reachable state Σ and every `t ∈ Σ.E_node`, t inhabits the external node-allocation registry's tracked domain." Then cite (c) at the K.δ k = 2 sub-case B discharge in place of the implicit derivation.

### Issue 3: K.δ case (ii) k = 0 prose elides the strict relation between freshness and frontier identification

**ASN-0047, K.δ case (ii) sub-case k = 0 (Rationale paragraph)**: The text says "Operationally, the conjunction `t ∈ E ∧ inc(t, 0) ∉ E` IS the frontier identification: under T10a's per-`(t, 0)` uniqueness ... combined with P1 (E-monotonicity, so any prior firing would leave its output permanently in E), `inc(t, 0) ∉ E` is logically equivalent to '(t, 0) has not yet fired on t's sub-allocator chain'..."

**Problem**: The biconditional "`inc(t, 0) ∉ E` ⟺ `(t, 0)` has not yet fired" requires more than T10a per-`(t, 0)` uniqueness and P1 alone. The forward direction (¬fired ⟹ ∉ E) holds when there is no *other* allocator that could produce `inc(t, 0)`. T10a GlobalUniqueness gives this, but the prose chain only names per-`(t, 0)` uniqueness, P1, and "logical equivalence" — without spelling out GlobalUniqueness's role in ruling out collisions from independent allocators. The argument is correct but reading it requires the reader to insert GlobalUniqueness silently.

**Required**: Insert one sentence naming T10a GlobalUniqueness as the premise ruling out cross-allocator collisions, alongside the per-`(t, 0)` uniqueness and P1 already cited.

### Issue 4: Dual initial-state definition

**ASN-0047, *The state model* (four-component Σ₀) and *Link store and extended system state* (five-component Σ₀)**: The initial state is defined twice — once with four components (C₀, E₀, M₀, R₀) and once extended with L₀ = ∅. The "Initial state invariant verification" paragraph after the first definition enumerates verifications against an invariant list that does not yet include link invariants; the extended definition then re-verifies the link clauses vacuously.

**Problem**: A reader stepping through inductively may verify the four-component base case, then face the five-component induction and have to re-establish the base case mentally. Splitting the base verification across two sites also produces two separate enumerations of which invariants hold vacuously at Σ₀, with no consolidated single statement.

**Required**: Consolidate to a single initial-state definition with all five components, and a single verification paragraph covering every per-state invariant in ExtendedReachableStateInvariants (including link invariants). The earlier four-component sections can refer forward to this consolidated statement.

### Issue 5: K.α "amendment" terminology contradicts its own disclaimer

**ASN-0047, *Amendments to existing transitions* (K.α amendment shorthand)** and downstream uses ("K.α's amendment fixes `subspace_I(a) = s_C`"): The ASN introduces "K.α amendment" as a shorthand and then explicitly says: "**K.α amendment (shorthand, no local addition).** ... No locally-introduced amendment of K.α is required in the extended state."

**Problem**: Calling a non-existent amendment an "amendment" creates parsing friction at every downstream citation. A reader encountering "K.α's amendment fixes `subspace_I(a) = s_C`" in the verification matrix has to remember that this is a documented shorthand for an inherited foundation precondition, not a local change. The Properties Introduced table further reinforces the confusion by listing "K.α amendment" alongside "K.μ⁺ amendment" and "K.μ⁻ amendment" — the latter two of which *are* local additions.

**Required**: Either drop the "K.α amendment" phrase entirely and cite ASN-0093's K.α precondition directly at every site, or rename it (e.g., "K.α content-subspace clause (inherited)") so the inheritance is visible at the citation point without footnote-tracking.

### Issue 6: Verification matrix "frame" entries hide a non-trivial discharge for L-related rows

**ASN-0047, ExtendedReachableStateInvariants verification matrix**, L-related rows (L0, L1, L1a, L1b, L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ) under K.α, K.μ⁺, K.μ⁻: Each cell reads "frame". The body text below the matrix says: "Frame entries against link-store invariants ... for the transitions K.α, K.μ⁺, K.μ⁻ refer to the amended forms ... These amendments extend each original four-component-state frame with the explicit `L' = L` conjunct; the L-related rows discharge to 'frame' on the strength of that amendment clause, not the original transition's frame."

**Problem**: A 27×8 matrix that flags 30+ cells as "frame" when the underlying frame is the *amended* form (with a clause added by this ASN) is misleading at a glance. The "frame" annotation suggests "nothing to prove" when in fact the amendment's `L' = L` conjunct is doing substantive work. The footnote-style explanation is in the body prose, separated from the matrix.

**Required**: Either (a) annotate the relevant matrix cells with "frame (amended)" or "L' = L (amended frame)" so the discharge mechanism is visible at the cell; or (b) move the prose note immediately under the matrix header so it cannot be missed.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
