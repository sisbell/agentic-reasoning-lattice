## Question 4 [theory]

> How does bounding a link's first endpoint separately from its second endpoint preserve the directional nature of a connection during discovery?

## How separate endpoint bounding preserves directionality during discovery

The short answer: because a Xanadu link records its two ends as *distinct roles* (a from-set and a to-set), and the search request matches each constraint against its *corresponding* role, you can pin down one end while leaving the other open — which is exactly what lets discovery ask the directional questions "what points *from* here?" versus "what points *to* here?"

### Directionality lives in the link structure first

A link is not a symmetric blob of connected bytes. It carries an asymmetry:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" (4/42)

So before any search happens, the two ends are already labeled by role. Discovery only has to *respect* that labeling.

### The search request mirrors the link's structure

The search request is itself partitioned into corresponding parts — a from-set, a to-set, and a three-set (type) — and the satisfaction rule matches each part of the request against the same-named endset of the link:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

The operative phrase is *"a corresponding part of the request."* The from-constraint is tested only against the link's from-set; the to-constraint only against the link's to-set. They are never pooled. This is what `FINDLINKSFROMTOTHREE` returns:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

### Why separate bounding is what produces directional answers

Because the two constraints are applied to two different roles, you can bound one and leave the other unconstrained:

- **Bound the from-set to span X, leave the to-set open** → you get every link *originating* at X, pointing anywhere. ("What does X say something about?")
- **Bound the to-set to span X, leave the from-set open** → you get every link *arriving* at X, from anywhere. ("What points at X?" — the backlinks query.)

If the two ends were merged into a single undirected set during search, both of these requests would collapse into the same answer: "every link touching X." The direction would be lost. It is precisely the *separate* bounding of first endpoint from second endpoint that keeps "from X" and "to X" as different, answerable questions.

This is how Xanadu solves backlinks while still distinguishing the two directions: the system indexes by every endset, so discovery works from either end —

> "Links are bidirectional in discovery. The system indexes links by all their endsets. You can search from any direction - find what points to this content, or find where this content points." (links.md, summarizing 4/41–4/60)

— but because each endset stays in its own labeled slot, "what points to this" and "where this content points" remain distinct results rather than one undifferentiated set.

### Why this matters semantically

Directionality is meaning. A citation runs *from* the citing text *to* the source; a comment runs *from* the commentary *to* its subject. Reversing the ends reverses the claim. By bounding from-set and to-set independently — and matching each only against its corresponding role — discovery returns connections in the same direction the author asserted them, so the retrieved relationship still means what it meant when it was made.

### A note on scale

This separation also keeps directional discovery efficient: constraining one end does not force the system to wade through everything attached to the other.

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

So bounding one endpoint tightly (say, the to-set) lets you find inbound links to a passage without being slowed by the universe of unrelated outbound links sharing the from-end.

---

In sum: the from-set and to-set are stored as distinct roles on the link (4/42), the search request carries matching from/to constraints, and the satisfaction rule applies each constraint to its *corresponding* endset (4/58, 4/69). Constraining the two ends separately is therefore not just an implementation convenience — it is the mechanism that keeps "links from X" and "links to X" as two different, direction-preserving queries.
