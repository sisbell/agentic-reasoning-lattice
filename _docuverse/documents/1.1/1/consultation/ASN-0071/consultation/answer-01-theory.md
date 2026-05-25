## Question 1 [theory]

> When a user asks which documents contain a given piece of content, what must the system guarantee about the completeness of the answer?

# Completeness Guarantee for FINDDOCSCONTAINING

The FEBE operation here is **FINDDOCSCONTAINING**. The system must guarantee that the returned list is **complete** along four dimensions:

## 1. ALL documents — not a sample

Nelson is explicit: it returns "a list of **all** documents containing any portion of the material" (4/70). This is the core completeness guarantee — no document containing any of the queried material may be omitted.

## 2. Any portion counts — partial inclusions are included

The query is satisfied by *any portion* of the material, not just complete copies. A document that transcludes a single sentence from a longer passage must still appear in the result.

> "This returns a list of all documents containing any portion of the material included by <vspec set>." — 4/70

## 3. Regardless of physical location — cross-server

Completeness extends across the entire docuverse, not just the local server:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." — 4/63

This is enforced through BEBE: the contractual obligation of Storage Vendors to honor cross-vendor requests means a local server must reach out to wherever the content lives to assemble a complete answer.

## 4. Both native and transcluded inclusions

The mechanism that makes this work is the Istream identity model. Because transclusion preserves shared I-addresses (rather than copying bytes), any document that transcludes content shares the same address fingerprint as the original. The search is structural — it matches by I-address, so both the home document and every transcluder are discoverable through one mechanism.

This is what makes Nelson's attribution guarantee operational:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." — 2/40

## What is NOT guaranteed

- **Bounded time / size** — the result set could be enormous if content is widely transcluded. Nelson does not specify pagination for FINDDOCSCONTAINING the way he does for FINDNEXTNLINKSFROMTOTHREE (4/69).
- **Ordering** — no ranking or relevance is implied.
- **Private documents** — Nelson's privacy principle ("the network may not monitor what is read or what is written in private documents," 2/59) implies private documents containing the material should not appear to non-authorized requesters. NEED_RAW: 4/70 to confirm whether FINDDOCSCONTAINING filters by visibility.

## Why completeness matters

This guarantee underwrites several Nelson-level promises:
- **Royalty distribution** — every byte delivered must be attributable, so every container must be findable
- **Provenance** — readers can trace any content to every context it appears in
- **The "two-way reading" model** — "the reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'" (2/46). FINDDOCSCONTAINING is the inclusion-side counterpart to that link-side query.
