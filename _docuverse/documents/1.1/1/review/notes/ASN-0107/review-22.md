# Review of ASN-0107

## REVISE

### Issue 1: R2's endpoint-removal mechanism ignores the canonical-prefix contraction discipline
**ASN-0107, R2 (ContentDeletionUnbounded)**: "Deleting an endpoint shared by `k` links can drop up to `k` links from the discovery count in one operation: `Δnum_disc ∈ {−k, …, 0}`" ... "Contracting an arrangement so as to remove that endpoint."
**Problem**: K.μ⁻ retains only canonical prefixes per subspace (`R = ⋃{[S,1,…,1,k] : 1 ≤ k ≤ n'_S}`, PerSubspaceContractionScope, ASN-0047) — it can drop *trailing* positions only. To remove the consulted V-position(s) mapping to an endpoint `a` sitting at a non-maximal position `[S, j]`, the operation must set `n'_S < j`, which deletes `[S, j], [S, j+1], …, [S, n_S]` — every later endpoint too. So "removing that endpoint" alone is generally impossible; collateral removal of trailing endpoints is forced, and those collateral removals can drop links beyond the `k` that reach `a`. R2 as written assumes a surgical single-endpoint removal that the contraction discipline forbids except when `a` is arrangement-maximal. R1 correctly carries this constraint as (P-max); R2 drops it.
**Required**: Condition R2 on `a` being the arrangement-maximal consulted endpoint, or restate the bound in terms of the set of endpoints actually removed by the canonical-prefix contraction (and the union of links reaching any of them), consistent with R1's (P-max).

### Issue 2: Repeated deferrals to the retrieval operation across three sections
**ASN-0107, State and Counting Request / W1 / Open Questions**: "returning the matched links is out of scope here"; W1: "Recovering *which* links matched requires a different operation — one that returns the links — and that operation is out of scope here"; Open Questions Q3 references "the corresponding retrieval operation."
**Problem**: Three paragraphs in different sections defer to the same downstream operation — the accretion pattern flagged for this note. The deferral adds nothing after the first statement.
**Required**: State the out-of-scope boundary once (the existing Scope section already names FINDLINKS/ASN-0099); remove the repeated deferrals.

### Issue 3: Reviser drift — meta-prose justifying preconditions and a non-necessity digression
**ASN-0107, R1 (P-uniq)**: "Under content sharing (M13/S5) a retained position `[S, j]` with `j < n_S` could also map `a`; this precondition excludes that case, which otherwise lands in the `Δ = 0` branch below."
**ASN-0107, D2 (reordering clause)**: "This is *not necessary*: because arrangements may map distinct V-positions to the same I-address (content sharing, M13/S5), a reorder that permutes positions within each shared-image class — without carrying a distinctly-imaged position across the `Wᵢ` boundary — leaves the image set unchanged though it does not fix `Wᵢ` setwise."
**Problem**: The P-uniq sentence explains *why the precondition is needed* and forward-references "the `Δ = 0` branch below" rather than stating what the precondition is. The D2 digression establishes a sufficient/non-necessary refinement that does not advance the non-monotonicity claim D2 carries. Both are the meta-prose-around-preconditions accretion pattern.
**Required**: Drop the P-uniq rationale sentence (the precondition stands on its own); cut or compress the D2 non-necessity aside to the operative fact (a reorder that moves a distinctly-imaged position across the `Wᵢ` boundary changes `Qᵢ`).

### Issue 4: R5 restates E4 and D2 without adding content
**ASN-0107, R5 (ConservationConditional)**: "Conservation of the count is anchoring-conditional: against a fixed permanent `Q` it holds (E4), and under discovery anchoring it fails (D2)."
**Problem**: R5 is a one-sentence synthesis that says exactly what E4 (existence conservation) and D2 (discovery non-monotonicity) already say. It is the "two paragraphs say the same thing in different words" pattern.
**Required**: Fold R5's content into the E/D section transition or remove it; it earns its own claim label only if it asserts something E4 and D2 do not.

### Issue 5: "Withdrawn link" terminology contradicts the no-retraction model
**ASN-0107, D3**: "A *withdrawn* link is never removed from `dom(Σ.L)` … but ceases to be reachable through the consulted arrangement."
**Problem**: R1 establishes "No store-level link retraction exists." Using "withdrawn link" invites the reading that the model has a withdrawal action on links, when the actual mechanism is arrangement contraction severing a link's *endpoints* from the consulted document. The link is never withdrawn; the content it references leaves the view.
**Required**: Replace "withdrawn link" with language naming the actual mechanism (e.g., "a link whose endpoints have left the consulted arrangement").

## OUT_OF_SCOPE

### Topic 1: Independently-anchored multi-document requests
The first Open Question (each request part anchored to a different evolving document) is correctly deferred; the conjunctive cross-document semantics it would require is new territory, not a gap in this ASN.

VERDICT: REVISE
