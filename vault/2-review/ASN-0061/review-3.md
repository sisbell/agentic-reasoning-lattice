# Review of ASN-0061

## REVISE

### Issue 1: D-CF justifications cite wrong or incomplete sources

**ASN-0061, Frame Conditions**: "C' = C follows from P0, ASN-0047" and "The provenance frame follows from J2 (ContractionIsolation, ASN-0047): arrangement contraction requires no coupling to other state components."

**Problem**: Two errors.

(a) P0 states `dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a))` — monotonicity and immutability. This gives C ⊆ C' (content can only grow), not C' = C (content stays the same). The equality C' = C requires additionally showing no new content is allocated. That fact comes from the elementary transition frames: both K.μ⁻ and K.μ⁺ have `C' = C` as frame conditions. P0 is the wrong citation.

(b) J2 covers K.μ⁻ only. DELETE is K.μ⁻ + K.μ⁺. The K.μ⁺ step has its own frame (`R' = R`), and the J1 coupling constraint — which could in principle require provenance recording for the extension step — must be shown vacuous. The composite transition section does this work correctly (`ran(M'(d)) ⊆ ran(M(d))` so `ran(M'(d)) \ ran(M(d)) = ∅`), but D-CF's justification cites only half the argument.

The same imprecision appears in the P4 verification: "Contains(Σ') ⊆ Contains(Σ) (since M'(d) lost mappings and no other arrangement changed)." The phrase "lost mappings" conflates domain reduction with range reduction. The operative fact is `ran(M'(d)) ⊆ ran(M(d))` — an I-address range property — which the J1 analysis establishes but D-CF and the P4 paragraph do not state.

**Required**: Cite the K.μ⁻ and K.μ⁺ frame conditions as the source of C' = C, E' = E, R' = R. Either defer justification to the composite transition section ("verified below") or reproduce the frame argument for both steps. For P4, state `ran(M'(d)) ⊆ ran(M(d))` explicitly as the reason Contains(Σ') ⊆ Contains(Σ).

### Issue 2: Composite transition decomposition invalid when R = ∅

**ASN-0061, DELETE as Composite Transition**: "The composite Σ → Σ' consists of two steps: (i) Arrangement contraction — K.μ⁻ ... (ii) Arrangement extension — K.μ⁺ ..."

**Problem**: K.μ⁺ (ASN-0047) requires strict domain extension: `dom(M'(d)) ⊃ dom(M(d))`. When R = ∅ — which occurs whenever the deletion extends through the last position (Cases 1 and 4 of D-DP) — there are no right-region positions to reintroduce. Step (ii) would add zero new positions, violating K.μ⁺'s strict-superset precondition. The composite as written is not a valid sequence of elementary transitions in this case.

The postconditions (D-LEFT, D-DOM, D-SHIFT, D-DP) are all correct when R = ∅ — the issue is only with the formal decomposition into ASN-0047 elementary transitions.

**Required**: Make step (ii) conditional on R ≠ ∅. When R = ∅, the composite reduces to K.μ⁻ alone. State this explicitly and verify the coupling constraints (J0, J1, J1') for the K.μ⁻-only case (all vacuous: no content allocated, no new I-addresses in range, no new provenance). The existing coupling analysis remains valid for the R ≠ ∅ case.

## OUT_OF_SCOPE

### Topic 1: Generalization beyond ordinal depth 1

The depth restriction D-PRE(iv) (#p = 2, ordinal depth 1) is load-bearing: D-SEP's round-trip uses TA4 whose zero-prefix condition is vacuously satisfied only at depth 1; D-DP's contiguity proof relies on depth-1 ordinals being natural numbers (subtraction by a constant preserves unit gaps between consecutive integers). At ordinal depth 2+, TA4's precondition is no longer vacuous (ordinal components are positive by S8a, not zero), and contiguity between multi-component ordinals requires a richer argument. The ASN correctly identifies this as an open question.

**Why out of scope**: This requires extending the tumbler algebra (ASN-0034) with new lemmas for deep-ordinal round-trips and deep contiguity, then re-proving D-SEP and D-DP under weaker hypotheses. New territory, not an error in this ASN.

### Topic 2: Link endset interaction with deletion

When DELETE removes V-positions whose I-addresses appear in link endsets, the links survive (they attach to I-addresses, not V-positions), but the reachability of those I-addresses through the arrangement changes. The ASN notes this as an open question.

**Why out of scope**: Link semantics are explicitly excluded from this ASN's scope. The interaction between deletion and link discoverability is a separate specification concern.

VERDICT: REVISE
