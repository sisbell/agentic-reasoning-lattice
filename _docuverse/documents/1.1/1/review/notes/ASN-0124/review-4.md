# Review of ASN-0124

I checked every introduced claim (FD-IMGC through FD-COINC) against its derivation, the four named constructions (FD-NEUT(c), FD-LOSSY, FD-CONVEX, FD-FRESH), the dynamics partition, the wp analysis, and the worked illustration. Specifics I verified rather than took on faith:

- **FD-IMGC** equality `image_C = image ∩ dom(C)`: both directions discharge correctly — (⊇) genuinely needs S3★ + SD to rule out an `s_L` witness mapping to a content address, and the argument does so. The whole containment layer rests on this and it holds.
- **FD-STEP** is exhaustive over the vocabulary (K.α/K.δ/K.λ/K.ρ/K.μ⁺_L inert by FD-FRAME; K.μ⁺/K.μ⁻/K.μ~ the only movers), and each per-document formula is exactly the comprehension read at the one changed arrangement.
- **FD-LOSSY**: the two-state construction is valid — I checked J0/J1★/J1'★ initial-to-final on both composites, the strict-contraction precondition on the clear, and that `dom(M) = {d}` over the whole trace makes the set equality `{d}={d}` hold stratum-wide while incidence differs `{1}` vs `{2}`.
- **FD-FRESH**: the iterated-K.α / clear / rebuild / K.ρ composite is a *valid* composite (per-state invariants hold at every elementary-reachable state; the mid-composite removal of old images is harmless because the couplings are initial-to-final), and the finddocs-invariance follows cleanly from FD-FRAME + FD-STEP with `A_new ∩ I = ∅` riding on `I ⊆ dom(Σ.C)`.
- **FD-WITNESS**: (⊆) uses P4a's trace-witness, (⊇) chains P4★-at-boundary then P2-along-suffix. Both land. FD-GHOST's `k=n`-term subtraction is correct.
- **FD-VDYN**: the four cases are exhaustive for a single transition (only one arrangement moves per step; a K.δ-fresh document cannot be named at Σ), and each composes resolution-drift with containment-motion soundly; the K.μ~ case correctly localizes all motion to `I → I'` via F-IMG-SWING-through-FD-IMGC.

No proof-by-"similarly," no bare checkmarks, no improper cross-references (all citations — ASN-0034/0036/0043/0045/0047/0053/0058/0082/0086/0093/0098/0127 — are foundation), no reinvention of foundation notation (`image_C`, `ran_C`, `resolve`, `finddocs`, `finddocs_R` are genuine derived constructs over ASN-0127's `image` and ASN-0047's `Contains_C`/`R`). Boundary cases are handled: empty `I`/`Q`, fresh document, full clearance (`Ret = ∅`), first insertion, pure append, empty intersection (FD-COOC's `I = ∅` guard, read within `dom(Σ.M)`). The concrete example (Worked Illustration), the non-trivial wp (FD-CWP, including its `Ret = ∅` boundary), and the derived-consequence depth (FD-CHAIN, FD-VERS, FD-COOC) are all present.

I weighed whether the historical companion (FD-HIST–FD-COINC) is scope creep, since the note declares "the containment query alone." It is the present-tense operation's soundness foil — FD-SOUND's exclusion is exactly FD-GHOST, and `finddocs_R` is provably what the implementation computes (deviation 1). It is stated abstractly over `R` (an alternative "has-ever-contained" implementation would have to satisfy FD-HIST/FD-WITNESS), and the deeper historical questions are deferred. This is in-scope and correct, not drift.

## REVISE

(none)

## OUT_OF_SCOPE

The eight open questions correctly mark new territory rather than gaps in this ASN. Two I independently confirmed are genuinely deferrable, not latent defects:

### Topic 1: Interior-of-composite coherence of the live ⊆ historical bound
**Why out of scope**: FD-SUPER is correctly restricted to composite boundaries (P4★ is a boundary property); at an interior elementary state `R` may lag containment, so `finddocs ⊆ finddocs_R` can transiently fail. The ASN does not claim it there, and open question 1 names exactly this. Resolving it requires a coherence contract on interior states, which is future work.

### Topic 2: Multiplicity / attribution-bearing answers
**Why out of scope**: FD-V's bare-identity codomain and FD-LOSSY's positionlessness are deliberate; enriching the answer with matched material, positions, or per-member multiplicity (open questions 3, 8) would inherit new soundness/stability obligations and belongs in a separate refinement ASN, as the note states.

VERDICT: CONVERGED
