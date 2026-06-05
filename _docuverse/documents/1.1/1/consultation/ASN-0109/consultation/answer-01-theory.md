## Question 1 [theory]

> When a link is read by its address, what must the system return about the content endpoints the link connects?

When a link is read by its address (the FEBE operation **RETRIEVEENDSETS**), the system must return the link's **endsets** — specifically the two *content* endpoints, the **from-set** and the **to-set**.

Per Nelson, the operation is defined simply:

> "RETRIEVEENDSETS spec-set / This returns a list of all link end-sets that are in spec-set." (4/70)

What each returned endset must convey:

1. **It is a set of spans, not a point.** A content endpoint is never a single location — it is an arbitrary, possibly discontiguous collection of byte-spans:
   > "one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

2. **The two directional ends.** The from-set (bytes the link is "from") and the to-set (bytes the link is "to"):
   > "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" (4/42)

3. **Spans pointing anywhere in the docuverse.** Each endset maps to positions on the tumbler line and may reach across multiple documents:
   > "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." (4/43)

Because these endsets are span-sets anchored to bytes (Istream content) rather than positions, what the system returns remains valid even after the connected documents are edited — "if anything is left at each end" (4/43).

A note on the third endset: a link also has a **type** (the "three-set"), but that endset *categorizes* the link rather than designating connected content, and is matched by address rather than read for content (4/44–4/45). The question asks specifically about the **content endpoints the link connects** — those are the from-set and to-set returned by RETRIEVEENDSETS.

The curated sources confirm RETRIEVEENDSETS "returns the from-set and to-set of links" (FEBE/endsets operation tables), consistent with the verbatim definition at 4/70.
