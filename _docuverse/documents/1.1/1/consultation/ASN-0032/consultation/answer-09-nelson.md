## Question 9 [nelson]

> Must the system guarantee that every version of a document preserves the links that were present at each point in its history?

## Yes — but the mechanism is implicit, not independently specified

Nelson's architecture strongly implies that link state is preserved per-version, but he never provides an explicit, separate guarantee for link history. The evidence comes from three converging lines.

### 1. Deleted links explicitly await historical backtrack

The strongest direct evidence is the status description for deleted links on page 4/9:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, **may remain included in other versions**.)" [LM 4/9]

This exactly parallels deleted bytes:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "may remain included in other versions" means that if you delete a link from version N, earlier versions that contained that link still show it. This only works if versions capture link state.

### 2. The general historical backtrack guarantee covers links

Nelson's version history guarantee is stated broadly:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

And the retrieval operation returns both content types together:

> **RETRIEVEV**: "This returns the material (text and links) determined by \<spec set\>." [LM 4/67]

If RETRIEVEV returns text *and* links, and the system promises reconstruction of any previous state, then that reconstructed state must include the links that existed at that time.

### 3. Links live in the append-only store

Links have permanent tumbler addresses in the `0.2.N` subspace, assigned in order of arrival:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

The append-only model means these addresses are never reused. A link at `D.V.0.2.5` always refers to the 5th link created in that document. "Deleting" it removes it from the current V-space view but not from I-space — the same non-destructive semantics as byte deletion.

### What IS ambiguous

There is a genuine gap around **CREATENEWVERSION**:

> "This creates a new document with the contents of document \<doc id\>." [LM 4/66]

Nelson separately describes a document as consisting of "its contents (including history and alternatives) and its out-links" [LM 2/31]. Whether "contents" in the CREATENEWVERSION command includes out-links or only bytes is not explicit. The grammar of 2/31 could be read either way — "contents" as an umbrella term, or "contents" and "out-links" as distinct components.

However, the weight of evidence favors inclusion. Links are part of the document's tumbler subspace, retrieval returns both, and the deleted-link description explicitly references version preservation.

### What Nelson does NOT specify

- The **mechanism** for link-specific historical backtrack. Byte history has detailed infrastructure (enfilades, I-space/V-space separation). Link history has no corresponding architectural description.
- Whether link history is tracked with the same granularity as byte history (every individual change vs. version snapshots).
- How link deletion interacts with SHOWRELATIONOF2VERSIONS — whether version comparison reports link differences, not just content differences.

NEED_RAW: [4/9, 4/30-4/31] — to verify the full context of the deleted-links diagram and the link addressing details around version boundaries.

### Summary

The system **should** guarantee per-version link preservation. This follows from the explicit "may remain included in other versions" status of deleted links, the general historical backtrack promise, and the append-only storage model. But Nelson treats this as a consequence of the architecture's general properties rather than stating it as an independent guarantee — and the detailed mechanism for link history reconstruction is left unspecified.
