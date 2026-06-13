# Review of ASN-0130

I checked the proof obligations claim by claim, with particular attention to the operational surfaces (`register_pred`, `certify_pd_stable`, evaluation-by-reference), the wp derivations, the well-foundedness of `sig`, the substitution induction in PR3a, and the soundness of the ST⁺ lift. I also ran the boundary cases the substrate makes available (empty run, single-address run, self-reference, frontier-ghost reference, born-nullified deposit, de-registration of a referent, overlapping runs, mid-run reference, `k = 0`, non-Boolean/view-parameterized certification). The note withstands all of them, and every cross-reference is to a foundation ASN (0034/0036/0043/0086/0093/0126/0128/0129).

## REVISE

(none)

The proofs that usually fail here hold:

- **PR2 + PR-SIG well-foundedness is non-circular.** PR2 is stated over deposit *events* and never consults `sig`; `sig`'s induction then rides PR2's strict `e₁(r) < e₁(D)` order, and PR0(iii) at `a` consumes only `sig` of strictly-earlier referents, not `sig(a)`. Self-reference is correctly shown *unconstructible* (every tuple denoting a start is inactive at a miss, so (iv) has no witness), not merely cycle-checked-away.
- **PR3a's substitution induction is rigorous.** WT-α and WT-W carry the right freshness provisos; the "no step captures / no step interferes" argument correctly localizes every `yⱼ` occurrence inside `u` (binders are fresh ν's, `Eⱼ` free vars lie in `dom(Γ)`), and the PC2 plain-composition discharge is applied last-parameter-first with the weakening bookkeeping made explicit. The coherence point — that `expand(a)`'s sort equals the `C_D` derived from the *reference-bearing* body — is actually established, not assumed.
- **The wp's are genuine weakest preconditions.** POST-ref's two-disjunct partition (standing tuple satisfies it regardless of the call; else fresh active deposit needs `VALID ∧ d∈dom(M) ∧ C3`) is correct, and the note correctly keeps `C3` under PR-DISC while collapsing it only on *additionally* surface-disciplined derivations — it does not conflate the registration discipline with the retraction discipline.
- **ST⁺ soundness is carried, not waved.** The bound-constant reading reduces each instantiation to a closed PD0 term whose rule-firings are value-independent; the one real extension (aggregate threshold "ℕ literal" → "literal or bound parameter") is shown sound from the *fixity* of the threshold across a step, and "the aggregate rule is the lone exception" checks out against PD0's other side conditions, all of which already admit "bound value." The worked `quiescent_v1` refusal (active-slice test, not grow-only → not ST) and the `armed` certification against the *expanded* term (not the literal `a₂(t) ∧ …`) verify the design's central distinction concretely.
- **The capture example is correct.** `chkW` genuinely captures under naive substitution (host address `x` swallowed by `quiescent_v1`'s tuple-binder `x`, even tripping well-typing), while `gate`'s parameter-name coincidence is correctly identified as benign.

## OUT_OF_SCOPE

### Topic 1: Producibility of a contiguous definition run under concurrent allocation
**Why out of scope**: PR0(i) correctly *validates* that a presented `A_def` is a contiguous segment of one origin's K.α chain, and the worked example explicitly conditions step 1 on "no other K.α scoped to `d_b` interleaved." But ASN-0093 exposes only single-step K.α; nothing in the substrate is an atomic multi-segment allocation primitive guaranteeing a builder can emit an `n`-address run without a concurrent *same-document content* allocation splitting it. The operation's soundness does not depend on this (an interleaved run simply fails (i), it does not falsify any claim), so this is not an error in PR0 — but whether the platform should ship a contiguous-run allocation primitive (or a re-anchoring path) is new territory for a future ASN. The udanax-green parenthetical gestures at the implementation's linear cursor without lifting it to a substrate guarantee.

(Note: the lint's conflation of "uncertified predicate" with "legitimately non-predicate," dangling live references, cross-substrate portability, and certificate classes beyond ST are already correctly carried as the note's own open questions; the lint/versioning interaction — superseded-but-pinned old versions remaining in `M_pdef` — is subsumed by the note's "scope the lint to a protocol" remark.)

Anti-bloat pass: I scanned for the flagged accretion patterns (rationale sub-paragraphs, relocated findings, excluded-case imaginings, repeated downstream deferrals, duplicate paragraphs). PR5a defers permanence/wp to PR0/PR1 with the actual argument re-derived rather than restated; PR-SIG's mutual-reference motivation operates at the *content* level (where cycles are constructible) to justify registration-grounding, so it is not imagining a case the discipline excludes; the three `Purity/View/Parameters` labels carry definitional content of ST⁺, not "why-needed" prose. I found the density load-bearing rather than obstructive — no source-level meta-prose finding to flag.

VERDICT: CONVERGED
