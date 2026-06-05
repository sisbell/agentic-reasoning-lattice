# Review of ASN-0100

The technical content is sound: I checked the three-region partition (S2 disjointness via last-component ranges + TS2), the invariant discharges against ASN-0047's ExtendedReachableStateInvariants list (all per-state and composite-boundary conjuncts are addressed), the edge cases (j=0, append j=N, empty document, empty-content/non-empty-link), the INS.chain-shift derivation, the D-CTG★ closed-interval reduction, the projection-shift correspondence, and both wp computations. I found no correctness gap.

The remaining issues are the meta-prose accretion this note's `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: Forward-reference accretion in the "Composite atomicity" paragraph
**ASN-0100, §The Operation: Formal Contract**: "The composite-level atomicity established in §Atomicity has as its consequence here the determinacy of Σ'… An implementation that realizes the sequential transition model (for instance, multiple threads serialised onto the abstract total order) inherits this determinacy; the concurrency-control mechanism it uses is below this ASN's abstraction level."
**Problem**: This paragraph defers to §Atomicity ("established in §Atomicity") and then re-derives the determinacy conclusion that §Atomicity's "The post-state Σ' is *uniquely determined*…" subsection establishes in full, component by component. A reader following the formal contract's effects must skip ahead and then re-encounter the same argument. This is the forward-reference deferral pattern.
**Required**: Drop the determinacy re-derivation here; state the effects and let §Atomicity carry the uniqueness/atomicity argument once.

### Issue 2: Duplicated implementation-freedom / below-abstraction prose
**ASN-0100, §Atomicity (closing)**: "Implementations realise the composite via transactional sequencing, locking, copy-on-write, or log-and-commit — but the choice of decomposition is below the level of abstraction at which INSERT is specified. External observers see the composite boundary; the intermediate states are not externally observable."
**Problem**: This repeats the point already made in the "Composite atomicity" paragraph (Issue 1): implementation/concurrency mechanism is below the abstraction level, decomposition choice is not observable. Two paragraphs in different sections make the same non-object-level claim.
**Required**: Keep one statement of implementation freedom (the §Atomicity location is the natural home); remove the other.

### Issue 3: K.μ⁻ firing condition re-explained across four sections
**ASN-0100**: The rule "K.μ⁻ fires iff the content-subspace Right region is non-empty" is restated in the Substrate Decomposition step 2 ("fired iff the pre-state content-subspace Right region … is non-empty"), in §Coverage ("When K.μ⁻ does not fire … In every K.μ⁻-omitted case P_0^R = ∅"), in §Position Constraints ("K.μ⁻ is omitted from the composite"), and again in §Atomicity's uniqueness subsection.
**Problem**: The same conditional and its three triggering cases (empty content subspace, append) are re-derived in each location rather than established once and cited. This is the "two paragraphs say the same thing in different words" pattern, compounded across sections.
**Required**: State the K.μ⁻ firing condition and its case split once (in the Substrate Decomposition), and reference it from §Coverage / §Position Constraints / §Atomicity rather than re-deriving P_0^R = ∅ each time.

## OUT_OF_SCOPE

### Topic 1: Recovery of canonical order after partial failure
**Why out of scope**: The first Open Question (implementation guarantees for recovering canonical order after partial failure) is genuinely future territory — failure/recovery semantics are below this ASN's abstraction level and belong to an implementation-substrate note, not here.

VERDICT: REVISE
