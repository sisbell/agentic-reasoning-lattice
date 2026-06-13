## Question 9 [theory]

> When a link is retracted or withdrawn from visibility, must the count exclude it immediately, and how does that exclusion coexist with the system's commitment to the permanence of what was once created?

## Short answer

Yes — the *current* count must drop it the instant it is withdrawn. And no — that costs nothing against permanence, because the two statements are about two different spaces. "Exclude it now" is a fact about the Vstream, the current arrangement. "It endures forever" is a fact about the Istream, the permanent record. A link can leave the live view in the very breath that it stays in the archive, and the linking enfilade was built precisely so both are true at once. When Barus solved it, the property I had asked for was exactly this pairing:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

*Instantaneous and permanent.* That is the whole answer in three words. The rest is why each half holds.

## Why the count excludes it immediately

A link count is not a stored number that someone remembers to decrement. It is the cardinality of a search — `FINDNUMOFLINKSFROMTOTHREE` answers "how many links satisfy this request, *right now*?" — and the rule for satisfaction is:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

A retracted link is, by definition, no longer present to satisfy anything. My note on a document's technical contents lists this state explicitly:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

*Not currently addressable.* If it cannot be addressed in the current docuverse, it cannot satisfy a search of the current docuverse — so it is not in the count. There is no separate "please update the tally" step to forget or defer, because the tally was never kept apart from the index. The enfilade holds that index in "canonical order" at all times [LM 1/34], so the moment of withdrawal *is* the moment of exclusion. And the withdrawn link costs everyone else's counting nothing:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

Immediacy here is not a latency promise bolted on afterward. It falls out of counting-by-search over an always-canonical index.

## Why that does not touch permanence

Here is the move that dissolves the apparent paradox. Withdrawal is a **Vstream** act, not an **Istream** act. Read the same annotation again:

> "...awaiting historical backtrack functions, may remain included in other versions." [LM 4/9]

The link left the *current arrangement*. It was not destroyed. This is exactly the discipline I insist on for text: DELETE removes content from a document's current view but never from the permanent store, and the removed thing "may remain included in other versions." Nothing in Xanadu is ever truly destroyed; it becomes *not-currently-addressable*, which is a claim about the present view, not about existence.

So the count is **view-relative**, and that is the reconciliation:

- A count taken against the **current** version excludes the withdrawn link — immediately.
- A count taken against an **earlier** version, or against **another document that had included** that link, still includes it — permanently.

Permanence never promised that a withdrawn link would keep appearing in the live tally. It promised that the link, its address, and its history would never be lost — that you can always go back and find it, count it, and follow it where it still lives. Both promises are kept, and they are kept by separating identity (Istream) from arrangement (Vstream).

## Two kinds of counting — and they behave oppositely

It sharpens the picture to notice that I built two different counters, and they treat withdrawal in opposite ways, each correctly:

1. **The search count** ("how many links point here *now*?") is a snapshot of the live view. It *excludes* the withdrawn link at once. Its job is to track the present.

2. **The cash register** is the opposite kind of object:

   > "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document. The cash register has no size limit." [LM 5/13]

   It records *deliveries that already happened*. Withdrawing a link tomorrow does not un-deliver the times it was followed yesterday; the register only ever increments. Here permanence is more absolute still: the historical fact of use is monotonic and is never retracted, regardless of present visibility.

These never collide, because they answer different questions — "how many are there now?" versus "how much has flowed?" The system is obliged to keep both honestly.

## One caution about the word "visibility"

"Withdrawn from visibility" can mean two different things, and only one of them changes the count:

- **Retraction / deletion** by the owner makes the link *not currently addressable* [LM 4/9] — the case above; the current count drops it at once.
- **Filtering** at a front end — what I called *sieving* — hides a link from one reader without affecting what exists:

  > "This filtering by different attributes we call 'sieving', and it can only be set up for a comparatively small number of traits-- say, location and author and time." [LM 2/47]

  A sieved link is still in the docuverse and still counted at the back end; it is merely not shown to that viewer. "Invisible to me right now" via a filter does not, and must not, change anyone's count.

## Where my intent stops and implementation begins

I specified that owners may withdraw their own links, and that withdrawal yields the not-currently-addressable / recoverable state [LM 4/9]. I also insisted that things others depend on do not simply vanish:

> "It is in the common interest that a thing once published stay published... Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

These sit together comfortably *because* withdrawal is never destruction: "staying published" is honored at the Istream level even when a link leaves the current view. What I did **not** fully pin down is the governance around a *published* link that others have already meta-linked to — whether its retraction is the owner's unilateral act or is itself subject to that "lengthy due process." That is a contractual question I left open. The structural guarantee — immediate exclusion from the live count, permanent survival in the record — holds either way.
