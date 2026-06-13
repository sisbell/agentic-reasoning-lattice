## Question 10 [theory]

> What does offering a count as a distinct service — rather than requiring the asker to retrieve the links themselves — commit the design to about the cost of link discovery, and does returning a count promise that the counted links are themselves obtainable on demand?

## Short answer

1. **Offering a count as its own command commits the design to an asymmetric‑cost model for link discovery: the *cardinality* of the answer set must be computable without delivering the answer set — knowing "how many" is cheaper than getting "all of them."** If counting cost the same as retrieving, a separate `FINDNUMOFLINKSFROMTOTHREE` would be strictly worse than letting the front end retrieve and count locally. The command's existence *is* the commitment.

2. **No.** A count is an existence/cardinality assertion, not a retrieval warranty. Permanence makes the counted links obtainable *in principle*; the distributed, "always broken" network makes obtainability *on demand* best‑effort, which the count never promises.

---

## 1. What a standalone count commits the design to

The decisive structural fact is that Xanadu separates *discovery* from *delivery*, and the count sits firmly on the discovery side:

> "Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments." (4/61)

So every link-search command — including the count — is index/search machinery, not content delivery. That gives a selectivity ladder, each rung cheaper than the next:

- `FINDNUMOFLINKSFROMTOTHREE` → just the cardinality (cheapest)
- `FINDLINKSFROMTOTHREE` / `FINDNEXTNLINKSFROMTOTHREE` → the *addresses* of matching links (paginated)
- `RETRIEVEENDSETS` → the links' actual endsets
- `RETRIEVEV` → actual content fragments (the only true delivery)

Exposing the bottom rung as a distinct service asserts that the back end's "inter-indexing mechanisms" can answer *how many match* by traversing index structure, **without** paying to materialize each match. This is consistent with the search-cost law Nelson states for links:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

Discovery cost tracks the *matching* set, not the total link population — and a count is exactly the "size of the matching set" probe. Its purpose is to be the planning primitive that lets a front end size a query before committing to the expensive retrieval that follows — the same problem the paginated retrieval addresses by capping "no more than `<nlinks>` items" to handle "avalanches of material" (4/69). A count is only useful as a guard against avalanches if it is cheaper than the avalanche it guards. The commitment, in one line: **link discovery must support cardinality queries decoupled from, and cheaper than, link delivery** — which is precisely what the "efficiently ever-linkable enfilade" and the logarithmic "soft corridor" exist to make credible.

## 2. Does the count promise the counted links are obtainable on demand?

No — and the architecture makes the gap explicit.

**What the count *does* assert.** Only links and bytes are actually stored (everything else is ghost/conceptual: 4/23), so a counted link is a real object, and permanence guarantees its address stays valid:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." (4/19)

So the counted links are obtainable *in principle*.

**Why "on demand" is *not* promised.** The count can be answered from the responding server's model of the docuverse, even when the link's content is homed elsewhere:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse..." (4/72)

But delivery rides the distributed path, which is explicitly best-effort:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." (4/75)

So the system tolerates a "not currently available" outcome, and retrieval is a *separate* tier (`RETRIEVEENDSETS`, then `RETRIEVEV`) subject to its own resource/availability limits — Nelson's Resource Unit exists precisely for requests the back end can't fully satisfy. There is also a temporal seam: a count is a snapshot against current state, and current-addressability is mutable — a deleted link becomes "not currently addressable, awaiting historical backtrack functions," even though it persists in Istream. A count taken before such a change does not warrant that every member is still currently fetchable.

**Bottom line:** the count promises *"N matching links exist"* (and, by permanence, exist durably), not *"here are N handles you can fetch right now."* The design deliberately puts counting on the index/discovery side of the one-and-only delivery boundary (`RETRIEVEV`, 4/61); carrying a per-item retrieval guarantee across that boundary would erase the very separation that makes a cheap count possible.

---

*NEED_RAW: 4/68–4/69 (pages 235–236) — I relied on the curated operation maps, which attest `FINDNUMOFLINKSFROMTOTHREE` as a command and describe it as "count matching links," but the curated sources don't contain Nelson's verbatim spec text for that specific command (unlike `FINDLINKSFROMTOTHREE` at 4/69 and `RETRIEVEENDSETS` at 4/70). Reading the protocol pages would let me ground the count command's exact wording and confirm whether Nelson comments directly on its cost or return semantics. I don't have a Read/file tool available in this session to open the page images myself.*
