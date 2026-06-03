# Review of ASN-0071

## REVISE

### Issue 1: Post-hoc coverage justification embedded in the worked scenario

**ASN-0071, "A worked scenario" (multi-address and cross-depth queries)**: 
- "The resolve-equivalence of the Resolution section is thus checked against a concrete multi-block arrangement with a shared I-address across blocks, **not merely asserted**."
- "The set-flattening absorbs the duplicate a₁ ... — **the dedup step that the singleton query left untested**"
- "the empty/non-empty intersection distinction is **genuinely tested**, since neither references what the other does"
- "**confirming the subtree-capture intent against a concrete result set rather than stopping at the abstract** `⟦σ⟧ ∩ dom = n positions`."

**Problem**: These sentences do not advance the computation — they are reviewer-facing claims *about what the example covers* ("not merely asserted," "genuinely tested," "left untested"). This is exactly the exhaustiveness/defensive-justification accretion the anti-bloat pass targets. The computations themselves (the actual `resolve`, the set-flattening, the per-document predicate evaluations) are the content and stand on their own; the reader following the math does not need to be told that a case was thereby "tested."

**Required**: Delete the coverage-justification clauses. Keep the concrete computations; drop the meta-commentary asserting that they demonstrate coverage.

### Issue 2: Motivational meta-prose framing the added queries

**ASN-0071, "A worked scenario"**: 
- "The singleton query Q resolves to one I-address, so it cannot exercise partial overlap ... We construct a second query whose resolution carries two I-addresses..."
- "Every document above has common content depth m_C = 2, so the cross-depth subtree capture (#u < m) cannot be exercised against an actual arrangement — it requires a deeper source. We extend the construction with one depth-3 document..."

**Problem**: This is "the prior example left X untested, so we add Y to test it" reasoning — reviewer-defense narration of why each example exists, not exposition the reader needs. The examples are valuable; the framing that justifies their addition is accretion of the same shape as Issue 1.

**Required**: Present the second and third queries directly (e.g., "A multi-address query: take `Q_D = ...`") without the "cannot be exercised, so we construct" justification.

### Issue 3: PC's defensive relationship-to-C0a framing

**ASN-0071, "The query"**: "This is the relaxed analogue of ASN-0058's C0a (which assumes well-formedness), proven here directly from the vspec preconditions `subspace(u) = s_C` and `actionPoint(ℓ) = #u ≥ 2`, **with no appeal to well-formedness**."

**Problem**: The clause "proven here directly ... with no appeal to well-formedness" is a defensive justification of the proof's method rather than a step in it. The proof that follows already shows the derivation from preconditions; stating in advance that it avoids well-formedness adds nothing the proof does not show.

**Required**: Reduce to the load-bearing fact (PC is the relaxed analogue of C0a; the proof below derives it from the vspec preconditions), and drop the "with no appeal to well-formedness" defense.

### Issue 4: F-SHARE / "Discovery through sharing" restates F-COMP / F-PART

**ASN-0071, "Discovery through sharing" + F-SHARE**: "`a ∈ iaddrs(Q)(Σ) ∧ a ∈ ran(Σ.M(d)) ∧ d ∈ Σ.E_doc ⟹ d ∈ find(Q)(Σ)`" (basis: "direct from F-find").

**Problem**: F-SHARE is a sufficient-condition specialization of F-COMP/F-PART — a single shared `a` makes the intersection non-empty, which F-PART already states biconditionally. Its opening prose ("A query discovers every document that shares its resolved content") repeats "Partial overlap suffices." The genuinely new content in this section is the `origin(a)` home-vs-transcluding recovery; the rest duplicates the preceding section.

**Required**: Either fold the cross-document-discovery claim into F-PART/F-COMP and keep only the origin-recovery material as distinct, or justify why F-SHARE states something F-PART does not. As written it is a fourth "direct from F-find" unfolding with overlapping prose.

## OUT_OF_SCOPE

None beyond what the ASN already defers in Open Questions (the current-containment vs. `R` relationship, vspec-rejection policy, and contraction-transition invariant are correctly parked there).

VERDICT: REVISE
