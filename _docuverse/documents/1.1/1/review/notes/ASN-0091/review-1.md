# Review of ASN-0091

## REVISE

### Issue 1: Domain Stability derivation is not entailed by RA-π's signature alone

**ASN-0091, "Domain Stability and Range Invariance"**: "RA-π's signature `dom(Σ.M(d)) → dom(Σ.M(d))` forces equality of domains across the transition."

**Problem**: The signature only states that π maps from and into dom(Σ.M(d)). Combined with RA-π's equation, this entails dom(Σ'.M(d)) ⊇ π(dom(Σ.M(d))) = dom(Σ.M(d)) — the forward inclusion. The reverse inclusion dom(Σ'.M(d)) ⊆ dom(Σ.M(d)) is not entailed: nothing in RA-π or RA-frame as stated prevents Σ'.M(d) from being defined at additional V-positions outside dom(Σ.M(d)).

**Required**: Either add `dom(Σ'.M(d)) = dom(Σ.M(d))` as an explicit conjunct in the definition of "Vstream-only on d", or explicitly invoke ASN-0084's K.μ~-FIX (which establishes this via D-SEQ★) when transitioning from REARRANGE_K to the abstract class.

### Issue 2: R-FRAME-P/S do not contain Σ'.L = Σ.L

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "ASN-0084's R-FRAME-P/S discharge RA-frame."

**Problem**: RA-frame includes `Σ'.L = Σ.L`. ASN-0084's R-FRAME-P and R-FRAME-S each contain exactly three clauses: (a) non-S subspace V-positions in d preserved; (b) other documents' arrangements preserved; (c) C' = C. L preservation is not among them. The L' = L invariant comes from K.μ~'s frame in ASN-0047 ("C' = C; E' = E; R' = R; L' = L; (A d' : d' ≠ d : M'(d') = M(d'))"), not from R-FRAME-P/S.

**Required**: Either cite K.μ~'s frame from ASN-0047 directly (where L' = L is explicit), or note that REARRANGE_K instantiates K.μ~ and inherits the full frame from there.

### Issue 3: RE-frag witness lacks concrete verification

**ASN-0091, "Run Decomposition Is Not Invariant"**: "A direct witness: a 3-cut pivot on a single maximal run of length `n ≥ 3`, with cuts placed at the run's first V-position, one position later, and just past the run's end..."

**Problem**: The witness is described in prose. A reader cannot tell whether R-PRE is satisfied without working out the example themselves. The claim that "the single pre-state run becomes two post-state runs — a long run of n − 1 consecutive (V, I) pairs and a singleton at the displaced position" requires explicit verification against ASN-0084's R-P1 and R-P2 post-conditions.

**Required**: Work the example explicitly. For instance: dom(M(d)) = {[s_C, 1], [s_C, 2], [s_C, 3]} with M(d)([s_C, k]) = a + k − 1 (single maximal run of length 3). With cuts (c₀, c₁, c₂) = ([s_C, 1], [s_C, 2], [s_C, 4]), apply R-P1/R-P2 to obtain M'(d)([s_C, 1]) = a+1, M'(d)([s_C, 2]) = a+2, M'(d)([s_C, 3]) = a. Verify that maximal runs of M'(d) are ([s_C, 1], a+1, 2) and ([s_C, 3], a, 1) — cardinality 2, strictly greater than the pre-state cardinality 1.

### Issue 4: "Reverse direction" of cardinality change has no witness

**ASN-0091, "Run Decomposition Is Not Invariant"**: "The reverse direction can also occur: rearrangement can bring previously separated V-runs into adjacency, reducing the decomposition's cardinality."

**Problem**: This bidirectional claim is asserted without supporting argument. The witness for cardinality increase doesn't symmetrically establish cardinality decrease — REARRANGE_K is a specific operation parameterized by a cut sequence, and the inverse of a pivot/swap is not in general another pivot/swap on the post-state.

**Required**: Either supply a concrete witness for cardinality decrease (e.g., a fragmented arrangement where a single REARRANGE_K coalesces two runs into one), or weaken the claim to its established half ("cardinality can strictly increase").

### Issue 5: Identity permutation case unhandled in abstract class

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: The "Vstream-only on d" class is defined by RA-π + RA-frame.

**Problem**: The identity bijection π = id satisfies RA-π trivially (M'(d)(v) = M(d)(v) for every v) and RA-frame holds with Σ' = Σ. So the abstract class includes Σ' = Σ as a degenerate "rearrangement". However, ASN-0084's K.μ~ admissibility requires π ≠ id (clause (ii)). The relationship between the abstract class (which admits identity) and REARRANGE_K (which excludes it) is not addressed.

**Required**: Note this distinction explicitly. Either restrict "Vstream-only on d" to non-identity bijections, or clarify that the abstract claims hold for the (degenerate) identity case as well, with REARRANGE_K being a strictly non-trivial subset.

### Issue 6: No worked example verifying derived consequences

**ASN-0091, throughout**: The ASN derives RE-C, RE-dom, RE-ran, RE-μ, RE-L, RE-cov, RE-disc, RE-proj, RE-frag, RE-other, RE-trans, RE-sub, RE-origin, RE-R — fourteen claims.

**Problem**: No concrete scenario traces a small arrangement through REARRANGE_K and verifies these claims numerically. The witness for RE-frag is the closest the ASN comes, and even that is informal. For an ASN that derives so many consequences, a single worked example demonstrating that all the RE-* claims hold simultaneously on a concrete pre-state and post-state would significantly strengthen the proof and catch any hidden inconsistencies.

**Required**: Add a worked example. For a 3-document state with d transcluding content from d' and links connecting positions in d, exhibit pre-state Σ.M(d), Σ.M(d'), Σ.L, then apply a specific REARRANGE_K, exhibit the post-state, and confirm each of RE-C through RE-R against the explicit values.

### Issue 7: Multi-step closure not addressed

**ASN-0091, "Claims Introduced" table**: Each claim is stated as a single-step property (Σ → Σ').

**Problem**: Foundation ASN-0098 distinguishes single-step lemmas (LP2, LP3, ...) from multi-step lemmas (LP2★, LP3★, ...). ASN-0091 does not address whether its claims compose across sequences of REARRANGE invocations, nor how they interact with non-REARRANGE transitions interleaved in a multi-step trace. RE-disc, RE-trans, and RE-proj in particular would benefit from a multi-step ★ form.

**Required**: Either add multi-step (★) versions for the survivability claims (RE-disc★, RE-trans★, RE-proj★ for pure REARRANGE sequences) or explicitly note that the single-step claims compose by induction over REARRANGE-only sequences, while mixed sequences are governed by the per-operation lemmas of the foundation.

## OUT_OF_SCOPE

### Topic 1: Identity REARRANGE composition

The Open Question on whether every well-formedness-preserving bijection is realizable as a finite composition of cut-sequence rearrangements is correctly out of scope for this ASN.

### Topic 2: Link-subspace rearrangement semantics

The Open Question on link-subspace rearrangement semantics is correctly out of scope — REARRANGE_K fixes S = s_C per CS3.

### Topic 3: Bound on cardinality increase

The Open Question on an upper bound for maximal-run-decomposition cardinality increase per REARRANGE is a future characterisation, not an error in this ASN.

### Topic 4: Observational equivalence at link-discoverability level

The Open Question on observational equivalence under link discoverability is properly future work.

VERDICT: REVISE
