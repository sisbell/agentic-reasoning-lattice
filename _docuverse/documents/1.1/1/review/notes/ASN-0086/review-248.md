# Review of ASN-0086

## REVISE

No REVISE items. Detail on what I checked and why each potential issue resolves:

**Correctness of the load-bearing proofs.**
- R0a (FlatLinkDomain) — both cases sound. Cross-home (Case 1) correctly derives `home(a') = home(a)` from `a ≼ a'` via `zeros(w) = 0`, contradicting `d ≠ d'`, yielding `¬(a ≼ a')` and a vacuous implication. Same-home (Case 2) uses L-ContiguousPrefix + (UL) uniform length + T3. Arity-blind, as needed downstream.
- R-Scope (SingleTupleScope) — the P1 branch invokes R0a-at-Σ, the self-emit branch invokes R0a-at-Σ' (since `a ∉ dom(Σ.L)`). Both correctly reduce `{t : a ≼ t} ∩ A_rel^{Σ'}` to `{a}`. Arity-independence holds because the antichain argument never consults `|Σ.L(a)|`.
- wp Case 2's restriction to *layer-reachable* states is genuinely load-bearing, not over-scoping: without the unit-depth discipline a pre-existing non-unit-depth retraction to-span could cover the fresh `a_emit`, breaking the wp. The disciplinedness discharge (induction over layer-reachable trajectories, with the triple-restriction blocking higher-arity `K~R` emissions from growing `L_R`) closes this.

**Boundary coverage.** Empty endsets (`F=G=∅`), empty initial store (Step 0 first-emission), self-emit (Step 4, both wp disjuncts fail), retraction-of-retractor (Step 3, R6b non-fixpoint), and higher-arity targets (excluded from every `L_K`, harmless under Nullify) are all handled. The worked sketch computes concrete tumblers (`a₁=1.0.1.0.1.0.2.1`, etc.) and verifies R0–R6c, Observe's hist/oper split, and L-ContiguousPrefix indices against them.

**Anti-bloat scan.** The forward-reference prose flagged by prior cycles appears already trimmed. The remaining forward-pointing sentences (e.g. R5's "Self-targeting is what makes the Nullify operation possible," the Three Operations lead-in) are *statements of what an operation does* — explicitly exempt from the meta-prose definition. The only residual document-ordering pointer ("by Lemma — SliceUniqueness, stated next") is negligible and not worth a cycle.

**Self-containment.** All cross-references are to foundation ASNs (0034/0036/0040/0043/0093); no reinvented notation (`coverage`, `home`, `origin`, `δ`, `shift`, `inc`, `subspace_I` all sourced from foundations).

## OUT_OF_SCOPE

### Topic 1: Higher-arity active subsets and binary projections
**Why out of scope**: The note correctly excludes `|Σ.L(a)| > 3` links from every `L_K` (they index no tuple) and defers the `L_K^{(n)} ⊆ A_rel × ℘(A)^n` treatment to Open Question 2. This is new territory, not a defect here.

### Topic 2: Cross-layer retraction-stability discipline
**Why out of scope**: What a non-K.σ/K.α/K.λ higher-layer operation must satisfy for R6a/R6c to survive (Open Question on cross-layer discipline) is future-ASN material; the note's substrate is exactly the three K-operations.

### Topic 3: L_K ↔ Σ.M visibility invariants and Observe ordering/consistency
**Why out of scope**: Concurrency model, Observe result ordering, and arrangement-visibility coupling are flagged as Open Questions and belong to a later layer.

VERDICT: CONVERGED
