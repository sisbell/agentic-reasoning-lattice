# Review of ASN-0121

## REVISE

### Issue 1: State model declared as a triple, then reasoned over as the ASN-0047 five-tuple

**ASN-0121, "What is being matched" (intro)**: "We write the system state as `Σ = (Σ.C, Σ.M, Σ.L)` — the content store, the family of document arrangements, and the link store."

**ASN-0121, "The answer is forced"**: "K.δ extends `Σ.E` (and, for documents, `dom(Σ.M)`) while framing `Σ.C`, `Σ.L`, and `Σ.R` fixed ... K.ρ writes only `Σ.R`."

**Problem**: The state is declared as a three-tuple `(Σ.C, Σ.M, Σ.L)`, but the monotonicity argument that underwrites FL-RET/FL-MON/FL-STB ranges over the full ASN-0047 vocabulary and explicitly reads `Σ.E` and `Σ.R` — components that do not exist in the declared triple. The transition vocabulary `→` the ASN adopts (K.δ, K.ρ included) operates on ASN-0047's five-tuple `(C, L, E, M, R)`. The declared state and the state the proofs quantify over are not the same object.

**Required**: Declare the state as ASN-0047's five-tuple, and state once that `findlinks` reads only the `(L)`-projection (and addresses) — making explicit that `Σ.E`, `Σ.R`, `Σ.C`, `Σ.M` enter only the surrounding transition vocabulary, not the query.

### Issue 2: No weakest-precondition analysis for any operation that can change the result

**ASN-0121, FL-MON / FL-RET**: stated as monotonicity facts across transitions.

**Problem**: The ASN observes (correctly) that `findlinks(q, ·)` is a function of the link store alone, so the *only* operation that can alter the result is K.λ (link creation, including retraction tuples). That makes the natural, non-trivial weakest precondition computable and informative — yet it is never computed. For a freshly created link `ℓ` from K.λ with value `(F,G,Θ)` homed at `d`:

  `wp(K.λ, "ℓ ∈ findlinks(q, ·)") ≡ liftH(d, q.H) ∧ lift(F, q.F) ∧ lift(G, q.G) ∧ lift(Θ, q.Θ)`

(ℓ fresh ⟹ `ℓ ∉ nullified`, so addressability drops out). FL-MON and FL-RET are monotonicity statements, not a wp computation, and the rubric calls out missing/trivial wp analysis as a depth gap. Sibling foundation ASNs supply explicit wp (ASN-0098 LP12a; ASN-0086 "wp Case 1/2").

**Required**: Add an explicit wp derivation for the one class of transition that changes the result — appearance of a newly created link in the answer, and persistence under a retraction-bearing K.λ — naming premises and showing the chain.

### Issue 3: Decidability of the matching predicate is never established

**ASN-0121, "The satisfaction rule"**: `touch(e, r) ≡ coverage(e) ∩ coverage(r) ≠ ∅`.

**Problem**: The ASN repeatedly treats `findlinks` as a realizable query (Gregory's index, "snapshot," "the answer as a whole"), but never establishes that `touch` — hence `sat`, hence the result set — is decidable. The exactly-analogous concern was discharged in the foundation as a load-bearing lemma (ASN-0086 CoverageEqualityDecidable, by cell decomposition of finite span-unions). Coverage-intersection-nonemptiness is decidable by the same argument, but the ASN neither states nor derives it. As written, `findlinks` is a mathematically defined set with no guarantee an alternative implementation can compute it.

**Required**: State and discharge "`touch(e, r)` is decidable" (finite endsets ⟹ finite interval unions ⟹ cell-wise membership comparison, cf. ASN-0086 CoverageEqualityDecidable), and note the result is finite (subset of `dom(Σ.L)`, L-fin).

### Issue 4: The request grammar is described in prose but never formally typed

**ASN-0121, "What is being matched"**: "The home-component `H` ranges over the *organizational-prefix* axis: its spans are rooted at node-, account-, or document-level addresses."

**Problem**: The formalism (`athome(a, H) ≡ home(a) ∈ coverage(H)`, FL-DEF) imposes no such restriction on `H`, and the restriction is nowhere used or enforced — an element-rooted `H` is admissible and simply vacuous (its coverage contains no document-level `home(a)`). So the prose reads like a typing constraint that the definitions do not carry. The request type is never given a formal definition (`q ∈ (Endset ∪ {∗})⁴`, with or without a constraint on `H`), leaving it ambiguous whether prefix-rooting is a well-formedness condition or merely conventional usage exercised in Trace 6.

**Required**: Either formalize the request type and the `H` constraint (and show where it is load-bearing), or drop the prose restriction and state that `H` is an arbitrary endset, with prefix-rooted spans being the intended convention.

## OUT_OF_SCOPE

### Topic 1: Version-/time-qualified inquiry
Recovering a link retracted in the current state via a prior version is correctly left to a future ASN (Open Question 1); FL-RET is properly scoped to current addressability.

### Topic 2: V-spec ↔ I-address request agreement
The invariant connecting arrangement-mediated request phrasing to the I-address regime (Open Question 2) is new territory, not an error here.

### Topic 3: Cross-store federation
Reaching links homed in independently administered stores (Open Question 5) is beyond the single-state semantics of this operation.

VERDICT: REVISE
