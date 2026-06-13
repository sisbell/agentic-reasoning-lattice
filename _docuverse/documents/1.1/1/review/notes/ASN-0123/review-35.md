# Review of ASN-0123

I read this as a specification of the fork operation and verified its proofs against the foundations, with particular attention to the operation cases (owned/cross-owner, empty source, iterated forks), the cross-transition-system soundness apparatus (PS, VN-B1, SA), and the severance theorem. The note also carries the anti-bloat classifier, so I separately audited its meta-prose for forward-reference accretion.

## What I verified (no defect found)

**The core proofs hold.**

- **SA (StoredAddressAntichain)** — the zero-counting argument is correct: if `a ≺ b` are both stored with form `[d,0,s,k]`, then `b` inherits `a`'s separator at position `#d₀+1`, which lands inside `b`'s document prefix `d'` (whose own positions `1..#d₀` already carry `d₀`'s two zeros), forcing `zeros(d') ≥ 3` against `zeros(d')=2`. The downstream use in G2 (carry-through is non-empty *exactly when* `a ∈ ran(M'(v))`, since `coverage` is the full subtree but only `a` is stored in it) is sound.
- **VN-B1** — the induction over K.δ arrivals is complete: Node(e) excluded by `zeros≠2`; `k=2` excluded by the penultimate-zero argument; `k=1` forces `c₁`; `k=0` forces the frontier `c_{m+1}` via TA5-SigValid + T4-validity of the operand. The deliberate refusal to cite ASN-0040 B2 (whose global-B1 precondition is not available) is justified — B2's stated hypothesis genuinely does not transfer.
- **V9 severance + O5(ii)-as-theorem** — verified the structural maximality discharge: the length-`(#pfx(π)+1)` prefix `w=[pfx(π),0]` has `zeros(w)=2`, so any coverer `π''` longer than `pfx(π)` satisfies `w ≼ pfx(π'')` and `zeros(pfx(π''))≥2` by Z-mono, contradicting O1a. The severance proof then closes both branches of the `pfx(π_o)`/`pfx(π)` comparison correctly. This is the one real soundness point in the cross-owner case and it is now derived from ASN-0047's `A_doc=S(pfx(π),2)` structure rather than asserted.
- **V-WF** — both ValidComposite★ clauses discharged for both branches and the `n=0` degenerate; K.δ operand/freshness/parent, K.μ⁺ subspace+contiguity, K.ρ grounding, J0 vacuity, J1★/J1'★ via the `R'` clause. Invariant preservation is correctly delegated wholesale to ExtendedReachableStateInvariants rather than hand-waved per-invariant.
- **V9w** — the source-side row `(a,d_src)∈R` is correctly grounded on P4★ *as a composite-boundary property* licensed by P-bdy, with the boundary hypothesis explicitly flagged as load-bearing. V13's two-sided pinning (J1★ below, J1'★ above) is correct, including `|R'∖R|=|A|≤n` (provenance counts shared addresses, not positions — confirmed against the worked instance).
- **V8, V10, V12, V13** — coverer-set equality (V8), LP12-at-`d=v` with `ran(M'(v))=A` and `L'=L` (V10), and the identity/content non-injectivity (V12) all check.

**Completeness.** Boundary and operation cases are covered: empty source (`n=0`, the composite collapses to the lone K.δ), links-only source (also `n=0`, links not transcribed by V2b/CL-OWN/K.μ⁺_L), first vs. subsequent fork (nextv), node-tier owner forking in place (V8 is tier-agnostic), iterated forks (V6), shared/transcluded content (V9w notes `origin(a)≠d_src` admitted). I found no missing edge case.

**Depth.** Consequences are derived, not just stated (V6 unbounded-depth via the renumber-or-refuse dilemma; V7 navigation asymmetry; V9 severance; V12 boundary). Three worked instances exercise distinct claim clusters, and the cross-owner instance correctly isolates severance-with-carry-through. V10's biconditional supplies the exact (weakest) condition for version-side discoverability.

**Self-containment.** All ASN references are to foundations; no non-foundation ASN is cited in the body, and no foundation notation is reinvented (trunc/Z-mono/SA/nextv/VN-B1 are genuine local lemmas, not restatements).

## REVISE

None. I specifically audited the forward-reference meta-prose flagged by the classifier — the nextv/B2 non-citation digression, the V-WF→V9 cross-citation for `Document(v)` ("the one stream-form consequence this composite consumes"), the PS hybrid-reading framing, the precondition node-tier-exclusion rationale, and the J4/atomicity remarks. Each carries a load-bearing function (cross-transition-system non-transfer justification, non-circularity scoping, cross-foundation soundness setup, scope-boundary rationale, or named-source operand disambiguation), and the densest "defensive" passages (VN-B1-vs-B1, V0-vs-B8, PS's O4-for-E bridge, the V-WF/V9 O5(ii) discharge, SA's antichain) are exactly the ones a prior audit already deemed load-bearing. I could not isolate a passage that is both skippable *and* non-load-bearing without removing content the argument relies on.

## OUT_OF_SCOPE

The eight Open Questions (concurrent-fork serialization, derivation-direction recovery across ownership, link-subspace carry-through, location-fixed windowing vs. arrangement isolation, withdrawal/supersession, provenance-vs-derivation after contraction, correspondence under divergence) are correctly held as future territory rather than smuggled in as claims. The Scope paragraph's exclusions (document creation, version comparison, content/link operations, delivery, replication) are respected — no claim is defined for an out-of-scope operation.

VERDICT: CONVERGED
