# Review of ASN-0099

## REVISE

### Issue 1: Duplicate Nelson LM 2/46 citation, same quote and point, in two sections
**ASN-0099, "The Reader's Question" and "Local Atomicity"**: opening — "backlink discovery ... must be answerable on demand (Nelson, *Literary Machines* 2/46: 'without appreciable delay')"; Local Atomicity — "Nelson's design intent at LM 2/46 — backlinks returnable 'without appreciable delay' — is the reader-experience commitment behind this atomicity."
**Problem**: The identical citation and quote carry the identical point in two places — the "two paragraphs say the same thing" pattern. The second occurrence adds no reasoning the first did not.
**Required**: Keep the motivating quote in the opening; drop it from Local Atomicity, where the operative content is SequentialTransitionAxiom, not the Nelson gloss.

### Issue 2: F11 and F19 repeat the same "V-side analogue is not a theorem" aside
**ASN-0099, F11 and F19**: F11 — "the V-side analogue — fixing (R, d) and quantifying across edits — is not a theorem of this ASN and could not be, since K.μ⁻ can shrink ran(Σ.M(d)) (Query 5 below exhibits the divergence concretely)." F19 — "the V-side analogue would fix (R, d) and quantify across edits, which K.μ⁻ invalidates."
**Problem**: The same observation (V-side fails under K.μ⁻ contraction, divergence shown in Query 5) is stated twice in different words across two sections. Both defer to Query 5.
**Required**: State the I-side/V-side asymmetry once (at F11, the persistence claim), and have F19 cite it rather than re-derive the aside.

### Issue 3: F4 framing and "realizability discharge" are accreted justification prose
**ASN-0099, "The Match Predicate" / F4**: "The witnesses below carry the load... The witnesses below exhibit this for three strengthenings and two weakenings of F1's per-endset overlap test." And: "*Realizability discharge.* The disagreement is always realizable: K.λ admits, at any state with dom(Σ.M) ≠ ∅, a link of arity N ≥ 3 ... so every F1-admitted (endset configuration, I) pair is realizable..."
**Problem**: The claim F4 asserts ("any predicate disagreeing with F1 is a different operation") is near-tautological. The five fully-derived witnesses are concrete and have individuation value, but the surrounding exhaustiveness framing ("three strengthenings and two weakenings") and the general "realizability discharge" paragraph are meta-prose justifying the predicate choice rather than advancing the operation's definition — the reader must skip past them to reach the concrete witnesses.
**Required**: Keep the concrete witnesses; cut the "carry the load" framing and collapse the general realizability paragraph into a single clause (the I-set is a query parameter, endsets are K.λ-free, hence every witness is realizable).

### Issue 4: "Reflection" section is design-rationale essay restating established motivation
**ASN-0099, "Reflection"**: "The specification is spare because of design choices established for other reasons. Because links attach to bytes (L13)... Because bytes carry permanent identity (S0, C0)... Because arrangement is separated from content identity... None of these were established for discovery; discovery falls out of them."
**Problem**: This litany advances no claim — it re-narrates motivations already carried by F5, F6, F8, F19 and the cited foundations. Essay content in a structural slot.
**Required**: Reduce to at most one sentence, or remove; the substantive consequences (identity-not-value, arrangement-independence, monotonicity) are already theorems above.

## OUT_OF_SCOPE

### Topic 1: FOLLOWLINK / RETRIEVEENDSETS (inverse direction)
**Why out of scope**: The ASN correctly lists resolving result endsets back to V-positions as unspecified; that is a separate operation, not a gap here.

### Topic 2: Out-of-store query semantics, partition tolerance, consistency model, access-control composition
**Why out of scope**: Each is named under "What We Have Not Specified" as future territory; absence of coverage is intentional, not an error.

The proofs themselves are sound: F13/F20/F20a distributivity chains, F9/F9-λ single-step exhaustion of V's impact, F12 factoring, and the six worked queries are all correct and well-bounded (empty query, empty store, empty constraint/target/scope, out-of-range slot, link-subspace image all handled). The findings above are prose accretion, not logical defects.

VERDICT: REVISE
