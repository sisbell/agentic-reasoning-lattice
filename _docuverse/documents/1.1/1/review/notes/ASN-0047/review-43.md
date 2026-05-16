# Review of ASN-0047

## REVISE

### Issue 1: K.λ allocation description has notation and operator errors
**ASN-0047, Link allocation (K.λ)**: "in which case t = [d.0.s_L.0] is the link-prefix base and ℓ = [d.0.s_L.0.1] is the minimum element-level link address under d"
**Problem**: For d = [1, 0, 1, 0, 1] and s_L = 2, parsing the dot-notation as component concatenation gives [d.0.s_L.0] = [1, 0, 1, 0, 1, 0, 2, 0] with zeros = 4, and [d.0.s_L.0.1] = [1, 0, 1, 0, 1, 0, 2, 0, 1] with zeros = 4. Both contradict L1's requirement zeros(ℓ) = 3. The worked example shows ℓ = 1.0.1.0.1.0.2.1 (length 8, zeros = 3), which corresponds to [d.0.s_L.1] without the extra zero. Additionally, going from [d, 0, s_L] to [d, 0, s_L, 1] requires inc(·, 1) (descent), not inc(·, 0) (sibling). The precondition uniformly claims "inc(t, 0)" but only the V_{s_L}(d) ≠ ∅ branch uses sibling allocation; the first-link branch requires descent.
**Required**: Fix the notation to [d.0.s_L.1] (no trailing zero before the 1), and either split the precondition into two cases with different inc operators, or describe the allocation chain via L1c's chain-existential directly (with k₁ = 2 from the document, k₂ = 0 to advance to subspace s_L, k₃ = 1 to descend to the first element). The current wording produces tumblers that violate L1.

### Issue 2: "We include links in E_doc" contradicts formal definitions
**ASN-0047, Definition (Entity set)**: "E_doc = {e ∈ E : IsDocument(e)} — documents and links" followed by "We include links in E_doc"
**Problem**: ASN-0045's IsDocument requires zeros(t) = 2; L1 (ASN-0043) requires zeros(ℓ) = 3 for links. Therefore IsDocument(ℓ) is false for any link ℓ, and ¬(ℓ ∈ E_doc) follows from the formal definition. The comment "documents and links" in E_doc's stratification and the prose "We include links in E_doc" are inconsistent with E_doc's definition. In the extended state (C, L, E, M, R), links inhabit L (separate component), not E. The K.λ precondition correctly places ℓ ∉ E (since ℓ has zeros = 3 and E excludes elements). 
**Required**: Remove the "documents and links" framing from E_doc. Clarify that links are in L (a distinct state component), with origin(ℓ) ∈ E_doc relating links to their owning documents. The phrase "We include links in E_doc" should be deleted or replaced with "Links are owned by documents (origin(ℓ) ∈ E_doc) but inhabit a separate state component L, not E_doc."

### Issue 3: K.μ~ definition does not explicitly require subspace-preserving bijection
**ASN-0047, K.μ~ (Arrangement reordering)**: "there exists a bijection π : dom(M(d)) → dom(M'(d)) such that: (A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))"
**Problem**: The bijection π is not constrained to preserve subspaces. A π that maps a link-subspace v to a content-subspace π(v) satisfies the stated K.μ~ contract (preserving S8a, S8-depth, D-CTG, D-MIN at the output is possible in principle). Such a π would give M'(d)(π(v)) = M(d)(v) ∈ dom(L) at a content-subspace V-position, violating S3★. The ASN derives subspace preservation indirectly through the K.μ⁻ + K.μ⁺ decomposition and link-subspace fixity, but the K.μ~ definition itself permits subspace-violating π. The "distinguished composite" framing carries the constraint implicitly. 
**Required**: Add subspace preservation as an explicit precondition of K.μ~: `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))`. This makes the constraint visible at the definition site rather than buried in the decomposition analysis.

### Issue 4: Foundation ASN amendments not properly identified
**ASN-0047, multiple sites**: 
- L0 in "Link store and extended system state" includes both an L-clause and a C-clause; ASN-0043's L0 only has the L-clause
- L3 (amended) changes |Σ.L(a)| ≥ 3 to Σ.L(a) = (F, G, Θ) (fixed triple) and drops the non-empty type-endset clause
- D-CTG★ and D-MIN★ remove ASN-0036's link-subspace exemption, strengthening contiguity to apply universally per-subspace
**Problem**: ASN-0036 and ASN-0043 are listed as foundation ASNs that this ASN may use but not modify. The amendments above modify foundation invariants without flagging this as exceptional. The text mentions "amends ASN-0043's L3" for L3 but does not similarly identify the L0 C-clause as new (it appears as if it were ASN-0043's L0). D-CTG★/D-MIN★ are presented as "amendments" but to a foundation ASN.
**Required**: Either (a) explicitly identify each foundation amendment, with rationale and a statement that the foundation should be updated to incorporate them, or (b) introduce new property names (L0★, L3★, D-CTG★, D-MIN★) without describing them as amendments to the foundation, treating them as new properties this ASN introduces. The current presentation conflates "extending a property in this ASN" with "amending a foundation ASN."

### Issue 5: SC-NEQ stated as fact but not labeled as an axiom
**ASN-0047, Link store and extended system state**: "**SC-NEQ (SubspaceDistinctness).** `s_C ≠ s_L`. This is the structural precondition for every disjointness argument in this ASN."
**Problem**: SC-NEQ is load-bearing for L0, L14, T7-based disjointness, but it is not derived from anything in the foundation or in this ASN — it must be an axiom. The label "SC-NEQ" and the description "structural precondition" suggest something axiomatic but the status is not explicit. Properties like NoDeallocation (ASN-0034) and S0 (ASN-0036) are clearly labeled axioms; SC-NEQ should be similarly identified.
**Required**: Label SC-NEQ explicitly as an axiom of this ASN, e.g., "**SC-NEQ (Axiom, SubspaceDistinctness).** `s_C ≠ s_L`."

### Issue 6: Permanence-from-frames lemma does not address L
**ASN-0047, Lemma (Permanence from elementary frames)**: "Every valid composite transition satisfies P0, P1, and P2."
**Problem**: In the extended state, L is also append-only with immutable values (captured by L12). The Permanence-from-frames lemma should establish that the elementary frames also preserve L12 — K.λ extends L preserving existing entries; all other transitions hold L in frame. The current lemma only claims P0, P1, P2. In the extended ExtendedReachableStateInvariants theorem, L12 is asserted but the per-step derivation is folded into "Class (a) elementary invariants" rather than into the permanence lemma.
**Required**: Extend the permanence-from-frames lemma in the extended state to include L12, paralleling P0 for C: every elementary transition's frame yields `dom(L) ⊆ dom(L') ∧ (A ℓ : ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`. Alternatively, introduce a Class (a) sub-lemma covering all the append-only-with-value-preservation invariants uniformly.

### Issue 7: K.μ⁻ admissibility precondition references D-CTG★/D-SEQ★ defined later
**ASN-0047, K.μ⁻ (Arrangement contraction)**: "*Admissible removal (per-subspace suffix or full-subspace clearance).* By the per-subspace amendment of D-CTG★, D-MIN★, and the derived D-SEQ★, each non-empty subspace S at the input has `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}`..."
**Problem**: K.μ⁻ is presented in the "Elementary transitions" section. Its admissibility precondition cites D-CTG★, D-MIN★, and D-SEQ★, all of which are defined in the later "Amendments to existing transitions" section. The forward reference makes the K.μ⁻ precondition unreadable on first encounter without skipping ahead.
**Required**: Either reorder the document so that the D-CTG★/D-MIN★/D-SEQ★ definitions precede the elementary transitions, or restate K.μ⁻'s admissibility precondition in self-contained terms (e.g., explicit per-subspace suffix removal without appeal to the amended D-* names).

### Issue 8: K.λ does not verify L1b (#E(ℓ) ≥ 2)
**ASN-0047, K.λ (LinkAllocation)**: The precondition lists zeros(ℓ) = 3, fields(ℓ).E₁ = s_L, origin(ℓ) = d, but does not require #E(ℓ) ≥ 2.
**Problem**: L1b (ASN-0043) requires #E(ℓ) ≥ 2 for every link address. The K.λ structural requirement produces ℓ from inc on the link allocator's frontier, and the resulting ℓ should have #E(ℓ) ≥ 2 — but this is not stated. From the worked example, ℓ = [1, 0, 1, 0, 1, 0, 2, 1] has E = [2, 1] with #E = 2, satisfying L1b. The intermediate t = [d, 0, s_L] = [1, 0, 1, 0, 1, 0, 2] has #E = 1, violating L1b — but t is not in dom(L), only ℓ is. The precondition should make explicit that ℓ satisfies L1b.
**Required**: Add #E(ℓ) ≥ 2 to K.λ's precondition (or derive it explicitly from the inc chain via L1c), preserving L1b for the new entry.

### Issue 9: Link withdrawal restriction under D-CTG★ understated
**ASN-0047, Orphan links and coupling flexibility**: "Valid link-subspace contractions are suffix truncations: for V_{s_L}(d) = {[s_L, 1, …, 1, k] : 1 ≤ k ≤ n}, the result must be {[s_L, 1, …, 1, k] : 1 ≤ k ≤ n'} for some 0 ≤ n' < n."
**Problem**: ASN-0036's D-CTG explicitly exempts the link subspace from contiguity ("tombstones is permitted"); this ASN strengthens it. The consequence is severe: a user cannot withdraw a single arbitrary link if other links exist after it — the user must withdraw all subsequent links first. This contradicts Nelson's design where withdrawn links transition to "not currently addressable" status (LM 4/9) regardless of position. The ASN defers to an open question on the withdrawal mechanism, but the practical impact — that withdrawal of arbitrary links is impossible under the current rules — should be acknowledged in the body, not just in the open questions.
**Required**: Add a paragraph in the D-CTG/D-MIN amendment section noting that this strengthening renders single-link withdrawal at non-maximum positions impossible, that this conflicts with Nelson's tombstoning design, and that resolution is deferred to the open question. The current open question lists this as an unresolved invariant choice but does not flag that K.μ⁻'s amended precondition forbids the operation entirely.

### Issue 10: K.δ for non-root entities — inc chain incomplete
**ASN-0047, K.δ (Entity creation)**: "the address is produced by a T10a-conforming allocation event: e = inc(t, k) for some t ∈ T with origin(t) = parent(e), with k ∈ {0, 1, 2}"
**Problem**: A single inc(t, k) cannot in general produce e from any t with origin(t) = parent(e). For example, creating a document e = [N, 0, U, 0, D] under account parent(e) = [N, 0, U] requires k = 2 (adding two positions: zero separator and D value). But for a sibling document e = [N, 0, U, 0, D+1] from an existing document t = [N, 0, U, 0, D], we'd use inc(t, 0). Yet origin(t) = N.0.U = parent(e), as required — but t itself is a document, not an account. The phrase "origin(t) = parent(e)" mixes two different conditions: when k = 0 (sibling), t is at the same level as e (origin matches parent); when k > 0 (descent), t is at parent's level (t is in parent's domain). The single condition origin(t) = parent(e) is ambiguous.
**Required**: Distinguish the cases. For k = 0: t must be a previously allocated address at e's level under parent(e). For k > 0: t must be a previously allocated address at parent(e)'s level (or be parent(e) itself for the depth-step from parent). Clarify what "origin(t) = parent(e)" means for each case.

### Issue 11: K.μ⁺ value-preservation under domain extension argument
**ASN-0047, K.μ⁺ (Arrangement extension)**: "Functionality (S2) is preserved: dom(M'(d)) ⊃ dom(M(d)) with value preservation at existing positions means new entries are assigned at positions outside dom(M(d)), so M'(d) remains a function — extending a partial function at disjoint domain elements cannot introduce ambiguity."
**Problem**: The justification assumes new V-positions are outside dom(M(d)). This follows from the strict containment `dom(M'(d)) ⊃ dom(M(d))` and value preservation at existing positions, but the argument is implicit. What if K.μ⁺ "extends" by adding a new mapping at a V-position already in dom(M(d)) with a different value? The strict containment and value-preservation conjunction would fail (since the value at the existing position changed), so this case is excluded by definition. The argument is correct but underdeveloped.
**Required**: State explicitly that K.μ⁺'s simultaneous requirement of strict domain extension AND value preservation at existing positions forces new mappings at positions disjoint from dom(M(d)). The K.μ~ decomposition discussion relies on this property; making the argument explicit at K.μ⁺'s definition would strengthen the foundation.

### Issue 12: SC-NEQ derivation from foundation is asserted but not shown
**ASN-0047, Link store and extended system state**: "By T7 (SubspaceDisjointness, ASN-0034), `s_C ≠ s_L` implies that no tumbler can be both a content address and a link address."
**Problem**: T7 is referenced as a foundation result, but T7 (per ASN-0034 statements) refers to T7 (FirstElementFieldDistinction), which addresses element-field distinction within a document. The connection between T7 and "no tumbler can be both a content address and a link address" — that is, dom(C) ∩ dom(L) = ∅ for distinct subspace identifiers — needs the additional premises (a) every content address has fields(a).E₁ = s_C, (b) every link address has fields(a).E₁ = s_L. These premises come from L0, not T7. The derivation chain is L0 + T7 → L14, not just T7.
**Required**: State the derivation chain explicitly: L0 (subspace partition) + SC-NEQ (axiom) + T7 (first-element-field distinction) implies L14 (store disjointness). Currently the ASN cites T7 as if it alone implies the disjointness.

## OUT_OF_SCOPE

### Topic 1: Concrete operations (INSERT, DELETE, COPY, REARRANGE, MAKELINK)
**Why out of scope**: Listed as explicitly out of scope; this ASN only specifies elementary transitions and the composite invariants they must satisfy.

### Topic 2: Withdrawal mechanism for arbitrary-position link removal
**Why out of scope**: Already an open question. The required mechanism (tombstoning, status flags, or alternative contiguity weakening) belongs in a future ASN.

### Topic 3: Concurrency and allocation atomicity for K.λ
**Why out of scope**: Already an open question; concurrent allocator coordination is a separate concern from the abstract transition model.

### Topic 4: Refractive following for transcluded link inheritance under forking
**Why out of scope**: Mechanism for sharing link discoverability through transclusion belongs in a separate analysis.

VERDICT: REVISE
