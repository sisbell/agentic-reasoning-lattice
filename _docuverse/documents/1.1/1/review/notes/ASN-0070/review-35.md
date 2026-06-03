# Review of ASN-0070

## REVISE

### Issue 1: Open Question is already settled by an invoked foundation
**ASN-0070, Open Questions**: "Must `R(d, e)` always yield V-positions whose subsequent content lookup via `M(d)` and `C` succeeds, or may resolution succeed where content access would fail?"

**Problem**: This is posed as open, but the note's own foundations decide it. For content-subspace resolutions, every `v ∈ R(d, e)|_{s_C}` has `M(d)(v) ∈ dom(C)` by S3★ (GeneralizedReferentialIntegrity, ASN-0047) — content lookup *always* succeeds. For link-subspace resolutions, `M(d)(v) ∈ dom(L)`, which by L14 (StoreDisjointness) is disjoint from `dom(C)`, so a `C`-lookup trivially does not apply — by design, not by gap. Both branches are determined; nothing is open. The note even invokes S3★ and L14 elsewhere (F-subspace derivation). Posing a settled question as open is a depth/clarity failure.

**Required**: Either remove the question, or convert it to a stated derived guarantee ("content-subspace resolutions always reference allocated content, via S3★; link-subspace resolutions reference links, via L14"). If a genuinely open variant is intended, restate it so it is not closed by S3★/L14.

### Issue 2: Worked-example assumption introduced mid-computation
**ASN-0070, A Worked Example (Configuration 1)**: "Assuming `a₀, a₀ + 1, a₀ + 2` are disjoint from `{a₁, a₁ + 1, a₁ + 2}` (allocations from distinct sub-allocators per GlobalUniqueness), the intersection is empty."

**Problem**: The example's verification of F-sound and F-complete depends on `a₀…`/`a₁…` allocator-distinctness, but this is introduced as an in-line "Assuming" during the per-block computation rather than fixed in the configuration setup. A reader checking soundness must back-track to discover that the result hinges on an unstated setup premise. The same premise is silently re-used in Configurations 4 and 5.

**Required**: State the allocator-distinctness of `a₀` and `a₁` (and that both lie in `dom(C)`) once, in the Configuration block where `M(d)` is laid out, and reference it from the per-block steps.

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics under concurrent modification
**Why out of scope**: The second Open Question (concurrency guarantees while the queried document is concurrently modified) is genuinely new territory — the transition model is sequential (SequentialTransitionAxiom, ASN-0047), so concurrency belongs to a future ASN, not a revision here.

### Topic 2: Transclusion-lineage relationships between `follow(ℓ, d, i)` and `follow(ℓ, d', i)`
**Why out of scope**: The third Open Question concerns cross-document derivation relationships not yet modeled; legitimately deferred.

Notes on the anti-bloat pass: I checked for the flagged accretion patterns (repeated deferrals to one downstream location, axiom-rationale sub-paragraphs, use-site inventories in definition bodies, imagined-excluded cases, document-ordering justifications). None are present at a flaggable level — the Discussion section explicitly *consolidates* the Nelson readings rather than scattering them per-lemma, F-contig's proof appears once (in Computation) and is referenced rather than duplicated, and the F-canonical proof is dense but entirely load-bearing. The note appears to have already absorbed prior anti-bloat passes. The F-multi "Structural admissibility" paragraph borders on reachability meta-prose but carries a non-obvious, informative contrast (content subspace has no injectivity constraint, unlike CL-UNIQ for links), so I am not flagging it.

VERDICT: REVISE
