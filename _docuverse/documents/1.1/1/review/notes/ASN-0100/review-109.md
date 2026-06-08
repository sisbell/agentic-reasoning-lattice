# Review of ASN-0100

I read this against the foundation contracts and traced each effect, each invariant conjunct, and each intermediate state of the substrate composite. The treatment is unusually complete, so this review records the checks I ran and where they landed.

**Boundary cases — all covered.**
- Position 0 / prepend (`j = 0`): the dedicated example exercises the *forced* full content-subspace clearance (`n'_{s_C} = 0`), total shift, and re-pin of the minimum. The forced-ordering analysis correctly makes the K.μ⁻-before-K.μ⁺ dependency conditional on `Right ≠ ∅`.
- Append / last (`j = N`): K.μ⁻ omitted, `Right = ∅`, handled and exemplified.
- Empty document: first-emission branch keys on `dom(C)`, not the arrangement; the residual-content-under-empty-subspace interaction is correctly routed to the subsequent-emission branch.
- Deep subspace (`m_C = 3`): the off-prefix exclusion in D-CTG★ — the one genuinely live step at `m ≥ 3` — is shown via T1 case (i) on an actual off-prefix tuple `[1,2,1]`, not asserted.

**Tiling (the hardest invariant) — verified.** Left `{1,…,p_m−1}`, Insertion `{p_m,…,p_m+n−1}`, Shifted-right `{p_m+n,…,N+n}` are shown pairwise disjoint via last-component arithmetic (soundly, after first establishing shared prefix from D-SEQ★/D-CTG-depth) and their union is contiguous `{1,…,N+n}`. INS.M-exhaustive closes the "no fourth region" gap that functionality depends on.

**Invariant conjuncts — all addressed.** I cross-checked every conjunct of ExtendedReachableStateInvariants (per-state, boundary, transition, couplings). S4, P6, P7 (per-state vs P7a boundary correctly distinguished), L0's two-conjunct split, C1b/C1c per-address discharge, S8★ uniqueness via C1a/M12 — each is handled at intermediates and at the boundary. The composite-boundary premise in INS.pre is load-bearing and correctly justified (it makes pre-state P4★ available for the Shifted-right provenance argument).

**Reuse of I3 — sound.** The Left ∪ Shifted-right regions are correctly identified as the `S = s_C` instance of I3, with the gap-fill (Insertion) explicitly outside I3's scope and the cross-region disjointness supplied independently. I3-S2/S3/VP/VD/fin transfer because INSERT's `M'(d)` agrees with I3's arrangement exactly on those regions.

**Depth requirements met.** Two non-trivial wp computations (discoverability preservation with tight-endset collapse; provenance membership with chain-element characterisation), full step-by-step INS.proj derivation through every intermediate, and derived consequences (cross-document allocation independence, identity-by-allocation). Five worked examples each isolate a distinct mechanism rather than repeating one.

**Cross-references — clean.** Every cited ASN (0034, 0036, 0047, 0058, 0082, 0093, 0098) is a foundation; no non-foundation references and no reinvented notation.

**Anti-bloat scan.** I checked specifically for forward-reference accretion, imagined-excluded cases, axiom-rationale prose, and duplicate paragraphs. The "What is not allocated" subsection and the Two-Stream background are statements of what the operation does/does not do (exempt by the stated criterion, not noise). The Nelson grounding in the Atomicity close connects the formal result to the source mandate and is brief enough to be acceptable framing rather than non-advancing prose. I found no paragraph that imagines a precondition-excluded case, no use-site inventories in definition slots, and no document-ordering justifications.

I could not find a hand-wave, a skipped case, an unaddressed conjunct, or a "by similar reasoning" substituting for a multi-case argument.

## REVISE

(none)

VERDICT: CONVERGED
