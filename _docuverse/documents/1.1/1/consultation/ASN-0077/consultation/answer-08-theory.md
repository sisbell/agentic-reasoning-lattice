## Question 8 [theory]

> Must origin identification work uniformly for spans of any size, from a single character to an entire document?

Yes. Origin identification works uniformly across all scales — this is a foundational design property, not a feature that varies with span size.

**The structural basis:**

Every byte has a permanent Istream address with the form `Node.0.User.0.Document.0.Element`. The Document field encodes origin directly. Since spans are defined by tumbler boundaries, origin identification reduces to examining I-addresses — which works identically whether the span contains one byte or the entire docuverse.

**Nelson's explicit commitment to uniformity:**

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

The phrase "any specific word or character" establishes the smallest scale. The addressing system extends seamlessly upward:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server—or the entire docuverse." (4/38)

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." (4/24)

**The design intent:**

From the spans concept: *"Nelson designed the tumbler system specifically so that spans work naturally from the smallest to largest units... This eliminates the need for different reference mechanisms at different scales."*

This is what I called **uniform reference at all scales**. There is no special syntax for "one byte" vs "one document" vs "everything" — it's all spans, just with different boundaries. Origin identification follows the same uniformity: a single mechanism resolves home document for any span, because the I-address of any byte within the span carries that information structurally.

**Why this matters semantically:**

If origin identification worked differently at different scales, attribution would become a scale-dependent privilege rather than a structural guarantee. Quoting one character would have different attribution semantics than quoting a paragraph — which would break the principle that *"attribution cannot be severed by operations within the system."* The uniformity is what makes the attribution guarantee meaningful.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

This mechanism applies identically whether you're requesting one byte or a million.
