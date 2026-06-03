# Review of ASN-0070

I read the note as a pure-query specification: `R(d,e)` (inverse image), the `follow` operation, the canonical-form theorem, and a catalogue of derived properties, validated against six worked configurations. The mathematics is sound — I checked the F-canonical existence/uniqueness argument (the consecutivity characterisation, both inclusions in Step 1's `k = m` case, and the left/right-closure gap arguments in Step 4), the F-subspace biconditional, the F-contig contiguity claim, and the P-depth reduction in the worked examples. All hold. Edge cases (empty arrangement, empty endset, type slot, multiplicity, cross-subspace straddle, interior-offset clip) are exercised. My findings are confined to the anti-bloat patterns the classifier flags.

## REVISE

### Issue 1: "Design grounding (Nelson)" is a motivational catalog in a structural slot
**ASN-0070, Derived Properties (opening paragraph)**: "Several of these lemmas are the structural form of design commitments Nelson states informally. F-det realises... F-origin realises... F-state realises... F-multidoc realises..."
**Problem**: This paragraph is essay content that explains *why* four lemmas matter rather than advancing any claim. Its form is a use-site inventory — "lemma X realises Nelson commitment Y" enumerated four times — placed at the head of the Derived Properties section. This is exactly the "essay content in structural slots / explains why rather than what" accretion pattern. It also partially overlaps the per-lemma design prose already carried inline (e.g. F-empty's "There is no exception, no error, no fallback"; F-multidoc's home-document remark), so the motivation lives in two places.
**Required**: Remove the consolidated catalog. If a specific Nelson commitment is load-bearing for a single lemma (e.g. F-origin's native/transcluded indistinguishability), fold that one sentence into that lemma's prose; drop the rest.

### Issue 2: Frame slot replicated verbatim across every derived-property lemma
**ASN-0070, F-det / F-sound / F-complete / F-empty / F-multi / F-slot / F-origin / F-state / F-multidoc / F-contig**: each repeats "**Frame.** No state modification." (F-subspace/F0: "State-pure").
**Problem**: `follow` is a pure query and F-frame (INV) establishes `Σ' = Σ` once. The derived properties are consequences, not operations; restating state-purity on each is boilerplate the reader skips. Roughly a dozen identical Frame lines carry no information past F-frame.
**Required**: State once (e.g. at the head of Derived Properties) that all derived properties inherit F-frame's state-purity, and drop the per-lemma Frame slots, or retain it only where a lemma observes a cross-transition property (F-persist, F-state) for which the distinction is non-trivial.

## OUT_OF_SCOPE

### Topic 1: Multi-home resolution, concurrency, and transclusion-lineage relationships
**Why out of scope**: These are correctly parked in the note's own Open Questions section and concern future operations/protocol semantics, not this query's specification. No action needed.

VERDICT: REVISE
