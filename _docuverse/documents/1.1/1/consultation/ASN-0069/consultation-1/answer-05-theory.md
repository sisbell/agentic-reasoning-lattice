## Question 5 [theory]

> Does the design require that a fork preserve V-positions and V→I mappings literally (same tumblers, same images), or does it only require that the inherited content be reachable from `d_new` in some structurally faithful way (admitting rebased V-positions or rearranged correspondences)?

# Fork Semantics: Structural Faithfulness, Not Literal V-Preservation

The design requires structural faithfulness through shared Istream origin and computable correspondence — **not** literal preservation of V→I mappings as identical tumblers/images.

## What the spec actually says about the fork

CREATENEWVERSION reads:

> "This creates a new document with the contents of document `<doc id>`. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The phrase "with the contents of" speaks of *contents* — the Istream identity of the bytes — and "ancestry" is carried by the document **id**, not by sameness of V-positions.

## What IS required

1. **Shared Istream origin.** The inherited bytes must remain Istream-identical, so transclusions and correspondence still hold. "Native bytes of a document are those actually stored under its control… all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

2. **Ancestry expressed in the address.** "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29] The fork is signaled by the new id, not by V-identity.

3. **Correspondence computable.** SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70] This operation is meaningful only because corresponding parts may sit at *different* V-positions; otherwise correspondence collapses to identity and the operation is pointless.

4. **Refractive link-following.** "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

## What is NOT required

**Literal V-position preservation across versions.** V-stream addresses are explicitly described as ephemeral and local:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Versions are *arrangements*, and arrangements are equal in standing:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

The whole point of separating Vstream from Istream is that the V-side may be rearranged while the I-side carries identity. If forks were required to freeze V-positions forever, prismatic storage would degenerate into copy-on-write file versioning.

## The prismatic metaphor settles it

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another." [LM 2/19]

A prism *refracts*. It does not transmit positions unchanged. The new version is faithful to the source by virtue of being the *same content* viewed through a different arrangement, and that faithfulness is recovered by correspondence — not by matching tumbler numerals.

## The fork moment, narrowly

The spec is silent on whether V→I must be bitwise identical at the *instant* of CREATENEWVERSION. Two readings are consistent with the design:

- **Natural default:** the fork begins with the same V-arrangement as the parent, because "with the contents of" is most simply read that way. This is the cheapest implementation and matches what users expect at t=0.
- **Permitted alternative:** a fork that begins with a rebased V-arrangement is still well-formed *provided* Istream identity is preserved and SHOWRELATIONOF2VERSIONS returns the correct correspondence. Nothing in [LM 4/66], [LM 4/29], or [LM 2/19] forbids this.

What is forbidden is a fork whose inherited content is **not reachable** from `d_new` as the *same* Istream bytes — because that breaks transclusion, breaks refractive link-following, and breaks the equivalence-of-arrangements principle. The invariant is reachability and correspondence, not numeral equality.

## Summary

| Property | Required at fork? |
|---|---|
| Shared Istream identity for inherited content | **Yes** |
| Ancestry encoded in `d_new` | **Yes** |
| Correspondence computable between `d_old` and `d_new` | **Yes** |
| V-positions identical (same tumblers, same images) | **No** — a sensible default at t=0, but not a design requirement; versions diverge anyway. |

The spec mandates *structural* faithfulness. Identical V→I mappings are a permitted starting state, not an obligation.
