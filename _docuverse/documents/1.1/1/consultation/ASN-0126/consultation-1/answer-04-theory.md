## Question 4 [theory]

> Are typed relations intended to be allowed to reference addresses where no content yet exists (ghost references), or must every endset address resolve to stored content?

Yes — typed relations are explicitly **intended** to reference addresses where no content exists. These are what Nelson calls "ghost elements," and they are a deliberate design feature, not a degenerate edge case.

## The core answer

A link's type is itself an endset (the "three-set"), and like all endsets it points to addresses on the tumbler line. Crucially, the search mechanism matches on the **address** of the type, not on whatever may (or may not) be stored there:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

This is what makes ghost references valid:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

## Why this works architecturally

Ghost elements are a fundamental property of the address space, not a special case for link types. Only content bytes and links are ever physically stored; everything else (servers, accounts, documents) is a conceptual position on the tumbler line:

> "Thus the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage. Consider what we may call 'ghost elements'." (4/23)

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

So the answer to your either/or is clear: **endset addresses do NOT need to resolve to stored content.** The type endset in particular is designed to exploit this — you define a link type simply by choosing an address to represent it, with nothing necessarily stored there. This is precisely what makes the type system open-ended and user-extensible without any registry or schema:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." (4/43)

## Important scope note

This guarantee is strongest and most explicit for the **type** endset, because type-matching is address-based by design. The from-set and to-set are also arbitrary endsets that "may point to spans anywhere in the docuverse" (4/45), and the survivability model tolerates ends where content has been deleted — but their *purpose* is to connect actual content, so a from/to endset pointing at a permanently empty address is semantically inert even though it is structurally legal. The type endset is the case where pointing at a ghost address is not just permitted but the normal, intended idiom.

**Design intent summary:** Typed relations are explicitly allowed (and expected) to use ghost references. The system never requires a type address to resolve to stored content, because type search compares addresses, not contents.
