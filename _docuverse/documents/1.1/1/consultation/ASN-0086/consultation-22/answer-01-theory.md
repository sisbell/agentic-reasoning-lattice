## Question 1 [theory]

> Did Nelson's link design intend links to be sited only at element-field depth 2, or did it admit deeper-sited links (e.g., links spawned as children of other links)?

# Did Links Admit Deeper Siting Than Depth 2?

**Deeper-sited links were admitted, not excluded.** The depth-2 case (`N.0.U.0.D.V.0.2.N`) is the standard XU.87.1 form, but I made the extension explicit:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

This sits inside a broader design commitment: every numbered item is a forking item. As I wrote on the docuverse as a whole:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

> "So the docuverse is all really one big forking document." [LM 4/18]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

By that principle, a link — being a numbered item with a tumbler address — admits descendants on the same footing as a document, account, or node.

## Two Senses to Keep Separate

There are two notions of "deeper links" that are easy to conflate, and I admitted both but through different mechanisms:

1. **Link-to-link** (semantic): one link *points at* another link via its to-set. This is a property of the endset machinery — links have addresses, so links can be targets:
   > "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." [LM 4/49]

   The pointing link still sits at its own depth-2 address; only the *target* is another link.

2. **Address-tree depth below a link** (structural): a link sited *under* another link's address (further digits after `2.N`). This is what 4/31 explicitly allows — links subdivided like documents are subdivided into versions.

The two compose: compound and faceted link structures "may be built into arbitrary compound structures mapped to tumbler-space" [LM 4/51], and the address-space subdivision provides one natural home for the pieces.

## Verdict

The depth-2 standard is a XU.87.1 convention, not a design ceiling. The "subdivision of links by further digits" was kept open by intent. Implementations are free to flatten everything to depth 2 if they wish, but they should not claim that the design *forbids* deeper siting — it explicitly permits it.

NEED_RAW: 4/31 (to surface which specific "possible uses" were discussed beyond the brief mention)
