## Question 1 [theory]

> When the system is asked which anchoring touches a region of content, must it return the touching material itself — the spans where links attach — rather than the identities of the links that attach there?

I'll examine this question carefully. It hinges on a precise distinction between two things a link carries: its **identity** (its own address) and its **endsets** (the spans where it attaches to content). Let me verify the exact semantics of the relevant FEBE operations against the original pages, since my curated sources show a small discrepancy in how `RETRIEVEENDSETS` is described.

Let me read the operations pages directly.

`★ Insight ─────────────────────────────────────`
The question sets up an opposition — "the touching material itself" (endset spans) vs. "the identities of the links." In Xanadu these are two different return values served by two different operations (`RETRIEVEENDSETS` vs. `FINDLINKSFROMTOTHREE`). Whether the framing's "rather than" holds depends on which question is actually being asked.
`─────────────────────────────────────────────────`

Let me check the raw pages to nail the exact semantics.
