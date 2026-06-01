# Review of ASN-0086

## REVISE

### Issue 1: State space underspecified — contradicts P2c non-vacuity and the function-ness "full state space" claim

**ASN-0086, Emit_K definition / WP Case 1**: "Where Σ is the substrate's state space (every state reachable from `Σ_init`)" vs. "Every `→*`-reachable state is substrate-conforming" (substrate-conforming state def) vs. "P2c is therefore a genuine, dischargeable conjunct, not a vacuous standing invariant ... Dropping P2c admits a non-conforming pre-state" (WP Case 1).

**Problem**: These three claims cannot all hold under the only reachability the ASN formally defines. The "Definition — Reachability" introduces only `→*` (closure of `→ ≡ K.σ ∪ K.α ∪ K.λ`), and the substrate-conforming-state definition asserts *every* `→*`-reachable state is conforming. So if "every state reachable from `Σ_init`" reads as `→*`-reachable — the only defined notion — then the state space is entirely conforming, P2c is a vacuous standing invariant, and WP Case 1's necessity argument ("dropping P2c admits a non-conforming pre-state") is false. Conversely, the function-ness Lemma explicitly insists it "holds over the full state space rather than only at substrate-conforming states," which is only meaningful if the domain contains non-conforming states — i.e., if the operation/wp domain is `↝`-reachable (categorical), not `→*`-reachable. The ASN never states this, and never defines `↝`-reachability.

This matters concretely: a non-conforming nested link pair is genuinely achievable via `↝`. A non-conforming layer may emit `a'' = inc(a, 1)` at the same home as `a` (`k=1` appends `[1]`, preserving `zeros = 3` per L1 and giving `#E(a'') = #E(a)+1 ≥ 2` per L1b), yielding `a ≼ a''` with both L0/L1/L1a/L1b/L1c-conforming. This is exactly the witness WP Case 1's P2c-necessity needs — but it exists only because the domain is `↝`-reachable, never made explicit.

**Required**: State that the operation and wp domain ranges over `↝`-reachable states (which may be non-conforming), define that reachability, and rewrite Emit_K's "every state reachable from `Σ_init`" to disambiguate `→` from `↝`. Then P2c is genuinely dischargeable and the function-ness "full state space" remark has content; absent this, the `→*`-reading makes P2c vacuous and contradicts both.

### Issue 2: Dangling cross-reference to a non-existent paragraph title

**ASN-0086, WP Case 1**: "is exactly the result proved absolute under R0a in the Definition of Nullify (paragraph *Single-tuple scope, absolute under R0a*)."

**Problem**: The paragraph in the Nullify definition is titled "*Single-tuple scope under R0a*", not "Single-tuple scope, absolute under R0a." The cited name does not exist verbatim. WP Case 1 then explicitly declines to repeat the argument ("We cite that derivation here rather than repeat the antichain argument"), so the load-bearing sufficiency step of a wp computation depends entirely on a citation that misnames its target — a precise reader must hunt for it.

**Required**: Fix the citation to match the actual paragraph title (or rename the paragraph), so the wp's sufficiency derivation resolves to a real location.

### Issue 3: Provenance meta-prose around a consumed-foundation lemma

**ASN-0086, R0a-Cor2 proof and Properties table**: "ChainElementT4Validity itself routes through T10a.4 (T4PreservationUnderDiscipline, ASN-0034) as its underlying ASN-0034 hook" / table: "ChainElementT4Validity (ASN-0093) — routing through T10a.4 (ASN-0034) as its underlying hook."

**Problem**: ChainElementT4Validity is an ASN-0093 lemma (a consumed foundation here). Explaining its *internal provenance* — that it itself routes through T10a.4 — advances nothing in this ASN's argument; the proof needs only "every chain element is T4-valid (ChainElementT4Validity)." This is the "new prose explaining why a cited result is grounded rather than what it gives" pattern the anti-bloat classifier targets, and it recurs in both the proof and the summary table.

**Required**: Cite ChainElementT4Validity directly and delete the "routes through T10a.4 as its underlying hook" provenance clause in both locations.

### Issue 4: Duplicated "R0 is uniform over L3-conforming triples" assertion

**ASN-0086, R5 Step 3 and Corollary R5.1**: Step 3 — "R0's emission argument is uniform over *any* L3-conforming triple regardless of `coverage(F)`, `coverage(G)`, or `coverage(K)`"; R5.1 — "R0's invariant-preservation is uniform over L3-conforming triples, inspecting neither slot nor coverage."

**Problem**: Two adjacent passages in the same section state the same fact in different words. R5.1 is a corollary of Steps 2–3; its parenthetical re-derives the uniformity Step 3 already established. This is the "two paragraphs say the same thing in different words" pattern.

**Required**: State the uniformity once (in Step 3) and have R5.1 cite it rather than restate it.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs. Observe, ordering of Observe results, and `nullified` cardinality bounds
**Why out of scope**: These are correctly deferred to the Open Questions. They concern a concurrency/consistency model the present note does not establish, not errors in the single-authority, sequential-transition substrate it actually specifies (SequentialTransitionAxiom, ASN-0093).

### Topic 2: Multi-arity typed relations (`|Σ.L(a)| > 3`)
**Why out of scope**: The note explicitly restricts to standard-triple links and flags higher-arity handling as future work. Nullifying a higher-arity address is shown to be well-formed but outside any `A_K`; defining `L_K^{(n)}` projections is new territory.

VERDICT: REVISE
