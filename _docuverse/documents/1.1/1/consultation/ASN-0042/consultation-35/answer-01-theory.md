## Question 1 [theory]

> When a principal creates a fork in response to non-ownership of target content, must the new address be a content-bearing element-level address (the inclusion-link endpoint), or does the design admit forks at any level within the principal's domain?

# Forks in Response to Non-Ownership

The design admits forks **at any level within the principal's domain**. There is no requirement that the new address be an element-level (content-bearing) one. In fact, the natural response to non-ownership is typically a **document-level fork**, not an element-level one.

## The Mechanism Is Uniform Across Levels

The forking process is the same regardless of level:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

A principal cannot fork *inside* the target's domain — you do not create element-level addresses inside Alice's document. You fork inside *your own* domain.

## What the Principal Actually Creates

When responding to non-ownership, the principal creates a new container — typically a document under their own account — and uses inclusion links to reference the target:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

The element-level addresses that anchor the inclusion live *in the target's domain*. They are the **destination** of the inclusion link, not the principal's fork.

Document and version forks are the same shape of operation:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

## The Layered Picture

- **Principal's fork**: a new address in their own domain, at whichever level is appropriate (account → document → version)
- **Element-level addresses inside that fork**: created incidentally as the principal places content (including inclusion links)
- **Inclusion-link target endpoint**: an element-level address in the *target's* domain, untouched by the principal

So the inclusion-link endpoints exist at the element level by virtue of pointing at content bytes, but they exist *as the target side of the link*, not as the principal's fork.

NEED_RAW: 4/18-4/22, 4/28-4/30. The curated sources strongly support the "any level" reading and the document-level convention, but I have not verified whether Nelson explicitly addresses the constraint question in the framing you asked. A close reading of 4/18-4/22 (forking) and 4/28-4/30 (document/version subdivision) would confirm whether the design *requires* a particular level for the non-ownership case or merely *typifies* the document-level response.
