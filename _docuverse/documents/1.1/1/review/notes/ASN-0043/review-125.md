# Review of ASN-0043

## REVISE

### Issue 1: L11a's shared-home argument asserts `s_L ≠ 1` without grounding
**ASN-0043, L11a — LinkUniqueness (shared-home case)**: "The base `d.0.1` carries subspace identifier `1` at position `#d + 2`, whereas every link carries `s_L` there (L0) **with `s_L ≠ 1`**; reaching the link subspace is therefore possible only by sibling-advancing at depth 1 up to `d.0.s_L` before any descent."

**Problem**: The parenthetical `s_L ≠ 1` is invoked as a fact to justify that the depth-1 sibling sweep from `d.0.1` to `d.0.s_L` is mandatory. But nothing in the stated invariants grounds it. The note fixes only `s_C ≠ s_L` (Subspace Residence section), and the first subspace produced by `inc(d, 2)` is always identifier `1` (TA5, `k>0` appends `[0,…,0,1]`). The constants `s_C`, `s_L` are abstract: `subspace_I` for I-addresses (element-field projection) is decoupled from ASN-0036's `subspace` for V-positions, so no invariant forces content into subspace 1. If `s_C = 2` and `s_L = 1`, then `s_L = 1` and the quoted premise is false. Notably, the L9 Case A construction is written to be robust to this ("applied `s_L − 1` times" → 0 sweeps when `s_L = 1`), but the L11a prose is not — it presents the sweep as forced via `s_L ≠ 1`.

The theorem's *conclusion* survives `s_L = 1` (the sweep is vacuous; both chains still share `inc(d, 2)` and the second spawn `inc(d.0.1, 1)`), but the *justification as written* rests on an ungrounded premise.

**Required**: Either ground `s_L ≠ 1` from a stated invariant/convention (e.g., that subspace 1 is the content subspace `s_C`), or restructure the step so it holds with a vacuous sweep when `s_L = 1` (as L9 already does), rather than asserting `s_L ≠ 1` as a fact.

### Issue 2: L11a carries a roadmap/preview sentence that does not advance the argument
**ASN-0043, L11a (opening of shared-home case)**: "A link address has element field beginning with the link-subspace identifier `s_L` and depth `#E ≥ 2` by L1b; **the argument that follows traces shared edges of 𝒯 and terminates with `a₁`, `a₂` as descendants of one shared link-ordinal allocator, whatever the element-field depth.**"

**Problem**: The bolded clause previews what the subsequent three numbered steps will establish ("the argument that follows traces… and terminates with…"), then the same conclusion is restated again at the end of the case ("In either case `a₁` and `a₂` are genuine allocation events of the one tree 𝒯… descendants of the single shared link-ordinal allocator whatever the element-field depth"). This is the forward-reference accretion the note's `review-mode.anti-bloat` classifier flags: a meta-preview that the precise reader must skip past, duplicating the case's own conclusion line.

**Required**: Delete the preview clause; the numbered steps and their closing sentence already deliver the conclusion.

## OUT_OF_SCOPE

### Topic 1: Extending content-side disjointness beyond the `s_C`-resident slice
The note scopes `dom(Σ.L) ∩ dom(Σ.C) = ∅` to the `s_C`-resident slice (L0a) and records the general case as an Open Question.
**Why out of scope**: Fixing a global content-subspace constant is a content-store invariant (ASN-0036 territory), not a link-model defect; the scoping is explicitly acknowledged and the link-side guarantees are derived correctly within it.

VERDICT: REVISE
