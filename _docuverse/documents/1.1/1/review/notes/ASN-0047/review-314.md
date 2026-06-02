# Review of ASN-0047

I read the full transition model, checked each elementary transition's effect/frame against the invariant package, traced all six worked examples, and audited the Class (a)/(b) verification matrix and the K.δ/K.μ~/J4 proofs. The mathematics is sound — I found no correctness defect in the proofs, the coupling analysis, or the worked examples. The remaining issues are accretion/meta-prose, which the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: The same freshness condition is stated three times in K.δ case (ii) k = 0
**ASN-0047, Elementary transitions — K.δ case (ii)**: The case-level where-clause says `e ∉ E ∧ T4-valid(e) ∧ ¬Element(e)` "apply uniformly to all three sub-cases." The freshness paragraph then says the guard is "`inc(t, 0) ∉ E` at k = 0 and `e ∉ E` at k ∈ {1, 2}." The k = 0 sub-case then lists "`t ∈ E ∧ ¬Node(t) ∧ inc(t, 0) ∉ E`."

**Problem**: For k = 0, `e = inc(t, 0)`, so the case-level conjunct `e ∉ E`, the freshness-paragraph form `inc(t, 0) ∉ E`, and the sub-case conjunct `inc(t, 0) ∉ E` are the *identical* condition stated three times. A precise reader must verify they are not three distinct obligations before proceeding. This is exactly the "two paragraphs in the same document say the same thing" accretion pattern the note flags.

**Required**: State the k = 0 freshness once. Either drop `inc(t, 0) ∉ E` from the k = 0 sub-case (it is the case-level `e ∉ E` specialised) or note explicitly that the sub-case conjunct *is* the case-level conjunct under `e = inc(t, 0)`, not an additional requirement.

### Issue 2: J3 re-derives K.μ~-RANGE rather than citing it
**ASN-0047, Coupling and isolation — J3**: "By K.μ~-RANGE (range-invariance), Contains(Σ') = Contains(Σ). The 'no coupling' claim holds at the elementary granularity the Class (a) induction uses... at the intermediate state (post-K.μ⁻, pre-K.μ⁺) the content-subspace range has contracted, but the subsequent K.μ⁺ step re-adds only V-positions whose content I-addresses already lay in `ran(M(d)|_{s_C})` — K.μ~-RANGE establishes `ran(M'(d)) = ran(M(d))` across the pair, so the K.μ⁺ step introduces no range-new content I-address."

**Problem**: The intermediate-state range argument re-walks reasoning already discharged by K.μ~-RANGE's own proof (which itself establishes `ran(M'(d)) = ran(M(d))` via the bijection equation and LRP). The paragraph cites K.μ~-RANGE and then re-derives it in the same breath. This is consequence-derivation duplicated across sections.

**Required**: Collapse J3 to the load-bearing statement — `C' = C ∧ L' = L ∧ E' = E ∧ R' = R`, with `Contains(Σ') = Contains(Σ)` by K.μ~-RANGE and J1★ vacuous since no range-new content arises — and drop the re-derivation of the intermediate-state range invariance.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior arrangement contraction
The ASN's K.μ⁻ models only suffix removal; interior withdrawal with compaction (the implementation's `DELETEVSPAN`) is not modeled. This is correctly left as an Open Question in the ASN and belongs to the named-operations layer, not a revision of the transition vocabulary.

**Why out of scope**: Named operations (DELETE/DELETEVSPAN) and their renumbering mechanics are explicitly out of scope; the abstract suffix-only K.μ⁻ is a complete elementary transition on its own terms.

VERDICT: REVISE
