## Question 9 [nelson]

> If a new link referencing the content is created after the content already exists, must the system make that link immediately discoverable or is eventual appearance acceptable?

## Link Discovery Timing: Immediate vs. Eventual

Nelson's design implies **immediate local discoverability** with **eventual cross-network propagation** — but he frames the user-facing guarantee in terms of responsiveness, not synchronization timing.

### Local Server: Immediate

MAKELINK is synchronous — it "creates a link in document \<doc id\>" and "returns the id of the link made" [4/68]. Once the back end returns the link ID, that link is indexed locally:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [4/41]

"Thereafter maintained" means: once created, the back end takes responsibility. There is no deferred-indexing concept. The link exists and is searchable on its home server from the moment MAKELINK returns.

### Cross-Network: Eventual, Not Instant

The BEBE protocol describes an explicitly eventual model for cross-server awareness:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." [4/72]

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [4/72]

The key phrase is **"continuously valid"** — not "continuously complete." Each server's model is always internally consistent but grows and shrinks with demand. Material migrates between servers for specific reasons:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [4/71]

Point 2 explicitly mentions index material — link indexes propagate between servers, but driven by demand, not instant broadcast.

### The Forwarding Backstop

Even when a server's subrepresentation hasn't yet received a new link, BEBE provides a forwarding mechanism:

> "First, by the forwarding of requests as they fan out from users to servers able to supply" [4/70]

So a link search that can't be fully satisfied locally gets forwarded to servers that can supply the answer. This means a newly created link is **always discoverable** — either through the local subrepresentation (if propagated) or through forwarding to the home server (if not yet propagated). The question is latency, not availability.

### The User-Facing Guarantee

Nelson states the user expectation clearly:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [2/46]

**"Without appreciable delay"** is the guarantee — not "instantaneously" and not "within N milliseconds." This is a responsiveness standard, not a synchronization guarantee. It applies to showing connections that exist, mediated by the BEBE forwarding and subrepresentation system.

### The Search Efficiency Guarantee

Nelson also guarantees that scale doesn't degrade search:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [4/60]

This is about filtering efficiency, not propagation timing — but it reinforces that link search should remain fast regardless of how many links exist in the system.

### Summary

| Scope | Timing | Mechanism |
|-------|--------|-----------|
| Home server | Immediate | MAKELINK is synchronous; back-end indexes on return |
| Remote server (cached) | Eventual | BEBE subrepresentation propagates with demand |
| Remote server (uncached) | On-demand | BEBE forwards request to home server |
| User experience | "Without appreciable delay" | Forwarding + subrepresentation together |

Nelson designed for a system where link creation is **locally atomic** and **network-eventually-discoverable**, with forwarding as the completeness backstop. He does not require instant global visibility, but he does require that the system never returns "link not found" when forwarding would find it — the system should do the work of finding it transparently.

The architecture is what we would now call **eventual consistency with read-forwarding** — each node is always valid, propagation happens continuously, and queries that can't be satisfied locally are forwarded to authoritative sources.
