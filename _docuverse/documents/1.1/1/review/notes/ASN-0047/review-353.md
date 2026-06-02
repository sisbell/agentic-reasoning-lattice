# Review of ASN-0047

I read the full transition model, checked the elementary transitions and their frames, the K.μ~ decomposition, the J-couplings, the Class (a)/(b) invariant matrices, and re-derived the concrete tumbler arithmetic in all six worked examples. The technical content is sound: the Bridging lemma, FrontierEquivalence/ChildSpawnFreshness, the D-SEQ★ derivation (both `m=2` and `m≥3`), K.μ~-FIX/RANGE, the φ-bijection fork characterization (including the duplicate-source multiplicity case), and the interior/prior-provenance replacement traces all check out. No correctness gap, no non-foundation cross-references, no implementation drift.

The remaining findings are the meta-prose accretion the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Defensive clause-status prose in K.μ~ admissibility
**ASN-0047, *Decomposition of K.μ~*** (admissibility paragraph): "clause (v) is a genuine defining conjunct, not derivable *from* (i)–(iv) + CL-UNIQ but guaranteed by the full-clearance realization..." and "Clause (iv) is a genuine independent hypothesis, not a consequence of (i)–(iii)..."
**Problem**: This is prose about the *status* of each clause (defending its non-redundancy against an implied objection), interleaved with the definition itself. Per the anti-bloat criteria, this is the "explains why X is needed rather than what it says" pattern. A reader following the admissibility definition must repeatedly parse "genuine ... not derivable from ..." status-claims between the actual conjuncts. The independence *counterexamples* (the link-swap transposition for (v), the cross-subspace transposition for (iv)) are legitimate content and should stay.
**Required**: State each clause once. Move the independence demonstrations to a single short "the conjuncts are mutually independent: [counterexamples]" note after the definition, dropping the "genuine defining conjunct / not derivable / genuine independent hypothesis" framing.

### Issue 2: General proof step deferring to worked examples
**ASN-0047, *Decomposition of K.μ~*, Sufficiency**: "The remaining clauses hold by exactly the reasoning the *link allocation and arrangement* and *fork* worked examples carry out for their K.μ~ swaps — (iv) and (v) because ...; (iii) because ...; (i) because ..."
**Problem**: The clause-by-clause reasons are in fact given inline, so the proof is valid — but the lead-in "by exactly the reasoning the worked examples carry out" is a gratuitous backward reference. Worked examples verify concrete swaps; citing them to discharge a *general* sufficiency claim adds nothing and invites the misreading that the general case rests on examples. This is a use-site pointer decorating prose that already stands on its own.
**Required**: Delete the "by exactly the reasoning the worked examples carry out" clause; keep the inline "(iv)/(v) because ... (iii) because ... (i) because ..." reasons, which constitute the actual argument.

## OUT_OF_SCOPE

### Topic 1: Reordering within the link subspace
K.μ~ fixes every link-subspace V-position pointwise (clause (v) / LRP), so although the ASN brings the link subspace under the ordered D-CTG★/D-MIN★/D-SEQ★ regime, link positions can never be permuted. Whether and how a link subspace may be reordered (and what would motivate the content/link asymmetry) is new territory, consistent with the ASN's existing open question on renumbering-aware interior link withdrawal — not a defect in this ASN.

VERDICT: REVISE
