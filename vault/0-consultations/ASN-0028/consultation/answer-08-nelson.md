## Question 8 [nelson]

> Must the system preserve the order in which documents were created, and does a document's position in that ordering carry any meaning?

## Does Creation Order Matter in Xanadu?

**Short answer:** The system structurally preserves creation order through sequential tumbler assignment, but Nelson explicitly denies that this ordering carries semantic meaning.

### Creation Order IS Preserved

Sequential numbering is an unavoidable consequence of the forking/baptism mechanism. Documents under an account are created by successive forking:

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

So document 1.2.3 was necessarily created after 1.2.2 under account 1.2. This is structural — the system cannot assign these numbers out of order.

For **links within a document**, creation order is even more explicitly preserved:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Link 2.1 is always the first link created; link 2.755 is always the 755th. Deleting link 2.5 does not renumber 2.6 onward.

At the **byte level**, I-space content is append-only — "filed, as it were, chronologically" [LM 2/14]. Later-created bytes have higher I-addresses within a document.

### But the Ordering Carries No Semantic Meaning

Nelson is explicit on two points that drain the ordering of significance:

**Tumblers impose no structure on content:**

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]

**Time is not encoded in the address:**

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

That document 1.2.3 comes after 1.2.2 tells you about creation sequence but says nothing about the document's subject, importance, or relationship to 1.2.2. The numbering is purely a mechanism for allocating unique, permanent addresses.

### Even Version Numbers Don't Imply Derivation

Perhaps most strikingly, Nelson disclaims semantic meaning even for version/subdocument numbers:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

And:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

### Summary

| What | Preserved? | Meaningful? |
|------|-----------|-------------|
| Document creation order under an account | Yes (sequential forking) | No (mapping mechanism only) |
| Link creation order within a document | Yes (permanent order of arrival) | Structural fact, but no semantic weight |
| Byte creation order in I-space | Yes (append-only) | Implementation detail, not user-facing |
| Version numbering | Yes (sequential) | Explicitly "no specific relationship of derivation" |
| Timestamps | Tracked separately | Yes — used for filtering (e.g., "links from last week") |

The system **must** preserve creation order because the addressing mechanism makes it structurally inevitable — you cannot assign tumbler 2.3 before 2.2. But this ordering is a side effect of the allocation mechanism, not a semantic property. Nelson designed tumblers as a **mapping mechanism**, not a **categorization system**. Actual temporal information is kept separately as metadata, usable for filtering but not baked into the address structure.
