# Failure-Side Priming

## Pattern

When an LLM both produces and judges findings in a loop, feed the next pass only the findings that downstream judgment **rejected**, paired with the rationale that rejected them. Never feed accepted findings.

## Mechanism

In-context learning has asymmetric signal across the produce-judge interaction:

| Outcome | What persists | What the next judge sees |
|---|---|---|
| Finding accepted | Edit to artifact | Current artifact (post-edit). The lesson is invisible — only the corrected state is observable. |
| Finding rejected | Comment + written rationale | Both: the finding text and the rationale that refused it. Full teaching signal preserved in language. |

Feeding the union — accepted plus rejected — flattens the asymmetry. The accepted findings, which represent confirmed types of issue, look to the next judge like *templates to apply* rather than completed work. The judge pattern-matches across the union, and successful variants of those templates produce successively smaller false positives until the loop runs out of cycles.

Feeding only rejections, framed explicitly as "these were declined as invalid," cuts pattern-matching the right way — toward suppression of those shapes, not replication.

## Detection

The signature is a sequence of cycles where:

- Each cycle's findings have the same conceptual shape.
- Each cycle's edit is smaller than the last.
- All findings are accepted (resolution.edit, never resolution.reject).
- The artifact's correctness was not at issue in any cycle — only its style or density.
- Convergence arrives by hitting the iteration cap, not by the producer reporting clean.

When that pattern appears, the producer has fed itself into a perfectionism corner.

## When it applies

Any LLM-as-judge site where:

- The finding text is rich (paragraph of reasoning, not a label) — pattern-matchable shape exists.
- Rejections produce written rationales, not just flags.
- The cycle is bounded — perfectionism cycling is observable as a sequence.
- Convergence is gated by the producer's verdict.

In this codebase: the cone reviewer, full-review reviewer, note-convergence reviewer, validate-revise per-rule reviser, contract producer in claim derivation. Each fits the shape.

## Origin

Surfaced during ASN-0034 cone-review work on T4 (HierarchicalParsing). Four consecutive cycles produced REVISE findings, each accepted, each finding successively smaller variants of the same theme — "redundant narration about dependencies" — until the prose was tightened past any reader benefit. The proof itself was correct in cycle 1 and stayed correct.

The reviewer was being fed up to five prior reviews' full finding bodies on every cycle. It pattern-matched on its own past outputs.

## Related

- [Audit by Content](../design-notes/audit-by-content.md) — the rationale text is where the teaching signal lives. This pattern depends on rationales being read, not just counted.
- [Production Drive](../design-notes/production-drive.md) — perfectionism cycling is the production drive's failure mode at the LLM-as-judge boundary.
- [Convergence Protocol](../protocols/convergence-protocol.md) — defines the comment/resolution/rejection machinery whose rejection state primes future passes.
