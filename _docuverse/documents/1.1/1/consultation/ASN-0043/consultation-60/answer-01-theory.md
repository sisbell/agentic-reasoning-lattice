## Question 1 [theory]

> Does the design requirement that "every link carries a type endset" mandate that the type endset be non-empty (referencing at least one span), or is it satisfied by the structural presence of a third slot that may be empty?

# Type Endset: Must Be Non-Empty, Not Just Structurally Present

The design intent is that the type endset **must reference at least one address** — the structural slot alone is not sufficient. The endset can point to a "ghost element" (an address where nothing is stored), but it must point somewhere.

## Reasoning from the curated sources

**1. The type endset is defined as something that points.** Nelson specifies it positively, not as an optional slot:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

"Pointing anywhere" presumes pointing somewhere.

**2. The search semantics require a non-empty type endset to be meaningful.**

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

"One span of each endset" — a type-constrained search has no span to match against if the type endset is empty. The link would be invisible to all type-based retrieval, which contradicts the type endset's stated purpose.

**3. Nelson explicitly addresses the "empty-target" case — and resolves it via ghost elements, not via empty endsets:**

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

The distinction is sharp: the *target* of the type pointer may be empty (ghost element), but the *endset itself* must contain a pointer. Nelson never says "the type endset may be empty" — he says the pointer may target an address with nothing stored there.

**4. The type endset's architectural role requires at least one address.** The whole reason for the third endset is categorization — search by address-match. An empty type endset would be untyped, defeating the design.

## A nuance: one-sided links

Nelson does describe "one-sided links" where one endset (from or to) is effectively absent — the paragraph designator example uses only the first endset [LM 4/48]. But this concerns from/to asymmetry, not the type endset. Paragraph links still carry a type designation (the "paragraph" type address).

## Caveat — NEED_RAW: 4/43-4/47, 4/58

The curated sources strongly imply the non-empty requirement but do not contain a verbatim sentence saying "the type endset must contain at least one pointer." If you need an explicit prohibition (vs. inferred from positive specification), the raw pages 210-214 and 225 should be read directly to confirm Nelson never permits a structurally-present-but-empty type endset.
