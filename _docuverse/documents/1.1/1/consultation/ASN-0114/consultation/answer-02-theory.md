## Question 2 [theory]

> What relationship must the returned specification bear to the end the link actually records at the selected position — must it denote exactly the same content region, no more and no less?

## Answer

Yes. The returned endset specification must denote **exactly the content region the link actually holds at that end — no more and no less** — and Nelson's span semantics are what force this.

### Why exactness is required

An endset is not a point or an approximation; it is a **span-set**, and Nelson defines span-sets precisely so they can designate a region *exactly, including nothing else*:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

Because each of a link's three endsets *is* such a span-set —

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." (4/43)

— retrieving the end means returning that exact span-set. `RETRIEVEENDSETS` is specified to hand back what the link records, not a paraphrase of it:

> "This returns a list of all link end-sets that are in <spec set>." (4/70)

### What "exactly" means here: the bytes the link seized

The recorded region is defined by the *bytes* the link grabbed, not by positions or surrounding context. The link "seizes" a span and clings to it:

> "Essentially, the link seizes a point or span (or any other structure) in the Prismatic Document and holds to it." (2/26)

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." (4/42)

So the returned spec must cover precisely those bytes (by their Istream identity) — it must not pad outward to engulf neighboring content (**no more**), and it must not under-report the bytes still attached (**no less**).

### The subtle case: editing and partial survival

Exactness is *to what the link currently records*, which may differ from what it originally recorded. Survivability means a link holds only to whatever bytes remain:

> "If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

So if part of an end has been deleted, the end the link "actually records at the selected position" is now that surviving, possibly discontiguous, subset — and the returned span-set must denote *that* exactly, not the original full extent.

### Important distinction: retrieval exactness ≠ search permissiveness

Do not confuse this with link *search*, which is deliberately permissive. For matching a query, mere overlap suffices:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

That permissive "one span satisfies a corresponding part" rule governs whether a link is *found*. It does **not** loosen what gets *returned* as the endset. A link can match a request via partial overlap, yet the endset you then retrieve still denotes exactly the region the link records — no more, no less.

---

**Scope note:** The exactness conclusion is a direct inference from Nelson's span-set definition (4/25), the endset-as-span-set definition (4/43), and the `RETRIEVEENDSETS` spec (4/70). Nelson does not state in a single sentence "the returned endset equals the recorded region exactly"; that identity follows from combining those passages. If you want me to confirm the precise wording around `RETRIEVEENDSETS` and any exactness qualifier in the protocol text: NEED_RAW: 4/57–4/60, 4/70.
