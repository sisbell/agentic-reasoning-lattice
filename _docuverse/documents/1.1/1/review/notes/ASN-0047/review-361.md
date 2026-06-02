# Review of ASN-0047

I checked the transition model against the foundation invariants, traced every elementary transition's frame and precondition, and verified the worked examples' invariant checks. I could not find a correctness defect in the core argument: the five-component permanence hierarchy, the K.δ case split, the K.μ~ decomposition, J4's φ-bijection characterization, and the Class (a)/(b) split are sound, and the boundary cases the standard checklist demands (empty document, full clearance, zero-extension insertion, self-transclusion, duplicate-I-address fork) are each either handled or correctly routed to an operation-level open question. The findings below are the duplicate/essay-prose patterns the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Duplicated nested-node T4-legality justification (SSGU and CrossNodeAccountBase)
**ASN-0047, NodeRootedForest (SSGU) and CrossDocEntityDisjoint (CrossNodeAccountBase)**: SSGU writes "*Nested nodes* (WLOG `N ≼ N'` with `#N < #N'`, the configuration NodeBaptism permits since multi-component node tumblers are T4-legal)"; CrossNodeAccountBase repeats "the case NodeBaptism does *not* forbid, since multi-component node tumblers are T4-legal (`zeros = 0`, `t₁ ≠ 0`, `t_{#t} ≠ 0`, so e.g. `N₁ = [1,2] ≼ [1,2,3] = N₂`)" and then re-runs the same zero-separator-at-`#N+1` divergence argument.
**Problem**: The same justification (node tumblers may nest because multi-component nodes are T4-legal) and the same divergence mechanism appear in two sections. CrossNodeAccountBase already says "this is exactly the zero-separator divergence proved in SSGU ... instantiated at `a := b_account(N₁)`," so the re-justification of T4-legality and the re-statement of the example are redundant.
**Required**: In CrossNodeAccountBase, keep the instantiation pointer to SSGU and delete the re-derived T4-legality clause and worked `N₁=[1,2] ≼ [1,2,3]` example; cite SSGU for the nesting permission rather than re-establishing it.

### Issue 2: Near-verbatim duplication of the structural inc-chain derivation in C1c and L1c
**ASN-0047, Class (a) verification, *C1c* and *L1c* paragraphs**: Both paragraphs open with identical boilerplate ("Every `a ∈ dom(C)` / `ℓ ∈ dom(L)` must be reachable from a T4-valid document-level seed `s` ... by a *structural inc-chain* with `k₁ = 2` ...") and both carry the verbatim sentence "licensing the step under TA5a's `k = 1 ∧ zeros(t) ≤ 3` clause — the boundary case, admissible but exactly tight."
**Problem**: The L1c chain is the C1c chain plus one extra `inc(·,0)` step to reach the `s_L` anchor; the two derivations are otherwise word-for-word identical, including the per-step `kᵢ`-conformance enumeration and the "boundary case, admissible but exactly tight" remark. This is two paragraphs saying the same thing.
**Required**: Collapse to one shared derivation (the content/link chains differ only in the `s_C`-anchor vs. `b_C(d)→b_L(d)` step and `s_C`/`s_L`), stating the link case as "the content chain of C1c with one additional `inc(·,0)` to seat the `s_L` anchor," rather than reproducing the entire argument.

### Issue 3: Editorial flourishes in structural slots
**ASN-0047, *Destruction confinement***: "P3 makes the confinement vivid. Every destructive state change — every removal, every reordering — is confined to the presentational layer." and, under J2, "This is the deepest consequence of the design."
**Problem**: These sentences restate, in evaluative/essay register, what the formal P3 statement and its proof already establish; they do not advance the reasoning. The substantive content (the monotonicity conjuncts, the per-transition case analysis) is already complete without them.
**Required**: Delete the evaluative sentences; retain the formal statement, the proof, and the one load-bearing observation that deletion is purely presentational (which is cited to Gregory and carries verifiable content).

## OUT_OF_SCOPE

### Topic 1: Interior link/content withdrawal with renumbering
The model's K.μ⁻ contracts only by suffix removal, so an interior V-position cannot be withdrawn while preserving D-CTG★/D-MIN★. This is correctly already listed as an Open Question and is an operation-level concern (DELETEVSPAN is out of scope); it is not an error in this ASN.

META: not applicable — the ASN defines state, abstract transitions, and their invariants, and confines implementation references (POOM, granfilade, `docreatenewversion`) to motivating evidence, so it remains a specification, not implementation mechanics.

VERDICT: REVISE
