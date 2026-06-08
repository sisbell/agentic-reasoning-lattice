## Question 6 [theory]

> How does placing content together from several separate, non-adjacent sources — rather than one continuous stretch — reveal the difference between genuine reuse and mere replication?

## Assembly from scattered sources as a provenance test

When you gather content from one continuous stretch, the result *looks* the same whether you transcluded it or copied it — a single block is a single block. But when you deliberately assemble fragments from **several separate, non-adjacent sources**, the structure forces the question: does each fragment still know where it came from? Genuine reuse (transclusion) preserves a *distinct origin per fragment*; mere replication collapses everything into one undifferentiated new block.

### Why discontiguity makes the difference visible

In Xanadu, content identity is based on *creation*, not *appearance*. As the provenance source puts it: "Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. This is how the system distinguishes 'wrote the same words' from 'quoted from the original.'"

A discontiguous assembly is precisely the case where this distinction has teeth. The endset mechanism is built to express it:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

And spans formalize the "scattered" selection:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

Each span in that set retains its own home location. So a compound document woven from many sources is not one block — it is many references, each resolving back to a distinct origin:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Non-native byte-spans are called inclusions or virtual copies." (4/11)

Because the fetch itself must go to the home location, the connection cannot be severed. No matter how many sources you braid together, you can always recover each one:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

### Genuine reuse vs. mere replication

Transclusion is reference, not duplication — the `COPY` operation "shares I-addresses with the source" (4/67), and `FINDDOCSCONTAINING` "returns a list of all documents containing any portion of the material" (4/70). So a non-adjacent assembly exposes its full lineage: every distinct source remains queryable, live, and creditable. This is what Nelson calls the "annotated collage" — "any new viewpoint can be freely presented by an easily-made annotated collage" (2/45).

Replication destroys exactly this. A copy flattens many origins into one inert mass:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." (2/48)

> "Water flows freely, ice does not... Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." (2/48)

### The reveal

So the test is this: take material assembled from several non-adjacent sources and ask the system "where did each piece come from?" Under **genuine reuse**, the discontiguity is preserved as a set of distinct I-addresses — the collage names its many parents, each still live, each still owed royalty, each still receiving new links. Under **mere replication**, the answer is uniform and impoverished: every fragment now reports the *same* new home, the original provenances erased, the bytes frozen. Continuous copying can hide this collapse behind a single seam; non-adjacent assembly cannot — it multiplies the seams, and each seam either traces home or it doesn't.

(Citations above are verified from the curated sources. I did not need raw pages for this answer.)
