# Review of ASN-0128

## REVISE

### Issue 1: I0's justification for coverage-sameness is falsified by this note's own enumeration predicates, and the resulting information loss is never stated

**ASN-0128, I0 (SamenessIsCoverageEquality)**: "every observer the substrate provides reads coverage, never decomposition: `Observe` matches from-patterns against `coverage(F)`, the `nullified`/active-subset machinery reads `coverage(G')`, and type identity itself is coverage-keyed (TypeEquivalence). Coverage-equal duplicates would be indistinguishable to every query yet doubly present; collapsing exactly them is what `idem = ⊤` is for."

**Problem**: The claim "indistinguishable to every query" is true of the observers I0 lists, but this note then ships observers that read decomposition. Every enumeration predicate (D1 `members`, D3 `targets_of`, B2's `succs`/`chain`, B3's `sources_to`/`target_of`) returns `addrs(·)` — the set of unit-depth span starts — which is a function of the span decomposition, not of coverage. Two surface-emittable, coverage-equal endsets with different denoted sets exist by subtree absorption: `G = [t]` versus `G' = [t, t.ext]` have `coverage(G) = coverage(G')` (PrefixSpanCoverage) but `addrs(G) = {t} ≠ {t, t.ext} = addrs(G')`. These two are distinguishable by `targets_of` — yet I0 declares them *the same*, so under `idem = ⊤` the second emit hits and `t.ext` is silently dropped from every future enumeration answer. The note's own fanout example exercises exactly this pair ("a different address set with identical coverage … finds the now-active tuple, returns its address, takes no step") and presents the hit as a feature without naming the consequence: the caller presented a denotation-distinct target set and the enumeration surface will never reflect it. The committed rules (I0 coverage-sameness; AD denotation-enumeration) are individually precise, but the rationale offered for I0 is false on the note's own surface, and the absorption consequence — the one place where the two regimes visibly collide — appears nowhere.

**Required**: Either (a) refine I0's sameness for AD-encoded emits to denoted-set equality (`addrs(F) = addrs(F') ∧ addrs(G) = addrs(G')`), which on surface emits is strictly finer than coverage equality and restores the "indistinguishable to every query" property; or (b) keep coverage-sameness and fix the text: scope the "indistinguishable" claim to the membership/Observe/nullified machinery, and state explicitly — at I1's hit clause and in the fanout example — that a hit can suppress a denotation-distinct emission, after which enumeration reflects the incumbent tuple's denoted sets, not the suppressed call's. Whichever way, the choice must be argued against the alternative, not justified by a premise the note's own Denotation section contradicts.

### Issue 2: `retract_stale` has an unbound retracting document

**ASN-0128, B4 (age-staleness), Provides**: "`retract_stale(h)` — one `Nullify_Binary(·, d_retr, a)` per `a ∈ stale(h)` evaluated at the initial state"

**Problem**: `d_retr` occurs free. The declared signature takes only the horizon `h`, but the expansion issues wrapper calls that require a retracting document, checked against P0 (`d_retr ∈ dom(Σ.M)`) on every constituent call — and per S3 the from-fill makes `d_retr` part of each retraction's identity and attribution, so it cannot be defaulted by the substrate without deciding who is retracting. The paragraph then asserts "Each constituent call independently satisfies the wrapper's preconditions at its own pre-state" while only discharging P-tgt; P0 cannot even be evaluated for an unbound argument. Secondary ambiguity in the same sentence: "evaluated at the initial state" reads as `Σ_init` on first pass; context shows it means the batch's first pre-state.

**Required**: Bind the parameter — `retract_stale(d_retr, h)` — and discharge P0 explicitly (constant `d_retr` across the batch, so a P0 failure rejects every constituent call; say so). Replace "the initial state" with "the batch's initial state" or equivalent.

### Issue 3: Behavior labels B1–B4 collide with ASN-0126's bridge lemmas B1–B3, which this note cites throughout

**ASN-0128, Behaviors / S3**: behaviors are named "B1 (read-filter) … B4 (age-staleness)", while the note simultaneously leans on ASN-0126's B1 (SharedComponents), B2 (LemmaTransfer), B3 (PathTransfer) in RP-a/RP-b, I1a, I2, DR — and is forced to disambiguate its own labels inline: "(R6a/R6c carried across by ASN-0126's bridge lemmas B2 and B3 — its LemmaTransfer and PathTransfer, not this note's behaviors of the same names — …)".

**Problem**: The same identifiers name unrelated objects in a note that cites the foundation's B-series roughly a dozen times. The text itself demonstrates the confusion is live by carrying a defensive parenthetical, and every foundation citation must be prefixed "ASN-0126's" to stay unambiguous — one dropped qualifier anywhere produces a wrong reading. This violates the spirit of the notation-hygiene rule against foundations: reusing a foundation's labels for different objects is worse than reinventing its notation.

**Required**: Rename the behavior labels to a non-colliding series (e.g., BH1–BH4 or the descriptive names alone — read-filter, determinate-walk, typed-reverse-lookup, age-staleness — which the note already uses in parallel), and drop the disambiguation parenthetical once the collision is gone.

## OUT_OF_SCOPE

### Topic 1: Mutual filtering among multiple B1-registered types
**Why out of scope**: The committed semantics is determinate — each filter type's marks rewrite every *other* type's enumerations, sparing its own — but the design consequence (an address marked by two filter types becomes invisible in both types' default enumerations, while each type's own marks never hide its own members) is undiscussed. This is interaction territory of the same kind as Open Question 1's B1 × B2/B3 cases and belongs with that successor, not in this note.

### Topic 2: A unified surface-level wp for the idem-layered `Emit_K`
**Why out of scope**: DR computes the wrapper's per-branch wp completely; the analogous combined statement for `Emit_K` under `idem = ⊤` (gate ∧ (hit-exists ∨ miss-landing conjuncts)) is assembled nowhere, but all components are pinned (I1's four clauses, ASN-0126's WP, DR's C3-vacuity). Deriving the composite is new assembly, not a gap in any committed claim, and fits the predicate-composition successor.

VERDICT: REVISE
