# Review of ASN-0130

This is a carefully built note. The hard machinery — PR-SIG's registration-order stratification of typing, PR2's event-wise acyclicity, PR3a's substitution induction — is rigorous, and the foundation usage (S0/S1, L12, the `shift(x,1)=inc(x,0)` identity, RangeSterilization/DR for the born-nullified boundary) is consistent. My findings are about concrete demonstration and accreted prose, not soundness.

## REVISE

### Issue 1: The note's most novel mechanism — expansion with capture-avoiding renaming — is never concretely demonstrated, and the one example cited for it involves no capture

**ASN-0130, PR3 and Worked composition (steps 2, 4)**: "a referent's parameter may share its name with a host variable (the worked composition's `gate` does exactly this), and the rename is what keeps the two from ever meeting in one scope."

**Problem**: In the worked example, `quiescent_v1`'s body is `¬(E x ∈ A_W :: t ∈ coverage_F(x))` — it binds only `x`, with `t` a free parameter. Inlining it into `gate` substitutes `gate`'s `t` (the argument) for `quiescent_v1`'s parameter `t`, yielding `¬(E x ∈ A_W :: t ∈ coverage_F(x))` (now `gate`'s `t`). The binder `x` does not capture `t`, so **the result is correct with or without renaming** — the renaming here only α-renames a harmless binder. Capture in this framework arises only when a referent's *binder* coincides with a free variable of a passed *argument* (e.g. referent body `(E z ∈ A_K :: …)` with an argument mentioning `z`); the worked example contains no such case. So `gate` does not exercise the discipline it is cited to motivate — the "two `t`s" are a free parameter being replaced by the host argument, not two live variables that could collide.

Compounding this: `expand(·)` is never written out for any reference-bearing definition. The only definitions actually expanded/certified (a₁, a₂) have reference-free bodies, so `expand(a) = body` and PR5's load-bearing distinction — "the certified object is the definition's *expansion* … not the artifact's literal reference-bearing spelling" — is vacuous in every worked instance. The resolve→expand→evaluate pipeline and the substitution machinery of PR3a are proven but never shown producing a concrete term.

**Required**: Write `expand(gate)` out explicitly (e.g. `¬(E ν ∈ A_W :: t ∈ coverage_F(ν)) ∧ count({x ∈ A_H : t ∈ coverage_F(x)}) ≤ 3`). Then add one instance where naive substitution *would* capture — a referent whose binder name coincides with a free variable of the host's argument — so the renaming's necessity is actually demonstrated; or soften the claim that `gate` demonstrates it. Ideally, certify a reference-bearing definition so PR5 is exercised on a non-trivial expansion.

### Issue 2: PR5 re-explains PR-VIEW, carries naming-housekeeping meta-prose, and pre-summarizes a proof it defers downstream

**ASN-0130, PR5**: "its respelling through the fixed-view slices is always available (PC3's cross-view readings), and that is where an audit pin belongs anyway — in the spelling, which is the certified object."

**Problem**: This restates PR-VIEW's already-made point ("An author who needs a read pinned to a slice *regardless of caller* pins it in the spelling … respell every parameterized read through them"), plus an editorial flourish ("that is where an audit pin belongs anyway"). Two further instances in the same claim: "a parametric lift of it, written **ST⁺** and named so uniformly throughout" — naming-consistency meta-prose that advances no argument; and the closing "Permanence for the certificate slice is stated and proved at PR5a: the certified expansion can never change, so a certificate never expires" — a forward-deferral that *also* pre-summarizes the conclusion PR5a then proves in full. These are exactly the forward-reference accretion patterns the note's `review-mode.anti-bloat` classifier targets.

**Required**: Replace the respelling re-explanation with a citation to PR-VIEW; drop "named so uniformly throughout"; drop the PR5→PR5a permanence pre-summary and let PR5a carry it.

## OUT_OF_SCOPE

### Topic 1: Result-sort-aware domain restriction for the universal lint
**Why out of scope**: PR5 correctly establishes that `(A t ∈ M_pdef :: is_pd_stable(t))` is spuriously violated by legitimately non-Boolean definitions and that PL cannot narrow `M_pdef` by result sort (the sort is content/`sig`-derived, outside PL's read surface). A future ASN could add a Boolean-predicate sub-class or a result-sort classifier so the universal coverage lint becomes expressible; this is new substrate territory, not a defect here. The note's per-definition atom `is_pd_stable(t)` is sound as stated.

### Topic 2: Supersession-branch adjudication policy
**Why out of scope**: PR4 leaves branch resolution (`tip` returning ⊥ on competing successors) to readers, "BH2's stance." A policy layer for detecting/resolving definition-lineage branches is a separate concern; PR4's reliance on shipped S2/BH2 is correct for this note.

VERDICT: REVISE
