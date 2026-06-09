## Question 2 [theory]

> What relationship must each rearranged region bear to the positions it occupied before the transposition?

Short answer: each rearranged region must consist of **exactly the same content** it held before — the same bytes with the same permanent Istream identity. REARRANGE is a pure Vstream operation: it permutes where content *appears* (its V-addresses) without altering *what* the content is (its I-addresses). The relationship is therefore one of **preserved identity / correspondence**: every byte in a transposed region corresponds to the same byte before the move.

Supporting points from the curated sources:

**REARRANGE transposes regions** — it relocates existing content, it does not create or copy:
> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." (4/67)
(`memory/MEMORY.md` "Xanadu Operations" / Literary Machines 4/67)

**The content keeps its byte identity even as ordering changes**, which is what guarantees the correspondence between old and new positions:
> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

**Rearrangement is non-destructive — addresses (I-stream) stay valid**:
> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

**The structural basis**: a document is the mapping from V-addresses to I-addresses; REARRANGE changes that mapping, not the I-content. As the i-space/v-space material states, REARRANGE is a "pure Vstream operation" — the Istream content (and thus identity) is untouched, only its arrangement is permuted.

So the required relationship is: a rearranged region must be **the very same content (same Istream bytes/identity) repositioned** — a permutation of the Vstream that preserves each region's underlying identity and its correspondence to where it previously sat. It may not be a new copy, altered text, or content with new identity.

(Note: Nelson's text in 4/67 describes *what* REARRANGE does but does not state this identity-preservation relationship in those words; that conclusion is drawn from the Istream/Vstream model and the survivability statements at 4/30 and 4/43. If you want Nelson's exact wording on transposition semantics, NEED_RAW: 4/67.)
