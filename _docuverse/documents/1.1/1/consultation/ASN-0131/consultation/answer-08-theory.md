## Question 8 [theory]

> What soundness guarantee must hold: must every endset the operation returns genuinely touch the region asked about, so the answer never reports anchoring that does not reach it?

## Yes — soundness is non‑negotiable. Every endset a search returns must genuinely reach the region you named.

This is the half of a correct search that I would phrase as: *the answer never lies about contact.* If you ask "what links touch this span?", every result must actually have a strap landing in that span. A reported anchoring that does not reach the region is a false positive, and the system must not produce one.

### The contract that makes it soundness

The whole of link retrieval rests on a single satisfaction predicate:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

The retrieval operations are then specified to return *exactly the satisfiers* — and that "which are from…" clause is itself the soundness statement, embedded in the operation:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." [LM 4/69]

> "This returns a list of all link end-sets that are in <spec set>." [LM 4/70]

Read those carefully. The operation does not return links that *might* be from the region, or links near it — it returns links that *are* from it. RETRIEVEENDSETS returns endsets that *are in* the spec-set. To return an endset that is not in the spec-set would be to break the operation's own definition. So soundness is not an add-on guarantee; it is what the words "which are" and "that are in" mean.

(The term *soundness* is my framing; what I am the authority on is the predicate and the return contract above. Soundness is simply the requirement that the returned set never exceed what the predicate admits.)

### Be precise about what "genuinely touch" requires

Three distinctions matter, or you will mis-state the guarantee:

1. **Per constrained endset, against its corresponding part of the request.** A request names a home-set, from-set, to-set, and three-set. Soundness binds each *constrained* endset to *its* counterpart: the link's from-set to your from-request, its to-set to your to-request, its type to your three-set. If you only constrain the from-set, only the from-set must reach — the others may point anywhere.

2. **Existential, not universal.** An endset is an arbitrary, possibly discontiguous span‑set ("one end of a link may be on a broken, discontiguous set of bytes," [LM 4/42]). The guarantee is that *at least one* of its spans lands in the region — "one span of each endset" [LM 4/58]. It does **not** require the whole endset to lie inside the region. So "genuinely touch" means *genuinely reaches*, not *is wholly contained*. The other spans of that same endset legitimately point elsewhere.

3. **Partial overlap is real contact.** "From all or any part of <from set>" [LM 4/69] — a link qualifies whether it covers your whole region or only clips a piece of it. Soundness still demands that the clip be a true intersection, not a near miss.

### The type endset: contact means address, not content

For the third endset, "touch" is defined on the tumbler line, not on stored bytes:

> "What the 'type' designation points to is completely arbitrary… The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

So a sound type match is one whose type address genuinely falls within the requested three-set — even if that address is a ghost element with nothing stored there. Soundness here is "the address really lands in the span you asked for," nothing more and nothing less.

### Why this must hold — the design intent

A Xanadu link "is not between points, but between spans of data… we may visualize it as a strap between bytes" [LM 4/42]. The strap is a structural claim about the literature: *this reaches that.* The entire value of "What connects here from other documents?" — the backlinks discovery that paper never gave us — collapses if the system reports straps that do not actually grip. A reader must be able to "at once ascertain the home document of any specific word or character" [LM 2/40]; that trust extends to every reported connection. An unsound search would be a Ministry-of-Truth of citation: telling you a passage is anchored where it is not.

### Soundness vs. completeness — keep them apart

Your question is the soundness half: nothing spurious gets in. The complementary half is completeness/performance — nothing real gets drowned out:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

That line is about the junk‑link problem: even an ocean of non‑matching links must not hide the matches. It is the dual of what you asked. A correct retrieval owes you both — every returned endset truly reaches the region (soundness), and every endset that reaches it can be found (completeness). The satisfaction predicate at [LM 4/58] is the shared definition both halves are measured against.

**In one sentence:** a search may report an endset only when one of its spans genuinely intersects the corresponding part of your request — so the answer reports reach, never the appearance of reach.
