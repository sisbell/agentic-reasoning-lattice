# Review of ASN-0040

## REVISE

### Issue 1: B4 states its justification twice
**ASN-0040, Atomicity / B4**: para 1 — "Atomicity is therefore a corollary, not a separately imposed requirement." then B4 body — "Because `baptize(p, d) ∈ Σ` (B0a) and the foundation fixes every `op ∈ Σ` as a single partial function on 𝒮, the value `s'.B = s.B ∪ {next(s.B, p, d)}` is committed on one edge of `→`: there is no intermediate observable state s_mid with `s → s_mid → s'`."
**Problem**: Two paragraphs in the same section carry identical content (Σ-membership ⇒ single partial function ⇒ one edge ⇒ no intermediate state). The lead-in paragraph adds nothing the B4 statement does not. This is the anti-bloat "two paragraphs say the same thing in different words" pattern. The provenance tag "(corollary of B0a and the foundation Σ signature)" is then repeated at the B4 heading, the Bop ATOMIC line, B8's preconditions, B9's axiom list, and the table — a use-site inventory of the same fact.
**Required**: Keep one statement of atomicity. Drop the lead-in paragraph and reduce the repeated parenthetical to a single citation.

### Issue 2: S0 reproves a foundation result
**ASN-0040, S0 (StreamOrdering)**: "We derive the strict ordering directly from the per-step increase of inc(·, 0)."
**Problem**: S(p, d) — base `c₁ = inc(p, d)` with `d ∈ {1, 2}`, siblings `cₙ₊₁ = inc(cₙ, 0)` — is exactly the domain of a T10a child allocator: child-spawning by `inc(·, k')`, `k' ∈ {1,2}`, then sibling production by `inc(·, 0)`. S0's claim (strictly increasing under T1) is verbatim T10a.7 (EnumerationInjectivity), and the proof reuses the same premises (TA5(a) per-step increase, T1 transitivity, T1 irreflexivity). Standard 7 forbids reinventing what a foundation already proves.
**Required**: Cite T10a.7 for S0, or state explicitly why the baptism layer cannot invoke it (e.g., that S(p, d) is deliberately not treated as an allocator domain pending the `allocated(s) ⊆ s.B` open question). The same overlap should be acknowledged for B7 against T10a.5/T10a.6 — though B7 is genuinely more general (arbitrary B6-valid pairs, not allocators in one conforming tree), so it is not strictly subsumed; note the relationship rather than reprove silently.

### Issue 3: B6 condition-(i) paragraph is "why the axiom is needed" framing
**ASN-0040, B6**: "Condition (i) is imposed by definition, not forced by stream validity: a pure-trailing-zero parent at d = 1 yields a T4-valid stream, yet we exclude it to break the aliasing whereby such a parent and its truncation at d = 2 generate the identical stream — e.g. ([1, 0], 1) and ([1], 2) both produce {[1, 0, n] : n ≥ 1} ..."
**Problem**: The framing ("imposed by definition, not forced by stream validity ... the disambiguation that makes namespace disjointness (B7) well-posed") is meta-prose explaining why a clause exists rather than what it requires, and it forward-defers to B7. Per the anti-bloat guidance, the concrete aliasing example (`([1,0],1)` vs `([1],2)`) is object-level content and should be kept — flag the placement/framing, not the example.
**Required**: Keep the aliasing example; trim the surrounding rationale, and attach the example to where B7's well-posedness is actually established rather than as a standalone justification of clause (i).

### Issue 4: Trace Step 4 misnames the increment parameter
**ASN-0040, A baptism traced, Step 4**: "inc([1, 0, 1, 0, 1], 1) = [1, 0, 1, 0, 1, 1]. TA5(d) with k = d − 1 = 0 intermediate zeros."
**Problem**: The call is `inc(p, d)` with `d = 1`, so TA5's parameter `k = 1`. Writing "TA5(d) with k = d − 1 = 0" reuses the symbol `k` for the intermediate-zero count, colliding with TA5's own `k` (the depth). A precise reader must disentangle which `k` is meant.
**Required**: State it as "TA5(d) with d = 1: d − 1 = 0 intermediate zeros," reserving `k` for TA5's depth parameter.

## OUT_OF_SCOPE

### Topic 1: Relationship between s.B and allocated(s)
**Why out of scope**: Whether `allocated(s) ⊆ s.B` holds, and what aligns allocator-extension transitions with baptismal operations, is correctly deferred to a future ASN (already listed in Open Questions). This ASN is right to keep the registry component separate from the foundation's allocator domains — no claim to fix here.

VERDICT: REVISE
