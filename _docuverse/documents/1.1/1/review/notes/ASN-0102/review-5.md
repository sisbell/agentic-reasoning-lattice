# Review of ASN-0102

## REVISE

### Issue 1: ExtendedReachableStateInvariants discharge omits S8★ and S4
**ASN-0102, X14 (final paragraph)**: "The arrangement-side Class (a) conjuncts are exactly those established above: S2 and S8a (X16), S3★ and S3★-aux (the wp computation), D-CTG★/D-MIN★/D-SEQ★ (X16 …), S7a–S7d/S8-fin/S8-depth/C-fin …"
**Problem**: The note claims complete discharge of ExtendedReachableStateInvariants (ASN-0047), whose Class (a) conjunction explicitly includes **S8★** (PerSubspaceSpanDecomposition) and **S4** (OriginBasedIdentity). Neither is mentioned. S8★ is not vacuous: COPY rewrites `M(d)|_{s_C}` (copied + displaced classes), so the content-subspace arrangement's decomposition into correspondence runs must be re-established at the post-state — exactly the kind of "hard conjunct" that gets skipped. S4 is trivially preserved (no allocation) but is still an unaddressed member of the enumeration the note claims to exhaust.
**Required**: Add explicit discharge of S8★ for `M(d)|_{V_{s_C}(d)}` at `Σ'` (the post-state arrangement is functional, finite, contiguous, common-depth `m` — so S8★'s correspondence-run decomposition applies, with `B_copy` plus the displaced/unmoved runs as witnesses), and name S4 as preserved by `dom(Σ'.C) = dom(Σ.C)` (X1).

### Issue 2: S8a established only for copied positions, not displaced positions
**ASN-0102, X16**: "every copied position … does: `zeros = 0`, depth `m ≥ 2`, and all components positive … all post-state `s_C`-positions sharing depth `m` (S8-depth) …"
**Problem**: X16 proves S8a in detail only for the copied positions `v + c`. The displaced positions `u + W = shift(u, W)` are new keys in `dom(Σ'.M(d))` and must independently satisfy S8a (and depth `m`) for S2 well-definedness and S8-depth to hold; this is asserted ("all post-state `s_C`-positions sharing depth `m`") but not derived. The fact is one step from foundations (OrdShiftHom (c): shift preserves S8a unconditionally; `#shift(u,W) = #u = m`), but the proof states the conclusion without the citation.
**Required**: Cite shift's S8a- and depth-preservation for the displaced class, so all three V-position classes are shown S8a-compliant before concluding S2/S8-depth.

### Issue 3: X8 descends into implementation mechanics beyond the abstract guarantee
**ASN-0102, X8**: "The POOM side (`docopy` → `insertpm`) *does* coalesce such a boundary: `insertcbcnd` widens an existing crum in place exactly when `isanextensionnd`'s twin gates both pass … The spanfilade side (`insertspanf`) has no such extension mechanism … the POOM crum count drops below `k` while the spanfilade entry count stays at `k`."
**Problem**: The abstract, implementation-independent guarantee is "constructed count `k`, canonical (maximally-merged) count `≤ k`, equality iff no inter-reference boundary is I-adjacent." That is sound. The remainder describes which concrete index (POOM crum count vs. spanfilade entry count) realizes which value — a property of one implementation, not a system guarantee an alternative implementation must satisfy. Worse, it surfaces a divergence (POOM realizes `≤ k`, spanfilade realizes `k`) without resolving which is the abstract truth, conflating the abstract arrangement with the implementation's containment index.
**Required**: Reduce X8 to the abstract claim (constructed `k`, canonical `≤ k`, the I-adjacency equality condition). Move the POOM/spanfilade index-divergence observation to implementation evidence/commentary, or drop it; the abstract state commits only to the arrangement, not to two competing concrete fragmentation counts.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content by later operations
**Why out of scope**: The first Open Question (origin/discoverability invariants when copied content is later displaced) concerns interaction with INSERT/DELETE/REARRANGE applied after COPY — operation mechanics excluded by the stated scope, and properly a future ASN.

### Topic 2: Time-varying views of the same content reference
**Why out of scope**: The third Open Question (two references required to resolve to differing views across time) introduces version/view semantics not part of COPY's state transition; belongs to a later note on versioning/views.

VERDICT: REVISE
