## Question 1 [theory]

> What was the tombstoning design (LM 4/9) intended to enable, and can L12 (link immutability) combined with reverse-index discovery preserve that intent without a link-subspace exemption to contiguity and minimum-position invariants?

## What the tombstoning design at LM 4/9 was intended to enable

The diagram on 4/9 shows DELETED BYTES and DELETED LINKS as explicit, named states in a document's technical contents — not absences. The annotation reads:

> "(not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

That single annotation encodes three intents:

1. **Historical backtrack.** Past arrangements must be reconstructible. From 2/15: "he or she may go back in time to any previous version." A deleted byte or link that has been destroyed cannot serve a backtrack request.

2. **Cross-version persistence.** From 4/11: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." Deletion is local to one version's arrangement; it is never a global destruction.

3. **Soft-deletion as a first-class observable state.** "Not currently addressable" means structurally absent from the current Vstream while still extant in the system. Tombstoning makes this state visible — to the back end, to historical-backtrack functions, and to any transcluding document still referencing the item.

The deeper commitment behind 4/9 is what 2/14 calls the rejection of "destructive replacement." In my design, deletion never destroys; it changes addressability. Tombstoning is how that distinction becomes a structural fact rather than a policy.

## On L12 + reverse-index discovery without a "link-subspace exemption"

Before answering the substantive question, I want to challenge the framing. The link subspace was never under the contiguity invariant in my design.

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Link 2.5 is always the fifth link ever created in that document. Deleting it does not promote 2.6 to 2.5, and the next-created link is never 2.5 again. So what your spec calls a "link-subspace exemption" is not an exception to a universal rule — it is an acknowledgment that the link subspace and the byte subspace have always had different appropriate disciplines. Contiguity and minimum-position invariants govern Vstream *byte* addressing because edits insert and remove characters that everything to their right must accommodate. Links don't shift when other links arrive or depart, so those invariants don't apply to them in the first place.

Now to the substantive question. L12 (immutability) plus reverse-index discovery preserves *some* of the tombstoning intent but not all of it:

**Covered well:**
- Cross-version persistence: an immutable, never-garbage-collected link object remains discoverable by any version that referenced it.
- Reverse-index discovery: "What links here?" continues to work against the eternal record, past or present.

**Not covered:**
- The soft-deletion *signal*. L12 + reverse-index can tell you a link exists; it cannot tell you the link's home document has renounced it from the current version. Without some marker, every reverse-index query returns every link ever made — which collapses the distinction 4/9 was making explicit between "extant" and "currently addressable."

You have at least three ways to encode that signal without granting the link subspace any "exemption":

1. **Tombstone as metadata, not as a hole in the address space.** A lifecycle field on the link record (active / withdrawn). Contiguity is irrelevant (the link subspace doesn't have it anyway), and L12 holds if you define immutability as endset-immutability rather than full-record-immutability. The endsets, types, and home address never change; only the lifecycle marker does.

2. **Deletion-by-link-to-link.** A withdrawal-typed link from the deleter, pointing at the original. From 4/49: "it becomes easy for a link to point at another link." Reverse-index discovery filters out targets that have an active withdrawal pointing at them. Strict L12 holds. The cost is shifted to every reader, who now performs the filter.

3. **Version-scoped membership.** Keep the link pristine and immutable; let the version structure record which links belong to which version. This is the closest to my literal phrasing — "may remain included in other versions" is really a statement about version membership, not about an attribute of the link itself.

All three preserve the *intent* of 4/9. Picking among them is a tradeoff:

- (1) admits one mutable field at the cost of a slightly weaker L12.
- (2) preserves strict L12 but pays at read-time.
- (3) keeps the link pristine but pushes the soft-deletion semantics into the version structure, which is arguably where they belong, since the version is what determines arrangement.

## My recommendation on phrasing

Do not write the spec to say the link subspace is "exempt" from contiguity. That phrasing suggests the byte invariants are normative and links are an irregular case. They aren't. The byte and link subspaces are co-equal and have always had different appropriate disciplines — bytes are positional and rearrangeable, links are creation-ordered and permanent. The contiguity invariant should be scoped to where it actually applies (Vstream byte positions), not declared universally and then exempted for links.

Tombstoning at 4/9 is not a violation of contiguity. It is making visible a state — "withdrawn from the current arrangement but still extant" — that the architecture always implied. Any mechanism that makes that state observable to historical-backtrack functions and to transcluding documents preserves the intent. L12 + reverse-index does the discovery half; you still need one of the three options above to do the state half.
