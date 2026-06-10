# Review of ASN-0119

This note imports REARRANGE_K from ASN-0084 (foundation) and lifts it to the full `(C, L, E, M, R)` state, discharging the ASN-0047 invariant package and deriving the system-level guarantees (content permanence, extent conservation, link survival, isolation, atomicity). I checked the proofs against the foundation contracts and the worked examples against explicit ordinals.

**Correctness.** I found no errors. The induced permutation `π` does map each subspace onto itself (R-PPERM/R-SPERM destinations stay in the text subspace; non-`S` positions are fixed), so the S3★ inverse-permutation derivation, the key-set-unchanged inheritance of D-CTG★/D-SEQ★/D-MIN★/S8a/S8-depth/S8-fin/S3★-aux, the S8★ discharge via R-BLK+R-CANON, the link-subspace CL-OWN/CL-UNIQ via the frozen `s_L` frame, the footprint transport RA7a, and the worked pivot/swap (verified numerically: destinations tile `{1..5}`/`{1..6}`, ranges invariant, `diff[2] = w_β − w_α`) all hold. The P4a trace argument is sound: appending the REARRANGE step never alters prefix states, so the pre-state witness persists. The vacuity of J0/J1★/J1'★ and the preservation of P4★/P7a/P3 are correct.

The findings below are the prose-accretion issues the `anti-bloat` classifier flags — localized redundancy, no correctness defect.

## REVISE

### Issue 1: RA3's derivation re-proves a fact RA2 already gives directly
**ASN-0119, V-extent conservation**: "Conservation is immediate from RA2. The active V-positions of the text subspace s_C form a contiguous run by D-CTG★, and π permutes that run onto itself, so the run's cardinality and its endpoints are invariant: `|dom(M'(d))| = |dom(M(d))|`, min and max V-position fixed."
**Problem**: `dom(M'(d)) = dom(M(d))` (RA2) makes `V_{s_C}(d)` *the same set* — cardinality and endpoints are then trivially equal. The preservation paragraph already established this: "the active text-position set `V_{s_C}(d)` … is *literally unchanged as a set*." The D-CTG★-plus-`π`-permutes-the-run framing is a second, longer route to the same conclusion. The sentence even opens by conceding "Conservation is immediate from RA2" and then derives it again anyway.
**Required**: Drop the contiguity/permutation re-derivation; read RA3 off RA2 (and the already-stated "literally unchanged as a set") in one line.

### Issue 2: The P4a paragraph restates conclusions it has just argued
**ASN-0119, ASN-0047-obligations paragraph**: "…so it persists unchanged into the extended trace to Σ', witnessing (a, d) there as well — **the pre-state's trace witness persists, and the appended step is never consulted**." And later: "**P4a at Σ' thus holds on every valid trace — the REARRANGE-ending ones by the persistence argument above, all others by their final composite's ASN-0047 argument under the combined induction.**"
**Problem**: The clause after the em-dash restates the clause before it. The final sentence re-summarizes the two cases (REARRANGE-ending → persistence; others → ASN-0047 argument) that the preceding sentences already argued in full. A reader who followed the case split gains nothing from the echo. This is the kind of accreted summary the anti-bloat mode targets; the load-bearing content (the persistence argument, the combined-induction IH availability) is fine and should stay.
**Required**: Delete the post-em-dash restatement and the closing summary sentence; the two cases stand on their own.

### Issue 3: "suppress E and R … throughout" is contradicted by the discharge that follows
**ASN-0119, The two streams**: "the entity set E and the provenance relation R are inert under it, so we suppress E and R and write `Σ = (C, M, L)` for the active components **throughout**."
**Problem**: `E` and `R` are not suppressed throughout — the ASN-0047-obligations paragraph reasons about `R` at length (P4★ `Contains_C ⊆ R`, P4a, P7a, P7, J1'★) and about `E` (P6, P8, NodeLineage, ActivatedEmission). The reader is told to drop these from view and is then made to track them through the hardest paragraph in the note. "Inert" (i.e., `E' = E`, `R' = R`) is correct; "suppress … throughout" overstates.
**Required**: Reword to "suppress `E` and `R` from the state-tuple notation" (or similar), so the later by-name discharge of their invariants does not read as a contradiction.

## OUT_OF_SCOPE

Nothing to flag. The note's scoping is clean: depth-2/single-document/text-subspace confinement is stated and matches REARRANGE_K's contract, and the genuine future-work items — cross-document boundary-hood of transcluded cuts, order-independence of concurrent rearrangements, the content-index invariant under footprint fragmentation, prior-arrangement recoverability, and the closed-form-displacement boundary guard — are correctly held in Open Questions rather than smuggled into claims. No out-of-scope operation (INSERT/DELETE/COPY/MAKELINK/FINDLINKS/RETRIEVE/etc.) is defined; the `RETRIEVE`/transclusion mentions are observational context for atomicity (RA8b) and isolation (RA9), not claims.

VERDICT: REVISE
