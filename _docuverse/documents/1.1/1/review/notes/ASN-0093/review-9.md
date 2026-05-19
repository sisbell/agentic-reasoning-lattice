# Review of ASN-0093

I'll examine this allocation-substrate ASN for rigor in its claims, proofs, and operation specifications.

## REVISE

### Issue 1: T10a.8 application to non-tree-embedded chains is meta-argued, not formally derived

**ASN-0093, "Remark — T10a chain-lemma applicability to non-tree-embedded chains"**: "Inspection of the proofs of T10a.1, T10a.7, and T10a.8 in ASN-0034 confirms that the three lemmas decompose into two groups with distinct dependency profiles... The substrate substitutes the TA5a-based per-step propagation above for that T10a.4 citation, removing the tree-embedding dependency from T10a.8 when applied to sub-allocator chains."

**Problem**: T10a.8's formal precondition in ASN-0034 reads "Allocator with base address t₀, producing siblings by inc(·, 0), conforming to T10a." The substrate's chains are explicitly *not* claimed to be standalone T10a allocators ("the substrate makes no commitment about whether an implementation realises A_C(d)/A_L(d) as standalone T10a allocators"). T10a.8 therefore cannot be cited directly. The Remark's argument that T10a.8's *proof structure* generalizes when an alternative T4-validity source is substituted is meta-reasoning about T10a.8's proof, not a formal application of T10a.8.

**Required**: State a separate named lemma (e.g., "ChainUniformZeroCount") with explicit preconditions ("inc(·, 0)-extension chain with T4-valid first element") and a self-contained proof mirroring T10a.8's induction structure. Cite this new lemma where the ASN currently cites T10a.8. The same treatment should apply to any other T10a.* citation against substrate chains where the lemma's stated precondition isn't formally discharged.

### Issue 2: Chain-element T4-validity is established only in a Remark, not as a named lemma

**ASN-0093, throughout**: Chain-element T4-validity is referenced multiple times (in ChainPrefixExtension's step case, in K.α/K.λ freshness derivations against dom(L) via T7, in StoreT4Validity's proof, in the SubAllocatorAxiom derivable-clauses Remark) but is established only inline within the "T10a chain-lemma applicability" Remark: "FirstEmission supplies a T4-valid first emission... TA5a... propagates T4-validity to every chain element".

**Problem**: A property consumed in this many downstream sites should be a first-class lemma with explicit preconditions, postcondition, and proof. As stated, readers must locate the relevant phrase within a Remark whose primary purpose is meta-reasoning about T10a's lemmas. The dependency on this property is also not surfaced in the "Properties Introduced" table.

**Required**: Extract a named lemma ChainElementT4Validity with the form: "For every d ∈ dom(M) and every chain index n ≥ 1, the n-th element of A_C(d) (resp. A_L(d)) is T4-valid." Proof: induction on n with FirstEmission as base and TA5a (k=0 unconditional) as step. Add to the Properties Introduced table. Cite this lemma directly at consumption sites.

### Issue 3: SubAllocatorAxiom mixes axiom and derived content

**ASN-0093, SubAllocatorAxiom**: "Disjoint and FirstEmission's freshness conclusion are derivable from the remaining clauses (see Remark — derivable clauses); kept in the axiom for citation convenience."

**Problem**: An axiom block containing derivable clauses obscures what the substrate is actually committing to as primitive. The ASN itself notes "A leaner axiom retaining only Exists + FirstEmission's structural form + ChainDiscipline suffices." If derivable, these clauses should be lemmas. The current structure makes it harder to verify the axiom's minimality — a reader must work through the derivable-clauses Remark to identify which content is primitive.

**Required**: Strip Disjoint and FirstEmission's freshness conclusion from the axiom. Restate each as a named lemma with its derivation. The substantive axiomatic content (Exists, FirstEmission's structural form, ChainDiscipline) becomes a leaner three-clause axiom.

### Issue 4: ChainMembershipForOrigin's T10a.7 contrapositive argument is muddled

**ASN-0093, ChainMembershipForOrigin proof at K.α subsequent emission**: "T10a.7 (EnumerationInjectivity, applicability justified by the *T10a chain-lemma applicability* remark) gives strict monotonicity `m < n ⟹ t_m < t_n`, whose contrapositive `t_m ≥ t_n ⟹ m ≥ n` combined with `a' ≤ a_prev` (the lex-order max-property) yields `m ≤ n_prev`."

**Problem**: The contrapositive direction stated is `t_m ≥ t_n ⟹ m ≥ n`, but the application needs `t_m ≤ t_{n_prev} ⟹ m ≤ n_prev`. These are not the same instantiation — the contrapositive must be applied with `m` and `n` swapped: from `m < n ⟹ t_m < t_n` (universal in `m, n`), instantiate at `(n_prev, m)` to get `n_prev < m ⟹ t_{n_prev} < t_m`, contrapositive `t_m ≤ t_{n_prev} ⟹ m ≤ n_prev`. The presentation merges these into one step in a way that's hard to follow.

**Required**: Replace with explicit two-line derivation: "By T10a.7, `n ↦ t_n` is strictly monotone, hence injective and order-preserving in both directions. From `a' = t_m`, `a_prev = t_{n_prev}`, and `a' ≤ a_prev` (lex-order max), conclude `m ≤ n_prev`."

### Issue 5: Discharge matrix omits lemma preservation across transitions

**ASN-0093, "Discharge of stated invariants"**: The matrix has rows for each invariant (M0, M1, C0–C2, C-fin, L0–L14, L-fin) and columns for K.σ, K.α, K.λ. It does not include rows for ChainPrefixExtension, ChainMembershipForOrigin, or StoreT4Validity.

**Problem**: The Simultaneous-induction framing paragraph states that "all stated invariants together with the ChainPrefixExtension lemma, the ChainMembershipForOrigin lemma, and the StoreT4Validity corollary are proved by simultaneous induction." The matrix is the natural place to display this discharge structure but only shows the invariant half. ChainMembershipForOrigin's preservation is proved in its own section; StoreT4Validity's preservation is left implicit; ChainPrefixExtension is a chain-indexed property not state-dependent. The reader must reconstruct the lemma-preservation argument from scattered material.

**Required**: Either (a) extend the matrix with rows for each lemma showing how each transition preserves it, or (b) state explicitly in the matrix's preamble which properties are transition-indexed and which are chain-indexed, with pointers to where each lemma's preservation argument resides.

### Issue 6: Base case verification doesn't address derived lemmas

**ASN-0093, "Base case verification (at Σ₀ = (∅, ∅, ∅))"**: Lists which invariants are vacuously or trivially satisfied at Σ₀. Does not explicitly verify ChainPrefixExtension, ChainMembershipForOrigin, StoreT4Validity at the base.

**Problem**: For a simultaneous induction, the base case must hold for *every* property in the IH conjunction. The reader should not have to reconstruct that ChainMembershipForOrigin's base is "both intersections empty for every d, vacuously" or that StoreT4Validity's base is "vacuous over empty stores."

**Required**: Add a sentence to the Base case section: "Derived lemmas at Σ₀: ChainPrefixExtension holds vacuously since `dom(M₀) = ∅`; ChainMembershipForOrigin holds vacuously since both `dom(C₀)` and `dom(L₀)` are empty; StoreT4Validity holds vacuously over empty stores."

### Issue 7: Cross-document disjointness Case A's zero-count argument assumes more than M0 alone

**ASN-0093, Cross-document disjointness lemma, Case A**: "by the T4 zero-count argument above; #d₁ + 1 ≤ #d₂ since #d₁ < #d₂"

**Problem**: The argument that `d₂[#d₁+1] ≠ 0` chains: (1) `d₁ ≼ d₂` plus the prefix equality clause forces `d₂`'s first `#d₁` positions to match `d₁`'s; (2) `zeros(d₁) = 2` (M0 at `d₁`) places two zeros in those positions; (3) `zeros(d₂) = 2` (M0 at `d₂`) forces no further zeros in `d₂`. Step (2) requires M0 at *both* `d₁` and `d₂`, but the proof's prose only invokes "M0 at d₂". Both are needed to fix the zero locations.

**Required**: Clarify the dependency: "By M0 at `d₁`, `zeros(d₁) = 2`, and by `d₁ ≼ d₂` these two zero positions are inherited by `d₂` at the same indices. By M0 at `d₂`, `zeros(d₂) = 2`, so `d₂` has no further zeros; in particular `d₂[#d₁+1] ≠ 0`."

### Issue 8: ChainPrefixExtension's step case uses TA5-SigValid without first asserting chain-element T4-validity

**ASN-0093, ChainPrefixExtension proof, Step case**: "By the chain-element T4-validity established in the *T10a chain-lemma applicability* remark above (FirstEmission's T4-valid first emission + TA5a per-step under `k = 0` unconditional preservation), `t_n` is T4-valid; TA5-SigValid (SigOnValidAddresses, ASN-0034) then pins `sig(t_n) = #t_n = #d + 3`."

**Problem**: The step at chain index n+1 establishes ChainPrefixExtension at n+1 using `t_n`'s T4-validity. But `t_n`'s T4-validity is itself proved by induction on chain index — there's a hidden second induction nested inside ChainPrefixExtension's induction. Without separating chain-element T4-validity into its own prior lemma (Issue 2), the proof structure conflates two inductions.

**Required**: Establish chain-element T4-validity as a standalone lemma proved by chain induction (separate from ChainPrefixExtension). Then ChainPrefixExtension's induction cites this lemma for `t_n`'s T4-validity at each step — no nested induction.

### Issue 9: K.σ does not state that the address space outside dom(C) ∪ dom(L) ∪ dom(M) is admissible

**ASN-0093, K.σ precondition**: "`d ∉ dom(M)` (fresh document address)"; "`ValidAddress(d) ∧ zeros(d) = 2`".

**Problem**: The substrate doesn't require `d ∉ dom(C) ∪ dom(L)` explicitly. The note argues this is automatic: "Since no address can simultaneously satisfy zeros = 2 and zeros = 3, d ∉ dom(C) ∪ dom(L) is forced by the precondition list together with C1/L1." The argument is sound, but freshness against `dom(M)` itself is only stated; what about against tumblers that, while not in dom(M), are sub-allocator anchors of other documents (b_C(d') or b_L(d'))? Since the anchors are not in dom(M), nothing in the precondition list forbids `d = b_C(d')` for some `d' ∈ dom(M)`.

If `d = b_C(d')` for `d' ∈ dom(M)`, then `zeros(d) = 3` (by the anchor's structural form), violating the precondition `zeros(d) = 2`. So this case is excluded. But the substrate hasn't explicitly traced this: an anchor has `zeros = 3` ≠ 2, so K.σ's `zeros(d) = 2` precondition rules out anchor collisions.

**Required**: Add a one-sentence note: "Cross-anchor freshness: anchors b_C(d') and b_L(d') for d' ∈ dom(M) have zeros = 3, so K.σ's precondition `zeros(d) = 2` rules out collision with any sub-allocator anchor."

### Issue 10: The "T10a-discipline-satisfying chains" notion is informal

**ASN-0093, SubAllocatorAxiom.ChainDiscipline**: "the substrate treats these chains as T10a-discipline-satisfying chains — finite inc(·, 0)-extension chains whose elements inherit the per-chain disciplines of T10a (T10a.1, T10a.7, T10a.8) — without claiming that A_C(d) and A_L(d) are embedded in T10a's global allocator tree as standalone allocators with spawning triples."

**Problem**: "T10a-discipline-satisfying chain" is introduced as terminology but never formally defined. The intended definition appears to be "an inc(·, 0)-extension chain with a T4-valid first element, satisfying T10a.1, T10a.7, T10a.8" — but this circular (the lemmas being inherited are themselves the defining content). A cleaner approach: define a structural predicate "T10a-conforming sibling stream" purely in terms of the recurrence `t_{n+1} = inc(t_n, 0)` and T4-validity of `t_1`, then prove that such streams satisfy T10a.1, T10a.7, T10a.8 (or their generalized forms per Issue 1).

**Required**: Add an explicit definition of "T10a-discipline-satisfying chain" with the structural-only characterization, separating it from the claim that the per-chain disciplines hold. The proof obligations become explicit.

## OUT_OF_SCOPE

### Topic 1: Activation lifetime of sub-allocator chains across cross-allocator interactions

The substrate's SubAllocatorAxiom.Exists activates A_C(d) and A_L(d) when d enters dom(M). Once active, M1 keeps them active. But the axiom doesn't address what happens if a downstream ASN introduces a mechanism by which an entire document is *forgotten* — not the substrate's concern, but worth noting that any future "document retirement" operation would conflict with SubAllocatorAxiom.Exists.

**Why out of scope**: Document retirement / arrangement-removing transitions are deferred (the Scope section excludes K.μ family and the explicit removal-of-d cases). The current discipline that "M1 makes activations permanent" is the substrate's correct posture.

### Topic 2: Cross-subspace sub-allocators beyond s_C and s_L

The Open Questions section already flags "Sub-allocator stratification beyond A_C(d) and A_L(d). Future subspace identifiers s ≥ 3 would require parallel sub-allocators; the present axiom commits to exactly two (content and link)."

**Why out of scope**: Correctly identified as a future-ASN extension.

### Topic 3: K.λ's endset spans pointing to addresses outside dom(C) ∪ dom(L)

L4 in ASN-0043 allows endset spans to reference arbitrary tumblers (not necessarily in any store). The substrate inherits this. No ghost-endset discipline is imposed.

**Why out of scope**: ASN-0043 deliberately leaves endset address admissibility open; the substrate appropriately doesn't tighten this. Any future "endset referential integrity" discipline would be a higher-layer concern.

VERDICT: REVISE
