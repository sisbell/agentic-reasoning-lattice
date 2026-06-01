# Review of ASN-0086

## REVISE

### Issue 1: Worked-example freshness cites the wrong ASN-0093 lemma
**ASN-0086, Worked Sketch, Step 1**: "witnessing R0 (TupleAddressFreshness): `b₁ ∉ dom(Σ_0.L)` is fresh by **FirstEmissionFreshness's generalization through subsequent emissions** (chain elements are distinct...)."
**Problem**: `b₁ = inc(a₁, 0)` is a *subsequent* emission (the predicate `{ℓ' : origin(ℓ') = d} = {a₁} ≠ ∅` fires). ASN-0093 supplies a dedicated lemma, SubsequentEmissionFreshness, for exactly this case — and R0's own proof cites it for the subsequent branch. The worked example instead invents a non-existent "generalization" of FirstEmissionFreshness (which is stated only for the empty-homed-set first emission). This is a hand-wave where a foundation lemma is directly available, and it is internally inconsistent with R0.
**Required**: Cite SubsequentEmissionFreshness for `b₁` (and likewise for `a₂`, `b₂` in Steps 2–3), matching R0's proof.

### Issue 2: R0a Case 1 proves a redundant second direction
**ASN-0086, R0a, Case 1**: the "Reverse direction: `¬(a' ≼ a)`" paragraph.
**Problem**: R0a quantifies `(A a, a' ∈ dom(Σ.L))` over *ordered* pairs. Proving `¬(a ≼ a')` for an arbitrary distinct-home pair `(a, a')` already discharges `¬(a' ≼ a)` by instantiating the same argument at `(a', a)`. The reverse paragraph is a verbatim-symmetric relabeling of the forward one and advances no new reasoning — exactly the "two paragraphs say the same thing in different words" pattern the anti-bloat classifier names.
**Required**: Delete the reverse direction; note that the conclusion follows for the swapped pair by symmetry of the quantifier.

### Issue 3: Foundation sets and properties re-badged under new notation
**ASN-0086, Definitions A^Σ / A_doc^Σ / A_rel^Σ; table rows R2/R3/R4**: `A_doc^Σ = dom(Σ.C)`, `A_rel^Σ = dom(Σ.L)`; "R2 ... (= L12)", "R3 ... (= L12a + R2)", "R4 ... (= SD)".
**Problem**: `A_doc`/`A_rel` are pure aliases for `dom(Σ.C)`/`dom(Σ.L)`, and R2/R3/R4 are foundation properties (L12, L12a, SD) restated with new labels and new names (TupleAddressPermanence, TupleAddressDisjointness). Standard 7 forbids reinventing notation a foundation already defines; the relational view gains nothing from renaming the stores, and R4's content ("`A_doc^Σ ∩ A_rel^Σ = ∅`") is literally SD with substituted symbols. The ceremony obscures which lemmas carry actual new content (R6a–c).
**Required**: Use `dom(Σ.C)`/`dom(Σ.L)` directly (or justify why a partition alias earns its keep), and demote R2/R3/R4 to one-line citations of L12/L12a/SD rather than full restated lemmas.

### Issue 4: Meta-prose around dependency provenance and notation
**ASN-0086, R6b**: "This half rests on the Definition alone... This cross-state half is not definitional — it depends on R3." **Emit_K Definition**: the parenthetical "(The address-returning convention ... is metonymic: the state is ambient...)". **Nullify / WP**: repeated deferrals "...discharged in Case 1 of the Weakest-Precondition Analysis below."
**Problem**: These are provenance annotations and notation apologetics, not reasoning. R6b's "(i)/(ii)" split narrates *which premise* each clause leans on rather than stating the claim; the metonymy paragraph explains a notation choice; the cross-section deferrals point forward without advancing the local argument. This is the meta-prose accretion the appended classifier flags.
**Required**: State R6b's two facts plainly; drop the dependency commentary and the metonymy paragraph; replace forward deferrals with the result stated once at its home.

### Issue 5: "strictly shrinks A_K" overstated in R6c Consequence
**ASN-0086, R6c Consequence**: "a single retraction emission strictly shrinks `A_K` at every type whose tuple address it covers (witnessed by R6c's set-difference: `(a, F, G) ∈ A_K^Σ ∩ (L_K^{Σ'} \ A_K^{Σ'})`...)."
**Problem**: The strict shrink holds only if the covered tuple `(a, F, G)` was *active* at Σ (`a ∉ nullified(Σ)`). If `a` was already nullified, the retraction adds an `L_R` tuple but `A_K` is unchanged — precisely the situation the worked Step 3 exhibits (`A_K^{Σ_3} = A_K^{Σ_2}`). The parenthetical silently assumes `(a, F, G) ∈ A_K^Σ`, contradicting the "at every type ... it covers" universal.
**Required**: Condition the strictness on the covered tuple being active, or restate as "shrinks (non-strictly)."

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations `L_K^{(n)} ⊆ A_rel × ℘(A)^n`
**Why out of scope**: The note explicitly restricts `L^Σ` to standard-triple links and defers `|Σ.L(a)| > 3` to an Open Question. R0a/R0a-Cor2 already cover all arities structurally; the relational construction over higher arities is genuinely new territory, not a defect here.

### Topic 2: Concurrency / atomicity consistency model for Observe vs. Emit
**Why out of scope**: The substrate's SequentialAtomicTransitions axiom (ASN-0093) totally orders transitions; a concurrent observation model is new specification, correctly listed under Open Questions.

VERDICT: REVISE
