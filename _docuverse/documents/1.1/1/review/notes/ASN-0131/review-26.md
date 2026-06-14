# Review of ASN-0131

The technical content is sound. I verified the worked instance (the `e₃`/`θ` field-agreement disjointness, the width-2 straddling span coverage `{a₂,a₃}`, the touch tests against `I={a₂}`), the RE-UDIST factoring through the region-independent `Avail(Σ)`, the RE-CWP weakest precondition (including the `R=∅` collapse), and both directions of the RE-RET biconditional (forward via R6a + the hypothesis, backward via R0a/R-Scope). All hold. The findings below are localized prose issues, two of them the anti-bloat patterns the classifier targets.

## REVISE

### Issue 1: Retraction analysis elaborates a hypothesis-excluded sub-scenario
**ASN-0131, "Stability" → Under retraction**: "*Absent it, a Θ meeting the image surfaces b as the fresh pair (3, Θ) … and, contrary to what one might hope, that pair need not be distinct from one the retracted link itself bore: when ℓ is itself a retraction link, Σ.L(ℓ).e₃ = Θ, so ℓ bears (3, Θ) too and b re-witnesses the very pair its target bore.*"

**Problem**: RE-RET *adopts* the hypothesis `coverage(Θ) ∩ dom(Σ.C) = ∅` and routes its exception to Open Question 6. The re-witnessing sub-scenario lives entirely in the hypothesis-failure world (`Θ` meets the content image, `ℓ` is itself a retraction link) — exactly the territory the adopted hypothesis excludes and OQ6 owns. This is the "paragraph imagines a case the claim's precondition already excludes" pattern. The necessity of the hypothesis is genuinely worth one clause; the worked counterfactual ("`b` re-witnesses the very pair its target bore") is an excursion into OQ6's case analysis that does not advance RE-RET.

**Required**: Compress the load-bearing point to a single clause — *absent the hypothesis, `b`'s type-slot `Θ` could meet the content image and surface `(3,Θ)`, so the forward direction rests on it* — and drop the `ℓ`-is-a-retraction-link re-witnessing elaboration (let OQ6 carry it).

### Issue 2: Umbrella "root reason" inaccurate for K.δ document-registration
**ASN-0131, "Stability" → "Three further transition kinds…"**: "*Three further transition kinds leave the answer fixed for the same root reason — each touches none of the state RE reads (RE-LOC).*"

**Problem**: K.δ in the `Document(e)` case extends `Σ.M` (it adds the key `d_new` with `Σ'.M(d_new)=∅`), so it *does* touch state RE-LOC names RE a function of. The umbrella reason "touches none of the state RE reads" is therefore false for K.δ-doc; the per-transition sentence silently switches to the correct reason ("leaves … on every pre-existing arrangement, for document registration, LP8"). The grouping of K.δ with K.α and K.ρ under one inaccurate reason makes a reader briefly accept a false generalization.

**Required**: State the actual common reason — each leaves the queried fiber `Σ.M(d)` and `Σ.L` fixed (LP8 supplying the K.δ-doc case) — rather than "touches none of the state RE reads."

### Issue 3: Soundness/completeness section restates one definitional fact three ways
**ASN-0131, "Soundness and completeness"**: "*The result is exactly the touching set: neither more (soundness) nor less (completeness).*" … "*These two together are the whole of the operation's relation to the region: it surfaces the touching anchoring, all of it and only it.*"

**Problem**: RE-SND and RE-CMP are immediate reads of the RE-DEF biconditional, not theorems requiring argument — the section is exposition, and within it the "exactly the touching set" conclusion is stated three times in close succession ("neither more … nor less," "all of it and only it," "the whole of the operation's relation"). This is the "say the same thing in different words" pattern.

**Required**: Keep the two claims (they are legitimately introduced) but collapse the triple-restated conclusion to one statement, and drop the proof-like framing ("This is the half that makes the answer trustworthy…") for facts that are immediate from the definition.

## OUT_OF_SCOPE

The seven Open Questions correctly fence the future territory (whole-vs-touching spans, multiplicity preservation, rendered V-order, intersection-distributivity, non-co-resident stores, type-slot-vs-content matching, link-subspace regions). The note does not define claims for the excluded sibling operations (FINDLINKSFROMTOTHREE, READLINK, etc.) — it cites them only by name for contrast — so there are no in-body claims to flag out of scope. The existence/discovery taxonomy is cited (E-MONO/D-NONMONO/D-ZERO, ASN-0127), not rebuilt; RE-SEL applies it rather than re-deriving it, honoring the "cite, do not rebuild" boundary.

VERDICT: REVISE
