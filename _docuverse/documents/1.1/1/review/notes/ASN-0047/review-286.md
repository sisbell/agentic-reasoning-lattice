# Review of ASN-0047

I checked the transition model on its own terms: the five-component state, the seven elementary transitions plus K.μ~, the coupling constraints, and the per-state/composite-boundary invariant split. The mathematical content is sound — I verified the K.δ entity chain, the fork (k=1 and k=0) range bounds, the link-allocation tumbler arithmetic, and the K.μ~ admissibility clauses against the worked examples and they hold. The findings below are anti-bloat / reviser-drift, consistent with this note's `review-mode.anti-bloat` classifier, plus two precision items. I deliberately do **not** raise ASN size/splitting (previously declined) or the matrix cross-reference convention (previously declined as Issue 7).

## REVISE

### Issue 1: Redundant double-derivation in K.μ~-RANGE
**ASN-0047, *Decomposition of K.μ~* (K.μ~-RANGE proof)**: "By K.μ~-FIX, π is a bijection ... the image set `{M'(d)(π(v)) : v} = {M(d)(v) : v}` gives `ran(M'(d)) = ran(M(d))`. Subspace preservation likewise preserves the per-subspace ranges ... and the union of the two subspace equalities recovers `ran(M'(d)) = ran(M(d))`."
**Problem**: The global identity `ran(M'(d)) = ran(M(d))` is established in the first sentence and then re-established a second time via the per-subspace union. Only the per-subspace *content* equality is load-bearing for `Contains_C(Σ') = Contains_C(Σ)`; the global identity does not need to be derived twice. This is the "two paragraphs say the same thing in different words" pattern, here compressed into one paragraph.
**Required**: Derive the content-subspace range equality once (the quantity P4★/Contains_C actually needs) and drop the second global re-derivation, or state the global identity once and note the content/link split as a one-line consequence.

### Issue 2: Defensive meta-prose justifying matrix `frame` entries
**ASN-0047, Class (a) verification matrix preamble**: "For link-store invariant rows ... `frame` under K.α, K.μ⁺, K.μ⁻ rests on the amended forms of *Amendments to existing transitions* above, which add the explicit `L' = L` conjunct ... not on the original pre-link transitions, which made no commitment about L."
**Problem**: This paragraph explains *why a notation in the table is legitimate* rather than advancing any invariant. The fact it guards (the amended transitions carry `L' = L`) is already stated at each amended transition's Frame line; the reader does not need a defensive note that the cell does not rest on the superseded pre-link form. This is meta-prose the precise reader must skip past.
**Required**: Delete the justification. If a disambiguation is truly needed, it belongs as a one-clause footnote on the amended-frame lines, not as preamble that re-litigates which version of each transition the matrix references.

### Issue 3: Same conclusion derived two ways inside one sub-step
**ASN-0047, *Link-subspace fixity and realisation*, sub-step (4)**: the paragraph first concludes `π(v) = v` from "CL-UNIQ at Σ ... forces `π(v) = v`," then adds "LRP's functional identity *also* gives post-state CL-UNIQ preservation directly, without passing through the pointwise identity."
**Problem**: The second sentence is an alternative route to a CL-UNIQ conclusion appended to a paragraph whose stated job is the pointwise identity `π(v) = v`. Either the pointwise-identity route or the direct functional-identity route suffices for the CL-UNIQ matrix cell; carrying both, with the explicit "also ... directly, without passing through" framing, is redundant-derivation accretion.
**Required**: Pick the route the CL-UNIQ cell actually cites (the direct functional-identity one is simpler) and state it once; drop the parallel derivation.

### Issue 4: S8★ link-subspace "partition" claim understates the weakening
**ASN-0047, *Amendments to existing transitions*, S8★**: "S8★ retains the finite-run *partition* — the theorem-level statement of ASN-0036's S8 — together with ASN-0036's S8 condition (a) ... and condition (b)" but for the link subspace "omits (c)."
**Problem**: The trivial length-1 decomposition is presented as "the" partition, but it is a *chosen* (non-maximal) decomposition. ASN-0036's S8 partition is specifically the *maximal*-run partition, and that is what makes "the partition" well-defined. By dropping (c) the link-subspace decomposition is no longer canonical: if two adjacent link V-positions happen to stand in lockstep, the length-1 decomposition and a length-2 maximal decomposition both satisfy (a)/(b). The prose claims to "retain the partition" of S8 while silently switching from maximal to length-1.
**Required**: State explicitly that S8★(s_L) asserts existence of *a* run-partition satisfying (a)/(b), not the maximal one, and confirm in one line that nothing downstream consumes link-run maximality (so the weakening is harmless). One sentence closes it; as written the equivalence to "the theorem-level statement of S8" overclaims.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal with renumbering
The Open Questions already flag that K.μ⁻ models only suffix removal of link V-positions, while the implementation's interior `DELETEVSPAN` compacts-and-renumbers. This is correctly future territory, not a defect in the present K.μ⁻ — noted here only to confirm it is out of scope, not a missing case.

### Topic 2: One-sided / type-only links (`e₁ ∪ e₂ = ∅`)
Whether K.λ should constrain the from/to endsets is raised as an Open Question. Belongs to a future link-semantics ASN, not this transition model.

VERDICT: REVISE
