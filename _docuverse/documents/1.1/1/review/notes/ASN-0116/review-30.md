# Review of ASN-0116

## REVISE

### Issue 1: P5 (DocumentIsolation) is false for documents with link-subspace arrangements

**ASN-0116, P5 (DocumentIsolation) and the isolation paragraph preceding it**: "For every `d' ≠ d` ... for every `v' ∈ dom(M(d'))`, `M'(d')(v') ∈ dom(C')` with `C'(M'(d')(v')) = C(M(d')(v'))`." And in the proof: "`ran(M(d')) ⊆ dom(C)` (S3) ... so `A_new ∩ ran(M(d')) = ∅`."

**Problem**: The note explicitly works "inside ASN-0047's extended state `Σ = (C, L, E, M, R)`," where an arrangement may contain link-subspace V-positions that map into `dom(L)`, not `dom(C)` (S3★, GeneralizedReferentialIntegrity, which *supersedes* S3 for the extended state). Three consequences:

1. P5's boxed claim `M'(d')(v') ∈ dom(C')` is false for any `v'` in `d'`'s link subspace — such a `v'` resolves into `dom(L)`, and `C'` is undefined there.
2. The asserted `ran(M(d')) ⊆ dom(C)` is wrong; the correct bound is `ran(M(d')) ⊆ dom(C) ∪ dom(L)` (via S3★).
3. The disjointness argument invokes only `A_new ∩ dom(C) = ∅` (P0), leaving `A_new ∩ dom(L) = ∅` unaddressed — even though it holds (K.α's whole-store freshness, `a ∉ dom(C) ∪ dom(L)`, which the composite section already establishes but P0/P5 do not wire in).

The isolation *conclusion* survives, but a boxed claim and its proof are stated incorrectly for link-bearing documents.

**Required**: State P5 per-subspace (`subspace(v') = s_C ⟹ M'(d')(v') ∈ dom(C')` with content-value preservation; `subspace(v') = s_L ⟹ M'(d')(v') ∈ dom(L')` with link-value preservation via F-LINK); cite S3★ rather than the superseded S3; and discharge `A_new ∩ ran(M(d')) = ∅` from K.α's whole-store freshness (`A_new ∩ (dom(C) ∪ dom(L)) = ∅`), not from `A_new ∩ dom(C) = ∅` alone.

### Issue 2: Same S3-vs-S3★ imprecision in the left/shifted referential-integrity discharge

**ASN-0116, "The document remains one coherent sequence" (left and shifted regions)**: "each left or shifted position carries an I-address `M(d)(v) ∈ ran(M(d)) ⊆ dom(C)` (S3 at the pre-state)."

**Problem**: Same root defect. The note cites the superseded S3 (ASN-0036) while operating in ASN-0047's extended state, and writes the false blanket `ran(M(d)) ⊆ dom(C)` (`d` also carries link-subspace positions mapping into `dom(L)`). The application to content-subspace left/shifted positions is sound, but the citation and the range bound are wrong as written.

**Required**: Cite S3★ and restrict the bound to content-subspace positions (`subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)`), which is what the argument actually uses.

### Issue 3: Duplicated interval-disjointness fact under two names

**ASN-0116, Effect ("block-disjointness fact") and "The document remains one coherent sequence" ("Three-interval fact")**: the Effect states "the three index intervals `{1, …, J-1}` (left), `{J, …, J+n-1}` (block), and `{J+n, …, N+n}` (shifted suffix) are consecutive and pairwise disjoint"; the coherence section restates "The three index intervals are consecutive ... and pairwise disjoint, their union being `{1, …, N+n}`."

**Problem**: This is one fact stated twice in different words under two labels — the anti-bloat pattern "two paragraphs in the same document say the same thing in different words." Both I-SHIFT, I-LEFT, I-DOM (Effect) and the contiguity/single-valuedness arguments (coherence) lean on it, accreting a second statement.

**Required**: State the interval fact once (with its `union = {1,…,N+n}` and `0 < J ≤ N+1` derivation) and reference that single statement from both sites.

### Issue 4: Rhetorical "This is the answer to X" framings recur as essay scaffolding

**ASN-0116, multiple sites**: "This is the answer to *what is allocated to hold the new material*"; "Here is the answer to *what relationship the displaced positions bear to the prior arrangement*"; "This is also the answer to *how the insertion sits within the V-stream as a connected region*"; "This is the answer to *what relationship the displaced positions bear*."

**Problem**: Under the active anti-bloat classifier, these echo the opening problem-framing back at the reader without advancing the claim being proved — essay content threaded through the technical prose. The substantive sentences they attach to (the actual allocation/shift statements) carry the content on their own.

**Required**: Drop the framing clauses; keep the technical statements they precede.

## OUT_OF_SCOPE

The four Open Questions (transclusion of a shared position, concurrent insertion without a serializing authority, transclusion provenance, post-edit fragmentation of the inserted run) are correctly deferred — transclusion, concurrency/replication, and later editing are future-ASN territory, not gaps in INSERT. No action needed.

VERDICT: REVISE
