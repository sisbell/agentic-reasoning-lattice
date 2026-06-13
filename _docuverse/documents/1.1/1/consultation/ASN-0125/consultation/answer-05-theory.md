## Question 5 [theory]

> Should the supersession relationship be expressed as its own first-class link, as a field within the new link's structure, or as a typed relation — and what does the design gain or lose with each choice?

## Short answer

In my design these three options are not three parallel choices. A supersession assertion is a **link** — specifically a *metalink* — and its supersession-ness is carried by its **type** (the third endset). So "its own first-class link" and "a typed relation" are the *same object seen from two sides*: every link is first-class (owned, addressed, searchable), and every link's meaning is given by its type-endset. The only genuinely different option on your list is the third interpretation — burying supersession as a **field** in the document or version record — and that one I reject.

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." — 4/52-4/53

It belongs with the metalinks:

> "METALINKS: These are links expected to apply to whole documents, whether from outside or from inside." — 4/52

## Why not a field in the structure

This is the tempting shortcut, and it is wrong for a reason that runs to the bottom of the system.

The address *already* encodes ancestry — a new version's tumbler descends from its parent's. You might think supersession could simply be *read off* that structure, or stamped as a "supersedes" field on the new version. I deliberately refused that:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." — 4/29

And:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." — 2/19

No version is privileged a priori. Supersession is therefore not a *fact about structure*; it is a **claim** that someone makes — that *this* replaces *that*. A claim has an author, a date, and a possibility of being wrong or disputed. A field in a record has none of those. Putting supersession in the document's structure would make the *system* the author of the assertion. That is exactly backward.

## What the link / typed-relation choice gains

**1. Ownership — claim, not authority.** Because a link has a home document, its home address tells you *who* asserted the supersession. The very same footnote I attached to the Author link governs this:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." — 4/52

So a third party can assert "my D′ supersedes Alice's D," and the assertion is visibly *theirs* — discoverable, attributable, and rebuttable — without ever being mistaken for system truth. A field can only ever hold the owner's single value; it cannot represent an outside claim at all.

**2. Pluralism and disputability.** Competing supersession claims coexist, and a reader can weigh them. This is the whole point of a system meant "to promote cumulative order and the equitable coexistence of many viewpoints." A field forces one answer; the link layer lets the answers argue.

**3. One retrieval mechanism, no special-casing.** A supersession link is found by the same link search as everything else — `FINDLINKSFROMTOTHREE` — and I engineered that search so the existence of millions of unrelated links costs nothing:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." — 4/60

So the usual argument *for* a field — "a field-read is cheaper than a search" — does not bite here. The "front-end request for supersession links before reading" is just an ordinary constrained search.

**4. It is *dated*.** Links carry their time:

> "Since links will be dated, the time of mailing is shown." — 4/55

That lets you order competing supersession claims chronologically — which a static field cannot do.

**5. It survives, and it can itself be linked.** Links attach to spans of bytes, not positions, so the assertion survives editing of either end; and because links have addresses, a supersession claim can be commented on, disputed, or grouped by further links (the CONS-cell pattern):

> "Complex relational structures … may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP." — 4/51

## Why *typed relation* specifically — and not a hardwired link "kind"

Here is the one place where your (a) and (c) genuinely diverge, and it matters. I did **not** build "supersession" as a special back-end object. The type is just an *address* pointed at by the third endset:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." — 4/44

> "The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." — 4/44-4/45

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." — 4/45

The gains of making it a *typed relation* rather than a dedicated kind:

- **Extensibility with zero system change.** Supersession is a convention on an address, not a feature in the back end. Adding "supersession" required nothing new in the storage layer.
- **Subtypes come free.** A *correction* that supersedes is not the same as a *revision* that supersedes; the type machinery already supports hierarchy: "this mechanism can be used for hierarchical link types, subtypes and supertypes" (4/51). A field cannot subdivide its meaning this way.
- **It sits naturally beside its siblings** — the Alternative-Version link, the Counterpart link — all distinguished *only* by their type endset. Supersession says "this *replaces* that"; alternative-version says "this is a *parallel* of that." Same machinery, different type address.

## What it costs

I will not pretend the choice is free.

- **It leans on standardization.** Because the front end treats the supersession link as "the canonical way to find out whether you are reading the latest version" (4/52-4/53), the *type address* for supersession must be agreed upon. If two communities point their three-set at different addresses for "supersedes," the canonical-version check fragments. I flagged this priority myself:

  > "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig." — 4/52

  A field would sidestep that coordination — at the price of everything above. For supersession specifically, the standardization burden is real and worth paying.

- **No single enforced truth.** The system will not *tell* you the latest version; it will show you who *claimed* what, and let you decide. If your application wants one authoritative pointer, you must adopt a policy (e.g., trust only supersession links homed in the original owner's account). That policy lives in the front end, not the substrate — which is precisely where I want judgment to live.

## Bottom line

Make it a **typed link — a metalink**. It is first-class *because every link is*, and it carries its meaning *as a type*, because that is how all meaning is carried in this system. Never a field: a field would let the storage layer author a claim that rightfully belongs to a user, would collapse the distinction between *ancestry* (structural, "accidental," 4/29) and *supersession* (an asserted, dated, ownable, disputable act), and would forfeit the pluralism the whole docuverse exists to protect.

---

*A note on sources:* I answered entirely from the verified curated extracts (4/29, 4/44–4/45, 4/51, 4/52–4/53, 4/55, 4/60, 2/19). I did not have a file/image tool available in this session, so I did not re-read the page scans of 4/52–4/53; if you want me to confirm the exact ordering and wording of the metalink listing as it is laid out on the page, NEED_RAW: 4/52-4/53.
