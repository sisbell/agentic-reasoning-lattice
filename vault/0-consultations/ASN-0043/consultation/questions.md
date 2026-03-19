# Sub-Questions — Link Ontology

**Inquiry:** What is a link on the tumbler line? What structure must a connection between arbitrary spans of tumbler addresses have, and what properties must hold about those connections?

1. [nelson] What is the minimum structure of a link — what components must every connection between arbitrary spans of content contain?
2. [nelson] Must a link distinguish a "from" endpoint and a "to" endpoint, or are the endpoints of a connection symmetric and unordered?
3. [nelson] Can a single link connect more than two spans of content, or is every link strictly a pair of endpoints?
4. [nelson] Must each endpoint of a link identify a specific contiguous span of content, or may an endpoint designate a non-contiguous selection or an entire document?
5. [nelson] Does a link have its own unique, permanent identity within the system, distinct from the identities of the content it connects?
6. [nelson] Is a link itself a piece of content — something that can be addressed, quoted, and linked to in turn — or is it a separate category of object outside the content space?
7. [nelson] Must the system support typed links — connections that carry a declared kind or role such as "comment," "quotation," or "correction" — or are all links structurally uniform?
8. [nelson] Must two links that connect the same two spans of content be distinguishable as separate objects, or does the system treat identical connections as a single link?
9. [nelson] Can a link connect two spans within the same document, or must a connection always cross a document boundary?
10. [nelson] Must a single endpoint be confined to content within one document, or may one endpoint of a link span content across multiple documents?
11. [gregory] A link orgl stores three endsets (source, target, type) each containing I-address spans — is the three-endset structure the minimum necessary representation, or was it designed to be extensible to N endsets, and if so, what constrains it to exactly three?
12. [gregory] The type endset is itself an I-address span rather than a symbolic label or enumerated value — what was the design reasoning for making link type a content-identity reference on the tumbler line rather than a distinct categorical mechanism?
13. [gregory] What are the cardinality constraints on an individual endset — can an endset contain zero spans, exactly one span, or an unbounded number of spans, and does this differ between source, target, and type?
14. [gregory] Can a single endset span I-addresses originating from multiple documents (i.e., a source endset referencing content created in doc A and content created in doc B), or must each endset be confined to a single document's I-address range?
15. [gregory] Is the source/target distinction on a link an intrinsic structural asymmetry in the orgl representation, or is it a naming convention over two structurally identical endset slots — could a link be meaningfully "followed" in either direction with equal validity?
16. [gregory] A link has its own I-address (the link orgl at `docISA.0.2.N`) — can a link's endset reference another link's I-address, creating link-to-link connections, and if so, was this an intentional design capability or an emergent consequence of uniform I-address treatment?
17. [gregory] The type namespace lives at `1.0.2.x` in the global address space — what structure do type tumblers have, how are new types created, and is there a base set of built-in types that the system assumes?
18. [gregory] A link orgl is stored in the granfilade alongside text content — is a link ontologically a special kind of content on the permascroll (occupying I-space positions just as characters do), or is it a categorically different entity that merely uses the same storage substrate?
19. [gregory] When multiple I-address spans compose an endset, does their ordering within the endset carry semantic meaning (first span is primary, etc.), or is the endset an unordered set where only membership matters?
20. [gregory] Nelson described links as connecting arbitrary spans across the entire address space — was there a design constraint that both endpoints of a link must reference content that actually exists at link creation time, or can a link be created with endsets pointing to I-addresses that have not yet been allocated (forward references)?
