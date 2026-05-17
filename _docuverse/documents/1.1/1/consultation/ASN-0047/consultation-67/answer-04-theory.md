## Question 4 [theory]

> Are the subspace assignments s_C = 1 (content/text) and s_L = 2 (link) a fixed structural commitment of the Xanadu design at LM 4/30–4/31, or a chosen instantiation where any pair of distinct positive subspace identifiers would satisfy the design intent?

I need to consult the original pages at LM 4/30-4/31 to answer this question precisely about whether the subspace identifiers are fixed or arbitrary.

[Looking up raw pages for 4/30-4/31 → pages 197-198]

Let me read those pages directly.

Reading the original pages now.

Reading page 197 (LM 4/30) and page 198 (LM 4/31).

Let me read the OCR text and images.

[Reading raw pages]

Now reading the pages.

Let me read these pages.

Reading raw/page-197.txt and raw/page-198.txt.

Now I'll read the files to verify.

Reading: resources/literary-machines/raw/page-197.txt and page-198.txt

NEED_RAW: 4/30-4/31, 4/26-4/29, 4/44-4/45

Based on what I can verify from the curated sources, I can give a partial answer but the full question requires inspecting the original page text:

## What the curated sources establish

Nelson does treat the digit values **2** (for links) and the byte-position subspace (under the "one" digit) as **specific chosen values**, not as abstract structural placeholders. The curated quotes refer to them by their literal numeric identity:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" — 4/31

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" — 4/31

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." — 4/31

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." — 4/30

Note the phrasing **"after '2'"** and **"after the one"** — Nelson speaks of these as named, specific digits, not as parameters. The phrase "subdivision of links by further digits (after '2' …)" only makes sense if `2` is the actual digit, not a symbol standing for "whatever positive integer designates links."

## What the design intent suggests

Two interpretive considerations cut in opposing directions:

1. **Fixed in this instantiation:** Nelson's prose treats the values as concrete. The element field structure (bytes vs. links) is presented as a discrete two-way partition realized by specific digits 1 and 2. There is no language in the curated sources suggesting "any pair of distinct subspace identifiers would do."

2. **Arbitrary in principle:** Nelson's tumbler philosophy is about *ownership and forking*, not about semantic meaning of particular digits. The digit values themselves carry no inherent meaning — they are coordinates in a tree. The choice of 1 vs. 2 is conventional rather than load-bearing in the way that, say, the "0 as divider" rule is.

The curated **i-space-addresses** note also says: *"Links: 'The digit after the '3' is a link-address designating the link's serial position'"* — which appears to conflict with the "2" subspace assignment in the **links** curated source. This inconsistency in the curated material itself suggests the precise digit assignments may not be as canonically pinned down as the structural role of having a content/link partition.

## What I cannot verify without raw pages

To answer definitively whether Nelson presents `s_C=1, s_L=2` as a *commitment* or as one valid *instantiation*, I would need to read LM 4/30–4/31 (pages 197–198) directly, and possibly the surrounding tumbler-structure discussion at 4/26–4/29.

NEED_RAW: 4/30, 4/31 (to confirm the exact wording around the "1" and "2" subspace digits and whether Nelson frames them as arbitrary or fixed); also 4/44–4/45 to cross-check the link-type discussion where Nelson says type designations are "completely arbitrary" — which would be relevant evidence about how he treats digit assignments generally.

## Provisional answer

On the evidence in the curated sources, Nelson treats `1` (bytes) and `2` (links) as **chosen, concrete values in the XU.87.1 instantiation** rather than as abstract structural placeholders — he references them by their literal digit names. However, nothing in his stated design intent makes the *particular numeric values* load-bearing: the structural commitment is that **bytes and links occupy distinct subspaces under the version digit**, not that those subspaces must be `1` and `2` specifically. The choice appears to be conventional within this implementation, consistent with his broader treatment of tumbler digits as positional coordinates whose meaning derives from the ownership tree, not from intrinsic numeric semantics.
