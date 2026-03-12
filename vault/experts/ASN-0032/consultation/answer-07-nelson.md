## Question 7 [nelson]

> Can a link ever be destroyed or retracted, or does permanence mean that once a link exists it must exist forever?

## Link Deletion in Xanadu: Yes, But Never Truly Destroyed

A link **can** be deleted by its owner — but "deleted" in Xanadu does not mean what it means elsewhere. The link enters a liminal state: gone from current view, but not destroyed.

### The Owner Can Delete

Links are owned property. The owner of a link's home document can remove it, just as they can delete bytes from their document:

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

Nelson's technical diagram on page 4/9 explicitly lists **"DELETED LINKS"** as a valid document state, parallel to deleted bytes:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

### But Deletion Is Not Destruction

This is the critical Xanadu distinction. A "deleted" link is:

1. **Not currently addressable** — it disappears from the document's active view
2. **Awaiting historical backtrack** — it remains recoverable through version history
3. **Potentially alive in other versions** — if someone versioned your document before you deleted the link, their version still contains it

This follows the same principle as content deletion. Nelson rejects "destructive replacement" across the entire system. The append-only storage model means the link's I-space record persists even after V-space removal.

### Who Can and Cannot Delete

| Actor | Can they delete the link? |
|-------|--------------------------|
| Link owner (home document owner) | **Yes** — it's their property |
| Target document author | **No** — they can delete *content* the link points to, but not the link itself |
| Anyone else | **No** — ownership is absolute |

This asymmetry matters. If I link to your published document with a critical annotation, you cannot remove my link. You can only delete the content it points to — which would cause the link to lose its anchor (surviving only "if anything is left at each end" [LM 4/42]).

### The Permanence Tension

There is a real tension in Nelson's design between two principles:

**Permanence of addresses:** "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19] — the link's tumbler address never becomes invalid.

**Owner's right to withdraw:** "Only the owner has a right to withdraw a document or change it." [LM 2/29] — the owner can remove their own links.

Nelson resolves this through the V-space/I-space separation. The link's *address* in I-space remains permanently assigned. The link's *presence* in the document's current V-space arrangement can be removed. Historical backtrack can reconstruct the state where the link existed.

### Published Documents Add Friction

For published documents specifically, withdrawal is harder:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

Since links live inside documents, a published document's links inherit this friction. Nelson doesn't specify whether individual links within a published document can be deleted independently of the document itself — but the "deleted links" state on 4/9 applies to document contents generally.

### Summary

Once a link exists, it can be **retracted from current view** by its owner, but it is **never truly destroyed**. The I-space record persists, version history preserves it, and other versions may still contain it. Permanence in Xanadu means the *record* of the link's existence survives even the owner's decision to remove it — you can always reconstruct the moment when it was there.
