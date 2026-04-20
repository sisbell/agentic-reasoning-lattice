## Question 2 [nelson]

> When a document maps several consecutive positions to content that originates from different sources, is there a unique way to split that mapping into the fewest contiguous pieces that each reference one original span?

## Yes — the minimal span decomposition is unique

The uniqueness follows from three structural properties of the system that I specified:

### 1. V-space is a dense linear sequence

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

V-positions form a contiguous sequence 1, 2, 3, ..., n with no gaps. Every position maps to exactly one I-address.

### 2. I-space addresses are totally ordered on the tumbler line

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse, (or merely to a series of elements of the same type, which is a degenerate case of a subtree)." [LM 4/24]

The tumbler line imposes a total order. Two I-addresses are either adjacent on this line or they are not. There is no ambiguity — content from different documents cannot be adjacent because the document boundary creates a gap on the tumbler line.

### 3. Content identity is based on creation, not value

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Two independently created bytes with identical content have *different* I-addresses. Transcluded bytes *share* the original's I-address. The V→I mapping is therefore a well-defined function.

### Why uniqueness follows

Given the mapping V→I, define a **break** at V-position *v* whenever I(*v*) is not the tumbler-successor of I(*v*−1). A break is **forced** at every such point: no single contiguous I-span can bridge a discontinuity in the I-address sequence. Conversely, where I(*v*) *is* the successor of I(*v*−1), introducing a break would only *increase* the piece count without necessity.

The minimal decomposition therefore has exactly one span per maximal run of V-consecutive positions whose I-addresses are also consecutive on the tumbler line. The break points are determined entirely by the mapping — there is no choice involved.

This is, in mathematical terms, the unique run decomposition of the V→I mapping's first difference. It is the same reason that run-length encoding of a sequence is unique: runs are maximal by definition, and maximality leaves no room for alternative groupings.

### Architectural significance

This uniqueness is load-bearing. The POOM enfilade maps V→I, and spans are the currency of every FEBE operation:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

If the span decomposition were ambiguous, two representations of the same document could disagree on how to partition the V-stream, which would make COPY, RETRIEVEV, FINDDOCSCONTAINING, and SHOWRELATIONOF2VERSIONS produce inconsistent results. The system depends on a canonical representation of document structure as a span list — and the uniqueness of the minimal decomposition is what makes that canonical form possible.
