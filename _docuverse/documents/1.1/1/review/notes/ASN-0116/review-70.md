# Review of ASN-0116

## REVISE

No REVISE items. The load-bearing arguments were checked in detail rather than taken on trust; the checks and their outcomes follow, so the verdict is auditable.

**Composite validity (ValidComposite★ discharge).** The claim that no single K-atomic realises the arrangement change is correct: the shift rewrites values at existing suffix positions (forbidden by K.μ⁺'s prior-domain agreement) while strictly growing the domain (forbidden by K.μ⁻ and, via K.μ~-FIX, by K.μ~). The exhibited sequence K.α(×n) → K.μ⁻ → K.μ⁺ → K.ρ(×n) discharges each step's precondition at the correct intermediate state: the K.α steps leave M untouched (so K.μ⁻'s D-SEQ★-shaped retention formula evaluates against the pre-state arrangement, which is a composite boundary); K.μ⁻'s strict-contraction requirement `J−1 < N` holds across the full range `1 ≤ J ≤ N`, including the front-insertion case `n'_{s_C} = 0`, which the worked example exercises explicitly; K.μ⁺'s five obligations (targets in dom(C), S8a/S8-depth of added positions, density of the resulting content run, content-subspace restriction, strict-but-finite growth) are each discharged with named premises, the finiteness argument correctly routing the link subspace through S8-fin at the boundary rather than asserting it.

**Coupling constraints.** J0/J1★/J1'★ are evaluated boundary-to-boundary as ValidComposite★ requires. The range identity RAN (`ran(M'(d)) = ran(M(d)) ∪ A_new`, shifted-suffix addresses range-old) is derived, not asserted, and correctly drives all three: J1★'s quantifier over `E'_doc` is exhausted via F-ENT, the `d' ≠ d` instances are discharged by F-DOC, and J1'★'s range-new requirement on `R' ∖ R` holds because A_new is fresh against both stores, hence absent from any pre-state range by S3★.

**Allocation contiguity.** The identification of the k-th K.α's `a_prev` with the (k−1)-th in-insert allocation follows from ChainMembershipForOrigin (contiguous initial segment) plus ChainEnumerationInjectivity (strictly increasing, so newest = max), both cited in the document; both emission branches at k = 0 (fresh region vs. post-contraction non-empty region) are worked, including the re-insertion sub-case (b) where `V_S(d) = ∅` but the content region is not — a boundary easy to get wrong and handled correctly here.

**IP1's merge analysis.** The forward-merge impossibility argument is sound and non-trivial: `shift(a, n)` lies strictly beyond the post-allocation origin-`d` frontier (ChainMembershipForOrigin) and off every other origin's chain (CrossDocumentDisjointness), so it is outside `dom(C')`, while the suffix head `M(d)(q_J)` is inside `dom(C)` by S3★ — the argument holds for transcluded suffix content, as claimed. The backward-merge possibility is correctly conceded rather than hand-waved.

**IP4's decomposition and counting.** The four parts are pairwise disjoint (position ranges `< p`, block, `≥ shift(p, n)`, other subspaces) and exhaust `project(e, d, Σ')` against I-DOM. The bijection onto the first three parts is justified (TS2 for the suffix), giving the count formula. The incomparability analysis is correct in both directions: `shift(v_max, n)` cannot have been a prior witness (maximality contradiction via TS4), and a vacated slot can remain a witness through re-population — both verified. The "equality iff `coverage(e) ∩ A_new = ∅`" claim is correct because `A_new ∩ ran(M(d)) = ∅` (freshness against both stores plus S3★), which closes the gap between containment and emptiness in the resolved-content clause.

**IP6.** The derivation `D(d, Σ') = D(d, Σ) ∪ Added` is correct: LP12 at Σ', coverage held fixed by LP13/LP3★ across the composite (the multi-step forms, correctly chosen over the single-step lemmas), RAN substituted, and the set-level lift closed by F-LINK (`dom(Σ'.L) = dom(Σ.L)`) — the quantifier gap flagged in the prior cycle is now closed. The containment-vs-emptiness distinction is real and the worked example's `ℓ ∈ Added ∩ D(d, Σ)` configuration witnesses it concretely.

**Worked example arithmetic.** All checked: the shift table, the index intervals, the LP-Fin reduction of subtree coverage to start-membership (legitimate — every store entry has `#E = 2` by ChainMembershipForOrigin's chain form, so unit-depth subtrees meet store-backed sets only at their starts), the orphanhood of `ℓ'` (g' outside both stores, subspace s_C excluding `dom(L)` membership via L0), and the P4★/P7a provenance tracing.

**Anti-bloat scan** (per the `review-mode.anti-bloat` classifier): the note is dense but the prose advances reasoning. The Effect-paragraph's named "block-disjointness fact" and "gapped/filled bridge" are DRY devices used at multiple sites, not meta-prose; the justification for decomposing into K.μ⁻/K.μ⁺ establishes a non-obvious negative fact (no atomic realises the shift) rather than defending document structure; no consumer inventories, repeated deferrals, or excluded-case paragraphs found. The slot-vs-identity theme recurs (intro, displacement section, IP3), but each occurrence carries distinct formal content; this is thematic reinforcement, not duplicated claims.

## OUT_OF_SCOPE

### Topic 1: Concurrent insertion without a serializing authority
**Why out of scope**: The model inherits SequentialTransitionAxiom; relaxing it is a new modeling territory, and the ASN correctly parks it as an Open Question rather than smuggling in a partial answer.

### Topic 2: Provenance when content is placed by transclusion rather than fresh allocation
**Why out of scope**: This is COPY's obligation (the ASN-0118 reframe), and INSERT's provenance story (records keyed to fresh allocation, range-new addresses only) is deliberately silent on it. The Open Question states it precisely.

### Topic 3: System obligations after later editing fragments the inserted run
**Why out of scope**: IP1 correctly stops at characterising the run at creation (including its non-maximality cases); fragmentation under DELETE/REARRANGE belongs to those operations' reframes.

### Topic 4: Insertion at a position shared by transclusion with another document's arrangement
**Why out of scope**: IP5 settles isolation of the *other* document; what INSERT owes at a shared position beyond that is genuinely new ground, flagged in Open Questions.

VERDICT: CONVERGED
