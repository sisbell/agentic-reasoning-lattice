# Review of ASN-0053

## REVISE

(none)

I checked the following and found no defects:

- **Foundation usage.** All external references are to ASN-0034 (D0–D2, TA-LC, TA-assoc, TumblerSub, T12, TA-strict, etc.), which is a verified foundation — permitted. No non-foundation ASN numbers appear, and ⟦σ⟧ is a notation for the foundation `Span`/T12 set, not a reinvention.
- **Precondition discharge is explicit, not hand-waved.** WR discharges all of D2's preconditions; S5 discharges all four of TA-assoc's and all five of TA-LC's individually; S4/S8/S11/S11c invoke WF only after establishing `#s = #r` from level-uniformity + S6 each time. No "by similar reasoning."
- **Boundaries covered.** SC exhaustiveness enumerates all four-point orderings under the start<reach constraint; S1 covers empty/adjacent/separated/containment/equal; S11d tabulates all five SC cases including both containment directions (the `⟦α⟧ ⊂ ⟦β⟧` row derives emptiness rather than asserting it); S9 handles unequal-length sequences via the 1b/3b "shorter sequence" cases and the equal-start/equal-reach degeneracy via the TA-LC preamble.
- **Depth.** S7 derives the non-obvious consequence that every span is infinite (via T0(b) zero-extensions, with the `e < reach` step justified at the divergence position) and uses it to prove exact finite representation is impossible — a real derived result, not a restated postcondition. S3b/S4a establish the split↔merge bijection. S11's tightness argument uses S0 convexity to prove two is the minimum. Each property carries a concrete worked instance whose arithmetic I verified (the S8 example correctly exercises both merge and emit branches; the WR counterexample `[1,5] ⊖ [1,3,5] = [0,2,0]` correctly shows unequal-length failure).
- **Anti-bloat pass.** I looked specifically for forward-reference accretion, axiom-rationale prose, duplicated paragraphs, and use-site inventories. The post-proof prose after S4 ("each element appears in exactly one part…") and S4a ("level-uniformity is what makes recovery exact") restates proof content, but both fall under the protected category — statements of what an operation does and genuine derived insight — and neither forced me to skip past meta-prose to follow a claim. No "see X below" deferral chains, no document-ordering justifications, no consumer enumerations.

## OUT_OF_SCOPE

### Topic 1: Cross-level intersection, merge, and split
The whole algebra is restricted to level-uniform, level-compatible spans, and the cross-level cases (different-length endpoints, finer-level split points) are correctly deferred to the Open Questions rather than silently assumed away. The `level_compat` motivation and the WR unequal-length counterexample make the restriction honest. This is future territory, not a defect here.

### Topic 2: Span-set difference bound
S11d bounds single-span difference at 2; the tight bound on `normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)` for span-sets is explicitly raised as an Open Question. Appropriately deferred.

The ASN defines state (spans, span-sets, normalized form), operations (intersect, merge, split, difference, normalize), and invariants (convexity, intersection closure, normalization uniqueness, order-independence) at the right level of abstraction — no implementation drift, so no META.

VERDICT: CONVERGED
