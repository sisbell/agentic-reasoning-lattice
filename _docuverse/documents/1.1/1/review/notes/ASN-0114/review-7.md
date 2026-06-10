# Review of ASN-0114

This note is, on the whole, carefully built. F0–F8 are stated as abstract guarantees that an alternative implementation would have to satisfy; the derivations of F2 and F5 are mostly honest about their gaps (F5 in particular correctly identifies the single-step/multi-step gap between L12 and LP13 and cites the foundation lemma rather than hand-waving it); the worked instance discharges exactly the two claims a reader cannot check abstractly. The note has not drifted into implementation mechanics — no META. The findings below are real but local.

## REVISE

### Issue 1: Open Question 3 is already answered by F7
**ASN-0114, Open Questions**: "What invariant must distinguish, to a caller, a valid empty endset from an absent link, when both yield no positions?"
**Problem**: F7 (EmptyVersusInvalid) *is* this invariant. F7 explicitly routes a valid selector over an empty end to `⟨⟩` and routes `a ∉ dom(Σ.L)` (an absent link) to `⊥`, asserts `⟨⟩ ≠ ⊥` as "distinct return categories," and states "An implementation that collapses these two cases is incorrect." So the note already supplies, as a mandatory claim, the very invariant the open question presents as unresolved. Listing it under Open Questions contradicts F7.
**Required**: Remove the question, or reword it to identify what (if anything) remains *beyond* F7 — e.g., a question about how the `⟨⟩`/`⊥` distinction survives across a serialization or protocol boundary, which F7 (a statement about abstract `Σ`) does not address.

### Issue 2: Use-site inventory in the "Status of the result" paragraph
**ASN-0114, after F0 ("Status of the result — a relation")**: "wherever it appears as a single term inside `coverage(·)` (F5, F6, F8), that term is well-defined because F3 makes coverage independent of which witness is chosen."
**Problem**: The parenthetical enumeration `(F5, F6, F8)` is a downstream-consumer inventory — bookkeeping that names where the well-definedness fact will later be used rather than advancing the fact itself. This is exactly the accretion pattern the `review-mode.anti-bloat` classifier flags. The substantive content ("`coverage(followlink(...))` is well-defined because all F1-witnesses share a coverage, by F3") stands without the use-site list.
**Required**: Strike the `(F5, F6, F8)` inventory; state the well-definedness once and let the downstream claims rely on it implicitly.

### Issue 3: F5's "load-bearing" paragraph restates one point three times with defensive framing
**ASN-0114, after F5's derivation**: "We must not overstate what is load-bearing here. … Content-identity addressing is therefore not load-bearing for F5's coverage equality. … So L12 is what F5 needs; content-identity addressing is what makes F5's coverage-permanence mean material-permanence — a reading F5 does not formally state. … Either way, the result's coverage is permanently tied to the same link and the same selector."
**Problem**: The paragraph carries exactly one substantive distinction — coverage-permanence rides on L12 alone, while content-identity addressing is what upgrades it to *material*-permanence (a reading F5 does not formalize). That distinction is then asserted at least three times, wrapped in defensive meta-prose ("We must not overstate what is load-bearing here"). A precise reader has to skip the restatements to extract the single point. This is the meta-prose accretion the anti-bloat classifier targets.
**Required**: Reduce to the one distinction in one or two sentences (L12 ⟹ coverage-permanence; content-identity addressing is what makes "same coverage" mean "same material," which F5 does not formally claim). Drop the "we must not overstate" framing and the closing "Either way…" restatement.

### Issue 4: F2's proof excludes the singleton but not the empty result
**ASN-0114, F2 derivation**: "So if `R` were the singleton `⟨σ⟩` with `⟦σ⟧ ⊇ {p, r}`, then `q ∈ ⟦σ⟧ = coverage(R)`, yet `q ∉ coverage(eᵢ)` — contradicting F1. Hence a faithful `R` over a disconnected end must comprise two or more spans."
**Problem**: The conclusion is `|R| ≥ 2`, but the argument as written only rules out `|R| = 1`. To reach `|R| ≥ 2` you also need `R ≠ ⟨⟩`, i.e. `|R| ≥ 1`. That step is omitted. It is immediate — disconnectedness supplies `p, r ∈ coverage(eᵢ)`, so `coverage(eᵢ) ≠ ∅`, and by F1 `coverage(R) ≠ ∅`, forcing `R ≠ ⟨⟩` (ASN-0053 S2: only `⟨⟩` has empty coverage) — but a proof that claims `|R| ≥ 2` should close both the `0` and `1` boundaries explicitly rather than only the `1` boundary.
**Required**: Add the one-line exclusion of `R = ⟨⟩` (disconnected ⟹ non-empty coverage ⟹ `|R| ≥ 1`) before concluding `|R| ≥ 2`.

## OUT_OF_SCOPE

None. The note correctly fences resolution-against-a-document, link search/creation/editing, and replication out (the "recorded end versus its resolution" section and the Open Questions cover the boundary), and defines no claims that drift into that territory.

VERDICT: REVISE
