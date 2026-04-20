## Question 6 [nelson]

> Does the author of the original content retain any rights or privileges over that content when it appears in another author's document through sharing?

# Original Author's Rights Over Transcluded Content

Yes — the original author retains significant rights and privileges. This is one of Nelson's most carefully designed aspects of Xanadu. The architecture structurally guarantees these rights rather than relying on policy.

## Rights Retained

### 1. Ownership Is Never Transferred

Content included in another document remains the original author's property. Transclusion is reference, not copy — the bytes never leave the original author's I-space address.

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The compound document's author owns their arrangement and their original writing. The transcluded content remains owned by its creator.

### 2. Automatic Per-Byte Royalty

Every time the original content is delivered to a reader — even through someone else's document — the original author is paid automatically.

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

This is proportional and automatic. If someone builds a compound document that is 70% your content and 30% theirs, you receive 70% of the royalty. No negotiation, no contracts, no tracking — the system handles it.

### 3. Structural Attribution

The original author's identity is encoded in the I-space address itself. Attribution cannot be stripped because it IS the address.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

A reader of the compound document can always identify which words came from the original author and navigate directly to the original context. This is not metadata that can be removed — it is how the system fetches the content in the first place.

### 4. Non-Destruction of the Original

The original document cannot be damaged, modified, or altered by transclusion or derivative works.

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

### 5. Control Over Modification and Withdrawal

Only the original owner can change or withdraw their document.

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

No one who transcludes your content gains any ability to modify it.

## What the Original Author Gives Up

There is an explicit trade-off. By publishing, the author relinquishes two things:

### 1. Permission Control Over Quotation

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

### 2. Control Over Incoming Links

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

## The Design Principle

Nelson separates **control over use** from **compensation for use**. Traditional copyright conflates the two. Xanadu decouples them:

- **Control over use**: relinquished upon publication (anyone may quote, link, transclude)
- **Compensation for use**: permanently guaranteed (automatic per-byte royalty)
- **Attribution**: permanently guaranteed (structural, in the address)
- **Integrity of original**: permanently guaranteed (non-destructive architecture)

The author gives up the ability to say "no, you may not quote me" — but never gives up being paid, being credited, or having their original preserved intact.

## Summary Table

| Right | Retained? | Mechanism |
|-------|-----------|-----------|
| Ownership of content | Yes | I-space addresses are permanent |
| Per-byte royalty | Yes | Automatic with every delivery |
| Attribution | Yes | Structural (I-address encodes origin) |
| Original integrity | Yes | Append-only storage; transclusion is reference |
| Right to modify/withdraw | Yes | Only owner can change their document |
| Permission over quotation | **No** | Relinquished by publication contract |
| Control over incoming links | **No** | Relinquished by publication contract |
