## Question 2 [theory]

> Does the count assert that exactly that many links currently exist with that description, or only that at least that many were once created?

## Short answer

The count asserts how many links **currently** satisfy that description — not how many were ever created. It is a present-tense count of currently-addressable matching links, not a cumulative tally.

## Reasoning from the sources

**1. The search/count model is satisfaction-based and present-tense.**

The counting operation (`FINDNUMOFLINKSFROMTOTHREE`) is the count form of the same search that `FINDLINKSFROMTOTHREE` performs. Nelson describes that search in the present tense — "all links which **are**":

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

And the satisfaction rule:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

A count is just the cardinality of the set of links that *satisfy* — i.e., that presently exist and match.

**2. Deleted links do not satisfy, because they are "not currently addressable."**

Links can be deleted by their owners, and once deleted they leave the addressable set:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

Since a deleted link is "not currently addressable," it cannot satisfy a live search request, so it is not in the count. This is exactly why the count means "how many exist now" rather than "how many were ever made."

**3. Don't confuse the count with link *addresses*, which are cumulative.**

There's a real cumulative quantity in the system — but it's the addressing, not the count. Link instance addresses are assigned in permanent order of arrival and never renumbered:

> "The links designated by a tumbler address are in their permanent order of arrival." (4/31)

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

So the *highest link number* in a document reflects total links ever created (deleting link 2.5 doesn't renumber 2.6…2.N). But a **count of links matching a description** is a different thing: it reflects only the links that currently exist and currently match. The two can diverge whenever links have been deleted or edited so that an endset no longer falls within the request.

## One caveat

The curated sources give the verbatim text for `FINDLINKSFROMTOTHREE` (4/69) but not a separate verbatim definition for `FINDNUMOFLINKSFROMTOTHREE`. My conclusion treats the count as the cardinality of that same satisfaction set, which is consistent with how the curated material describes it ("Counts links matching endset criteria"). If you want Nelson's exact wording for the count operation specifically:

NEED_RAW: 4/68–4/69
