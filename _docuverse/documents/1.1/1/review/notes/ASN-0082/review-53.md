# Review of ASN-0082

## REVISE

### Issue 1: NAT-CA carries protocol-rationale and use-site-inventory prose
**ASN-0082, "The Ordinal Shift" (NAT-CA paragraph)**: "ASN-0034's NAT-* extraction likewise supplies no left-summand dominance law (no `a + b ≥ b` over ℕ); consequently the ordinal-dominance arguments below ... route entirely through tumbler arithmetic ... We state this constraint once here and do not repeat it at each use site."
**Problem**: The axiom statement (ℕ commutativity/associativity) is fine. The trailing material is meta-prose: it explains *why* the axiom is needed and *what is absent from a sibling foundation*, then inventories downstream consumers ("the ordinal-dominance arguments below ... the wp analyses") and announces a non-repetition protocol. None of this advances the claim. This is exactly the "new prose around an axiom explains why the axiom is needed" + "use-site inventory" pattern.
**Required**: Reduce NAT-CA to the axiom statement plus, at most, a one-clause note that ℕ-subtraction laws are routed through tumbler arithmetic. Delete the dominance-law aside and the "we state this once" protocol sentence.

### Issue 2: Span-algebra framing is duplicated across three sites
**ASN-0082, abstract; I3-S closing paragraph; D-S closing paragraph**: abstract — "the displacement arithmetic underlying span endpoints (reach(σ) = start(σ) ⊕ width(σ)) commutes with uniform ordinal translation"; I3-S — "**the displacement arithmetic underlying span endpoints (SpanReach) commutes with uniform ordinal translation.**"; D-S — "the same commutativity-with-shift conclusion stated at I3-S above, now realized for the contraction direction."
**Problem**: The same sentence-level conclusion appears three times. The D-S closing paragraph adds nothing beyond pointing back to I3-S. Two paragraphs in different sections saying the same thing in different words.
**Required**: State the commutativity conclusion once (at the lemma that earns it). The D-S section needs only its derivation and verification; drop the recapitulation.

### Issue 3: Forward-looking essay about MAKELINK in a structural slot
**ASN-0082, "Arrangement invariants not preserved," Case S ≠ 1**: "A composing operation on the link subspace (e.g., MAKELINK, which allocates fresh I-addresses for the gap positions) has no contiguity invariants to re-establish; it need only place the new content and re-derive S8a for the freshly populated positions."
**Problem**: This describes the obligations of a future, unspecified operation rather than establishing anything about the shift sub-operation under review. It is scope/rationale essay content occupying an invariant-analysis slot.
**Required**: The relevant fact — that the foundation imposes no D-CTG/D-MIN/D-SEQ obligation on S ≠ 1, so the shift creates no violation — is already stated in the preceding sentence. Delete the MAKELINK speculation.

### Issue 4: Second link-subspace worked example largely re-covers the first
**ASN-0082, "Link-subspace insertion: shift into a sparse, tombstone-bearing pre-state"**: introduced by "We now exercise I3 itself against the link subspace as the *active* subspace ... with a sparse, tombstone-bearing pre-state V_2(d) that does not satisfy D-CTG."
**Problem**: The preceding cross-subspace example already demonstrates that I3's derivation (S8a + S8-depth, no D-CTG) is subspace-agnostic, and the verification here re-checks the same clauses (S8a via OrdShiftHom, no D-CTG appeal). The added value — shifting *into* a former tombstone gap — is one observation surrounded by a full example restatement.
**Problem is placement/redundancy**, not the existence of a concrete check.
**Required**: Either fold the one novel observation (a shifted image legitimately landing in a former tombstone slot) into the existing cross-subspace example, or trim the new example to that single point.

### Issue 5: D-S(a) routes a single-component ℕ identity through TA4 + ReverseInverse opaquely
**ASN-0082, D-S, derivation of (a)**: "Set x = s₂ − c; the partial-inverse law `(s₂ ⊖ c) ⊕ c = s₂` at depth 1 (ReverseInverse) gives `x + c = s₂`. Then `(s₂ + c') − c = ((x + c) + c') − c = ((x + c') + c) − c` ... and the depth-1 partial inverse `(y + c) − c = y` (TA4 ... with y = x + c') cancels c to leave `x + c'`."
**Problem**: The target identity `(s₂ + c') − c = (s₂ − c) + c'` (for s₂ ≥ c) is being proved at the level of the single position-2 component, i.e. as a natural-number fact, yet the derivation threads it through two separate tumbler-arithmetic lemmas plus NAT-CA, obscuring what is essentially `(a−c)+b = (a+b)−c`. Because NAT-CA was introduced precisely because ℕ-subtraction laws are unavailable, the chain is defensible but the presentation is harder to verify than the claim warrants.
**Required**: State explicitly that the identity is a position-2 (depth-1) natural-number equality, then give the minimal lemma chain. Make clear which subtractions are tumbler `⊖` and which are the induced ℕ operation, so the reader is not left reconstructing the lift.

## OUT_OF_SCOPE

### Topic 1: Generalization of D-SEP/D-DP to ordinal depth > 1
**Why out of scope**: The depth scoping axiom (#p = 2) is explicit, and the wp analysis for S8a-post correctly identifies why depth > 2 breaks TA4's zero-prefix precondition against S8a's componentwise positivity. This is genuinely new territory (the author's second Open Question), not a defect here.

### Topic 2: Updating external references after a shift repositions a V-position
**Why out of scope**: Correctly identified as the first Open Question; external-state reconciliation is a separate concern from the arrangement-layer transformation specified here.

VERDICT: REVISE
