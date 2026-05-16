# Review of ASN-0051

## REVISE

### Issue 1: SV6 sub-claim (ii)(b) — implicit case for `t ≠ s` with proper-prefix relationship

**ASN-0051, SV6 proof, sub-claim (ii)(b)**: "We therefore split on whether t = s: ... *t ≠ s.* Then t has a first position of divergence from s. If that position lay in [1, k−1], it would be a first divergence at some j < k — excluded by the no-early-divergence fact. So the first position of divergence lies at or beyond k, and t agrees with s on positions 1 through k−1."

**Problem**: The phrase "t has a first position of divergence from s" presupposes a T1(i) (component-wise) divergence — both have a component at that position and they differ. For t ≠ s with s ≺ t (s is a proper prefix of t), there is no T1(i) divergence within the shared range 1..#s; the relationship is T1(ii). This case can arise when #ℓ > #s permits #(s ⊕ ℓ) > #s, allowing t with #t > #s to satisfy t < s ⊕ ℓ. No precondition of SV6 excludes this configuration.

The conclusion holds in this case (since k − 1 < k ≤ #s by T12, and t agrees with s on 1..#s ⊇ 1..k−1), but the prose case-split does not exhibit it.

**Required**: Either add a third sub-bullet —
- *t ≠ s with s ≺ t (proper prefix, T1(ii)):* t agrees with s on 1..#s; since k − 1 < k ≤ #s, t agrees with s on 1..k−1.

— or rephrase the "t ≠ s" sub-case to explicitly enumerate the T1(i) and T1(ii) sub-cases (T1's trichotomy at t and s within s ≤ t reduces to t = s, T1(i) divergence at some j ≤ min(#t, #s), or s ≺ t). The same gap appears in the (a) #t ≥ k argument, where #t < k under s ≺ t is impossible (since #t > #s ≥ k) but is not explicitly traced.

### Issue 2: SV11 attainment for (m ≥ 2, p ≥ 3) marked conjectural

**ASN-0051, SV11 attainment-witness discussion**: "The `(m ≥ 2, p ≥ 3)` regime is *conjectural* per the status note above — ... but no explicit p ≥ 3 witness is exhibited in this revision."

**Problem**: An ASN that proves a biconditional should either exhibit witnesses across the full satisfiable regime or scope the unwitnessed regime out. The SV11 biconditional itself is fully proved, but leaving open whether its antecedent is jointly satisfiable at (m ≥ 2, p ≥ 3) means a reader cannot answer "is m · p tight in this regime, or is the true ceiling lower?" Downstream consumers of SV11 (e.g., link-discovery policy ASNs reasoning about fragment counts) cannot rely on the bound being attained without further work.

**Required**: One of: (a) exhibit a concrete (m ≥ 2, p ≥ 3) witness saturating m · p (e.g., extend the (m, p) = (2, 2) overlap construction to three pairwise-overlapping blocks); (b) prove non-attainment in the regime structurally (e.g., show that the M7/M12 realisability constraints rule out pairwise-overlapping configurations at p ≥ 3); or (c) scope the question out with explicit deferral ("attainability characterisation at (m ≥ 2, p ≥ 3) is deferred").

### Issue 3: SV11 attainment biconditional — disjoint-pair argument relies on undefended geometric claim

**ASN-0051, SV11 disjoint-pair non-attainment case**: "In particular, span j's contribution to β_{k₁} is a *suffix* of β_{k₁}'s ordinal sequence ending at β_{k₁}'s last element, and its contribution to β_{k₂} is a *prefix* of β_{k₂}'s ordinal sequence starting at β_{k₂}'s first element."

**Problem**: The "suffix ending at last element / prefix starting at first element" claim depends on a geometric fact about how a T-convex span interacts with two disjoint blocks β_{k₁} (preceding) and β_{k₂} (succeeding): specifically, that the I-extents of β_{k₁} and β_{k₂} are not interleaved in T with elements of any *third* block β_{k₃} positioned between them. With p ≥ 3, the I-extent of an intermediate block β_{k₃} could sit between β_{k₁}'s last element and β_{k₂}'s first element in T, and the span would necessarily contain elements of β_{k₃} too — affecting the suffix/prefix structure within β_{k₁} and β_{k₂}.

The argument as stated handles the two-block (p = 2) case cleanly. Its extension to p ≥ 3 requires the auxiliary fact that the "T-region between β_{k₁}'s last contributing element and β_{k₂}'s first contributing element" contains no element of any other block, which is not established.

**Required**: Either restrict the disjoint-pair argument to the (m ≥ 2, p = 2) case where it's airtight, or extend it with the auxiliary T-betweenness analysis needed for p ≥ 3 (showing that if span j hits both β_{k₁} and β_{k₂} in any pairwise-disjoint configuration, the suffix-coalescence conclusion still follows even when intermediate blocks' I-extents lie in between).

### Issue 4: π versus locate terminology drift in SV10 discussion

**ASN-0051, SV10 (DiscoveryResolutionIndependence) prose**: The property is named "DiscoveryResolutionIndependence", but the formal statement quantifies over `π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s)` — a projection (I-side) condition, not a resolution (V-side) condition.

The accompanying prose says: "But the projection in d returns only the singleton {i₂} (proper subset of the endset's coverage), *and resolution of the from-endset in d returns only the V-positions corresponding to i₂* — the other two I-addresses have no V-positions in d."

**Problem**: The Definition section explicitly states "Resolution of endset e in document d is the function `locate(e, d)`"; the formal claim uses π, not locate. The Resolution distinction (projection answers I-side, resolution answers V-side) is exactly what SV10 should formalize, but the formal expression only addresses the I-side. The intended discovery-resolution independence — "discovery can succeed while resolution at corresponding V-positions is asymmetric" — is not the formal claim.

**Required**: Either (a) restate the property as "DiscoveryProjectionIndependence" with the current π-based statement; or (b) augment the formal statement with a `locate(Σ.L(a).s, d) ⊊ ...` conjunct that captures the V-side independence the prose discusses. As stated, the name and content don't align.

### Issue 5: SV13(e) reordering clause overloads "preserves π exactly"

**ASN-0051, SV13(e)**: "Reordering of M(d) — via the *distinguished composite* K.μ~, which expands into a K.μ⁻ + K.μ⁺ pair under ASN-0047, not an elementary transition — preserves π(e, d) exactly: the I-addresses present in the projection are unchanged at the composite endpoints (per-step π may shrink at the K.μ⁻ stage and recover at the K.μ⁺ stage; see SV5's intermediate-state note)."

**Problem**: The summary clause says "preserves π(e, d) exactly" but then immediately qualifies "at the composite endpoints" — meaning the property is *not* preserved at intermediate states. A reader scanning SV13 for the synthesised guarantee gets a misleading first impression. The qualification is correct but pushes the reader to read SV5's "Composite-level scope" subsection to know whether "exactly" really means "exactly" in this context.

This matters when SV13(e) is composed with other operations: a valid composite that touches an intermediate state of K.μ~ before completion (e.g., concurrency protocols that read state mid-composite) cannot rely on π-preservation. Nothing in the formal definitions establishes intermediate-state atomicity.

**Required**: Either prefix the reordering clause with "at composite endpoints" to match the SV5 caveat, or add a clarifying note that the projection-preservation guarantee is composite-endpoint, not pointwise across the composite's internal trajectory. The current "preserves π(e, d) exactly" reads as if K.μ~ were atomic.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
