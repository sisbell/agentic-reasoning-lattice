## Question 10 [nelson]

> When content is shared rather than copied, must the system guarantee that all parties see identical content, or can the receiving document present a version that diverges over time?

## Shared Content: Identity vs. Arrangement

The answer is precise and has two layers, because Xanadu separates **content identity** (I-space) from **content arrangement** (V-space).

### Layer 1: Bytes Are Immutable — Always Identical

At the I-space level, there is no possibility of divergence. Content at an I-address never changes. When a receiving document transcludes bytes, it references their permanent I-address, and those bytes are fetched from their home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The system does not copy bytes into the receiving document. It references them. Everyone who references I-address X sees the same bytes at X, always.

### Layer 2: Windows Can Diverge by Design — Two Explicit Modes

However, the *source document's arrangement* can change (its V-space evolves through editing and versioning). Nelson explicitly provides **two window modes** that handle this differently:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

**Location-fixed (floating in time):** The receiving document tracks the source's current arrangement. Updates propagate automatically. All parties see the same current state. This is Nelson's solution to the distributed update problem:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

**Time-fixed (fixed in time):** The receiving document freezes at a specific version. The source may evolve, but the window shows what it showed at the moment of citation. The user can explicitly ask to see the current state, but divergence is the default behavior in this mode.

### So: Divergence Is Permitted, But Not Silent

The system guarantees that:

1. **Bytes are always identical** — I-space content is immutable
2. **Location-fixed windows track the source** — no divergence
3. **Time-fixed windows deliberately diverge** — but the user can always query "What has this passage become?"
4. **You always know where you are** — attribution is structural, so even in a divergent window, you can trace back to the source and compare

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The critical design insight: divergence in Xanadu is never *accidental* or *hidden*. It is either (a) impossible (I-space immutability) or (b) an explicit user choice (time-fixed windowing) with a built-in mechanism to reconcile ("What has this passage become?"). The receiving document cannot *silently* present different content from the source — either the window tracks the source, or the window is frozen at a declared point in time, and the system knows the difference.

### What About Derivative Documents?

There is a third case. A user can create a **derivative document** that explicitly modifies transcluded content:

> "A particular form of compound document is one which consists explicitly of an original and changes to it — which may be made by anyone." [LM 2/38]

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

Here, the derivative document *does* present different content — but the original is untouched, and the reader can always navigate back:

> "The old viewpoint is still present too — you can always say, 'Show me what this originally was.'" [LM 2/45]

### Summary

| Scenario | Divergence? | Guarantee |
|----------|-------------|-----------|
| Same I-address bytes | Never | I-space is immutable |
| Location-fixed window | No | Tracks source automatically |
| Time-fixed window | Yes, by design | User can query current state |
| Derivative document | Yes, by design | Original always accessible |

The system never allows *silent, undetectable* divergence. It either prevents it (immutable bytes), or makes it explicit and traceable (frozen windows, derivative documents with navigable originals).
