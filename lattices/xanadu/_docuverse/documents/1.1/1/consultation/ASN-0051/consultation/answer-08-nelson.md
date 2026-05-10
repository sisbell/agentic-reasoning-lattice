## Question 8 [nelson]

> Must the system preserve the directionality and endpoint ordering of a link across all state changes, or can editing operations ever alter which end is the source and which is the target?

## Link Directionality Is Fixed at Creation and Immutable

The system **must** preserve the directionality and endpoint ordering of a link across all state changes. No editing operation can alter which end is the source and which is the target.

### The Structural Argument

A link's three endsets (from-set, to-set, type) are assigned at creation via MAKELINK and become permanent structural properties of the link. Nelson:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" [LM 4/42]

The parenthetical — "what 'from' and 'to' mean depend on the specific case" — tells you that directionality carries **semantic weight** chosen by the link creator. A citation link goes from citing text to source. A comment link goes from commentary to subject. Swapping these would invert the meaning.

### No Operation Exists to Modify Links

Of the 17 FEBE commands in XU.87.1, none modifies a link's endsets after creation. The link operations are:

- **MAKELINK** — creates with fixed endsets
- **FINDLINKSFROMTOTHREE** — searches by endset constraints
- **RETRIEVEENDSETS** — returns endsets as stored
- **FINDNUMOFLINKSFROMTOTHREE** / **FINDNEXTNLINKSFROMTOTHREE** — pagination

There is no EDITLINK, MODIFYLINK, or SWAPENDSETS. The only way to "change" a link's directionality would be to delete it and create a new one — which produces a different link at a different address.

### Editing Operations Cannot Reach Link Structure

The editing operations (INSERT, DELETEVSPAN, REARRANGE, COPY, APPEND) operate on **document content** — bytes in the Vstream. Links point to **Istream addresses**, which are permanent. Nelson explicitly states:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Editing changes *where* bytes appear in the Vstream. It does not touch which bytes a link's from-set or to-set reference, let alone swap them.

### Survivability Preserves Endset Identity

Link survivability means links survive editing of the *content they point to*:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

The surviving link retains its original endset assignment. If the from-set bytes survive and the to-set bytes survive, the link survives — with the from-set still "from" and the to-set still "to." Survivability is about **persistence**, not transformation.

### The One-Sided Link Confirms This

Nelson's discussion of one-sided links (like paragraph designators) reveals that endpoint ordering is a deliberate architectural choice, not something the system infers:

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." [LM 4/48]

He finds it "inane" to call a single endset "from" — because the from/to distinction carries real semantic meaning. If the system could freely swap endpoints, this complaint would be nonsensical.

### Summary

Link directionality is:
1. **Assigned at creation** — via MAKELINK's three endset parameters
2. **Semantically meaningful** — "what 'from' and 'to' mean depend on the specific case"
3. **Structurally immutable** — no FEBE operation modifies link endsets
4. **Unreachable by editing** — content editing changes Vstream, not link structure
5. **Preserved through survivability** — surviving links keep their original endpoint ordering

The system has no mechanism, accidental or deliberate, by which an editing operation could swap or alter which end is source and which is target.
