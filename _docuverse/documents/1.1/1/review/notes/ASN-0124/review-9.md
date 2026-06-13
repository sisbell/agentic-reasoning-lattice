# Review of ASN-0124

I checked the derivations claim by claim and reconstructed the four worked constructions (FD-NEUT(c), FD-LOSSY, the FD-FRESH composite, the worked illustration) against the foundation contracts they cite. **The mathematics is sound.** FD-IMGC's `image_C = image ∩ dom(C)` equality survives the non-injective-arrangement case (the `b ∈ dom(C)` guard forces every preimage to content subspace via S3★/SD); FD-STEP's three movers are exhaustive over the vocabulary and the K.μ⁺ formula is correct in both the already-member and not-yet-member cases; the FD-FRESH clear-and-rebuild composite discharges J0/J1★/J1'★ initial-to-final exactly as claimed; FD-VDYN(d)'s absorption characterization and its worked-illustration "d_C drops" instance are mutually consistent; FD-WITNESS's two directions are correctly routed through P4a (⊆) and P4★+P2 (⊇), and FD-SUPER is properly restricted to composite boundaries. The depth requirements (explicit derivations, a non-trivial wp in FD-CWP, a concrete worked illustration verifying the key postconditions) are all met. No cross-ASN references outside the foundation set.

The findings below are all the meta-prose accretion this note's `review-mode.anti-bloat` classifier exists to catch. None is a correctness or completeness defect.

## REVISE

### Issue 1: Forward-reference deferrals around claims
**ASN-0124, FD-SOUND and FD-PART**:
- FD-SOUND closes: "(What a query keyed on past containment looks like, and why it is a different — also legitimate — operation, is the subject of the historical-companion section.)"
- FD-PART contains "(FD-IDENT below)" mid-sentence and "The conjunctive "contains all of it" question is not lost; it is a derived query, by composition — FD-COOC."

**Problem**: These are the exact pattern the classifier names — pointers to downstream claims that do not advance the claim carrying them. The historical-companion section, FD-IDENT, and FD-COOC each stand on their own; a reader following FD-SOUND or FD-PART must step past the pointer. "is not lost" is additionally defensive (answering an objection rather than stating the property).

**Required**: Delete the FD-SOUND parenthetical; in FD-PART drop "(FD-IDENT below)" and state the relation-strength point ("shared address of some portion, weaker than containment") without the forward citations and without "is not lost."

### Issue 2: Defensive justifications explaining why a property is not a defect
**ASN-0124, FD-NONMONO, FD-GROUND, and the post-FD-COINC paragraph**:
- FD-NONMONO: "this is correct behavior, not instability — Nelson's live set "shrinks (deletions) and grows (new inclusions)" by design."
- FD-GROUND: "(When the I-argument arrives through FD-RES this is moot — resolution is grounded — but the primitive is total over 𝒫(T) and safe there.)"
- Post-FD-COINC closer: "...the specification's job is to keep the two contracts distinct, and that is what FD-SOUND/FD-GHOST do."

**Problem**: Each defends rather than advances. "correct behavior, not instability" rebuts an imagined reading the Nelson citation already forecloses. The FD-GROUND parenthetical explains why the claim is needed despite being moot under composition — the groundedness it leans on is already FD-RES(a). The post-COINC clause is essay about the specification's purpose, appended to a paragraph that had already made its substantive point (J1★/J1'★ pin the index).

**Required**: Trim FD-NONMONO to the by-design statement; drop the FD-GROUND parenthetical (the primitive's totality is evident from its `I ⊆ T` signature); end the post-COINC paragraph at "...has implemented FD-HIST instead."

### Issue 3: The frame observation is re-enumerated in three claims
**ASN-0124, FD-LOCAL / FD-NEUT(a) / FD-IDENT(a)**: FD-LOCAL establishes χ "is a function of `I` and `Σ.M(d)` alone ... no `Σ.C` value, no `Σ.L`, no `Σ.R`, no allocation history occurs in it." FD-NEUT(a) re-asserts "no occurrence of origin(·), of Σ.R, or of any allocation-event datum"; FD-IDENT(a) re-asserts "no stored value Σ.C(·) is ever read" — while itself citing "by FD-LOCAL aggregated over d."

**Problem**: Two paragraphs restate FD-LOCAL's frame in different words. FD-IDENT(a) shows the redundancy in microcosm: it cites FD-LOCAL and then re-derives the frame anyway.

**Required**: Have FD-NEUT(a) and FD-IDENT(a) cite FD-LOCAL for the frame and assert only their specific consequence (origin-blindness; value-blindness — "two states agreeing on `M` give identical answers"), without re-listing the components χ does not read.

## OUT_OF_SCOPE

### Topic 1: Temporal ordering and past-state reach of the historical query
**Why out of scope**: FD-HIST answers "ever contained" without rank, time, or version order, and FD-WITNESS witnesses against past arrangements only through the present provenance relation. The note correctly does not attempt a temporal contract or genuine past-state reach; both are captured in Open Questions 2 and 4. FD-HIST's presence as a characterization tool (bounding the live query, locating the green deviation) is in-scope and properly motivated, not a second operation specified for its own sake.

META: not applicable — the note specifies a query's abstract contract (FD-COMPLETE/FD-SOUND), its algebra, and its dynamics, with implementation evidence kept clearly in the evidence section; it has not drifted into implementation mechanics.

VERDICT: REVISE
