## Question 2 [theory]

> Must every piece of content carry permanent evidence of its original authorship and source document?

# Yes—For Source Document. Conditionally—For Authorship.

The answer requires distinguishing two things the question conflates:

## Source Document: Always Preserved, Structurally

Every byte in the docuverse carries permanent evidence of its source document through its Istream address. The tumbler structure `Node.0.User.0.Document.0.Element` encodes origin into the address itself—not as metadata that can be stripped, but as the means by which the bytes are retrieved.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is structural, not informational. To fetch the byte, the system must request it from its home:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When you transclude content, you do not copy it—you reference its permanent I-address. The connection cannot be severed because the fetching mechanism requires it.

## Authorship: Owner Always, Identity Optionally

The User field of the tumbler always identifies the owning account, so ownership is permanent. But the *human identity* behind that account is not required to be known. I explicitly permitted anonymous publication:

> "Normally publication will be by accountable individuals and companies with known residence or place of business. Still, there is no reason that anonymous publication by walk-in and transient users of this system should not be allowed. We may call this 'John Doe publication.'" [LM 2/60]

So the system guarantees you can trace content back to the owning account, but not necessarily to a named human author.

## The Boundary of the Guarantee

The attribution guarantee holds *within the system*. Once bytes leave—copied to paper, exported to disk—the connection dies:

> "He or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy." [LM 2/48]

## Summary

| Aspect | Required? |
|--------|-----------|
| Permanent I-address encoding home document | Yes—structural |
| Traceability to owning User account | Yes—structural |
| Traceability to named human author | No—John Doe publication is permitted |
| Preservation when content exits the docuverse | No—copies lose connection |

The system *cannot* sever attribution to source document and owning account. It *does not require* that the account holder be publicly identified.
