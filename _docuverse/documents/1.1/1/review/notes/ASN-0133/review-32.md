# Review of ASN-0133

I checked the termination machinery hard, because that is where this kind of note fails: Q5/Q5a's bounds, Q6's regime split, the H-RF/H-W separation, the SF/extinction interaction, the open-model environment cases, and the Q0 view-rebuild. The mathematics holds up. The classification in Q0 is genuinely exhaustive (every view-sensitive constituent — the four view-parameterized atoms, the four UV-rewritten behavior collections including `chain` via `elems`/`is_in_chain` — is accounted for, and the Boolean-trigger restriction is what makes the `chain`-order loss harmless). Q5a's separation from Q5/H-W is sound, Q6's three-obstruction split is correct, the regime form of H-SFAIR is derived correctly and the max-`N′` closure is airtight. The worked `cmt`/`res` example traces the nested quantifier end-to-end and exercises the in-place-falsification discharge against removal. No correctness defects found.

The findings below are the anti-bloat patterns this note's classifier asks for, plus one forward-pointer. They are prose-efficiency, not correctness — but the classifier is on precisely because accreted meta-prose around the forward references has been compounding across cycles, so they belong under REVISE.

## REVISE

### Issue 1: "Triggers: inline or by reference" restates two points 3× / 2× within one paragraph
**ASN-0133, The rule model → "Triggers: inline or by reference"**: the inline-registry-carries-nothing point appears three times — "A registry of inline triggers depends on ASN-0130 not at all — its triggers are PL terms evaluated directly (PC4/PC5)" … "a registry of inline triggers carries none" … "An inline-trigger registry carries no such premise — its triggers are PL terms by construction (PC4/PC5)" — the first and last being near-verbatim, same `(PC4/PC5)` citation and all. The de-registration-still-evaluates point appears twice — "such a trigger stays evaluable … even after its definition is de-registered" (own definition) and "A trigger whose definition references a since-de-registered definition still evaluates: PR3 keys evaluation on content, not registration …" (referenced definition) — two scenarios, identical mechanism (PR3 keys on ever-registration/content), stated in full both times.

**Problem**: This is the "two paragraphs say the same thing in different words" pattern, concentrated inside a single already-long paragraph. The reader has to recognize the third inline-statement as the same as the first, and the second de-registration sentence as the same mechanism as the first. The load-bearing content here is narrow: (a) inline triggers carry no PR-DISC premise; (b) pdef triggers inherit PR-DISC, which PR3a/PR2 need for `expand ∈ PL`; (c) PR3 keys on content so de-registration (of self or referent) doesn't break evaluability.

**Required**: State (a) once, (b) once, (c) once (covering self- and referent-de-registration in one sentence). The paragraph should lose roughly a third of its length with no loss of content.

### Issue 2: H-SFAIR's characterizations are restated in full across three sections instead of stated once and cited
**ASN-0133, H-SFAIR / Q6 / "What this note doesn't cover"**: three H-SFAIR meta-claims each recur:
- *Satisfiability needs turn-fairness this note doesn't supply* — 3×: "satisfiable only under a turn-fairness in which the scheduler eventually fires any recurrently-presented argument — a condition this note neither states nor derives" (H-SFAIR), "satisfiable only under a turn-fairness this note does not supply" (Q6 parenthetical), "the turn/serialization model H-SFAIR's satisfiability needs" (doesn't-cover bullet).
- *H-SFAIR is the strong-scheduling form of regime (i), not a parallel route* — 2×: "H-SFAIR is the strong-scheduling form of regime (i), not a disjoint second route" (H-SFAIR), "regime (i) secured by scheduling, not a parallel route" (Q6).
- *The regime-form iff* — stated in full at H-SFAIR ("in this all-SF regime H-SFAIR holds iff no `(ρ, x)` is trigger-true at infinitely many indices") and then restated in full at Q6 immediately after the citation "By its regime form (derived at H-SFAIR), in this all-SF regime H-SFAIR holds iff no `(ρ, x)` is trigger-true at infinitely many indices."

**Problem**: Q6 cites "derived at H-SFAIR" and then re-derives/re-states the iff anyway; the satisfiability caveat is paid three times. This is the "multiple sections defer to / restate the same result" pattern — the cross-references resolve to content that is also reproduced in place, so the citations buy nothing.

**Required**: State the regime form and the satisfiability-needs-turn-fairness condition once, at H-SFAIR. Q6 should cite-and-apply ("by H-SFAIR's regime form, case (3)'s σ is excluded …") without restating the iff; the doesn't-cover bullet should be the only other mention.

## OUT_OF_SCOPE

### Topic 1: Registration-checkability of the stratification legality condition
The worked example introduces stratification with the legality condition "resolver emissions never **enlarge the producer's domain**," and argues for this case that re-arm is vacuously excluded (SF producer) so domain growth is the only divergence route. The note's central taxonomy is checkable-at-registration vs meta-level (Q-EXT makes at-most-once a registration fact; bounded growth is meta-level). It does not place the stratification legality condition on that axis — yet for the worked rule it is a syntactic footprint check: the producer domain reads `attn`/`tgt`, the resolver emits `res`, and PD2 (FrameStability, ASN-0129) gives invariance of an active-slice term under deposits of types outside its read set, so "resolver does not enlarge producer's domain" is decidable from FP footprints alone.

**Why out of scope**: The note frames stratification as a design heuristic, not a core claim, so omitting its checkability status is a scope choice rather than a gap. But it is a natural refinement adjacent to Open Question 1 (structural lints for "this registry terminates on bounded input") — a future note could promote stratification legality to a PD2-based registration lint, parallel to Q-EXT, rather than leaving it a semantic condition on emissions.

VERDICT: REVISE
