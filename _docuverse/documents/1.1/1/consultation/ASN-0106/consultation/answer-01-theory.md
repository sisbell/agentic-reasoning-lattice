## Question 1 [theory]

> When several spans of one document are read together, what must the system return as a single result rather than a loose collection of separate pieces?

## Answer

The system must return a **span-set** (also called a "spanset" or "request set") — a single, structured collection of spans treated as one unit — not a loose bag of disconnected fragments.

When you want several separated pieces of a document at once, Nelson's design requires those pieces to be expressed and handled as a coherent set of spans, each a simple "from-to" range, that together cover *exactly* what is wanted and nothing else:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

> "A request set is a set of spans, or spanset, presented to the back end in the FEBE protocol... The manipulation of request sets is an important aspect of what front-end functions do." (4/37)

This is the unit that travels through the protocol as a single result. The relevant FEBE operations all take or return span-sets rather than enumerated loose pieces:

- **RETRIEVEV** "returns the material (text and links) determined by `<spec set>`." (4/67)
- **RETRIEVEDOCVSPANSET** "returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." (4/68)

### Why a single set, not loose pieces

Two principles in the curated sources support returning a unified set:

1. **Spans are content-defined, not counted.** A span's contents are implicit in its boundaries, so a set of spans is a precise designation of "exactly these regions," determined by the address structure rather than by listing fragments:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

2. **The part you ask for is materialized as a whole (part-pounce).** Even though the underlying content lives in scattered fragments, the system assembles it into the coherent thing you requested:

> "When you 'go to' a certain part of a document, the whole document is not ready to show; yet the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." (2/16)

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." (2/16)

So: several spans read together come back as one **span-set** of material, structurally unified and exact, rather than a loose collection of separate pieces.
