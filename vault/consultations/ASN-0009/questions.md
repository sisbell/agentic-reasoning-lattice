# Sub-Questions — Version Semantics

**Inquiry:** What does creating a new version preserve and establish? What is the version fork model — how do versions relate to each other and to shared content?

1. [nelson] When a user creates a new version of a document, must the new version initially contain exactly the same content as the original, or only the text content without the links?
2. [nelson] Does creating a new version establish a permanent record of which document it was derived from, and is that parentage relationship itself permanent?
3. [nelson] If two versions share the same content, does editing one version's content affect what the other version displays, or are they independent after forking?
4. [nelson] When a new version is created, do the links attached to the original document carry over into the new version, or does the new version start with no links?
5. [nelson] Can a user create a new version of someone else's document, or must version creation be restricted to the document's owner?
6. [nelson] After a version fork, if both versions are edited independently, is there any designed mechanism for merging them back together, or do versions only diverge?
7. [nelson] Does the identity of content shared between two versions remain the same — that is, can the system recognize that two versions contain the identical original material?
8. [nelson] Must every version of a document be independently permanent, or can a version's existence depend on the continued existence of its parent?
9. [nelson] When content is transcluded from a document into another document, and the source document is then versioned, which version does the transclusion point to — the original, the new version, or both?
10. [nelson] Is there a limit to how many times a document can be versioned, and do all versions form a tree structure, or can a version have multiple parents?
11. [gregory] When CREATENEWVERSION copies the text subspace POOM, is the new POOM a structurally independent B-tree (deep copy of all crums), or does it share any tree nodes with the source document's POOM?
12. [gregory] After CREATENEWVERSION, if the original document is edited (INSERT or DELETE), does the version's POOM remain completely unchanged — same V-addresses, same I-address mappings, same tree structure?
13. [gregory] When you version a version (CREATENEWVERSION of document `1.1.0.1.0.1.0.1`), is the new version allocated as a child of the version (`1.1.0.1.0.1.0.1.0.1`) or as a sibling under the original (`1.1.0.1.0.1.0.2`)?
14. [gregory] Does CREATENEWVERSION create DOCISPAN entries in the spanfilade for the new version document, and if so, are they per-I-span entries matching the source's text content — or a single entry covering the entire I-address range?
15. [gregory] When a document contains transcluded content (I-addresses originating from another document's allocation range), does CREATENEWVERSION preserve those cross-document I-address references in the version's POOM, maintaining the transclusion chain?
16. [gregory] Does CREATENEWVERSION copy the type subspace (`3.x`) entries from the source POOM, or is only text subspace (`1.x`) copied — and if type entries exist, what happens to them?
17. [gregory] When a non-owner versions a document, the version is allocated under the non-owner's account — does the version's POOM still use the original document's I-addresses, or are fresh I-addresses allocated under the non-owner's I-address range?
18. [gregory] If you INSERT new text into a version and then call FINDDOCSCONTAINING with a specset from the original, does the original appear in the results — and does the version also appear because of the shared I-addresses from the initial copy?
19. [gregory] Was the version model intended to support eventual merging of divergent versions back together, or was the design philosophy that versions diverge permanently and are compared (SHOWRELATIONOF2VERSIONS) but never converged?
20. [gregory] After CREATENEWVERSION, if a CREATELINK is made on the original document targeting content that was copied to the version, is that new link immediately discoverable via find_links on the version through the shared I-addresses — even though the link was created after the version fork?
