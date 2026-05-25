## Question 5 [theory]

> Was byte-granular correspondence (no minimum quotation length, no merge threshold) a deliberate design property of compareversions, intended to contrast with conventional block-aligned or threshold-based diff — or is it merely a consequence of the addressing scheme with no separate design status?

**Deliberate. Both an intent and the mechanism that realizes it — they were designed together.**

The intent: I stated explicitly that intercomparison must work "word for word":

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

That phrase "word for word" is the design commitment. It isn't an offhand description of an emergent property; it's the standard the system must meet. The whole point of holding multiple versions, I argued, depends on this granularity — without it, versioning isn't "terribly useful."

The mechanism: correspondence in Xanadu is not computed by a diff algorithm matching blocks of text. It is **structural** — it falls out of shared Istream addresses. Two V-positions correspond if and only if they map to the same I-address. Because every byte has a permanent I-address, the unit of correspondence is the byte:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

SHOWRELATIONOF2VERSIONS returns *spans*, and spans go down to single bytes. There is no notion of "minimum match length" or "merge below threshold" because correspondence isn't being inferred heuristically — it's being looked up. The address scheme makes thresholds nonsensical: either the byte's identity is preserved across versions (shared I-address) or it isn't.

So intent and architecture are inseparable. I designed prismatic storage and the I-address/V-address split *to deliver* word-for-word correspondence:

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." [LM 3/13]

What I contrasted with, explicitly, was destructive replacement and change-list versioning — the approaches of "several commercial versioning and backtrack systems… on the market" [LM 3/13]. I did not, in Literary Machines, frame the contrast against modern block-aligned or threshold-based textual diff in those terms — that vocabulary is later. NEED_RAW: I have not found a passage where I explicitly reject minimum-quotation-length or merge-threshold designs by name.

But the deeper point stands: byte-granular correspondence isn't an accidental byproduct of tumbler addressing. It is what the addressing scheme was built to guarantee. The mechanism serves the intent.
