## Question 13 [theory]

> Does the Xanadu link design admit links with empty from-endset and to-endset (a "type-only marker"), or must F and G always be non-empty alongside the mandatory Θ?

# Does Xanadu admit type-only marker links?

## Short Answer

**Nelson explicitly admits one-sided links (one endset empty), but does NOT explicitly address links with both F and G empty.** The architecture leaves this ambiguous. The search semantics suggest each endset needs at least one span to be findable, but the "arbitrary collection of spans" framing does not formally forbid empty endsets.

## What Nelson Explicitly Says

### 1. The Three Endsets Are Symmetric

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

All three endsets follow the same convention — "arbitrary collection." "Arbitrary" could in principle include the empty collection, but Nelson never states this explicitly.

### 2. One-Sided Links Are Explicitly Admitted

From the raw text on page 4/48:

> "An important variation is the link with only one side, e.g. something pointing to material, but not from other material. The paragraph designator is an example." [LM 4/48]

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." [LM 4/48]

This establishes that *omitting an endset is allowed*, but the convention is to still use the first endset (F) to carry the single side. Nelson treats this as a case where the second side (G) is conventionally absent — not as a zero-sided case.

### 3. Search Semantics Suggest Non-Empty Endsets

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58, also 4/59]

This is the "AND of the ORs" principle. The phrasing "one span of each endset" strongly implies each endset must contain at least one span to participate in search at all. A link with empty F and empty G would only be discoverable through its type endset.

### 4. Ghost Elements Apply to the *Target*, Not the Endset Itself

> "What the 'type' designation points to is completely arbitrary... Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/44-4/45]

Ghost elements mean the *address pointed to* need not have stored content. They do **not** mean the endset itself can be empty — the endset still contains a pointer (a span of length 1) to that ghost address.

## The Architectural Gap

Nelson describes:
- ✅ Two-sided links (normal case) — F, G, Θ all non-empty
- ✅ One-sided links (4/48) — F non-empty, G omitted by convention, Θ non-empty
- ✅ Ghost-targeted endsets (4/45) — endsets pointing at addresses with no stored content
- ❓ **Type-only markers** — F empty AND G empty, only Θ non-empty — **never explicitly discussed**

NEED_RAW: 4/41-4/60 if you want a definitive answer on whether empty span-sets are formally permitted. The relevant search-semantics passage at 4/58-4/59 suggests they are not findable through ordinary link search, but Nelson does not state a creation-time prohibition.

## Design Intent Reading

If you asked me what I *intended*, I would say: a link is fundamentally a *connection*. The whole point of the mechanism is to bind spans together. A "link" that connects nothing to nothing — only carrying a type — is conceptually closer to a free-floating annotation or a tag than to what I called a "connective unit" [LM 4/41]:

> "A Xanadu link is a connective unit, a package of connecting or marking information." [LM 4/41]

For pure type-only markers, the natural Xanadu pattern would be a **one-sided link** [LM 4/48] — use F to mark the location being categorized, and use Θ to specify the category. That is the construct I explicitly designed for "pointing to material" without a counterpart.

So while the bare architecture probably does not *forbid* an empty-F, empty-G link, the semantic intent says: if you want a type-only marker, use a one-sided link and put the marked location in F.
