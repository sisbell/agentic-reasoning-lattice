## Question 1 [theory]

> What was the intended shape for `citation.depends` — specifically, what does the from-slot represent, does the to-slot target documents or tuples, and is the relation meant to be idempotent (set-of-targets) or non-idempotent (sequence of dependency-events)?

The specific construct `citation.depends` — with named slots and dependency semantics — does not appear in Literary Machines. What I specified about Citation Links is more general:

**Citation Link as a type.** I listed it among the literary link types: "Like a footnote reference with bridge to source" (4/54). That is the entirety of my direct treatment.

**The shape inherited from all links.** Every Xanadu link, including a Citation Link, has the same three-endset structure:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" (4/42)

For a citation, the natural reading is: from-set = the citing passage (the bytes doing the citing), to-set = the cited material (the source being pointed to). Both are span-sets over **bytes**, not over "documents" or "tuples":

> "A Xanadu link is not between points, but between spans of data." (4/42)

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." (4/43)

So in my model, the to-slot always targets spans of bytes. If you want "the whole document," you express that as a span covering all its bytes — there is no separate "document-valued" target.

**Idempotency.** I never address this question directly. My link model has two relevant properties that pull in opposite directions:

- *Endsets are sets.* "An arbitrary collection of spans" (4/43) is set-shaped — the search satisfaction rule treats them as sets: "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request" (4/58).
- *Each MAKELINK creates a distinct link with its own permanent address.* Two MAKELINK calls with identical endsets produce two different links at two different addresses, sequenced by creation order: "The links designated by a tumbler address are in their permanent order of arrival" (4/31).

So whether `citation.depends` is "the set of cited spans" or "the sequence of citation events" depends on whether you read at the **endset level** (set semantics) or the **link-instance level** (each MAKELINK is its own event, ordered, addressable, deletable independently).

NEED_RAW: 4/53-4/55 for the full Citation Link description; 4/56-4/58 for link search semantics that bear on whether multiple equivalent links collapse or remain distinct. The term `.depends` and any decomposition of citation into a dependency relation is project-level work, not something I specified in Literary Machines — that design decision is yours to make, and either reading is consistent with my framework.
