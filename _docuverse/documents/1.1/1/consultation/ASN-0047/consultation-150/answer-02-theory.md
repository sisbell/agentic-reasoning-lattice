## Question 2 [theory]

> Was a document's link-subspace V-position depth intended to be fixed permanently once chosen, or only while the link subspace is non-empty — and if permanent, why does the content subspace carry no analogous cross-state depth commitment?

The raw page files aren't present in this working directory, so I'll answer from the verified curated sources and flag where the question runs past them.

## Short answer

The curated sources let me firmly establish the *asymmetry* the question rests on, and explain *why* it exists — but they do **not** explicitly resolve the precise "depth fixed permanently vs. only while non-empty" distinction. That last refinement goes beyond what Nelson states. I'll separate the three layers.

## What is verified

**Link V-positions are permanent and cross-state.** A link's position in its home document is fixed by order of arrival and is never reassigned:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Concretely, link `2.1` is always the first link created, `2.755` always the 755th, and deleting link `2.5` does **not** renumber `2.6…2.N` (curated `links` entry, from 4/31). The two illustrative addresses Nelson gives:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

**Byte V-positions are mutable and version-local.** By contrast, the byte subspace position is the *current* ordering and is freely reshuffled:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)
> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

## Why content carries no analogous cross-state commitment

This is the heart of part 2, and it follows directly from the Istream/Vstream split. **Bytes carry two addresses; links effectively carry one.**

- A byte's *permanent identity* lives in the **Istream** (the I-address), which "never changes" (curated `i-space-v-space`). Its **Vstream** position is explicitly disposable: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing" (4/11). Because permanence is already guaranteed by the I-address, the V-position is *free* to mutate — there is nothing for a cross-state V-commitment to protect.

- A link, by contrast, is identified by its home-document order-of-arrival position. That position **is** its stable identity (it is what `RETRIEVEENDSETS`, link-to-link references, and type/instance addressing resolve against). There is no separate "link Istream" doing the permanence work, so the V-position itself must be the permanent anchor. Hence links are fixed in "permanent order of arrival" (4/31) while bytes are not.

So the answer to "why no analogous content commitment" is: **content's cross-state permanence is discharged by the Istream, not by its V-position; links have no such second address, so their V-position must itself be permanent.** The asymmetry is a consequence of where each thing's permanence is stored, not an arbitrary choice.

## Where the question runs past Nelson (flagging)

The question's sharper distinction — whether the link subspace's *depth* (number of digits beneath `…V.0.2`) is committed *permanently once chosen* or only *while the subspace is non-empty* (i.e., could an emptied link subspace be re-baptized at a different depth?) — is **not** settled in the curated material. The one passage that bears on link *depth* is deliberately non-committal:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

That is, Nelson treats further link-subspace depth as an open design avenue ("a distinct possibility… discussed"), not as a fixed, committed structure. Nothing in the verified sources states that a chosen depth is locked for all time, nor that it relaxes when the subspace empties. The permanence Nelson *does* assert is over link **ordinal positions** ("permanent order of arrival"), not over the **depth** of the subspace's digit structure.

Given the general tumbler invariant — "New items may be continually inserted in tumbler-space while the other addresses remain valid" (4/19) — the *natural* reading is that any depth, once it has baptized live addresses, is permanent (re-baptizing it would invalidate existing addresses, which tumblers forbid). That would make depth permanence a corollary of address permanence rather than a separately stated rule. But this is inference, not text.

To confirm the depth-specific intent (permanent vs. while-non-empty) and whether deletion ever frees a subspace for redefinition, I'd need the raw addressing pages:

**NEED_RAW: 4/29–4/31** (document/version/byte/link subspace structure and the "subdivision by further digits" discussion), and **4/23–4/25** (ghost elements + how spans/positions persist for emptied addresses).
