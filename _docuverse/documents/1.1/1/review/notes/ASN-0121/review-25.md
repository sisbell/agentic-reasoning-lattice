# Review of ASN-0121

I worked through every introduced claim (FL-DEF through FL-REACH), checked the satisfaction rule against Nelson's "AND of the ORs," verified the seven worked traces arithmetically, and scrutinized the three-case weakest-precondition analysis for exhaustiveness and the ghost-coverage / self-retraction subtleties.

## Findings

The ASN derives rather than stipulates `findlinks` (soundness and completeness meeting with no slack forces FL-DEF), and the load-bearing guarantees are each given real derivations, not checkmarks:

- **Boundary cases are covered**, not hand-waved: all-wildcard (unit) vs. constrained-empty (zero) are kept distinct (FL-EMP), with the link-side empty-endset symmetry handled (Trace 5); empty store and orphan/resurrection cases route through ASN-0098 correctly; residence is exercised concretely at document and node granularity (Trace 6), not left at `H = ∗`.
- **The wp analysis is non-trivial and exhaustive.** The fresh-link space is partitioned by retraction-relation membership `L_R^{Σ'}` (arity-3 ∧ slot-3 coverage *equality* `coverage(e₃) = coverage(R)`), not coverage-match alone — the arity-3 conjunct is correctly load-bearing (a higher-arity retraction-typed link routes to case (a) with `L_R` unchanged). The ghost-pre-coverage conjunct in case (a) and the self-retraction conjunct in case (c) are both genuinely live and witnessed in Trace 7. The ⊆ direction of the case (b) `nullified` increment is correctly supplied by the singleton `L_R` extension where R6b gives only ⊇.
- **K.λ is correctly isolated** as the unique result-changing transition, grounded in `findlinks` being a function of `Σ.L` alone (and `nullified ⊆ Σ.L`), with the monotonicity of `nullified` argued structurally over the full ASN-0047 vocabulary rather than by a fragile per-operation enumeration.
- **FL-REACH(d)** correctly avoids the overclaim that `findlinks` is a superset of the *request-independent* discoverable union, restricting to the satisfying slice and exhibiting strictness via satisfying orphans.

I checked the `athome` totality argument (the wide element-rooted span `p=[1,0,1,0,1,0,1,1]`, `ℓ=[0,0,0,0,1,1,1,1]` does yield `p⊕ℓ=[1,0,1,0,2,1,1,1]` containing document tumbler `[1,0,1,0,2]`), the FL-DIR witness (disjoint equal-length non-nesting subtrees), and Trace 6's home-projection (`home([1,0,1,0,2,0,2,1]) = [1,0,1,0,2]`). All check out.

Cross-references are confined to foundation ASNs (0034, 0036, 0043, 0047, 0053, 0086, 0093, 0098). No notation is reinvented — `coverage`, `home`, `nullified`, `L_R`, `discoverable_from`, span machinery are all inherited. Implementation evidence (Gregory, consultations) is used as grounding/divergence-flagging, not as the specification; the abstract claims remain implementation-independent. No drift.

The three FL-WP cases frame each step as "Let `Σ → Σ'` be a K.λ step that allocates …", presupposing enabledness via the framing rather than carrying a `home(ℓ) ∈ dom(Σ.M)` conjunct as ASN-0086 wp Case 2 does. I considered flagging this, but the conditional framing makes each wp internally consistent (a weakest precondition *relative to the parameterized operation firing*), and the ASN cites ASN-0086 only for the ghost-coverage conjunct, not for replicating its enabledness form. No defect.

## REVISE

None.

## OUT_OF_SCOPE

The five Open Questions (version/time-qualified inquiry, I-address vs. V-spec correspondence, single-subtree-test conditions on `H`, exact subtype-by-containment conditions on the type endset, and cross-federation completeness) are correctly identified by the author as future territory rather than gaps in this ASN.

VERDICT: CONVERGED
