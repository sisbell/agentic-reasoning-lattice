## Question 3 [theory]

> Does Nelson's design attach any meaning to where in its home document a link sits in the V-stream (e.g., a required structure or ordering for link positions), or is the placement of the first link an implementation-free choice?

The raw page images aren't readable in this session (no file-reading tool is enabled), so this answer rests on the curated, verified extracts above. They cover the question well, with one discrepancy I flag at the end.

## Short answer

Nelson's design attaches exactly one meaning to a link's position in its home document, and it is mandated, not an implementation choice: **link addresses record the permanent order of arrival** (creation order). Beyond that chronology, the position carries no structural or semantic meaning — and links don't actually sit in the text V-stream at all.

## The details

**Links live in a separate subspace, not among the text bytes.** A document's element field divides into a byte subspace and a link subspace. Link addresses take the form `N.0.U.0.D.V.0.2.N` — Nelson's own examples are "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" and "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" [LM 4/31]. So a link has no position interleaved with the document's text; "where the link sits" means only "which slot in the link subspace."

**Within that subspace, ordering is specified by Nelson: permanent order of arrival.** "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]. The "first link" is simply whichever link was created first; its number 2.1 is assigned mechanically by arrival and is permanent. An implementation is *not* free to place it elsewhere or renumber it. This contrasts with text bytes, whose V-stream order "may be continually altered by editorial operations" [LM 4/30] — note that REARRANGE is defined only over text: "Rearrange transposes two regions of text" [LM 4/67]. The curated extract of the I-address structure states explicitly that links are currently not rearrangeable. Permanence of these slots is load-bearing: link addresses are themselves link targets (the link-to-link mechanism, where a to-set can "point to the actual link address in the tumbler line, with a span of 1" [LM 4/49]), and the general guarantee that "new items may be continually inserted in tumbler-space while the other addresses remain valid" [LM 4/19] would break if link positions were an implementation whim. The curated material's claim that deleting link 2.5 does not renumber 2.6 onward is a curator inference from "permanent order of arrival," not a verbatim Nelson statement, but it follows directly.

**The position carries no content-structural meaning.** A link's slot says nothing about where in the document it applies, or even that it applies to the document at all: "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]. So there is no required correspondence between link order and text structure — residence means ownership, the serial number means arrival time, and that's the whole story.

**Nelson left room for more structure but didn't define it.** "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]. Any structure *below* the serial position is explicitly open territory.

## Caveat

The curated sources contain a discrepancy worth checking against the originals: the I-address extract (sourced 4/26–4/30) quotes "The digit after the '3' is a link-address designating the link's serial position," while the 4/31 examples and the rest of the corpus consistently show links under the `0.2` subspace. Whether the '3' is an OCR/curation artifact or reflects something real on the page affects only the subspace digit, not the order-of-arrival conclusion. NEED_RAW: [4/30-4/31]
