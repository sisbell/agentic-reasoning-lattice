## Question 9 [theory]

> When material is transcluded from one document into a second, and from the second into a third, must containment carry through the entire chain so that every document in the chain appears in the result?

I'll examine the relevant operations and concepts. This question hinges on how FINDDOCSCONTAINING interacts with multi-level transclusion, so let me check the raw pages for the operation's specification.

Let me identify the right files first.

`★ Insight ─────────────────────────────────────`
The key tension: "the chain" (A→B→C as a derivation lineage) versus "containment" (which documents actually hold a given byte). These are different things in Xanadu, because transclusion preserves I-addresses — it doesn't create a layered pointer-chain in storage.
`─────────────────────────────────────────────────`
