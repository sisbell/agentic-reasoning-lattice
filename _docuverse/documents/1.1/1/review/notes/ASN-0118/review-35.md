# Review of ASN-0118

## REVISE

### Issue 1: J1★'s discharge covers only the placed addresses of the destination document
**ASN-0118, "COPY as a valid composite"**: "The discharge turns on a single *membership* obligation, which we must read off J1★ exactly. For each `cᵢ` that is *range-new* — placed by CP2 *and* not already in the content-subspace range of `M(d)` in the pre-state `Σ` — ASN-0047's coupling J1★ (ExtensionRecordsProvenance) demands the membership `(cᵢ, d) ∈ Σ'.R`."

**Problem**: J1★ is universally quantified over *every* document `d' ∈ E'_doc` and *every* address `a` new to that document's content-subspace range. The section discharges only the instances `(d, cᵢ)` for placed addresses, leaving two parts of the quantifier implicit:

(a) *Destination, non-placed addresses.* J1★ fires for any `a` new to `d`'s content-subspace range, not just the placed `cᵢ`. The proof therefore needs the containment "range-new ⊆ {c₀, …, c_{W−1}}", i.e. that the post-state content-subspace range of `M(d)` equals the pre-state content-subspace range ∪ the placed set. This is derivable from CP3c plus CP3a/CP3b (left and trailing images preserved, placement images the only additions), but the only place a range equation is proved is the link-discoverability wp paragraph two sections later — and there it is proved for the *full* range `ran(Σ'.M(d))`, not the content-subspace restriction that J1★'s witness clause (`subspace(v) = s_C`) actually tests. At the point where ValidComposite clause 2 is being discharged, the sentence "only the net change in `d`'s content-subspace range matters" asserts the needed conclusion without proving it.

(b) *Other documents.* For every `d' ≠ d`, J1★ is vacuous because each step in the composite frames `M(d')` unchanged, so no address is range-new for `d'` — but this is never stated. The non-uniformity is conspicuous: the section explicitly walks J0's vacuous discharge (empty quantifier range, no K.α step), yet omits the strictly analogous vacuity argument for J1★'s other-document instances. The same one-line observation completes J1'★'s coverage of the full quantifier (no pair `(a, d')` with `d' ≠ d` enters `R`, since the only `R`-touching steps record pairs at `d`).

As written, the admissibility argument establishes a strictly weaker statement than ASN-0047's ValidComposite clause 2 requires.

**Required**: In the composite-validity section, (i) state and discharge the content-subspace range equation for `d` — `{a : (E v ∈ dom(Σ'.M(d)) : subspace(v) = s_C ∧ Σ'.M(d)(v) = a)} = {a : (E v ∈ dom(Σ.M(d)) : subspace(v) = s_C ∧ Σ.M(d)(v) = a)} ∪ {c₀, …, c_{W−1}}` — from CP3c/CP3a/CP3b (or forward-cite the wp section's derivation, restricted to `s_C`), so that range-new ⊆ placed is explicit before the three-branch case split; (ii) add the one-line vacuity discharge of J1★ for all `d' ≠ d` via the steps' other-document frames, with the corresponding remark for J1'★.

## OUT_OF_SCOPE

### Topic 1: Block-seam identity of the placed region under canonical re-decomposition
When two V-specs resolve to same-origin, I-adjacent runs that the placement lays down consecutively, the destination's canonical (maximally merged) decomposition fuses them into one block, erasing the spec-set seam even though the origin multiset (CP11) is untouched — CP11 is per-address and remains sound. Whether any guarantee should preserve spec-set boundaries as block boundaries belongs with the correspondence-relation question the ASN already lists as open.
**Why out of scope**: The ASN claims origin-multiset preservation, not seam preservation; block-level seam identity is new territory for a correspondence ASN, not an error here.

### Topic 2: Partial-binding width shortfall
The relationship between a partially-bound span's nominal extent and its smaller resolved width `W` is correctly deferred — the ASN states the shortfall is silent and poses the guarantee question in Open Questions.
**Why out of scope**: The design choice is recorded and consistent (resolution by restriction, `W ≥ 1` gate); what COPY should *promise* about the shortfall is a future-ASN question.

VERDICT: REVISE

The ASN is otherwise in strong shape, and I verified its load-bearing arguments in detail rather than taking them on faith: the relaxation of ASN-0058's condition (iii) is properly routed around C0a (single-subspace via the content-residence precondition, single-depth via S8-depth on the active positions, both independent of `#s`/`#ℓ`); both relaxation examples compute correctly under TumblerAdd (`[1,1,5] ⊕ [0,9,0] = [1,10,0]` capturing depth-2 positions `2 ≤ k ≤ 10`, including the prefix-ordered `[1,10]`); the displacing-case K.μ⁻ + K.μ⁺ decomposition matches ASN-0047's per-subspace retention discipline exactly (canonical prefix `n'_{s_C} = j < N`, link subspace retained in full, `j = 0` boundary handled); CP3c's three-range union, the tiling arithmetic, and the worked two-source example (including the `[1,2]+3 = [1,5]` shift, the origin multiset `⦃d_A, d_A, d_B⦄`, and the S4-based range-new classification) all check out numerically; and the CP8 three-branch provenance analysis correctly uses P4★ only at the composite boundary the standing precondition supplies. The single finding is a completeness gap in the central admissibility proof, fixable with two sentences and a forward citation.
