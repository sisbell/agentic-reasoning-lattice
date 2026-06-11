# Review of ASN-0127

The technical content checks out: I verified the derivations (F-IMG-SWING's reindexing and cardinality pinning, F-IMG-TAX's four witnesses by direct computation of the bijection equations, F-UDIST/F-IMONO, F-FULL's bridge to LP12, E-CONS's two directions including the least-index anchor, D-CWP's bridge and biconditional, and every numbered computation in the worked illustration, including the prefix-incomparability premises and the J0/J1★ composite obligations). I found no logical error, no missing boundary case, and no precondition gap. All cross-references are to foundation ASNs. The findings below are all instances of the forward-reference/meta-prose accretion this note's anti-bloat classifier asks to be flagged — prose-level, individually small, but exactly the pattern that compounds across cycles.

## REVISE

### Issue 1: Orphaned C1a/run-structure exposition in Phase 1
**ASN-0127, Phase 1, paragraph after F-IMG's degenerate cases**: "When `W` is a contiguous V-span in some subspace `S`, the image is a union of I-runs delivered by ASN-0058's *restriction* decomposition. … The restriction is load-bearing: blocks of the *full* arrangement (B1–B3, ASN-0058, quantified over all of `dom(Σ.M(d))`) may straddle `W`'s boundary, and their full I-extents `I(βⱼ)` would overstate the image…"
**Problem**: No claim in this note consumes the run decomposition. "I-run," "block," and C1a never reappear — F-IMG-MONO through D-CWP and the entire worked illustration treat the image as a plain forward image of a partial function. The "load-bearing" sentence defends against a miscomputation (using full-block I-extents) that no claim anywhere performs; this is anti-objection prose, not reasoning. The only sentence in the paragraph with downstream relevance is the closing one (S3★ routing link-subspace positions into the image, with L4 admissibility), which is genuine context for K.μ⁺_L and D-CWP's link-subspace retention positions.
**Required**: Delete the C1a/run-structure material or compress it to a single citation-bearing sentence; retain the S3★/L4 sentence. If the run structure is groundwork for composing with ASN-0058's resolution machinery, it belongs in the ASN that performs that composition (the note's own Q4 territory).

### Issue 2: Defensive parentheticals in F-IMG-TAX's witness-admissibility paragraph
**ASN-0127, F-IMG-TAX, *Witness admissibility***: three clauses — "(K.μ~-FIX is a consequence of admissibility, not a premise available while admissibility is being established)"; "— the witnesses are realizable at states K.μ~ can actually fire from —"; "pairwise distinct by ChainEnumerationInjectivity (ASN-0093), not by stipulation."
**Problem**: Each is protocol rationale rather than content. The construction already does the work the parentheticals defend: domain fixity is proved "by construction" in the same sentence, so the circularity disclaimer about K.μ~-FIX adds nothing; the realizability em-dash clause restates the S3★ discharge it interrupts; "not by stipulation" argues with an objection nobody in the document raises once the ChainEnumerationInjectivity citation is present. This is review-cycle scar tissue the precise reader must step around.
**Required**: Delete all three clauses. The paragraph's obligations (admissibility (i)–(v), S3★ at pre- and post-state, value-distinctness) remain fully discharged without them.

### Issue 3: Correction-shaped prose and verbatim D-ABSORB restatement in D-NONMONO's K.μ~ clause
**ASN-0127, D-NONMONO, K.μ~ bullet**: "whether `findlinks_V` inherits a monotone motion is decided not by the injectivity of `Σ.M(d_q)` but by which of F-IMG-TAX's two moved-image shapes obtains; injectivity governs only which shapes are *available* (F-IMG-TAX), not the monotonicity conclusion directly" and "(and image-motion is in any case necessary but not sufficient for the discovery set to move, D-ABSORB)."
**Problem**: The first sentence corrects a misattribution no part of the document makes — nothing in the note ever claims injectivity decides monotonicity — so it reads as a prior finding's content relocated rather than removed (the not-X-but-Y framing is the tell). The second parenthetical restates D-ABSORB's statement verbatim in an adjacent section where a bare citation suffices; the same fact now appears twice in the document in different words.
**Required**: State the case split directly — containment image-motion ⟹ F-IMONO applies (bridged through F-INERT); incomparable image-motion ⟹ monotone transfer unavailable, refuted by the worked illustration's swing — citing F-IMG-TAX and D-ABSORB without re-narrating either.

### Issue 4: Duplicated K.μ~ admissibility derivation in the worked illustration's swing bullet
**ASN-0127, Worked illustration, *Swing under K.μ~***: "a valid K.μ~ on `d`: `π` permutes the position set `{v_1, v_2, v_3}`, so `dom(Σ'.M(d)) = π(dom(Σ.M(d))) = dom(Σ.M(d))` — domain fixity by construction; it preserves length and subspace, has non-trivial net effect (`v_1`'s image changes), and the arrangement-shape invariants (D-CTG★, D-MIN★, ASN-0047; S8a, S8-depth, ASN-0036) hold in the post-state because the V-position domain is unchanged."
**Problem**: This is a near-verbatim restatement of F-IMG-TAX's witness-admissibility construction. The document already established the economical pattern at D-ABSORB's witness ("the injective-witness shape of F-IMG-TAX, whose transposition `π = (v₁ v₂)` is admissible by the same construction"); the same argument should not appear in full twice — the illustration's state (initial-segment positions `[1,k]`, first emissions of `A_C(d)`) is exactly the pinned shape the F-IMG-TAX paragraph covers.
**Required**: Replace the re-derivation with a cite-back to the F-IMG-TAX construction, as D-ABSORB already does.

### Issue 5: D-PRES's first sentence duplicates the discovery-anchoring intro
**ASN-0127, Discovery anchoring**: intro — "the I-argument is read off the live arrangement at query time rather than given as a fixed set"; D-PRES — "image(W, d_q, Σ) is a live reading of d_q's arrangement."
**Problem**: The same statement appears in adjacent paragraphs in different words. D-PRES's substantive content is its second sentence (editing `d_q` moves the resolved request while `dom(Σ.L)` is fixed); the first sentence is the intro repeated.
**Required**: Keep one formulation. The cleanest cut: drop D-PRES's first sentence and let the named claim carry only the mutability observation.

## OUT_OF_SCOPE

### Topic 1: Per-state availability characterization for containment motion
**Why out of scope**: F-IMG-TAX correctly establishes the class-level facts (non-injectivity necessary; both shapes realized by witnesses). Characterizing *for which* `(Σ.M(d), W)` an admissible `π` exhibiting containment motion exists — a per-arrangement decidable condition rather than an existence claim over the class — is a new characterization result, not a gap in this ASN.

### Topic 2: Formal predicate syntax for F-CIL's side condition
**Why out of scope**: F-CIL's "consults only `Σ.L` and query-data" is the same informal predicate-class discipline as ASN-0098's Closure schema (★), and it is applied here only to `matches`, where the discharge is concrete. A formal grammar of admissible membership predicates is future territory, not a defect of the meta-lemma as used.

VERDICT: REVISE
