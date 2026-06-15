# Review of ASN-0133

I worked the proofs of Q0, Q1, Q3, Q5, Q5a, Q-EXT, Q-FLIP, Q6, and the SC tier, and checked the two worked examples arithmetically (both compute correctly). The injection in Q5, the extinction-by-class argument in Q-EXT, the Marker-pattern dedup/born-nullified handling in Q3, and the falsifier counterexample in Q-FLIP are all sound. Two substantive problems remain, plus accreted meta-prose the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: H-SFAIR is claimed not to constrain the environment, yet is used to exclude an environment behavior

**ASN-0133, H-SFAIR (StrongFairnessHypothesis)**: "Like H-FAIR, it constrains only the registry's scheduling, not the environment."

**Problem**: This is contradicted twice over by the note's own use of H-SFAIR.

(a) The note derives the *regime form*: "in this regime H-SFAIR holds iff *no* `(ρ, x)` is trigger-true at infinitely many indices." In the all-SF, extinction-disciplined regime, Q-EXT caps each argument at **one** real fire, so the scheduler *cannot* satisfy "real-fired at infinitely many indices" for any recurring argument. Whether an argument is trigger-true at infinitely many indices is therefore decided by the environment (it re-presents/re-flags), not by the scheduler. So assuming H-SFAIR here is an assumption about the *environment* (it does not cycle), which a scheduler cannot unilaterally enforce.

(b) The note then *uses* H-SFAIR precisely to exclude case (3): "H-SFAIR closes case (3): by its regime form, case (3)'s σ is excluded." Case (3) is defined entirely by an environment behavior ("an environment *cycling finitely many* trigger-true arguments *out of phase*"). A hypothesis that excludes an environment behavior constrains the environment.

(c) The note elsewhere admits exactly this: Q6 says H-SFAIR is "trading regime (i)'s environment footprint-idleness for environment turn-cooperation," and packages "the environment eventually leaving each argument in-domain and trigger-true at some scheduler turn." That is an environment condition.

The asymmetry with H-FAIR is the actual content: H-FAIR's discharge is a *disjunction* (real-fired **or** removed **or** falsified), so a scheduler that eventually fires any persistently-enabled argument satisfies it whatever the environment does — genuinely a scheduler property. H-SFAIR's consequent ("real-fired infinitely often") has no environment-action disjunct, so in this regime it is not unilaterally schedulable. "Like H-FAIR" is the precise error.

**Required**: Drop "Like H-FAIR, it constrains only the registry's scheduling, not the environment." State that H-SFAIR is a property of σ whose satisfiability in the SF+extinction regime requires environment cooperation (the regime form makes it equivalent to "no argument enabled infinitely often," which the scheduler cannot force) — i.e., it is a joint scheduler+environment condition, unlike H-FAIR.

### Issue 2: Q0's universality argument never handles a walk-sequence atom's *unfiltered* value

**ASN-0133, Q0**: "every view-sensitive part of every trigger *and* of every domain can be moved to one chosen term view by the rebuilds just classified, and the per-rule conjuncts, so rewritten, PC0-conjoin into a single PC3-conforming term."

**Problem**: The classified rebuilds are: (a) the four view-parameterized atoms to audit/active via `L_K`/`A_K` bases (PC3); (b) the six UV-collections' *default* values as filters; (c) `chain`-default via `elems`-then-filter. None of these produces `chain`'s **unfiltered** (active/audit) value. Unlike `succs`/`sources_to`/`stale`, whose "raw active reading" is an `A_K`-based term renderable at any top-level view, `chain`'s element set requires the determinate walk — transitive closure — which PL cannot rebuild (PC6a, C-reach). So `chain`'s unfiltered value is available *only* by reading the `chain` atom at a non-default term view; at top-level `default`, `elems(chain(x))` is the filtered set and the full walk is unrecoverable.

A trigger can genuinely need this: `(∃ y ∈ elems(chain(x)) :: P(y))` quantifies over the full walk (a valid QD domain by set-valued closure). `is_in_chain` does **not** close the gap — it tests membership of one specific element, it is not a domain to quantify over.

The conclusion ("∈ PL for *every* registry") does in fact hold, because top-level **audit** renders every constituent (audit native, active via `A_K` bases, default via UV filters, and `chain` natively full since audit=active for the walk). But Q0 never states that a safe common view always exists, and the "Heterogeneous rewrite, worked" subsection actually *picks top-level default* — safe there only because `ρ_walk` reads `succs` (rebuildable), not `chain`. So the proof of the central recognizability claim has a missing step exactly where the choice of common view is constrained.

**Required**: Add the step that a common admissible view always exists — e.g., top-level audit renders every constituent, including the one value (`chain` unfiltered) that no fixed-view-base rebuild reconstructs — and note that top-level default is *unsafe* whenever a trigger consumes a walk-sequence atom unfiltered, so the worked example's choice of default is licensed only by its atom set.

### Issue 3: Q0 re-derives foundation view-mechanics at essay length

**ASN-0133, Q0**: e.g. "View-parameterization is not, however, the whole of view-sensitivity, and the merge must account for the rest."; "What that blocks is only the *naive* merge — the one that leaves each view-parameterized atom at its native view; for a heterogeneous-view registry that merge is ill-formed."; "the filter being precisely UV's own default-view rewrite (ASN-0129) recast as a PL term."

**Problem**: A large fraction of Q0 narrates the proof and recapitulates UV/PC3 (foundation) — what UV rewrites, that PC0 needs a common view, what "naive merge" means — before stating the rebuild equations. The load-bearing content is small: each of audit/active/default values is expressible from `A_K`/`L_K` bases plus the view-stable `is_filtered`, so all constituents render at one chosen view; `chain` is the sole non-rebuildable case (Issue 2). The "Heterogeneous rewrite, worked" subsection then restates the naive-merge-fails reasoning a third time before its (genuinely useful) value computation. A precise reader must skip connective and recapitulative prose to reach the four rebuild equations.

**Required**: Compress Q0 to the rebuild equations + the common-view existence argument; cite UV/PC3 rather than re-deriving them; keep the worked subsection's value table but drop its re-derivation of Q0's argument.

### Issue 4: Q6's three-case analysis carries an unproven exhaustiveness claim and is not load-bearing for the theorem

**ASN-0133, Q6**: "The non-grow-only case has a definite structure: three obstructions to a *reached-and-held* quiescent state, not all failing the same way."

**Problem**: The positive result — under H-SFAIR + bounded growth, quiescence is reached and held — follows *directly* from the regime form ("no argument trigger-true infinitely often" + finitely many arguments ⇒ finite max trigger-true index ⇒ quiescent past it). The three-case taxonomy is offered as necessity-motivation, but (i) it is stated as an exhaustive classification ("three obstructions") with no proof of exhaustiveness, and (ii) case (1) is excluded by a *standing hypothesis of the regime* (bounded growth), so its full H-RF/H-FAIR/bounded-growth verification re-examines a case the precondition already rules out. The H-SFAIR closure spells out only case (3), though the regime form excludes (2) identically — leaving the taxonomy half-used.

**Required**: Either prove the three obstructions exhaustive, or demote the taxonomy to two named counterexamples establishing *necessity* of the extra hypothesis (one holding-failure, one reaching-failure), and drop the "three obstructions" exhaustiveness framing and the case-(1) walk-through.

### Issue 5: Repeated downstream deferrals and forward-pointer justifications

**ASN-0133, multiple sections**:
- Worked composition: "the general cross-rule coupling discipline ... is Open Question 4's cascade/re-opening theory, left there." Open question 4: "is where a future cascade/re-opening theory would live." Q8 re-entry connects to the same. Three sites defer to one downstream location.
- Q-EXT: "This *step-agnosticism* is exactly why Q5a's bound survives environment input in the open model." — justifies a property by its downstream use rather than stating the property.
- Q1 close: "Recognizability and absorption are *unconditional* relative to the dynamics hypotheses the termination results below name — fairness, finite real fires, bounded domain growth." — forward inventory of hypotheses not yet introduced.

**Problem**: These are the accretion patterns the classifier flags: the same forward reference restated across sections, and prose around a claim that explains why it will matter later instead of advancing it.

**Required**: State each property where it is defined; carry the cascade/re-opening pointer once (Open Question 4) and reference that single site; remove the anticipatory hypothesis inventory.

## OUT_OF_SCOPE

### Topic 1: A constructive scheduler/environment model realizing H-SFAIR
**Why out of scope**: Showing that *some* (scheduler, environment) discipline satisfies H-SFAIR — the turn/serialization model its satisfiability needs — is genuinely a protocol/implementation result, correctly listed under "What this note doesn't cover." The note need only state the conditional theorem (fixing Issue 1's mis-scoping); building the witness belongs above this layer.

### Topic 2: `pd_extinct` (SF certification as a designated class)
**Why out of scope**: Open Question 1 correctly identifies that ASN-0130 ships only the ST⁺ certificate, and that an SF certificate to make "terminates on bounded input" a structural lint is catalog growth for a future ASN, not a revision here.

META: not warranted — the substrate-relevant nucleus (quiescence is PL-recognizable; absorption; the falsifier accounting via PD0/PD1/PD2) is genuine state/invariant content stated abstractly, and the scheduler/environment machinery is deliberately and correctly deferred; the issues above are inconsistency and incompleteness, which are fixable.

VERDICT: REVISE
