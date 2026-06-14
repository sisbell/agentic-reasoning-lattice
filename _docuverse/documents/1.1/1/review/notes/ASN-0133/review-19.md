# Review of ASN-0133

I read this as a conditional-termination theorem for forward-chaining rule systems on the substrate, and reviewed it for hand-waves, missing cases, and overclaims. It is unusually rigorous; below I record the places I scrutinized hardest, because a CONVERGED verdict on a note this intricate should show its work.

## REVISE

None. The claims I checked all hold, including the ones most likely to hide a gap:

**Q0 (Recognizability) — the "single PL term for *every* registry" claim.** I enumerated every atom in ASN-0129's `V_atom` against the two sources of view-sensitivity. The view-parameterized constituents are exactly `members, targets_of, is_K, M_K` (PC3's four); the UV-rewritten collections add `succs, sources_to, chain, stale`. Everything else — `tip, target_of, age, targets_keyed, is_filtered, is_in_chain`, the V-TUP/V-PRIM/V-DOC reads, and the fixed-view slices `A_K`/`L_K` — is genuinely view-stable. Each of the eight rebuilds over fixed-view bases (the `chain` case correctly hinges on PL having no sequence-to-sequence filter, forcing `elems`/`is_in_chain`). The exhaustiveness argument is sound, so the "for every registry" claim is earned, not asserted.

**Q5a — both hypotheses load-bearing.** Verified the two counterexamples are real: SF-without-extinction (`cmt`-trigger fired by emitting a `res`) spins forever on a constant domain; extinction-without-SF loses permanence. Q-EXT genuinely consumes both. The open/closed distinction is also correct: in the closed case `bounded-domain-growth ⟺ H-RF` (unbounded `⋃_k[D_ρ]` needs unbounded deposits needs unbounded real fires), so the route collapses to a restatement — the trade "buys something exactly when there is an environment to bound" is precise.

**Q6 — the obstruction triad.** I traced (1)/(2)/(3) against the grow-only split. The key discrimination — (1) and (3) obstruct *reaching*, (2) obstructs only *holding* — is correct, and obstruction (3) (finitely many arguments cycled out of phase through domain membership, since SF forbids falsify-and-re-arm) is a genuine witness that weak H-FAIR + bounded growth does *not* reach quiescence, correctly isolating H-SFAIR as the closing hypothesis. The `H-SFAIR ⟹ H-FAIR` proof and its restriction to infinite σ (the finite-σ terminal-trigger-true case breaks it) are both right.

**Q3 + the idem=⊤ dedup subtlety.** The audit-slice spelling argument is airtight: firing certifies no `c ∈ L_K` covers `a`; a dedup hit would be an `A_K ⊆ L_K` tuple covering `a` by coverage-equality, contradicting the fire — so the emit is necessarily a miss and grows `L_K`, even born-nullified. The reachable-vs-schema-level reading of the "strong enough" quantifier, and the honest distinction between *static* and *effective*, are correctly drawn.

**Q-FLIP — completeness of the re-armer inventory.** I checked whether `is_doc`/K.σ is a missing falsifier. It is not: `dom(Σ.M)` grows monotonically, so `is_doc(d)` is ⊤-stable — it can drive at most one ⊥→⊤ for a fixed argument and cannot re-arm a fired one, so it is correctly excluded from the *repeated*-re-armer inventory (and the `¬def(target_of(s,K))` "several" example is a valid no-retraction counterexample to the folklore).

**Worked example.** Traced Σ₀→Σ₁→Σ₂ explicitly. `[D_{ρ_R}]_{Σ₂} = L_cmt = {c}` (emitting `res` doesn't touch `L_cmt`), `T_P(t,Σ₂)=⊥` (the `cmt` covers `t`), both conjuncts hold, `quiescent_R(Σ₂)=⊤`. The reliance on regime (i) (environment idle) for the producer's reached-and-held half is stated, not smuggled.

Boundary cases (empty registry, empty domain, zero real fires `N=none`, finite σ ending non-quiescent, single-rule registry) are all addressed. Foundations are used by reference without reinvention, and no non-foundation ASN is cited by number.

## OUT_OF_SCOPE

### Topic 1: Multi-step-fire H-ATOM discharge
The turn-serialization that would discharge H-ATOM for multi-tuple contracts is carried as a standing scheduler obligation and deferred. Correct deferral — the load-bearing marker fires are single-step (atomic for free via I4), so this costs nothing here.

### Topic 2: A scheduler / turn-fairness model
H-SFAIR's satisfiability against an arbitrary withdraw-before-every-fire environment fails; the note repairs only the satisfiability *claim* and defers the turn-fairness construction. This belongs in the scheduler note, not here.

### Topic 3: The SF certificate (`pd_extinct`)
SF membership is the load-bearing *uncertified* registration check (PD0 is syntax-directed, so it is decidable — the gap is a shipped class, not a procedure). Whether `pd_extinct` should ship is correctly the note's Open Question 1, future territory.

VERDICT: CONVERGED
