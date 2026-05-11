## Question 3 [theory]

> Does Nelson's baptism principle commit documents themselves to being allocated as document-level tumblers (zeros = 2) under their owning user's prefix via the same allocator discipline that produces I-addresses, so that distinct document creations are distinct allocation events under T10a?

Yes, Nelson's baptism principle commits to this.

**1. Documents are allocated under their owning user's prefix.** Nelson explicitly enumerates documents alongside nodes, accounts, and versions in the baptism mechanism:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

The User owns its sub-numeric space, and document numbers are forked under it.

**2. Same allocator discipline as I-addresses.** Baptism is the *universal* mechanism, not a separate one for content:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

The four-field structure `Node.0.User.0.Document.0.Element` is itself produced by repeated baptism at each major divider. The document-level tumbler (terminating at the third field, hence 2 major-divider zeros) is one stage of the same allocator that, when extended one more zero-divider deep, produces the I-address of an element.

**3. Distinct creations are distinct allocation events.** Forking proceeds by integer succession under the owner:

> "Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

Each act of subdivision is a discrete event producing a distinct sub-number — there is no merging or reuse, and "new items may be continually inserted in tumbler-space while the other addresses remain valid" [LM 4/19]. Two document creations under the same user therefore yield two distinct document-level tumblers.

**On T10a specifically.** Nelson's text supports modeling each document creation as a distinct allocation event under the user's prefix, governed by the same baptism discipline as I-address allocation. The curated sources do not name a "T10a"; that label is internal to your specification, and the question of whether T10a's *formal* statement matches this commitment requires checking T10a's text directly — but on the underlying intent, Nelson is unambiguous.

NEED_RAW: none — curated sources cover this.
