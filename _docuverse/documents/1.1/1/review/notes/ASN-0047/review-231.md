# Review of ASN-0047

This ASN carries the `review-mode.anti-bloat` classifier, so I focus on forward-reference accretion and meta-prose in addition to the standard rigor checks. The mathematical core (K.δ identity discharges, the D-SEQ★ derivation, the K.μ~ necessity/sufficiency argument, GlobalLineage) is rigorous and I found no correctness defects in the proofs I checked against concrete tumbler values. The findings below are bloat at source, plus one genuine duplication.

I have deliberately avoided the two previously-declined findings (split-the-ASN; matrix-cells-reference-machinery). The findings below are a different pattern: meta-prose and repetition *inside body prose*, not navigation requests against the matrix.

## REVISE

### Issue 1: Route-comparison meta-prose in S8★
**ASN-0047, *Amendments to existing transitions*, S8★ content-subspace route**: "The mirror of the explicit lockstep treatment given in the *Link subspace* route below, here delivered by OrdShiftHom(a) rather than by reduction to `nⱼ = 1`."

**Problem**: This sentence advances no part of the content-subspace discharge. It exists only to relate the content route to the link route stated further down — exactly the "defer to a downstream treatment" pattern. The OrdShiftHom(a) shift-closure argument immediately preceding it is complete on its own; the reader does not need to be told it is a "mirror" of a later paragraph.

**Required**: Delete the sentence. The shift-closure step stands without the cross-route comparison.

### Issue 2: Forward-reference inventory in the J1★ derivation
**ASN-0047, *Scoped coupling constraints*, derivation of J1★**: "The matrix entry P4★ under K.μ⁺ in *Class (b)* below corresponds to this derivation's discharge: at the composite boundary, K.ρ (under J1★) supplies the missing `(a, d) ∈ R'` for every new content-subspace range entry, restoring P4★."

**Problem**: The wp computation has already concluded "to maintain P4★, K.ρ must co-occur within the composite … which is J1★ above." This added sentence only announces that a later matrix cell will say the same thing — a use-site inventory that duplicates the conclusion the derivation just reached. It is the body-prose mirror of the meta-prose this classifier targets.

**Required**: Remove the sentence; the derivation already establishes the coupling and the matrix already records the discharge.

### Issue 3: The "necessary but not sufficient" cardinality caveat is stated three times
**ASN-0047, K.μ~ precondition / necessity proof / realisation**:
- precondition: "this entails `|dom_C(M(d))| ≥ 2` but is strictly stronger"
- necessity: "(which in turn entails `|dom_C(M(d))| ≥ 2`, but the bare cardinality bound is not sufficient — a constant-valued `M(d)|_{dom_C}` of cardinality ≥ 2 admits only net-identity permutations)"
- realisation: "bare cardinality `|dom_C(M(d))| ≥ 2` is necessary but not sufficient, per *Necessity and sufficiency of the precondition* above"

**Problem**: Two paragraphs in the same document saying the same thing in different words. The caveat is load-bearing exactly once (where the precondition is stated as "takes at least two distinct values"). The necessity proof legitimately *derives* the non-constant condition, but the parenthetical re-explaining "not sufficient" there, plus the realisation paragraph re-asserting it with a back-reference, are repetitions of an already-fixed point.

**Required**: State the caveat once at the precondition. In the realisation paragraph, cite the precondition without re-explaining sufficiency; drop the parenthetical in the necessity proof (the derivation itself shows non-constancy).

### Issue 4: Exhaustiveness-inventory essay in a worked-example slot
**ASN-0047, *Worked example: prior-provenance and first-time-transcluded replacements*, closing "Contrast with the four-step fresh-content form" paragraph**: "The three forms partition by the (pre-state membership of `aₓ` in `dom(C)`, pre-state membership of `(aₓ, d)` in `R`) pair: (in C, in R) ⟹ two-step; (in C, not in R) ⟹ three-step; (not in C, not in R) ⟹ four-step. The (not in C, in R) combination is excluded by P7 …"

**Problem**: A worked example demonstrates the postconditions against a concrete scenario. This closing paragraph instead constructs a 2×2 taxonomy of replacement forms across two worked examples and argues exhaustiveness — essay content placed in a worked-example slot. The case-distinguishing fact ("pre-state `(aₓ, d) ∈ R` ⟹ no trailing K.ρ") is already made inline at each variant's J1★ check.

**Required**: Cut the taxonomy paragraph. If the cross-variant relationship is worth keeping, one sentence at the head of the example ("two- vs three-step differ by whether `(aₓ, d) ∈ R` at the pre-state") suffices; the four-step form belongs to the other example.

### Issue 5: Defensive justification + downstream deferral attached to D-CTG★/D-MIN★
**ASN-0047, *Amendments to existing transitions*, "Justification" under D-CTG★/D-MIN★**: "D-CTG★/D-MIN★ constrain *arrangement* … not link existence or discoverability — every link persists in dom(L) with fixed endsets (L12) regardless of arrangement state. The cost the strengthening imposes on link withdrawal is discussed in *Orphan links and coupling flexibility*."

**Problem**: This explains *why the strengthening is acceptable* rather than what the invariants say, and then defers the one substantive consequence (withdrawal cost) to a downstream section. The withdrawal cost is in fact developed in two places (the *Orphan links* section and Open Question on tombstoning), so this paragraph is a pointer, not content.

**Required**: Reduce to the load-bearing fact ("the strengthening drops ASN-0036's link-subspace exemption") and let the *Orphan links* section carry the cost discussion without an anticipatory pointer here.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The J4 fork composite leaves the forked document's link subspace empty and notes "A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is correctly deferred and already an Open Question — no action needed.

META: not applicable — the ASN defines extended system state (C, L, E, M, R), the elementary transitions over it, and the per-state/composite-boundary invariants abstractly; it has not drifted into implementation mechanics.

VERDICT: REVISE
