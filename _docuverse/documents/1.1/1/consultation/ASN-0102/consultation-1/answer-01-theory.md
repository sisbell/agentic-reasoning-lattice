## Question 1 [theory]

> Is COPY intended to operate exclusively on the content subspace, or is placement of existing content into the link subspace also within its intended scope?

## Short answer

COPY is intended to operate on the **content (byte) subspace** — it transcludes content and places it at a V‑stream byte position. Placement of content *into the link subspace* is not within its intended scope. The link subspace is governed by a different discipline (creation‑order, non‑rearrangeable addresses) and is populated by `MAKELINK`, not by `COPY`.

## The reasoning from the sources

**1. COPY's destination is a V‑stream byte address.** The operation is defined as:

> "The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>." (4/67)

The destination is a `doc vsa` — a *virtual stream address*, i.e., a byte position in the content stream. Nelson describes the vstream byte address explicitly:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

The link subspace, by contrast, is *not* addressed by byte position. Links live in the `0.2.N` subspace, distinct from the `1.x` byte stream (see `links.md`, citing 4/31).

**2. COPY is the transclusion operation — about content identity.** Per the transclusion FEBE mapping, COPY is "the transclusion operation - reference, not copy," sharing I‑addresses with the source. Its whole purpose is making content appear at a byte position while preserving its Istream origin:

> "Non-native byte-spans are called inclusions or virtual copies." (4/11)

This is content semantics, not link placement.

**3. The link subspace cannot receive arbitrary placement.** Links keep permanent creation‑order addresses:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

And links are not rearrangeable in the way bytes are — the link‑address is "designating the link's serial position" (per `i-space-addresses.md`, 4/30). You cannot "copy" content into a chosen slot of the link subspace because that subspace has no positional addressing under user control; it grows only by arrival order. Links are instead created and maintained by the back end:

> "It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." (4/41)

Creation of a link is the province of `MAKELINK`:

> "This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. It returns the id of the link made." (4/68)

**4. Why COPY needn't touch the link subspace anyway.** Because COPY shares the source's I‑addresses, any links attached to the copied bytes remain discoverable through those shared addresses via correspondence/refractive following:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version." (2/26)

So there is no design need for COPY to deposit link objects into the destination's link subspace.

## One caveat on the source-side spec-set

There is a subtlety worth flagging. Both `RETRIEVEV` and `COPY` take a "spec set," and `RETRIEVEV` "returns the material (text and links) determined by <spec set>" (4/67). This shows a spec‑set *can* designate links, which leaves open the narrow question of how COPY treats links that fall within its source span. The curated text I have describes COPY's destination unambiguously as a byte vsa (content subspace) but summarizes rather than reproduces the full COPY definition.

NEED_RAW: 4/66–4/67 (to confirm verbatim whether COPY's source spec-set is restricted to text, and whether any link-handling on copy is specified).
