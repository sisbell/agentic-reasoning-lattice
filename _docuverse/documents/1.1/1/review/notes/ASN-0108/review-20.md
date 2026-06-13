# Review of ASN-0108

## REVISE

### Issue 1: W9b's charge-exhaustiveness omits a tail-entry route

**ASN-0108, W9b (CumulativeInflowSufficiency)**: "the events come in three kinds — (1) the initial tail elements at the first call, (2) fresh matching links created ahead of the cursor (D-NONMONO's `K.λ` case), and (3) *links that orphaned (W7; LP17 of ASN-0098) and then resurrected (LP18 of ASN-0098) ahead of a cursor*." And: "The charge is well-defined and exhaustive: a delivered link sits in `After(c, Σ)`, and it entered that tail as an initial element (kind 1), by creation ahead of the cursor (kind 2), or — having been delivered before and thereby dropped below the advancing cursor — by resurrecting ahead of a later cursor (kind 3)."

**Problem**: The three-kind enumeration is not exhaustive, so the "exhaustive" claim that anchors the per-link multiplicity bound is unestablished. Consider a link `L` created by `K.λ` *before* the windowing begins, whose endsets reference content not yet in any consulted arrangement — a born ghost (permitted by L4/L9, ASN-0043; not discoverable by LP17, ASN-0098). At the first call `L ∉ Match` (so not kind 1). It is not created during windowing (so not kind 2). It was never a member, so it never "orphaned (W7)" and was never "delivered before" — so it is not kind 3 as the charge explicitly scopes it. Then a `K.μ⁺` step during windowing adds `M(d)(v) = a*` with `a* ∈ coverage(L's endset)` (the LP18 mechanism, but applied to a never-discoverable link), placing `L` into the tail and yielding a delivery the charge cannot route.

The *theorem* survives — the underlying definition ("any single transition that places a link into the reachable tail") does count this entry, and one such delivery is charged to one such event (1 ≤ 1). But the *proof's* exhaustiveness step, which routes every tail entry through kinds 1/2/3, is what fails. This is precisely the "three operations preserve, therefore all do" pattern the standards forbid: a fourth route is exhibited.

**Required**: Either broaden kind 3 to "links that become discoverable ahead of a cursor (LP18 mechanism), whether or not previously a member" — dropping the `(W7)` / "delivered before" qualifiers — or state explicitly that the three kinds are illustrative and that the charge's exhaustiveness rests on the *definition* of tail-inflow event, not the taxonomy.

### Issue 2: W4 derives and recaps W9a's count formula

**ASN-0108, W4 proof**: "for the constant schedule `N_i = N` it is `⌈m/N⌉ + [N divides m]` (the extra `+1` precisely when `N | m`), matching W9a, which states its count formula for the fixed-N case." And the post-proof paragraph: "only the closed-form count of W9a presumes a fixed `N`. The completeness W4 advertises is thus available for the full flexibility W11 grants."

**Problem**: The closed-form `⌈m/N⌉ + [N divides m]` appears inside W4's proof and again as W9a's headline claim — the same formula in two slots. W4's termination obligation needs only "terminates in finitely many calls" (which the strictly-increasing `S_i` argument supplies); the count belongs to W9a. The post-proof paragraph then makes a *third* pass over the same point (variable-schedule independence + the W9a count) and adds forward references to W9a (now cited twice within W4) and W11. This is forward-reference accretion: a structural slot (W4's proof) carrying W9a's content plus a recap that re-defers downstream.

**Required**: Cut the inline closed-form derivation in W4's proof to "terminates in finitely many calls (count: W9a)"; fold the variable-schedule-independence observation into one sentence rather than the proof-plus-recap pair.

### Issue 3: W5's "same hazard" parenthetical overgeneralizes

**ASN-0108, W5, second walk**: "(Equivalently: re-evaluated at the cursor `z` the reader actually held, the same event reads as a clause-1 crossing of `w` below `z` — the two clauses are the same hazard viewed at successive cursors, which is precisely why W5 must demand both at every cursor the pass uses.)"

**Problem**: The equivalence is true for the walk's pair only because `z` happens to become the next cursor. Clause 2 quantifies over *every* pair in `After(c, ·)`, including pairs neither member of which ever becomes a cursor; clause-1-at-cursors does not constrain those. So clauses 1 and 2 are *not* "the same hazard" in general — clause 2 is genuinely stronger than clause-1-applied-at-cursors, which is exactly why W9d can later carve out clause 2 as separately dispensable for termination. The parenthetical generalizes from one pair (cursor-involving) to a blanket equivalence that does not hold, leaving the reader unsure whether clause 2 adds anything. The precise reader has to reconcile this aside against W9d's contrary treatment.

**Required**: Restrict the claim to the walk's situation (the reordered pair includes the next cursor, so *there* it reads as a clause-1 crossing), or drop the "the two clauses are the same hazard" generalization.

### Issue 4: W6 and W6a carry removable defensive meta-prose

**ASN-0108, W6**: "We claim only this forward direction, which is the one the analysis below uses. We do *not* assert the converse (append-at-tail ⟹ allocation-monotone), and it does not hold in general: append-at-tail quantifies only over the *enumerated matching* links, whereas allocation-monotonicity is a property of *all* allocated links..."

**ASN-0108, W6a**: "The earlier 'addresses are not reused' argument reaches only the address key; the `K.λ` frame argument is what discharges the universal across both."

**Problem**: The W6 sentence is a defensive scope disclaimer about an unused converse; the W6a sentence inventories *which* argument covers *which* key rather than advancing W6a's claim. Both match the flagged anti-bloat patterns (defensive justification; argument inventory). The reader skips past them to follow the claim. The matching-vs-all-allocated distinction is genuine but not load-bearing for any guarantee here.

**Required**: Delete the converse disclaimer in W6; in W6a, keep the `K.λ`-frame justification and drop the meta-sentence comparing the two arguments' reach.

## OUT_OF_SCOPE

The author's six Open Questions (multi-document keys, eventual delivery under non-monotone keys, cross-call completeness invariant, empty-vs-irrecoverable cursor disambiguation, delivery-vs-count correspondence, partition stability across mutation) are correctly deferred — each names territory a future ASN must open, not a gap in this one. W10's deferral of the cardinality query and the count operation is likewise appropriately scoped out. No mis-scoping found.

META: none — the ASN defines an operation (windowed retrieval) and its abstract guarantees, parameterized by the ordering key rather than fixed to one index, and stays on the system-guarantee side throughout.

VERDICT: REVISE
