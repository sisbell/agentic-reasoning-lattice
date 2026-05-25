# Sub-Questions — CREATENEWVERSION Operation

**Inquiry:** What is the precise effect of forking a document into a new version? What is copied, what is shared, and what relationship exists between the source and the new version?

1. [theory] When a document is forked, what content must be considered shared between the source and the new version rather than duplicated?
2. [theory] What identity must a forked version carry that distinguishes it from its source while preserving its lineage?
3. [theory] Must the act of forking be invisible to the source document's owner, or does the design require some form of acknowledgment?
4. [theory] What guarantees about content permanence must hold across both the source and the fork after the fork occurs?
5. [theory] When a user forks a document, what rights or claims over the shared content does the new version's owner acquire?
6. [theory] Must subsequent edits to the source document be reflected in the fork, or are the two versions independent from the moment of forking?
7. [theory] What must the system guarantee about the ability to compare a fork against its source at any future moment?
8. [theory] Does the design require that every fork be attributable to a specific user, and what must that attribution preserve?
9. [theory] What must happen to the shared content if the source document is later withdrawn — must the fork retain access?
10. [evidence] When CREATENEWVERSION copies the source's text subspace POOM, does it deep-copy the bottom crums into freshly allocated tree nodes, or does the new version share any tree structure with the source's POOM?
11. [evidence] Why does CREATENEWVERSION exclude the link subspace (internally 2.x) from the copy — was this a deliberate decision to keep links anchored to the home document, or a side effect of doretrievedocvspanfoo extracting only the text span?
12. [evidence] Does CREATENEWVERSION emit DOCISPAN entries in the spanfilade for the new version, given that no new I-spans are introduced — and if so, is there one DOCISPAN per shared I-span in the source's text subspace?
13. [evidence] If the source document is empty (no text, no links), or contains only link-subspace entries, what does CREATENEWVERSION produce — an empty version, a no-op, or an error?
14. [evidence] If CREATENEWVERSION is invoked twice in succession on the same source, does each invocation independently derive from the source's current state, or does the second version pick up any structural difference from the first?
15. [evidence] In the new version's POOM, are the V-addresses literally identical to the source's (so V:1.1 in the version corresponds positionally to V:1.1 in the source), or are they rebased/translated relative to the new document's address?
16. [evidence] Does the new version own an independent I-address allocation range rooted at its own docISA, such that future content allocations under the version cannot collide with the source's findisatoinsertmolecule queries, or do source and version share an allocation parent?
