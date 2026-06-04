# Review of ASN-0091

## REVISE

### Issue 1: Clause (i) discharge bundles per-position and set-level invariants under one justification
**ASN-0091, "Clause Correspondences and Per-Invariant Discharges" (K.μ~ admissibility table, clause (i))**: "each follows at Σ' from RA-dom (dom(Σ'.M(d)) = dom(Σ.M(d))) together with state-independent V-position projections (subspace, depth, componentwise positivity, per-subspace ordering), none disturbed by the bijection"
**Problem**: Clause (i) covers four invariants of two distinct kinds, but the one-line discharge treats them uniformly. S8a (zeros=0, depth≥2, positive components) is a *per-position* predicate, preserved because each position in the unchanged domain still satisfies it. D-CTG★ (contiguity) and D-MIN★ (minimum = [S,1,…,1]) are *set-level* predicates over the populated set V_S(d); they are NOT "V-position projections" and π's reshuffling is irrelevant to them. They are preserved for a different reason: RA-dom fixes dom(Σ'.M(d)), hence fixes V_S(Σ'.M(d)) = V_S(Σ.M(d)) (subspace is a function of v alone), so any set-level predicate carries over verbatim. The conclusion is correct, but "follows from RA-dom together with state-independent projections" is the "X follows from Y+Z" pattern, not a proof.
**Required**: Split the discharge: (a) S8a holds per-position on the unchanged domain; (b) D-CTG★, D-MIN★, S8-depth are predicates of V_S(d), preserved because RA-dom forces V_S(Σ'.M(d)) = V_S(Σ.M(d)) — π is irrelevant to them.

### Issue 2: Duplicate downstream deferral and redundant restatement of the RA-adm discharge
**ASN-0091, RA-adm table row and the paragraph following the table**: the table row states "discharge by RA-frame in 'State-Component-Only Invariants'", and a later sentence repeats "The binary transition invariants, which fall outside the per-state list, are discharged in 'State-Component-Only Invariants' below." Separately, the RA-adm table row's reachability description ("any per-state foundation invariant holds at every reachable state … ExtendedReachableStateInvariants is the explicit form") is re-stated nearly verbatim in the multi-sentence paragraph immediately after the table ("RA-adm requires that every per-state foundation invariant … ExtendedReachableStateInvariants is the explicit form of this implication, giving …").
**Problem**: Two pointers to the same downstream section, and the reachability⟹invariants discharge is said twice (table cell + following paragraph) with the same content. The reader must reconcile two copies to confirm they say the same thing.
**Required**: State the reachability discharge once (either the table cell or the paragraph, not both) and defer the binary invariants to the named section a single time.

### Issue 3: Collapse case explained twice
**ASN-0091, "Net-effect split" paragraph and "reachability discharge" paragraph**: The net-effect split paragraph says "In the *collapse case* (`M'(d) = M(d)` with π ≠ id) the transition is the identity `Σ' = Σ`, realised by the empty composite (see the reachability discharge below)…". The later paragraph re-derives the same: "In the collapse case `M'(d) = M(d)`, the REARRANGE_K transition is the identity `Σ' = Σ`; clause (ii) excludes `M'(d) = M(d)`, so K.μ~ is unavailable and none is owed. The realiser is the *empty* sequence…".
**Problem**: The same fact (collapse ⇒ Σ'=Σ ⇒ empty composite) is stated in two places, the first forward-pointing to the second ("see the reachability discharge below"). This is the multiple-paragraphs-deferring-to-the-same-location and same-thing-twice pattern.
**Required**: Establish the collapse-case realiser once, at the point where reachability of Σ' is discharged; drop the forward pointer.

### Issue 4: Meta-prose justifying proof economy rather than advancing the argument
**ASN-0091, paragraph following the K.μ~ admissibility table**: "Establishing Σ' reachable thus discharges RA-adm wholesale — there is no separate shape-package layer and no per-state frame-inheritance enumeration, since reachability already delivers the whole per-state package." Also the clause (i) parenthetical: "constructive, and prior to any reachability appeal (this clause is itself a premise of K.μ~ validity)".
**Problem**: These sentences describe why the proof does *not* need a separate layer/enumeration and justify the ordering of the argument, rather than stating an object-level fact. They are the "explains why the axiom/structure is needed" pattern; a reader following the discharge must skip past them.
**Required**: Delete the "wholesale / no separate layer / no enumeration" sentence and the ordering parenthetical; the discharge stands on the reachability implication alone.

## OUT_OF_SCOPE

### Topic 1: Reconstitution of a same-source span split by a cut, and link-subspace rearrangement semantics
**Why out of scope**: These are correctly parked in Open Questions. The note explicitly declines to claim that two fragments *jointly reconstitute* the original source span (RE-trans prose) and asks what link-subspace rearrangement would preserve — both are new territory for a future ASN, not defects in this one.

VERDICT: REVISE
