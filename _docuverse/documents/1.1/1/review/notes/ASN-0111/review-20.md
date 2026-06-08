# Review of ASN-0111

## REVISE

### Issue 1: RL4 contradicts itself on whether the read discloses ownership
**ASN-0111, RL4 (Home disclosure) and Claims table**: The claims-table row reads "Home disclosure — `home(a)` is determined by the read key alone, independent of endsets; **the read reveals ownership**." The body two sentences later states: "**The read does not output the home** — `readlink(a, Σ)` returns endsets only."
**Problem**: These cannot both stand. `home(a)` is recoverable from the *address* `a` by T4 field projection (L2) — a caller derives it from the key it must already hold to invoke the read, *without performing the read at all*. The read's output is endsets only. So ownership is disclosed by the key, not by the read. The section heading "What the read reveals that the endpoints do not" lists ownership as the third item, conflating "learnable from the address" with "returned by the read." The whole point of READLINK (consulting only `Σ.L`) is undercut by claiming it surfaces a field that is purely address-derived and not in its output.
**Required**: State the claim precisely — the *read key* `a` encodes `home(a)`; the read itself returns endsets and does not output the home. Drop "the read reveals ownership" from the table, or rephrase to "the caller holding the key can derive ownership." Reconcile the "What the read reveals" framing so home is attributed to the address, not the read.

### Issue 2: Method-narration meta-prose that advances no claim
**ASN-0111, The problem (final paragraph)**: "The reasoning below proceeds by asking, repeatedly, *what must be true for the read to deliver the recorded relationship?* — and refining the specification each time the answer forces a new commitment."
**Problem**: This is essay content describing the note's rhetorical method, not a claim, definition, or step of reasoning. A precise reader must skip it to reach content. This is exactly the meta-prose the anti-bloat classifier targets.
**Required**: Delete the sentence; the derivation sections speak for themselves.

### Issue 3: Defensive existence-justification preamble in the invariants section
**ASN-0111, Invariants governing the returned structure (opening)**: "These are not new obligations but the foundation invariants viewed through the read interface; an alternative implementation's read must honour them because the stored values of any reachable state do. They are claims about the reachable class of states, not about arbitrary stores."
**Problem**: This is prose explaining *why the invariant restatements are present* and *why they hold* rather than stating what they say — it duplicates the standing-precondition paragraph already established under "Deriving the read" ("Where we write 'for a state `Σ`,' read 'for a reachable, invariant-satisfying `Σ`'"). The reachable-state point is now made in two sections in different words.
**Required**: Reduce to a single clause keying the invariants to the already-established standing precondition; remove the alternative-implementation justification, which restates the standing precondition without advancing it.

## OUT_OF_SCOPE

### Topic 1: Validity/currency a reader may conclude from a read alone
**Why out of scope**: The first Open Question (what a reader can conclude about continued validity without consulting an arrangement) is correctly deferred — it concerns the read/follow boundary and belongs to a future traversal or validity ASN, not this one.

META: (none — the ASN stays squarely on specifying the read operation and its guarantees.)

VERDICT: REVISE
