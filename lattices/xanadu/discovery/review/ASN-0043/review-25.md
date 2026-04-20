# Review of ASN-0043

## REVISE

### Issue 1: L9 ghost address existence argument has a gap

**ASN-0043, L9 (TypeGhostPermission)**: "Choose a fresh ghost address `g ∈ T` with `fields(g).E₁ = s_C` and `g ∉ dom(Σ.C)` (such an address exists: by S7a, every address in `dom(Σ.C)` is allocated under some document's prefix; by T9, allocation within each document's content subspace is strictly increasing; by T0(a), components are unbounded — so a content-subspace address beyond the allocation frontier of every document is always available)."

**Problem**: The existence argument assumes the content subspace has free addresses. T9 gives forward allocation and T0(a) gives unbounded components, but these establish that `T` contains tumblers with arbitrarily large components — not that `T \ dom(Σ.C)` does. L9 quantifies over all conforming states (`A Σ : Σ satisfies L0–L14 ∧ S0–S3`), not just reachable states. The content subspace and `dom(Σ.C)` are both countable; a conforming state with `dom(Σ.C)` covering the entire content subspace is not excluded by any invariant. In such a state, no `s_C`-subspace ghost address exists and the witness fails.

**Required**: Choose `g` in a subspace `s_X` with `s_X ≠ s_C` and `s_X ≠ s_L` (such a subspace always exists: T0(a) gives unbounded first element-field components, and only two values are populated by L0). Then `g ∉ dom(Σ'.C)` by L0 (content occupies `s_C`) and `g ∉ dom(Σ'.L)` by L0 (links occupy `s_L`), unconditionally. The rest of the verification carries through unchanged — the span `(g, δ(1, #g))` is well-formed by T12 regardless of subspace, and no L0–L14 property constrains type endset targets to any particular subspace.

This also affects the parenthetical existence argument for the link address `a` in the same witness ("Allocate a new link address `a` via forward allocation (T9) within `d`'s link subspace") — the same occupancy concern applies to the link subspace. The fix is analogous: allocate under a fresh document prefix (always available since L0 populates only `s_C` and `s_L`, leaving every other subspace empty, and fresh document prefixes exist by T0).

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage belongs in a foundation ASN

PrefixSpanCoverage is a general property of tumbler arithmetic and span denotation — it characterises how unit-depth spans interact with the prefix relation. It depends only on T1, T3, T12, OrdinalShift, and TA-strict (all ASN-0034). Nothing in the statement or proof references links, endsets, or the link store. The result is used here for L10 (type hierarchy) but would equally serve any future ASN that needs to reason about prefix-rooted spans (e.g., content range queries, document subtree selection). Factoring it into a span algebra foundation would make the dependency explicit and let this ASN cite it rather than prove it.

**Why out of scope**: This is a factoring concern, not an error. The lemma is correctly stated and proved; it is just more general than the link ontology.

### Topic 2: S3 / link V-position tension

The ASN correctly derives from S3 + L0 that no arrangement can map a V-position to a link address, making links non-transcludable. It also correctly notes that Gregory's implementation places links in V-positions within a dedicated subspace of the document's permutation matrix, and that "accommodating this in the abstract model would require extending the arrangement semantics beyond S3." This is a genuine tension between the current abstract model and the implementation evidence, but resolving it requires extending S3's domain to include link-subspace V-mappings — a change to the arrangement layer, not to the link ontology.

**Why out of scope**: The ASN's own scope section excludes "POOM structure and V-stream mechanics." The non-transclusion derivation is correct given S3 as stated; the question is whether S3 should be amended, which belongs in a future arrangement ASN.

VERDICT: REVISE
