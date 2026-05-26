# Review of ASN-0091

## REVISE

### Issue 1: RE-trans★ multi-step argument is misdirected

**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences", RE-trans★ subsection**: "the unrestricted ★ form delivers only (i) + (ii) for the transclusion at d — the home-document arrangement may have undergone its own permutation in the interim, though the transclusion relationship at d remains intact because each rearrangement at `origin(a)` itself preserves `origin(a)`'s range (RE-ran applied at the step targeting `origin(a)`), so `a` remains in `ran(Σⱼ.M(origin(a)))` for every j."

**Problem**: The justification rests on the wrong predicate. Clause (i) of the transclusion is `a ∈ ran(Σ.M(d))`, which concerns d's range, not `origin(a)`'s range. Whether `a` remains in `ran(Σⱼ.M(origin(a)))` is irrelevant to whether `a` remains in `ran(Σⱼ.M(d))`. The clean argument is: at each step i, either step i targets d (giving `ran(Σᵢ.M(d)) = ran(Σᵢ₋₁.M(d))` by RE-ran) or it doesn't (giving `Σᵢ.M(d) = Σᵢ₋₁.M(d)` by RE-other, hence range preservation). Composing across n steps preserves `ran(M(d))` and `μ_a(M(d))` — that is what supports (i) and (ii). The detour through `ran(M(origin(a)))` is non-load-bearing.

**Required**: Replace the prose with the per-step preservation argument over `ran(M(d))` (RE-ran when step targets d, RE-other otherwise). State explicitly that the per-step ran/μ preservation chains transitively.

### Issue 2: 4-cut swap not concretely demonstrated

**ASN-0091, "Worked Example"**: The entire worked example exercises only the 3-cut pivot. R-SPERM (4-cut swap) is mentioned in Section 1 but never traced.

**Problem**: The ASN claims that all RE-* properties hold uniformly across both 3-cut pivot and 4-cut swap (via R-PPERM and R-SPERM respectively), but supplies no concrete witness for the 4-cut case. RE-trans has a non-trivial structural test under 4-cut swap (a μ-region transclusion can land between α and β post-state with width difference `w_β − w_α`, which is not exercised by any pivot). RE-frag's behaviour under 4-cut is also unexamined — does w_α ≠ w_β affect run cardinality in a structurally distinctive way?

**Required**: Add a 4-cut concrete trace, verifying each RE-* claim against specific values. Include a case where w_α ≠ w_β so the μ-region's net displacement is non-zero (per ASN-0084's R-DISP).

### Issue 3: RE-proj citation of RE-cov is incorrect

**ASN-0091, "Projection Transports Along π"**: "For each `v ∈ project(e, d, Σ)`, the V-position `π(v)` holds the same I-address (RA-π), and that address remains in coverage (RE-cov), so `π(v) ∈ project(e, d, Σ')`."

**Problem**: For a general endset `e` passed as a parameter to project, `coverage(e)` is a function of `e` alone — it does not depend on state (per the foundation definition in ASN-0098). The step "remains in coverage" is trivial because `coverage(e)` does not change between Σ and Σ'. RE-cov is a claim about coverage of link-slot endsets `Σ.L(a).eᵢ`, which is invariant because `Σ.L(a)` is invariant. The citation conflates two different facts.

**Required**: Either rephrase to note that `coverage(e)` is state-independent by definition of coverage, or restrict the RE-proj statement to link-slot endsets and cite RE-cov consistently throughout.

### Issue 4: RE-frag direct witness conflates content-subspace and total cardinality

**ASN-0091, "Run Decomposition Is Not Invariant"**: The direct witness ("a maximal run `(v, a, n)` with `n ≥ 2`") uses a pre-state with three content-subspace V-positions and no link-subspace V-positions. The post-state run cardinality is computed as "2" (post-state) vs. "1" (pre-state).

**Problem**: RE-frag is stated as a claim about "the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)`" — the total cardinality across all subspaces. The witness implicitly has total = content-only, but this is never stated. A reader checking RE-frag against the worked example (where total includes a shared link-subspace run) needs the connection made explicit.

**Required**: State explicitly that the direct witness has empty link subspace, so total cardinality equals content-subspace cardinality, and the strict increase is at the total level. Alternatively, modify the witness to include the link subspace.

### Issue 5: Abstract class admissibility not stated

**ASN-0091, Section 1**: The abstract Vstream-only class is defined via RA-dom, RA-π, RA-frame only. Foundation invariant preservation at Σ' is not part of the class definition.

**Problem**: Without an admissibility constraint, the abstract class admits bijections π that violate foundation invariants at Σ' (e.g., a π mapping a content-subspace V-position to a link-subspace V-position would violate S3★ + L14). Such transitions are not valid in the foundation transition system. The author treats the abstract class as "Vstream-only on d" without naming the admissibility constraint that distinguishes valid REARRANGE transitions from arbitrary bijection-witnessed RA-π satisfiers. K.μ~'s admissibility clause (i) supplies this, but the ASN never inherits it explicitly at the abstract level.

**Required**: Add an admissibility clause to the abstract class definition — either by importing K.μ~ admissibility (i) explicitly, or by requiring "Σ' satisfies every foundation invariant Σ satisfies." Without this, RE-sub's framing as "the one consequence that does not flow from the abstract class alone" is suspect — RE-sub *does* follow at the K.μ~ level (S3★ + L14 force subspace preservation), just not the strict-bijection level. Either justify why the abstract class is the strict version, or attribute RE-sub more carefully.

### Issue 6: Identity-exclusion claim about REARRANGE_K is over-strong

**ASN-0091, Section 1**: "REARRANGE_K excludes this degenerate case via ASN-0084's K.μ~ admissibility clause (ii) alone (`π ≠ id`); the existence precondition `|dom_C(M(d))| ≥ 2` plays an independent role..."

**Problem**: REARRANGE_K's cut sequence construction makes π non-identity *automatically* — the construction itself forces `π(c₀) ≠ c₀` because `c₀ + w_β + 0 ≠ c₀` when `w_β ≥ 1` (and R-PRE forces `w_β ≥ 1`). Clause (ii) is satisfied by construction, not used to exclude cases. The framing "clause (ii) alone excludes" suggests clause (ii) is doing work that the cut sequence has already done.

**Required**: State that the cut-sequence construction makes π non-identity by construction (because `w_α, w_β ≥ 1`), and clause (ii) is the formal vehicle confirming this. Alternatively, drop the discussion of clause (ii) as the "exclusion mechanism" since it's redundant with the cut-sequence structure.

## OUT_OF_SCOPE

### Topic 1: Span-level transclusion preservation guarantees

Open Question 1 ("cross-document transclusion when a cut splits a span transcluded from the same source document") asks for guarantees at the span-level, where RE-trans only delivers I-address-level guarantees. This is a legitimate future topic — it would require a span-of-transclusion abstraction not yet developed in the foundation.

**Why out of scope**: Span-level transclusion as a primitive is new territory beyond ASN-0091's focus on per-address arrangement permutation. The author correctly identifies this as an open question.

### Topic 2: Link-subspace REARRANGE semantics

Open Question 2 asks what semantics rearrangement should carry on the link subspace. ASN-0091 establishes that REARRANGE_K (cut subspace = s_C) leaves link subspace unchanged.

**Why out of scope**: An operation that rearranges the link subspace would be a new operation; defining its invariants is future work.

### Topic 3: Realisability of arbitrary bijections by cut composition

Open Question 5 asks whether every admissible bijection of dom(M(d)) can be realized by finite cut-sequence compositions. This is a completeness theorem about REARRANGE_K vs. the abstract K.μ~ class.

**Why out of scope**: A completeness theorem deserves its own ASN; ASN-0091 establishes properties of the abstract class and one realization, leaving the realization-vs-class gap for future work.

VERDICT: REVISE
