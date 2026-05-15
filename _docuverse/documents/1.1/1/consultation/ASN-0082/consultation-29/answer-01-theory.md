## Question 1 [theory]

> Does Xanadu's design define INSERT for the link subspace (V_2), or is INSERT specified only for the text subspace by analogy with DELETEVSPAN's "vspan" prefix?

# INSERT and the Link Subspace

**INSERT is defined only for the text subspace.** The FEBE specification at 4/66 takes a `<text set>` parameter and explicitly describes character displacement:

> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

There is no `INSERTLINK` or analogous operation in the 17 FEBE commands. New links are created via **MAKELINK** (4/68), which creates a link and returns its ID — it does not place the link at a chosen position.

## The Architectural Reason

The link subspace doesn't *have* positional semantics that INSERT could operate on. Per 4/31:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document."

Link addresses are `N.0.U.0.D.V.0.2.1`, `N.0.U.0.D.V.0.2.755`, etc. — sequential by creation order, not rearrangeable. Bytes get V-addresses that shift with editing; links get serial IDs that never move. INSERT presumes a positional sequence into which content can be wedged; the link subspace by design has none.

## On the "vspan" Prefix

DELETEVSPAN's prefix names the *operand type* (a V-span), not a subspace restriction. INSERT takes `<text set>` for the same reason — it is a parameter-type label. The asymmetry between INSERT (text-only) and DELETEVSPAN (span-typed) reflects the asymmetry between the two subspaces: bytes have a positional V-stream that can be inserted into; links have a creation-order register that can only be appended via MAKELINK.

## Nelson Flags This as Open

He explicitly notes that link addressing could be extended but isn't:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

So: **No INSERT for V_2.** Creation is MAKELINK; the link gets the next ordinal in 0.2.N; there is no positional insertion semantics defined.
