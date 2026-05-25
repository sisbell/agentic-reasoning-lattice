# Review of ASN-0098

## REVISE

### Issue 1: Citation error — "P0 of ASN-0093" does not exist
**ASN-0098, Store Monotonicity★ proof**: "Each is the reflexive-transitive closure of the corresponding single-step monotonicity guarantee (P0 of ASN-0093 for content; L12 of ASN-0093 for links, in its membership-persistence consequence)."
**Problem**: ASN-0093's content-immutability claim is labelled **C0** (ContentImmutability), not P0. P0 (ContentPermanence) lives in ASN-0047. Both state the same content-monotonicity guarantee, but the citation as written points to a label that doesn't exist in ASN-0093.
**Required**: Change to "C0 of ASN-0093" (consistent with the surrounding ASN-0093 citations like M1 and L14) or "P0 of ASN-0047".

### Issue 2: LP11 — second conjunct asserted without proof
**ASN-0098, LP11**: The formal statement includes `ran(Σ'.M(d)) = ran(Σ.M(d))` alongside `project(e, d, Σ') = π(project(e, d, Σ))`, and is restated in the claims table.
**Problem**: The proof body derives the projection equality via a biconditional chain and derives the *restricted* range equality `{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = ...`, but the *unrestricted* range equality `ran(Σ'.M(d)) = ran(Σ.M(d))` (which the postcondition asserts) is never explicitly derived. The worked trace and the parenthetical informal claim ("because π is a bijection") gesture at the argument but don't discharge it.
**Required**: Add an explicit step: from the bijection equation `Σ'.M(d)(π(v)) = Σ.M(d)(v)` over all `v ∈ dom(Σ.M(d))`, take the image on both sides; since `π : dom(Σ.M(d)) → dom(Σ'.M(d))` is a bijection (K.μ~-FIX), `ran(Σ.M(d)) = {Σ'.M(d)(v') : v' ∈ dom(Σ'.M(d))} = ran(Σ'.M(d))`.

### Issue 3: LP9 prose conflates the tight-endset case with the general case
**ASN-0098, LP9 commentary**: "When K.μ⁺ adds entries mapping V-positions to newly K.α-allocated I-addresses, those I-addresses lie outside any existing endset's coverage (the typical case — formalised below as LP19), and the projection does not grow."
**Problem**: The claim "those I-addresses lie outside any existing endset's coverage" is *false* in general — it holds only for tight endsets, as LP19 makes precise. The parenthetical "the typical case — formalised below as LP19" qualifies the claim but is easy to miss. The corresponding LP6 commentary is much sharper ("whenever `e` was tightly constructed... Without tightness, the new I-address could fall within a half-open coverage interval"). LP9 should match LP6's precision.
**Required**: Reword LP9's commentary so the conditional structure ("for tight endsets, the projection does not grow; without tightness, growth is possible") is the main clause, not a parenthetical aside.

### Issue 4: Reference-frame ambiguity in State Components
**ASN-0098, State Components**: "We work over the state structure inherited from the foundations. Three components matter here." Followed by C, M, L only.
**Problem**: The ASN later cites K.σ (ASN-0093 only), K.ρ (ASN-0047 only — and ASN-0047 carries state component R that this ASN does not include), and the K.μ family (ASN-0047). The "Remark on K.δ" tries to reconcile this but doesn't address why operations on R-bearing states (K.ρ) are admissible in a frame that lists only C, M, L. A reader cannot tell whether the system state includes R, E, etc., or only C, M, L.
**Required**: Either (i) commit to one reference frame and note in passing that operations from the other reduce to it for projection purposes, or (ii) explicitly state that the projection guarantees are robust across both reference frames because projection consults only `coverage(e)` and `Σ.M(d)`, neither of which depends on R or E.

### Issue 5: LP20 — exhaustiveness of subspace case split is implicit
**ASN-0098, LP20 proof**: "The argument splits by subspace using S3★ (GeneralizedReferentialIntegrity, ASN-0047): for content-subspace V-positions, `Σ.M(d)(v) ∈ dom(Σ.C)`; for link-subspace V-positions, `Σ.M(d)(v) ∈ dom(Σ.L)`."
**Problem**: The case split assumes every `v ∈ project(e, d, Σ)` has `subspace(v) ∈ {s_C, s_L}`. This exhaustiveness is supplied by S3★-aux (SubspaceExhaustiveness, ASN-0047), not by S3★ itself. Without citing S3★-aux, the proof has a gap: a hypothetical V-position in some third subspace would escape the case split.
**Required**: Add a citation to S3★-aux alongside S3★ to discharge exhaustiveness.

### Issue 6: LP14 numbering note contains internal-revision artifact
**ASN-0098, "Numbering note" beneath Claims Introduced**: "LP14 has been reclaimed here to label the K.ρ frame lemma added in this revision (Issue 2)."
**Problem**: "(Issue 2)" is a reviewer-issue reference from an earlier revision cycle, not a stable identifier in the published ASN. A future reader cannot resolve "Issue 2" to anything in the document.
**Required**: Remove "(Issue 2)" — the note already reads coherently without it.

### Issue 7: LP13 table summary is ambiguous
**ASN-0098, Claims Introduced table, LP13 row**: "Partial survival: discoverability requires only one I-address per slot to remain in range"
**Problem**: "only one I-address per slot" reads ambiguously between (a) "for every slot, only one I-address is needed" — a per-slot conjunctive condition — and (b) "from any single slot, only one I-address suffices" — the intended existential reading. The body prose is clearer ("requires only that *some* I-address from *some* endset persist in `d`'s range").
**Required**: Reword the table entry to match the body, e.g., "Partial survival: discoverability requires only one I-address in some slot's coverage-range intersection to remain."

### Issue 8: LP19 quantifies over "K.α (or K.λ)" but the proof handles them uniformly only on first reading
**ASN-0098, LP19**: The statement says "any K.α (or K.λ) transition `Σ → Σ_post` allocating a fresh address `a_new`". The proof opens with "K.α's precondition (ASN-0093) requires `a_new ∉ dom(Σ.C) ∪ dom(Σ.L)`... the analogous L14 disjointness applies to K.λ."
**Problem**: The K.λ argument is mentioned in a clause, but K.λ's actual precondition (from ASN-0093) is `ℓ ∉ dom(L) ∪ dom(C)` — directly the freshness condition needed, not "L14 disjointness applied". L14 is a state-level invariant about domain disjointness; what discharges the proof is K.λ's per-call freshness precondition, just as K.α's is for the content case.
**Required**: Replace "the analogous L14 disjointness applies to K.λ" with a direct citation of K.λ's freshness precondition `ℓ ∉ dom(L) ∪ dom(C)` (ASN-0093).

## OUT_OF_SCOPE

The Open Questions section catalogues precisely what's deferred — reverse-discovery primitives, V-order/I-order correspondence, links referencing links, partial coverage at link creation, fork-composite invariants. These are correctly identified as future work and not flagged as gaps in this ASN.

VERDICT: REVISE
