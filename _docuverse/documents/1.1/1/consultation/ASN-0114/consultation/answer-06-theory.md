## Question 6 [theory]

> If the selected end is empty — the link records no content at that position — what must be returned, and how must that differ from the case of an invalid selector?

## Empty endset vs. invalid selector

These are categorically different outcomes, and Nelson's design intent requires the system to keep them distinct: **an empty end must return the empty span-set as a successful, well-formed value; an invalid selector is not a value at all but an error/domain violation.**

### The empty end returns the empty span-set — and that is a legitimate value

In Xanadu, "emptiness" is a first-class, valid state of a span. A span is defined by its boundaries, not by a count of what it contains, and the quantity it covers can legitimately be zero:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

So when you retrieve an endset (e.g., via **RETRIEVEENDSETS**, which "returns the from-set and to-set"), a position that records no content yields an **empty span-set** — a span-set with no spans. This is a normal, successful result. The link still exists, the address is well-formed, and the answer to "what is at this end?" is simply "nothing right now."

This is reinforced by Nelson's treatment of *ghost elements*: addressing a position with no stored content is explicitly supported, not an error.

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (`ghost-elements`, citing 4/23)

The whole point of ghost elements and empty spans is that *absence of content is a meaningful, queryable condition* — the address is valid, the result is empty. An empty end must therefore round-trip cleanly: you get back an empty span-set, and you can act on it (it may fill in later).

### An invalid selector is outside the domain — it must not masquerade as "empty"

An invalid selector is a different thing entirely: a malformed tumbler, or an address you cannot legitimately reach. Nelson notes that not every address is arithmetically reachable from a given starting point:

> "Starting from a given tumbler address, it may only be possible arithmetically to get to some places in the Docuverse — those notationally after that address." (4/25)

The crucial design consequence is that the two cases **must not collapse to the same return**. If an invalid selector returned an empty span-set, a caller could not distinguish "this end legitimately holds nothing (and may hold something tomorrow)" from "this request was ill-formed (and will never mean anything)." That confusion would break the very guarantees ghost elements and empty spans are meant to provide — that emptiness is a real, evolving state of a valid address.

So:

| Case | What it means | What must be returned |
|------|---------------|----------------------|
| **Empty end** | Valid, well-formed address; no content recorded *now* | The **empty span-set** — a successful result |
| **Invalid selector** | Malformed / out-of-domain address | An **error / failure**, distinct from any span-set value |

The empty span-set is the correct *answer* to a valid question; the invalid selector means *there was no valid question to answer*.

---

**NEED_RAW: 4/58–4/70** — The curated sources establish the semantic intent (empty spans and ghost-element addresses are valid, non-error results), but they do not contain an explicit statement of the FEBE return-value or error contract distinguishing a malformed/invalid selector from an empty result. If you want a verbatim quote on how RETRIEVEENDSETS or the link-search commands report an ill-formed request versus an empty endset, those protocol pages (around 4/58–4/70) would need to be checked directly — I did not find that distinction stated verbatim in the verified material above.
