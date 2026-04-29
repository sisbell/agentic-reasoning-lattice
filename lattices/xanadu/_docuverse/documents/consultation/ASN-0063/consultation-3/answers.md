# Revision Consultation — ASN-0063

**Review:** review-3.md
**Date:** 2026-03-21 18:51

## Summary

7 REVISE items analyzed: 6 internal, 1 consulted (1 nelson, 0 gregory)

## Consultation Results

### Issue 2: Framework extension permits orphan links without acknowledgment

**Category:** NELSON
**Reason:** Whether links may exist in dom(L) without placement in any document's arrangement is a design intent question about link lifecycle — the framework permits it but the ASN neither prevents nor endorses it.

**Nelson question:** Must every link be placed in its home document's arrangement at creation time, or are orphan links (existing in the link store but not in any document's arrangement) valid system states — for example, after link withdrawal?

**Nelson's Answer:**

## Answer: Orphan Links After Withdrawal Are Valid

**At creation, a link must have a home document.** MAKELINK explicitly requires it: "This creates a link in document `<doc id>`" [4/68]. There is no protocol command to create an unattached link. The home document determines ownership — "Its home document indicates who owns it, and not what it points to" [4/12].

**After creation, orphan links are a valid and explicitly specified system state.** The diagram on page 4/9 shows the technical contents of a document in four categories:

- CURRENT BYTES
- DELETED BYTES
- CURRENT LINKS  
- **DELETED LINKS**

Nelson annotates both deleted categories identically:

> "not currently addressable, awaiting historical backtrack functions, may remain included in other versions." [4/9]

This is a link that exists in permanent storage (it has its Istream address in the `2.x` subspace) but is not in the document's current active set. It is an orphan — present in the link store, absent from any current arrangement.

### The Parallel with Bytes

The architecture treats link deletion exactly like byte deletion. For bytes, DELETE removes from Vstream but preserves in Istream:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [4/11]

The same logic applies to links. The link's permanent address in the `2.x` subspace (its "permanent order of arrival" [4/31]) is its Istream identity. Deletion removes it from the document's current link set but does not destroy it.

### What "Not Currently Addressable" Means

A deleted link:

1. **Cannot be found by FINDLINKS** — It is not in the current set, so link search operations over the docuverse will not return it.
2. **Can be recovered through historical backtrack** — Previous versions of the home document still contain it. "May remain included in other versions" means exactly this.
3. **Retains its permanent address** — The `2.x` position is never reused. Link `2.5` is always the fifth link created in that document, whether current or deleted.
4. **Does not affect its targets** — The content the link pointed to is unaffected. Link survivability is about the reverse direction (content edits not breaking links); link deletion is a separate owner action.

### Why This Matters

The orphan state resolves a tension in the architecture. Links are owned property ("A Xanadu link is a connective unit... It is owned by a user" [4/41]), and owners have the right to withdraw their property ("Only the owner has a right to withdraw a document or change it" [2/29]). But the permanence guarantee means nothing is truly destroyed. The orphan state — existing but not currently addressable — satisfies both requirements.

### Summary

| State | In link store? | In current arrangement? | Discoverable via FINDLINKS? | Recoverable? |
|-------|---------------|------------------------|----------------------------|-------------|
| Active link | Yes | Yes | Yes | N/A |
| Deleted/orphan link | Yes | No | No | Yes (historical backtrack) |
| Never created | No | No | No | No |

A link is always born into a home document's arrangement (MAKELINK requires `<doc id>`). It can subsequently become orphaned through owner deletion, entering the "not currently addressable" state that Nelson explicitly diagrams on 4/9. This is not an error condition — it is a designed system state, parallel to deleted bytes, awaiting historical backtrack.
