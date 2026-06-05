## Question 4 [theory]

> What does reading spans together reveal about the gaps between them that would remain invisible if each span were read on its own?

Reading spans together makes the **gaps legible as structure** — something a lone span can never show, because a single span carries no information about what lies outside its own boundaries.

## A span alone hides its own context

Nelson designed spans so that their contents are *implicit in their endpoints*:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

A span read in isolation tells you only "from here to there." It says nothing about what comes before, after, or — crucially — what was *cut out from the middle*. The boundary that matters most, the one between two spans, simply isn't visible from inside one of them.

## Span-sets make the gap deliberate

The gap only acquires meaning when spans are placed side by side as a span-set:

> "if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

"Including nothing else" is the key phrase. The gap between members of a span-set is not an accident or absence — it is an *active exclusion*. Read together, two spans assert "this, and this, but not what lies between." Read apart, that assertion vanishes.

## Editing turns one span into two — and the gap is the edit

This is where gaps become evidence. Links attach to bytes, not positions, so:

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end**." (4/43)

When a once-contiguous endset survives editing as a *broken, discontiguous set of bytes*, the discontinuity itself is the trace of the operation:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset" (4/42)

A single surviving fragment looks like ordinary content. Both fragments read together reveal that something was deleted or inserted *in the gap* — the gap is the shape of the edit, invisible until you see what it separates.

## Correspondence: the gaps *are* the differences

The clearest case is version comparison. `SHOWRELATIONOF2VERSIONS`:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70)

Each corresponding pair, read alone, is just "the same content." But laid against each other, the spans that *don't* pair up — the gaps between corresponding spans — are precisely what changed:

> "a facility that holds multiple versions of the same material... is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." (2/20)

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." (3/13)

Highlighting correspondence is the same act as exposing the gaps. What is *same* is the matched spans; what is *different* is everything in between. Neither version read on its own reveals an insertion or deletion — only the gaps between aligned spans do.

## The gap is a subtree, not a measurement

Finally, reading spans together reveals that the gap is *structural*, not a byte-count:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." (4/25)

So the space between two spans is itself a zone on the tumbler line — a subtree that may be empty now and full later:

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

## In short

A lone span is content with implicit, self-contained boundaries. Spans read *together* turn the space between them into information: a deliberate exclusion (span-set), the scar of an edit (survivability), the difference between versions (correspondence), or a fillable region of the docuverse tree. The gap is invisible from inside any single span because a span knows only its own endpoints — it takes juxtaposition to make the silence between them speak.
