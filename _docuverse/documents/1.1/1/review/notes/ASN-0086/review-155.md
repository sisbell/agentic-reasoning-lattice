# Review of ASN-0086

I checked the proofs (R0, R0a, L‑ContiguousPrefix, R‑Scope, R7a), the wp analysis, and the worked sketch against the foundations. The mathematics is sound — the freshness discharges, the zero‑counting antichain argument (Case 1 of R0a), the contiguity induction, and the four‑step worked example all hold up under inspection. The findings below are about prose that does not land on a claim, and a wp case that produces a non‑result. Per the `review-mode.anti-bloat` classifier, I surface accretion patterns in addition.

## REVISE

### Issue 1: wp Case 1 produces no weakest precondition — extended analysis lands on "left open"

**ASN-0086, Weakest-Precondition Analysis, Case 1**: "the exact weakest precondition for Case 1's postcondition is left open."

**Problem**: Case 1 sits under a heading that promises weakest‑precondition analysis, but delivers only a *sufficient* precondition `P0 ∧ P1 ∧ PC`. It then spends four sub-paragraphs (*Non-weakestness*, the local pair `L(Σ)`, *Sufficiency of the local pair*, *Relation to PC*) establishing that PC is non‑weakest, that the local pair is strictly weaker, and that the local pair is *also* not weakest because of the self‑emission boundary `a = a_emit(Σ, d_retr)`. The chain of refinements terminates at "left open." The reasoning is correct and honest, but it is a screen of analysis whose conclusion is indeterminacy — a reader must work through the whole detour to learn there is no result. (Case 2 already satisfies the non‑trivial‑wp obligation in full, so Case 1 is not load‑bearing for the section.)

**Required**: Either compute the weakest precondition for Case 1 (including the off‑P1 self‑emission case the local‑pair discussion identifies), or compress the entire passage to a one‑line remark — "`P0 ∧ P1 ∧ PC` is sufficient but not weakest; PC's global antichain strictly over‑constrains a local postcondition" — and stop. The local‑pair construction and self‑emission boundary should not be paraded only to be discarded.

### Issue 2: the non-fixpoint / restoration-by-reemission point is restated across four locations

**ASN-0086, R6b Remark and R6c consequence**:
- R6b Remark: "retraction-of-retraction is not a fixpoint … restoration of `b`'s prior targets must therefore proceed by fresh emission at a distinct address, not by retraction-of-retraction."
- R6c (post-proof): "To 'restore' content, emit a fresh tuple with the desired value (R0). The new tuple receives a fresh address; the retracted tuple keeps its address (R2) and stays out of `A_K` (R6a)."

**Problem**: These two paragraphs, in different sections, state the same conceptual claim in different words. The same point is then made twice more in the worked sketch (Step 2: "we do *not* attempt to nullify the retraction (which by R6b would be ineffective)"; Step 3 close: "restoring `(F₁, G₁)` … requires fresh emission at a fresh address … not retraction-of-retraction"). The worked-example instances are legitimately illustrative, but R6b's Remark and R6c's consequence are redundant against each other.

**Required**: Keep one abstract statement of "restoration is fresh emission, never retraction-of-retraction" (R6c's consequence is the natural home, as it follows R6c's formal claim) and remove the duplicate from the R6b Remark, leaving R6b's Remark to state only the audit-slice/non-fixpoint mechanism it uniquely contributes.

### Issue 3: two conformance definitions defer to the same downstream Remark

**ASN-0086, Definition — state-local-conforming state** and **Definition — substrate-conforming state**: both forward-reference "Remark — NestedLinkWitness, below" ("The separation is witnessed by states that preserve every state-local invariant yet violate R0a's antichain (Remark — NestedLinkWitness, below)"; "The witness of Remark — NestedLinkWitness satisfies (b) yet …").

**Problem**: Two consecutive definitions both lean on a witness stated only afterward. This is the "multiple paragraphs defer to the same downstream location" accretion pattern. The witness is short and load-bearing for both.

**Required**: State the NestedLinkWitness construction before the two definitions, so each can cite it as an established fact rather than a forward promise.

## OUT_OF_SCOPE

### Topic 1: invariants coupling `L_K` to arrangements `Σ.M`, multi-arity typed relations, concurrency/atomicity of Emit vs Observe, cardinality bounds on `nullified(Σ)`
**Why out of scope**: These are correctly enumerated in the Open Questions and depend on machinery (visibility predicates, higher-arity `L_K^{(n)}`, a concurrency model) that this note does not introduce. They are future ASNs, not defects here.

### Topic 2: elevating the unit-depth retraction discipline to a substrate-level K-operation
**Why out of scope**: Whether the substrate should expose a value-shape constraint on retraction tuples is a genuine design question, correctly posed as open. The note's treatment of it as a layer convention (with the address-vs-shape gap honestly flagged) is internally consistent.

VERDICT: REVISE
