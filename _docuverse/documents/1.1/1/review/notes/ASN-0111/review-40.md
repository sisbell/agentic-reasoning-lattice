# Review of ASN-0111

## REVISE

### Issue 1: RL5's screen-passing branch claims allocatability that the transition vocabulary does not provide

**ASN-0111, "Determinacy and the immutability of the recorded relationship" (RL5), and Claims table, RL5 row**: "for a *screen-passing* address, absence from `dom(Σ.L)` is not preserved by `→*` — a subsequent K.λ can allocate `a` itself (any screen-passing address at the frontier of an active link sub-allocator is a candidate)"

**Problem**: This is stated as a property of the screen-passing class, and it is false for concrete families of screen-passing addresses. Under the standing precondition's transition vocabulary, every address that ever enters `dom(L)` lies on some link sub-allocator chain `A_L(d)`, and every element of such a chain has element-field depth exactly 2: the first emission `[d.0.s_L.1]` has `#E = 2`, and every subsequent emission is `inc(·, 0)`, which preserves length (TA5(c), with `sig = #` on T4-valid addresses by TA5-SigValid). Therefore `a = [1.0.1.0.1.0.2.1.1]` passes every screen conjunct (T4-valid; `zeros = 3`; `E(a) = [2,1,1]` so `subspace_I(a) = s_L`; `#E(a) = 3 ≥ 2`) yet satisfies `a ∉ dom(Σ'.L)` at every reachable `Σ'` — its `⊥` is permanent despite the screen passing. A second family arises under ASN-0047's K.δ-based document creation: `a = [2.0.1.0.1.0.2.1]` passes the screen, but its node field `[2]` violates NodeLineage (`n₀ = [1] ≼` every node entity), so `home(a)` can never enter `dom(M)`, and L1a excludes `a` from `dom(L)` at every reachable state. The sentence "a subsequent K.λ can allocate `a` itself" is thus false at these addresses, and the claims-table phrasing "carries no stability at screen-passing addresses" repeats the overstatement. The true dichotomy is asymmetric: screen failure *proves* permanence; screen passage proves nothing in either direction — within the screen-passing class, some addresses are permanently absent and some (exactly the frontier-reachable ones) can later be allocated. Note also that the same passage's clause "which is exactly the permanence that RL0's 'a failed screen guarantees `⊥` without an invocation' already relies on" misdescribes RL0 — RL0's claim is per-state and does not rely on permanence across futures.

**Required**: Restate the split as: (i) screen-failing ⟹ `⊥` permanent (each conjunct necessary at every reachable state); (ii) screen-passing ⟹ permanence is not derivable from the address alone — exhibit the frontier witness for instability (a screen-passing `a` at the frontier of an active `A_L(d)`, `⊥` before the K.λ step, a link value after) and acknowledge, or exhibit, the permanently-absent screen-passing family. Keep the caching discipline ("do not cache `⊥` at a screen-passing address") but justify it by undecidability-from-the-address, not by universal allocatability. Update the claims-table RL5 row to match.

### Issue 2: RL4's non-vacuity construction leaves its own base hypothesis unwitnessed

**ASN-0111, "Faithful disclosure of nesting" (RL4)**: "Take any reachable `Σ*` with a document `d ∈ dom(Σ*.M)`"

**Problem**: The paragraph's stated purpose is to discharge a vacuity worry ("The exclusion has force only if the state pair RL4 quantifies over actually exists"). An existence proof must discharge its own existential hypotheses, and this one does not: at `Σ₀`, `(E₀)_doc = ∅`, so the existence of a reachable state containing an allocated document is exactly the kind of fact the paragraph cannot assume. It is true, but it must be shown — the ASN set this standard for itself two sentences earlier.

**Required**: One sentence exhibiting the prefix from `Σ₀`: K.δ case (ii) with `k = 2` at `n₀` yields the account `inc(n₀, 2) = [1.0.1]` (operand `zeros = 0 ≤ 1`, parent `n₀ ∈ E`, freshness by ChildSpawnFreshness); K.δ case (ii) with `k = 2` at `[1.0.1]` yields the document `inc([1.0.1], 2) = [1.0.1.0.1]` (operand `zeros = 1 ≤ 1`); the post-state is the required `Σ*`.

### Issue 3: RL0's "no partial-success middle state" passage duplicates RL1 (anti-bloat)

**ASN-0111, "Deriving the read"**: "Separately, there is no partial-success middle state: no execution returns a proper sub-value of the stored entry. This is a property of the *operation*, not of the codomain — `Link` is closed under shrinking a connective slot … it is the definition that never returns one."

**Problem**: "No execution returns a proper sub-value of the stored entry" is RL1's completeness clause ("omitting nothing and introducing nothing"; "every recorded span … is returned") restated one section early in different words — the two-paragraphs-saying-the-same-thing pattern this review mode flags. The passage is also not about RL0's actual content: RL0 establishes the `Link`-versus-`⊥` dichotomy, and a shrunk sub-value is a member of `Link`, so the partial-success question is a value-fidelity (RL1) question, misplaced in the totality section. The only content here that RL1 does not already carry is the codomain-closure observation (fragments of stored values inhabit `Link ∪ {⊥}`, so completeness is enforced by the definition, not by the type), which genuinely sharpens RL1.

**Required**: Delete the partial-success sentences from the RL0 section; relocate the one-sentence codomain-closure observation into the RL1 section, where completeness is stated.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
