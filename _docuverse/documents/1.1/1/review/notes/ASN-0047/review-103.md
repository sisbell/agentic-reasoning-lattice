# Review of ASN-0047

## REVISE

### Issue 1: K.δ k=1 discharge prose conflates T1 and T2 cases

**ASN-0047, "K.δ case (ii) discharge and parent-allocator activation"**: "The step e = inc(t, 1) is a T10a T1 sibling-increment (after the first version) or T2 spawn step (for the first version) on A_v(t)."

**Problem**: K.δ k=1 deterministically produces inc(t, 1) for a given t. By T10a's per-(t, k') uniqueness, this can fire at most once per t. Hence K.δ k=1 is always a T2 spawn step on A_v(t), never a T1 sibling-increment. T1 siblings on A_v(t) correspond to K.δ k=0 events on prior versions (which produce inc(prev, 0)) — those are different K.δ cases entirely. The "T1 sibling-increment (after the first version)" clause is incorrect.

**Required**: Remove the T1 clause from the K.δ k=1 discharge. State that K.δ k=1 is always a T2 spawn step on A_v(t), and note (separately, if useful) that subsequent versions arise from K.δ k=0 events on prior versions, which are T1 siblings on A_v(t).

### Issue 2: A_v(d) activation discipline is implicit

**ASN-0047, Sub-allocator names definition and K.δ k=1 discharge**: SubAllocatorAxiom activates A_C(d) and A_L(d) "for each d ∈ E_doc, the entity-allocation event placing d into E_doc activates...". A_v(d) has no analogous activation clause. The K.δ k=1 discharge says A_v(t) "was activated by a prior K.δ event whose effect activated t's version sub-allocator A_v(t)" — but no prior K.δ effect is specified to activate version sub-allocators.

**Problem**: The activation discipline for A_v(d) is left as prose. Either (a) it's activated by t's creation K.δ event (in which case the K.δ definition's effect clause or a SubAllocatorAxiom-like extension should formalize this), or (b) it's activated by the first K.δ k=1 event on t itself (a T2 spawn step from t-as-spawnPt). The ASN's prose is ambiguous between these readings.

**Required**: Decide which discipline applies and formalize it. If (b), state the K.δ k=1 discharge as: "K.δ k=1 with operand t is itself the T2 spawn step that activates A_v(t); the spawnPt premise is discharged by K.δ k=1's precondition t ∈ E_doc placing t in A_doc(parent(t))'s tracked domain." Remove the "prior K.δ event whose effect activated" wording.

### Issue 3: SubAllocatorAxiom's T10a.6 non-violation paragraph mixes meta-prose with substance

**ASN-0047, after SubAllocatorAxiom definition**: "*T10a.6 (DomainDisjointness) non-violation.* The activation cannot be derived from T10a's T2 spawning rule because b_C(d), b_L(d) inhabit no predecessor's tracked domain. Disjointness between A_C(d)'s and A_L(d)'s outputs is structural..."

**Problem**: The first sentence explains *why* the axiom is needed (T10a doesn't suffice) — this is the "axiom prose explaining why the axiom is needed rather than what it says" pattern. The second sentence (structural disjointness) is substantive content that should be part of the axiom's commitments, not a defense.

**Required**: Remove the "non-violation" framing and the why-explanation. Fold the structural disjointness statement into SubAllocatorAxiom's body (e.g., as a fourth sub-clause: "SubAllocatorAxiom.Disjointness").

### Issue 4: L3's relationship-to-foundation essay content

**ASN-0047, L3 definition**: After stating L3, the ASN has a "*Relationship to ASN-0043's foundation L3*" section with (i) "Reachability closure" and (ii) "Higher-arity exclusion" sub-paragraphs.

**Problem**: This is essay content in a definition slot. (i) is a derivation of L3 from K.λ's precondition and L12, which is closer to a proof than a definition; (ii) is a defensive note about higher-arity links being "out of scope". Neither belongs in L3's definition. The closing sentence about Nelson's design intent and Gregory's implementation is historical citation, not specification.

**Required**: Reduce L3's definition to its content (arity = 3, Θ ≠ ∅). If the derivation (i) is needed, move it under ExtendedReachableStateInvariants. Remove the "higher-arity exclusion" defensive note and the Nelson/Gregory citation.

### Issue 5: ValidComposite★ notation disambiguation is a use-site inventory

**ASN-0047, "Notation disambiguation: atomic vs. composite Σ → Σ'"**: "`Σ → Σ'` denotes the boundary of a finite sequence of elementary transitions when used in coupling/composite contexts (J0, J1, J1★, J1'★, P3, ExtendedReachableStateInvariants, ExtendedTransitionInvariants), and a single atomic step elsewhere..."

**Problem**: This is the "use-site inventory" pattern from the bloat classifier — a paragraph enumerating which sites use the symbol in which sense, which compensates for ambiguous notation rather than fixing it.

**Required**: Either use distinct notation for atomic vs. composite transitions (e.g., `Σ →ₐ Σ'` for atomic, `Σ →* Σ'` for composite), or fix one reading globally and re-state any clause that needs the other meaning explicitly. Remove the inventory paragraph.

### Issue 6: K.μ⁻ has a redundant precondition

**ASN-0047, K.μ⁻ definition**: "*Precondition:* d ∈ E_doc; dom(M(d)) ≠ ∅ — the pre-state arrangement must be non-empty (the strict-subset clause `dom(M'(d)) ⊂ dom(M(d))` has no witness when `dom(M(d)) = ∅`); ..."

And in the K.μ⁻ amendment: "(2) *Strict contraction* `(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)` — at least one subspace shrinks strictly."

**Problem**: If dom(M(d)) = ∅, then V_S(d) = ∅ for both subspaces, and the strict-contraction clause has no witness — it's false. So strict contraction implies non-empty arrangement; stating both is redundant. The parenthetical "the strict-subset clause has no witness when dom(M(d)) = ∅" is defensive explanation that doesn't earn its place.

**Required**: Drop `dom(M(d)) ≠ ∅` from the explicit precondition list; the strict-contraction clause carries the obligation.

### Issue 7: D-SEQ★ derivation dangling reference to ASN-0036's D-CTG-depth

**ASN-0047, D-SEQ★ derivation closing**: "The infinite-cardinality contradiction in Step 1 supplies, for an arbitrary subspace S, the per-subspace analogue of the D-CTG-depth property that ASN-0036 states specifically for the text subspace V_1(d). Here it is derived directly from D-CTG★ + S8-fin + S8a, so D-SEQ★ does not require a separate D-CTG-depth axiom for non-text subspaces."

**Problem**: This sentence cites ASN-0036's D-CTG-depth, notes that the derivation reconstructs the property without reusing it, then explains *why* the citation matters ("so D-SEQ★ does not require a separate axiom"). The reference is dangling — it's invoked only to explain its absence. This is meta-prose defending a design choice.

**Required**: Remove the reference. The D-SEQ★ derivation stands on D-CTG★ + S8-fin + S8a; no defense of independence from ASN-0036's D-CTG-depth is needed.

### Issue 8: K.μ⁻ exhaustiveness lemma proves cases that are immediately excluded

**ASN-0047, K.μ⁻ amendment exhaustiveness lemma**: Proves a three-way partition (a)/(b)/(c) of post-state shapes, then "Only case (a) is admissible under D-CTG★ / D-MIN★: (b) violates D-CTG★...; (c) violates D-MIN★...".

**Problem**: Cases (b) and (c) are exhaustively analyzed (with a detailed case-analysis tree on contiguity, minimum membership, etc.) only to be ruled out by the D-CTG★/D-MIN★ postconditions. This is the "exhaustiveness claim where the precondition already excludes the non-admissible cases" pattern. The lemma would be tighter as: "Under D-CTG★ + D-MIN★ + D-SEQ★, every admissible K.μ⁻ contraction is case (a) suffix removal; (b) and (c) are excluded by the post-state invariants."

**Required**: Restructure the lemma to derive case (a) directly from the per-state invariants, without proving exhaustiveness of all three cases. If exhaustiveness over post-state shapes is needed, state it as a side remark, not the main lemma.

### Issue 9: ExtendedReachableStateInvariants "Foundation invariants" subsection duplicates the main iteration

**ASN-0047, ExtendedReachableStateInvariants proof**: The main proof iterates K.α / K.δ / K.λ / K.μ⁺ / etc., showing each preserves the invariant conjuncts. Then a "**Foundation invariants**" subsection drills into S4, S7a–d, L1b, L-fin, D-SEQ★, NodeLineage separately.

**Problem**: The two structures are duplicative. The main iteration says "K.α preserves S4 via T10a's GlobalUniqueness on the content sub-allocator; cross-document distinctness via the Cross-document disjointness chain" — the same content the Foundation invariants subsection then re-treats under "S4". This is the "two paragraphs in different sections saying the same thing" pattern.

**Required**: Either fold the Foundation invariants subsection's content into the main per-transition iteration, or restructure the proof to be entirely per-invariant (one paragraph per invariant, iterating over transitions within each). Don't have both.

### Issue 10: Worked example for K.δ k = 1 is missing

**ASN-0047, worked examples**: Provides traces for K.δ case (i) node baptism, K.δ case (ii) k = 2 account/document descent (in "Entity hierarchy by K.δ"), K.μ⁺/K.μ⁻/K.μ~ (in "Fork with subsequent insertion" and "Interior content replacement"), K.λ/K.μ⁺_L (in "Link allocation and arrangement"). The Fork example invokes K.δ k = 1 implicitly (`d₂ = 1.0.1.0.1.1 = inc(d₁, 1)`), but verification of the K.δ k = 1 case's preconditions — specifically A_v(d₁)'s activation and the T2 spawn discharge — is not exhibited.

**Problem**: Given issues 1 and 2 (the K.δ k = 1 discharge prose and the A_v activation gap), the absence of a concrete trace for K.δ k = 1 leaves the trickiest case under-verified. The Fork worked example doesn't separately check A_v(d₁)'s activation, conflating the entire fork composite into one block.

**Required**: After resolving issues 1 and 2, add a step in the Fork worked example (or a dedicated K.δ k = 1 example) explicitly verifying the A_v(d₁) activation discharge — naming the spawn point, the parent allocator, and the T2 admissibility.

## OUT_OF_SCOPE

(None — all gaps I identified relate to claims this ASN already makes. The explicit Scope section and Open Questions cover the genuine future-ASN topics.)

VERDICT: REVISE
