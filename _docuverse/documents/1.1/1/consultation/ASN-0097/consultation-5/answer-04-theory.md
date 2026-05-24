## Question 4 [theory]

> Did Nelson's design intend MAKELINK to admit endsets with no spans or with all-zero-width spans (yielding cov(e) = ∅), or was an endset always required to denote at least one I-address?

# Endsets and Empty Coverage

Nelson's design intent points to **endsets always denoting at least one I-address**, though he never addresses the empty or zero-coverage case explicitly. The evidence:

## Spans are inherently non-point

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

Nelson deliberately rejects point-based linking. A zero-width span collapses to a point — the very thing Nelson contrasts links against.

## Survivability requires content at each end

The diagram caption on page 4/43 is explicit:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

This is conditional: if NOTHING is left at an end, the link does NOT survive. An endset with cov(e) = ∅ would already be in that broken state at creation — there is nothing to attach to.

## Endsets are consistently framed as pointing somewhere

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" [LM 4/45, diagram caption]

The "arbitrary collection" language is about flexibility of selection (discontiguous, scattered) — not about admitting empty selection.

## The type endset has special license but still denotes addresses

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

This is the closest Nelson comes to allowing "nothing there" — but note carefully: the **address** is still denoted; only the **content stored at that address** may be absent. A ghost element is a position with zero stored content, not an empty endset. The type is matched by address, so the address itself must still exist:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

## Search semantics presuppose non-empty endsets

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

This requires "one span of each endset" — an endset with no spans cannot satisfy any search request and would be functionally undiscoverable.

## What Nelson does NOT say

Nelson does not explicitly define MAKELINK's behavior when handed an empty endset, nor does he prohibit it at the protocol layer. The signature on 4/68 simply states:

> "MAKELINK: This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. It returns the id of the link made." [LM 4/68]

No cardinality constraint is stated. The empty case appears to be an implementation question left unaddressed.

## Conclusion on intent

Reading the conceptual material as a whole, Nelson's vision is incompatible with cov(e) = ∅:

1. Links **connect** bytes — that is their definition
2. A link with an empty endset has nothing to connect on that side
3. Such a link would be unsurvivable from birth and unfindable by search
4. It contradicts the "strap between bytes" metaphor at the heart of the design

**From-set and to-set** were intended to denote at least one I-address worth of bytes. **The type endset** was intended to denote at least one address (possibly a ghost element with no stored content, but still an address). The empty/zero-coverage case falls outside the link concept Nelson was specifying.

NEED_RAW: 4/68 (page 235) and surrounding 4/61-4/70 — to confirm no FEBE-level discussion of endset validity at link creation time exists beyond the curated MAKELINK signature.
