# Review of ASN-0047

This is an exceptionally thorough ASN. The state model, elementary transitions, coupling constraints, and invariant inductions are largely well-constructed, and the worked examples coordinate against named invariants. I have a small number of substantive items that warrant revision, plus a few presentational concerns.

## REVISE

### Issue 1: K.μ⁺_L's m_L parameter freedom at the first-link case

**ASN-0047, K.μ⁺_L precondition list**: "If V_{s_L}(d) = ∅, m_L is a parameter of the transition, subject only to m_L ≥ 2."

**Problem**: The first link arrangement in any document fixes the link-subspace depth permanently (via S8-depth on subsequent K.μ⁺_L events). Different m_L choices produce structurally distinct link-subspace arrangements. The ASN supplies the structural lower bound (m_L ≥ 2 from subspace-closure considerations) but neither pins m_L nor explicitly defers the choice — it sits in a no-man's-land between freedom and constraint. The implementation evidence (Gregory's `findnextlinkvsa` hardcodes the first link VSA at `2.1`, suggesting m_L = 2) is not cited at this site.

**Required**: Either (a) commit definitionally to m_L = 2 with Nelson/Gregory citation, parallel to the SubspaceConventionAxiom commitment for (s_C, s_L) = (1, 2); or (b) explicitly defer the choice to the existing open question "What invariants must the link subspace satisfy beyond those inherited from D-CTG, D-MIN, and S8-depth," with a forward pointer at the K.μ⁺_L definition site so readers know the freedom is intentional rather than oversight.

### Issue 2: Link-subspace analog of S8 correspondence runs not explicit

**ASN-0047, ExtendedReachableStateInvariants proof, *S8-scope in the extended state***: "The composite invariant `S8` at the post-state decomposes per subspace: content-subspace finite span by ASN-0036's S8 over the projection, link-subspace finite span by D-CTG★, D-MIN★, S8-fin, S8-depth, and S8a applied per subspace to V_{s_L}(d) (yielding D-SEQ★)."

**Problem**: ASN-0036's S8 doesn't merely assert finite-span existence — it provides a *correspondence run* structure `(v_j, a_j, n_j)` representing V-position-to-I-address runs, used by downstream span and link operations. The ASN supplies D-SEQ★(s_L) (canonical V-positions) but never defines the link-subspace analog of correspondence runs (mapping link-subspace V-positions to sibling link I-addresses). Worked example 5 implicitly exhibits this structure (sibling V-positions [2,1], [2,2] mapping to sibling link addresses ℓ, ℓ₂), but the structural property isn't named as an invariant. If downstream operations need correspondence runs in the link subspace (e.g., for link-batch arrangement or link-subspace span queries), this gap matters.

**Required**: Either (a) explicitly define link-subspace correspondence runs as an invariant analog of S8's content-subspace structure — provable from K.λ's sibling discipline + K.μ⁺_L's shift-from-max placement; or (b) explicitly acknowledge that link-subspace correspondence-run structure is outside this ASN's scope and identify which downstream ASN will supply it.

### Issue 3: K.δ case (ii) precondition presentation complexity

**ASN-0047, K.δ case (ii)**: The K.δ case (ii) precondition list spans roughly 60 lines, interleaving (i) the sub-case partition by k value, (ii) the `t ∈ E` requirement (which varies by k), (iii) the *Two scopes of "T10a's domain"* clarification, (iv) the *Three discharge paths for `e ∉ E`*, and (v) the *Operational T10a allocator for live-operand sub-cases*.

**Problem**: The structure is correct but cognitively overloaded. A reader trying to verify K.δ's preconditions for a specific case must reconstruct the routing from prose at multiple sites. Worked example 4 (ghost-base versioning) annotates the routing per step, but the K.δ definition itself lacks a tabular summary. This forces every downstream proof that cites K.δ to re-derive the routing.

**Required**: Add a compact summary table at the K.δ definition site, with columns `(case, k, t requirement, discharge path, operational allocator)` and rows for case (i), case (ii) k = 0, k = 1 live, k = 1 ghost, k = 2. This is presentational, not substantive — the content is all present, but a table would make the dispatch immediate.

### Issue 4: K.μ~ contract's subspace-preservation redundancy

**ASN-0047, K.μ~ — contract**: Subspace preservation is listed as an admissibility constraint, then the *Derivability of subspace-preservation from S3★ + L14* paragraph shows it is in fact derivable, then *Why subspace-preservation is nonetheless listed as an admissibility constraint* defends the redundancy.

**Problem**: Three layers of presentation for what amounts to "this is in the contract but follows from other things." The defense ("definitional convenience so downstream proofs can cite it by name") is reasonable but the result is harder to read than necessary. The asymmetric treatment with link-subspace identity (also derivable, but kept as a separate corollary) is justified by derivation-depth differences but adds further complexity.

**Required**: Either (a) remove subspace preservation from the admissibility list and add a single sentence "S3★ + L14 + the bijection equation force π to be subspace-preserving (derivation below)"; or (b) keep it as a contract clause and remove the derivation paragraph and the defense, treating it purely as a stipulation. The current three-layer presentation isn't sustainable.

### Issue 5: NodeLineage label inconsistency

**ASN-0047, NodeLineage axiom**: NodeLineage is labeled "Axiom" but is also presented as discharged inductively (base via reflexivity, inductive step via K.δ case (i)'s `n₀ ≼ e` precondition).

**Problem**: If NodeLineage holds at every reachable state because K.δ case (i)'s precondition enforces it, then NodeLineage is a derived invariant rather than an axiom. The ASN's actual axiom (in the sense of an unprovable premise) is the K.δ case (i) precondition itself. Compare with NodeUniqueAllocation, which truly is axiomatic — `e ∉ E` cannot be derived from any T10a property at the node layer. NodeLineage's "axiom" labeling conflates design-intent with formal axiomaticity.

**Required**: Either (a) reclassify NodeLineage as a derived invariant (label "LEMMA" or "THM") and treat the K.δ case (i) `n₀ ≼ e` precondition as the operative discharge; or (b) clearly distinguish "design-intent axiom" from "formal axiom" and apply that distinction uniformly (J0 has the same dual character and would need re-examination).

## OUT_OF_SCOPE

### Topic 1: Link-subspace correspondence-run query and traversal semantics

**Why out of scope**: Operations that consume link-subspace correspondence runs (link enumeration, link-batch arrangement queries, link-subspace span operations) belong to a downstream link-operations ASN. Issue 2 flags only the structural-invariant gap — defining correspondence runs as a property — not query semantics.

### Topic 2: Account-level depth-1 tumbler extension (k = 1 for accounts)

**Why out of scope**: Already explicitly deferred to an open question. The current `IsDocument(t)` restriction at K.δ k = 1 is a deliberate scope exclusion citing the absence of documented account-version semantics in Nelson/Gregory.

VERDICT: REVISE
