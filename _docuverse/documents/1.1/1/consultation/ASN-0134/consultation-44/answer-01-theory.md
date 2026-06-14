## Question 1 [theory]

> Was document creation intended to draw addresses from an account-level owned-numbers sub-allocator — the account handing out contiguous document addresses by order of arrival, exactly as a document hands out content addresses — or did the design leave document-address freshness unspecified?

I'll verify the exact wording on the pages dealing with forking, the document field, and link allocation order before answering—this is a precise design-intent question where the gap between "specified mechanism" and "specified freshness discipline" matters.

`★ Insight ─────────────────────────────────────`
The question hinges on a distinction that's easy to blur: there is a difference between specifying the *allocation mechanism* (who hands out document numbers) and specifying a *freshness/ordering discipline* (that they come strictly by order of arrival). Nelson states one explicitly for links — I need to check whether he extends it to documents.
`─────────────────────────────────────────────────`

Let me read the relevant raw pages to confirm exact wording.
