# Review of ASN-0047

## REVISE

### Issue 1: K.δ "Precondition discharge structure" table is inconsistent with the three-path partition

**ASN-0047, K.δ case analysis table**: The table cells route by k-value and "live/ghost" labels (where "ghost" = `t ∉ E_doc`), but the named-rules enumeration immediately below partitions discharge paths by `InEntityAllocatorDomain(t)`, which is strictly stronger than `t ∈ E_doc`.

**Problem**: The table labels "k = 1 (live)" as Path 1 with operand requirement `t ∈ E_doc`. But Path 1's actual premise is `InEntityAllocatorDomain(t)`. The configuration `t ∈ E_doc ∧ ¬InEntityAllocatorDomain(t)` — Exemplar (c) in the Path 2 coverage discussion (k=1 versioning of a ghost-chain document) — falls under Path 2 even though `t ∈ E_doc`. Similarly the k=0 and k=2 cells unconditionally label Path 1, but Exemplars (b) and (d) (ghost-chain downstream emissions where `t ∈ E ∧ ¬InEntityAllocatorDomain(t)`) route to Path 2. The table is misleading enough that a reader using it as the routing reference would discharge the wrong path for these configurations.

**Required**: Either sharpen the table cells to use `InEntityAllocatorDomain(t)` as the partition criterion explicitly, or add rows splitting each k-value by Path 1 vs Path 2 premise.

### Issue 2: K.μ~ admissibility presentation creates a circular-looking derivation

**ASN-0047, Decomposition of K.μ~, "Admissibility constraints" paragraph and subsequent derivation**: The constraints list {S8a, S8-depth, D-CTG★, D-MIN★} but omits S3★ at the post-state. The "Derivation of subspace-preservation from S3★ + L14" then supposes "M'(d) satisfies S3★" — a property not in the listed admissibility. The subsequent invariant preservation argument verifies S3★ at the post-state using subspace preservation as a premise.

**Problem**: Subspace preservation ← S3★(Σ') and S3★(Σ') ← subspace preservation. The text's intended resolution (S3★ at output implicit in "reachable state" admissibility) is plausible but is not stated. Under the strict reading where admissibility is exactly the listed conditions, the inductive step can't close because neither subspace preservation nor S3★(Σ') has an independent ground.

**Required**: Either explicitly list S3★ at the post-state as an admissibility constraint (and treat subspace preservation as derived), or explicitly list subspace preservation as an admissibility constraint (and derive S3★ at the post-state from it + pre-state S3★ + the bijection equation). Pick one and the circularity dissolves.

### Issue 3: m_L = 2 is a definitional commitment but not formalized like SubspaceConventionAxiom

**ASN-0047, K.μ⁺_L precondition**: "m_L = 2, the design baseline convention pinned definitionally by this ASN parallel to SubspaceConventionAxiom's commitment to `(s_C, s_L) = (1, 2)`".

**Problem**: The parallel to SubspaceConventionAxiom is asserted but not realized. SubspaceConventionAxiom is named, has a formal statement, has consultation evidence cited, and appears in the Properties Introduced table. m_L = 2 has none of these — it appears only inline in K.μ⁺_L's precondition prose. Both are "definitional commitments pinning specific integer values", and the asymmetric treatment is inconsistent.

**Required**: Either elevate m_L = 2 to a named axiom (e.g., `LinkVPositionDepthAxiom`) with a formal statement and Properties Introduced row, parallel to SubspaceConventionAxiom; or absorb it into SubspaceConventionAxiom's statement; or downgrade SubspaceConventionAxiom to inline prose. The two definitional commitments should be presented the same way.

### Issue 4: "T" notation conflicts with foundation T0

**ASN-0047, K.δ case (ii) "Two scopes of T10a's domain"**: "`InTumblerUniverse(t) := t ∈ T` — the *tumbler-allocation layer*: `T` is T10a's universe of allocated tumblers, the set of every tumbler ever issued at the namespace-allocation layer". Worked example 4 then uses "T₆" as a state-indexed quantity.

**Problem**: Foundation T0 (ASN-0034) defines T as the carrier set of *all possible* tumblers (every nonempty finite sequence of naturals), fixed and not state-indexed. The ASN's "T" is being redefined as "tumblers allocated up to state s" — a state-indexed subset. Under foundation T, `t ∈ T` is trivially true for any tumbler, making `InTumblerUniverse(t)` vacuous; under the ASN's T, the membership has nontrivial content but the symbol collides with the foundation. The "T₆" notation in worked example 4 makes the state-indexing explicit but is incompatible with T0's fixed carrier.

**Required**: Use a distinct name for the state-indexed allocated set — `Allocated(s)`, `Issued(s)`, or refer to ASN-0034's `allocated(s)` (defined in AllocatedSet). Reserve T for the foundation carrier. Equivalently: define `InTumblerUniverse(t) := t ∈ allocated(s)` at the relevant state s.

## OUT_OF_SCOPE

(None — the ASN's scope statement is explicit, and the open questions appropriately defer named operations, withdrawal mechanisms, version-management semantics, and concurrency.)

VERDICT: REVISE
