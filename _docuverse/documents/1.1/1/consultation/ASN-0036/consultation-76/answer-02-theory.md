## Question 2 [theory]

> Did the strand-level design intend a strict invariant that a V-position's subspace identifier must equal the I-address subspace identifier of the content it maps to, or was the V-side/I-side subspace correspondence treated as an operation-layer concern outside the two-stream foundation?

# On Strand-Level Subspace Correspondence

The short answer: I did not formalize a strict V-to-I subspace-identifier invariant at the strand level. The Vstream/Istream distinction in my design operates primarily at the byte level, and the byte/link subspace separation was treated as a structural feature of the addressing scheme rather than as a formal cross-stream invariant.

## What I did specify at the strand level

The Vstream is fundamentally the **byte stream**:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

So within the byte domain, V-positions reference byte content — including non-native bytes via transclusion. The I-address of a transcluded byte points back to its home document's byte storage. The byte-ness is preserved by the *operations* (INSERT, COPY, etc.), not stated as a strand-level type invariant.

## What I said about the link subspace

Links live in their own subspace with different rules:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

The asymmetry matters: **links do not participate in Vstream arrangement the way bytes do.** Their creation-order addresses are permanent. So the question of "V-position subspace correspondence" doesn't apply to links in the same form as it does to bytes — links have no rearrangeable V-side to correspond from.

## Design intent vs. formal invariant

My emphasis at the strand level was on three things:

1. **Separating identity from arrangement** — content lives at a permanent I-address; documents arrange views of it
2. **Survivability through span-based linking** — links attach to bytes via I-addresses, not V-positions
3. **Recognizing links as first-class objects** with their own subspace and ownership

I did not write down "the V-position's subspace identifier must equal the I-address subspace identifier" as an axiom. The closest I came was treating the byte stream as the domain of Vstream addressing, which implicitly keeps byte-V to byte-I, but I did not formalize it.

## Where this belongs

Type-correspondence between V-side and I-side strikes me as an **operation-layer concern**. The strand-level foundation should make it *possible* to enforce — by carrying enough information in the addresses to distinguish bytes from links — but the invariant itself is a property of how operations like INSERT, COPY, MAKELINK, RETRIEVEV use the foundation. The operations would be malformed if they crossed subspaces inappropriately; the strand layer just provides the substrate.

If your implementation treats this as a foundation-level invariant, that is a reasonable defensive choice, but it goes beyond what I explicitly stated in the design.

## Caveat

NEED_RAW: 4/9-4/12 (V/I separation diagrams), 4/30-4/31 (subspace structure detail). The curated extracts cover the conceptual material but not in formal-invariant language. If you need to verify that no stronger statement exists in the surrounding text, those page images would be the place to look — particularly the diagram on 4/9 showing document contents states, and the discussion of element-field structure on 4/30.
