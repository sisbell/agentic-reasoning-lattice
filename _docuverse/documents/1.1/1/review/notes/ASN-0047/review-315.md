# Review of ASN-0047

## REVISE

### Issue 1: K.δ characterizes case-(ii) freshness as caller-checked "not derived from a structural fact," but the worked examples and S7d derive it from GlobalUniqueness

**ASN-0047, Elementary transitions, K.δ case (ii)**: "The freshness conjunct `e ∉ E` is a single caller-checked guard — checked against the present state Σ, **not derived from a structural fact** — read uniformly with `e = inc(t, k)`."

**Problem**: This uniform characterization is contradicted for `k ∈ {1, 2}` by the ASN's own discharges. The worked example Step 2 reads "`1.2.0.1 ∉ E₁` discharged by GlobalUniqueness (ASN-0034) at the account sub-allocator," and Step 3 similarly invokes GlobalUniqueness; the J4 trace discharges `1.0.1.0.1.1 ∉ E₁` via "GlobalUniqueness ... on the newly activated `A_v(d₁)`." These *do* derive freshness from a structural fact (GlobalUniqueness together with T10a's at-most-once-per-`(t, k')` constraint). The k = 0 sub-case is genuinely a dynamic frontier guard (FrontierEquivalence on the live state), but child-spawns at `k ∈ {1, 2}` are structurally fresh. S7d compounds the tension: it states "Freshness and distinctness are the case-(ii) preconditions discharged at the K.δ definition" — pointing back to the "caller-checked, not structural" text — while the worked examples discharge the identical obligation structurally. The "read uniformly" framing papers over a real difference between the two regimes.

**Required**: Split the freshness characterization by regime. State that k = 0 freshness is a dynamic frontier guard (FrontierEquivalence), and that `k ∈ {1, 2}` freshness is structurally guaranteed by T10a at-most-once-per-`(t, k')` plus GlobalUniqueness (matching the worked-example and S7d discharges). Remove the blanket "not derived from a structural fact ... read uniformly," which is false for child-spawns.

### Issue 2: The Bridging lemma justifies (†) `dom(M) = E_doc` twice

**ASN-0047, The state model, Bridging lemma (M–E_doc)**: First passage — "every allocated document is a document entity (K.δ's `Document` registration places it in `E_doc` and initialises `M(d) = ∅`), and conversely every `d ∈ E_doc` is an allocated document." Second passage (after the Notational convention) — "(†) holds by the lockstep K.δ effect (its `Document`-case registration grows `dom(M)` and `E_doc` together by the same `{e}`) together with the default-value convention that, for `d ∉ E_doc`, fixes `M(d) = ∅`; the two sets therefore have identical membership at every reachable state."

**Problem**: Two paragraphs separated by the default-value convention establish the same biconditional in different words. The second (lockstep + default-value) strictly supersedes the first (informal "and conversely"). This is the "two paragraphs say the same thing" accretion pattern.

**Required**: Keep the rigorous lockstep + default-value justification at one site and delete the informal restatement, or fold the "every allocated document is a document entity / conversely" clause into the single rigorous paragraph.

### Issue 3: P4a definition box carries a forward-deferral and a prose restatement that add no content

**ASN-0047, P4a (Trace witnessing)**: "The mechanism that discharges P4a is given in the Class (b) proof below." and "P4a therefore reads as 'every provenance entry corresponds to a content-subspace arrangement in some trace state,' consistent with both P7's grounding in `dom(C)` and J1'★'s content-scoped coupling."

**Problem**: The first sentence is a pure forward-pointer — to follow the actual discharge the reader must skip to the Class (b) proof. The second restates the already-stated formula in prose. The genuine definitional content (the *valid transition trace*, *transition history*, `M_k`, and the formula itself) is load-bearing and should stay; the meta-commentary around it is the flagged forward-deferral + restatement accretion. The well-typedness remark ("well-typed as a trace property even though it is not well-typed as a per-state invariant") also duplicates the temporal-scope point already made in the Extended reachable-state invariants preamble that this box cross-references.

**Required**: Delete the forward-deferral sentence and the "P4a therefore reads as ..." restatement; rely on the preamble for the temporal-scope classification rather than repeating it inline.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior arrangement edits (prepend, insert-in-middle, interior link withdrawal)
**Why out of scope**: K.μ⁺ is append-shaped and K.μ⁻ is suffix-only, so non-suffix arrangement edits decompose into clear-and-rebuild composites realizing named operations (INSERT/DELETEVSPAN), which are explicitly out of scope. The ASN already records the interior-link-withdrawal/`DELETEVSPAN` renumbering question as an open question; no revision is owed here.

VERDICT: REVISE
