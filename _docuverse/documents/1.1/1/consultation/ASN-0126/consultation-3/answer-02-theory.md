## Question 2 [theory]

> Is attributed retraction intended to be a substrate-provided, pre-registered standard type, or is registering a retraction type left to each app?

## Short answer

Nelson never names a "retraction" link type, so the question isn't answered directly. But the architecture he describes gives a clear principle: **link types are open-ended and user-definable, not a closed set the substrate must pre-register.** Whether a *retraction* type becomes a substrate-provided standard versus an app-local convention is exactly the kind of decision Nelson leaves open — he maintains only a "tentative," "provisional" standard set and explicitly defers full standardization.

## The architectural facts

**1. Types are user-definable by default — no registration authority is required.**

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." (4/43)

Because a type is just an *address* (the three-set), matched by address rather than content, defining a new type requires no schema change and no central registry:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

So *architecturally*, an app can mint a retraction type on its own — nothing in the substrate must bless it first.

**2. But Nelson does maintain a standard set "by convention," and treats standardization as a goal — just not yet settled.**

His list of link types is explicitly provisional:

> "A TENTATIVE LISTING OF SOME LINK TYPES. Link types are open-ended, so this is not the original beginning, but a first provisional, to give the flavor of current thinking."

> "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig." (4/52)

His tentative standard set (ordinary text links, literary links, metalinks) includes Connection, Comment, Counterpart, Quote-Link, Certified, Citation, and the metalinks Title, Author, and **Document Supersession** — but **no retraction type**. So retraction is not among the types Nelson pre-registers.

**3. "Attributed retraction" maps onto Nelson's *claim-via-link* pattern, which is deliberately not gated by ownership.**

The nearest things Nelson gives you are the Document Supersession metalink (for corrections/amendments) and the Author-claim-from-outside pattern. Both show that an assertion *about* a document is just a link living at the asserter's own address — a claim, not an authority:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." (4/52)

A retraction ("attributed" = signed, traceable to whoever asserts it) fits this mold exactly: it would be a link whose home address identifies who is retracting. The system makes the claim visible and traceable; it does not need to pre-register the type to allow the claim.

## Resolution

Putting the two together:

- **The substrate does not *need* to pre-register a retraction type** for retraction to work. The open-ended, address-matched type mechanism means any app can define one (4/43, 4/44-4/45).
- **But Nelson clearly intends a *convention-level* standard set to emerge** for interoperable, common literary acts (4/52). A retraction is exactly the kind of cross-app, civically significant act ("attributed," meant to be discoverable by anyone) that benefits from a standardized type address — so that one app's retraction is recognizable to another's reader. That argues for promoting it to a substrate-provided standard type *by convention*, while the mechanism still permits app-local types.

In Nelson's own terms, the system "provides the primitive ... and lets users build whatever structures they need." Retraction is not in his tentative list, so by his design it currently falls on the *app-defined* side — but it is precisely a candidate for the standardized-by-convention set he says is "a high priority."

NEED_RAW: 4/52-4/55 — to confirm the full tentative link-type listing contains no retraction/withdrawal type (the curated extract appears comprehensive, but verifying the raw pages would let me state definitively that Nelson names none).
