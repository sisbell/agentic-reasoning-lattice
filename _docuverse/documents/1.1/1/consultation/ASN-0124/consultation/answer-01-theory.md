## Question 1 [theory]

> When the system is asked which documents contain any portion of a named set of content regions, what exactly must be returned — bare document identities, or identities paired with an indication of which queried material each document contains?

I'll examine the curated sources, which directly cover the `FINDDOCSCONTAINING` operation, and verify against the original pages.

The curated **Operations** entry gives two verified descriptions of this operation:

> **FINDDOCSCONTAINING**: "This returns a list of all documents containing any portion of the material included by `<vspec set>`." (4/70). "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (4/63)

Let me read the original protocol pages (4/63 = raw page 230, 4/70 = raw page 237) to confirm there's no additional detail about the return structure.

`★ Insight ─────────────────────────────────────`
The decisive evidence here is **comparison across operations**. Nelson is explicit when an operation returns *pairs*: `SHOWRELATIONOF2VERSIONS` "returns a list of ordered pairs." So the absence of "pairs" language in `FINDDOCSCONTAINING` is meaningful, not accidental.
`─────────────────────────────────────────────────`

Let me verify by reading the original pages.
