# Review of ASN-0130

I checked the proof obligations in depth: the chain-segment identity in PR-ENC (`shift(x,1)=inc(x,0)` iterated over a resident run, grounded by `ChainMembershipForOrigin`), the stratified `sig`/`PR2(a)` induction (non-circular — PR2 never consumes `sig`), the born-nullified boundary in the PR0 wp, the substitution induction of PR3a (WT-α + WT-W + k-fold PC2, simultaneous-to-sequential reduction sound under fresh expansion names), and the ST⁺ soundness argument including the aggregate-threshold extension (correctly identified as PD0's *only* literal-restricted position). These are sound. The findings below are the prose/precision issues the anti-bloat classifier asks for; none touches the mathematics.

## REVISE

### Issue 1: The four-verdict distinction is stated three times in PR5a
**ASN-0130, PR5a**: check (0) reads "a third category distinct from both (ii)'s ill-posed (view-dependent) and (iii)'s unknown (Boolean but not provably ST)" — forward-referencing categories (ii) and (iii) before they are defined — and the closing sentence re-enumerates the whole set: "The four checks carry four distinct verdicts: (0) non-predicate, (i) not-actively-registered, (ii) ill-posed, (iii) unknown — only (iii) a claim about stability".
**Problem**: Each check already names its own verdict where it is defined. The forward reference in (0) and the closing re-enumeration both restate what the per-check prose establishes. The reader following the checks in order has the verdicts; the recap is noise.
**Required**: Drop the closing re-enumeration sentence and the cross-reference to (ii)/(iii) inside check (0); let each check carry its own verdict label once.

### Issue 2: "vacuously violated" is incorrect terminology (PR5)
**ASN-0130, PR5**: "On every such `t ∈ M_pdef`, `is_pd_stable(t)` is permanently false, and the universal lint is *vacuously* violated the moment one is registered".
**Problem**: A universal `(A t ∈ M_pdef :: is_pd_stable(t))` with a falsifying witness `t` is *substantively* false. "Vacuous" denotes the opposite condition (truth over an empty domain); placing it next to a universal quantifier in a logic-dense note invites exactly the wrong reading. The intended meaning is that the violation is benign/uninformative, not that it is vacuous.
**Required**: Reword to "spuriously violated" / "violated for a benign reason" — the violation is real but uninformative, not vacuous.

### Issue 3: PR5a's checks re-derive PR5's qualifications instead of citing them
**ASN-0130, PR5a (ii)**: "Failure is rejection *as ill-posed*, not as unstable (PR5's distinction): a view-dependent spelling has no absolute PD class to certify." **PR5a (iii)**: "parameters read as bound constants of their declared sorts, the verdict asserting ⊤-stability of every `Γ_D`-instantiation (PR5's *Parameters* qualification)."
**Problem**: The ill-posed-vs-unstable distinction is already made in PR5's *View* qualification, and the bound-constant parameter reading in PR5's *Parameters* qualification. PR5a (ii)/(iii) restate them and then parenthetically cite the very paragraph they are repeating ("(PR5's distinction)", "(PR5's *Parameters* qualification)"). The operation contract should state *what it checks* and defer the *meaning* to PR5, not re-explain it.
**Required**: In PR5a (ii)/(iii), state the check (view-independence scan; `expand(a) ∈ ST⁺` by the checker) and cite PR5 for the semantics, without re-drawing the distinctions.

### Issue 4: Navigational meta-prose around the PR0 wp
**ASN-0130, PR0**: "the equivalence is not unscoped, both directions drawing on the discipline at the two points flagged below"; "*first use of the discipline*"; "*second use of the discipline*"; "which is why the first disjunct stands clear of `VALID` rather than conjoined with it".
**Problem**: These are scaffolding about where the discipline is invoked and why the formula has its shape — they explain the *presentation* rather than advance the derivation. The discipline's role is already clear from the surrounding steps; the "stands clear of VALID rather than conjoined" clause justifies the formula's form, which the worked first-disjunct case already demonstrates.
**Required**: Remove the "first/second use of the discipline" labels and the self-forward-reference; let the two discipline invocations stand inline in the derivation. (Same applies to the mirrored wp prose in PR5a.)

## OUT_OF_SCOPE

### Topic 1: Compositional certification
PR5a certifies `expand(a)` — the full inlined expansion — directly, re-checking every referent's body each time. A definition referencing a previously certified one (e.g. `gate` over a certified `a₁`) could in principle leverage the referent's standing `pd_stable` certificate plus the host's inline part, since ST is compositional under the Boolean connectives. The note's direct approach is sound and complete; compositional certification is an optimization/future design.
**Why out of scope**: This is a new capability (cert-of-parts ⟹ cert-of-whole), not a defect in PR5/PR5a. Open Question 4 covers *new certificate classes* but not certificate *composition*; this is distinct future territory.

VERDICT: REVISE
