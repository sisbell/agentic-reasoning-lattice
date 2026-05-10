# Regional Review — ASN-0034/Span (cycle 1)

*2026-04-24 10:02*

### Meta-prose paragraph justifies T1 rather than elaborating it
**Class**: REVISE
**Foundation**: (foundation ASN; internal)
**ASN**: T1 (LexicographicOrder) — closing paragraph: "Nelson's assertion that the tumbler line is total — that two addresses are never incomparable — is architecturally load-bearing. Spans are defined as contiguous regions on the tumbler line: 'A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse.' If two addresses were incomparable, the interval between them would be undefined, and the entire machinery of span-sets, link endsets, and content reference would collapse."
**Issue**: This paragraph sits after T1's formal contract and advances no reasoning about the claim. It is the reviser-drift pattern called out in the rubric: new prose around an axiom that explains *why the axiom is needed* rather than what it says, plus an explicit use-site inventory ("span-sets, link endsets, content reference") appealing to downstream machinery — "link endsets" being a future-facing term that has no referent in this ASN. The precise reader must skip past it to reach T3.
**What needs resolving**: Remove the paragraph, or relocate its content to the section introduction where it can frame (not justify) the totality claim without invoking unestablished downstream objects.

### Sub-case (β)/(γ) labels invoked where only ordered-pair (β,γ) matters
**Class**: OBSERVE
**Foundation**: (foundation ASN; internal)
**ASN**: T1 Trichotomy, Case 3 — "Both clauses force `m ≠ n`: (β) gives `m + 1 ≤ n`, hence `m < n` via NAT-addcompat's `m < m + 1`; (γ) gives `n < m` symmetrically."
**Issue**: Case 3 bundles (β) and (γ) but the subsequent argument decides witness direction by which of `m < n` / `n < m` holds, not by whether the first divergence position satisfied (β) or (γ). The labels (β)/(γ) are reintroduced downstream only to derive `m ≠ n`; then the argument re-splits on `m < n` vs `n < m` via trichotomy. This works but makes the reader match two parallel case splits to each other. Soundness is unaffected.

VERDICT: REVISE
