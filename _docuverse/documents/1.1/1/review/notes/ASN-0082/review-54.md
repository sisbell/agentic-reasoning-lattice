# Review of ASN-0082

## REVISE

### Issue 1: wp paragraphs reason about cases the preconditions exclude
**ASN-0082, Weakest-precondition analysis (insertion, conjunct 2)**: "`n = 0` would reduce this to `vₘ > 0`, which holds, but `shift(v, 0) = v` would also collapse the entire shift semantics."
**ASN-0082, Weakest-precondition analysis (contraction, "Why the obligation sits at both v and p")**: "a `p₂ = 0` p with `c = v₂` would still admit `v ≥ r` with `v₂ − c = 0`."
**Problem**: I3's contract fixes `n ≥ 1` and `p ∈ V_1(d)` (hence S8a gives `p₂ ≥ 1`). Both passages construct and reason about excluded states (`n = 0`, `p₂ = 0`) to motivate preconditions already in the carrier. This is the "imagines a case the precondition already excludes" pattern — the reader must verify these hypotheticals are moot, which adds no reasoning.
**Required**: State the discharge directly (n ≥ 1 with vₘ ≥ 1 gives the conjunct; v ∈ R with p₂ ≥ 1 gives the conjunct). Drop the counterfactual `n = 0` / `p₂ = 0` constructions.

### Issue 2: label inventory in the contraction Scope paragraph
**ASN-0082, Post-Contraction Shift, Scope**: "The postconditions D-SHIFT, D-DOM, D-L, D-CS, D-CD, and D-I together with the lemmas D-BJ, D-SEP, D-DP, and the post-state preservation lemmas (S8-depth-post, S8a-post, D-CTG-post, D-MIN-post, D-SEQ-post, S8-fin-post, S2-post, S3-post, S7-post) constitute the full DELETE specification at the V-arrangement layer; no further composition is required..."
**Problem**: This enumerates every label in the section without advancing any claim — a use-site inventory. The labels appear in their own slots below; reciting them here is meta-prose the precise reader skips.
**Required**: Reduce to the load-bearing distinction ("contraction is a complete V-arrangement transformation, unlike the insertion shift sub-operation") without the roster.

### Issue 3: repeated downstream deferral to the "composing INSERT operation"
**ASN-0082**: three paragraphs defer to the same downstream location — Scope ("belonging in a composing INSERT ASN"), Arrangement invariants Case S=1 ("which the composing INSERT operation fills and re-validates"), Gap region ("where newly inserted content will be placed by the composing INSERT operation, which extends the closed domain established by I3-CS").
**Problem**: Matches "multiple paragraphs in different sections defer to the same downstream location." The deferral is established once in Scope; the later two repetitions are noise.
**Required**: State the deferral once. The Gap-region and Case-S=1 paragraphs should make their local point (gap positions excluded by I3-CS; D-CTG/D-MIN/D-SEQ violated) without re-announcing the composing operation.

### Issue 4: NAT-CA introduction explains its provenance rather than its content
**ASN-0082, NAT-CA**: "carrier facts of ℕ addition... supplied locally because ASN-0034's NAT-* extraction omits them. ℕ-subtraction laws, likewise absent from that extraction, are routed through tumbler arithmetic (TumblerAdd's `a ⊕ w ≥ w` and the partial inverse TA4)."
**Problem**: This is "new prose around an axiom explaining why the axiom is needed rather than what it says." The axiom statement (commutativity, associativity) is clear; the surrounding paragraph is about extraction gaps and routing strategy, not the axiom's meaning. The registry row repeats the same provenance justification ("supplied locally because ASN-0034's NAT-* extraction omits it").
**Required**: State NAT-CA as the two ℕ identities. Drop the extraction-gap commentary and the subtraction-routing aside (the routing is visible where TA4/ReverseInverse are actually invoked).

### Issue 5: duplicated cross-subspace prose across the two halves
**ASN-0082, cross-subspace worked examples (insertion and contraction)**: both build the same `[2,5]→ℓ₁, [2,9]→ℓ₂` link subspace and both close with near-identical prose — "the tombstone gap at [2, 6], [2, 7], [2, 8] remains" and "one subspace shifts to close gaps, the other carries gaps as durable structure."
**Problem**: Two passages saying the same thing in different words. The additional "Link-subspace insertion: shift into a former tombstone slot" paragraph compounds this, opening with derivation-restating meta-prose ("I3's derivation routes through S8a... without invoking D-CTG, so it is subspace-agnostic") that re-explains a point the cross-subspace example already made.
**Problem (cont.)**: The subspace-agnostic property of I3 is worth stating once; demonstrating it in both the passive (insertion cross-subspace) and active (tombstone-slot) directions, plus restating the derivation rationale, is more prose than the claim requires.
**Required**: Keep one cross-subspace demonstration per operation. Collapse the "shift into a former tombstone slot" note to a single sentence (a shifted image may land in a former tombstone slot; permitted because link sparsity, not gap structure, is the invariant) without re-narrating I3's derivation path.

## OUT_OF_SCOPE

### Topic 1: insertion shift into non-text subspaces vs. tombstoning
**Why out of scope**: I3 admits `S ≥ 1` and treats a link-subspace shift as a valid standalone operation, whereas the contraction section defers link mutation to tombstoning in "a future ASN." Whether link-subspace *insertion* should likewise use a tombstone-aware mechanism rather than a forward shift is a question for that future link-arrangement ASN, not a defect in this one.

VERDICT: REVISE
