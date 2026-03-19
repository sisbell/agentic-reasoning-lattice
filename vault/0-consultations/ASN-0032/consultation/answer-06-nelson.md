## Question 6 [nelson]

> Who owns a link — the person who created it, one of the connected document authors, or does ownership not apply to links?

## Link Ownership: The Creator Owns the Link

The answer is unambiguous: **the person who created the link owns it.** Ownership is determined by the link's *home document*, not by the documents it connects.

### The Core Rule

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user."
> — [LM 4/41]

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document."
> — [LM 4/12]

This is a deliberate separation of **ownership** from **application**. A link lives at an address in the creator's document space. That address determines who controls it — regardless of what content the link connects.

### Out-Links vs. In-Links

Nelson draws a sharp distinction between links you made (out-links) and links others made pointing to your content (in-links):

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not."
> — [LM 2/31]

If I create a comment link from my document to yours, that link is **mine**. It lives at my address. You cannot delete it, modify it, or prevent it. You control your content; I control my links.

### Why This Matters

This design solves the **marginalia problem**. In the paper world, your notes in your copy of a book don't reach anyone else. In Xanadu, your annotations are links that you own, stored at your address, but visible to anyone reading the annotated material. The target author has no veto power over your commentary.

It also explains why **published documents cannot be withdrawn**:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process."
> — [LM 2/43]

Other users' links — which are *their property* at *their addresses* — depend on the continued existence of the target content. Withdrawing a published document would break other people's property.

### The Address Structure Confirms This

Links within a document occupy the `2.x` subspace of that document's tumbler address:

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.755  → 755th link in document
```

The `N.0.U.0.D` portion encodes node, account, and document — which identifies the owner. The link's permanent address is under the creator's account, not under the accounts of the connected documents' authors.

### Summary

| Question | Answer |
|----------|--------|
| Who owns a link? | The creator (owner of the link's home document) |
| Can the target author delete it? | No |
| Can the target author prevent it? | No — free linking is part of the publication contract |
| Can the creator delete it? | Yes — it's their property |
| Does ownership transfer? | No — the home address is permanent |
