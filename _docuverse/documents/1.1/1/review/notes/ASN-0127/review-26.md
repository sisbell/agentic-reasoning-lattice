# Review of ASN-0127

## REVISE

### Issue 1: Circular appeal to K.μ~-FIX while establishing witness admissibility
**ASN-0127, F-IMG-SWING (Witness admissibility paragraph) and Worked illustration (swing bullet)**: "K.μ~-FIX keeps the V-position domain fixed, so the shape invariants (i) — S8a, S8-depth, D-CTG★, D-MIN★, all properties of that unchanged domain — persist in the post-state"; and "a valid K.μ~ on d: it fixes the V-position set {v_1, v_2, v_3} (K.μ~-FIX, ASN-0047)".
**Problem**: K.μ~-FIX is a *consequence* of admissibility, not a premise available while admissibility is being established. Its derivation (ASN-0047) invokes D-SEQ★ at the pre- **and post-**states — post-state D-SEQ★ is exactly what admissibility clause (i)'s package supplies — plus length preservation (iii). Using it to discharge clause (i) for a candidate reorder is circular. The fact is true for every constructed witness, but for a different reason: each witness's `π` is defined as a permutation of the pinned position set, so `dom(Σ'.M(d)) = π(dom(Σ.M(d))) = dom(Σ.M(d))` by construction, and the domain-only shape invariants persist from there. (F-IMG-SWING's main derivation uses K.μ~-FIX legitimately — there an admissible K.μ~ is given by hypothesis. The defect is only at the two sites where admissibility is the thing being proved.)
**Required**: At both sites, replace the K.μ~-FIX citation with by-construction domain fixity (`π` permutes the pinned domain), reserving K.μ~-FIX for contexts where an admissible K.μ~ is already in hand.

### Issue 2: Illustrated transitions skip their composite-coupling obligations
**ASN-0127, Worked illustration ("Stability under K.α" and "Rise under K.μ⁺" bullets)**: "allocating fresh content `a_4` adds nothing to `image(W, d, Σ)` (V-positions in `W` are unchanged); F-INERT carries the result"; and "apply K.μ⁺ adding `v_2 ↦ a_2`, a valid content-subspace extension restoring the contiguous segment `{v_1, v_2}` (D-SEQ★) whose image `a_2 ∈ dom(Σ₁.C)` discharges referential integrity (S3★)".
**Problem**: Both bullets verify elementary preconditions but are silent on ValidComposite★'s clause-2 couplings (ASN-0047). A bare K.α is not a valid composite: J0 requires every freshly allocated I-address to appear in some arrangement in the composite's post-state, and `a_4` is arranged nowhere — so "allocate `a_4`" is not by itself an available system evolution; it is legitimate only as an intra-composite atomic step or with an accompanying placement (any placement outside `W` leaves the bullet's conclusion intact). The rise step, as a single-step composite, carries a non-vacuous J1★ obligation: `a_2` is new to the content-subspace range of `M(d)` at `Σ₁`, so `(a_2, d) ∈ R'` is required. It is in fact satisfied — `(a_2, d)` entered `R` at the initial composite boundary by P4★ (where `v_2 ↦ a_2` was arranged) and persists by P2 across the contraction (frame `R' = R`) — but the illustration never says so, leaving the legitimacy of its own scenario for the reader to reconstruct.
**Required**: One sentence per bullet: frame the K.α event as an atomic step inside a J0-satisfying composite (or name `a_4`'s placement), and discharge the rise's J1★ from the standing record `(a_2, d) ∈ R` via P4★ + P2.

### Issue 3: "Necessary but not sufficient" — the insufficiency half has no witness
**ASN-0127, D-NONMONO (K.μ~ clause)**: "(Image-motion is in any case *necessary but not sufficient* for the discovery set to move: by F-MATCH's per-slot existential, a displaced in-region I-address relocates a link only when it was that link's *sole* in-region witness and the swapped-in address does not re-witness the same links.)"
**Problem**: The necessity half is proved (F-PRES/F-INERT route all discovery motion through the image). The insufficiency half is asserted with a mechanism sketch only — no state exhibits an image that moves while the discovery set stays fixed. The note's own discipline witnesses every other realizability claim (injective, gain, loss, four-position, lateral swing, cardinality variant); this is the one left as a claim rather than a proof.
**Required**: A two-line witness from existing machinery — e.g. a single stored link whose slot-1 endset is the two-span set `{(a_1, δ(1, #a_1)), (a_2, δ(1, #a_2))}` over the injective arrangement `v_1 ↦ a_1, v_2 ↦ a_2` with `W = {v_1}`: the transposition `(v_1 v_2)` moves the image `{a_1} ↦ {a_2}` while the link matches at both states, so `findlinks_disc` is fixed. Alternatively, demote the parenthetical to the proved necessity claim alone.

### Issue 4: E-INV re-derives F-CIL-perlink instead of citing it
**ASN-0127, E-INV (derivation)**: "LP13 gives `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)` … hence both arity equality `|Σ'.L(a)| = |Σ.L(a)|` and per-slot coverage equality … Then `matches(a, I, Σ') = … = matches(a, I, Σ)`, the middle equality discharged by LP13 (arity and per-slot coverage together)."
**Problem**: This is F-CIL-perlink's derivation repeated in different words. LP13 supplies exactly F-CIL-perlink's hypothesis (`a ∈ dom(Σ.L) ∩ dom(Σ'.L)` with `Σ'.L(a) = Σ.L(a)`), and F-CIL-perlink's conclusion is the very biconditional E-INV needs — and F-CIL-perlink is stated earlier in the document. The inline copy is also the weaker of the two: it compresses the L6 tuple-equality and coverage-determinism steps into "hence," attributing to LP13 (value equality only) what F-CIL-perlink derives explicitly. Duplicated argument is precisely the accretion pattern this note is flagged for.
**Required**: Replace E-INV's matches-chain with two citations: LP13 for persistence and per-link value equality across `Σ →* Σ'`, then F-CIL-perlink for the match biconditional.

### Issue 5: `findlinks_disc` duplicates `findlinks_V` (minor)
**ASN-0127, Discovery anchoring**: "`findlinks_disc(W, d_q, Σ) ≡ findlinks(image(W, d_q, Σ), Σ)` = `findlinks_V(W, d_q, Σ)`."
**Problem**: The definition introduces a second name for a combinator the note already owns — `findlinks_disc` is `findlinks_V` with zero semantic delta; the anchoring distinction lives in how the I-argument is obtained, which the surrounding prose already carries. The split then propagates: F-FULL, F-VDIST, and Q3 speak of `findlinks_V` while D-NONMONO, D-CWP, D-ZERO, and the worked illustration speak of `findlinks_disc`, and the Properties table lists both lanes without recording that they name one function. Two names for one object is notational duplication that invites drift.
**Required**: Use one symbol throughout (drop `findlinks_disc` in favor of `findlinks_V`, or rename once and use it uniformly), or at minimum record the identity in the table rows that use the second name.

## OUT_OF_SCOPE

### Topic 1: Fork-composite discovery
J4 (Fork, ASN-0047) populates `d_new` via the order-preserving bijection `φ` from `d_op`'s content subspace. The induced relation between `findlinks_V(·, d_new, Σ')` and `findlinks_V(·, d_op, Σ)`, and its transclusion-facing consequences (LP16-adjacent), are derivable from F-IMG + F-INERT machinery.
**Why out of scope**: this is derived territory over a named composite, not part of this note's per-transition foundation; nothing here is wrong for lacking it.

### Topic 2: Witness-multiplicity refinement
The "sole in-region witness" analysis suggests a derived count — for link `a` and region `W`, the number of in-region V-positions witnessing the match — which would systematize when reorder swings are absorbed versus transmitted and quantify D-CWP's stability condition.
**Why out of scope**: a refinement layer over F-MATCH, natural material for a successor ASN.

VERDICT: REVISE
