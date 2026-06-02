# Review of ASN-0047

I checked the state model, the seven elementary transitions, the K.μ~ composite and its necessity/sufficiency argument, the J4 fork (including the duplicate-I-address and k=0 subsequent-version cases), the D-SEQ★ derivation, and the Class (a)/(b) inductive verification. The formal core is sound — boundary cases (empty arrangements, empty subspaces, full clearance, non-injective transclusion, stale provenance) are genuinely covered, and the composite-boundary vs per-state temporal split is handled correctly (J1'★ correctly rejects place-then-remove composites). My findings are confined to the anti-bloat patterns the note solicits, plus one logical-status imprecision.

## REVISE

### Issue 1: Triple-coverage of the K.δ allocator-activation discharge
**ASN-0047, *Elementary transitions* (K.δ case (ii) k=1/k=2), *K.δ case (ii) discharge and parent-allocator activation*, and *ParentAllocatorDispatch***: The child-spawn / version activation story — operand tracking, spawnPt premise, T10a admissibility, which sub-allocator is activated — is told three times: prose in the K.δ box, again in the dedicated discharge section's table, and again in ParentAllocatorDispatch's proof.
**Problem**: This is the flagged pattern "multiple paragraphs in different sections defer to the same downstream location" / "two paragraphs say the same thing in different words." The K.δ box's k=2 sub-case and the discharge section's account/document/node table restate the same spawnPt-premise sourcing; a reader must reconcile three presentations of one mechanism.
**Required**: Designate one authoritative site (ParentAllocatorDispatch) and reduce the other two to a single pointer plus the one fact each locally needs (the zeros/parent identities), rather than re-narrating the activation.

### Issue 2: Repeated forward deferrals to the same downstream locations
**ASN-0047, K.μ⁻ elementary def, K.μ⁺ amendment, K.μ~ admissibility, Step (A), and the necessity proof**: "proved in *K.μ⁻ admissible contraction shape* below," "discharged ... by Step (B) below," "see *K.μ⁻ admissible contraction shape* below," "by Step (B) below" recur across separated sections.
**Problem**: Matches "multiple paragraphs in different sections defer to the same downstream location." Step (B) is pointed at from the admissibility intro, Step (A), and the necessity argument; the contraction-shape lemma from both the elementary def and the amendment. The deferrals accrete without advancing the local claim.
**Required**: Consolidate each derivation's dependents so the forward pointer appears once at the point of first need.

### Issue 3: SubAllocatorBundle re-narrates ASN-0093 lemmas as a source inventory
**ASN-0047, *Sub-allocator activation (SubAllocatorBundle)***: "The standing properties of these chains are foundation facts: each chain is a T10a-conforming ... (ChainDiscipline, ChainEnumerationInjectivity, ASN-0093); its first emission is ... (FirstEmission, ASN-0093) ... (FirstEmissionFreshness, ASN-0093) ... (ChainElementT4Validity, ASN-0093) ... (DisjointSubAllocatorChains, ASN-0093)."
**Problem**: This is consumer/source enumeration prose — it re-lists which foundation lemma supplies each already-foundation property rather than advancing the bundle's own content. The single genuine new fact (the cross-subspace disjointness delta dispatched by CrossDocDisjoint) is buried under the inventory.
**Required**: State the one new obligation the bundle discharges and cite the foundation lemmas once collectively; drop the per-property source recitation.

### Issue 4: K.μ~ admissibility clause (v) conflates hypothesis with derived fact
**ASN-0047, *Decomposition of K.μ~***: clause (v) "π is *link-subspace fixing*: `(A v ∈ dom_L(M(d)) :: π(v) = v)` (forced by LRP under the full-clearance realisation)."
**Problem**: Clauses (i)–(iv) are admissibility *criteria* a candidate π must satisfy; (v) is parenthetically declared *forced* by the realisation (and is in fact *derived* in Step (A), Case s_L, via CL-UNIQ). Listing a derived consequence as a sibling admissibility criterion, then later (necessity proof) re-importing it "as a hypothesis," leaves its logical status ambiguous — is it checked, assumed, or proved?
**Required**: Either present (v) as a derived property of every admissible π (not a criterion the caller imposes), or state explicitly that it is redundant with (i)+(iv)+CL-UNIQ and retained only as a reading aid. Pick one status and use it consistently across Step (A) and the necessity argument.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content withdrawal
**Why out of scope**: K.μ⁻ models only suffix removal; interior withdrawal with V-position compaction (the implementation's `DELETEVSPAN`) is a distinct contraction operation. The ASN already names this as an Open Question, and operation-level semantics (DELETE, INSERT) are explicitly out of scope. New territory, not an error here.

META: not applicable — the ASN defines abstract state (C, L, E, M, R), primitive transitions, and their invariants implementation-independently; it has not drifted into mechanics.

VERDICT: REVISE
