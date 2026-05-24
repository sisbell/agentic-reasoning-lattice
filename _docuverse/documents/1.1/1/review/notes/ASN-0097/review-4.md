# Review of ASN-0097

## REVISE

### Issue 1: Π15a's S3 invocation contradicts the worked example's d_link setup

**ASN-0097, §Independence from Arrangement (Π15a proof) and §A Worked Example (Initial state Σ₀)**: The proof states "By S3 (ReferentialIntegrity, ASN-0036), ran(Σ_pre.M(d)) ⊆ dom(Σ_pre.C) for every d ∈ E_doc" and combines this with "the disjointness dom(Σ.L) ∩ dom(Σ.C) = ∅" to derive ℓ ∉ ran(Σ_pre.M(d)). But the worked example sets `Σ₀.M(d_link) = {0 ↦ ℓ}` where ℓ ∈ dom(Σ₀.L).

**Problem**: Under the cited S3 plus cited disjointness, ℓ ∈ dom(Σ₀.L) forces ℓ ∉ dom(Σ₀.C), which by S3 forces ℓ ∉ ran(Σ₀.M(d_link)) — directly contradicting the worked example's placement of ℓ at V-position 0 of d_link. The framework's documented support for link subspaces (Vocabulary: documents have "two element subspaces: text content (subspace 1) and links (subspace 2)") means M(d) must be able to range over link addresses, but S3 as stated forbids this. The ASN cannot internally rely on both formulations.

**Required**: Either (a) restate S3 in subspace-specific form (e.g., ran(M(d)|_text) ⊆ dom(C) and ran(M(d)|_links) ⊆ dom(L)); (b) replace Π15a's proof with a direct global-freshness argument from K.λ over all current state including ran(M(d)); or (c) revise the worked example's d_link to be consistent with S3 as stated. As written, Π15a's proof and the worked example cannot both stand.

### Issue 2: Π15a's two-part freshness argument is conflated by "either"

**ASN-0097, §Independence from Arrangement (Π15a proof)**: "K.λ ... produces a link address ℓ fresh with respect to the prior allocation state; in particular ℓ ∉ dom(Σ_pre.L), and under the disjointness dom(Σ.L) ∩ dom(Σ.C) = ∅ ... ℓ ∉ dom(Σ_pre.C) either."

**Problem**: The word "either" suggests both facts share a derivation, but they don't. ℓ ∉ dom(Σ_pre.L) follows from allocator freshness over the link store. ℓ ∉ dom(Σ_pre.C) requires a structural premise — that ℓ inhabits a link subspace disjoint from the content subspace — which is alluded to by "for s_C-resident content" but never spelled out. A reader cannot reconstruct what guarantees the second non-membership.

**Required**: Decompose explicitly: (i) by allocator freshness, ℓ ∉ dom(Σ_pre.L); (ii) by allocator type, ℓ ∈ s_L (link subspace); (iii) by address-space partitioning, s_L ∩ s_C = ∅; (iv) therefore ℓ ∉ dom(Σ_pre.C). Step (ii)/(iii) must be made overt.

### Issue 3: The "I-side equivalent of reach" is used as a lemma without being labeled

**ASN-0097, §Backward Lookup: Discovery**: An equivalence — `reaches(ℓ, d, V_q, Σ) ⟺ (E i :: cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q}) ≠ ∅)` — is proved in prose between the definition of reaches and Π16. Π16's proof then says "We invoke the I-side equivalent of reaches proved above."

**Problem**: Every other substantive claim is labeled Π0–Π17 or appears in the claims table. This equivalence is a load-bearing lemma cited downstream, but is not labeled, not in the table, and not searchable by name. The chain of dependencies in §Backward Lookup is harder to track because of this.

**Required**: Promote the equivalence to a labeled Π (or labeled lemma) and add it to the claims table. The proof is sufficient; only structural elevation is needed.

### Issue 4: Π4's proof asserts negations about transitions rather than deriving them

**ASN-0097, §Permanence of Link Structure (Π4 proof)**: "Slot positions are permanent by Π2; no transition swaps, reorders, or relabels slots; no transition reinterprets the directional role of an existing slot."

**Problem**: The first clause cites Π2. The second and third clauses are universal negations over the transition vocabulary ("no transition does X") stated without derivation. As written they read as restatements rather than consequences. The actual chain — Π0 forces Σ'.L(ℓ) = Σ.L(ℓ), so the tuple is preserved component-wise; by L6/L7, directional role is a function of slot position; hence directional role is preserved — is not made explicit.

**Required**: Derive the directional permanence from Π0/Π2 plus L6/L7 in one or two sentences, rather than asserting negations about the transition vocabulary.

## OUT_OF_SCOPE

### Topic 1: COPY semantics across documents
COPY (mentioned in vocabulary) creates a new I-address. How a link's projection behaves across a COPY whose source is in cov(eᵢ) is not analyzed. This belongs to a future ASN on COPY semantics, not a defect here.

### Topic 2: Composite atomic transitions
The closed form Π11(d) covers K.μ⁻, K.μ⁺, K.μ~ in isolation. Compound atomic operations (e.g., a single atomic allocate-and-arrange) are not analyzed. The closed form would hold by composition; explicit treatment is reasonable future work.

### Topic 3: Discovery-primitive completeness
One of the listed open questions ("What is the minimal information a discovery primitive must consult to be complete") is appropriately deferred to a discovery-mechanism ASN.

VERDICT: REVISE
