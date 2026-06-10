# Review of ASN-0118

The operation itself is rigorously specified. The resolution/placement decomposition is sound, the composite-boundary argument for provenance is genuinely careful (the three-branch CP8 analysis correctly distinguishes range-new-fresh, range-new-already-recorded, and not-range-new, with P4★ properly scoped to the composite boundary), the tiling argument for D-CTG/D-SEQ preservation is derived from ordinal arithmetic rather than asserted, the worked example checks out numerically, and the link-discoverability wp is genuinely non-trivial. I found one internal inconsistency about how S2 is established, plus accumulated meta-prose that the anti-bloat pass is meant to surface.

## REVISE

### Issue 1: Two contradictory accounts of how S2 (arrangement functionality) is established

**ASN-0118, "Effect — displacement" (CP3a) vs. "The destination's prior arrangement is preserved"**: CP3a says "we borrow its arithmetic and its preservation lemmas wholesale — that the shifted positions remain well-formed (I3-VP), preserve depth (I3-VD), **keep the arrangement a function (I3-S2) and finite (I3-fin)**, and that the post-state remains **contiguous and sequential (D-CTG, D-SEQ preserved)**." The later section states the opposite: "the **function-ness and no-holes of COPY's actual Σ'.M(d) are not established by the I3 lemmas**: they rest on the tiling argument below ... together with K.μ⁺'s strict-extension contract."

**Problem**: These directly contradict on whether I3-S2 discharges COPY's functionality. I3's lemmas describe INSERT's arrangement, which fills the gap `[p, p+W)` with fresh content; COPY fills it with the placement positions, so I3-S2/D-CTG/D-SEQ are *about a different arrangement*. The later account is the correct one — COPY's functionality rests on the tiling (disjoint abutting intervals) plus CP3c's domain closure plus K.μ⁺ strict extension, not on I3-S2. A reader following CP3a believes a core invariant is discharged by a borrowed lemma that the ASN itself later disavows. S2 is too load-bearing to leave with two incompatible derivations.

**Required**: Narrow CP3a's borrow-list to what I3 genuinely supplies for the *shifted* positions (I3-VP well-formedness, I3-VD depth), and attribute function-ness, no-holes, contiguity, and sequentiality of COPY's `Σ'.M(d)` to the tiling argument + CP3c + K.μ⁺, consistent with the later paragraph. (Finiteness is robust either way but should likewise not be attributed to I3-fin "wholesale.")

### Issue 2: Standing-precondition paragraphs carry defensive justification and a brittle use-site inventory

**ASN-0118, "The substrate we build on"**: "At a non-reachable state these may fail, and so the scoping is **load-bearing, not decorative**; the project's foundation ASNs scope the same way (ASN-0086, ASN-0098)." And: "**We use P4★ exactly once, in the CP8 derivation**, and the boundary scoping is what makes that use sound; the per-state invariants above require only reachability and are unaffected by it."

**Problem**: "load-bearing, not decorative" is defensive editorializing; the enumerated per-state invariant list and "We use P4★ exactly once" are use-site inventories that add nothing to the argument and go stale — in fact "exactly once" is already inaccurate, since the worked example's self-transclusion variant invokes P4★ a second time. The substantive content is one sentence: states range over reachable states; P4★ additionally requires the composite-boundary scoping.

**Required**: Reduce each standing precondition to its content (reachability scope; composite-boundary scope licensing P4★). Drop the "load-bearing, not decorative" defense, the invariant inventory, and the "exactly once" count.

### Issue 3: The ordinal-level non-requirement is restated seven times

**ASN-0118, "What a spec-set names"**: across one passage the same non-requirement appears as "a *normalizing convention*, not a load-bearing precondition," "the operation never consumes it," "COPY's reasoning routes around the one place ordinal-level would be consumed," "neither on `actionPoint(ℓ)`," "we impose no ordinal-level requirement on the input," "a caller that supplies one buys nothing," and "the design is parametric in depth rather than normalizing ... never promoted to the ordinal level."

**Problem**: Seven phrasings of "ordinal-level is not required." The only sentence that advances the argument is that `act(ρ, Σ)` is single-subspace (content-residence) and single-depth (S8-depth) regardless of where `ℓ`'s action point falls, so CP0(a) rests on S3★ and CP0(c) on the single-subspace premise — neither on `actionPoint(ℓ)`. The reader must wade through the restatements to reach it.

**Required**: Keep the one load-bearing sentence (plus, if desired, a single Nelson/Gregory grounding clause). Delete the remaining restatements.

### Issue 4: Partial-binding admissibility is restated with defensive framing

**ASN-0118, "What a spec-set names"**: "We deliberately do *not* adopt ASN-0058's optional *well-formedness* condition," "a partially-bound — or even empty — span is a well-formed request," "partial binding was never a well-formedness violation," and "So `act` *resolves* partial binding by restriction — **a settled part of the operation, not a deferred question**."

**Problem**: The substantive claim — `act` intersects the denotation with bound positions, so a partially-bound span resolves by restriction — is made once and then re-asserted defensively. "a settled part of the operation, not a deferred question" and "We deliberately do not adopt" are reviewer-facing reassurances, not reasoning. (The Nelson and Gregory grounding clauses are legitimate and may stay.)

**Required**: State the restriction semantics once, keep at most one grounding citation, and remove the defensive framing.

## OUT_OF_SCOPE

The Open Questions section already scopes the genuinely future topics correctly (C2 width-shortfall under partial binding, placement order for repeated source spans, mixed-depth assembly, post-removal undiscoverability, correspondence relation, link-subspace transclusion). No misplaced claims for the harness-excluded operations (INSERT/DELETE/REARRANGE/MAKELINK/etc.) appear in the body — COPY consumes foundation operations (K.μ⁻, K.μ⁺, K.ρ) without redefining them.

VERDICT: REVISE
