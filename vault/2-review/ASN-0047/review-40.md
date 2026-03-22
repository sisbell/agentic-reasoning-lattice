# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ dom_C(M(d)) = ∅ argument uses S3★ and K.μ⁺ amendment before they are established

**ASN-0047, Elementary transitions, K.μ~**: "S3★ at the *pre*-state gives M(d)(v) ∈ dom(L) (since v is link-subspace). But K.μ⁺'s referential integrity precondition requires M'(d)(π(v)) ∈ dom(C), and dom(C) ∩ dom(L) = ∅ (L14) — contradiction."

**Problem**: The dom_C(M(d)) = ∅ case is presented as a self-contained proof within the "Elementary transitions" section, but it relies on two results that have not been established at that point: (a) S3★ (defined and proved in the "Generalized referential integrity" section, several sections later), specifically its link-subspace clause `M(d)(v) ∈ dom(L)` for link-subspace v; (b) the K.μ⁺ content-subspace amendment (defined in the "Amendments" section, immediately following). The text says "K.μ⁺ (amended)" without flagging the amendment as a forward reference, though the subsequent dom_C ≠ ∅ paragraph does flag forward references explicitly ("the K.μ⁺ amendment (below)," "the S3★ analysis… below"). This asymmetry makes the dom_C = ∅ argument appear verified when it depends on an inductive hypothesis (S3★ at the pre-state) that is only available within the ExtendedReachableStateInvariants induction.

**Required**: Either (a) defer the dom_C = ∅ argument to the S3★ section where it can be verified in reading order, or (b) mark the argument as depending on forward references with the same explicitness as the dom_C ≠ ∅ paragraph — e.g., "Assuming S3★ at the pre-state (established inductively in ExtendedReachableStateInvariants below) and the K.μ⁺ content-subspace amendment (§Amendments below)…"

### Issue 2: ReachableStateInvariants theorem statement omits invariants established by its proof

**ASN-0047, Coupling and isolation, Theorem (Reachable-state invariants)**: "Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies P4, P6, P7, P7a, P8, S2, S3, S8a, S8-depth, S8-fin, D-CTG, and D-MIN."

**Problem**: The inductive step references "P0/P1/P2 by the permanence lemma" and "S2/S3/S8a/S8-depth/S8-fin/D-CTG/D-MIN by the arrangement invariants lemma." The theorem statement enumerates the arrangement invariants (from the arrangement lemma) but not the permanence properties (from the permanence lemma), creating an asymmetry: both lemma groups are used in the proof, but only one appears in the statement. The ExtendedReachableStateInvariants corrects this by listing all invariants including P0, P1, P2, P3★, P5★, S0, S1, and S8. A downstream ASN referencing the four-component theorem might not realize P0–P2 are guaranteed at every reachable state, since the permanence lemma is stated as a per-composite property ("every valid composite transition satisfies…") rather than as a reachable-state invariant.

**Required**: Either (a) add P0, P1, P2 to the four-component theorem statement (matching the extended version's comprehensive approach), or (b) add a note explaining that the four-component theorem lists only state-intrinsic properties, with the permanence lemma providing the complementary transition-level guarantees. The current text does neither.

### Issue 3: K.μ~ consequence — dom(M'(d)) = dom(M(d)) — not derived

**ASN-0047, Elementary transitions, K.μ~**: "there exists a bijection π : dom(M(d)) → dom(M'(d)) such that (A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))"

**Problem**: The definition allows dom(M'(d)) ≠ dom(M(d)) — π is a bijection between potentially different sets. The opening prose says "V-positions may change without adding or removing mappings," which is accurate only if dom(M'(d)) = dom(M(d)). In fact, the D-SEQ shape of V_S at both input and output, combined with the bijection's equal cardinality per subspace (from subspace preservation via S3★ + L14 in the extended state, or trivially in the four-component state), forces V_S(d') = V_S(d) for each subspace S, hence dom(M'(d)) = dom(M(d)). This makes π a permutation of a fixed domain — a significant simplification that collapses the distinction between "changing V-positions" and "permuting I-address assignments at fixed V-positions." The ASN never states or derives this consequence. Without it, a reader might believe K.μ~ can shift V-positions (e.g., compacting a gap), when it cannot.

**Required**: Derive the corollary that dom(M'(d)) = dom(M(d)) from D-SEQ + bijection cardinality + subspace preservation. State it as a named consequence of K.μ~. This also simplifies the K.μ~ decomposition analysis: the intermediate K.μ⁻ + K.μ⁺ round-trip restores the same domain with permuted values.

## OUT_OF_SCOPE

### Topic 1: Endset referential integrity
**Why out of scope**: K.λ stores link values (F, G, Θ) with endset spans that may reference addresses not in dom(C). Whether endset spans must reference allocated content is a constraint of the MAKELINK operation, not of the elementary transition K.λ. The ASN correctly defers this to operation specifications (explicitly excluded from scope). The open question on "permanence properties for content that participates in link endsets" acknowledges the gap.

### Topic 2: Link-subspace reordering via contraction and re-extension
**Why out of scope**: K.μ~ preserves link-subspace mappings identically (link-subspace fixity), preventing link reordering through reordering transitions. However, K.μ⁻ (suffix truncation of the link subspace) followed by K.μ⁺_L (re-adding links in a different order) achieves the same net effect through a different path. This is a valid composite that the transition framework permits. Whether this should be constrained — and what invariants link ordering must satisfy — relates to the open question on link withdrawal invariants and link-specific ordering constraints.

VERDICT: REVISE
