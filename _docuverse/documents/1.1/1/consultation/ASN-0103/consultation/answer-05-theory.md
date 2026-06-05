## Question 5 [theory]

> What does the design promise about a new document's relationship to the shared content store — does its creation add any content, or only a place to hold content?

## A new document adds a place, not content

The design is explicit: **creating a document allocates an address (a place to hold content) but adds nothing to the shared content store.** Content enters the store only through separate operations that actually deposit bytes.

### CREATENEWDOCUMENT produces an empty document

The operation that brings a document into being makes it empty:

> "This creates an empty document. It returns the id of the new document." (4/65)

What you get back is an *id* — a tumbler address — not stored content.

### Documents are "ghost elements" until content is stored under them

The ghost-elements concept settles this directly. Only bytes and links are physically stored; documents are merely positions on the tumbler line:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." (4/23)

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

So a freshly created, empty document is a ghost element — a conceptually assigned position with nothing in the store beneath it.

### Content is added only by later operations

The Istream/permascroll (the shared append-only store) gains content only when you deposit bytes:

- **INSERT** — "This inserts `<text set>` in document `<doc id>` at `<doc vsa>`." (4/66)
- **APPEND** — "This appends `<text set>` onto the end of the text space of the document `<doc id>`." (4/67)
- **MAKELINK** — creates a link (the other stored entity type) (4/68)

These are what actually add to the store. The Istream/Vstream model reinforces the separation: the store holds permanent content (Istream), while a document is fundamentally an *arrangement* (Vstream) over content — and a new empty document is an arrangement over nothing yet.

### Why the design works this way

This is the point of ghost elements and the "address population... is also an abstraction" (4/23): the address space is conceptually infinite and cheap, while storage is finite and fills in only occupied points. Creating a document costs only a baptized address under your account (see forking, 4/20); it imposes no storage cost and contributes no bytes to the docuverse until you write into it.

**Summary:** A new document's creation establishes only a permanent place — an addressable position (a ghost element) — and adds no content to the shared store. The store grows only when INSERT, APPEND, or MAKELINK actually deposit bytes or links.
