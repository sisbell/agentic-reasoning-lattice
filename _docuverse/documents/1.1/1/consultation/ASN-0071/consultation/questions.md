# Sub-Questions — FINDDOCSCONTAINING Operation

**Inquiry:** Given content specified by a vspec-set, which documents contain any portion of that content? What determines the result set, and what guarantees govern completeness versus currency?

1. [theory] When a user asks which documents contain a given piece of content, what must the system guarantee about the completeness of the answer?
2. [theory] Must the result include every document that has ever contained that content, or only those that currently contain it?
3. [theory] What determines whether a document "contains" content — direct authorship, inclusion from elsewhere, or both?
4. [theory] Does the guarantee of finding all containing documents extend across all users' documents, or only those the requester is permitted to see?
5. [theory] How does the design reconcile the permanence of historical containment with the currency of present-day document state?
6. [theory] If a document once contained the specified content but no longer does, must the system still report it, and under what identity?
7. [theory] What must the system promise about the freshness of the result — is the answer guaranteed to reflect the moment of the query?
8. [theory] When content appears in multiple documents through sharing, must each containing document be reported independently and identifiably?
9. [theory] What guarantee governs the result when the specified content spans material drawn from many original sources?
10. [theory] Must the system distinguish, in its answer, between documents that contain the content as original authorship versus those that contain it through reuse?
11. [evidence] When FINDDOCSCONTAINING receives a vspec-set, does it first resolve V-addresses to I-spans via the caller's POOM before querying the spanfilade, and what happens if the caller's POOM has no entry for part of the input vspec?
12. [evidence] Does FINDDOCSCONTAINING return a document if ANY portion of the queried I-spans overlaps a DOCISPAN entry, or does it require full coverage of the input span?
13. [evidence] Given that DOCISPAN entries are created per contiguous I-span at insertion time, how does FINDDOCSCONTAINING handle a query I-span that crosses multiple DOCISPAN boundaries within a single target document — one result or multiple?
14. [evidence] Since APPEND has the `insertspanf` call commented out, will FINDDOCSCONTAINING ever return a document whose content was added solely via APPEND, even when that content exactly matches the query?
15. [evidence] Because the spanfilade has no delete function, does FINDDOCSCONTAINING return documents that previously contained the queried I-spans but have since had them removed from their POOM via DELETEVSPAN — and is there any post-filter against the live POOM?
16. [evidence] What is the iteration order of returned documents — sorted by document ISA, by DOCISPAN insertion order in the spanfilade, or by some 2D-enfilade traversal order — and is the order stable across sessions?
17. [evidence] Does FINDDOCSCONTAINING enforce BERT/open-document gating on the returned documents (filtering out documents the caller cannot read), or does it return all matching document IDs regardless of access?
