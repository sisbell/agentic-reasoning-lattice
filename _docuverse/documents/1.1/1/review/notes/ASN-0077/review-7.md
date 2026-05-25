# Review of ASN-0077

## REVISE

### Issue 1: O0(b) derivation conflates L1c and K.λ roles

**ASN-0077, "Where origin already lives"**: "For `x ∈ dom(L)`, L1c (LinkAllocatorConformance, ASN-0047) supplies the analogous correspondence directly... The seed `t₀` is document-level (`zeros(t₀) = 2`) and equals `origin(ℓ)` by L1c's stated identification, so `origin(ℓ)` is precisely the document-level tumbler at the root of `ℓ`'s allocation chain — naming exactly the document under which `ℓ` was allocated."

**Problem**: L1c alone gives "structural projection = chain seed" (i.e., `t₀ = origin(ℓ)` where `t₀` is some document-level tumbler). It does *not* establish that this chain seed is *the document that allocated ℓ*. The "naming exactly the document under which ℓ was allocated" claim requires K.λ's precondition `origin(ℓ) = d ∈ E_doc`, which is introduced in the *next* sentence as "corroboration" rather than as a load-bearing premise. The derivation reads as if L1c discharges (b) by itself, when in fact two foundation citations are jointly required.

**Required**: Restructure the paragraph so that L1c is cited for the structural-projection-equals-chain-seed identity, K.λ is cited as the load-bearing source for chain-seed-equals-allocating-document, and the composition is explicit. Or fold K.λ into the primary chain rather than presenting it as ancillary.

### Issue 2: Vacuous "or ∅ otherwise" in V-span over link subspace

**ASN-0077, "Lifting origin to a V-span"** (after the equivalence chain): "So `origins_V(Σ, d, σ) = {d}` when the intersection is non-empty, and `∅` otherwise."

**Problem**: Precondition (vi) of the V-span operation forces every depth-`m` position in `⟦σ⟧` into `dom(M(d))`; in particular `u ∈ ⟦σ⟧ ∩ dom(M(d))`, so the intersection is *always* non-empty for admissible inputs. The "or ∅ otherwise" branch is unreachable. The ASN later derives this non-emptiness explicitly in "Empty-restriction within a non-empty document (V-span)", but the earlier mention is misleading on first read.

**Required**: Either drop the "or ∅ otherwise" branch (admissibility forces non-emptiness), or qualify it as "vacuously, since precondition (vi) excludes the empty-restriction case".

### Issue 3: Singleton I-span proof relies on an implicit "no children of A_C(d)" reading without citing K.α

**ASN-0077, "Edge cases", Singleton I-span (Case `#b > #a`)**: "Third, SubAllocatorAxiom (a) (ASN-0047) routes outputs by subspace... every output of `d` with `subspace_I = s_C` is an output of `A_C(d)` and not of `A_L(d)`. So `a` and `b` are both outputs of `A_C(d)`."

**Problem**: SubAllocatorAxiom (a) gives only the *forward* direction (A_C(d)'s outputs have `subspace_I = s_C`). The *converse* — every dom(C) element with `subspace_I = s_C` and `origin = d` lies in `dom(A_C(d))` — is the load-bearing step, and SubAllocatorAxiom (a) and (e) alone don't establish it. T10a-conformance permits child-spawning, so A_C(d) could in principle produce content outputs at length `> #d + 3` via child allocators. The converse holds because K.α's *Subsequent emission* rule uses `inc(max, 0)` of the max-with-same-origin, which is length-preserving (TA5(c)) and so confines every K.α emission for d to dom(A_C(d)). Without citing K.α's determinate algorithm here, the length-equality conclusion `#b = #d + 3` rests on an unstated reading.

**Required**: Insert a citation of K.α's *Subsequent emission* algorithm at the step that concludes "all of d's content allocations have length #d + 3", showing that K.α's `inc(max, 0)` rule structurally precludes A_C(d) from spawning content children.

### Issue 4: O0(c) totality clause is stated but its load-bearing portion is forward-deferred

**ASN-0077, Claim O0**: "(c) Totality and single-valuedness — `origin` is total on `dom(C) ∪ dom(L)` and single-valued; permanence under state transitions is O5, derived below."

**Problem**: Totality and single-valuedness are dispatched in one line ("Totality is (a). Single-valuedness is T4b's functional definition of projections"). Permanence is forward-deferred to O5. While O5's derivation does not circularly depend on O0(c) (it depends on O0(a) via O3), the lemma statement of O0 lists permanence as a postcondition but supplies no proof at its point of use. A reader reading O0 linearly must trust that O5 closes the loop. Either inline the permanence argument here (one sentence: "O3 below establishes origin as a pure projection of address components; combined with P3's `dom(C) ⊆ dom(C')` and `dom(L) ⊆ dom(L')`, the projected value is unchanged"), or remove permanence from O0(c) and present it as an independent consequence at O5 alone.

**Required**: Either inline the one-step permanence argument under O0(c), or drop the permanence sub-clause from O0 and let O5 carry it.

## OUT_OF_SCOPE

### Topic 1: Reporting link origins from an I-span

**Why out of scope**: The ASN explicitly notes that `origins_I` drops link addresses by intersecting with `dom(C)` rather than `dom(C) ∪ dom(L)`, and lists this asymmetry as Open Question 1. The V-span case handles links uniformly via S3★ and CL-OWN, so the present operation does meet Nelson's home-document requirement for the natural reader-facing case (V-spans). Whether SHOWORIGIN over an I-span should also surface link origins is a design question for a successor ASN.

### Topic 2: Transitive provenance / chain visibility

**Why out of scope**: The ASN correctly observes that SHOWORIGIN names the original allocating document without walking the transclusion chain (O4: parallel witnesses). Surfacing intermediate documents is a separate operation, raised in Open Question 2.

### Topic 3: Native vs transcluded distinction within a single document

**Why out of scope**: SHOWORIGIN as specified does not distinguish "natively allocated in d" from "transcluded into d". This is acknowledged in Open Question 3 as deferred to a separate operation.

VERDICT: REVISE
