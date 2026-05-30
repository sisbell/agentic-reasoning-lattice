# Review of ASN-0084

## REVISE

### Issue 1: Necessity sketch for R-PRE(iv) computes w_β via an identity that its own hypothesis invalidates
**ASN-0084, R-SP "Necessity sketch (R-PRE(iv) coverage)"**: "With w_α = ord(c₁) − ord(c₀) = 4 − 2 = 2 and w_β = ord(c₂) − ord(c₁) = 100 − 4 = 96 ... R-P1 with j = 2 demands M'(d)(c₀ + 2) = M(d)(c₁ + 2), i.e., M'(d)([1, 4]) = M(d)([1, 6]). ... [1, 6] ∉ dom(M(d))..."

**Problem**: The region width is *defined* as a cardinality — "We write w_α = |α|, w_β = |β|, w_μ = |μ| for the region widths." The identity `w_β = ord(c₂) − ord(c₁)` is *derived* only "Under R-PRE, by R-PRE(iv) and D-SEQ" (Width-ordinal identities paragraph). The sketch drops R-PRE(iv) and then uses the very identity that R-PRE(iv) licenses, obtaining w_β = 96. Under the actual definition, β = {v ∈ V_S(d) : c₁ ≤ v < c₂} = {[1,4], [1,5]}, so w_β = |β| = 2. With w_β = 2, R-P1 ranges over j ∈ {0,1} and references only M(d)([1,4]), M(d)([1,5]) — both defined. Likewise w_α = |α| = 2, and R-P1 ∪ R-P2 then tile exactly {[1,2],[1,3],[1,4],[1,5]} with R-EXT covering [1,1] and the empty right exterior. The pivot is a *well-defined* transposition of two 2-element regions; the cited failure at j = 2 (and "compounds at j = 3, ..., 95") never occurs. The sketch therefore does not demonstrate that R-PRE(iv) is load-bearing — it demonstrates only that conflating the cardinality width with the ordinal-difference width produces an apparent failure.

**Required**: Either (a) exhibit a genuine failure under the cardinality definition of w_β — note that under D-SEQ, V_S(d) is always contiguous {[1,1],…,[1,N]}, so the regions are always well-defined cardinalities and the source references c_i + j (j < w) always stay within V_S(d); this suggests R-PRE(iv) may be redundant for well-definedness given D-SEQ, which must be confronted — or (b) withdraw the claim that R-PRE(iv) is semantically load-bearing and characterize precisely what it adds beyond D-SEQ + a bound on c_{n−1}.

### Issue 2: CS3 well-typedness sketch repeats the same width conflation
**ASN-0084, R-SP "Well-typedness argument (R-PRE(iii) — CS3)"**: "Region β ... has no well-typed extent when its bounding cuts straddle subspaces: the cross-subspace interval [c₁, c₂) under T1 does not correspond to a region width..."

**Problem**: With K = ([1,2],[1,5],[2,1]) and V_S(d) = {[1,1],…,[1,5]}, the region β = {v ∈ V_S(d) : c₁ ≤ v < c₂} = {v ∈ V_S(d) : [1,5] ≤ v < [2,1]} = {[1,5]} is a perfectly well-defined set with cardinality |β| = 1. The "no well-typed extent" claim again presupposes the ordinal-difference reading of width (ord(c₂) − ord(c₁) across subspaces), not the stated cardinality definition. The argument that CS3 is a "well-typedness guard" is not established by this example; under the actual definition w_β = 1 and R-P1 is evaluable.

**Required**: Argue CS3's necessity from the actual definitions (e.g., from the ambiguity of "the subspace S" in R-PRE(iv) when cuts span subspaces, or from the frame condition R-FRAME-P/S(a) treating subspace 2 as inert while a cut names a subspace-2 position), not from an ill-typed ordinal difference.

### Issue 3: Δ / R-DISP machinery is introduced and then declared non-operational
**ASN-0084, Displacement Analysis / R-BLK Phase 3**: "Phase 3 is formulated entirely in terms of π; the displacement Δ plays no operational role. ... These magnitudes are *descriptive*."

**Problem**: PermutationDisplacement and R-DISP (a full LEMMA with a six-case proof, plus a custom signed-magnitude carrier on which "We do *not* define addition, multiplication, or an ordering") are introduced, then explicitly stated to drive no postcondition and to be consumed "only as an equality predicate." Every postcondition (R-PIV, R-SWP, R-PPERM, R-SPERM, R-BLK) is stated and proved through π alone; R-COMM, not R-DISP, supplies the within-region commutation that Phase 3 needs. This is unused machinery carrying its own bespoke carrier type — exactly the "minimum that addressing requires" caution against unverified, unused obligation.

**Required**: Either connect R-DISP to a postcondition it is necessary for, or demote it to a remark (and drop the signed-magnitude carrier definition), keeping the descriptive cross-checks in the worked examples without the lemma apparatus.

### Issue 4: Canonical-decomposition apparatus is not load-bearing for any postcondition
**ASN-0084, Canonical decomposition steps (a)–(d) and helper lemma**: the exhaustive-Merge confluence/termination argument over Split and Merge.

**Problem**: R-SP's own "Q is non-trivial" paragraph states that S8 existence is satisfied by *any* correspondence-run partition ("Singleton-run partitions establish S8 existence"), and B' = R-BLK(B) "is valid but not necessarily maximal." No stated postcondition requires the *maximal/canonical* partition or the claim that the merge process reaches it; that content is used only in the worked examples' descriptive "canonical partition" lines, which could cite S8's uniqueness directly. The merge-order-independence proof (a)–(d) plus the from-scratch "Existence of a maximum" helper lemma therefore reprove operational content S8 already exports the uniqueness of, without feeding any obligation of this ASN.

**Required**: Either identify the postcondition that consumes merge-process confluence, or remove (a)–(d) and the helper lemma, deferring the operationalization of canonical reduction to a future ASN and letting the worked examples cite S8 for uniqueness.

### Issue 5: Meta-prose — dependency-audit use-site inventory in the body
**ASN-0084, opening "Dependency audit" paragraph**: "ASN-0034 and ASN-0036 are load-bearing throughout: every region/interval argument, displacement computation, and run-decomposition step below cites one or both (T1, OrdinalShift, TS2–TS5, TA5, and the NAT-* arithmetic axioms ...; S0–S8, D-CTG, D-SEQ, D-MIN, and OrdShiftHom ...)."

**Problem**: This is a use-site inventory justifying the `depends:` set rather than advancing any claim. The catalogue of which lemmas are cited where, and the argument for removing ASN-0053, is editorial metadata that the precise reader must read past. It belongs in the inquiry's dependency record, not the ASN body.

**Required**: Remove the inventory; if ASN-0053 is genuinely unused, record that in the `depends:` set itself, not in expository prose.

### Issue 6: Meta-prose — "Q is non-trivial" and necessity-sketch framing in R-SP
**ASN-0084, R-SP**: the "Q is non-trivial" paragraph, the "*Scope.*" preamble, the "Remaining conjuncts (R-PRE(i), R-PRE(ii))" paragraph, and the closing "The arguments above establish the qualitative claim ... left as the open question recorded above."

**Problem**: R-SP is stated as sufficiency-only, then accretes paragraphs defending why Q is non-trivial, why three conjuncts are "load-bearing," and a taxonomy of "semantic precondition" vs "well-typedness guard" — none of which discharge the lemma's stated postcondition (the ⇐ implication). This is defensive justification around the claim rather than the claim's proof. Combined with Issues 1–2 (the sketches it frames are themselves flawed), the necessity material should be cut to the sufficiency proof plus, at most, one correct counterexample.

**Required**: Reduce R-SP to its sufficiency proof; move any retained necessity result to a separate, correctly-argued lemma.

## OUT_OF_SCOPE

### Topic 1: Link-subspace integrity under text rearrangement
**Why out of scope**: REARRANGE is deliberately confined to the text subspace; the effect of text rearrangement on subspace-2 links (which reference I-addresses, preserved here by C′ = C and ran-invariance) is a separate operation/ASN, not a gap in this one.

### Topic 2: Composition of rearrangements and k-cut (k > 4) generalization
**Why out of scope**: Already recorded under Open Questions; these are future territory, not defects in the present 3/4-cut development.

META:

VERDICT: REVISE
