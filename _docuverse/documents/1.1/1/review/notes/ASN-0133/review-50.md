# Review of ASN-0133

This is a careful, honest note: the termination results are stated as conditional theorems with hypotheses named (H-FIN, H-ATOM, H-FAIR, H-SFAIR, H-RF, regime (i), grow-only, bounded growth, all-SF, extinction), the obstruction analysis in Q6's non-grow-only case is genuinely thorough, and the worked trace verifies the nested quantifier end to end. I checked Q0's view-merge, Q5/Q5a's bounds, Q-EXT, and the three Q6 regimes; the mathematics holds. The findings below are a factual error in the worked example's justification, a consistency gap in the satisfiability remark, and the meta-prose the anti-bloat classifier targets.

## REVISE

### Issue 1: The worked registry's "type isolation" claim is false

**ASN-0133, Worked composition (post-Bound paragraph)**: "Q4's warning that locally disciplined rules can re-arm each other is here *vacuous by type isolation* — no fire of either rule enlarges the other's domain" and earlier "the two rules' domains and emissions are *type-isolated*."

**Problem**: ρ_P's domain is `{t ∈ M_tgt : is_attn(t)}` and ρ_R's domain is `L_cmt`; ρ_P **fires by emitting one `cmt`**, which enters `L_cmt`. So a ρ_P fire *does* enlarge ρ_R's domain — and ρ_P's emission type (`cmt`) *is* ρ_R's domain type (`L_cmt`). "No fire of either rule enlarges the other's domain" and "domains and emissions are type-isolated" are both false: the coupling ρ_P → ρ_R is real (the note even relies on it — "comments entering `L_cmt` through ρ_P, one per flagged target"). The conclusion (no internal divergence; Q4's *mutual* re-arm warning vacuous) is correct, but for a different reason: only the **return path** ρ_R → ρ_P is isolated (`res` lands in `L_res`, which ρ_P's domain `M_tgt`/`is_attn` never reads), so the ρ_P → ρ_R feed is *one-way and acyclic* — it cannot close a cycle, and is bounded by ρ_P's environment-driven fires.

**Required**: Replace the symmetric "no fire enlarges the other's domain / type-isolated" justification with the asymmetric one: ρ_P → ρ_R is a bounded one-way feed, ρ_R → ρ_P is type-isolated, so the coupling is acyclic and Q4's *mutual*-re-arm warning has no instance.

### Issue 2: "H-FAIR satisfiable against an arbitrary environment" contradicts "no turn-fairness is stated"

**ASN-0133, H-SFAIR, *Satisfiability is environment-conditional***: "H-FAIR is satisfiable against an arbitrary environment because its removal and falsification escapes absorb interference a fire-only scheduler cannot forestall; the regime form of H-SFAIR is not." Combined with: "The interleaving model admits consecutive environment steps (*no turn-fairness is stated*)."

**Problem**: If consecutive environment steps are admitted with no turn-fairness, an environment may take *unboundedly many* steps in a row, never depositing a covering tuple. An SF-marker argument `¬(∃ c ∈ L_K :: x ∈ coverage_G(c))` then stays in-domain *and* trigger-true while the scheduler is starved — and **none** of H-FAIR's three discharges fires (no real-fire: scheduler never acts; no removal: domain unchanged; no falsification: no covering deposit). That σ violates H-FAIR and no scheduler can repair it, so H-FAIR is *not* satisfiable against this environment. The note's asymmetry is real but mis-stated: H-FAIR's satisfiability presumes **weak turn-fairness** (the scheduler receives infinitely many turns), exactly what the add-remove counterexample for H-SFAIR silently grants ("around each scheduler turn"); H-SFAIR additionally needs the **stronger joint** turn-fairness (the environment leaving recurrently-presented arguments in-domain *at* those turns). The single phrase "no turn-fairness is stated" conflates the two levels and makes the H-FAIR claim overreach.

**Required**: Distinguish the two levels. State that H-FAIR's satisfiability rests on scheduler liveness (weak turn-fairness), scope "arbitrary environment" to environments that do not starve the scheduler, and reserve "no turn-fairness is stated" for the *joint* turn-fairness only H-SFAIR needs.

### Issue 3: Regime (i) and its content-deposit subsumption are stated three times

**ASN-0133, three locations**:
- H-SFAIR: "Endless `dom(Σ.C)` deposits… leave the footprint constant and fall inside regime (i), not outside it."
- Q6 bullet: "(the *footprint-relevant state* — the `dom(Σ.M)`/`Σ.L` portions every `[D_ρ]` and `T_ρ` reads, FP — is eventually constant; … e.g. endless `dom(Σ.C)` content, both qualify)"
- Q6 proof: "(FP — the `dom(Σ.M)`/`Σ.L` portions every `[D_ρ]` and `T_ρ` reads; this subsumes … one whose every step lands outside all footprints, e.g. endless `dom(Σ.C)` deposits)"

**Problem**: The gloss "the `dom(Σ.M)`/`Σ.L` portions every `[D_ρ]` and `T_ρ` reads" is verbatim in the Q6 bullet and the Q6 proof, and the "endless `dom(Σ.C)` deposits → footprint constant → regime (i)" point appears in all three. The proof re-defines regime (i) that the bullet already defined. This is the anti-bloat "multiple paragraphs say the same thing / defer to the same downstream location" pattern.

**Required**: Define regime (i) and its content-deposit subsumption once (the bullet); the proof should reference that definition, not re-gloss it. Drop the H-SFAIR repetition or replace it with a bare back-reference.

### Issue 4: Residual defensive meta-prose

**ASN-0133, Q3 / Q1 / OQ5**:
- Q3 closes with "Sufficient, not necessary: … a rule may be disciplined for reasons no contract of this shape expresses. Failure-to-verify is not violation." — "Failure-to-verify is not violation" is a defensive coda that adds nothing the preceding sentence ("a sound characterization only") didn't establish, and "Sufficient, not necessary" duplicates OQ5 ("Q3 is sufficiency only: must every extinction-disciplined rule admit a strong-enough PL contract?").
- Q1: "holding for undisciplined registries, unfair schedulers, and divergent systems alike" — an exhaustiveness flourish on a claim ("unconditional relative to the dynamics hypotheses") already made.

**Problem**: These are the "defensive justifications / exhaustiveness claims" the classifier flags — prose that restates a point rather than advancing it, with one outright duplication across Q3 and OQ5.

**Required**: Cut the defensive codas; let OQ5 carry the sufficiency-not-necessity point once.

## OUT_OF_SCOPE

### Topic 1: The scheduler / turn-serialization model
**Why out of scope**: The construction of a scheduler discipline, its liveness proof, and the serialization that discharges H-ATOM are correctly deferred (the "What this note doesn't cover" section names them). Issue 2 is in-scope only because it concerns the precision of a claim *made in this note*; the underlying turn/serialization model itself belongs to the implementation layer, as the note states.

### Topic 2: pdef-trigger registries de-registered mid-lineage
**Why out of scope**: The note correctly notes recognizability survives de-registration via ever-registration keying (PR3). A full account of de-registration semantics (nullify vs. supersede of a `pdef` tuple) is ASN-0130 territory, not a gap here.

VERDICT: REVISE
