# Review of ASN-0134

This is an unusually careful note. The step/operation seam, the per-home conflict analysis (H0–H3), the invariant partition (W0–W6), and the quiescence treatment (V0–V2) are all rigorous, and the boundary cases a concurrency model can fail on — first-emission collision (H2 boundary), empty/singleton batch (A5, A1), self-emit nullify (W5), single-home `stale` (A1) — are explicitly covered. The central new result (clause 8 / §4 instance (i)) correctly surfaces that ASN-0128 I4's "serializing authority" is a non-per-home assumption and that I1a's proof silently identified an operation's dedup-read state with its deposit pre-state. I checked the §7 and §8 traces numerically and they hold.

Two findings, both localized.

## REVISE

### Issue 1: §7's nesting vignette contradicts the H1 proof on whether the anchor argument distinguishes nesting-home deposits

**ASN-0134, §7 (Cross-home commutation (H1))**: "had we chosen the nesting pair `d' = [1.0.1.0.1.1]` the document digits would not diverge (`d ≼ d'`), and **only the origin argument would settle distinctness** — which is exactly why H1 is stated by origin and not by anchor position."

**Problem**: This directly contradicts the H1 proof in §4, which says the opposite — that the anchor/separator argument *does* settle distinctness for nesting pairs:

> "(The separator-vs-nonzero-continuation argument CrossDocumentDisjointness itself uses would also serve: `b_S(d)` carries the field-separator `0` at index `#d`, whereas `d'`'s continuation there is necessarily non-zero ... so the anchors diverge at index `#d`; origin is simply the cleaner route.)"

H1 is correct and §7 is wrong. For the cited nesting pair `d=[1.0.1.0.1]`, `d'=[1.0.1.0.1.1]` (`#d = 5`): `b_C(d) = [1,0,1,0,1,0,1]` and `b_C(d') = [1,0,1,0,1,1,0,1]` diverge at index 5 (`0` vs `1`). So the anchors are prefix-incomparable, and CrossDocumentDisjointness — stated for *any* two distinct documents, nesting included — applies directly. The anchor-position argument settles distinctness for the nesting pair just as the origin argument does. §7 conflates "the anchors differ *at the document digit*" (which fails for nesting, position 4 agreeing) with "the anchors differ *somewhere*" (which holds, at the separator).

This also mis-motivates the design choice. The genuine reason H1 is stated by origin is *not* nesting (where both arguments work) — it is the **cross-subspace cross-document** case (`d ≠ d' ∧ S ≠ S'`, e.g. `A_C(d)` vs `A_L(d')`), which CrossDocumentDisjointness's single-`·` statement (`p_i := b_·(d_i)`) does not name, and which the note correctly flags elsewhere. §7 attributes origin's necessity to the wrong case.

**Required**: Replace "only the origin argument would settle distinctness" with a statement consistent with H1 — e.g. the *document-digit-divergence* argument fails for nesting, but the anchor-separator argument still works (anchors diverge at index `#d`); origin is preferred because it is the uniformly general route, the only one covering the cross-subspace cross-document pair that CrossDocumentDisjointness leaves unnamed.

### Issue 2: H3(b)'s commutation is mislabeled "disjoint-write"

**ASN-0134, §4 (H3 proof)**: "(a) and (b) are the disjoint-write-and-surviving-precondition argument just given — the registration analog of H1's disjoint-state commutation, with `dom(M)` in the role a sub-allocator chain plays there."

**Problem**: For case (a) (a `K.σ` against an allocation into `d ≠ d_new`) the "disjoint-write" framing is accurate — `K.σ` writes `dom(M)`, the allocation writes a store. But case (b) is *two* `K.σ` steps, and both read `dom(M)` (the precondition `d_new ∉ dom(M)`) *and* write `dom(M)` (insertion). These are not disjoint writes — they are read-and-write on the *same* shared component. They commute not by disjointness but because membership-test-and-insert of *distinct* elements does not interfere, which is exactly the freshness/`d_new ≠ d'_new` condition the proof's "surviving-precondition" clause invokes. The H1 analogy ("`dom(M)` in the role a chain plays") is also imperfect: H1 has two genuinely separate chains, whereas (b) has one `dom(M)`. The conclusion (commutation) is correct; the stated mechanism is not, and an implementer told "disjoint writes commute" might wrongly generalize to "any two registrations are independent" — they share `dom(M)` and commute only under element-distinctness.

**Required**: State (b)'s commutation as shared read-write on `dom(M)` commuting by distinct-element non-interference (the freshness already cited), rather than folding it into (a)'s disjoint-write argument.

## OUT_OF_SCOPE

### Topic: batch read-atomicity (the A5 / §2 interior-prefix gap)
**Why out of scope**: A5 deliberately establishes that a multi-step batch is *not* atomic (an interior read sees a strict prefix even for a W4-contiguous run), and §2 shows canonicity cannot signal settledness. The minimal contract that would close this for a *reader* is correctly deferred (Open Question 5), not asserted. This is appropriate scoping, not a defect — flagging it only to record that I confirmed A5's non-atomicity is a deliberate boundary, not an unproven claim.

META: (none — this is a consistency/isolation contract stated as obligations any implementation must meet, squarely a system-guarantee specification.)

VERDICT: REVISE
