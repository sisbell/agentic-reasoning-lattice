## Question 10 [theory]

> Does sharing a fragment's address with another user grant them the ability to read precisely the same content the original holder would see?

Short answer: **Not unconditionally.** Whether a shared address yields "precisely the same content the original holder would see" depends on two things: (1) whether the content is *published* or *private*, and (2) whether the address is an *Istream* (identity) address or a *Vstream* (current-arrangement) address.

## 1. Addressing is universal — but addressing is not access control

Tumbler addresses are permanent and universal, so any address you share *names* the same location anywhere in the docuverse:

> "any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

But naming a thing is not the same as being permitted to read it. Access is governed separately, by publication status:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." (2/42)

So:
- **Published content** — sharing the address *does* grant the recipient read access to that content.
- **Private content** — sharing the address does *not* grant access. Only the owner and designated associates may read it. The recipient holds a valid name they cannot resolve to content.

In other words, in Nelson's design an address is *not* a bearer capability for private material.

## 2. The XU.87.1 caveat

In the implementation Nelson documents, this access distinction was not yet built — everything was readable:

> "Private documents. (Currently all documents are visible to all users.)" (4/79)

So in that prototype, sharing any address *would* let another user read the content — but that reflects an unimplemented feature, not the intended guarantee.

## 3. "Precisely the same content" — I-address vs V-address

Even with access granted, whether the recipient sees *precisely* what the holder sees depends on which kind of address was shared.

An **Istream (I-address)** names immutable content permanently:

> "Every byte you create gets a permanent I-address ... That address will always return that exact content. Content at an I-address never changes." (from the curated Istream-addresses summary)

A **Vstream (V-address)** names a *position in the current arrangement*, which shifts as the document is edited:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

So a shared **I-address** reliably yields the identical fragment. A shared **V-address** (e.g., "byte 5 of this version") may resolve to different content later, because INSERT and DELETE renumber positions:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

## 4. Privacy is best-effort, not cryptographic

Finally, even the privacy boundary is not an absolute guarantee:

> "The network will not, may not monitor what is read or what is written in private documents. But these matters are not easy to guarantee." (2/59)

## Summary

| Condition | Does the shared address let them read the same content? |
|---|---|
| Published + I-address | Yes — exact, immutable content |
| Published + V-address | Yes, but the *content at that position* can change with editing |
| Private (Nelson's design) | No — access limited to owner and associates |
| Private (XU.87.1 prototype) | Yes — private docs unimplemented; "all documents visible to all users" (4/79) |

So an address is a permanent, universal *name*, but by design it confers read access only for published material. For private content, the address alone is not a key.
