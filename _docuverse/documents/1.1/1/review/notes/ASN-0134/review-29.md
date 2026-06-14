# Review of ASN-0134

I checked every operation→step claim, every conflict-commutation argument, the invariant partition, the quiescence soundness chain, and the contract's load-bearing analysis against the foundations. The note is unusually complete: cases are enumerated rather than waved (W5's P-tgt trichotomy, H1's nesting/cross-subspace split, A5's m∈{0,1,≥2} taxonomy), derivations are explicit (A6's B2/RP-a/RP-b transfer chain, the banking argument for V2), concrete examples are present (§7's four address vignettes, §8's nullify trace), and a non-trivial wp is computed (clause 2's per-home exclusion). I verified the three most error-prone novel arguments specifically:

- **Clause 8 necessity, both axes.** Cross-home: the both-miss interleaving deposits at distinct origins (H1), both born active. Same-home: clause 2 serializes only `[frontier-read+deposit]`, never the preceding global dedup-read, so two stale misses land at consecutive slots `φ, φ+1` — clause 2 *enables* the duplicate by averting the H2 collision that would otherwise reject one. The claim "permits regardless of home" is precise under the note's consistent reading of "per-home order" as the allocation serialization of H0/clause 2.
- **The I1a literal/operative gap.** ASN-0128 I1a's proof uses "the deposit's *own* pre-state has no active I0-member," which in the sequential model follows from "fired on a miss" only because dedup-read state = step pre-state. Under concurrency these diverge, the literal "K-surface-emitted" clause is satisfied while the operative one is not, and the note reads I1a operatively throughout — consistent, and not a claim the foundation is broken.
- **V2's strict-implication chain.** Both converse-failure witnesses hold: the trace-minus-nullify (`[no Q-affecting] ∧ ¬[one index] ∧ sound`) and the short-circuit combiner `g(v₁,v₂)=(v₁≠∅)∨(v₂=∅)` (`[sound] ∧ Q-affecting-step-present`).

The `age`/`stale` access-count discrimination, A6's canonical/transition split with the W3 reconciliation, the M1-label disambiguation, and the K.σ scoping (freshness as upstream hypothesis, H3 lifting confluence) are all coherent. Foundation usage is proper (T-series primitives and ASN-0086/0093/0126/0128 lemmas cited, not reinvented). MIC is an abstract contract, not mechanics — the concrete primitives are explicitly deferred to Open Questions — so the note has not drifted.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Whether the toggle family's instance (ii) admits any taming discipline
The note documents that a lone `idem=⊤` `Emit` racing a `Nullify` of its *active incumbent* is order-unstable (`A;B` → empty class; `B;A` → fresh active `A'`) and that this is "reduced by neither discipline" — emit-before-retract is vacuous because the incumbent was emitted long before the retraction, and clause 8 governs only racing coverage-equal *emits*. The Open Questions cover the target-residence race (OQ9) but pose no analogous question for instance (ii). Whether a *new* coordination discipline (an emit/nullify ordering on the incumbent, distinct from emit-before-retract) could make this verdict order-stable, or whether it is irreducible because the verdict reads the global `A_K`, is a legitimate future topic.

**Why out of scope**: This is honestly documented as residual non-confluence, not an error or overclaim — M1(b)'s no-duplicate guarantee is correctly scoped to exclude it (instance (ii) yields 0 or 1 active tuple, never 2). Resolving or proving-irreducible the lone-emit-vs-incumbent-nullify dependence is new territory for a later note, not a revision to this one.

VERDICT: CONVERGED
