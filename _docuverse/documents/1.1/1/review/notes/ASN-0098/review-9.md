# Review of ASN-0098

## REVISE

### Issue 1: Ancestor case missing in tightness achievability argument

**ASN-0098, "Boundary and Width Behaviour" / "Cross-chain interference"**: "Cross-chain interference splits into two cases by the prefix relation between document tumblers. Non-nesting documents. ... Nesting documents. The remaining case is documents d' standing in a proper prefix relation d₀ ≺ d'."

**Problem**: The case split is incomplete. By T1 trichotomy on the prefix relation, three cases arise for distinct documents d' ≠ d₀: (a) non-nesting, (b) d₀ ≺ d' (d' is a version descendant of d₀), and (c) d' ≺ d₀ (d' is a version ancestor of d₀). The author treats (a) and (b) but not (c). For a span s = [d₀.0.s_C.k_s] with #s = #d₀ + 3, chain elements of A_C(d') for d' ≺ d₀ have the form [d'.0.s_C.k] of length #d' + 3 < #s. At position #d'+1: b_{#d'+1} = 0 (the separator of d'.0.s_C), while s_{#d'+1} = (d₀)_{#d'+1} = y₁ ≥ 1 (since d₀ = [d', y₁, ..., y_r] with y_i ≥ 1, this being how version-descendants are structured). The argument that ancestors don't interfere is straightforward but the proof must include it.

**Required**: Extend the cross-chain interference argument to include the case d' ≺ d₀. Show that ancestor chain elements satisfy b < s (by T1 case (i) at position #d'+1 with 0 < y₁), hence b ∉ [s, s ⊕ ℓ). The achievability conclusion is still correct, but the proof must close this case.

### Issue 2: Displacement notation inconsistent with foundation in worked numerical example

**ASN-0098, "Worked numerical example"**: "Construct the endset e = {(s, ℓ)} with s = [d.0.1.1] and ℓ = δ(3, 4) = [0, 0, 0, 3] — a displacement at depth 4 advancing the final component by 3. Then s ⊕ ℓ = [d.0.1.4]"

**Problem**: ASN-0034 defines δ(n, m) as a length-m tumbler [0, ..., 0, n], so δ(3, 4) has length 4. But "Let d be a T4-valid document" forces zeros(d) = 2 (M0 of ASN-0093), hence #d ≥ 5 and #s = #d + 3 ≥ 8. By TumblerAdd's result-length identity, #(s ⊕ ℓ) = #ℓ = 4 ≠ #s. Concretely for the minimal d = [1,0,1,0,1]: s = [1,0,1,0,1,0,1,1] and s ⊕ ℓ computes (with action point k = 4) to r_i = s_i for i < 4 and r_4 = s_4 + ℓ_4 = 0 + 3 = 3, giving [1,0,1,3] of length 4 — not [d.0.1.4] (which would be [1,0,1,0,1,0,1,4] of length 8). The same error applies to the non-tight example with δ(4, 4). The qualitative point survives, but the arithmetic as written does not.

**Required**: Replace δ(3, 4) with δ(3, #s) (equivalently δ(3, #d+3)), and δ(4, 4) with δ(4, #s). Alternatively, work the example concretely with a specific document tumbler (e.g., d = [1,0,1,0,1]) and explicit length-8 displacements δ(3, 8) and δ(4, 8). The "depth 4" gloss conflates element-field depth with tumbler length and should be revised.

### Issue 3: LP4 hypothesis assumes both sides defined without explicit precondition

**ASN-0098, LP4**: "For every transition Σ → Σ', every endset e, and every document d ∈ dom(Σ.M): Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)"

**Problem**: The convention adopted earlier ("project(e, d, Σ) is left undefined when d ∉ dom(Σ.M)") makes Σ'.M(d) undefined when d ∉ dom(Σ'.M), so the hypothesis "Σ'.M(d) = Σ.M(d)" already requires d ∈ dom(Σ'.M) for the equation to be parseable. The lemma works in context because M1 (ASN-0093) makes dom monotonic, but the precondition is left implicit. Subsequent applications (LP6, LP7, LP14) explicitly cite the monotonicity, so the obligation arises but isn't named in the lemma itself.

**Required**: State the precondition d ∈ dom(Σ.M) ∩ dom(Σ'.M) explicitly, or note within LP4's proof that the hypothesis requires d ∈ dom(Σ'.M) and that this follows from M1 in every reference frame considered.

### Issue 4: Non-nesting case argument compresses T1 case analysis

**ASN-0098, "Non-nesting documents"**: "by T10 (PartitionIndependence, ASN-0034), chain elements of A_sub'(d') for d' non-nesting with d₀ differ from s at the document-prefix position and so do not fall in [s, s ⊕ ℓ) for spans confined to a single document's subspace."

**Problem**: T10 alone establishes only distinctness of addresses (a ≠ b), not lex position in the interval [s, s ⊕ ℓ). The argument that chain elements fall outside the interval requires T1 case (i) analysis at the divergence position j ≤ min(#d₀, #d'), showing that whether d'_j < d_{0,j} or d'_j > d_{0,j}, the chain element ends up below s or above s ⊕ ℓ respectively (using that (s ⊕ ℓ)_j = s_j in the prefix-copy region since j < k = #s). The "and so" elides this case analysis, which is non-trivial because it depends on the trichotomy at the divergence position. The descendant case ("nesting documents") spells the analogous argument out at position #d₀ + 1; the non-nesting case deserves the same treatment.

**Required**: Expand the non-nesting argument to spell out the T1 case analysis at the divergence position, mirroring the level of detail given for the descendant case.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery primitives
**Why out of scope**: The open questions section enumerates a "reverse-discovery primitive (given a V-position, return the set of links whose projections contain it)" as future work. The current ASN's forward-projection machinery is independently coherent and need not commit to the reverse direction here.

### Topic 2: V-order semantics of projected positions
**Why out of scope**: Whether V-positions in a projection reflect the I-order of their underlying I-addresses, and how K.μ~ interacts with this, is identified as an open question. The current ASN treats projection as an unordered set of V-positions, which is sufficient for the discoverability and displacement claims it makes.

### Topic 3: Link-to-link discoverability under transclusion constraints
**Why out of scope**: When endsets reference link addresses rather than content addresses, CL-OWN (ASN-0047) restricts which documents can arrange those links, making LP16's triple-intersection condition harder to satisfy. The structural consequences for link-to-link reachability are real but belong in a follow-up ASN; LP16 as stated remains correct.

VERDICT: REVISE
