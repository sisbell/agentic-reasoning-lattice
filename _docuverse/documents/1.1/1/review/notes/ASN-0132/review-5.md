# Review of ASN-0132

The note is a model of disciplined specification: it defines the count *through* `sat` rather than subordinating it to the enumeration (CN-SHARED), keeps the operation read-only and abstract, marks every implementation note as evidence-not-spec, and explicitly *declines* to make cost-asymmetry a correctness obligation. The worked example checks out address-by-address (I verified `coverage(F)` holds ordinals 5–12, that every d₂-prefixed address exceeds the upper bound at component 5, that `nullified(Σ) = {a₂}`, and that both home-bound variants resolve as claimed). The wp in CN-MONO is genuinely non-trivial and correctly carries the "not born already-retracted" conjunct from FL-WP(a), with the unit-depth collapse argument (via R0a's prefix antichain) sound. I found one precision defect.

## REVISE

### Issue 1: "forking copies content" mischaracterizes the very mechanism CN-UNIT(d) depends on

**ASN-0132, Claims-Introduced table, CN-UNIT row**: "version-refraction multiplicity (the latter three excluded by CN-LOC; **forking copies content, not links** — J4 ASN-0047 — so the version DAG adds no link address)"

**Problem**: J4 (ForkComposite, ASN-0047) does **not** copy content. Its only content-side step is K.μ⁺ via `φ`, with `M'(d_new)(φ(v)) = M(d_op)(v)` and the derived `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}})` — the new version's arrangement maps new V-positions onto the **same** existing I-addresses. There is no K.α step in J4; no new content address is allocated. In this spec's foundational vocabulary, that is *transclusion/sharing* (same address, shared identity), the opposite of *copy* (new address, independent content).

This is more than cosmetic. The paragraph's own argument — "a link to one version is a link to all versions" realized as appearance multiplicity — *requires* sharing: a link homed at the source surfaces in `d_new` precisely because `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d_new)) ≠ ∅`, and that intersection is non-empty only because the I-addresses are shared, not copied. If forking actually *copied* content to fresh addresses, the source's link would not reach the new version, and CN-UNIT(d) would fail. The table cell asserts the one thing that would break the claim it summarizes.

The body gets this right twice — CN-UNIT(b) calls transclusion "shared by reference," and CN-UNIT(d) itself says each version is "sharing the source's content I-addresses" — so the table cell is also internally inconsistent with the prose it indexes.

**Required**: Change "forking copies content, not links" to "forking shares content (references the same I-addresses), not links" — or equivalently "forking populates the new version's arrangement over the content subspace from the source's existing I-addresses (J4 has no K.α step), not links." The load-bearing conclusion ("so the version DAG adds no link address") is unaffected and correct.

## OUT_OF_SCOPE

No additional items. The note's own Open Questions section already defers the legitimately downstream concerns — the V-spec/I-address count invariant, cross-inquiry concurrency, count caching, fragmentation conformance, count-vs-enumeration cost, and federated counts — without smuggling any of them in as claims. The existence/discovery taxonomy is *applied* (CN-ORPHAN), not rebuilt, so ASN-0127's layer is cited rather than re-derived as the scope requires.

VERDICT: REVISE
