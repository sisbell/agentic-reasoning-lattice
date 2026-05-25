# Sub-Questions — SHOWORIGIN Operation

**Inquiry:** Given a span of content, identify its origin document.

1. [theory] What must the system guarantee about a span's ability to identify the document where its content originated?
2. [theory] Must every piece of content carry permanent evidence of its original authorship and source document?
3. [theory] When content appears in multiple documents through sharing, which document does the design consider its origin?
4. [theory] Must origin information for a span remain accurate forever, even after the original document is edited or withdrawn?
5. [theory] Does the design require that any user viewing a span be able to trace it back to its first appearance?
6. [theory] What must the system guarantee about distinguishing original content from content that was incorporated from elsewhere?
7. [theory] If a span's origin document is deleted by its owner, must the origin attribution still survive on derivative documents?
8. [theory] Must origin identification work uniformly for spans of any size, from a single character to an entire document?
9. [theory] Does the design treat origin as a property of the content itself or as a property of the document containing it?
10. [theory] What must the system guarantee about resolving origin when a span has passed through several intermediate documents before reaching its current location?
11. [evidence] When `find_documents_containing` queries the spanfilade with an I-address span, does it return the originating document first or in spanfilade-traversal order?
12. [evidence] Given an I-address from a content span, how does the system determine which document originally allocated it — is it derivable from the tumbler hierarchy (e.g., parent prefix of the I-address) alone, or does it require a spanfilade lookup?
13. [evidence] Does the spanfilade store a distinguished "origin" flag on DOCISPAN entries, or are all entries (origin document plus transcluding documents) structurally indistinguishable?
14. [evidence] If a span's I-addresses fall under the parent tumbler `1.1.0.1.0.5.0.1.x`, is the origin document always reliably `1.1.0.1.0.5` by tumbler-prefix decomposition, or can fragmented allocation break this assumption?
15. [evidence] For a span that has been transcluded across N documents, does `find_documents_containing` return all N documents, and in what tumbler order — by document I-address ascending?
16. [evidence] When the queried I-span crosses multiple DOCISPAN boundaries in the spanfilade (because the original content was inserted as separate operations), are multiple matches returned per origin document or is the result coalesced?
17. [evidence] If the originating document has been entirely DELETE'd from its POOM but the spanfilade still contains its DOCISPAN entries [FC-SPANFILADE-MONOTONIC], does the origin document still appear in `find_documents_containing` results?
18. [evidence] For a span originating from APPEND'd content (which skips `insertspanf` per [EC-APPEND-NO-DOCISPAN]), is there any backend mechanism to identify the origin document, or is such content origin-anonymous?
19. [evidence] When the span's I-addresses were allocated under a user's account rather than under a parent document (e.g., a version of a non-owned doc per [PRE-CREATENEWVERSION]), does origin-identification by tumbler prefix yield the account address instead of a document address?
