# Review of ASN-0131

This note is on-track: it specifies an abstract query (`Σ' = Σ`, reading only `Σ.M(d)` and `Σ.L`) with implementation-independent guarantees (overlap matching, unclipped extent, identity withholding, transclusion-blindness, present-tense stability). It leans correctly on ASN-0127's image/discovery machinery rather than rebuilding it. The defining biconditional is well-formed and RE-SEL's reduction to `findlinks_V ∩ addressable` checks out. But several claims are under-derived, one stability claim contradicts the note's own central invariant, and the mandatory boundary/example/wp depth is missing.

## REVISE

### Issue 1: Fragmentation under rearrangement contradicts the content-identity invariant
**ASN-0131, "Stability… as the document is edited" (rearrangement bullet) / RE-EDIT**: "a contiguous run of content, displaced piecewise by a rearrangement, can present an endset's footprint as *several* spans where it was one — the anchoring fragments under the arrangement (ASN-0082)".

**Problem**: RE returns content-identity-keyed endsets — `e = Σ.L(a).eᵢ`, spans over I-addresses (RE-DEF, RE-TRANS), whose coverage is *permanent* (RE-IDENT, via LP3/L12, ASN-0098/0043). The "fragmentation of a footprint into several spans" is a property of the **V-order projection/display** of content (ASN-0082), which RE does **not** report — and the V-rendered mode is explicitly deferred to open question 3. So under K.μ~ every surfaced endset is invariant; the *only* change to RE's answer is **membership** (which `(i, e)` pairs appear), because the image swings (F-IMG-SWING / LP11, ASN-0098). Listing fragmentation as a "subtler effect" of the answer's stability directly muddies RE-IDENT and risks implying the surfaced spans change shape — which RE-CLIP and RE-IDENT deny. The note even concedes "The same endset, the same covered I-addresses," yet presents the V-order shape change as an effect on the answer.

**Required**: Either drop the fragmentation passage, or state explicitly that it concerns the V-order display (the deferred rendered mode of open question 3), not RE's current content-identity answer — and state that under K.μ~ the answer changes only by membership (via the image swing), while every surfaced endset's spans remain invariant.

### Issue 2: Boundary behavior of RE is never stated
**ASN-0131, RE-DEF / "Existence and discoverability"**: the note discusses the *meaning* of a zero answer (D-ZERO) but never states *when* RE is forced empty.

**Problem**: Boundary cases are mandatory and absent:
- `W ∩ dom(Σ.M(d)) = ∅` (including a freshly registered `d` with empty arrangement) ⟹ `I = ∅` ⟹ `touch_R(e) = coverage(e) ∩ ∅ ≠ ∅` is false for all `e` ⟹ `RE = ∅`.
- `addressable(Σ) = ∅` (no links, or all nullified) ⟹ `RE = ∅`.
- An **empty endset** `e = ∅` (permitted for slots 1,2 by ASN-0043; only slot 3 must be non-empty per L3) has `coverage(∅) = ∅`, so `touch_R(∅)` is always false and such a slot is **never** surfaced — a corner of RE-OVL/RE-CMP worth stating.

**Required**: State RE's behavior on the empty image, the no-addressable-links case, and the empty-endset slot.

### Issue 3: Union-distributivity is a derivable consequence, deferred entirely to an open question
**ASN-0131, Open Questions**: "Must the surfaced anchoring distribute over unions and intersections of the queried region, so that querying a region is composable from querying its parts?"

**Problem**: The **union** half is an immediate corollary of the foundation and should be derived now, not deferred. Forward image over a union always distributes: `image(W₁∪W₂, d, Σ) = image(W₁,d,Σ) ∪ image(W₂,d,Σ)` (no injectivity needed). Then `touch_R` over the combined image is the disjunction of the parts, giving `RE(W₁∪W₂, d, Σ) = RE(W₁,d,Σ) ∪ RE(W₂,d,Σ)` — the RE-level analogue of F-UDIST/F-VDIST (ASN-0127), which is exactly what RE-SEL ties RE's selection to. Only the **intersection** half is genuinely subtle (forward images do not distribute over intersection without injectivity, which content-sharing M13/M14 breaks), and that half is fairly open.

**Required**: State and derive the union-distributivity corollary as an introduced claim; retain only the intersection question as open.

### Issue 4: The "finite, computable object" claim omits decidability of the addressability filter
**ASN-0131, "When does an endset touch the region?"**: "The image `I` is finite (S8-fin, ASN-0036), and `dom(Σ.L)` is finite (L-fin, ASN-0093), so the answer is a finite, computable object."

**Problem**: Membership in the answer requires `a ∈ addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)`. The decidability paragraph justifies only the touch test (CoverageEqualityDecidable run for overlap) and the finiteness of `I` and `dom(Σ.L)`. It does **not** establish that `nullified(Σ)` — hence addressability — is decidable, which is a necessary premise for "computable." (ASN-0086 does establish it: `nullified(Σ)` by CoverageEqualityDecidable + T2 span-membership.)

**Required**: Cite ASN-0086's computability of `nullified(Σ)` so the addressability filter is discharged as decidable.

### Issue 5: No concrete worked example
**ASN-0131, throughout**: the note is entirely abstract.

**Problem**: A concrete scenario verifying the operation's distinctive postconditions is mandatory and absent. RE-OVL (overlap, not containment), RE-CLIP (unclipped extent), RE-UNIT (identity withheld + collapse), and per-endset/per-slot surfacing are precisely the claims a worked example pins down.

**Required**: Add a worked scenario — e.g., document `d` with V-positions `[1,1]→a₁, [1,2]→a₂, [1,3]→a₃`; link `L₁` with a from-endset whose span straddles the region boundary (covering `a₂` inside and an address outside) and a to-endset pointing entirely outside `W`; a second link `L₂` sharing `L₁`'s from-endset value. Query `W = {[1,2]}` and check: the from-endset is surfaced **entire** (RE-CLIP), only slot 1 appears (per-endset), `L₁` and `L₂` collapse to one `(1, e)` pair (RE-UNIT), and no link address is returned.

### Issue 6: No weakest-precondition analysis for any non-trivial stability question
**ASN-0131, "Stability… as the document is edited"**: the entire stability treatment is qualitative (citing LP9/LP10/LP11/LP17/LP18, D-NONMONO).

**Problem**: Every foundation sibling of this operation carries a wp (D-CWP in ASN-0127, LP12a/LP12b in ASN-0098, wp Cases in ASN-0086). RE is the direct sibling of `findlinks_V`, yet no wp is derived. The natural non-trivial target: the precondition under which a K.μ⁻ contraction of `d` leaves RE's answer unchanged.

**Required**: Derive a wp for a non-trivial stability question — e.g., `wp(K.μ⁻[d, R], RE(W, d, ·) unchanged)` — paralleling D-CWP, accounting for both the image reduction `I_R` and the per-slot endset selection that distinguishes RE from `findlinks_V`.

## OUT_OF_SCOPE

### Topic 1: V-rendered surfacing of endsets into the querying document's V-positions
**Why out of scope**: Open question 3. The current note fixes the content-identity (I-keyed) deliverable; rendering into V-positions (and the guarantee for content `d` does not currently arrange) is new territory. (Note this is the mode whose phenomenon leaked into Issue 1.)

### Topic 2: Type-slot (slot-3) match semantics over a content region
**Why out of scope**: Open question 6. RE-DEF uniformly ranges over all slots, which is a clean definition; what a type-endset match against a content region *means* (type endsets are matched by address and ordinarily reference classifying addresses disjoint from content) is a distinct interpretive question.

### Topic 3: Multiplicity preservation, intersection-distributivity, and cross-server completeness
**Why out of scope**: Open questions 2, 4 (intersection half), and 5. Preserving link multiplicity in the anonymised answer, region-intersection composability under non-injective arrangements, and completeness against a non-co-resident link store are genuine future work, not errors here.

VERDICT: REVISE
