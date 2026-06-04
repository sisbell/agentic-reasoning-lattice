## Question 1 [theory]

> Was REARRANGE_K intended to be defined on every input satisfying R-PRE — including ones that yield M'(d) = M(d) — or should identity-producing invocations lie outside its domain?

I can't open the page images or local files in this session (no file-read tool is available to me here), so I'm answering from the verified curated sources, which cover REARRANGE at LM 4/67.

## Short answer

`REARRANGE_K` should be **defined on every input satisfying `R-PRE`, including invocations that yield `M'(d) = M(d)`**. Identity-producing invocations belong *inside* the domain, not outside it.

## Why this follows from Nelson's intent

Nelson defines REARRANGE entirely by its **cut points**, never by whether the result differs from the original:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." (4/67)

Three consequences:

1. **The domain is the set of well-formed cut specifications, not the set of "changes."** Nelson's operation is fully determined by where you cut. There is no clause in his description excluding cuts that happen to leave the arrangement unchanged (e.g., equal adjacent regions, or degenerate cut placement). If `R-PRE` captures cut well-formedness, then satisfying `R-PRE` is sufficient for membership in the domain.

2. **Excluding identity invocations would make the domain depend on the output, which is circular.** To decide whether an input is legal you'd have to first compute `M'(d)` and compare it to `M(d)`. A precondition that quietly depends on its own postcondition is exactly the kind of non-mechanical gate Nelson's protocol avoids — FEBE operations are specified by their inputs, "to be handled invisibly by programs" (operations, 4/61), not by inspecting their results.

3. **A no-op rearrange is a coherent event in the version model, not an illegal one.** Because edits act on the Vstream while Istream is untouched (`i-space-v-space`), a REARRANGE that yields `M'(d) = M(d)` is simply a Vstream operation whose mapping ends up equal to the prior mapping. Nothing in Nelson's model treats "produced the same arrangement" as an error condition; it's an ordinary, total case.

So the cleaner formalization keeps `REARRANGE_K` **total over `R-PRE`**: identity-producing inputs are in-domain and map to `M'(d) = M(d)`. This also keeps `REARRANGE_K` composable with the other operations without a special-case carve-out.

## Caveat on scope

NEED_RAW: 4/67 — only if you want me to confirm there is no *additional* sentence on that page constraining cut placement beyond what the curated extract quotes. The curated sources give Nelson's full operational description of REARRANGE but say nothing explicit about domain boundaries or identity results; the conclusion above is a design-intent inference from (a) his cut-point definition, (b) the input-driven nature of the FEBE protocol, and (c) the Vstream/Istream separation — not a verbatim ruling by Nelson. If your spec's `R-PRE` encodes something stronger than cut well-formedness, that would be the place to re-examine.
