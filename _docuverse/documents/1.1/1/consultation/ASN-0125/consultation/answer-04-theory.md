## Question 4 [theory]

> Must the relationship between an edited link and its original be recognizable as supersession specifically — distinguishable by readers from two independent links that merely happen to resemble one another?

## Short answer

**No.** Nelson neither requires nor natively provides this recognizability. By default, an "edited" link and its original are structurally just two distinct links — and the system deliberately refuses to read *resemblance* as *relationship*. So a revised link is, absent an explicit assertion to the contrary, indistinguishable from "two independent links that merely happen to resemble one another." Supersession between them exists only if someone makes it exist, by hand, as a typed link-to-link — and even then it is a *claim*, not an enforced structural fact.

Let me unpack why, because the question exposes three load-bearing pieces of the design.

---

## 1. "An edited link" is already the wrong frame — there is no link-editing

There is no operation in the protocol that modifies a link's endsets in place. The link-side of the command set is `MAKELINK`, the `FIND…` family, and `RETRIEVEENDSETS` — nothing that mutates an existing link's from-set, to-set, or type. Links also carry permanent, arrival-ordered identity:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

So to "change" a link you delete the old one and make a new one. The deletion is non-destructive bookkeeping —

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

— and the replacement is a *fresh* link with a *fresh* arrival-order address. Structurally, that new link stands in exactly the same relation to the deleted one as it does to any other link in the docuverse: none. There is no slot in a link's structure that says "I am the corrected form of #234."

---

## 2. Supersession, in my taxonomy, is a *document/version* relation — not a link relation

When I named supersession, I scoped it to whole works:

> "METALINKS: These are links expected to apply to whole documents, whether from outside or from inside." (4/52)

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." (4/52–4/53)

Note the noun: *document or version*. There is no "link-supersession link" in the type catalog, and there is no front-end convention of "request the supersession links *for a link* before reading it." The whole machinery that makes document supersession reader-facing — a normal, expected query the front end runs on your behalf — has no link-level counterpart in the specification.

---

## 3. The system never infers relationship from resemblance — by design

This is the heart of your question. Identity in the docuverse is by *creation and address*, never by *value*. Two links with byte-for-byte identical endsets are two different links, because they arrived separately (4/31). Resemblance carries no structural weight whatsoever.

That is a deliberate refusal, not an omission. If the system treated lookalike links as related, it would manufacture false positives — coincidental or independently-convergent links flagged as derivations — and it would corrode the attribution model, which depends on relationships being *asserted and owned* rather than *guessed*. So the very property a reader would lean on to "recognize supersession" — that the new link looks like the old — is precisely the property I declined to let the system act on.

The consequence is symmetric and exact: an edited link resembling its original, and two unrelated links resembling each other, present **identically** to the system. Neither is marked. Distinguishing them is not a guarantee the architecture offers.

---

## 4. You *can* make it recognizable — but only by saying so, and only as a claim

Because links live in tumbler-space alongside data, a link can point at another link:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." (4/49)

…and the type endset is open-ended, matched by address rather than content:

> "What the 'type' designation points to is completely arbitrary… The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44–4/45)

So if you want the relationship to exist in the docuverse, you point a link from the new link to the old and *type it as supersession*. That is the only way it becomes recognizable — and it is recognizable as supersession **specifically** only because you chose a supersession type rather than, say, a counterpart type, which would instead assert mere equivalence:

> "The counterpart link shows that there are correspondences between two equivalent documents, sections or passages." (4/53)

Two crucial caveats follow:

- **It is a claim, not an authority.** The same logic that lets an Author link be asserted from outside a document applies here: "Note that the Author link can also be used from outside a document to claim that the author is really someone else." (4/52, footnote). A supersession assertion lives at *its maker's* home address, is attributed to them, and can be followed, weighed, and rebutted. The system records the assertion; it does not certify it.
- **Document-versioning won't manufacture it for you.** Even if you version the *containing* document, the correspondence machinery (`SHOWRELATIONOF2VERSIONS`) corresponds *content spans*, not link identities. Comparing two versions would show "old link absent, new link present" — leaving the reader to *infer* a connection from resemblance, which is exactly the inference the architecture declines to underwrite.

---

## Bottom line (design intent)

Relationships in Xanadu are **made, not inferred**. I built every connection as an explicit, owned, typed link precisely so the structure of the docuverse reflects asserted relationships rather than algorithmic guesses about similarity. Therefore:

- It is **not required** that an edited link be recognizable as superseding its original.
- It is **not automatic** — by default the two are indistinguishable from coincidental lookalikes.
- It becomes recognizable **only by explicit assertion**, and when present it stands as a *claim* at the asserter's address, distinguishable from correspondence or comment only by the type you deliberately chose.

Resemblance was never meant to be evidence. If you want supersession to be readable, you must write it down.

---

*Scope note: Nelson does not discuss "link editing" or "link-level supersession" directly anywhere in the curated material — these are document/version constructs — so the answer above is composed from established facts (no modify-link command; arrival-order link identity, 4/31; document-scoped supersession, 4/52; resemblance-blind identity; open-ended link-to-link typing, 4/44/4/49). To independently confirm there is no link-modify command and no link-level supersession type I've overlooked, the authoritative raw pages are* **NEED_RAW: 4/52–4/55** *(the tentative link-type catalog) and* **4/61–4/70** *(the complete XU.87.1 command set).*
