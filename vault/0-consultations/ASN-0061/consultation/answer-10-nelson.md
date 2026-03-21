## Question 10 [nelson]

> After removal, must the system guarantee that any prior state of the document — including the removed content in its original position — remains recoverable and citable?

## Yes — both recovery and citability are guaranteed

Nelson's design answers this unambiguously across three reinforcing layers: Istream permanence, historical backtrack, and link survivability.

### 1. Removed content remains in permanent storage

DELETE is a Vstream operation only. It removes content from the document's current arrangement but leaves the Istream untouched.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The phrase "not currently addressable" is precise — the bytes are not addressable *in this version's Vstream*, but they remain at their permanent I-address forever. The append-only storage model makes this structural:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### 2. Prior states — including position — are recoverable

Historical backtrack explicitly reconstructs the full arrangement, not just the raw bytes:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

This means the *position* of removed content within the prior version's Vstream is recoverable — you get back the arrangement as it was, not just a bag of bytes. Nelson calls this "pounce":

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

And there is no privileged "current" version:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

### 3. Removed content remains citable

Citability follows from the permanence of I-addresses. Every byte has a permanent tumbler address that never changes:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Links to deleted content survive because they attach to I-addresses (bytes), not V-addresses (positions):

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Since DELETE never touches Istream, the bytes to which links are "strapped" remain. The links continue to resolve.

Furthermore, version-spanning links mean a citation to the pre-deletion version reaches through to corresponding content:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

### 4. The principle behind the guarantee

Nelson frames this as the core design commitment:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

Xanadu exists precisely to abolish destructive editing. The guarantee is not a feature bolted onto the system — it is the reason the system has two address spaces (Istream and Vstream) in the first place. Separation of permanent content from ephemeral arrangement is the architectural decision that makes recovery and citability automatic rather than optional.

### Summary

| Question | Answer | Mechanism |
|----------|--------|-----------|
| Must removed content be recoverable? | Yes | Istream is append-only; bytes never leave |
| Must prior arrangement be recoverable? | Yes | Historical backtrack reconstructs any version |
| Must removed content remain citable? | Yes | I-addresses are permanent; links survive |
| Is this a guarantee or a feature? | Guarantee | It is the architectural reason for I/V separation |
