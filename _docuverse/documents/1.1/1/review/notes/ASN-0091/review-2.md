# Review of ASN-0091

## REVISE

### Issue 1: Abstract class frame is too weak for RE-R

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "RA-frame: `Σ'.C = Σ.C ∧ Σ'.L = Σ.L ∧ (A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`"

**Problem**: RA-frame as defined does not include `Σ'.R = Σ.R`. The ASN then states "the abstract claims below are derivable from RA-dom, RA-π, and RA-frame alone." But RE-R (`Σ'.R = Σ.R`) is listed alongside the abstract claims and cannot be derived from RA-frame — it requires ASN-0047's J3 via K.μ~'s extended frame. The ASN's own derivation of RE-R explicitly cites J3 rather than RA-frame, contradicting the abstract-derivability claim.

**Required**: Either strengthen RA-frame to include `Σ'.R = Σ.R` (and `Σ'.E = Σ.E` for ASN-0047 state-model completeness), making RE-R abstract-derivable, or explicitly demote RE-R to a REARRANGE_K-specific claim and update the introductory framing to acknowledge the partition.

### Issue 2: RE-sub is not derivable from the abstract class

**ASN-0091, "Subspace Frame"**: "RE-sub: `(A v : v ∈ dom(Σ.M(d)) ∧ subspace(v) ≠ S :: Σ'.M(d)(v) = Σ.M(d)(v))`"

**Problem**: The abstract class's π is any bijection on `dom(Σ.M(d))` — it may move V-positions across subspaces. RE-sub requires π to fix non-S V-positions, which is a REARRANGE_K-specific property supplied by ASN-0084's R-FRAME-P/S. The ASN says "the abstract claims below are derivable from RA-dom, RA-π, and RA-frame alone, independent of how π was generated," then lists RE-sub among the derived claims. The derivation in the Subspace Frame section correctly cites R-FRAME-P/S, but the framing as "abstract" is inconsistent.

**Required**: Either add a subspace-fixing constraint to RA-π for the abstract class (e.g., a designated "cut subspace" parameter), or explicitly mark RE-sub as REARRANGE_K-specific in the Claims Introduced table and update the introduction.

### Issue 3: Claims Introduced table conflates abstract and REARRANGE_K-specific claims

**ASN-0091, "Claims Introduced"**: All RE-* claims are listed uniformly as "introduced" without distinguishing which are derivable from the abstract class (RE-C, RE-dom, RE-ran, RE-μ, RE-L, RE-cov, RE-disc, RE-proj, RE-frag, RE-other, RE-trans, RE-origin) from those requiring REARRANGE_K specifics (RE-sub, RE-R).

**Problem**: A reader cannot tell from the table which claims survive at the level of an arbitrary Vstream-only transition versus which require the cut-sequence structure. This matters: an alternative realization of the abstract class (e.g., a non-cut-sequence rearrangement) would satisfy the former but not necessarily the latter without independent justification.

**Required**: Add a column or annotation to the Claims Introduced table indicating each claim's provenance (abstract class vs. REARRANGE_K vs. K.μ~ frame).

### Issue 4: `→_R` notation undefined

**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences"**: "For a finite sequence of REARRANGE-only transitions `Σ₀ →_R Σ₁ →_R ⋯ →_R Σ_n`"

**Problem**: The arrow `→_R` is introduced without prior definition. Earlier sections refer to "REARRANGE" or "REARRANGE_K" or "Vstream-only on d" but never define `→_R`.

**Required**: Add a definition such as "`Σ →_R Σ'` denotes a transition satisfying RA-dom, RA-π, and RA-frame for some document d" (or, if REARRANGE_K-only is intended, "a K.μ~ transition").

### Issue 5: Multi-step run-decomposition claim under-stated

**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences"**: "RE-frag★: run-decomposition cardinality can drift in either direction across the sequence (each step may increase or decrease it independently); no monotonicity claim is available even in the limit."

**Problem**: The witnesses for fragmentation and coalescence are at the single-step level. The claim that "no monotonicity is available even in the limit" is not formally established — a multi-step witness (e.g., a sequence whose net cardinality change is non-monotonic across steps but eventually bounded) would discharge it. The single-step witnesses are necessary but not sufficient for the "in the limit" assertion.

**Required**: Either supply a multi-step witness or weaken the claim to "no per-step monotonicity is available."

## OUT_OF_SCOPE

### Topic 1: Cross-document transclusion continuity under fragmenting cuts

The first Open Question — "What guarantees must rearrangement preserve about cross-document transclusion when a cut splits a span transcluded from the same source document into two non-contiguous pieces?" — is correctly identified as future work. RE-trans handles the per-address preservation; the *continuity* question (does the source span still resolve as a single transclusion, or as two?) is a separate property that belongs to a future ASN on transclusion semantics.

**Why out of scope**: The ASN's commitment is to derive what REARRANGE preserves about content, links, projections, and provenance. Continuity of transcluded spans across fragmenting cuts requires a separate definition of "transcluded span" as a structural entity beyond the per-address relationship — this is new territory.

### Topic 2: Link-subspace rearrangement

The second Open Question asks for semantics on the link subspace. ASN-0084's CS3 fixes the cut subspace at s_C; link-subspace rearrangement would require a separate operation definition.

**Why out of scope**: The current REARRANGE_K is content-subspace-only by construction; an analogous link-subspace operation is a future operation, not a gap in this ASN.

### Topic 3: Observational equivalence under rearrangement

The third Open Question asks when two distinct rearrangements are equivalent at the discoverability level. This is a quotient question over the rearrangement permutation group.

**Why out of scope**: Defining the equivalence requires machinery (an observation predicate, a quotient structure) that this ASN doesn't introduce.

### Topic 4: Cardinality bounds on fragmentation

The fourth Open Question asks for an upper bound on run-decomposition cardinality increase per rearrangement.

**Why out of scope**: This is a quantitative result requiring counting arguments over the cut sequence and run structure — different territory from the present qualitative invariants.

### Topic 5: Realizability of arbitrary bijections via cut sequences

The fifth Open Question asks whether every well-formedness-preserving bijection is realizable by cut-sequence rearrangements.

**Why out of scope**: This is a completeness question about the cut-sequence operation, which lives at the ASN-0084 level (the cut-sequence specification), not at this ASN's level (REARRANGE properties).

VERDICT: REVISE
