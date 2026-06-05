## Question 5 [theory]

> What does the count deliberately not tell the caller about the identity or permanence of the individual links it summarizes?

## What the count withholds

`FINDNUMOFLINKSFROMTOTHREE` returns a single cardinality — "how many links satisfy this request." By design it answers *how many*, never *which*. It deliberately discards two things about the individual links it summarizes:

### 1. Identity — the permanent tumbler address of each link

Every link is a first-class object with its own permanent address and home document. The count surfaces none of this. From the links source, individual links are addressed by creation order within their home document:

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.755  → 755th link in document
```

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

The count gives you no addresses, so it tells you nothing about *which* links matched, who owns them (the home document determines ownership — `4/12`), their endsets, or their types. To get identity you must use a different operation — `FINDLINKSFROMTOTHREE` ("returns a list of all links which are...", 4/69) or `RETRIEVEENDSETS`. The count is intentionally upstream of that: it lets you size a result before pulling identities, which matters given the "junk-link problem" and paginated retrieval via `FINDNEXTNLINKSFROMTOTHREE`.

### 2. Permanence — the order-of-arrival that constitutes each link's stable existence

A count is a transient quantity; the identity of any one link is permanent and independent of it. Because link addresses are never renumbered —

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

— deleting one link does not shift the others (deleting `2.5` does not renumber `2.6`…`2.N`). The count cannot express this: the same number "47" could describe an entirely different set of links at two moments (one deleted, one created), even though every surviving link retains its exact permanent address throughout. The aggregate carries none of the order-of-arrival information that makes each link a stable, individually addressable object.

### Why this is deliberate

This mirrors Nelson's treatment of spans, which are aggregates that say nothing about their constituents:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

A count is the same kind of abstraction in reverse — a number standing in for a set, stripped of the per-element addresses and permanence that define the links themselves. Identity and permanence live in the tumbler addresses; the count lives at a level above them and is silent about both.
