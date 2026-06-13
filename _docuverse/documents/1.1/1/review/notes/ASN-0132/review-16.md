# Review of ASN-0132

The mathematics is sound. I checked the definition's well-definedness (finite computable comprehension over `dom(Σ.L)`, L-fin + FL-DEC), the four-case unit argument in CN-UNIT (each rejected multiplicity is either a `Σ.M`-quantity excluded by CN-LOC or an inside-`touch` quantity absorbed by the existential — including the version-refraction case, which correctly reduces to appearance multiplicity via J4's "no other elementary steps" leaving `Σ.L` untouched), the CN-MONO wp derivation (which reconstructs FL-WP(a) exactly, second conjunct and all, and correctly inherits the disciplined-domain collapse from ASN-0086 wp Case 2 rather than re-deriving it), and the worked example (every contribution — `a₁`=1 with triple-anchor collapse, `a₂`=0 nullified-but-present, `a₃`=1 orphan, `a₄`=0 disjoint, `a_R`=0 empty-from, plus the all-wildcard `=4` and the home-to-`d₂` genuine CN-ZERO). All verify. No skipped cases, no proof-by-checkmark, no cross-ASN reference outside the foundation set, no notation reinvention. The findings below are prose only, responsive to the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Self-referential and rhetorical framing that does not advance the argument
**ASN-0132, intro and several claim lead-ins**: recurring meta-prose announces importance or describes the note rather than carrying reasoning, and the reader skips it to reach the claim:
- Intro: "It is forced by what a link *is*, and **most of this note is the argument that forces it**." — the closing clause describes the document, not the subject; the thesis is discharged by CN-UNIT.
- Under CN-DEF: "**One point deserves immediate emphasis:**" — filler before a substantive sentence.
- "**This is the load-bearing fact for everything below:**" / "**The separation is load-bearing:**" / "**One caveat applies, and CN-STAB makes it precise.**" / "...and **is the whole content of the consistency guarantee**."

**Problem**: These are non-advancing rhetorical lead-ins; individually minor, collectively they are the meta-prose accretion the classifier targets. The substantive content sits in the claims themselves (CN-UNIT, CN-DEF, CN-ENUM, CN-STAB).
**Required**: Delete the framing and state the content directly; the claim blocks already carry it.

### Issue 2: Cost section over-elaborates a scope exclusion
**ASN-0132, "A census, computed" closing (cost discussion)**: "This is a genuine and attractive design aspiration: a cheap count is a planning primitive, letting a front end size a result before committing to the expense of retrieving it."
**Problem**: The substantive point — cost-asymmetry is quality-of-service, not a correctness obligation, hence not a claim — is one sentence; the "design aspiration / planning primitive / size a result" elaboration is essay content. The planning-primitive idea is then restated a third time in the Open Questions ("...let a count serve as a planning primitive"), so the same notion appears in CN-OBT's neighbourhood, the cost paragraph, and the open question.
**Required**: Reduce to the QoS-vs-correctness distinction (which one sentence plus CN-OBT already carry) and let the Open Question hold the aspiration; drop the intra-document duplication.

## OUT_OF_SCOPE

The topics raised in passing during review — agreement between an address-set count and a V-spec count (resolution invariant), count/enumerate cross-inquiry consistency under a concurrency discipline, count cacheability conditions, fragmented-endset deduplication guarantees, count-versus-enumeration cost, and federated counting across independently administered stores — are correctly left to future ASNs and are already captured verbatim in this ASN's Open Questions. No claim drifts into them; CN-UNIT and CN-ORPHAN *apply* ASN-0127's existence/discovery taxonomy and ASN-0098's discovery predicate rather than rebuilding them.

VERDICT: REVISE
