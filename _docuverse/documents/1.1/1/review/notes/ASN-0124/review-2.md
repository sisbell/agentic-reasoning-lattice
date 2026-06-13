# Review of ASN-0124

This is an unusually rigorous note. I checked every introduced claim against its derivation and the cited foundations, worked the two load-bearing constructions (FD-NEUT(c), FD-LOSSY) and the worked illustration step-by-step against the K-vocabulary, and verified the composite-validity arguments in FD-FRESH and FD-VDYN. The proofs hold, edge cases are covered (empty regions, empty/fresh documents, full clearance, ghost and link-store addresses in `I`, the `I = ∅` boundary in FD-COOC, first-insertion in FD-FRESH), and the cross-ASN references are all to foundation ASNs. Two issues remain, both at the level of prose precision — but one is an internal inconsistency with a proved lemma, so it must be reconciled.

## REVISE

### Issue 1: FD-LOCAL(ii) "can add members" contradicts FD-FRAME

**ASN-0124, FD-LOCAL, corollary (ii)**: "non-impedance — enlarging the docuverse (new documents, new content, new links, new provenance) can add members but can never remove `d`: the quantity of material not satisfying a request does not impede the answer on material that does."

**Problem**: The four enumerated enlargements are exactly the transitions FD-FRAME *proves* leave the answer fixed: "K.α, K.λ, K.ρ, K.δ … all satisfy `finddocs(I, Σ') = finddocs(I, Σ)`." New content allocation (K.α), new links (K.λ), new provenance (K.ρ), and new documents (K.δ — the Document case adds `d_new` with `M'(d_new) = ∅`, "never a member") add **no** members. The only member-adding transition is content-arrangement extension K.μ⁺ (FD-STEP growth clause), which is absent from the parenthetical. So "can add members" both misleads and stands in direct tension with FD-FRAME. (The load-bearing content — "can never remove `d`" — is sound, following from FD-LOCAL(i).)

**Required**: Drop "can add members," or attribute member-addition to K.μ⁺ explicitly and separate it from the inert `{K.δ, K.α, K.λ, K.ρ}` enlargements the parenthetical lists. The non-impedance principle Nelson cites [LM 4/60] is fully carried by "can never remove `d`."

### Issue 2: FD-COMPLETE misdescribes the quantifier's range

**ASN-0124, FD-COMPLETE**: "The quantifier ranges over the entire document stratum at Σ: every node, every account, every version (each version is its own document entity)."

**Problem**: The formal statement quantifies `d ∈ dom(Σ.M) = E_doc`, which contains only document-level entities (`zeros = 2`). Nodes (`zeros = 0`) and accounts (`zeros = 1`) are in `E` but excluded from `E_doc`, so they are **not** in the quantifier's domain — and FD-V fixes the codomain as `𝒫(E_doc)`, "each member a T4-valid document tumbler (`zeros = 2`, M0)." `finddocs` can never return a node or an account. The gloss lists them as members of the document stratum.

**Required**: Restate the range as `E_doc` only — e.g., "ranges over every document at Σ — every version of every document under every node and account (each version is its own document entity)." The surrounding sentences (no locality/authorship/asker parameter; completeness global by construction) are correct as written.

## OUT_OF_SCOPE

None. The note stays cleanly within the containment query, cites ASN-0127's image layer rather than rebuilding it, and parks the genuinely forward-looking concerns (interior-of-composite coherence behind the FD-SUPER scoping, temporal ordering of provenance, attribution-bearing answers, past-state reach, distributed availability, authority, provenance compaction, multiplicity) in its own Open Questions, where they belong.

VERDICT: REVISE
