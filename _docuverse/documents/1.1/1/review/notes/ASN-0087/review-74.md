# Review of ASN-0087

## REVISE

### Issue 1: Per-subspace invariants D-CTG★, D-MIN★, D-SEQ★ discharged only for the link subspace at `d`

**ASN-0087, Invariant Preservation → Per-State Invariants**: The D-MIN★ discharge opens "we must show `min(V_{s_L}^{Σ'}(d)) = [s_L, 1, ..., 1]`"; D-SEQ★ and D-CTG★ likewise reason only about `V_{s_L}^{Σ'}(d)`.

**Problem**: D-CTG★, D-MIN★, and D-SEQ★ are universally quantified over all `(d', S)` with `V_S(d') ≠ ∅` (ASN-0047). The proofs address exactly one conjunct: the modified link subspace at the home document `d`. The content-subspace conjunct at `d` (e.g. in the worked example `V_{s_C}(d) = {[1,1],[1,2]} ≠ ∅`, so `min(V_{s_C}(d)) = [s_C,1]` is a live D-MIN★ obligation) and every conjunct at `d' ≠ d` are never explicitly discharged. They hold trivially — `V_{s_C}(d)` is frame-fixed and `M'(d') = M(d')` for `d' ≠ d` — but the batch-inheritance sentence near the end of the section covers only invariants "quantifying solely over `C`, `E`, `R`, or the document set `dom(M)`," which excludes these arrangement-indexed invariants. The review standard "Every invariant conjunct addressed" is not met for the unmodified subspace/documents.

**Required**: For each of D-CTG★, D-MIN★, D-SEQ★ (and to be parallel, S2/S8a as set-level claims), add an explicit one-line note that the content-subspace conjunct at `d` and all conjuncts at `d' ≠ d` are preserved by frame (`V_{s_C}(d)` unchanged; `M'(d') = M(d')`), so only the `s_L`-at-`d` conjunct requires argument.

### Issue 2: Redundant restatement of foundation definitions and a repeated mechanism/actual distinction

**ASN-0087, "What Is Indexed?"**: the `project` and `discoverable_from` definitions are re-typeset verbatim from ASN-0098 before LP12 is invoked.

**Problem**: These are foundation (ASN-0098) definitions; restating them in full rather than citing-and-applying is the kind of accreted redundancy the anti-bloat pass targets. Separately, the mechanism-vs-actual-discoverability point is made three times in near-identical words — "The Problem" ("The discoverability *mechanism* and *actual* discoverability are distinct…"), the head of "What Is Indexed?", and again in the M-NoIndexState conclusion. Two of these paragraphs say the same thing and the reader must re-confirm no new content was added.

**Required**: Cite the ASN-0098 `project`/`discoverable_from` definitions instead of re-typesetting them, and state the mechanism-vs-actual distinction once (it belongs with M-NoIndexState, where it does work), removing the duplicate prose.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets and limiting cases of permanently-unallocated type addresses
The Open Questions list (constraints on endsets referencing not-yet-allocated I-addresses; discoverability when a type endset references an address that will never be allocated) is correctly deferred — these concern an authoring-discipline ASN, not MAKELINK's transition semantics.

### Topic 2: Protocol-level atomicity of the composite
The visibility bound on the intermediate state `Σ_mid` is explicitly assigned to "the protocol layer above the substrate" and is genuinely a future-ASN concern, not a defect here.

VERDICT: REVISE
