# Review of ASN-0108

## REVISE

### Issue 1: The content-position key violates the injectivity that W0 and W1 require

**ASN-0108, "The Enumeration Order" / W6/W8**: W0 records "κ must be injective on [Match]" as a requirement, and W1 states "No two distinct matching links occupy the same enumeration position." Yet the ASN later asserts: "An implementation that orders by matched-content position satisfies W0–W5 but forfeits W6's append guarantee."

**Problem**: A content-position key `κ(a) = (position of the endpoint a matched)` is **not injective on Match**. Two distinct matching links can reference the same content endpoint (same matched span boundary), producing `κ(a) = κ(b)` for `a ≠ b`. This ties them, violating W0's injectivity premise and W1's position uniqueness directly. The implementation evidence makes this concrete: the insertion-sort key is "the matched span's boundary, not the link's identity" — and equal boundaries tie. So the ASN claims a key reading satisfies W0 while that reading contradicts the very requirement W0 imposes, and contradicts W1. Note `After(c,Σ)` uses strict `<_K`, so a tied link is *excluded* — a silent skip distinct from W6's.

**Required**: Either (a) require the key to be a composite that breaks ties by permanent link address (making the content-position reading `κ(a) = (endpoint-pos, a)`, restoring injectivity), or (b) state explicitly that the content-position reading fails W0/W1 absent such a tiebreaker, and correct the "satisfies W0–W5" claim. The choice of key is the ASN's declared central topic, so this is in scope.

### Issue 2: W5's necessity claim ("only if state-stable") is too strong

**ASN-0108, W5**: "Resumption is well-defined across Σ → Σ' *only if* the ordering key is state-stable: ... `κ_{Σ'}(a) = κ_Σ(a)`."

**Problem**: Under the ASN's own model, `After(c, Σ')` is "defined by `κ(c)` alone" with `κ(c)` recomputed at `Σ'` (W8's discussion of keys becoming "irrecoverable when the content is gone" presupposes recomputation). If the key is recomputed, only **relative-order stability among survivors** is necessary, not absolute key invariance. A key that shifts uniformly (e.g. every key `+1`) violates state-stability as defined yet preserves every comparison `κ_{Σ'}(c) <_K κ_{Σ'}(a)`, so resumption stays well-defined. The "only if" therefore asserts a stronger condition than is necessary; absolute invariance is *sufficient*, order-preservation is *necessary*.

**Required**: Restate the necessary condition as preservation of relative `≺`-order among links present in both states (and of the cursor's cut-point), with absolute key invariance presented as the simplest sufficient discipline that the address-based key attains unconditionally.

### Issue 3: W9's exhaustion signal is stated unconditionally but W8 identifies a counterexample

**ASN-0108, W9**: "A window returning fewer than N links signals exhaustion: every matching link reachable past the cursor has been delivered."

**Problem**: W8 itself notes that with a non-state-stable key, an irrecoverable cursor key makes "the successor set collapse and the call returns the empty window — *indistinguishable from genuine exhaustion (W9)*." So an empty/short window does **not** reliably signal exhaustion; it may signal cursor invalidation. W9 is true unconditionally only under a recoverable/state-stable key. As written, W9 over-claims and contradicts the hazard W8 raises.

**Required**: Condition W9 on cursor-key recoverability (equivalently, a state-stable key), cross-referencing W8, so that "short window ⟹ exhaustion" is not asserted in the regime where W8 shows it fails.

### Issue 4: No concrete worked example, and W4's termination clause misdescribes the non-divisible case

**ASN-0108, W4 proof / W9a**: The W4 termination remark says the bound "reaches a value < N after ⌈m/N⌉ windows, after which one more call yields the empty window."

**Problem**: (a) Per the review standards, the ASN works no concrete pagination scenario verifying its key postconditions (e.g. the exact-multiple terminator, or a blind-spot link). The proofs and W9a are entirely abstract. (b) The quoted termination clause is wrong in the non-divisible case: for `m=5, N=2` the third window (ranks `[5]`) is *itself* short, so the reader stops on it — there is **no** extra empty call. The extra empty call occurs only when `N | m`, which is exactly why W9a carries the `[N divides m]` term. The W4 remark thus contradicts W9a's own formula.

**Required**: Add at least one concrete walk — e.g. `m=4, N=2` (full, full, empty-terminator: 3 calls) versus `m=5, N=2` (full, full, short-terminator: 3 calls) — checking W4/W9/W9a numerically; and correct W4's termination clause to match W9a (the trailing empty call is needed only when `N` divides `m`).

### Issue 5: W6's biconditional asserts a backward direction it does not justify

**ASN-0108, W6**: "append-at-tail — *iff* the ordering key is allocation-monotone."

**Problem**: Only the forward direction (allocation-monotone ⟹ append-at-tail) is argued, and it is the only direction the ASN uses. The backward direction (append-at-tail ⟹ allocation-monotone) is unproven and dubious as stated: append-at-tail quantifies over *enumerated matching* links, while allocation-monotonicity is a property of *all* allocated links, so a key could append matching links at the tail without being globally allocation-monotone. A bare "iff" with one direction unsupported is a claim, not a proof.

**Required**: Either prove the backward direction with explicit quantifier scoping, or weaken to the forward implication actually used (allocation-monotone ⟹ append-at-tail).

## OUT_OF_SCOPE

### Topic 1: Global ordering across multiple home documents
**Why out of scope**: The ASN correctly scopes the address-based key's allocation-monotonicity to "a single home document's link allocator" (T9 requires `same_allocator`) and defers the cross-document case to its Open Questions. A globally allocation-monotone key over interleaved document prefixes is new territory for a future ASN, not a defect here.

### Topic 2: Which links match (the satisfaction predicate)
**Why out of scope**: The ASN deliberately imports `Match(q, Σ)` as given and defers the anchoring/satisfaction semantics to the full-set and count operations. This is a sound boundary.

VERDICT: REVISE
