# Review of ASN-0100

## REVISE

### Issue 1: Post-insertion shift and its invariant-preservation lemmas are re-derived instead of inherited from ASN-0082's I3 family

**ASN-0100, §Effect Three / §Arrangement functionality / §Referential integrity / §Post-state V-position well-formedness**: INS.M-shift is stated as "For v ∈ V_{s_C}(d) with v ≥ p: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v)."

**Problem**: This is verbatim ASN-0082's I3 (PostInsertionShift) specialized to S = s_C, and ASN-0082 is a foundation ASN. ASN-0082 already establishes, for post-insertion shift, the very preservation results this ASN re-proves from the substrate: I3-VP (S8a), I3-VD (S8-depth), I3-S3 (S3★), I3-S2 (S2), I3-fin (S8-fin), I3-L (left frame), I3-X (cross-subspace frame), I3-D (cross-document frame). ASN-0100 cites ASN-0082 only for the lower-level OrdAddHom / OrdinalShift / δ machinery and never mentions the I3 family, then independently re-derives S2, S3★, S8a, S8-depth, S8-fin preservation under the shift. Rule 7 requires using the foundation rather than re-deriving it.

**Required**: Establish once that the composite's post-state arrangement M'(d) matches I3's post-insertion arrangement (same shift formula, same regions), then invoke the I3-* family for the shift-region invariant preservation. If the substrate-composite realization genuinely needs an independent argument (e.g., because the intermediate-state atomicity proof cannot use I3's single-step postcondition), state that reason explicitly and scope the re-derivation to it — do not silently duplicate the foundation result.

### Issue 2: Cross-document projection invariance is proven twice by the same argument

**ASN-0100, §Cross-document independence (Q3)** vs **§Coverage and link discoverability (INS.proj, d' ≠ d bullet)**: Both passages conclude `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)` for d' ≠ d, and both derive it identically — "every elementary step frames M(d'), so LP4 gives equality at each step, composing across the finite step sequence yields the result."

**Problem**: This is the anti-bloat pattern of two paragraphs in the same document proving the same proposition in different words. Both are statements about the same composite boundary (Σ, Σ'); neither is a per-state-vs-boundary distinction that would justify the overlap.

**Required**: INS.proj is the general statement (it covers all d', both subspaces, and the d = d' regions). Let it be the canonical home; have §Cross-document independence cite INS.proj's d' ≠ d case rather than re-running the LP4-composition argument.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L semantics)
**Why out of scope**: The ASN restricts to the content subspace and explicitly bounds this out; the analogous link-subspace operation is correctly left to a future ASN.

VERDICT: REVISE
