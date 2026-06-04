# Review of ASN-0100

This ASN is technically thorough and, on the substance, correct: the three-effect decomposition, the substrate composite (n K.α + optional K.μ⁻ + K.μ⁺ + n K.ρ), the per-state/composite-boundary atomicity split, the full invariant sweep (S2, S3★, S4, S7/C1b/C1c, S8★ via C1a, D-CTG★/D-MIN★/D-SEQ★, L0 content clause, P0–P8, J0/J1★/J1'★), the two wp analyses, and the three worked examples all check out, including boundaries (j=0, j=N append, empty document, empty-arrangement-vs-fresh-allocator sub-case). The closed-interval reduction for D-CTG★ at m ≥ 3 and the INS.chain-shift derivation (inc(·,0) = shift(·,1) from T4-validity) are genuinely complete, not hand-waved.

The findings below are the accretion patterns this review mode is charged to surface. They are prose/organization issues, not correctness defects — but they are real, and per the rubric any REVISE item yields a REVISE verdict.

## REVISE

### Issue 1: Atomicity-location cross-reference accretion
**ASN-0100, §Atomicity**: "This is the single prose statement of the definitional-atomicity claim; the Formal Contract refers here, and INS.atomicity catalogs it."
**Problem**: This sentence advances no reasoning — it is pure document-organization bookkeeping that the reader must skip to follow the argument. It is the keystone of a three-way coordination about *where* composite atomicity is stated: the Formal Contract's "Composite atomicity" paragraph defers with "(the argument is given once in §Atomicity)", the INS.pre claim row defers with "(Composite-level atomicity is not a precondition; see INS.atomicity)", and §Atomicity then points back at both. This is exactly the "multiple paragraphs defer to the same downstream location" / "prose justifies document ordering" pattern.
**Required**: Delete the self-referential cataloging sentence. Keep the object-level content (composite atomicity is definitional under ValidComposite★ because the elementaries form a contiguous transition sequence) stated once in §Atomicity; drop the coordinating pointers in the Formal Contract and INS.pre, or reduce to a single neutral cross-reference.

### Issue 2: Use-site / downstream-consumer annotations in claim bodies
**ASN-0100, §The Operation: Formal Contract (INS.M-exhaustive paragraph)**: "The S2 functionality argument (§Arrangement functionality) cites this clause."
**Problem**: This enumerates a downstream consumer of the clause rather than advancing the clause's content — the flagged "definition's introduction enumerates downstream consumers" pattern. (Compounded by the fact that S2 functionality does not actually require exhaustiveness: pairwise-disjoint, single-valued regions establish functionality regardless of whether a fourth region could exist, so the citation overstates the dependency.) Similar consumer-pointing annotations recur, e.g. §Cross-document independence stating the projection-invariance claim then deferring its proof to "§Coverage and link discoverability (the d' ≠ d case)."
**Required**: Drop the "cites this clause" annotation; let the consuming section invoke the clause by label without the carrier announcing its consumers. Either inline the short cross-document derivation where the claim is stated or move the claim to where it is proved, rather than splitting statement from proof across sections.

## OUT_OF_SCOPE

The ASN correctly bounds DELETE, COPY, REARRANGE, link-subspace insertion (K.μ⁺_L), version derivation, and BEBE replication out of scope (§Bounding the Scope, §INSERT vs COPY), and the Open Questions are appropriately deferred. No misclassified in-scope content was found.

VERDICT: REVISE
