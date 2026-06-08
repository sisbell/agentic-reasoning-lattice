# Review of ASN-0112

I checked the displacement arithmetic (V1–V3, V-ReachTight, V-LevelUniform), the two covering cases of V2, the worked examples (both the standard cross-subspace report and the depth-divergent variant), the wp derivations, and the V18 transition inventory. The technical content is sound: the case split on `#origin_d` vs `#reach_d` is exhaustive and correctly discharged via D0/D1, the cross-subspace `k=1` divergence and resulting overshoot `r⋆ > reach_d` compute correctly, V5/V6 exact-cover-vs-bounding-box is properly forced by S3★-aux + D-CTG★, and the empty-result totality (V11) is honestly stated. No correctness, edge-case, or cross-ASN-reference defects found (all of ASN-0034/0036/0043/0047/0053 are foundation).

The findings below are anti-bloat only, per the note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: V11 closing sentence recaps the paragraph; "freshly created or fully emptied" duplicated
**ASN-0112, "Every document answers, including the empty one"**: the paragraph establishes "When `O(d) = ∅`, the result is the empty span-set `⟨⟩`" near the top, then closes with "Emptiness is a *valid state of the address space*, not an undefined result; an allocated document with an empty arrangement … — whether freshly created or fully emptied — answers identically, with the empty span-set."
**Problem**: The closing clause restates the paragraph's already-established thesis (result is `⟨⟩`; not undefined), and "freshly created or fully emptied" appears both in the intro sentence ("a freshly created or fully emptied document has `O(d) = ∅`") and again in the closing sentence. The recap does not advance the argument — the substantive empty-case content (undefined `min`, sentinel-not-address) sits between the two restatements.
**Required**: Drop the recapping clause; keep the one philosophical point ("emptiness is a valid state, not an undefined result") attached to a single statement of the empty result, and cite "freshly created or fully emptied" once.

### Issue 2: equidepth-from-S8-depth re-derived across adjacent V-ReachTight and V-LevelUniform paragraphs
**ASN-0112, "The bounding span and its two endpoints"**: V-ReachTight states "it holds automatically in the single-subspace regime (S8-depth makes the endpoints equidepth)"; the immediately following V-LevelUniform paragraph repeats "In the single-subspace regime the endpoints are equidepth (S8-depth), so `#origin_d = #reach_d`."
**Problem**: The same sub-derivation (single-subspace ⟹ `#origin_d = #reach_d`, by S8-depth) is performed twice in consecutive paragraphs that, as the note itself says, turn on "the same depth axis." The repeated premise is noise the reader must re-parse.
**Required**: Establish the single-subspace equidepth fact once (it is the shared premise of both claims) and have the second paragraph cite rather than re-derive it.

## OUT_OF_SCOPE

None. The Open Questions correctly defer per-run/per-subspace composition (Q1, Q4), version reporting (Q3), and out-of-range addressing (Q5) to future ASNs without asserting claims about them; they introduce no in-body coverage of the excluded operations.

VERDICT: REVISE
