# Sub-Questions — SHOWDELETIONS Operation

**Inquiry:** Nelson (LM 4/79) lists 'show deletions' as a desired feature. Given two documents that share history, identify which content was present in one arrangement but absent from the other. The operation should return the deleted content in a form the system can act on.

1. [theory] What must the system guarantee about the identity of content that appears in one document arrangement but is absent from another?
2. [theory] When two documents share history, what does the design require the system to recognize as "deleted content" versus content that was merely never included?
3. [theory] Must the deleted content returned by this operation retain its original identity, or is it sufficient to return a copy of the missing material?
4. [theory] What guarantee does the design make about the permanence of content that has been removed from a document but exists in an ancestor arrangement?
5. [theory] Must the result of a deletion comparison itself be a referenceable document that users can link to, share, and quote from?
6. [theory] How should the system treat content that was deleted from one document but remains present in another document sharing the same history?
7. [theory] What must the design guarantee about the ordering of deleted content when it is returned — must the original sequence be preserved?
8. [theory] Should users be able to share the result of a "show deletions" comparison with other users, and must that shared view remain stable over time?
9. [theory] Must the deleted content returned be actionable for further operations such as restoration into a new document arrangement?
10. [theory] What is the design's guarantee regarding the symmetry of this operation — must comparing document A to document B yield a result related to comparing B to A?
11. [evidence] Given two documents sharing history (via CREATENEWVERSION), can the difference between their POOMs be computed as the set-difference of I-address ranges, and does the implementation expose such an operation?
12. [evidence] Does SHOWRELATIONOF2VERSIONS / `correspond.c` return only shared I-spans, or does it also enumerate the I-spans present in one document's POOM but absent from the other?
13. [evidence] When DELETE removes a V→I mapping from a POOM, can the deleted I-address range still be recovered by querying the granfilade or spanfilade for I-addresses originally allocated under that document?
14. [evidence] Does the spanfilade's monotonic-growth property mean a "deleted content" query could intersect spanfilade DOCISPAN entries against current POOM I-spans to identify ranges no longer present?
15. [evidence] For a version V created from source D, do the I-addresses unique to D's POOM (those not appearing in V's POOM) constitute the "added since version" set, and is this directly enumerable?
16. [evidence] Does the granfilade retain enough metadata to reconstruct the original V-position context of a now-deleted I-span, or is V-position information only preserved while a POOM entry exists?
17. [evidence] Can a deleted I-range be transcluded back into a document via COPY using its preserved I-addresses, given that granfilade content persists permanently after DELETE?
18. [evidence] When comparing two documents that share history, does the I-address allocation parent (docISA) of unique I-spans reveal which document was the origin of the differing content?
19. [evidence] Is there any per-document audit structure (beyond the POOM, granfilade, and spanfilade) that records the historical sequence of which I-spans were ever mapped into a document's V-space?
20. [evidence] For the "show deletions" feature, would the returned content need to be expressed as a sporglset (I-address spans with origin document) rather than a VSpec, given that the deleted content has no current V-position?
