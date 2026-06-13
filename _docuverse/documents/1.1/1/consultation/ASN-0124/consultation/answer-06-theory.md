## Question 6 [theory]

> What completeness guarantee does the design make — is it an invariant that no document anywhere in the docuverse containing any queried portion may be silently omitted from the answer?

I wasn't able to open the raw page images/text in this environment (tool output isn't rendering), so I'll answer from the verified curated sources and flag the sub-claims that would need raw-page confirmation.

## Short answer

At the level of **design intent and operational contract, yes** — completeness is the stated guarantee, and it is precisely a "no matching document is omitted" guarantee. But three qualifications matter: (1) it is completeness over *content identity*, not text similarity; (2) Nelson states it as the **return contract of an operation**, not as a formally labeled "invariant"; and (3) the *silent*-omission edge case — what happens to a matching document sitting on an unreachable node — is not spelled out for this query, and the docuverse-wide version of it was not actually implemented in XU.87.1.

## The operation that carries the guarantee

The relevant operation is **FINDDOCSCONTAINING**, and its defining text is explicitly a completeness contract:

> "This returns a list of **all** documents containing **any portion** of the material included by <vspec set>." (4/70)

> "This returns a list of all documents containing any of the material specified by the span addresses, **regardless of where the native copies are located**." (4/63)

Two phrases do the work:
- **"all documents … any portion"** — even a single overlapping fragment qualifies a document for the result; nothing matching is dropped.
- **"regardless of where the native copies are located"** — the completeness is *docuverse-wide in intent*, not just local to one server.

So the result-set completeness you describe is exactly Nelson's stated contract for this operation.

## Crucial precision: completeness over *identity*, not text

"Containing any queried portion" means containing the *same bytes* — content sharing the queried **Istream (I-address) origin** — not coincidentally-identical text. Transclusions are "inclusions or virtual copies" that share the original's I-address (4/11), whereas independently typed identical text gets *different* I-addresses. So FINDDOCSCONTAINING is a query over the transclusion/inclusion graph keyed on Istream addresses (see `transclusion.md`, `sporgl-provenance.md`, `i-space-v-space.md`: it "Searches Istream origin, returns Vstream locations"). The invariant, read correctly, is: *no document that includes bytes from the queried I-span may be omitted.* A coincidental textual twin is not "containing the material" and correctly does **not** appear.

## Why completeness is structurally possible

It rests on two design properties already in the curated sources:
- **Origin traceability** — every byte has a permanent I-address, and inclusions carry it, so the back end can search on the span itself (`origin-traceability.md`).
- **Back-end inter-indexing** — links/inclusions are "maintained by the back end through the back end's inter-indexing mechanisms" (4/41), which is what makes the "find everything pointing here / containing this" direction answerable.

## The closest thing to an explicit "no silent omission" invariant

For *link* search, Nelson states a genuine completeness-style principle in capitals:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

with the satisfaction rule:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

This is the strongest invariant-shaped statement in the curated material: irrelevant material cannot crowd out, hide, or impede the matching results. It is the spirit of "no silent omission," but it is stated for **link search**, and it is framed as a *performance/scaling* guarantee ("DOES NOT IN PRINCIPLE IMPEDE") rather than as a labeled completeness axiom for document-containment.

## The qualifications on calling it an "invariant"

1. **Not formally labeled as such.** Nelson gives it as the operation's return value ("returns a list of all documents…"), not as a named invariant. The completeness is unmistakable in the wording, but "invariant" is your framing, not his explicit term.

2. **The "silent" failure mode is unaddressed for this query.** The design openly assumes "computer networks are always broken" (4/75). The general network posture is to *surface* unavailability and route around it (redundancy, forwarding, a "not currently available" fallback per `network.md`/`vendor-interoperation.md`) rather than to drop content silently — which argues *against* silent omission. But the curated sources tie that fallback to content **retrieval/forwarding (BEBE)**, and do **not** explicitly say what a `FINDDOCSCONTAINING` *discovery* query returns when a matching document lives on a disconnected node (reported as unavailable, vs. silently absent). That specific guarantee is not stated.

3. **Not realized in XU.87.1.** Per `session-model.md`, multi-server methods were among the things "Nelson explicitly left unimplemented in XU.87.1" (4/79). So single-server FINDDOCSCONTAINING was complete over that server's contents, but the *docuverse-wide* "regardless of where native copies are located" completeness depended on BEBE forwarding/subrepresentation that was still future work — and a later "barrel-roll shared search model which repeatedly crosses the address space" (4/59) was described as a future enhancement, not a shipped guarantee.

## Bottom line

The design **does** make result-set completeness the contract for FINDDOCSCONTAINING — "all documents containing any portion … regardless of where the native copies are located" (4/70, 4/63) — and a parallel "non-matching material cannot impede the search" principle exists for links (4/60). Read as a specification-level guarantee, it is a no-omission invariant over inclusion-identity. What Nelson does **not** explicitly elevate to an invariant is the adversarial/partial-failure case your phrasing targets — that under network breakage no matching document may be *silently* dropped (as opposed to flagged unavailable). The general "networks are always broken" stance leans toward signaling rather than silent loss, but that is not stated for this operation, and the docuverse-wide form of the guarantee was unimplemented in XU.87.1.

NEED_RAW: 4/60 (page 227) and 4/63, 4/70 (pages 230, 237) — to confirm whether any surrounding text frames containment-search completeness as an explicit invariant or attaches a partial-availability/omission caveat; and 4/74–4/75 (pages 241–242) — to confirm whether the "not currently available" fallback is stated to apply to discovery queries (FINDDOCSCONTAINING/link search) and not only to content retrieval.
