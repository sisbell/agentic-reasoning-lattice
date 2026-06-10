# Review of ASN-0116

I checked this as a manuscript whose central risk is layer contamination: the content store must stay append-only while the arrangement is rewritten, and the two effects (allocate, shift) must not leak into each other. I traced the composite decomposition, every step-precondition, the four named invariants, the derived consequences, the wp, and all boundary cases.

The hardest obligations are discharged, not hand-waved:

- **Density/no-gap (D-SEQ★).** The post-state `V_{s_C}(d') = {q_1, …, q_{N+n}}` is established by the explicit block-disjointness fact — the three index intervals `{1,…,J−1}`, `{J,…,J+n−1}`, `{J+n,…,N+n}` are consecutive, gap-free, union `{1,…,N+n}`. Cross-checked via K.μ⁺ precondition (iii) and ExtendedReachableStateInvariants. This is the invariant most often skipped; here it is done twice, both explicitly.
- **Composite validity.** The K.μ⁻→K.μ⁺ decomposition is correctly motivated (a single K.μ⁺ is barred by prior-domain agreement since suffix slots change value; K.μ~ is barred by K.μ~-FIX since the domain grows). The five K.μ⁺ preconditions (i)–(v) are each discharged at the intermediate state, including the load-bearing ordering (K.α must precede K.μ⁺ so the block targets are in `dom(C)`), and the finiteness argument correctly pulls the link subspace's finiteness from S8-fin at the composite boundary Σ.
- **Provenance couplings.** J0/J1★/J1'★ are driven by the range identity RAN; the subtle point — that the shifted suffix is *range-old* (already in `ran(M(d))`, merely re-slotted) and therefore triggers no new R entry — is handled correctly in both the Effect and the worked example, against P4★ at the boundary.
- **Forward-merge impossibility (IP1).** `shift(a, n) ∉ dom(C')` (beyond d's frontier on `A_C(d)`) versus `M(d)(q_J) ∈ dom(C)` by S3★ is robust to the transclusion case, as claimed.
- **Non-monotone witness sets (IP4).** The analysis correctly resists the naive monotonicity assumption: the V-position sets are incomparable when a suffix witness shifts (proven via the greatest-suffix-witness argument), while the *count* and *resolved content* grow monotonically. The cross-subspace witness branch (link images of d's positions) is not skipped.
- **wp (IP6).** The derivation yields `Added ⊆ D(d,Σ)` (containment), and the ASN correctly distinguishes this from the strictly stronger emptiness form, exhibiting in the worked example a link (ℓ) that lies in `Added ∩ D(d,Σ)` — exactly the member the emptiness form over-rejects.

Boundary cases are covered and load-bearing: front insertion (J=1, the only branch exercising `n'_{s_C}=0` strict contraction), append (J=N+1, K.μ⁻ dropped), and empty-subspace with both sub-cases (a) fresh document and (b) re-insertion after full contraction, where the K.α start address is correctly governed by the *content region* rather than the (empty) arrangement.

All cross-ASN references are to foundation ASNs (0034, 0036, 0040, 0043, 0045, 0047, 0053, 0058, 0082, 0084, 0086, 0093, 0098). No reinvented foundation notation. The prose is dense but is motivational/house-style, implementation evidence, or substantive case analysis — I did not find accreted meta-prose, defensive document-ordering justification, use-site inventories, or duplicated paragraphs that I had to skip to follow a claim. The `q_k`/shift abbreviation is consistent with D-SEQ★'s canonical form.

## REVISE

None.

## OUT_OF_SCOPE

None. The ASN stays within its mandate: it uses K.μ⁻/K.μ⁺ as foundation atomics (mechanism), not as DELETE/REARRANGE, and the link clauses (IP4/IP6) reason about survival/discoverability *under* insertion without creating links. The four open questions (transclusion at the insertion point, concurrent insertion freshness, provenance under transclusion, post-edit fragmentation) are correctly deferred to the operations named in the Scope section.

VERDICT: CONVERGED
