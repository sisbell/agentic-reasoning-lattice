# Review of ASN-0042

## REVISE

### Issue 1: "Content-bearing document address" contradicts O10(c)'s own definition of content-bearing depth

**ASN-0042, O10, "Forking at greater depth"**: "For an account-level principal (`zeros(pfx(π)) = 1`), the single baptism produces a content-bearing document address (`zeros(a') = 2`) in one allocation call."

**Problem**: O10(c) states explicitly that "Content-bearing depth (element level, `zeros = 3`) is not guaranteed by O10 itself; it requires further organizational baptisms within `dom(a')`." The same "Forking at greater depth" paragraph also says "Descending further to content-bearing depth follows O10(c)" — confirming a `zeros = 2` document address is *not* content-bearing. Then the very next sentence calls the `zeros = 2` document address "content-bearing." A `zeros = 2` address is a document address by T4c, and content lives at element level (`zeros = 3`). The label is internally contradictory.

**Required**: Remove "content-bearing" from the `zeros = 2` description. State it as "a document-level address (`zeros = 2`), one tier above content-bearing element depth."

### Issue 2: Level terminology drifts between "user level" and "account-level slot" for the same `zeros = 1` fork

**ASN-0042, O10(c)** vs **"Forking at greater depth"**: O10(c) says a node-level principal's fork lands at "user level"; the later paragraph says it "yields an account-level namespace slot (`zeros(a') = 1`)."

**Problem**: T4c fixes `zeros = 1` ↔ user address. The two passages name the identical structural tier differently (user vs account). A precise reader cannot tell whether a distinction is intended.

**Required**: Pick one level name for `zeros = 1` and use it consistently in both passages.

### Issue 3: Forward-reference accretion around the "single-allocation-point evidence"

**ASN-0042, O17b**: "Gregory's implementation corroborates the coupling, and we anchor the allocation-site evidence here for reuse: every registry write in udanax-green funnels through a single allocation point…"

**Problem**: "we anchor … here for reuse" is meta-prose announcing a downstream-citation hub rather than advancing the axiom. The hub is then back-referenced from three separate sections — O18 ("The single-allocation-point evidence anchored at O17b confirms…"), DelegatorAllocatesPrefix ("By the single-allocation-point evidence anchored at O17b…"), and O10 ("Gregory's allocator behaves identically, by the single-allocation-point evidence anchored at O17b"). This is exactly the "multiple paragraphs in different sections defer to the same downstream location" pattern the anti-bloat classifier targets; it compounds across cycles.

**Required**: State the implementation evidence plainly at O17b without "anchor … for reuse," and at each use site state the relevant fact directly rather than back-pointing to the anchor.

### Issue 4: O14's last clause inventories downstream consumers instead of stating what it asserts

**ASN-0042, O14**: "This last clause is the base case that, together with O17b's per-transition coupling, makes every reachable `Σ.B` an ASN-0040-reachable registry by induction — so B1 (ContiguousPrefix), `hwm`, `next`, and B6 are available on `Σ.B` at every reachable state."

**Problem**: This explains *why the clause is needed* and enumerates its downstream consumers (B1, hwm, next, B6) rather than stating the clause's content. The induction it describes is performed in O10's construction; the enumeration belongs there (or nowhere), not appended to a bootstrap axiom clause.

**Required**: Drop the consumer inventory. The clause says `Σ₀.B` is an ASN-0040-reachable registry conforming to B₀ conf.; that is its content.

### Issue 5: The `zeros(a') = zeros(pfx(π)) + 1` fact is restated three times

**ASN-0042, O10**: the fact appears in (a) the O10(c) clause body, (b) the "Condition (c) is enforced by the construction `a' = pfx(π).0.{hwm_0 + 1}` …" paragraph, and (c) the Formal Contract's `zeros(a') = zeros(pfx(π)) + 1` clause with its parenthetical re-derivation.

**Problem**: Three paragraphs in one section say the same thing in different words (paragraph-level redundancy flagged by the anti-bloat classifier).

**Required**: State and justify it once (the construction-based derivation), and let the Formal Contract assert the clause without re-deriving.

### Issue 6: Residual "unified argument" meta-commentary in O10

**ASN-0042, O10**: "The argument is unified: a single baptism by `π` produces such an address in every reachable state, with the trajectory length independent of `zeros(pfx(π))`."

**Problem**: "The argument is unified" and "trajectory length independent of `zeros`" are commentary about the proof's structure relative to a prior (presumably case-split) version — reviser drift, not reasoning that advances the claim. A "single baptism" is trajectory length 1 by definition, so the independence remark is vacuous.

**Required**: Replace with a direct statement: "A single baptism by `π` produces such an address in every reachable state, for both `zeros(pfx(π)) = 0` and `zeros(pfx(π)) = 1`."

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
**Why out of scope**: The ASN correctly observes Nelson's "bought the document rights" implies transfer but Gregory's codebase has none, and defers the invariants to an Open Question. This is future territory, not an error here.

### Topic 2: Cross-node identity federation consistency with O9
**Why out of scope**: O9 establishes node-locality; how a federation layer would preserve it is new territory, already listed as an Open Question.

VERDICT: REVISE
