# Review of ASN-0047

## REVISE

### Issue 1: GlobalLineage proof — incorrect step count

**ASN-0047, Temporal decomposition (GlobalLineage derivation)**: "Recursive descent through parent chains terminates at a node (since each step strictly decreases `zeros`, the chain reaches `zeros = 0` in at most three steps)"

**Problem**: For entities the `zeros` projection ranges over `{0, 1, 2}` (E excludes IsElement by definition), so the parent chain has at most **two** steps (document → account → node), not three. The "three" appears to confuse element-level addresses with entities.

**Required**: Replace "in at most three steps" with "in at most two steps" (the document case has the longest chain: doc → account → node).

### Issue 2: J1 derivation citation in Properties table is misleading

**ASN-0047, Properties Introduced (J0 row)**: "J1 below is *derived* by wp from J0 (and so not axiomatic)"

**Problem**: The main text derives J1 from the design choice to preserve P4 (`Contains(Σ) ⊆ R`), not from J0. J0 and J1 are independent couplings: J0 couples K.α with K.μ⁺ (placement requirement), J1 couples K.μ⁺ with K.ρ (provenance recording). The table entry mis-attributes J1's derivation.

**Required**: Correct the table entry to state that J1 is derived by wp from the requirement to preserve P4 (or to maintain `Contains(Σ) ⊆ R`), not from J0.

### Issue 3: NodeAllocationRegistry is informal but labeled "Definition"

**ASN-0047, Elementary transitions**: "**NodeAllocationRegistry (Definition).** A *node-allocation registry* is a deterministic discipline external to T10a's allocator-state machinery..."

**Problem**: The "Definition" contains no formal content — it describes a "discipline" whose actual requirements are stated as `NodeUniqueAllocation`. As an ASN definition slot it should either fix a formal object or be relabeled. As written, it adds prose mass without contributing to the proof obligations.

**Required**: Either (a) elevate it to a real definition with formal operational content (state space, issuing function signature, atomicity discipline), or (b) relabel as a "Note" or "Discussion" and acknowledge that the registry is an abstract obligation discharged by NodeUniqueAllocation alone.

### Issue 4: P5 and "Permanence from elementary frames" lemma are redundant

**ASN-0047, Elementary transitions / Destruction confinement**: P5 (Destruction confinement) and the immediately preceding "Lemma (Permanence from elementary frames)" both state that every valid composite preserves P0, P1, P2 (and L12 in the extended state).

**Problem**: These claim essentially the same property with slightly different framings. P5 is then superseded in the extended state by P3. The ASN carries three near-duplicate predicates (lemma + P5 + P3).

**Required**: Consolidate. Either fold the lemma into P5's proof, or drop P5 as redundant and let P3 carry the full statement with a single proof.

### Issue 5: Link-subspace replacement asymmetry not addressed

**ASN-0047, Elementary transitions ("Replacement at the maximum position of a subspace" and "Replacement at an interior position of a subspace")**

**Problem**: The two replacement paragraphs discuss content-subspace replacement only. Link-subspace "replacement" is structurally different: K.μ⁺_L requires `ℓ ∉ ran(M(d))` (first-arrangement) and forces placement at the contiguous min or `shift(max, 1)`, so the same link cannot be re-added at the same V-position. Withdrawing then re-adding a link via K.μ⁻ + K.μ⁺_L necessarily relocates it; substituting a "new" link requires fresh K.λ allocation. The ASN omits this asymmetry from its replacement decomposition discussion.

**Required**: Add an explicit paragraph stating that link-subspace replacement is not symmetric with content replacement: the K.μ⁺_L first-arrangement constraint plus D-CTG★ forbid re-positioning at the original slot, so user-level "replacement" of a link composes as K.μ⁻ + K.λ + K.μ⁺_L with a fresh address.

### Issue 6: Forward-reference accretion and meta-prose

**ASN-0047, multiple sections**

**Problem**: The anti-bloat addendum flagged this ASN's susceptibility to meta-prose. Several specific patterns survive in the current draft:

(a) **K.μ~ "Choice of decomposition" paragraph**: "We adopt the full-clearance decomposition here for uniform treatment across arbitrary π — every non-identity permutation, whether it fixes a prefix or not, decomposes cleanly under full clearance — so downstream invariant verification need not case-split on the longest fixed prefix of π. The choice is presentational..." — pure justification of a presentational choice.

(b) **J4 "Operational shape" paragraph**: "The choice of V-positions in M'(d_new), and the bijection between d_src's content-subspace V-positions and those V-positions, is operation-specific. The strand model fixes only what step (ii) must satisfy..." — explains what is *not* specified rather than advancing the specification.

(c) **"Composite-boundary check (P4★ at M_post)"** in the interior-replacement worked example: "P4★ is a composite invariant per Class (b) and is not required to hold at intermediate states; restoration happens at the K.ρ step below." — meta-prose explaining why a violation is acceptable, rather than tracing the violation/restoration mechanically.

(d) **"Deviation: ..." lines** in worked examples (e.g., "Deviation: S3★ reduces to S3 here because V_{s_L}(d₂) = ∅"): pure relationship-explanation meta-prose.

(e) **"Notation." block** in the fork example: "Verification lines use extended-state labels (P4★, J1★, etc.); since the example's arrangement is content-subspace-only, each starred form reduces here to its four-component ancestor." — presentation commentary.

**Required**: Strip these passages. Choose one decomposition for K.μ~ and present it without comparative justification (move alternatives to open questions if needed); state J4's effect without the "what is not fixed" gloss; trace intermediate-state P4★ status mechanically without naming the class membership; drop "Deviation:" tags and any "Notation:" preamble that explains starred-vs-unstarred equivalence on a per-example basis.

### Issue 7: S4 cross-document distinctness for K.δ on documents lacks explicit lemma citation

**ASN-0047, Foundation invariants block (S4 entry)**: "For K.δ on non-node entities, the same allocator discipline applies via T10a GlobalUniqueness on non-ghost chains..."

**Problem**: The S4 paragraph cites the *Cross-document disjointness chain* lemma for cross-document K.α and K.λ distinctness, but doesn't address the analogous question for K.δ events placing two documents under different accounts. Cross-document distinctness at the entity-allocation layer relies on T10a.{2,5} applied at the *account* level — the document sub-allocators under distinct accounts have non-nesting prefixes by the same argument used for content/link anchors. The chain isn't completed for K.δ.

**Required**: Extend the S4 paragraph to cite the Cross-document disjointness lemma (or an account-level analog) for K.δ events on documents whose parent accounts differ, in addition to the within-account T10a GlobalUniqueness case.

### Issue 8: SubAllocatorAxiom activation timing relative to T10a's spawnPt premise

**ASN-0047, Allocator hierarchy under documents**: "Once each element-field anchor heads a frontier (not derivable from T10a alone — admitted as SubAllocatorAxiom below), the sub-allocator behaves as a T10a-conforming `inc(·, 0)` chain..."

**Problem**: T10a's T2 spawning premise requires `spawnPt(A) ∈ dom_s(parent(A))` at the activation event. The anchors `b_C(d), b_L(d)` are structurally producible via inc steps from d, but they are not themselves elements of any T10a-tracked allocator's domain (as the ASN itself notes: "The anchors are not themselves in `dom(C) ∪ dom(L)`"). SubAllocatorAxiom bundles activation into the K.δ event, but the relationship to T10a's standard activation discipline is left implicit. The ASN admits this informally but doesn't catalogue what T10a property is being bypassed or whether the bypass interacts with T10a.6 (DomainDisjointness) at the parent layer.

**Required**: Add a sentence explicitly noting that SubAllocatorAxiom activates sub-allocators outside T10a's standard T2 spawning step (the anchors are not in any predecessor allocator's tracked domain), and confirm that this bypass does not violate T10a.6 by appealing to subspace identifier distinctness (s_C ≠ s_L) at the anchor level rather than to domain disjointness in the T10a sense.

### Issue 9: K.μ⁻ exhaustiveness lemma — proof of mutual exclusion of cases (b) and (c)

**ASN-0047, K.μ⁻ exhaustiveness lemma**: "(c)'s contiguity clause excludes any K' carrying an interior hole."

**Problem**: The mutual-exclusion argument for cases (b) and (c) hinges on (c) requiring K' contiguous over `[k_min, k_max]` while (b) exhibits an interior hole. The proof states this disjointness in the closing prose ("they are themselves disjoint because (c) requires K' to be contiguous over `[k_min, k_max]` whereas (b) exhibits an interior hole `k₀ ∈ (k_min, k_max) ∩ (K \ K')` violating contiguity"). However, the proof's case structure only reaches case (c) under the "K' contiguous over `[k_min, k_max]`" sub-branch with `k_min ≥ 2`; the disjointness from (b) follows by construction, not as an additional argument. The closing prose suggests an extra disjointness step that isn't actually needed and creates the appearance of redundant verification.

**Required**: Tighten the closing paragraph of the proof. Either remove the disjointness re-verification (it follows directly from the case-split structure) or note that the disjointness is by construction of the case-analysis tree, not by an additional argument over a configuration that the structure already excludes.

### Issue 10: Initial state and base case at Σ₀ — bootstrap node baptism event not characterized

**ASN-0047, The state model (Initial state)**: "E₀ = {n₀} where n₀ = `[1]` — the canonical single-component bootstrap node"

**Problem**: The initial state seeds n₀ into E without a K.δ event. NodeUniqueAllocation is stated as "Every K.δ node-allocation event — every elementary transition of K.δ whose effect places an entity `e` with `IsNode(e)` into E — produces an address satisfying...". The bootstrap node is in E₀ without going through K.δ, so NodeUniqueAllocation does not constrain it. The status of n₀ as a "seed" rather than an "allocated" entity is implicit but not explicitly handled in the invariant preservation arguments (e.g., S4's "distinct allocation events produce distinct addresses" — does n₀'s presence at Σ₀ count as an allocation event?).

**Required**: Add one sentence at the initial state declaration stating that the bootstrap node n₀ is established by system genesis rather than by a K.δ event, and that NodeUniqueAllocation's discharge applies only to subsequent K.δ events. The base case of the NodeLineage induction already discharges `n₀ ≼ n₀` by reflexivity; making the genesis-vs-allocation distinction explicit avoids ambiguity in the S4 invariant.

### Issue 11: P3 versus L12 — labeling and coverage

**ASN-0047, Extended monotonicity invariants**: "P3 is introduced fresh in this ASN as a synthesis of P0 ∧ L12 ∧ P1 ∧ P2 — one named monotonicity predicate over `Σ → Σ'` covering every component except M."

**Problem**: P3 packages L12 as a conjunct, but the Properties table lists L12 as separately retained (and ExtendedTransitionInvariants names both P3 and L12). This creates label redundancy: L12 is both a foundation invariant carried into this ASN and a sub-clause of the new P3 predicate. The relationship between the named foundation invariant and the new synthesis is unclear.

**Required**: Either (a) drop L12 from ExtendedTransitionInvariants as subsumed by P3, with one mention that P3 extends ASN-0043's L12, or (b) drop P3 in favor of citing the four foundation invariants separately (P0, P1, P2, L12). Currently both are listed and the relationship between them adds proof-obligation mass without adding content.

## OUT_OF_SCOPE

### Topic 1: Concurrent operation discipline

The ASN's open questions raise concurrency considerations (ghost-base K.δ freshness under concurrent allocations, K.λ allocation serialization, multi-protocol entity allocation). The present ASN explicitly relies on SequentialTransitionAxiom (single-event sequential atomic transitions); concurrency belongs to a future ASN.

**Why out of scope**: SequentialTransitionAxiom fixes the transition model at sequential atomic events. Concurrent discipline is genuinely new territory requiring a separate ASN to define interleaving semantics, conflict resolution, and the relationship between sequential and concurrent invariant preservation.

### Topic 2: Link-withdrawal mechanism

The "Link-withdrawal gap under D-CTG★ / D-MIN★" paragraph identifies that interior link withdrawal is not expressible under the amended contiguity invariants. The reconciliation mechanism (tombstones, status flags, retraction links) is acknowledged as unspecified.

**Why out of scope**: This is an additional state component or operation set that hasn't been introduced; the present ASN's invariant set (D-CTG★/D-MIN★) is consistent without it. The reconciliation belongs to a follow-on ASN that introduces the withdrawal mechanism.

### Topic 3: Account-level depth-1 tumbler extension (K.δ k=1 with IsAccount(t))

The open questions ask whether account-level k=1 extension should be admitted. The present ASN's precondition explicitly excludes it (k=1 requires IsDocument(t)).

**Why out of scope**: Admitting account-level versioning would require additional invariant work for account identity semantics; it is genuinely new territory rather than an error in the current scope.

### Topic 4: Realisation of NodeAllocationRegistry

The open questions ask what protocol a node-allocation registry must implement. The present ASN abstracts this as the NodeUniqueAllocation axiom.

**Why out of scope**: The mechanism (whether Nelson's hierarchical baptism or Gregory's granfilade dispatch) belongs to a future operations-layer ASN that ties abstract baptism to a concrete protocol.

VERDICT: REVISE
