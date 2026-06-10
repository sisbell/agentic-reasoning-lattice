# Review of ASN-0127

This is a careful, dense note. The two-phase factoring is clean, the keystone meta-lemma (F-CIL) is the right abstraction, and the existence/discovery taxonomy is well-motivated. The algebraic lemmas (F-UDIST, F-IMONO, F-VDIST), the stability chain (F-PRES → F-INERT → F-LAMBDA), and the existence-anchoring results (E-INV, E-MONO, E-CONS) all check out, including the careful LP13-vs-LP3★ distinction in E-INV (arity *and* per-slot coverage, not coverage alone). F-IMG-SWING's cardinality argument and its non-injective witness are correct and admissible as a K.μ~ transition. D-NONMONO's case split is exhaustive over `V_atomic ∪ {K.μ~}`, and D-CWP's weakest precondition (`A = A ∪ B ⟺ B ⊆ A`) is right and non-trivial. The issue is in the one place the note grounds itself concretely.

## REVISE

### Issue 1: The worked illustration uses coverage values that no endset can produce

**ASN-0127, "Worked illustration"**: "`L_1 = ({a_1}, {a_3}, Θ)` … `e₂ ∩ {a_1, a_2} = {a_3} ∩ {a_1, a_2} = ∅`, and the type slot `e₃ ∩ {a_1, a_2} = {a_θ} ∩ {a_1, a_2} = ∅` since `a_θ ∉ {a_1, a_2, a_3}`."

**Problem**: The example treats each endset's coverage as the literal singleton address it names (`coverage(e₁) = {a_1}`, `coverage(e₂) = {a_3}`, `coverage(e₃) = {a_θ}`). No endset has singleton coverage. By PrefixSpanCoverage (foundation), the minimal span `(x, δ(1, #x))` has `coverage = {t ∈ T : x ≼ t}` — the entire subtree of `x`, which always contains `x.0, x.1, …` and is therefore infinite. A union of spans only enlarges this. So every coverage value used in the note's sole concrete verification is unrealizable.

Under the correct semantics `coverage = subtree(·)`, the example's conclusions survive, but only under an assumption the note never states: that `a_1, a_2, a_3, a_θ` are *mutually prefix-incomparable*. Concretely:
- "L_1 matches via slot 1" needs `subtree(a_1) ∩ {a_1, a_2} = {a_1}`, i.e. `a_1 ⋠ a_2`;
- "`e₂ ∩ {a_1, a_2} = ∅`" needs `subtree(a_3) ∩ {a_1, a_2} = ∅`, i.e. `a_3 ⋠ a_1 ∧ a_3 ⋠ a_2`;
- "`e₃ ∩ {a_1, a_2} = ∅`" needs `a_θ ⋠ a_1 ∧ a_θ ⋠ a_2` — `a_θ ∉ {a_1,a_2,a_3}` is *not* sufficient on its own; a prefix relation would still pull the descendant in.

The stated emptiness/non-emptiness therefore rides on prefix-incomparability, not on the singleton coverages the text computes with. A reader mapping the example back to the model hits a contradiction with a foundation the note itself depends on for `coverage`.

A related smaller slip in the same passage: slot 1 is intersected against the singleton witnesses (`e₁ ∩ {a_1}`, `e₁ ∩ {a_2}`) while slots 2 and 3 are intersected against the full query set `{a_1, a_2}`. The intersection target should be the query I-set throughout.

**Required**: Make the verification faithful — either (a) write the endsets as actual spans, use `coverage({(a_i, δ(1, #a_i))}) = {t : a_i ≼ t}`, and state that `a_1, a_2, a_3` are content-chain siblings (prefix-incomparable by T10a.2) and `a_θ` is a cross-subspace type address, so each `coverage ∩ {a_1, a_2}` reduces to the claimed value; or (b) explicitly declare the address-set shorthand and the prefix-incomparability premise it silently relies on. Either way, intersect every slot against the full query I-set.

### Issue 2: F-IMG-SWING asserts the injective-regime motion without a witness

**ASN-0127, F-IMG-SWING**: "Under injective `Σ.M(d)` only membership change is realizable."

**Problem**: The note proves cardinality is fixed under injective `Σ.M(d)` (`|π⁻¹(R) ∩ dom| = |R ∩ dom|` carries to equal-size images) and witnesses the *non-injective* cardinality gain. It never witnesses that the image moves at all under injective `Σ.M(d)` — the only supplied witness is non-injective. The positive half of the claim ("membership *can* change") is asserted but, in the injective regime specifically, unrealized; a skeptic could ask whether injective `M` leaves every image fixed. Given the note's own standard (it bothers to witness the harder non-injective case), the easier claim deserves the same treatment.

**Required**: Add a one-line injective witness, e.g. `Σ.M(d): v₁ ↦ a, v₂ ↦ b` (injective), `R = {v₁}`, transposition reorder `π = (v₁ v₂)` sends `image(R, d, Σ) = {a}` to `image(R, d, Σ') = {b}` — same cardinality, membership changed.

## OUT_OF_SCOPE

### Topic 1: Content-keyed queries through `Σ.C`, uniform discovery wp, and composition with ASN-0098's `project`
**Why out of scope**: The four open questions (content-keyed vs arrangement-keyed queries; slot-filter distributivity; the uniform wp generalizing D-CWP across the whole K-vocabulary; composition of `image()` with the LP** projection results) are correctly identified as future territory. The note deliberately defines `image` as the forward V→I map, complementary to ASN-0098's backward `project`, and does not duplicate it — the composition belongs in a successor ASN, not here.

VERDICT: REVISE
