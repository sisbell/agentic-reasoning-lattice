# Review of ASN-0134

I checked the proofs in §1–§9. The mathematics is sound: H0/H1/H2 are correct (including the first-emission boundary in H2, handled explicitly), G1's confluence-by-adjacent-transposition argument is valid, H3's two distinct commutation modes are correctly separated, the §4 both-miss / I1a literal-vs-operative analysis is right, the V2 strict-implication chain and its converse-failure witnesses check out, and the §7/§8 worked traces compute correctly. The "seven of eight clauses load-bearing" necessity argument holds. I found no correctness defect, no missing edge case, and no foundation reinvention.

The findings below are all the `review-mode.anti-bloat` kind: meta-prose and content that has accreted across cycles around forward references. They are REVISE because the note carries the anti-bloat classifier and these patterns compound if not cut at source.

## REVISE

### Issue 1: The K.σ-scoping exposition is restated in full at five sites

**ASN-0134, §1 parenthetical / §4 body / H3 / SAFE(c) / MIC omissions**: The same three facts — K.σ takes a caller-supplied `d`, two same-`d` registrations collide and are "resolved by rejecting the loser," and freshness is an "assumed precondition supplied by the excluded entity-allocation layer" — are spelled out at five locations.

- §1: "K.σ is a state-changing step that the step-level claims A0–A7 govern like any other (canonicity, A6, included) ... treating document-address freshness as an assumed precondition."
- §4: "It remains a step of `𝔼` — the step-level claims A0–A7 apply to it unchanged, canonicity (A6) included ... the substrate resolves by *rejecting the loser* ... *assumed preconditions*, supplied by the entity-allocation layer this note excludes."
- H3: "(Two registrations of the *same* `d_new` collide as §4's scoping notes, resolved by rejecting the loser; freshness excludes them from one schedule.)"
- SAFE(c): "two agents racing the *same* caller-supplied `d` is a genuine collision, but the substrate resolves it by rejecting the loser ... the office of the assumed document-address freshness the excluded entity-allocation layer supplies."
- MIC: "document-address freshness ... is an assumed precondition discharged by the excluded entity-allocation layer."

**Problem**: The §1 and §4 sentences ("step-level claims A0–A7 govern/apply ... canonicity A6 included") are near-verbatim duplicates; SAFE(c) and MIC re-derive the rejection-and-freshness mechanism rather than pointing to it. This is the "multiple paragraphs defer to the same downstream location" and "two paragraphs say the same thing in different words" pattern.

**Required**: State the K.σ scoping once where the conflict analysis lives (§4 body). Replace the §1 parenthetical, H3 parenthetical, SAFE(c), and MIC restatements with bare pointers (e.g. "K.σ scoped out, §4").

### Issue 2: §4's closing paragraph recapitulates its own per-instance analysis

**ASN-0134, §4 ("The honest statement is therefore two-level…")**: After instances (i), (ii), and the target-residence race are each analyzed at length, the closing paragraph re-summarizes all three — the toggle reading the global `A_K`, the both-miss duplicate, surface-discipline excluding none, clause 8 suppressing (i), instance (ii) reduced by neither — content already established above.

**Problem**: The paragraph's own phrasing concedes the redundancy: "a duplicate per-home MIC permits, *as derived at instance (i) above*." The clause-8 role is itself stated twice inside instance (i) ("only a *global* per-coverage-class serialization … does (§9 clause 8)" and "Clause 8 (§9) is exactly what restores the coincidence …") and then a third time in this closing recap. A reader who has followed the per-instance derivations skims the recap.

**Required**: Reduce the closing paragraph to the genuinely new synthesizing claim (the two-level step-vs-operation framing and the "two families part company under discipline" contrast) and drop the per-instance re-derivations, which the instance paragraphs already own.

### Issue 3: Numbering/ordering justifications and a use-site inventory (minor)

**ASN-0134, V1 / W4 / §4 close**:
- V1: "durability — V1, *numbered below V2 but presented after it, as the coda once soundness is settled* — follows."
- W4: "the stronger run contiguity (W4), *numbered with this contiguity family (W2/W3/W4) but … deferred to §6's dedicated treatment*."
- §4 close: "§9's SAFE(b) notes the toggle family from the de-duplication side, and W5 and Open Question 9 the target-residence race."

**Problem**: The first two are document-ordering justifications (prose explaining why a claim sits where it does); the third is a downstream use-site inventory. None advances the reasoning of the claim it decorates — both are explicitly flagged patterns.

**Required**: Drop the numbering/placement asides (present V1 after V2 without narrating that choice; introduce W4 in §6 without justifying the deferral). Cut the use-site inventory or compress to a single pointer.

## OUT_OF_SCOPE

None to add. The note correctly confines the excluded topics (scheduler/fairness, rule bodies, BEBE, mechanism choice, predicate-cost) to "What this note does not cover" and the Open Questions, and defines no claims for them.

META: (none — the note defines an abstract per-implementation contract (MIC) and its guarantees (SAFE) stated independently of mechanism, which is legitimate specification territory; it has not drifted into implementation mechanics.)

VERDICT: REVISE
