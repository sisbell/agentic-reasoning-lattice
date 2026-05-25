# Review of ASN-0069

## REVISE

### Issue 1: V1's subsequent-fork case extends J4 without explicit acknowledgment

**ASN-0069, "What Must Be Constructed" and V1**: "The composite is J4 of ASN-0047, named *ForkComposite*. We adopt it as the structural skeleton..." and later "V1 (*new-version identity*): A fork of `d_src` produces a new entity `d_new` allocated as `A_v(d_src)`'s next emission per the Allocator hierarchy (ASN-0047): *First fork of `d_src`* ... `d_new = inc(d_src, 1)`, produced by K.δ case (ii) with `k = 1`, `t = d_src`. *Subsequent fork of `d_src`* ... `d_new = inc(d_prev, 0)`, produced by K.δ case (ii) with `k = 0`, `t = d_prev`."

**Problem**: J4 of ASN-0047 specifies clause (i) strictly as "K.δ case (ii) with k = 1 and t = d_src, producing `d_new = inc(d_src, 1)` with `d_new ∉ E_doc`." This covers only the first fork. V1's subsequent-fork case (k=0 with t=d_prev) is a genuine extension of J4 not contemplated by its text — the K.δ sub-case differs (sibling generation rather than version-spawning), the operand differs (d_prev rather than d_src), and the result differs. The ASN explicitly frames V7's empty-source case as an extension ("We frame V7 as an *extension* of J4"), but does not similarly frame the subsequent-fork case. The reader is left to infer that V0 generalizes J4 along two dimensions simultaneously without parallel acknowledgment.

**Required**: Add an explicit framing parallel to V7's, stating that V0 generalizes J4's clause (i) to admit subsequent forks via `inc(d_prev, 0)` (K.δ case (ii) at k=0, t=d_prev), citing ASN-0047's Allocator hierarchy convention for A_v(d_src) as the basis for the extension.

### Issue 2: K.δ sub-case A freshness argument cites unnamed foundation property

**ASN-0069, "The Fork Composite" verification**: "By T10a's allocator discipline applied to `A_v(d_src)` (ASN-0047's Allocator hierarchy), `d_new = inc(d_src, 1)` is `A_v(d_src)`'s first emission; T10a.6 (DomainDisjointness, ASN-0034) makes its domain disjoint from every other allocator's, and the per-allocator chain-advancement uniqueness places the first emission outside any other allocator's range, so `d_new ∉ E`."

**Problem**: "Per-allocator chain-advancement uniqueness" is not a named foundation property. T10a.7 (EnumerationInjectivity) supplies within-allocator injectivity but does not directly supply first-emission freshness. The freshness `inc(d_src, 1) ∉ E` for sub-case A requires citing T10a's at-most-once-per-(t, k') child-spawning constraint explicitly: each parameter pair yields at most one event, so if no prior K.δ at (k=1, t=d_src) has fired (the V1 sub-case A predicate), then `inc(d_src, 1) ∉ E`. The K.δ uniform precondition `e ∉ E` then holds.

**Required**: Replace "per-allocator chain-advancement uniqueness" with an explicit citation to T10a's at-most-once-per-(t, k') child-spawning constraint, and connect this to the sub-case A predicate "A_v(d_src) has emitted no prior version" to show why this implies freshness.

### Issue 3: V8b is informal but makes precise claims requiring formal grounding

**ASN-0069, V8b**: "If after the fork either `M(d_src)` or `M(d_new)` is modified by K.μ⁻ (removing V-positions) or K.μ~ (reordering), the correspondence holds only over V-positions still present in both arrangements with their original mappings. Insertions into either side (K.μ⁺) introduce V-positions absent from the other, where correspondence fails by domain incompatibility."

**Problem**: V8b is stated as a corollary but its substantive claim — that correspondence under post-fork editing reduces to V-positions surviving in both arrangements — is not formally established. The claim is intuitively correct (it follows from V5a's bidirectional independence plus per-document frame discipline) but the reader cannot verify it from the prose alone. The "structural test V8 captures the correspondence *given the current state of each arrangement*" sentence acknowledges the temporal indexing but does not state the corollary precisely.

**Required**: Either (a) formalize V8b as a precise claim with derivation — e.g., "for any state Σ_g reachable from the post-fork state Σ_f, the correspondence holds over `{v ∈ V_{s_C}(d_src) : v ∈ dom(M_g(d_src)) ∩ dom(M_g(d_new)) ∧ M_g(d_src)(v) = M_g(d_new)(v)}`, with V5a establishing that each side's modifications do not propagate to the other" — or (b) drop V8b's specific operational claims (K.μ⁻, K.μ~, K.μ⁺) and replace with a single observational remark that correspondence is state-relative.

## OUT_OF_SCOPE

None. The Open Questions section appropriately lists topics for future ASNs (concurrent forks, fork discoverability, snapshot vs living forks, transcludent sources, etc.). The ASN's chosen scope — characterizing the fork composite as a state transition — is internally coherent.

VERDICT: REVISE
