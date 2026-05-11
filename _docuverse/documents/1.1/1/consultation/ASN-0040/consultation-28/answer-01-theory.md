## Question 1 [theory]

> Did Nelson's design require at least one root address (e.g. an "Earth node" or designated initial position) to exist at system genesis, or did the design admit a system that begins with an empty address space and grows entirely by baptism?

Yes — my design required at least one root. The address "1" must exist at genesis; it cannot be empty.

The key passage is at 4/28:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

This is architecturally forced by how baptism works. Baptism is *downward* subdivision — forking new digits to the right under an existing owned number:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

You cannot baptize "1.2" without an owner of "1" first existing to do the baptizing. The forking tree must have a root.

Three points worth noting:

1. **The "1" serves a dual purpose.** It is simultaneously the founding server AND the designator for "the entire docuverse." A digit of "one" with leading zeros designates "all of" a level — so `0.0.0.1` means "the entire docuverse" [LM 4/38]. The root and the universe share the same numeral.

2. **The root need not have stored content.** Ghost elements (see `ghost-elements.md`) tell us that "while a number on the line may represent a document or an account, that doesn't mean there's an object stored for it" [LM 4/23]. So "1" must exist as an *addressable position* — the conceptual root of the tree — but it doesn't require any byte to be stored there. The address space is abstract; the storage is sparse.

3. **The docuverse is one forking tree, not many.** "So the docuverse is all really one big forking document" [LM 4/18]. There is no allowance for multiple disjoint top-level roots growing independently. Everything traces back to the single "1."

So: empty-genesis growth-entirely-by-baptism is not what I designed. The "1" is the designated initial position — it must be there before anything else can be baptized.
