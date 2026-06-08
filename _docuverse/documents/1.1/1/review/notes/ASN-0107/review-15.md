# Review of ASN-0107

## REVISE

### Issue 1: P1's deduplication paragraph specifies backend mechanics, not a system guarantee

**ASN-0107, "What Is Counted" (P1)**: "We note as an implementation observation that a backend which materialises the matching set as a list and *walks the list* must deduplicate before counting: if a single multi-span link can be appended to that list more than once — as happens when an endpoint's several spans each independently match — then the walk overcounts, and the returned integer is a multiset tally in violation of P1."

**Problem**: The note's own charter is to state "the abstract guarantees ... independent of how it walks its indices." This paragraph then introduces a specific walk-the-list backend and a per-walk deduplication procedure — implementation mechanics. The load-bearing guarantee (`num` is set cardinality, contribution `∈ {0,1}`) is already fully stated in P1's first two sentences; the materialise/walk/deduplicate story adds no abstract content and is exactly the kind of accretion the precise reader must skip past. The classifier on this note (`review-mode.anti-bloat`) targets this.

**Required**: Trim the list-walk/deduplication digression. If a faithfulness-to-the-set obligation must be stated, state it as a guarantee ("any enumeration realising `match` must collapse multi-span matches per link") in one clause, without describing a backend's list traversal.

### Issue 2: The "returning the links is a separate, out-of-scope operation" remark is stated twice

**ASN-0107, "State and the Counting Request"**: "the operation that *returns* those links is a different operation, out of scope here."
**ASN-0107, W1**: "Recovering *which* links matched requires a different operation — one that returns the links — and that operation is out of scope here precisely because it answers a different question."

**Problem**: Two paragraphs in different sections carry the same content. W1 is the natural home (it is the consequence of cardinal abstraction); the State-section instance restates it before it is needed.

**Required**: Keep the remark at one site (W1) and reduce the State-section mention to the bare scope note, or drop the duplicate.

### Issue 3: R5's existence-count half is E4 restated

**ASN-0107, R5 and Claims table**: "Conservation (= E4) holds for the existence count ... the identity is exactly E4" / table row "R5 | Conservation (= E4) ...".

**Problem**: The note labels R5's existence-count content `= E4` in both prose and table — an explicit acknowledgement that one half of R5 reproduces E4 verbatim. Only the negative discovery-count result is new.

**Required**: Fold R5's novel content (conservation *fails* under discovery anchoring) into a single statement and cite E4 for the affirmative half rather than re-asserting it as a fresh conservation identity.

## OUT_OF_SCOPE

### Topic 1: Independently-anchored multi-document requests
The first Open Question (three parts anchored to separately-evolving documents) is correctly deferred; the conjunctive `sat` over per-slot arrangements would need its own monotonicity analysis. Not an error here.

### Topic 2: Coincidence of discovery and existence counts
The second Open Question (when every resident matching link is also discoverable) is genuinely new territory requiring the retrieval operation's contract; correctly left open.

VERDICT: REVISE
