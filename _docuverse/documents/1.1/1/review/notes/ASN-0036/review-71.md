# Review of ASN-0036

## REVISE

### Issue 1: Within-subspace uniqueness proof omits divergence-position lower bound

**ASN-0036, S8 proof "Uniqueness within a subspace"**: "Suppose for contradiction that t ≠ v satisfies #t = m and v ≤ t < v + 1, the sequences diverge at some first position j ≤ m."

**Problem**: For `v, w ∈ V_S(d)` with the same subspace `v₁ = w₁ = S`, the divergence position j must satisfy j ≥ 2 (since they agree at position 1 by hypothesis). The case analysis "j < m" and "j = m" implicitly excludes j = 1 but does not say so. At m = 2, this matters: case "j < m" reduces to j = 1, which is impossible — so only case "j = m" is operative. A reader checking m = 2 may briefly wonder why "j < m" is even considered.

**Required**: Add one sentence at the start of the case analysis: "Since v, w have the same subspace, v₁ = w₁, so j ≥ 2." Then note that at m = 2 only the j = m case applies.

### Issue 2: S5 cross-document construction has ambiguous "distinct V-positions"

**ASN-0036, S5 proof "Cross-document construction"**: "N + 1 documents d₁, …, d_{N+1}, with M_N(dᵢ) = {vᵢ ↦ a} for pairwise distinct V-positions vᵢ."

**Problem**: It is not stated whether "pairwise distinct" means distinct across documents (the vᵢ for i ≠ j are different tumblers) or merely that each document's singleton arrangement is well-formed (each dᵢ has one V-position, but vᵢ could equal vⱼ for i ≠ j across documents). Either reading yields multiplicity N+1, but the formal counting `|{(d, v) : v ∈ dom(M(d)) ∧ M(d)(v) = a}|` counts pairs `(d, v)`, so the cross-document case works under either interpretation. The within-document case explicitly says "pairwise distinct" — clear there. Cross-document case is ambiguous.

**Required**: Clarify the intent in the cross-document construction. If positions need not be distinct across documents, drop "distinct"; if they must be, say so explicitly. Either way, note that the multiplicity counting is by pairs.

### Issue 3: S8 existence postcondition is satisfied trivially; architectural intent diverges from formal claim

**ASN-0036, S8 proof and surrounding discussion**: The proof establishes "There exists a finite set of correspondence runs..." by constructing the singleton decomposition (each v becomes its own run with n=1). The text immediately afterward discusses `#runs(d)` as if there is a canonical run count, citing CPU hotspot data from Gregory and an abandoned consolidation function.

**Problem**: The formal theorem only guarantees that *some* decomposition exists. Singleton always works. The architecturally interesting claim — that consecutive allocations naturally form longer runs, that `#runs(d)` is meaningfully proportional to "editing events" — is asserted in prose but not formalized. The reader is invited to take `#runs(d)` as a quantity but the theorem does not establish it as well-defined (multiple decompositions of different cardinality may coexist, as the open questions section acknowledges).

**Required**: Either (a) explicitly note in the proof that the singleton decomposition is one of potentially many decompositions, and that `#runs(d)` is not canonical without further constraint; or (b) strengthen the theorem to establish a canonical (e.g., maximal) decomposition; or (c) defer the `#runs(d)` discussion entirely to the operations layer where the structure is preserved.

### Issue 4: OrdAddHom postcondition (b) derivation is one sentence

**ASN-0036, OrdAddHom Formal Contract postcondition (b)**: "subspace(v ⊕ w) = subspace(v) — since k ≥ 2, TumblerAdd copies r₁ = v₁ from the start, preserving the subspace identifier."

**Problem**: This is a one-clause derivation appearing only in the contract block, not the proof body. The proof body proves only postcondition (a). The reader must reconstruct the (b) derivation from the contract clause: TumblerAdd's prefix-copy region is `1 ≤ i < k`; since k ≥ 2, position 1 is in this region, so r₁ = v₁; subspace(v ⊕ w) := (v ⊕ w)₁ = r₁ = v₁ =: subspace(v). Brief, but currently spread across the contract and the precondition `w₁ = 0` (which forces k ≥ 2). Postcondition (c) chains (a) and (b) but is also justified entirely in the contract. A complete proof body would walk through all three postconditions.

**Required**: Add (b) and (c) derivations to the proof body, even if brief. Currently the proof claims to establish OrdAddHom but only proves (a) explicitly.

## OUT_OF_SCOPE

### Topic 1: Operation-specific D-CTG/D-MIN preservation
**Why out of scope**: The ASN explicitly states "Whether DELETE, INSERT, COPY, and REARRANGE preserve D-CTG is a verification obligation for each operation's ASN." Operation semantics belong in operation ASNs, not here.

### Topic 2: Subtraction homomorphism for ord
**Why out of scope**: Listed in the open questions. The ASN establishes addition homomorphism (OrdAddHom) and shift homomorphism (OrdShiftHom) — subtraction would require analyzing TA7a's conditional S-membership for subtraction (TA7a.1, TA7a.2, TA7a.3) and is appropriately deferred.

### Topic 3: Round-trip property for ord/vpos under arithmetic
**Why out of scope**: Listed in open questions. Requires the subtraction analysis above plus the partial-inverse conditions of TA4 (PartialInverse, ASN-0034). Belongs in a future ASN that addresses both.

### Topic 4: Garbage collection / orphan reachability
**Why out of scope**: The ASN establishes S6 (persistence independence) and notes Gregory's evidence on commented-out reclamation. The question of whether orphaned content should be queryable is acknowledged in open questions and belongs in a future ASN about querying or storage management.

### Topic 5: Sharing inverse computability
**Why out of scope**: Open question about cost bounds for "given a, find documents referencing a." This is an efficiency property of an implementation, not an abstract invariant.

VERDICT: REVISE
