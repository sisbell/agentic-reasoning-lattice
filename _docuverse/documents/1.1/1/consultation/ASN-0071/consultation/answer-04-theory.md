## Question 4 [theory]

> Does the guarantee of finding all containing documents extend across all users' documents, or only those the requester is permitted to see?

Nelson does not explicitly address access control for FINDDOCSCONTAINING. The operation is specified as:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

The "regardless" clause concerns physical distribution across servers, not privacy.

However, this must be read against Nelson's access model:

> "A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

And the privacy guarantee:

> "The network will not, may not monitor what is read or what is written in private documents." [LM 2/59]

The intent is clear: revealing the *existence* of a private document to an unauthorized requester — even just as a hit in a search result — would violate the privacy principle. A search that surfaces "document X contains your query material" implicitly leaks that document X exists and contains specific content. That is monitoring-adjacent.

So the design intent: **FINDDOCSCONTAINING must respect privacy.** It should return all *published* documents containing the material, plus any *private* documents the requester owns or is designated for. Private documents owned by others must not appear in results.

Critically, Nelson himself flags this as unimplemented in the current rig:

> "Private documents. (Currently all documents are visible to all users.)" [LM 4/79]

So in XU.87.1, FINDDOCSCONTAINING returns everything because the access layer doesn't yet exist. This is acknowledged as a deficiency to be fixed, not the design intent.

NEED_RAW: 4/63, 4/79 — to confirm whether Nelson explicitly ties FINDDOCSCONTAINING (or any search operation) to access control beyond what's quoted above. The curated sources establish the principle by implication but I want to verify there isn't a more direct statement about search-side filtering.
