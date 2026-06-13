# Review of ASN-0108

I checked the windowing operation's enumeration order, cursor semantics, partition proof, the weakest-precondition analyses, and the termination chain (W9–W9d). Most of the mathematics is sound and unusually careful — the W2 offset-cursor wp nesting, the W4 variable-schedule partition, the W9a count formula (verified against all four boundary walks: m=4→3, m=5→3, m=0→1, N>m→1), and the W9b multiplicity-charge argument all hold. The W9c "does not guarantee" framing and the W9b/W9d sufficiency framings are correctly stated as guarantees, not as necessity. One claim, however, asserts a necessity it does not have.

## REVISE

### Issue 1: W5 overclaims clause 1 as *necessary* for coherence

**ASN-0108, W5 (OrderStability)**: "Resumption is *coherent* … *if and only if* the key satisfies **clause 1 (cut-point preservation)** at every cursor the reader actually holds" and "Clause 1 at the held cursors is the necessary *and* sufficient condition." (Restated in the claims table: "Coherent resumption … holds *iff* clause 1 … is maintained at every visited cursor.")

**Problem**: Clause 1 at every held cursor is **sufficient** for whole-pass coherence but **not necessary**. The "iff" fails in the necessity direction. The error is seeded by the justification's definition of a skip as the *event* of a tail link dropping below the cursor — "A **skip** is a still-matching tail link `a` … falling to or below the cursor … so it drops from `After(c, Σ')`" — which conflates the *event* (a clause-1 failure at one transition) with the *outcome* (omission from the whole pass). A link that drops below one cursor can rise back above a later cursor and be delivered exactly once, so coherence (no-skip ∧ no-re-delivery over the pass) survives clause-1 failures.

Counterexample, in the note's own notation (three both-states links `a, b, d`; `N = 1`; a mutable content-position key; all three match at every state):

- `Σ₀`: `κ(a)=5, κ(b)=10, κ(d)=15` → `a ≺ b ≺ d`. Call 1 at `⊥` delivers `{a}`, cursor `c₁ = a`.
- `Σ₀ → Σ₁` moves `κ(d): 15 → 3`. **Clause 1 fails at `c₁ = a`** for `(a, d)`: `κ_{Σ₀}(a)=5 <_K κ_{Σ₀}(d)=15` but `¬(κ_{Σ₁}(a)=5 <_K κ_{Σ₁}(d)=3)`.
- Call 2 at `a`: `After(a, Σ₁) = {x : 5 <_K κ(x)} = {b}`. Deliver `{b}` (full, size `1 = N`, so the reader continues), cursor `c₂ = b`.
- `Σ₁ → Σ₂` moves `κ(d): 3 → 20`. **Clause 1 fails at `c₂ = b`** for `(b, d)`: `d` rises from below `b` to above `b`.
- Call 3 at `b`: `After(b, Σ₂) = {x : 10 <_K κ(x)} = {d}`. Deliver `{d}`, cursor `c₃ = d`.
- Call 4 at `d`: `After(d, Σ₃) = ∅`, short → stop.

Delivered: `a, b, d`, each exactly once — **coherent (no skip, no re-delivery)** — while clause 1 failed at *both* held cursors. (Two links are insufficient: with only `a, d`, the drop of `d` below `a` yields an immediate short window at Call 2 and a genuine skip — the cut-point walk's pattern. The third link `b` keeps Call 2 full so the reader proceeds to Call 3, by which time `d` has risen. This is exactly the gap between "drops below the cursor" and "omitted from the pass.")

Note that the parallel claim in W9 is correctly framed: "a short window … certifies *exhaustion of the reachable tail* only under clause 1 at every visited cursor" reads as a *guarantee* statement (like W9c's "does not guarantee"), which is true. Only W5 uses the strong "if and only if / necessary and sufficient."

**Required**: Demote W5 (body and table) to a sufficiency statement: clause 1 at every held cursor is *sufficient* for coherence. Either drop the necessity claim or replace it with the genuine characterization. (The tight necessary-and-sufficient condition for whole-pass coherence is global — "the delivered multiset equals `Match` with each both-states tail link once" — not a per-cursor local condition, precisely because local violations can cancel; under a strict per-transition reading the "iff" is instead vacuous, since per-transition coherence is clause 1 by definition.) Also fix the skip/duplicate justification so it argues about omission/re-delivery over the pass, not about the per-transition drop/rise event.

### Issue 2: The computability-vs-clause-1 distinction is asserted redundantly across sections

**ASN-0108, "A ladder of key conditions" and W9**: the same conceptual separation — "whether `κ(c)` can be evaluated" vs. "whether comparisons move" — is drawn in the ladder ("Two of them concern *whether κ(c) can be evaluated at all* … The other three concern *whether comparisons move under evolution*") and then re-hammered in W9: "'Recoverable' (computability) and 'cut-point preserved' (clause 1) are *not* the same condition, and W9 needs both, named distinctly," "*no cut-point preservation is consulted*," "Computability is exactly the right proviso," "Computability ≠ clause 1."

**Problem**: This note carries the `review-mode.anti-bloat` classifier. The distinction is real and load-bearing, but it is restated four-plus times across the ladder and W9 — the "compounds across cycles" residue the classifier targets. Two adjacent accretion patterns sit in the ladder paragraph itself: a definition introduced by enumerating downstream consumers — "**Computability** … — what W2, W8, and W9 also call the cursor key being *recoverable*" — and a re-listing of items W5 already defined — "they are W5's already-defined conditions — clause 1 (cut-point preservation), clause 2 (tail-order preservation), and state-stability."

**Required**: State the computability/clause-1 distinction once (the ladder is the natural site) and reference it from W9 rather than re-deriving it. In the ladder, keep the two genuinely new definitions (computability, value-totality) and the one load-bearing implication (value-totality ⟹ state-stability); drop the consumer enumeration ("what W2, W8, and W9 also call …") and the re-listing of W5's three conditions.

### Issue 3: W6a's F-LAMBDA citation is to the wrong matching-set notion

**ASN-0108, W6a**: "the set-level statement is ASN-0127's F-LAMBDA, that a K.λ creation contributes the fresh `ℓ_new` to the matching set disjointly."

**Problem**: F-LAMBDA (ASN-0127) is about `findlinks(I, Σ)` for a *fixed* I-address set `I`, whereas this note's matching set is `Match = findlinks_V(W, d_q, Σ)` (the discoverability reading). The cited theorem does not directly apply; the bridge — that K.λ frames `M`, so `image(W, d_q, Σ)` is unchanged and `findlinks_V` inherits F-LAMBDA's disjoint addition at the frozen `I = image(W, d_q, Σ)` — is what actually delivers the conclusion and is left unstated. "X follows from F-LAMBDA" is a claim, not the step.

**Required**: State the one-line bridge (image frozen under K.λ's `M' = M` frame, then F-LAMBDA at the fixed image), or cite the `findlinks_V`-level result directly if one exists.

## OUT_OF_SCOPE

The Open Questions correctly defer multi-document ordering (the W6 cross-document blind spot), eventual-delivery guarantees for non-allocation-monotone keys, cross-state completeness invariants, exhaustion-vs-cursor-invalidation under content keys, and delivery/sizing correspondence to future ASNs. W10's deferral of absolute progress to a separate cardinality query is likewise appropriate. No overreach into count-only/full-set retrieval, MAKELINK, FOLLOWLINK, or BEBE was found.

VERDICT: REVISE
