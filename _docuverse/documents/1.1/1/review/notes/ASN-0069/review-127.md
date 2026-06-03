# Review of ASN-0069

## REVISE

### Issue 1: V8 perpetuity claim asserts a derived guarantee without derivation
**ASN-0069, §"Structural Correspondence", closing sentence**: "The intercomparison guarantee is *perpetual*: V8 holds in the post-fork state, and its consequences propagate to every subsequent state in which neither side has overwritten the relevant V-positions."

**Problem**: This is the load-bearing payoff of the whole correspondence account — that "word-for-word" intercomparison works *forever*, not just at fork-time. It is the one substantive consequence in the ASN stated as a one-line assertion with no derivation. V8 itself is proved only at the post-fork state; the forward-time propagation rests on two unnamed premises: (i) inherited I-addresses persist with unchanged value in `dom(C)` across every subsequent state (P0 / ContentPermanence), and (ii) a given V-position retains its mapping until that specific document's arrangement is modified at that position (per-document frame V5a, and K.μ⁻'s retention semantics for *which* positions survive a contraction). Neither is cited. The reviewer standard "derived guarantees stated without derivation — name the premises, show the chain" applies directly: the most important consequence in the section is the least justified.

**Required**: Either (a) promote perpetuity to a named property with an explicit derivation — for every `v ∈ V_{s_C}(d_op)` and every state `Σ''` reachable from the post-fork state in which no transition is M-targeted at `d_op` or `d_new` at position `v`, `M''(d_op)(v) = M''(d_new)(v)`, derived from V8 + P0 (address/value persistence) + V5a (position retention) — or (b) recast the sentence explicitly as an informal observation and drop the word "guarantee," so it is not read as a derived result.

## OUT_OF_SCOPE

### Topic 1: Semantics of repeated forks chaining off the latest version rather than `d_src`
A subsequent fork of `d_src` takes its content operand `d_op = max(dom(A_v(d_src)))` (the prior version), not `d_src` — so the second "version of `d_src`" transcribes the *first version's* edited content, not the original's. The ASN faithfully applies J4's operand-tracking rule and handles this correctly (V10(b), worked example). Whether that operand-selection semantics is the intended reading of CREATENEWVERSION is a question about J4 (ASN-0047, foundation), not this ASN.

**Why out of scope**: The behavior is fixed by foundation J4; ASN-0069 applies it consistently and documents the consequence honestly. No revision to this ASN is warranted.

VERDICT: REVISE
