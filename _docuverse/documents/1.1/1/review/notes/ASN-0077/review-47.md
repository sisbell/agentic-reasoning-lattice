# Review of ASN-0077

I read every proof in this ASN with the foundation contracts open beside it. The pointwise machinery (O0, O5), the I-span and V-span lifts, the singleton I-span case analysis, the equivalence chain (F1)≡(F2)≡(F3), the O11/O11′/O11★★ extension lemmas with their O11.1 well-formedness corollary, and the O13/O14 negative claims with their worked witnesses all check out. The case analyses are complete (the #b<#a / #b=#a / #b>#a split in the singleton case is airtight, the modifies-M(d) / leaves-M(d)-fixed binary partition genuinely avoids vocabulary-enumeration), the edge cases are addressed (empty intersection, empty arrangement, empty-restriction, link subspace, cross-subspace), and the wp(SHOWORIGIN_I,|result|=1) analysis is the non-trivial one the standards demand.

I found one issue: an internal inconsistency between the closing prose and the proven claims.

## REVISE

### Issue 1: Summary over-claims permanence in a way O6 and O14 contradict
**ASN-0077, Summary (final paragraph)**: "every byte names its home, every span reveals its sources, and the answer never changes once given."
**Problem**: "the answer never changes once given" is true only for the *pointwise* origin of a fixed address (O5/O5★). At the span level the ASN itself proves the opposite: O6/O6★ (Monotonic growth) show an I-span's reported set *grows* as content is allocated, and O14 (K.μ~ non-preservation) exhibits a V-span whose answer changes to an *incomparable* set under reordering (`{d₁}` → `{d₃}`). The opening framing ("it must give one answer, and the same answer in every state of the system") has the same slack — a multi-origin span returns a set, not "one answer," and the V-span set is arrangement-dependent. The body resolves this correctly via O5 (pointwise) vs. O6/O7/O13/O14 (span-level), but the summary sentence flatly asserts a permanence the ASN has just disproved for spans.
**Required**: Qualify the closing line so the permanence claim is scoped to the pointwise guarantee — e.g., "the pointwise origin of any byte never changes (O5), while span-level answers grow monotonically under allocation (O6) and are stable only under fixed or extended arrangements (O7, O11/O11′)." The opening abstract framing should likewise signal that invariance is the pointwise property, with span results derived from it.

## OUT_OF_SCOPE

### Topic 1: Reporting link origins from an I-span (cross-subspace I-span)
**Why out of scope**: The I-span lift restricts to `dom(C)` by definitional choice; extending to link addresses is correctly deferred to Open Question 1, not an error in the present construction.

### Topic 2: Surfacing the intermediate transclusion chain
**Why out of scope**: SHOWORIGIN's direct-answer semantics (O4) deliberately walks no chain; a chain-surfacing operation is correctly left to a future ASN.

VERDICT: REVISE
