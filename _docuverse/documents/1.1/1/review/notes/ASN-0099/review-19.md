# Review of ASN-0099

## REVISE

### Issue 1: A1's discharge is informal, not substrate-derived

**ASN-0099, A1 (LinkStoreInertOfNonAllocatingOperations)**: "For the remaining three operations — K.μ⁺, K.μ⁻, and K.ρ — whose published frames in ASN-0047 do not name `L` — the preservation is established by two converging sources of authority: (1) Design intent (Nelson). ... (2) Implementation evidence (Gregory, udanax-green)."

**Problem**: A1 is not derivable from substrate axioms. L12 (LinkImmutability) gives per-link value preservation; L12a (LinkStoreMonotonicity) gives `dom(L) ⊆ dom(L')`. Neither rules out dom(L) growing during K.μ⁺, K.μ⁻, or K.ρ — that requires A1's strengthening that *no new links are added*. The ASN discharges this strengthening by appeal to design intent and implementation history, which is not a formal substrate derivation. F9, F9★, F9-cor, F9★-cor, F17, and F18 are load-bearing on this informal discharge. A reviewer asked to verify these claims must accept Nelson+Gregory as authoritative.

**Required**: Either (a) flag A1 as a substrate amendment request to ASN-0047 (which should add `L' = L` to the K.μ⁺, K.μ⁻, K.ρ frames explicitly), (b) re-state A1 as an explicit hypothesis pending substrate confirmation rather than discharging it locally, or (c) weaken F9 (and downstream F17, F18) to monotonic inclusion only — equivalent to F19/F19-filt/F19-sco at single steps — when A1 cannot be discharged formally. The current presentation introduces a substrate-level structural invariant at the applications level with informal grounding, which is unusual for a verification-oriented spec.

### Issue 2: F12 mislabeled in claims table

**ASN-0099, Claims Introduced table**: F12 is listed under "introduced" twice — once in the operation table (correctly as "definition" for `findlinks_V`) and once in the claims table (where it appears as both definition and "introduced").

**Problem**: The body text says explicitly that F12 is "DEFINITION of findlinks_V (not a derived identity)" and that the equivalence "holds by stipulation." The claims table entry says "definition" — consistent — but the entry's prose says "names the V→I→Link composite for citation in downstream derivations; this is a definition, not a derived identity." This is correct but redundant with the parenthetical in the body.

**Required**: Minor. Either consolidate the body's F12 framing with the claims-table entry, or drop one of the redundant labels. Not a correctness issue, just presentation noise.

### Issue 3: Empty scope boundary not surfaced alongside other empty cases

**ASN-0099, "The Empty Query" section**: discusses empty I (returns ∅), empty C (returns dom(L)), empty J in a constraint (returns ∅), empty dom(L) (returns ∅).

**Problem**: The empty scope case — `S = ∅`, giving `findlinks_scoped(I, ∅, Σ) = findlinks(I, Σ) ∩ ∅ = ∅` for any I — is not called out in the "empty" enumeration. F14's intersection form makes the result trivial, but the same is true of the other empty cases that are explicitly discussed. The asymmetry leaves a small gap in the boundary-case roster.

**Required**: Add one sentence to the empty-query discussion noting that `S = ∅` likewise produces the empty result, by direct intersection. Minor.

### Issue 4: Multi-step survivability lemmas lack worked-example coverage

**ASN-0099, "A Worked Example"**: covers F1, F2, F3, F5, F6, F7, F8, F9, F10, F11, F13, F14, F15, F17, F19, F20 (and others implicitly). F9★, F9★-cor, F9-cor are not exercised against a concrete instance.

**Problem**: The single-step survivability claims (F9) are exercised in Query 4. The multi-step closures (F9★, F9★-cor) and the single-step non-allocating preservation across the full V ∖ {K.λ} (F9-cor) are not concretely demonstrated. F9★ and F9★-cor are operationally distinct — they cover sequences interleaving multiple non-allocating operations, common in practice. Without an example, the reader has to take "per-step F9 chained by transitivity" on faith for a derivation that, while plausible, has more moving parts than F9 alone (K.ρ-stepping through R changes, K.σ stepping through dom(M) changes, etc.).

**Required**: Extend the worked example with a multi-step sequence — e.g., K.σ adding a new document `d_c`, K.α extending `dom(C)` under `d_c`, K.ρ recording provenance, then K.μ⁻ contracting `d_a` — and verify findlinks(I, ·) is invariant across the whole chain. This exercises F9★-cor concretely, and would also surface any latent A1-dependency issue at K.ρ.

### Issue 5: F4's first witness uses `α.0` as a coverage point — non-T4 tumblers in coverage need explicit acknowledgment

**ASN-0099, F4 first witness**: "`α.0 ∈ coverage(Σ.L(a).eᵢ)` (since `α ≼ α.0` by the definition of `≼` extending `α` with one further component)"

**Problem**: The witness relies on `α.0` (α extended with a 0 component) being in coverage. But `α` is an element-level address with `zeros(α) = 3` and `α[#α] ≠ 0` (T4). Appending a 0 to α yields a tumbler with `zeros = 4`, which is not T4-valid, and an adjacent zero (since `α` itself ends in a non-zero, but the new zero is at the last position making it the new last component) — but also possibly not satisfying T4's "no adjacent zeros" if α's second-to-last component matters. More importantly: this tumbler is in T (per T0, any finite sequence of naturals with length ≥ 1) but is not a valid address. The witness implicitly relies on coverage extending over all of T, not just T4-valid tumblers. This is correct (PrefixSpanCoverage in ASN-0043 gives coverage as `{t ∈ T : x ≼ t}`, ranging over all of T), but the reader has to make this jump silently.

**Required**: Add one sentence acknowledging that coverage ranges over T (not over T4-valid addresses), so `α.0` is legitimately in coverage even though it would not be a valid address. This makes the witness construction transparent.

### Issue 6: Worked example's depth-2 V-position for link subspace introduces a state inconsistency

**ASN-0099, Query 9 setup**: The pre-state Σ has `Σ.M(d_a) = {v_a^1 ↦ α₁, v_a^2 ↦ α₂, v_a^3 ↦ α₃}` — content-subspace positions only. The K.μ⁺_L step adds `v_a^L := [s_L, 1]` of depth 2.

**Problem**: Per S8-depth (ASN-0036) and S8a, all V-positions within a single subspace of a document share a common depth `m_S`. The content-subspace positions `v_a^k = [s_C, 1, ..., 1, k]` are stated to have "depth `m_C`" (unspecified value, with `m_C ≥ 2`). The link-subspace position `v_a^L = [s_L, 1]` has depth 2 (by LinkVPositionDepthAxiom). The depths can legitimately differ across subspaces, so no contradiction — but this is the first time the example exercises a *different* depth for the link subspace than for the content subspace, and the reader has to know LinkVPositionDepthAxiom to verify admissibility. The example could state the depth values explicitly (e.g., `m_C = 2` for content subspace and `m_L = 2` for link subspace) to make the per-subspace depth structure visible.

**Required**: Fix `m_C = 2` in the worked example setup so that all V-positions in d_a's content subspace are explicitly `[s_C, k]` for some k. This makes the V-position structure uniform with what Query 9 introduces for the link subspace, and exercises S8-depth's per-subspace independence visibly rather than implicitly.

### Issue 7: Filtered + scoped composition not formally addressed

**ASN-0099, Operation definitions**: introduces `findlinks_filtered(C, Σ)` and `findlinks_scoped(I, S, Σ)` separately but doesn't formally compose them.

**Problem**: A reader might naturally want to combine: "links satisfying constraint set C, restricted to scope S". The natural composition is `findlinks_filtered(C, Σ) ∩ S`. Is this consistent with the F2/F3-style conformance contract? Does it satisfy F15 ∧ F17 simultaneously? The ASN doesn't say. This is the operationally most common form (filter + scope), and its absence from the formal vocabulary is a gap.

**Required**: Either (a) add a definition `findlinks_filtered_scoped(C, S, Σ) := findlinks_filtered(C, Σ) ∩ S` with corresponding determinism/survivability/monotonicity claims, or (b) explicitly note in "What we have not specified" that the composition is intended to be naive intersection without further specification.

## OUT_OF_SCOPE

### Topic 1: I→V resolution (FOLLOWLINK / RETRIEVEENDSETS)

**Why out of scope**: ASN-0099 covers V→I→Link discovery. The reverse direction — given a link, find the V-positions in some target document that arrange the link's endset coverage — is a distinct operation with its own subtleties (notably handling I-addresses no current arrangement maps). This belongs in a future ASN, not in this revision.

### Topic 2: Multi-instance / distributed semantics

**Why out of scope**: The ASN is single-instance, single-state abstract specification. Distribution, replication, partition tolerance, and consistency models are higher-layer concerns that compose with this operation but don't define it.

### Topic 3: Access control composition

**Why out of scope**: Scope filtering (F14) covers the structural shape of access control composition. The actual access-control predicate (who can see which links) is policy, not abstract specification.

### Topic 4: wp analysis for non-FINDLINKS operations on findlinks postconditions

**Why out of scope**: F9, F9★, F9-cor, F9★-cor, F11, F19, F19-filt, F19-sco collectively characterize how findlinks evolves under arbitrary state transitions. Explicit wp derivations of the form `wp(K.μ⁺, findlinks(I, ·) = X)` would mostly evaluate trivially since findlinks depends only on Σ.L. The non-trivial wp at K.λ — `wp(K.λ allocating ℓ_new, ℓ_new ∈ findlinks(I, ·))` reducing to `(E i : coverage(eᵢ) ∩ I ≠ ∅)` — is operationally just the post-state match predicate. Adding these would not deepen the analysis materially.

### Topic 5: Time bounds, latency guarantees, indexing freshness windows

**Why out of scope**: The ASN's atomicity claim (no intermediate state in which a link exists but is undiscoverable) is a state-level invariant, not a wall-clock guarantee. Quantitative timing belongs to implementation specifications.

VERDICT: REVISE
