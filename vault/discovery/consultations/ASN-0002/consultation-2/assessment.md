# Revision Categorization — ASN-0002 review-2

**Date:** 2026-02-28 14:05

## Issue 1: AP5 is false as stated; link survivability derivation is unsound
Category: INTERNAL
Reason: The ASN already distinguishes monotonic extension (INSERT, CREATELINK) from mutation of existing entries throughout the operation analyses. The corrected AP5 and repaired derivation are derivable from definitions and reasoning already present.

## Issue 2: System state Σ omits `links`; AP12 quantifies over an undefined set
Category: INTERNAL
Reason: The CREATELINK section already states that links are stored in ispace at fresh addresses in the link subspace. Defining `links` as the derived subset of `dom.ispace` in the link subspace, and specifying `endsets` as a projection of link content, requires only information already in the ASN.

## Issue 3: AP12 is derivable from AP1 but presented as independent
Category: INTERNAL
Reason: The derivation chain — links stored in ispace, endsets are part of link content, AP1 guarantees content immutability — uses only premises already stated in the ASN. Relabeling AP12 as derived and writing the explicit derivation is a purely internal restructuring.

## Issue 4: `vspace(d)` typed as total function but used as partial
Category: INTERNAL
Reason: The inconsistency between the `→` notation and the operations (DELETE removes entries, `#vspace(d)` implies finite domain) is a notation error fixable by changing the type signature to `⇀` to match `ispace`'s existing notation. No external evidence needed.

## Issue 5: AP8 formalizes only one direction; the bijectivity claim is half-proved
Category: INTERNAL
Reason: The ASN already provides Gregory's evidence that REARRANGE modifies only V-displacements, leaving I-displacements untouched and creating no new entries. The reverse direction — no new I-addresses appear — follows directly from this already-cited evidence. The fix is to state AP8 as set equality using reasoning already present.

## Issue 6: AP14 is ambiguous for multi-document operations
Category: INTERNAL
Reason: The ASN's per-operation frame conditions already specify which document's V-space is modified (e.g., COPY modifies the target, not the source). Defining "target document" and restating AP14 in those terms requires only information already in the operation analyses.

## Issue 7: No concrete worked example
Category: INTERNAL
Reason: The ASN provides sufficient definitions and operation specifications to construct a worked example using abstract addresses. The suggested scenario (INSERT, DELETE, COPY, CREATELINK) can be checked against the postconditions using only the properties and operation effects already stated.

## Issue 8: Ghost address permanence is asserted but not derived
Category: NELSON
Reason: AP0 covers addresses in `dom.ispace`; AP4 covers allocation gaps. But ghost addresses occupy address-space positions assigned to servers, accounts, or documents — the permanence of those structural range assignments is a design intent question not answerable from the ASN or implementation alone.
Nelson question: In the tumbler address hierarchy, is the assignment of an address range to a server, account, or document intended to be permanent and irrevocable — i.e., once a range is committed to an entity, can that range never be reassigned to a different entity, even if the entity has no stored content?

## Issue 9: CREATENEWVERSION — "does not enter `dom.ispace`" is asserted without formal grounding
Category: GREGORY
Reason: The ASN references a "document registry (a component of Σ outside ispace)" that is never defined. Formalizing the distinction between content addresses and document identity addresses, and specifying where document identities are recorded, requires evidence about the implementation's data structures beyond what the ASN currently cites.
Gregory question: When CREATENEWVERSION creates a new document, what data structure records the new document's existence and identity — is it a structure separate from the content store (granfilade), and what fields does that record contain?
