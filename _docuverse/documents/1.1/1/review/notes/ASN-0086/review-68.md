# Review of ASN-0086

## REVISE

### Issue 1: T_cat^Σ defined but never used as a load-bearing concept
**ASN-0086, Definition — TypeCatalog**: "For each state Σ, the *type catalog at Σ* is the subset actually in use: T_cat^Σ = {Θ ∈ T_admissible : (E a ∈ dom(Σ.L) :: |Σ.L(a)| = 3 ∧ Σ.L(a).e₃ = Θ)}"
**Problem**: The Definition introduces T_cat^Σ then immediately tells the reader to ignore it ("Type indices in what follows range over T_admissible, not T_cat^Σ"). T_cat^Σ does not appear in any subsequent R-claim, operation, proof, Worked Sketch step, or WP analysis. The Definition adds noise without contribution. The fact that the very next paragraph distinguishes its semantics from L_K^Σ membership (literal-equality vs. coverage-equivalence) only matters if T_cat^Σ is used somewhere — it isn't.
**Required**: Either remove the T_cat^Σ Definition entirely, or articulate at least one substantive downstream use that justifies its inclusion. If the intent is to provide a hook for future ASNs needing "which types are currently in use," state that explicitly and tag the definition as forward-facing.

### Issue 2: R6c-Corollary proof citation is incomplete
**ASN-0086, R6c-Corollary's Proof, Step 1**: "By ASN-0043's L12 (LinkImmutability) and L12a (LinkStoreMonotonicity), every arrangement-modifying step Σ_k ↦ Σ_{k+1} in ↦ \ → holds Σ_{k+1}.L = Σ_k.L pointwise"
**Problem**: L12 gives value-preservation on dom(Σ_k.L); L12a gives dom monotonicity. Together they yield only that Σ_{k+1}.L *extends* Σ_k.L — not that Σ_{k+1}.L = Σ_k.L identically. The dom-equality conclusion requires the partition fact (arrangement-modifying steps in ↦ \ → are *defined* not to extend dom(Σ.L)) established earlier in the "Broader transition relation ↦" paragraph. That paragraph already combines L12, L12a, and the partition fact to derive Σ'.L = Σ.L; the R6c-Corollary proof should cite that combined result, not L12 + L12a alone.
**Required**: Replace the citation "By L12 and L12a" with a reference to the arrangement-modification frame on ↦-steps established in the Definition of ↦, which combines all three conditions (i)–(iii).

### Issue 3: Substrate-conforming layer Definition omits ASN-0093 invariants
**ASN-0086, Definition — substrate-conforming layer**: "Concretely, this is the full invariant catalog of ASN-0043 — L0, L1, L1a, L1b, L1c, L3, L12, L12a, L14, L14a, L-fin — together with the ASN-0036 invariants S0, S1, S2, S3, S7a–d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ."
**Problem**: The enumeration omits ASN-0093's own substrate-level invariants: M0 (DocumentTumblerWellFormed), M1 (ArrangementMonotonicity), C0 (ContentImmutability), C1 (ContentElementLevel), C1b (ContentElementFieldDepth), C1c (ContentAllocatorConformance), C-fin (ContentStoreFiniteness). R7a's proof depends on the broader catalog — its deterministic K.λ replay argument invokes ChainMembershipForOrigin (an ASN-0093 lemma) which rests on these invariants. The general opening clause ("every invariant the underlying substrate ASNs posit at each step") implicitly covers them, but the explicit per-invariant list creates the misleading impression that the listed invariants are exhaustive.
**Required**: Extend the enumeration to include ASN-0093's M0, M1, C0, C1, C1b, C1c, C-fin, or remove the per-invariant list in favor of the general clause alone.

### Issue 4: Worked Sketch does not concretely demonstrate R6b
**ASN-0086, Worked Sketch**: The Sketch covers Step 0 (first-emission), Step 1 (Nullify a₁), and Step 2 (re-emit at a₂), with each step annotated by which R-claims it witnesses.
**Problem**: R6b (SingleDepthRetraction) is mentioned briefly in Step 1's computation ("Witnesses R6b. ✓") but its substantive operational content — that emitting Nullify(b₁) does NOT undo a₁'s nullified status — is never exhibited concretely. R6b's non-fixpoint semantics on retraction-of-retraction is one of the substantive lemmas (it determines that restoration is fresh emission, never recursion); without a concrete demonstration, the reader is left to infer the property from the abstract Justification alone. The Worked Sketch is the natural site for the demonstration.
**Required**: Extend the Worked Sketch with a Step 3 invoking Nullify(b₁) and verifying: (a) the second retraction is emitted at a fresh address (e.g., c₁ = 1.0.1.0.1.0.2.4 by K.λ's subsequent-emission rule at d); (b) b₁ ∈ nullified(Σ_3); (c) a₁ ∈ nullified(Σ_3) unchanged — the single-pass check over L_R^{Σ_3} still finds the original retraction tuple at b₁ targeting a₁, regardless of b₁'s own status; (d) (a₂, F₁, G₁) ∈ A_K^{Σ_3} unchanged.

## OUT_OF_SCOPE

The ASN's Open Questions section already covers the main deferred topics — multi-arity link relations, concurrent operation atomicity, cardinality bounds on nullified, cross-relation invariants with arrangements, depth-2 link addressing tightening, retraction discipline elevation, and dynamic catalog extension. No additional out-of-scope items arose from the review.

VERDICT: REVISE
