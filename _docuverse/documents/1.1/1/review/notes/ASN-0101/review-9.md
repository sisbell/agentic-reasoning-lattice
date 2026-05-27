# Review of ASN-0101

## REVISE

### Issue 1: Composite-substitute enumeration includes vacuous or redundant cases

**ASN-0101, "The operation" section**: The text lists three classes where the K.μ⁻ + K.μ~ composite substitute is "unavailable on a non-trivial sub-class of DEL instances":
> "every link-subspace interior deletion in a document with |V_{s_C}(d)| < 2, every content-subspace interior deletion with n_S = 1, and every content-subspace case in which all admissible permutations equal the identity."

**Problem**: Cases 2 and 3 don't establish what they claim.

*Case 2 ("content-subspace interior deletion with n_S = 1"):* When n_S = 1, the subspace has exactly one position. The only possible deletion is n=1, p=1 — removing the singleton. This is not "interior" in any meaningful sense, and K.μ⁻ alone (suffix truncation with n'_{s_C} = 0) handles it directly. DEL is not needed; the composite fails only because K.μ~ wasn't needed in the first place.

*Case 3 ("all admissible permutations equal the identity"):* With |V_{s_C}(d)| ≥ 2, a transposition is always admissible — S3★, CL-OWN, CL-UNIQ, S8a, S8-depth are all subspace-preserving permutations satisfy them. When |V_{s_C}(d)| < 2, this case is subsumed by case 1 or case 2. The case as stated appears vacuous.

**Required**: Either consolidate to the single genuine case (interior link-subspace deletion with |V_{s_C}(d)| < 2 is the killer case under obstacle #2), or articulate precisely what cases 2 and 3 add beyond case 1. The current enumeration overstates the support for DEL's primitivity.

### Issue 2: No explicit weakest precondition analysis

**ASN-0101, throughout**: The ASN provides D9 as a forward characterization of how `project` evolves under DEL, but never computes an explicit `wp(DEL[d, σ], Q)` for any non-trivial postcondition Q.

**Problem**: D9 establishes the forward relationship `project(L'(ℓ).eᵢ, d, Σ') ∩ V_S(M'(d)) = (project(L(ℓ).eᵢ, d, Σ) ∩ Λ) ∪ {σ_d(v) : v ∈ project(L(ℓ).eᵢ, d, Σ) ∩ Ρ}`, but doesn't derive the reverse — under what pre-state condition does some post-state property hold? For instance, `wp(DEL[d, σ], discoverable_from(ℓ, d, Σ'))` should reduce to a precise pre-state predicate (e.g., "the link's projection from d has at least one V-position outside X"). The review criteria explicitly call out wp analysis as required.

**Required**: Add an explicit wp computation for at least one non-trivial postcondition. The natural candidates: wp for discoverability preservation, wp for "specific V-position v is in the post-state projection", or wp for "a particular link's projection cardinality is preserved".

### Issue 3: Worked example covers only single-document case

**ASN-0101, "A worked example" and "A link-subspace example" sections**: Both examples operate on a single document `d`. The cross-document case (D9's first bullet, `d'' ≠ d`) is established by D5 + D3 but never exercised concretely.

**Problem**: A central architectural commitment of the ASN — that transclusion is safe because deletion is per-document — has no concrete verification. The review criteria require concrete examples for key postconditions, and D5 (cross-document isolation) and the corresponding D9 clause are arguably the deepest preservation claims in the ASN.

**Required**: Add a concrete example with two documents `d` and `d'` where some I-address `a` lives in both `ran(M(d))` and `ran(M(d'))` via transclusion. Show `DEL[d, σ]` removes the reference from `d`'s arrangement while `a ∈ ran(M'(d'))` and `a ∈ dom(C')`, and verify a link projecting to `a` retains discoverability from `d'`.

### Issue 4: Σ_mid distinguishability argument under-specified

**ASN-0101, "The operation" section**: The argument that K.μ~ + K.μ⁻ exposes a distinguishable intermediate state uses two predicates:
> "Either predicate distinguishes the intermediate from at least one endpoint, witnessing Σ_mid as a state distinct from both."

**Problem**: The second predicate (`M(d)(v₁) = a₁` for `v₁ ∈ Λ`) is conditioned on "whenever the permutation moves elements of Λ" — but the natural permutation that moves X to the suffix leaves Λ fixed entirely. The text claims this predicate distinguishes Σ_pre from Σ_mid but only under a condition that may not hold for the most natural composite. A cleaner argument: π ≠ id (required by K.μ~) directly forces some v with M_mid(d)(v) ≠ M_pre(d)(v), giving Σ_mid ≠ Σ_pre without needing to argue about Λ vs Ρ specifically.

**Required**: Replace the Λ-conditional argument with the simpler "π ≠ id ⟹ ∃v : M_mid(d)(v) ≠ M_pre(d)(v) ⟹ Σ_mid ≠ Σ_pre" argument, which doesn't depend on which region the permutation moves.

### Issue 5: D8 Group (i) S2 disjointness argument compressed

**ASN-0101, D8 justification**: The functionality argument states:
> "S2 holds by the construction of M'(d): the sources Λ, Q, and V_{S'}(d) for S' ≠ S each provide a single value for each position, and they cover disjoint subsets of the post-state domain."

The disjointness of Λ ∩ Q relies on the last-component ranges: Λ has last component ≤ p−1, Q has last component in {p, ..., n_S−n}.

**Problem**: When n = n_S−p+1 (the maximum permitted by the containment precondition), Q's range {p, ..., n_S−n} = {p, ..., p−1} = ∅, so Q = ∅ trivially disjoint from Λ. When n < n_S−p+1, the ranges are genuinely disjoint. The boundary behavior of Q's defining range when the integer interval becomes degenerate is not commented on, even though it intersects the "deletion at the end" boundary case and the "singleton interior" case where these endpoints can coincide.

**Required**: Note explicitly that Q's last-component range {p, ..., n_S−n} is non-empty iff n < n_S−p+1, and that when this range is empty Q = ∅ (handled in the "Ρ = ∅" boundary case). The disjointness of Λ ∩ Q then has two routes: non-vacuous range comparison vs. trivial vacuity. This matters because boundary cases must verify D8 explicitly, and the discharge route differs.

### Issue 6: S9 (TwoStreamSeparation) not explicitly addressed

**ASN-0101, D8**: The lists in Groups (i), (ii), (iii) do not include S9 (TwoStreamSeparation, ASN-0036).

**Problem**: S9 is a foundation transition predicate: "Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(C) :: a ∈ dom(C') ∧ C'(a) = C(a))". DELETE is precisely an arrangement-modifying transition, so S9's antecedent fires and the consequent must be verified. D2 establishes the consequent (`dom(C') = dom(C)` with values preserved), so S9 holds — but D8 should explicitly list it. Currently a reader has to derive that S9 is covered.

**Required**: Add S9 to D8's Group (iii) with the one-line justification "by D2".

### Issue 7: ChainEnumerationInjectivity and substrate invariants from ASN-0093

**ASN-0101, D8 Group (ii)**: The text lists invariants but does not mention the substrate-level ChainEnumerationInjectivity, ChainUniformLength, ChainUniformZeroCount, or FirstEmissionFreshness lemmas from ASN-0093.

**Problem**: These are derivations from `dom(C)` and `dom(L)` being unchanged, but the connection should be noted — these lemmas characterise the structure of allocator chains, and DEL must not perturb them. With `dom(C') = dom(C)` and `dom(L') = dom(L)`, the chain structures are pointwise preserved, but D8 should mention this in Group (ii) (alongside C1, C1b, C1c).

**Required**: Add a brief mention in D8 Group (ii) that the substrate's chain-discipline lemmas (ChainEnumerationInjectivity, ChainUniformLength, etc.) hold trivially because `dom(C') = dom(C)`, `dom(L') = dom(L)`, and the chain structure is a structural property of these domains.

## OUT_OF_SCOPE

### Topic 1: Versioning and historical reconstruction

The ASN's "Note on recoverability" section discusses J4 ForkComposite and the relationship between DEL and versioning. The substantive treatment of versioning (creating versions, traversing version DAGs, reconstructing prior states) belongs in a separate ASN — explicitly out of scope here.

### Topic 2: Recoverable DELETE / UNDO

The open questions raise reversibility, fully-reversible DELETE, and causal ordering across documents. These are downstream concerns appropriate for future ASNs on undo, time-travel queries, and inter-document causality.

### Topic 3: Link resurrection and ghost projection mechanics

The orphaned-then-re-projected pattern is mentioned (and follows LP18 in ASN-0098). A full treatment of operations that intentionally rebuild discoverability of dormant links is downstream.

### Topic 4: Implementation-level concerns

Auxiliary indices, tree representation, and orphan enumeration are explicitly called out as out of scope by the ASN itself ("Boundaries the abstract specification does not cross" section).

VERDICT: REVISE
