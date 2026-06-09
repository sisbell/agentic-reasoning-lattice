## Question 2 [theory]

> Is a retraction link itself meant to be discoverable as a result of `FINDLINKSFROMTOTHREE` (e.g. via a type-`R` query), or are retraction links intended to be search machinery that the operation is not obliged to surface as ordinary results?

## Short answer

In my design there is no such thing as a link that is "search machinery the operation is not obliged to surface." A retraction link — like every link — is a first-class object in tumbler-space with its own address, and a type-`R` query to `FINDLINKSFROMTOTHREE` is obliged to return it. There is no privileged class of links exempt from ordinary search results.

First, a flag on terminology: **"retraction link" and "type-R query" are not concepts from *Literary Machines*.** They appear to be constructs of your ASN-0121 work, not mine. I can tell you authoritatively how *any* link — whatever its type — behaves under my operations, but the specific semantics you've assigned to "retraction" are yours to define, and I can only constrain them to the extent they must obey the link model below. NEED_RAW only if you want me to check the raw pages for a "retraction"-named type; I do not believe one exists.

## Why retraction links must be discoverable

### 1. There is essentially nothing but documents and links

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." (4/41)

There is no third category — no "machinery" tier of invisible connective tissue. If it is a link, it lives in tumbler-space and is reachable by link search.

### 2. Search is defined purely by endset satisfaction, including the type endset

`FINDLINKSFROMTOTHREE` is defined as:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

And the satisfaction rule is uniform across all three endsets:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

A type-`R` query is simply a request whose three-set is constrained to the address representing retraction. Any link whose type endset includes that address satisfies the request and is returned. Nothing in the operation's definition allows it to withhold a satisfying link because of what kind of link it is.

### 3. Type is matched by address, not interpreted — so "R" gets no special handling

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44–4/45)

The search engine cannot treat a retraction type differently, because it never inspects what the type *means*. To the back end, `R` is just another address in the three-set. This is precisely why the type system is "open-ended" (4/43) — and why no type can be a hidden one.

### 4. Filtering "junk" is a front-end concern, not a back-end exemption

If your worry is that retraction links would clutter ordinary results, my answer is that suppression happens at the front end, never by exempting a type from search:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

The system's stance is that you can always *constrain* a search to exclude what you don't want, and the back end indexes everything. The "Link Filters" and "Junk-Link Problem" are addressed in front-end design — the back end surfaces; the front end sieves.

## Consequence for your ASN-0121 design

Two things follow, and they bound what "retraction" can legitimately mean in my model:

1. **A type-`R` query must surface retraction links.** That is the affirmative half of your question — yes, unambiguously.

2. **A *general* query cannot silently hide them either.** If a retraction link's from/to endsets fall within some unrelated query's request set, the operation will return it as an ordinary result. The back end has no license to treat it as invisible machinery. If you want a reader not to *see* retractions in a given view, that is a front-end filtering decision (sieving by type), not a property the operation is permitted to assume.

So if any part of your spec relies on retraction links being *structurally* unsurfaceable by `FINDLINKSFROMTOTHREE`, that contradicts the link model. The correct framing is: retraction links are always discoverable; whether they are *displayed* is a filtering choice made above the protocol.

If you want, point me at the ASN-0121 formal statements and I can check whether your retraction semantics are consistent with this constraint.
