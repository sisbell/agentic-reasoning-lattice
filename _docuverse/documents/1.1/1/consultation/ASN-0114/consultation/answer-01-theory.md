## Question 1 [theory]

> When a link's address is presented together with a selector naming one of its ends, what must the design guarantee the result represents about that single end?

## Answer

When you present a link's address together with a selector that names one of its ends (its from-set, to-set, or type), the design must guarantee that the result represents that **entire single endset** — the complete, possibly discontiguous, arbitrary span-set constituting that one end — and nothing collapsed, truncated, or substituted for it.

The crucial property is that an endset is **not a point and not necessarily a single span**. Each end of a Xanadu link is an arbitrary collection of spans pointing anywhere in the docuverse. So "the result for one named end" must be the whole span-set, faithfully:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." (4/43)

Because all three ends follow the same convention, the selector simply names *which* of the three symmetrical endsets to project; the guarantee is that the returned value is that endset in full:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

The FEBE operation that does exactly this projection is **RETRIEVEENDSETS**, which "returns a list of all link end-sets that are in `<spec set>`" (operations, 4/70). The address identifies the link; the selector picks the end; the result must be the entire span-set of that end.

### What the guarantee must preserve

1. **Completeness** — every span belonging to that end is included; the result is not reduced to a single representative point or span. (The endset "may be on a broken, discontiguous set of bytes," 4/42.)
2. **Discontiguity** — if the end touches several non-adjacent regions, the result is a span-set, not one collapsed range. (Curated `endsets.md` notes each endset "is an arbitrary span-set (can be discontiguous).")
3. **Location fidelity** — the spans map exactly to their positions in the universal address space: "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." (4/45)
4. **Identity, not content** — for the type end especially, the result is defined by *address*, not by what (if anything) is stored there: "The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44–4/45), and "Link types may be ghost elements." (4/45)

In short: naming one end of a link must yield a faithful, exact representation of that end as a complete arbitrary span-set in tumbler-space — the same generalized endset object the link was built from, neither narrowed to a point nor flattened to a single span.

---

One caveat on scope: the curated sources establish the *structure* an endset has and that RETRIEVEENDSETS projects it, but they don't give a verbatim statement phrased as "the result for one named end must be exactly that end's full span-set." That framing is my synthesis from the endset definition (4/42–4/45) plus the RETRIEVEENDSETS description (4/70). If you want Nelson's exact wording around RETRIEVEENDSETS and any per-end return guarantees, I'd check NEED_RAW: 4/68–4/70.
