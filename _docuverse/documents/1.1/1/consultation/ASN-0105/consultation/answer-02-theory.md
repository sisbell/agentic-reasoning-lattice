## Question 2 [theory]

> What relationship must the returned content bear to the document's arrangement at the precise moment the read occurs, and must it reflect that arrangement exactly?

## The Read Reflects the Vstream Arrangement Exactly

Yes. The content a read returns must correspond **exactly** to the document's Vstream arrangement — its current ordering of bytes — at the moment the read resolves. This is the heart of what I call *part-pounce*.

### Reads materialize the current arrangement on demand

When you read, you are not pulling a stored "whole document" off a shelf. You are asking the system to construct, then and there, exactly the part you named, in exactly the order the document presently arranges it:

> "This system is built around the assumption that you are reading from a screen, not from paper. When you 'go to' a certain part of a document, the whole document is not ready to show; yet the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." (2/16)

> "We call this pounce. You pounce like a cat on a given thing, and it seems to be there, having been constructed while you are, as it were, in midair." (2/16)

The guarantee is precise and total:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." (2/16)

That part is assembled per the Vstream — the *virtual byte stream* — which is the document's arrangement of content as it stands right now:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

`RETRIEVEV` is the operation that does this: "This returns the material (text and links) determined by `<spec set>`." (4/67) The spec-set names V-positions, so what comes back is whatever the current V→I mapping says lives at those positions.

### Why it must be exact, and why "exact" tracks editing

The arrangement is not fixed — it shifts with every edit — and the read must honor whatever the arrangement is at that instant:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

So the *content identity* (Istream) is permanent, but the *arrangement* (Vstream) is what a read reflects, and that arrangement is live. After an INSERT, the same content sits at different V-addresses; a read at those addresses returns the post-insert ordering, exactly.

### The time/version qualifier

"Exactly" means exactly the arrangement you addressed — which is normally the present version, but may be any past one. Because every prior arrangement is preserved, a read can target a specific version at a specific time, and it will faithfully reconstruct *that* arrangement:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)

So the relationship is one of **exact correspondence to a designated arrangement**: by default the document's current Vstream at the moment of the read, materialized faithfully from fragments; or, if you so specify, the exact arrangement of a named historical version. The read never returns an approximate or stale view of the version it is reading — it constructs precisely that arrangement on demand.
