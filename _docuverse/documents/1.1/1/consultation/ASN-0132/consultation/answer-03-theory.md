## Question 3 [theory]

> Must a link anchored to content that no document currently presents still be counted, or is countability conditional on the link being surfaced somewhere a reader could encounter it?

## Answer

**The link must still be counted.** In Xanadu, countability is a *structural* property — it depends on the link's endsets resolving to addresses that fall within the search request, not on whether the anchored content is currently presented in any document's Vstream or reachable by a reader. "Surfaced somewhere a reader could encounter it" is a *front-end filtering* question, which Nelson deliberately separates from the *back-end* operation of finding and counting links.

Four converging principles from *Literary Machines* force this conclusion.

### 1. Links anchor to bytes (Istream), not to presented positions (Vstream)

A link is "a strap between bytes," and it persists as long as the bytes exist — independent of how (or whether) they currently appear in a document:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

The survival condition is "bytes are left" / "anything is left at each end" — an Istream-existence test, not a Vstream-presentation test.

### 2. "No document currently presents it" does not remove the content

Deletion removes content from a document's *current arrangement*; it never removes the bytes from permanent storage:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

So content "no document currently presents" still exists at its permanent I-addresses. The link's endsets still resolve. There is nothing about the deletion that touches the link.

### 3. Search and counting match *addresses*, not stored/presented content

This is the decisive point. The retrieval mechanism never inspects what is at an address — it considers only the address itself:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

Nelson pushes this to its limit with **ghost elements**: links to addresses where *nothing is stored at all* are still valid search targets.

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

This yields the strongest form of the answer *a fortiori* (my inference, built on Nelson's explicit ghost-element rule): if a link pointing at an address where **nothing was ever stored** is still findable and countable, then a link pointing at content that *does* exist in Istream but merely isn't presented in any current Vstream is *even more clearly* countable. Presentation status is simply not a variable the count operation reads.

### 4. Counting is back-end and unconditional; "encounterability" is front-end filtering

Nelson architecturally separates "what links exist on these addresses" (back end) from "what should this reader see" (front end). The count operation returns *all* address-satisfying links:

> "FINDLINKSFROMTOTHREE … returns a list of all links which are (1) in `<home set>`, (2) from all or any part of `<from set>`, and (3) to all or any part of `<to set>` and `<three set>`." (4/69)

> "If the home-set is the whole docuverse, all links between these two elements are returned." (4/63)

And crucially, irrelevant or unreachable links do not subtract from the count of the others — they coexist in the same address space:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

Deciding which of those counted links a reader actually *encounters* is the job of the front end, kept invisible from the user-facing concern of content and links:

> "The user's concerns are document content and links, and the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." (4/61)

So "is the link surfaced where a reader could meet it?" is exactly the question a front-end *filter* answers — it is not the question the count answers.

### The one genuine break condition

A link becomes uncountable only when **nothing is left at an end** — when all bytes of an endset cease to exist as addressable content (4/43, "if anything is left at each end"). But in pure Xanadu this cannot be caused by editing or deletion, because Istream is permanent and append-only; deletion only changes the Vstream mapping. Therefore "content no document currently presents" never crosses that threshold: its bytes are still left, the strap is still attached, and the link is still counted.

## Summary of design intent

| | Governs | Reads | Affected by "no document presents it"? |
|---|---|---|---|
| **Countability** (FINDNUM…, FINDLINKS…) | back end | endset **addresses** | **No** |
| **Surfacing / encounterability** | front end | relevance, current views | Yes (filters it) |

Counting a link tells you the connection *exists in the docuverse*; surfacing it tells you a reader will *meet it now*. Nelson's whole link model — survivability by spans, address-only search, ghost elements, and the front-end/back-end split — is built precisely so these two stay independent. A link anchored to content nobody currently shows is still part of the literature's structure, and the system still counts it.

---

**Scope note / NEED_RAW: 4/58-4/60.** Nelson does not, in the curated sources, address this exact edge case ("counting a link whose anchor is in no current Vstream") in a single sentence; the answer above is a deduction forced by the convergence of the four explicitly stated principles. If you want to confirm whether the link-search pages state the count operation's treatment of deleted-but-extant or non-presented content more directly — or describe junk-link filtering as Nelson's own words rather than curated paraphrase — those would be the pages to pull.
