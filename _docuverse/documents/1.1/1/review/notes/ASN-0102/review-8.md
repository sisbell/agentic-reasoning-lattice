# Review of ASN-0102

This is a careful, deeply-worked note. The wp computation for S3★, the tiling argument in X16, the New/Old split discharging J1★/J1'★, and the strengthened within-reference non-coalescence argument in X8 are all rigorous, and the worked example exercises the non-trivial claims (X8, X11, X12, X16) against concrete values. I checked the boundary cases the guidance flags — `p = 1` (insert before all), `p = n_S + 1` (insert at end), `n_S = 0` (empty subspace), `W ≥ 1` (zero-width excluded), self-transclusion (`d_s = d`) — and each is handled. One genuine precision gap remains.

## REVISE

### Issue 1: P2 establishes `d ∈ dom(Σ.M)`, but the provenance extension and coupling discharges require `d ∈ E_doc`

**ASN-0102, Precondition (P2)**: "`d ∈ dom(Σ.M)`."

**Problem**: The provenance relation is typed `Σ.R ⊆ T_elem × E_doc` (ASN-0047). COPY's effect writes `Σ'.R = Σ.R ∪ {(a_j+i, d)}`, and the entire X14 discharge — J1★, J1'★, P4★ — quantifies over `d ∈ E_doc` (and `E'_doc`). But the only document-membership the precondition supplies is `d ∈ dom(Σ.M)`. The note uses `dom(Σ.M)` and `E_doc` interchangeably ("for each document `d`, an arrangement `Σ.M(d)`" in the setup, then "`d ∈ E_doc`" throughout X14) without stating the bridge. In the integrated ASN-0047 model `dom(M) = E_doc` holds by construction (K.δ's IsDocument case adds `e` to both `E` and `dom(M)` together), but ASN-0102 relies on this identification silently. Without it, the pair `(a_j+i, d)` added to `Σ.R` is not shown to be well-typed, and the J-coupling discharges are not shown to apply to `d`.

**Required**: Either strengthen P2 to `d ∈ E_doc` (and derive `d ∈ dom(Σ.M)` from it), or add one sentence establishing `dom(Σ.M) = E_doc` as a standing identity inherited from the foundation, so that the `Σ.R`-extension is well-typed and the E_doc-quantified couplings are applicable.

## OUT_OF_SCOPE

### Topic 1: Discoverability of links into `d` after COPY changes `ran(M(d))`
COPY enlarges `ran(Σ'.M(d))`, which can make links whose endsets cover the copied addresses discoverable from `d` (ASN-0098 territory). The note's open questions correctly defer this; link semantics are out of scope.

### Topic 2: Re-displacement of copied content by subsequent operations
The first open question (origin-to-discoverability tie under later displacement) belongs to the operation that performs the later displacement (INSERT/DELETE mechanics), not to COPY's contract.

### Topic 3: Cross-temporal divergence of two references to the same content
The third open question (references resolving to differing views across time) is genuinely new territory for a future versioning/derivation ASN.

VERDICT: REVISE
