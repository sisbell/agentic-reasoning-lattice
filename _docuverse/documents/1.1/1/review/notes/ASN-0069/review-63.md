# Review of ASN-0069

## REVISE

### Issue 1: Σ-superscript notation explained twice
**ASN-0069, V0 "Composite structure" paragraph and "Notation for the verification" paragraph**: Both paragraphs explain the same distinction — parenthesised `Σ^{(j)}` for intra-composite sub-states versus unbracketed `Σ¹…Σ^k` for post-composite end-states ("intentionally typographically distinct…", "intentionally distinct from V10's and V11's…").
**Problem**: Two paragraphs in different sections say the same thing in different words — the flagged duplication pattern. The reader meets the full convention in V0, then again verbatim-in-substance at the verification.
**Required**: State the convention once (at the verification, its point of use) and delete the V0 restatement.

### Issue 2: Reviser drift — imagining a precondition-excluded case
**ASN-0069, "The Fork Composite" verification, K.δ sub-case A freshness step (ii)**: "A K.δ event at `(t = d_src, k' = 2)` is inadmissible to begin with… violating the precondition. *Even were such an event admissible*, TA5(d) at `k = 2` would produce…"
**Problem**: The paragraph first establishes the case is excluded by precondition, then argues a length-distinctness fallback for a case it just ruled out. This is the "imagines a case the claim's precondition already excludes" pattern.
**Required**: Drop the "even were such an event admissible" sub-argument; the precondition exclusion is sufficient.

### Issue 3: V5a corollaries enumerate downstream consumers
**ASN-0069, V5a Corollary 1 and Corollary 2**: "the form consumed by V10(b) for sibling forks (`d¹ = d_new¹`, `d² = d_new²`)"; "The corollary also underwrites V11's first premise-scope remark… V11 takes its premise as a hypothesis… and Corollary 2 supplies the operational discharge…"
**Problem**: A general lemma's body inventories its use sites rather than advancing the lemma. The downstream-consumer enumeration belongs at the use sites (which already cite V5a), not inside V5a.
**Required**: State V5a and its corollaries as standalone frame facts; remove the "consumed by / underwrites" use-site catalog.

### Issue 4: Document-construction justification and forward pointer to adjacent prose
**ASN-0069, V2 derivation and V4**: V2: "We nonetheless re-derive it by induction… because the length identity… is reused by V11a's recovery argument; the induction is retained for that by-product, not to re-establish the prefix relation J4 already gives." V4: "The structural justification for this choice — and the alternatives ruled out — appears immediately after V4's statement below."
**Problem**: V2's sentence justifies why a derivation is present in the document (construction rationale, not reasoning). V4's sentence is a forward pointer to the paragraph immediately following it.
**Required**: Delete the V2 retention-rationale sentence (just present the derivation). Delete V4's pointer-to-next-paragraph.

### Issue 5: Alternative-ASN speculation does not advance the claim
**ASN-0069, V4 and V4b**: "We note that an alternative ASN could weaken V4 to admit rebased V-positions or rearranged correspondences, provided it strengthened V8 with explicit correspondence tables. Such an ASN would still satisfy J4… The choice made here is to keep the correspondence relation structurally implicit…"
**Problem**: Essay about hypothetical alternative specifications. The design commitment and its two structural justifications ("Why V-positions are not rebased", "Why I-addresses are not rebased") already establish the choice; the counterfactual-ASN paragraph is meta-prose.
**Required**: Remove the alternative-ASN speculation; retain only the two structural justifications.

### Issue 6: Paragraph-length entries in the Properties Introduced table
**ASN-0069, Properties Introduced table, rows V5a, V8b, V6a**: Each entry runs ~60–100 words restating the full claim with its corollaries and per-transition qualifications (e.g., V8b: "let `F := …` and `Π_g := …`; then… K.α, K.λ, K.ρ, K.δ, K.μ⁺_L, and third-document K.μ⁻/K.μ⁺ (and the K.μ~ composite they form) each leave `Π_g` invariant").
**Problem**: A summary table carrying essay content in a structural slot. The table should index claims, not re-prove them.
**Required**: Reduce each entry to a one-line statement; the body holds the detail.

### Issue 7: V8b non-monotonicity remark over-proves a negative
**ASN-0069, V8b "Non-monotonicity" paragraph**: The remark establishes that `Π_g` "need not decay monotonically," then exhaustively proves invariance of `Π_g` under K.α, K.λ, K.ρ, K.δ, K.μ⁺_L, and third-document K.μ⁻/K.μ⁺/K.μ~ (multi-step traces (i)–(iv) for K.μ⁺_L).
**Problem**: Accreted exhaustiveness. The load-bearing content of V8b is (i) the set bound and (ii) initial coverage; the remark's claim is that witnesses can leave and re-enter only via K.μ⁻/K.μ⁺ on the two documents. The full per-transition invariance proof for every other kind is disproportionate to a "need not decay monotonically" remark.
**Required**: Reduce to the operative statement — only K.μ⁻/K.μ⁺ targeting `d_op` or `d_new` can move `Π_g`; all other elementary kinds frame `M` and so fix `Π_g`. Drop the kind-by-kind expansion.

### Issue 8: Empty-arrangement vignette preamble is a use-site inventory
**ASN-0069, "Worked Example", "*Empty-arrangement cases (V7)*" preamble**: "The next two vignettes illustrate V7's K.δ-alone composite across two configurations… and together verify four properties: (i)… (ii)… (iii)… (iv)…" followed by inline "(i)"–"(iv)" back-references in the vignettes.
**Problem**: Scaffolding that catalogs what the examples will show before showing them — meta-organization, not reasoning. The vignettes already state which properties they exercise.
**Required**: Remove the enumerated preamble and the "(i)"–"(iv)" cross-references; let each vignette state its checks inline.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork during source modification
**Why out of scope**: The first Open Question (guarantees beyond the sequential atomic transition axiom under concurrency) is genuinely new territory — a concurrency model this ASN does not introduce. Correctly deferred.

### Topic 2: Snapshot vs living fork distinction
**Why out of scope**: Distinguishing frozen-at-fork-time arrangements from arrangements tracking the source's current state requires invariants this ASN does not define; it is a separate operation/semantics question, not an error here.

META: The ASN remains within specification territory — it defines a state transition, its preconditions/effects/frame, and invariants stated abstractly enough to bind any implementation; the findings are accreted meta-prose, not drift.

VERDICT: REVISE
