# Review of ASN-0036

## REVISE

### Issue 1: Deferral prose repeated four times across the S8 region
**ASN-0036, Span decomposition / Worked example**: The statement "S8 proves only the singleton (n=1) partition; maximal runs (n>1) are deferred to Open Questions" appears in (a) the section intro ("introduced as forward-scaffolding... which we defer to Open Questions"), (b) the S8 statement body ("Cast in the general correspondence-run form... the instance with every nⱼ = 1"), (c) the paragraph after the statement ("What S8 establishes is exactly this singleton partition... stands as forward-scaffolding for that deferred question"), and (d) the Worked example header ("not a proof of maximal-run existence or uniqueness, which S8 leaves to Open Questions. S8 itself proves only the singleton (n = 1) partition").
**Problem**: This is forward-reference accretion — multiple paragraphs saying the same thing and deferring to the same downstream location. The reader must re-absorb the same caveat four times.
**Required**: State the singleton scope once, at the S8 statement. Remove the duplicate caveats from the intro, the post-statement paragraph, and the worked example.

### Issue 2: The general correspondence-run apparatus is unused machinery
**ASN-0036, Span decomposition**: The correspondence-run definition is introduced with general `n` (`(A k : 0 ≤ k < n : Σ.M(d)(shift(v, k)) = shift(a, k))`), S8's postcondition (b) is stated in the general `(vⱼ, aⱼ, nⱼ)` form, and the `shift(·, k)` extension to general `k` on I-addresses is developed — yet S8 proves only `nⱼ = 1`, where (b) collapses to `M(d)(vⱼ) = aⱼ` and `shift` is only used at `k = 0` (the identity).
**Problem**: The spec's own minimality principle (TA-assoc: "Anything more would be unused machinery and unverified obligation") is violated. The general-`n` definition, the general postcondition form, and the general-`k` shift machinery carry obligations this ASN never discharges. Vacuous generality — the witness always sets `nⱼ = 1`.
**Required**: State and prove the singleton partition directly (postcondition (b) as `M(d)(vⱼ) = aⱼ`). Move the maximal-run apparatus (general `n`, ordinal-displacement identity, general-`k` shift) entirely into the Open Question that defers it. The worked example's by-hand `n = 5` / `n = 2` "maximal run" verifications (including the explicit `k = 3` computation) demonstrate this deferred, unproven content rather than what S8 establishes — relocate or reframe them to verify the proven singleton partition and the design constraints (S0, S3, S7, D-SEQ) only.

### Issue 3: "Pairwise disjoint intervals" overstates the proof
**ASN-0036, S8 postcondition**: "whose half-open intervals are pairwise disjoint and cover dom(M(d))."
**Problem**: The formal claim (a) and the proof establish only V-position-level uniqueness — `(E! j :: vⱼ ≤ v < shift(vⱼ, nⱼ))` for `v ∈ dom(M(d))`. Disjointness of the intervals `[vᵢ, shift(vᵢ,1))` as tumbler sets (which range over non-V-position tumblers of other depths, e.g. `[1,1,5]` inside the depth-2 interval `[[1,1],[1,2))`) is asserted in the prose header but never proven. The within-subspace lemma is stated only for `t` with `#t = m`, so it does not cover intervening tumblers of other depths.
**Problem detail**: The header claim is stronger than both the formal (a) and the proof.
**Required**: Either align the prose to the formal claim ("the runs partition the V-positions of dom(M(d))") or prove interval-level disjointness as tumbler sets. The ingredients (cross-subspace subtree containment via T5/T10; consecutive same-subspace ordinals) are present but not assembled into the stated conclusion.

### Issue 4: Section-title drift
**ASN-0036, section header "Span decomposition"**: The section is titled "Span decomposition," but its sole theorem is now "S8 (Singleton span partition)" and the body explicitly disclaims the decomposition (maximal-run) content.
**Problem**: Title names content the section no longer delivers.
**Required**: Retitle to match the singleton-partition scope (e.g., "Singleton span partition").

## OUT_OF_SCOPE

### Topic 1: Existence and uniqueness of maximal correspondence runs
**Why out of scope**: This is the genuinely structural question (does the arrangement admit a unique minimal-cardinality decomposition into maximal runs?), and it is already correctly routed to Open Questions. It belongs in a future ASN, not this one — provided Issue 2 strips the half-built apparatus back out of S8's contract.

### Topic 2: Operation preservation of D-CTG / D-MIN / subspace alignment
**Why out of scope**: Whether INSERT/DELETE/COPY/REARRANGE preserve the contiguity and alignment invariants is operation-layer territory, explicitly listed out of scope and correctly deferred to Open Questions.

VERDICT: REVISE
