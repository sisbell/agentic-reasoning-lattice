## Question 2 [theory]

> In the original link model, was the home document of a new link intended to be a caller-supplied parameter of the emit operation, or determined implicitly by allocator policy or ambient context?

The home document is a **caller-supplied parameter** of the emit operation. This is explicit in the FEBE specification of MAKELINK.

## The MAKELINK signature

From LM 4/68:
> "This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. It returns the id of the link made."

The `<doc id>` is the home document, supplied by the caller alongside the three endsets.

## Why it must be a parameter

Nelson explains the necessity directly at LM 4/63:
> "The document must be specified because that determines the actual residence of the link—since a document may contain a link between two other documents."

The home document cannot be inferred from the endsets, because the from-set and to-set may both reside in documents other than the link's home. A link's home is structurally independent of what it connects.

## Confirmed by the ownership model

The link's home determines ownership, not its endpoints. From LM 4/12:
> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document."

If home were determined by allocator policy or ambient context (e.g., "use the document containing the from-set"), this independence would be impossible. The caller must explicitly choose where the link lives, because that choice assigns ownership and controls where it is searchable as a native link.

## Summary

Home document is an **explicit required parameter** of MAKELINK, not implicit. The protocol exposes it precisely because ownership and residence are orthogonal to the link's endpoints, and only the caller knows the intended owner.
