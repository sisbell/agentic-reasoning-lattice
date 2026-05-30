# Review of ASN-0082

## REVISE

### Issue 1: D-SEQ-post cites D-SEP(b) for `|X| = c` outside D-SEP(b)'s stated precondition

**ASN-0082, D-SEQ-post (cardinality chain)**: "= N − c (|X| = c from D-SEP(b)'s explicit form X = {[1, k] : p₂ ≤ k < p₂ + c})"

**Problem**: D-SEP(b) is explicitly guarded "when R ≠ ∅," and its explicit-X derivation lives inside Case 2 (v > r). But D-SEQ-post must also establish `n = N − c` in the subcase L ≠ ∅, R = ∅, where the post-state V_1(d′) = L is non-empty. In that subcase D-SEP(b) does not fire, so the citation supplying `|X| = c` is unsupported. The numeric result still holds (when R = ∅, the closed form gives N = p₂ + c − 1, so |L| = p₂ − 1 = N − c), but the cardinality chain as written rests on a lemma whose precondition is violated.

**Required**: Derive `|X| = c` directly from the containment precondition (`p₂ + w₂ − 1 ≤ N`) and pre-state D-SEQ — both of which hold regardless of R — rather than from D-SEP(b); or factor the explicit-X form out of D-SEP(b)'s R ≠ ∅ guard so it is available unconditionally.

### Issue 2: "mathematically forced" overstates the depth restriction

**ASN-0082, Depth axiom**: "The asymmetry with I3 (which is established at arbitrary m ≥ 2) is mathematically forced: the contraction proof depends on TA4 in a way that I3 does not."

**Problem**: What is forced is that *this proof route* (D-SEP via TA4, whose zero-prefix precondition collides with S8a's componentwise positivity at depth > 2) requires `#p = 2`. The Open Question concedes contraction may generalize past depth 1 with a different gap-closure argument. "Mathematically forced" reads as a claim about contraction itself, not about the chosen proof, and is contradicted by the ASN's own Open Question.

**Required**: Scope the claim to the proof strategy ("forced by the TA4-based gap-closure argument used here"), consistent with the Open Question.

### Issue 3: NAT-CA introduction carries non-derivability essay (meta-prose around an axiom)

**ASN-0082, NAT-CA**: "ASN-0034's minimal NAT-* extraction ... names only the order-and-monotonicity facts its own proofs required; commutativity is *not* derivable from them, as the order-monotone but non-commutative model of ordinal addition shows, so we supply these two carrier facts here."

**Problem**: This is prose explaining *why the axiom is needed* rather than what it states — exactly the accretion pattern flagged for this note. The model-theoretic non-derivability argument is essay content occupying an axiom slot.

**Required**: State NAT-CA (commutativity and associativity of ℕ addition) and cite it as a carrier fact in one line; drop the non-derivability narrative.

### Issue 4: I3-S and D-S close with duplicated summary prose

**ASN-0082, end of "Span Width Preservation" and "Span Width Preservation Under Contraction"**: "Both endpoints of a within-subspace span shift by the same displacement ...; the width — the displacement between them — is invariant. This connects ... the displacement arithmetic underlying span endpoints (SpanReach) commutes with uniform ordinal translation." (and the near-identical contraction variant)

**Problem**: Two paragraphs in the same document state the same conclusion in different words — accretion pattern. The duplication adds no reasoning.

**Required**: State the commutativity-with-shift conclusion once (e.g., at the I3-S/D-S pairing), referenced from both.

### Issue 5: Meta-summary inventorying which clauses the worked examples "exercise"

**ASN-0082, after the link-subspace insertion example**: "The two worked examples ... together exercise the I3-I3-L-I3-X-I3-V-I3-CS-I3-CX postcondition cluster across both axes of subspace selection, and confirm that the lemma's wp derivation is invariant under the subspace identifier."

**Problem**: This is a use-site inventory / exhaustiveness claim about the examples rather than reasoning that advances a claim. The examples already demonstrate what they demonstrate; the catalog of clause labels is noise the reader skips. The second (link-active) example is itself largely a structural duplicate of the cross-subspace example with the active/passive roles swapped.

**Required**: Remove the inventory sentence; if both subspace-axis examples are retained, trim the second to the one fact it adds (I3 over a sparse, D-CTG-exempt active subspace) rather than re-running the full verification checklist.

## OUT_OF_SCOPE

### Topic 1: Generalization of contraction to ordinal depth > 1
**Why out of scope**: The depth restriction `#p = 2` and whether D-SEP/D-DP generalize to deeper ordinals is correctly identified as the Open Question. A depth-general gap-closure argument that avoids TA4's zero-prefix collision belongs in a future ASN, not this one.

### Topic 2: External-reference update after shift
**Why out of scope**: The first Open Question (how external state holding a V-position learns of repositioning) is a protocol concern for a future ASN; it is not a gap in the arrangement-layer guarantees specified here.

VERDICT: REVISE
