## Question 5 [nelson]

> Does the original creator's attribution to the removed content persist after removal, and can the creator still be identified as its source?

# Yes — Attribution Survives Removal Absolutely

In Xanadu, "deletion" never touches the layer where attribution lives. The creator can always be identified. Here's why:

## DELETE Only Affects Vstream

DELETE removes content from the document's **current arrangement** (Vstream) but does not touch **permanent storage** (Istream):

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The content itself — and its permanent address — remain intact.

## Attribution Is Structural, Not Metadata

Every byte in Xanadu has a permanent Istream address with the form:

```
Node.0.User.0.Document.0.Element
```

The **User** field and **Document** field directly encode who created the content and in which document. This is not a tag that can be stripped — it is the address itself. To fetch the content, the system must reference this address:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

## The Chain After Deletion

After content is "deleted" from a document:

| What happens | Attribution affected? |
|---|---|
| Content removed from Vstream (current view) | No — I-address unchanged |
| Content remains in Istream permanently | No — still at original address |
| Previous versions still contain the content | No — same I-addresses |
| Other documents that transclude it still show it | No — they reference the same I-address |
| Links to the content's I-address still resolve | No — Istream is append-only |

## The Append-Only Foundation

The entire storage model prevents attribution loss:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is never overwritten, never truly removed. The permascroll (Nelson's "hyperfile") grows monotonically. Since the I-address encodes provenance and the content at that address is permanent, **there is no operation in Xanadu that can sever attribution**.

## Summary

The original creator's attribution persists after removal because:

1. **Deletion is a Vstream operation** — it changes the view, not the content
2. **I-addresses are permanent** — they encode the creator structurally
3. **Storage is append-only** — nothing is ever destroyed
4. **Attribution is the address** — it cannot be stripped without destroying the addressing system itself

This is by design. Nelson built Xanadu so that the connection between content and creator is inherent in the architecture, not dependent on any metadata that could be lost through editing operations.
