## Question 3 [theory]

> In Nelson's design vocabulary, are coverage-style relations (where later assertions supersede earlier ones) and comment-style relations (where each emission is a distinct event) meant to be structurally distinct kinds of links, or are they the same kind of link with different layer-level reading conventions?

# Links Are Structurally Identical; Semantics Live in the Type Endset

The vocabulary "coverage-style" and "comment-style" and "layer-level reading conventions" is not mine — those are framings being imposed on my design. But mapping them onto my actual architecture:

## All links share one structure

Every link in Xanadu has the same three-endset form regardless of its semantic purpose. There is no structurally distinct "supersession link mechanism" versus "comment link mechanism." The difference is encoded entirely in the third endset (the type), which is matched by address, not by content.

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose. **This is done with a mechanism which is powerful and symmetrical.**" [LM 4/43]

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. **This is symmetrical with the other endsets.**" [LM 4/44]

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. **The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address.**" [LM 4/44-4/45]

So a Comment Link and a Document Supersession Link are not different kinds of links — they are the same kind of link with different addresses in the type-set. The front end interprets that type address to render the appropriate behavior.

## The list confirms uniformity

In my tentative listing [LM 4/52-4/55], Comment Link, Counterpart Link, Document Supersession Link, Suggested-Threading Link, Citation Link — all sit alongside each other in one open-ended catalog. None are privileged with special machinery:

> "A TENTATIVE LISTING OF SOME LINK TYPES. Link types are open-ended, so this is not the original beginning, but a first provisional, to give the flavor of current thinking." [LM 4/52]

## The "reading convention" is the front end

You're right that interpretation happens at a layer above the link mechanism. The back end stores and indexes; the front end decides what a "supersession" type means versus what a "comment" type means. From [LM 4/61]:

> "None of these commands are to be seen by the user. The user's concerns are document content and links, and the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things."

This is deliberate. I did not want to bake semantic categories into the storage substrate. Categorization systems have a half-life [LM 2/49]; the architecture must outlive any particular semantic taxonomy.

## One important caveat: supersession also touches the version mechanism

While the Document Supersession Link itself is just an ordinary metalink, *coverage* in the deeper sense — newer versions replacing older — does have structural support outside the link mechanism: the version subfield in the tumbler address [LM 4/29]. Versioning is built into addressing. Commentary is not. So if your "coverage-style" relation is meant to invoke version supersession, there is a structural distinction *at the addressing level*, but the link that announces it ("this supersedes that") remains an ordinary three-endset link.

## Summary

| Level | Coverage-style (e.g. supersession) | Comment-style |
|---|---|---|
| Link structure | Three endsets | Three endsets — identical |
| Type endset | Points to "supersession" address | Points to "comment" address |
| Storage mechanism | Same | Same |
| Search mechanism | Same (address match) | Same (address match) |
| Front-end interpretation | "Replace what you were reading" | "Show alongside" |
| Underlying addressing | May also involve version subfield | Pure link, no version interplay |

The structural answer is: **same kind of link**. The behavioral answer is: **different reading conventions on the same mechanism**. Both are intentional. The link layer is deliberately neutral; the meaning lives in the type endset's address and in what the front end does with it.

NEED_RAW: 4/52 (full tentative listing of link types) — to confirm whether I distinguished "comment" and any coverage-style type as architecturally separate or just listed them side by side. The curated extract shows them in one undifferentiated catalog, which supports the structural-uniformity reading.
