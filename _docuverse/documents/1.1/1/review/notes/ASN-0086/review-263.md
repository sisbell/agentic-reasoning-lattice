# Review of ASN-0086

I checked the relational layer (R0–R6, R-Scope), the two wp cases, and the worked sketch against the ASN-0093/0043/0034 foundations. The mathematics is sound: R0a's antichain (both home-cases), R-Scope's self-emit branch, the wp equivalences, and the five-step worked cycle all hold up under scrutiny, and the foundation references are all to listed foundation ASNs. My findings are confined to prose that the `review-mode.anti-bloat` classifier flags as accreted, plus one genuine redundancy.

## REVISE

### Issue 1: Defensive presentation-prose in the wp analysis
**ASN-0086, Weakest-Precondition Analysis (Case 2)**: "Delivering it explicitly lets the wp be stated over the ASN's declared `→*`-reachable working domain, with no recourse to a trajectory-bound 'layer-reachable' restriction." — and in the Disciplined-domain simplification: "The simplification is a property of the sub-domain, not a re-statement of the wp."

**Problem**: Neither sentence advances the wp. The first justifies *why* the third conjunct is delivered as a state predicate (a presentation rationale); the second pre-empts an objection about the simplification's status. These are exactly the "defensive justifications in structural slots" the anti-bloat pass targets — a reader following the derivation must skip past them. The wp formula and its two-direction derivation already stand on their own.

**Required**: Drop both sentences. State the third conjunct, note it is finitely checkable over `L_R^Σ`, and let the derivation carry the rest. If the disciplined-domain form is worth keeping, present it as a labeled corollary without the defensive coda.

### Issue 2: The "triple-restriction excludes higher-arity" fact is restated at three sites
**ASN-0086, Definition — TypedRelation / Definition — Nullified / discipline-discharge (Three Operations)**: TypedRelation establishes "the `|Σ.L(a)| = 3` conjunct restricts every `L_K`… higher-arity links… inhabit `A_rel` but index no tuple of any `L_K`." The Nullified note then re-explains "ranges over the triple-restricted `L_R^Σ` (the `|Σ.L(a)| = 3` conjunct of Definition — TypedRelation) — so only standard-triple links can retract." The discipline discharge re-derives it a third time: "A higher-arity K.λ emission… cannot grow `L_R` — `L_R^Σ` is triple-restricted by the `|Σ.L(a)| = 3` conjunct…".

**Problem**: The discipline-discharge use is load-bearing (it is a case of the induction). The Nullified-definition note, however, re-states the same consequence already fixed at TypedRelation in different words — the "two paragraphs say the same thing" pattern. It carries no new obligation; the `L_R` subscript already inherits the triple-restriction by construction.

**Required**: In the Nullified note, cite the triple-restriction by reference (it is inherent in `L_R^Σ`'s definition) rather than re-arguing that higher-arity links cannot retract; keep the single load-bearing derivation at the discipline-discharge step.

## OUT_OF_SCOPE

### Topic 1: Concurrency model for Emit/Observe (Open Questions 4, 5)
**Why out of scope**: Atomicity of `Emit_K` against concurrent `Observe_K`, and any ordering guarantee on `Observe` results, require a concurrency/consistency model the substrate does not yet carry. ASN-0086 correctly defers these; they belong to a future ASN that models interleaving, not to this single-writer transition layer.

### Topic 2: Cardinality discipline on `nullified(Σ)` (Open Question 6)
**Why out of scope**: Whether a structural ratio must bound `|nullified(Σ)|` relative to `|dom(Σ.L)|` is a new resource-discipline question, not a defect in the present invariants. `nullified` is well-defined and monotone here regardless of its size.

VERDICT: REVISE
