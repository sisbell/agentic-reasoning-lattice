# Review of ASN-0099

## REVISE

### Issue 1: Triplicated witness-inventory tag "three strengthenings and two weakenings"

**ASN-0099, "The Match Predicate" (F1 intro, F4, realizability discharge)**: The same inventory phrase recurs three times:
- F1 paragraph: "The realizability witnesses below — three strengthenings and two weakenings — carry the load"
- F4 statement: "The witnesses below exhibit this for three strengthenings and two weakenings of F1's per-endset overlap test."
- Realizability discharge: "The witnesses below — three strengthenings and two weakenings — are concrete instances."

**Problem**: This is the use-site/exhaustiveness-inventory accretion pattern. The reader is told the same count three times before reaching a single witness. The witnesses themselves are labeled "Strengthening 1/2/3, Weakening 1/2," so the running count adds nothing.

**Required**: State the partition once (at F4, where the individuation claim lives) and delete the two other announcements.

### Issue 2: Quadruplicated A1/F9 decomposition statement ("atomic ops directly, K.μ~ via constituents")

**ASN-0099, A1 body, A1 table row, F9 body, F9 table row**: The fact that K.μ~ is reached only through its K.μ⁻ + K.μ⁺ decomposition is asserted four times:
- A1 body: "K.μ~ is the non-atomic K.μ⁻ + K.μ⁺ composite, so A1 reaches it through its two atomic constituents..."
- A1 table row: "K.μ~ reached only via its K.μ⁻ + K.μ⁺ decomposition (A1a at both)"
- F9 body: "atomic ops directly, K.μ~ through its two atomic constituents"
- F9 table row: "each atomic op (via A1a + F8), the K.μ~ composite"

**Problem**: Two paragraphs (plus two table rows) say the same thing in different words. The decomposition routing belongs at exactly one site (A1's body, where K.μ~ is non-atomic and the constituent argument is made).

**Required**: Carry the K.μ~-via-constituents argument once in A1's body. F9 should cite A1 without re-deriving the routing; trim the table rows to bare statements.

### Issue 3: Verbatim re-derivation between the meta-lemma and sub-lemma

**ASN-0099, "Determinism and Comprehension Invariance"**: ComprehensionInvariantUnderΣL's chain and PerLinkInvarianceUnderValuePreservation's proof are the same derivation written twice: both run "L6 component-wise tuple equality ⟹ |Σ.L(a)| equality and per-slot endset equality ⟹ coverage deterministic ⟹ predicates evaluate identically."

**Problem**: The two lemmas have a genuinely load-bearing hypothesis difference (global `Σ.L = Σ'.L` vs. per-link `Σ'.L(a) = Σ.L(a)`), so both should exist — but reproving the identical chain is duplication. The connecting paragraph ("The per-link case of ComprehensionInvariantUnderΣL stands on its own, under the weaker hypothesis...") is meta-prose justifying the coexistence rather than advancing either claim.

**Required**: Prove the per-link steps once; have the sub-lemma's proof cite "the per-link steps of ComprehensionInvariantUnderΣL applied at the weaker hypothesis." Delete the justifying bridge paragraph.

### Issue 4: F11's distinction-from-ASN-0098 essay with double forward-defer

**ASN-0099, "Persistent Discoverability (I-Side)"**: After F11's two-line proof, two paragraphs ("Distinction from ASN-0098's V-side discoverability..." and "I-side persistence is exactly what permits F19's monotonicity...") expand on the I-side/V-side contrast, defer forward to Query 5 twice ("Query 5 below exhibits the divergence concretely," "as Query 5 demonstrates"), and motivate F19 rather than establishing F11.

**Problem**: This is forward-reference accretion plus downstream-consumer prose. The substantive content — that V-side persistence is *not* claimed and is invalidated by K.μ⁻ — is one sentence; the surrounding essay restates it via the LP12 coincidence, the Nelson citation, and the F19-quantifier comparison.

**Required**: Reduce to one sentence stating that F11 is I-side and that the V-side analogue fails under K.μ⁻ (with the Query 5 cross-reference at most once). Move any F19-motivation to F19, where it belongs.

### Issue 5: Overlap between "What We Have Not Specified" and "Open Questions"

**ASN-0099, final two list sections**: Partition tolerance, consistency model, access-control composition, the inverse direction, and querying I-addresses outside `dom(Σ.C) ∪ dom(Σ.L)` each appear in both lists — once as a scope disclaimer, once as a research question.

**Problem**: The two sections restate the same five gaps in two registers. The duplication forces the reader to cross-check that the question list is not introducing new territory.

**Required**: Keep the bare exclusions in "What We Have Not Specified" and let "Open Questions" pose only the genuinely new questions (auditability witness, K.λ-to-appearance time bound, minimum substrate commitment), cross-referencing rather than re-listing the shared items.

## OUT_OF_SCOPE

None. The note stays within link-discovery state, operation, and invariant territory; the deferred items in the closing sections are correctly marked as future work.

VERDICT: REVISE
