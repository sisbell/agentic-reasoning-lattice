# Review of ASN-0118

The mathematics is sound. I checked the composite decomposition (the K.μ⁻ + K.μ⁺ + K.ρ split, retention counts `n'_{s_C} = j`, `n'_{s_L} = n_{s_L}`, the intermediate-state invariants), the tiling argument (left `[min,p)`, placement `[p,p+W)`, shifted `[p+W,max+W]` abut without gap by TS1/TS5), the provenance three-branch case analysis (range-new fresh, range-new-already-recorded via P2, not-range-new via P4★+P2), the J0 vacuous discharge, the CP0 bridge grounding run-interior addresses through S8 lockstep, and the worked example arithmetic. All hold. Edge cases (empty destination, append, `j=0`, self-transclusion, multi-source non-contiguity) are covered, and the P4★-at-composite-boundary scoping is correctly justified.

The findings below are the accretion patterns this note's anti-bloat classifier asks for, plus one open-question inconsistency.

## REVISE

### Issue 1: Use-site inventory and non-use note in the resolution section

**ASN-0118, "What a spec-set names" / content spec-sets paragraph**: "Resolution integrity (CP0(a)) rests on S3★ over exactly the bound positions COPY acts on, and the run-decomposition (CP0(c)) on the single-subspace premise so obtained. The one ASN-0058 property that genuinely does *not* survive partial binding — its width-preservation C2 — COPY never uses; we record its loss as an open question."

**Problem**: The useful core of this paragraph is one sentence — "content-residence confines `act(ρ,Σ) ⊆ V_{s_C}(d_s)` to a single subspace, and S8-depth gives common depth; these two facts are the only premises the arithmetic needs." What follows is meta-prose: a use-site inventory mapping the premise forward to claims not yet stated ("CP0(a) rests on…, CP0(c) on…") and a non-use note about C2 deferring to an open question. This is the pattern where a definition's introduction enumerates downstream consumers rather than advancing the definition. The "discarded full-binding hypothesis" framing also recurs three times across this region — at "what resolution recovers" ("COPY thus does not require ASN-0058's optional full-binding well-formedness condition"), here, and at CP0(c) ("licensed without the full-binding hypothesis… not by ASN-0058's C0a stated under well-formedness") — and the necessity argument for content-residence is then restated a fourth time at the operation's precondition.

**Required**: Keep the two-premise identification. Drop the CP0(a)/CP0(c) inventory and the C2-non-use sentence (the open question already records the C2 loss). State "act handles partial binding by restriction; full-binding is not required" once, not across three subsections.

### Issue 2: Duplicated domain-closure rationale (CP3c and CP6)

**ASN-0118, CP3c discussion**: "so that `d`'s per-state invariants are dischargeable from the postconditions alone, not only through the exhibited composite (CP6's domain-equality conjunct does the same for the non-text subspaces)."

**ASN-0118, CP6 middle-clause discussion**: "making `d`'s non-text invariants (S2, S3★, CL-OWN, CL-UNIQ) dischargeable from the postconditions alone rather than only through the exhibited composite".

**Problem**: The same methodological justification — a domain-closure conjunct makes invariants dischargeable from the postconditions rather than from the composite decomposition — is stated twice, nearly verbatim, with CP3c forward-cross-linking CP6 and CP6 back-linking CP3c ("the non-text instance of CP3c's closure principle"). Once the back-reference is in place, the trailing restatement at CP6 is redundant. This is the "two paragraphs say the same thing in different words" pattern.

**Required**: State the closure principle once (at CP3c, where the S2 double-binding gap argument is the genuine content). At CP6, the phrase "the non-text instance of CP3c's closure principle" suffices — drop the re-justification that follows it.

### Issue 3: Two forward-deferrals to the tiling argument

**ASN-0118, CP3 displacement note**: "rest instead on the tiling argument delivered under prior-arrangement preservation below"

**ASN-0118, CP3c**: "their disjointness is the tiling argument given later under prior-arrangement preservation"

**Problem**: Two paragraphs in different sections defer to the same downstream delivery (the tiling in "The destination's prior arrangement is preserved"). Minor, but it is the listed "multiple paragraphs defer to the same downstream location" pattern, and it compounds the reader's need to hold a pending obligation.

**Required**: One pointer to the tiling is enough. Since CP3c already names the three abutting ranges, let CP3c carry the single forward pointer and drop the second from the CP3 displacement gloss (or vice versa).

### Issue 4: Open Question 2 is already answered by CP0

**ASN-0118, Open Questions**: "What invariant fixes the placement order when a spec-set names overlapping or repeated source spans that resolve a single I-address to multiple positions in the resolved sequence?"

**Problem**: CP0 already fixes this. `resolve(R, Σ)` is the spec-set-ordered concatenation of per-spec resolutions, each internally ascending by V-start (C1b), so the resolved sequence `⟨c₀,…,c_{W−1}⟩` is totally ordered; CP2 then binds `p+i ↦ cᵢ` in that order. A single I-address appearing at indices `i` and `j` is placed at `p+i` and `p+j` in exactly the order its indices dictate. The "invariant that fixes the placement order" is CP0 itself — the question poses as open something the ASN's own construction resolves.

**Required**: Either remove the question, or, if a deeper subtlety is intended (e.g., whether duplicate placements should be deduplicated, or a normalization guarantee on the resulting arrangement), name that subtlety — placement *order* is not it.

## OUT_OF_SCOPE

The remaining open questions (C2 width-relationship under partial binding, level-uniformity across differing source depths, post-removal link undiscoverability, the correspondence relation, link-subspace transclusion) are correctly deferred — each is a property additional to a fully-specified operation, not a gap in COPY's pre/post/frame definition. No out-of-scope operation (INSERT, DELETE, REARRANGE, MAKELINK, etc.) is defined here; the REPLICATE contrast is a hypothetical foil, not a defined transition, which is appropriate.

VERDICT: REVISE
