# Metalinks

Source: Literary Machines, 4/52

## Semantic Intent

### What It Means

Metalinks are links that apply to whole documents rather than to passages within them. They answer questions about the document as a unit: Who wrote this? What is it called? Has it been replaced by something newer?

Nelson distinguishes metalinks from "ordinary text links" because they operate at a different level. An ordinary link might connect a paragraph to a comment, or a quotation to its source. A metalink says something about the entire work—it provides metadata through the link mechanism rather than through special fields or headers.

This is an architectural insight: instead of having separate systems for metadata (title fields, author fields) and for connections (links), Xanadu unifies them. A title is just a link from the title text to the whole document. An authorship claim is a link from the author's name to the work. This means metadata participates in the same universal web of connections as everything else.

### User Guarantee

**Document-level information is discoverable through the same mechanism as any other connection.** You don't need special queries for "what is the title" versus "what links to this"—both are link traversals.

### Principle Served

Metalinks embody Nelson's principle that the docuverse is a unified space of interconnection. Metadata is not a separate system bolted onto documents—it's woven into the same fabric of links. This means:

- Author attributions can be challenged (someone can link to "claim" authorship)
- Titles can be disputed (alternative title links can exist)
- Supersession is explicit and discoverable (not hidden in system fields)

The social dynamics of authorship and naming become visible in the link structure itself.

### How Users Experience It

- Look up a document's title by following its Title metalink
- See who claims authorship through Author metalinks (potentially disputed)
- Check if a document is obsolete via Supersession metalinks
- All these queries use the same link-traversal interface as any other

### Nelson's Words

> "METALINKS: These are links expected to apply to whole documents, whether from outside or from inside." (4/52)

> "While the title and the author's name ordinarily reside inside a document (though not necessarily at the beginning), the 'author' and 'title' links will normally go from the author's name and the principal appearance of the title to the whole document." (4/52)

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." (4/52, footnote)

## Examples from Literary Machines

Nelson lists three metalink types on page 4/52:

**Title** — Links the title text to the whole document it names.

**Author** — Links the author's name to the whole document they wrote. Can originate from inside the document (self-attribution) or outside (external attribution or dispute).

**Document Supersession Link** — Declares that one document or version has been replaced by another. See [supersession-link.md](supersession-link.md) for full extraction.
