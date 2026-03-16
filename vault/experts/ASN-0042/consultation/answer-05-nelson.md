## Question 5 [nelson]

> Can ownership of a position be permanently transferred from one user to another, or is the original assignment irrevocable?

## Ownership Transfer in Xanadu

Nelson's text reveals a **deliberate separation** between the permanent address (which encodes origin) and the ownership of rights (which he implies can transfer). But he specifies no mechanism for the transfer itself.

### Evidence That Transfer Is Contemplated

The clearest statement is from 2/29:

> "Every document has an owner, the person who created and stored it **(or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights**... Only the owner has a right to withdraw a document or change it." [LM 2/29]

The parenthetical is significant. Nelson explicitly names two cases where the owner is NOT the person who typed the words:

1. A publishing company that "arranged" creation
2. Someone who "bought the document rights"

Both imply ownership can originate with or transfer to a different party than the creator.

### But the Address Is Irrevocable

The tumbler address permanently encodes the originating account:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The I-space address structure is `Node.0.User.0.Document.0.Element` [LM 4/26]. The User field is baked into the permanent address. If user 3 creates a document at `1.0.3.0.5`, that address cannot become `1.0.7.0.5` after a sale to user 7. The address tells you where content was *born*, not who currently holds the rights.

This means the **address encodes provenance, not current ownership**. The system must track current ownership separately from the address — presumably in what Nelson calls "the user's system area, along with passwords and accounting information" [LM 5/13].

### What Is NOT Specified

Nelson provides no mechanism for:

- How ownership transfer is recorded in the system
- Whether the original account holder retains any residual rights
- How royalty routing changes after transfer (the "cash register" lives at the document, but who collects?)
- Whether transfer of a document also transfers the right to fork sub-addresses under it
- Whether an entire account (the User field and everything below it) can be transferred

### The Tension

There is an unresolved tension between two principles:

| Principle | Implication |
|-----------|-------------|
| **Permanent addresses** | The User field in the tumbler forever says "created by account X" |
| **Transferable ownership** | "Someone who has bought the document rights" is the owner |
| **Origin traceability** | "You can at once ascertain the home document of any specific word or character" [LM 2/40] |

Origin traceability survives transfer — it traces to the *document*, not the *owner*. The I-address always tells you which document created the bytes. But if ownership transfers, the User field in that document's address no longer identifies the current owner. The address becomes a historical record ("created under this account") rather than a current authority record ("owned by this account").

### My Assessment as Designer

The address assignment is irrevocable — that is structural and absolute. But **ownership of the rights to a document** (modification, withdrawal, royalty collection) is transferable. I said as much when I mentioned "someone who has bought the document rights."

The address is like a birth certificate — it records where something originated. Ownership is like a deed — it records who currently holds the rights. These are different things, and the system needs both. I did not specify the deed mechanism in detail, which is a gap in the specification.

NEED_RAW: [2/29-2/31, 5/19-5/21] — The full text of the ownership section and the publication agreement may contain additional detail about transfer mechanics or constraints that the curated extracts abbreviate.
