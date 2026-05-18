## Question 7 [theory]

> Does Nelson's design require the bootstrap node address to be specifically `[1]`, or is it any single-component positive tumbler with `[1]` as the canonical convention consistent with the single root authority (LM 4/17–4/22)?

Reading the relevant page to verify the curated quote.

[I'll read page 195 (LM 4/28) for direct verification.]

Based on the curated sources, I can answer directly with high confidence. Let me read the original page to confirm the canonical passage.

Specifically `[1]`. Nelson's design requires it.

The decisive passage is at LM 4/28:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position."

This is not stylistic convention — it is structurally and semantically required, for two interlocking reasons:

**1. Single root authority (LM 4/17–4/22).** All numeration descends by forking from one source. As Nelson puts it: *"The basic principle is that of owned numbers... Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers"* (4/17). Because *"so the docuverse is all really one big forking document"* (4/18), there must be a single canonical root from which the tree descends. Any other single-digit choice would mean either (a) multiple roots — contradicting the forking model — or (b) an arbitrary relabeling that breaks point 2 below.

**2. The "1 means all of" convention.** Nelson reserves the digit "1" with a specific span semantic: *"A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server—or the entire docuverse"* (LM 4/38, via the spans extraction). The reason the root must be `[1]` specifically — not `[2]` or `[7]` — is that this is what lets the single digit "1" in the first position refer to "the entire docuverse." Nelson makes the link explicit at 4/28: the redundancy of "always 1" is paid for in exchange for this addressing affordance.

**So the framing in your question collapses:** there is no "single-component positive tumbler with `[1]` as canonical convention" interpretation that survives Nelson's text. The single root authority and the "1 = all of" convention together force the bootstrap node to be `[1]`. A different number would either fragment the root or invalidate the docuverse-wide "1" span — both of which Nelson's design explicitly relies on.
