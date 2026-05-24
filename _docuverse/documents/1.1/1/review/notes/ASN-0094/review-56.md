# Review of ASN-0094

## REVISE

### Issue 1: NAT-sub appendix's predecessor existence cited but not derived

**ASN-0094, Appendix: Local NAT Primitives, NAT-sub Existence step Case B**: "By NAT-discrete and NAT-order, `m` has a predecessor `m' ∈ ℕ` with `m = m' + 1` and `n ≤ m'`."

**Problem**: NAT-discrete (no element between `m` and `m+1`) and NAT-order (strict total order) do not jointly entail that every positive `m ∈ ℕ` has a predecessor. This is the surjectivity of successor on positives, which requires Peano induction. NAT-wellorder gives least-element principle (hence strong induction), and the appendix uses induction freely elsewhere ("by induction on `m` over NAT-wellorder"), but the predecessor claim is asserted with a citation that points to axioms which alone are insufficient. Without an explicit derivation, the appendix's "without additional Peano-style induction" wording in the *Background facts* paragraph misleads readers about what NAT-discrete + NAT-order actually give.

A reader attempting to verify the appendix discovers that:
- Strong induction (from NAT-wellorder) on `P(m) := m = 0 ∨ ∃m'. m' + 1 = m` does close — P(0) trivial; if P(n) then n+1 has predecessor n. But this is *not* what "NAT-discrete and NAT-order" gives.
- Trichotomy + NAT-discrete contrapositive (m < n ⟹ m+1 ≤ n) helps bound positions but doesn't construct the predecessor.

**Required**: Either (a) supply the explicit Peano-induction derivation from NAT-wellorder + (Peano-zero-least), naming each step; or (b) add (Peano-pred) as a third Peano-core supplement to the appendix, alongside (Peano-rec) and (Peano-zero-least).

### Issue 2: Per-shape uniformity downgrade leaves a load-bearing gap unaddressed

**ASN-0094, Sh5(a) Status of per-shape uniformity**: "The earlier draft phrased per-shape uniformity at the body-shape level... as a *commitment* enforced by hand-review. The present draft explicitly downgrades this from a commitment to an *aspiration*..."

**Problem**: Multiple framework consumers rely on shape-mate body convergence:
- The Canonical Shape Catalog row for Resolution claims "five base templates modulo codomain shift" inherited from DirectedPair.
- The *Catalog row structure: base, opt-in, parametric* paragraph reads "Every K registered at the shape inherits the row's base templates."
- Sh5(b)'s *Signature derivation rule* states "Two registered K's at the same shape therefore inherit identical signatures for every base template."

These statements describe a property the framework downgrades to aspiration. The downgrade itself acknowledges no mechanical gate enforces template-body convergence at the same shape; a future catalog row at, say, `(1, 1, A_doc, A_doc, ⊤)` could in principle register divergent base templates from DirectedPair without violating any framework gate, and no recipe (auditor review checklist, body-shape derivation procedure from shape components) is committed.

The framework records "sharpening the aspiration to a procedural recipe... is recorded as an open work item; the present draft does not undertake it." But Sh5(b)'s *Signature derivation rule* and the catalog rows continue to read as though convergence were guaranteed.

**Required**: Either (a) sharpen the aspiration into a procedural recipe before the per-K opt-in machinery (FDD, SHCD) and parametric `_via` consumers depend on it; or (b) revise the catalog row prose and Sh5(b) to consistently surface the hand-curated status — wherever the framework says "inherit" or "shape-mate convergence," say "by the catalog's current hand-curation."

### Issue 3: AllocatedAddressAntichain's Sub-case 3b worked example exhibits a configuration forbidden by R0a-Cor2

**ASN-0094, AllocatedAddressAntichain, Worked example — Case 3 (cross-domain) walkthrough**: "Sub-case 3b... at the same numerical skeleton with side assignments swapped (taking `x' = [1, 0, 2, 0, 1, 0, 5, 1]`... and `a' = [1, 0, 2, 0, 1, 0, 5, 1, 7]`...) the L1b-faithful `a'` of length 9 used here exhibits the subspace contradiction at Step 3.3b... R0a-Cor2 closes off the vacuity earlier still."

**Problem**: The framework presents Sub-case 3b's worked example to illustrate the proof's argument path, but `a'` has `#E(a') = 3`, violating R0a-Cor2 (which strengthens L1b to `#E(·) = 2`). A reader walking the example sees Steps 3.1/3.2/3.3b unfold against a configuration the substrate-conforming layer never produces. The acknowledgment "R0a-Cor2 closes off the vacuity earlier still" appears as a parenthetical aside rather than as a structural warning to the reader.

The lemma's correctness is not at issue — Sub-case 3a's walkthrough is consistent with R0a-Cor2, and the lemma holds. The concern is pedagogical: the framework uses a structurally-impossible example as its sole concrete walkthrough of Sub-case 3b.

**Required**: Either (a) replace Sub-case 3b's example with one consistent with R0a-Cor2 (e.g., differing arguments where `#a' = #x'` but the substrate-cross-domain case still arises), or (b) prepend a clear note that Sub-case 3b's example exists only under L1b's weaker `#E ≥ 2` reading, with R0a-Cor2 closing the case earlier by length-counting alone.

### Issue 4: Sh5(b)'s exhaustiveness claim is universally framed but only checked per-row

**ASN-0094, Sh5(b)**: "every symbol appearing in a template body falls into exactly one of the six categories, with no implicit residual"

**Problem**: The universal "every symbol falls into exactly one" is asserted, then the framework provides a per-row audit table covering the 11 currently-accepted catalog rows and one rejected candidate. The exhaustiveness is verified *for the current catalog*, not for arbitrary future templates. The Sh5(b) status acknowledges this through the *minimal review checklist* (step 0–3) — a procedural per-row check — but the universal framing in Sh5(b)'s opening paragraph and in the audit table preamble conflicts with the META status the framework commits to.

A reader encountering "every symbol... no implicit residual" reads this as a closed-world theorem; the audit table's per-row classification then reads as an enumerated verification of that theorem. But the framework's actual commitment is weaker: future symbol introductions require auditor walk-through.

**Required**: Reframe Sh5(b)'s prose to match its META status — "the discipline categorizes every symbol the *current catalog's templates* cite into one of the six categories; future extensions require the per-row checklist (step 0–3 above)" — rather than asserting universal exhaustiveness.

## OUT_OF_SCOPE

### Topic 1: Multi-process consistency
Framework's atomicity premise reduces to within-call sequentiality on single-process substrates. Multi-process coordination protocols at the `~`-equivalence class scope would extend the framework rather than fill a gap.

### Topic 2: `(0, 0)` shapes
A single-tuple-existence flag with no from/to attribution. Listed as open design choice; current catalog has no demand.

### Topic 3: Composite shapes
Relations whose F or G is constrained by another relation's content. Listed as open refinement candidate.

### Topic 4: Ghost-targeting slot semantics
The framework restricts slot addresses to allocated targets; L9 admits ghosts for non-slot uses. Listed as open design choice.

### Topic 5: Sixth shape-tuple component
Whether per-K opt-ins (FDD, SHCD) should be promoted to shape-tuple components. Listed as open design choice; current opt-in encoding is reasonable.

### Topic 6: Cross-process shape registry consistency
Lifetime constancy is asserted at the substrate level within a single process. Listed as open question alongside Topic 1.

VERDICT: REVISE
