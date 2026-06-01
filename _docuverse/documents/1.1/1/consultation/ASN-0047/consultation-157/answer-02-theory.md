## Question 2 [theory]

> Is a document's text (content-subspace) V-position depth a fixed per-document property determined at first insertion, or may it legitimately differ each time the text is fully cleared and re-populated — and if links are fixed but text is not, what design distinction justifies the asymmetry?

I don't have file-read tooling exposed in this session (only inert MCP connectors), so I'll answer from the verified curated sources and flag anything that needs the raw pages.

## Short answer

A document's **content-subspace V-positions are not a fixed per-document property**. They are a transient *view* coordinate, recomputed on every editorial operation. So if the text is fully cleared and re-populated, the new text legitimately receives fresh V-positions — there is nothing "frozen at first insertion" about them. **Links, by contrast, are addressed by permanent order of arrival** and never renumber. The asymmetry is justified by *where each kind of object keeps its stable identity*.

## Why byte V-positions are not fixed

V-stream byte addressing is explicitly described as the *current ordering*, mutable by edits:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

INSERT confirms positions are recomputed, not forked:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

The curated V-space notes summarize the guarantee: V-addresses are *dense* ("there are no gaps") and start at 1, so they are a flat, contiguous index over the current arrangement. Clearing and re-populating therefore just yields positions 1..N again over the new content. There is no per-document constant being preserved.

## Why links are fixed

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

Deleting link 5 does not renumber 6..N — link addresses are creation-order and permanent.

## The design distinction that justifies the asymmetry

The key is that **bytes have two addresses but links effectively have one stable identity**:

- A byte's *permanent* identity lives in **I-space** (its home/native address). Links attach to bytes via that I-address, which is exactly why byte V-positions are free to churn — *"the links are to the bytes themselves, any links to those bytes remain stably attached to them"* (4/30). The V-position is just a disposable rendering coordinate; nothing depends on it.

- A link, however, has **no separate I-space identity to fall back on** — its address *is* its identity. Links are first-class, ownable, referenceable objects: other links can point at them (link-to-link, 4/49), and the search machinery matches on the link's *address* (endsets/types matched by address, 4/44–4/45). If a link's address were recomputed on edit, every reference to it and every indexed search result would be invalidated.

So the rule reduces to: **stable identity must live somewhere.** For content, it lives in I-space, freeing the V-position to be a recomputed view. For links, the address itself must carry the stability, so it is pinned to permanent order of arrival. This is the same V/I separation Nelson builds the whole model on — content is arrangeable (Vstream), identity is permanent (Istream) — applied consistently: links behave like I-space objects because they have nowhere else to anchor.

## Caveat on "depth" specifically

The framing in terms of V-position *depth* (tumbler nesting depth of the position field, and whether re-population could change it) is **not addressed verbatim** in the curated sources. What the sources establish is that content V-positions are a dense, flat, recomputed index (insertion renumbers rather than forks, 4/66) — which implies depth is not a frozen per-document constant but simply tracks the current arrangement. If you need a definitive statement on tumbler-digit depth under clear/re-populate cycles (as opposed to renumbering behavior), that goes beyond the curated text.

NEED_RAW: 4/30–4/31 (raw pages 197–198) to confirm exact content-subspace digit/depth wording and the "0.1" byte-subspace vs the "3"/"0.2" link-subspace discrepancy that appears between the curated links and i-space-address notes.
