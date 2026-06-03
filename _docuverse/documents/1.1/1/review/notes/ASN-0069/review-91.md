# Review of ASN-0069

## REVISE

### Issue 1: V5a's two "corollaries" are trivial self-admitted instantiations, one with a vestigial label
**ASN-0069, §"Frame: Source Isolation", V5a Corollary 2**: "For any two distinct documents `d¹, d² ∈ E_doc` and any subsequent sequence `Σ' →* Σ''` in which no step is M-targeted at `d¹`: `M''(d¹) = M'(d¹)`. This is V5a instantiated at `d* = d¹`."

**Problem**: Corollary 2 is, by its own admission, V5a instantiated at `d* = d¹`. The second label `d²` never appears in either the hypothesis or the conclusion — it plays no role, yet the "pairwise independence" framing implies a genuine two-document result. Corollary 1 ("Symmetric for `d* = d_new`") is likewise just V5a at `d* = d_src` / `d* = d_new`. Both corollaries add no content over the general V5a statement; they exist only to give V10(b) and V12 something named to cite. V10(b) then spends a long paragraph ("Direction 1 … instantiate Corollary 2 at `(d¹, d²) = (d_new², d_new¹)` … Direction 2 … by the same argument with operands swapped") unpacking what is a one-line instantiation. This is named-sub-result accretion.

**Required**: Drop the two corollaries (and the unused `d²` label). Have V10(b) and V12 cite V5a directly as "V5a at `d* = …`". Collapse V10(b)'s Direction 1 / Direction 2 walk-through to a single sentence noting both directions are V5a instantiated at the respective `d*`, valid because `d_new¹ ≠ d_new²` (V10(a)).

### Issue 2: B8 uniqueness is established twice
**ASN-0069, §"Identity by Sub-Allocation"**: "(iii) distinct emissions of one namespace are distinct addresses under a single authority by B8 (Uniqueness)…"
**ASN-0069, §"Identity by Sub-Allocation", V2 "Address uniqueness" consequence**: "B8 (Uniqueness, ASN-0040) supplies the address-distinctness guarantee directly: cross-namespace baptisms produce distinct addresses unconditionally, and same-namespace baptisms produce distinct addresses under a single authority — so no two forks … share a tumbler."

**Problem**: The B8 transfer is performed in the opening paragraph (item iii) and then re-explained, more fully, in V2's "Address uniqueness" consequence — two paragraphs in the same section delivering the same B8 result. The V2 version legitimately adds the freshness (`e ∉ E`) and permanence (T8) framing, but the cross-namespace/same-namespace clause restatement is redundant with item (iii). It also sits under V2 ("prefix-encoded ancestry"), which is about `≼`, not uniqueness.

**Required**: State B8 once. Keep the freshness + T8-permanence framing in the V2 consequence but cite the already-established B8 transfer rather than re-expounding both of its clauses; or move the uniqueness consequence out from under V2 (which is an ancestry claim).

### Issue 3: V1's closing sentence is navigational meta-prose
**ASN-0069, §"Identity by Sub-Allocation"**: "V1 instantiates J4's allocation-and-operand-tracking rule directly — the k=1 branch on a first fork, the k=0 branch on a subsequent fork; the one deviation, literal inheritance, is V4."

**Problem**: This sentence relates V1 to J4 and forward-points to V4 without advancing any reasoning — the k=1/k=0 dispatch is already stated in the V1 box itself, and "the one deviation … is V4" is a navigation cue. It is the "relate-to-foundation-clause-and-point-downstream" filler the anti-bloat pass targets.

**Required**: Delete the sentence. The V1 box already carries the dispatch; V4 introduces itself.

## OUT_OF_SCOPE

The Open Questions section appropriately defers concurrency, snapshot-vs-living forks, transcludent sources, and version-space coherence to future ASNs; no scope violations to flag. The substantive proofs (V1 inductions, V4/V4b, V6a's two-direction set equalities, V11's chain induction, the ValidComposite★ verification including the empty-source K.δ-alone branch) are complete and the boundary cases (empty source, fork-of-fork, sibling forks, link-bearing source) are all covered.

VERDICT: REVISE
