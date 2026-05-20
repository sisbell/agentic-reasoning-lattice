## Question 1 [theory]

> Was retraction intended to carry an attribution endset (who retracted), or is retraction in the design strictly a bare "this tuple is nullified" operation with no actor recorded?

Let me clarify what I actually specified, because the question's binary leaves out the third (and correct) option.

**I did not specify a "retraction" operation.** The FEBE protocol has no RETRACT verb [LM 4/61-4/70]. The operations adjacent to your question are:

- DELETEVSPAN — removes a span from a document's Vstream, but content persists in Istream and other versions [LM 4/9, 4/66]
- Withdrawal of a published document — requires "lengthy due process" [LM 2/43]
- Peremptory challenge — third-party removal of defamatory John Doe content [LM 2/60]
- Supersession link — declares obsolescence [LM 4/52-4/53]

**More importantly: in my framework, the actor is never an endset.** It is structural — encoded in the home document address.

A link has three endsets (from, to, type). None is "who made this":

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

The actor is found through ownership of the home:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

This is the same mechanism I gave for the Author metalink:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." [LM 4/52]

Anyone can make the claim; the home address shows *who* made it. The same applies to supersession — the claim and its author are distinct from the from/to/type triad.

**So neither half of your binary is right.** Retraction was not intended to carry an attribution endset, but it was also not intended as a bare "tuple is nullified" with no actor recorded. The actor is recorded — at the home address of whatever entity performs the retraction. Structural attribution, not endset metadata.

The general invariant:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

That applies to links and to any operation that produces a record. If your Nullify primitive emits an addressable artifact, its home address answers "who." If it does not emit anything addressable, you have lost the actor — and that is a departure from my design, not a faithful implementation of it.

NEED_RAW: [4/9, 4/61-4/70] — to confirm no RETRACT verb appears in the FEBE command list and that the document-state enumeration ("deleted bytes / deleted links") is the full set of nullification states I named.
