# Review of ASN-0091

## REVISE

### Issue 1: RE-subpres proof doesn't rule out third subspace values
**ASN-0091, "Subspace preservation at the abstract level"**: The contradiction arguments establish `subspace(v) = s_C ⟹ subspace(π(v)) ≠ s_L` and `subspace(v) = s_L ⟹ subspace(π(v)) ≠ s_C`. Neither rules out `subspace(π(v))` being a third value. If `subspace(π(v))` were a value other than `s_C` or `s_L`, both clauses of post-state S3★ would be vacuously satisfied and no contradiction would emerge.
**Problem**: The proof concludes `subspace(π(v)) = subspace(v)`, but the binary case analysis is incomplete without first constraining `subspace(π(v)) ∈ {s_C, s_L}`. The conclusion as stated is stronger than what the displayed argument establishes.
**Required**: Explicitly invoke S3★-aux at Σ' (preserved by RA-adm) to first establish `subspace(π(v)) ∈ {s_C, s_L}`, after which the two cross-direction exclusions imply `subspace(π(v)) = subspace(v)` together.

### Issue 2: Worked Example 4 lacks admissibility verification
**ASN-0091, "Worked Example — Bijection Non-Uniqueness Under Shared I-Addresses"**: This example demonstrates RE-proj's uniformity across two distinct witness bijections π₁ and π₂. Unlike the first three worked examples (which include an `Admissibility (RA-adm)` block verifying S2, S3★, S8★, P4★, etc. concretely against the post-state), this example omits the admissibility verification entirely.
**Problem**: The example asserts a concrete REARRANGE_K transition `Σ → Σ'` exists with shared I-addresses, but does not verify that the constructed Σ' satisfies the foundation invariants. The bijection-non-uniqueness claim depends on the transition being admissible.
**Required**: Add an admissibility verification block analogous to the first three examples — particularly noting that S5 (UnrestrictedSharing) admits the shared `a` at both `[1, 2]` and `[1, 3]` in the post-state — or explicitly note that the verification follows the same pattern as the prior examples and is omitted for focus.

### Issue 3: RE-frag★/RE-coal★/RE-eq★ claim has no explicit witness
**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences"**: The arbitrary-direction-sequence claim — that every finite direction sequence `(s_1, ..., s_n) ∈ {+, −, =}^n` is realizable — is justified by a "spatial partitioning" construction described in prose, but no explicit `Σ_0 → Σ_1 → Σ_2` trace is exhibited demonstrating even a two-step instance.
**Problem**: The construction's feasibility — particularly the simultaneous staging of distinct I-address patterns in disjoint V-sub-ranges within a single arrangement, and the cut-sequence confinement relying on RE-ext to preserve non-target sub-ranges across steps — is asserted but not concretely verified at the level the prior worked examples set as the standard.
**Required**: Provide a concrete two-step trace (e.g., realizing `(+, −)`) showing the staged Σ_0, the first cut sequence's effect on sub-range 1 (with cardinality change verified), and the second cut sequence's effect on sub-range 2 (with cardinality change verified, while sub-range 1's post-step-1 pattern is preserved by RE-ext at step 2).

### Issue 4: Bijection-class characterization's forward direction compressed
**ASN-0091, "REARRANGE as Vstream-Only Operation"** (paragraph beginning "For a *fixed* transition `Σ → Σ'`..."): The forward direction reads "RA-π reads `Σ'.M(d)(π(v)) = Σ.M(d)(v)`, so `v ∈ Σ.M(d)⁻¹(a)` forces `π(v) ∈ Σ'.M(d)⁻¹(a)`". This establishes that π maps `Σ.M(d)⁻¹(a)` *into* `Σ'.M(d)⁻¹(a)`, but the "restricts to a bijection" claim bundles four independent inferences: (a) mapping-into; (b) injectivity from π globally injective; (c) surjectivity onto `Σ'.M(d)⁻¹(a)` from π globally surjective + the inverse pre-image argument; (d) equicardinality.
**Problem**: The characterization is correct but the forward derivation displays only (a) explicitly; (b), (c), and (d) are folded into the "bijects the partitioning blocks" phrase.
**Required**: Either lay out the four inferences explicitly, or cite that (b)–(d) follow from π's global bijectivity on finite sets.

## OUT_OF_SCOPE

### Topic 1: Link subspace rearrangement semantics
**Why out of scope**: CS3 fixes the cut subspace at s_C, and the open question "What semantics, if any, should rearrangement carry on the link subspace?" places link-subspace rearrangement in a future ASN.

### Topic 2: Topological bounds on run-decomposition cardinality
**Why out of scope**: The ASN exhibits witnesses for RE-frag/coal/eq but does not place an upper bound on the cardinality increase. The open question is appropriately deferred.

### Topic 3: Observational equivalence of distinct rearrangement transitions at the link-discoverability level
**Why out of scope**: An open question — beyond this ASN's commitment to arrangement-level characterization of REARRANGE.

### Topic 4: Realizability of arbitrary admissible bijections via cut-sequence compositions
**Why out of scope**: An open question — whether every admissibility-preserving bijection of `dom(M(d))` can be realized as a finite composition of REARRANGE_K invocations.

VERDICT: REVISE
