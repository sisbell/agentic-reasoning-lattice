# Review of ASN-0133

The mathematics here is sound. I checked the load-bearing proofs — Q0's view-rebuild into a single PL term, Q3's idem=⊤ dedup-vs-fire exclusion, Q5's injectivity-by-index bound, Q5a's open-model domain bound, Q6's three-obstruction case split, and the worked Σ₀→Σ₁→Σ₂ trace — and they hold up; the hypothesis-naming discipline the note sets for itself is genuinely met. The findings below are the meta-prose accretion the `review-mode.anti-bloat` classifier is watching for, plus one parse stumble. None are correctness errors.

## REVISE

### Issue 1: the Marker-pattern definition enumerates its downstream consumers
**ASN-0133, Q3 (StaticCheckability), "The Marker pattern"**: "the **Marker pattern**, the load-bearing construction this note returns to (Q-EXT, Q5a, and the worked example)"
**Problem**: The introduction of the construction inventories where it will later be used — exactly the "definition's introduction enumerates downstream consumers" pattern. The parenthetical, and the self-description "the load-bearing construction this note returns to," advance the definition not at all.
**Required**: Drop "(Q-EXT, Q5a, and the worked example)" and the self-description; introduce the Marker pattern by what it is.

### Issue 2: the per-occurrence reading is justified by a use-site inventory
**ASN-0133, H-FAIR (FairnessHypothesis)**: "This is the *per-occurrence* reading, not once-per-argument: ... — the strength Q6's regime (i) and the finite-σ case both turn on, and the strength H-SFAIR's strong form must supply (below)."
**Problem**: The reading is defined and then defended by listing the three downstream sites that depend on it. The definition (through "across a later tail") stands on its own; the trailing "what turns on it" list is forward-reference meta-prose.
**Required**: Keep the definition; cut the use-site inventory.

### Issue 3: the Marker-pattern at-most-once mechanism is re-spelled at each use
**ASN-0133, Q-EXT and Q5a**: Q-EXT states the mechanism in full — "its trigger is an SF spelling (SF by PD0's quantifier rule) and its emit-the-witness contract is the extinction half in Q3's decidable-match case ... registration-time and spelling-level." Q5a re-spells the same breakdown: "at-most-once-per-argument is a registration-time fact for these Marker-pattern rules (Q-EXT — the SF spelling via the spelling class, the extinction discipline via Q3's decidable-match)."
**Problem**: The "two halves, both checkable at registration (SF via the spelling class, extinction via Q3's decidable match)" mechanism is given in full at both sites (and re-derived again in the worked example's Class-check/Extinction paragraphs). After the first full statement a citation carries it.
**Required**: State the mechanism once (Q-EXT); at Q5a cite it ("at-most-once by Q-EXT") without re-spelling the SF-via-spelling-class / extinction-via-Q3 split.

### Issue 4: confusing trailing self-reference in the pdef-trigger conditionality note
**ASN-0133, "Triggers: inline or by reference"**: "so recognizability is *not* unconditional relative to PR-DISC (Q0 and Q1 are unconditional only relative to the termination dynamics hypotheses, Q1)"
**Problem**: The bare "Q1" appended after "hypotheses" reads as a list element rather than a see-pointer, and the parenthetical also restates Q1's own unconditionality claim. The reader must stop to disambiguate which conditionality (PR-DISC vs. dynamics) is meant.
**Required**: Drop the parenthetical (Q1 already states the unconditionality), or rewrite the pointer unambiguously, e.g. "(unconditional w.r.t. the dynamics hypotheses — see Q1 — but conditional on PR-DISC here)."

### Issue 5: the intro thesis restates the subtitle
**ASN-0133, opening paragraph**: "The note's discipline is to name each hypothesis rather than smuggle it in."
**Problem**: This is essay content about the note's own method, and it duplicates the subtitle ("termination as a conditional theorem with every hypothesis named"). The preceding sentence already states the substantive fact (unconditional termination is not provable; honest treatments name conditions).
**Required**: Cut the self-referential sentence; the subtitle and the preceding fact already carry it.

## OUT_OF_SCOPE

None to route. The "What this note doesn't cover" and "Open questions" sections already scope the future work appropriately — scheduler construction and the serialization that discharges H-ATOM, environment/workload models, the `pd_extinct` SF-certificate (OQ1), a PL surrogate for H-W (OQ2), per-scope vs. global termination (OQ3), and cross-scope re-entry (OQ4). In particular the SF-certificate gap (the note relies on SF-membership being a decidable syntactic check, while ASN-0130 ships only the ST⁺ certificate) is correctly captured as OQ1, not a defect in this note.

VERDICT: REVISE
