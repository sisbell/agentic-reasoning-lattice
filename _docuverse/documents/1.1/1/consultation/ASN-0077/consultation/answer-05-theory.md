## Question 5 [theory]

> Does the design require that any user viewing a span be able to trace it back to its first appearance?

Yes, the design requires this. Origin traceability is **structural**, not optional — it's built into the addressing system itself.

## The Mechanism

Every byte has a permanent Istream address with the form `Node.0.User.0.Document.0.Element`. The Document field directly encodes the **home document** — the document where the byte was first created. Transclusions don't duplicate content; they reference the original I-address. So the "first appearance" is encoded in the address itself and cannot be severed.

## What I Explicitly Guarantee

From Chapter 2, in my discussion of windowing and compound documents:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. **You always know where you are, and can at once ascertain the home document of any specific word or character.**" — LM 2/40

This is a user-facing guarantee, not just an implementation detail. The compound document layered with transclusions ("glass panes") must always reveal the home document of any byte the user is looking at.

From Chapter 4, on how bytes work mechanically:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." — LM 4/11

The fetching mechanism itself requires going back to the home location — the connection cannot be hidden.

## FEBE Supports the Inverse Query Too

The protocol includes an operation specifically for tracing content to its sources:

> "This returns a list of all documents containing any portion of the material included by <vspec set>." — LM 4/70 (FINDDOCSCONTAINING)

A user (or front end on their behalf) can query: "Show me every document where this span appears" — and the back end answers from the index of I-addresses.

## Why This Matters

Origin traceability is a load-bearing guarantee for several other things I designed:
- **Attribution** — authors get credit automatically because origin is structural
- **Royalties** — the system knows whom to pay because the I-address says whose document the bytes came from
- **"Show me what this was originally"** — readers of derivative versions can always return to the source
- **The link freedom contract** — quoting without permission only works because attribution survives the quote

If users couldn't trace back to first appearance, the whole literary fabric I'm trying to weave would unravel. Traditional quotation strips attribution by copying; transclusion preserves it by reference. The design choice is deliberate and non-negotiable.
