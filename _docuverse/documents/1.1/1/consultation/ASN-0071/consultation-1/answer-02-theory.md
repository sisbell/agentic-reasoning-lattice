## Question 2 [theory]

> Does Nelson's notion of "containing" in FINDDOCSCONTAINING admit queries naming link-subspace positions, or is it restricted to content-subspace material?

I'll examine the relevant pages to ground my answer in what Nelson actually wrote.

[Read page-237.png] [Read page-230.png]

Let me check those pages directly.

[Read page-237.png] [Read page-230.png]
[Read 2 tool uses in parallel]

Based on the curated sources, here is what I can establish — and where the question runs past Nelson's explicit text.

## What Nelson Specifies

FINDDOCSCONTAINING is defined twice in the protocol chapter:

> "This returns a list of all documents containing any portion of the material included by <vspec set>." (4/70)

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (4/63)

Two clues here:

1. **The parameter is `<vspec set>`** — a virtual specification set, i.e., a set of spans in tumbler-space.
2. **"Material … regardless of where the native copies are located"** — the operation's reason for existing is to chase **transclusion**, the mechanism by which non-native bytes appear in a document's V-stream.

## What the Architecture Allows vs. What the Operation Means

Spans are universal. A span is "from here to there" on the tumbler line, and Nelson is explicit that spans can cover any subtree:

> "A tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." (4/24)

Link instances have tumbler addresses in the `0.2.N` subspace of their home document, so an arbitrary span *can* name them. There is no syntactic prohibition.

But the semantic of "containing" is asymmetric between bytes and links:

- **Bytes (`0.1.N`)**: Native to one document, but transcludable into any other. Many documents can "contain" the same byte. FINDDOCSCONTAINING is precisely the inverse-index for this many-to-one relation.
- **Links (`0.2.N`)**: A link has exactly one home. "A document includes only the links of which it is the home document." (4/31) Links are not transcluded the way bytes are — a link lives where it was created.

So if you asked FINDDOCSCONTAINING for a link-subspace span, the only document that could meaningfully be said to "contain" it is its home document — which you already know from the address itself. The operation would degenerate.

## My Reading

Nelson's "containing" tracks the transclusion relation. The whole point of the operation, as the FINDDOCSCONTAINING entry on 4/63 makes clear, is to find documents whose V-stream pulls in material whose native copy lives elsewhere. Links, by Nelson's own statement on 4/31, do not participate in that relation — they have one home, full stop.

So the operation is **restricted in semantic intent to content-subspace material**, even though the address scheme would not syntactically prevent a link-subspace span from being passed.

## NEED_RAW

NEED_RAW: 4/63, 4/70 — to confirm Nelson never gives a worked example using link-subspace addresses in `<vspec set>` for this command, and to check whether the formal command grammar on 4/70 narrows `<vspec set>` to byte spans.

The curated sources cover the conceptual basis but don't include the verbatim command grammar from 4/70 nor any example invocations. Reading those pages would let me state definitively whether Nelson's specification *syntactically* admits link spans or only narrates byte spans.
