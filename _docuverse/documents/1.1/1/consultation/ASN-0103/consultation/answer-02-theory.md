## Question 2 [theory]

> When a document is created empty, what does the design guarantee about its content — does it hold nothing, or some inherent starting state the user can rely on?

## An empty document holds *nothing* — zero content — but it does have *identity*

Nelson is explicit that the creation operation produces a genuinely empty document, not one seeded with any default or inherent content:

> "CREATENEWDOCUMENT: This creates an empty document. It returns the id of the new document." (4/65)

Two things are worth separating here — **content** and **identity** — because the design guarantees opposite things about each.

### Content: nothing to rely on
An empty document contains no native bytes, no transclusions, and no links. There is no inherent starting state — no default text, no placeholder, no boilerplate the user can count on. The Vstream arrangement is simply empty. This follows from how the Vstream works: it is a dense, contiguous sequence of byte positions, so a document with zero bytes has zero V-addresses. Content only enters through subsequent operations (INSERT, APPEND, COPY).

Contrast this with the *other* creation path, which deliberately is *not* empty:

> "CREATENEWVERSION: This creates a new document with the contents of document `<doc id>`. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

So if you want a starting state, you fork an existing document (transcluding its contents); if you want nothing, you create new. The design keeps these strictly distinct.

### Identity: permanent from the moment of creation
What the user *can* rely on immediately is the document's **address**. CREATENEWDOCUMENT "returns the id of the new document" — a permanent tumbler address — even though no bytes exist yet. This is consistent with Nelson's "ghost element" principle, where a position in tumbler-space is real and addressable even when nothing is stored there:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

So an empty document is an addressable container with a permanent identity but no contents — you can already link to it before you've written a single byte.

### Summary
- **Content guarantee:** holds nothing. No inherent starting state.
- **Identity guarantee:** a permanent, unique tumbler address exists from creation onward.
- **Want a starting state?** Use CREATENEWVERSION (forks contents), not CREATENEWDOCUMENT.
