# Failure-Side Priming

## Pattern

When an LLM serves as both producer and judge of structured findings — and an outer process loops the produce-judge cycle until convergence — feeding the judge's prior findings back as context for the next pass creates a pattern-matching feedback loop. The judge sees its own past outputs, generalizes their *shape*, and produces successively smaller variants of the same finding type until the loop runs out of cycles or the variants become so trivial they cross the OBSERVE/REVISE threshold by accident.

The fix is asymmetric: pass forward only the findings that were **rejected** by downstream judgment, paired with the rationale that rejected them. Successful findings get absorbed into the artifact (the prose, the code, the proof) and their teaching signal is the absence of that issue going forward. Failed findings keep their full teaching signal — what was raised, what was wrong with raising it — and that's exactly what the next judge needs to suppress the same false positive.

## Mechanism

In-context learning has asymmetric signal between the two outcomes:

| Outcome | What persists | What the next judge sees |
|---|---|---|
| Finding accepted | Edit to artifact | Current artifact (post-edit). The lesson is invisible — only the corrected state is observable. |
| Finding rejected | Comment + rationale | Both: "this was raised" + "this was wrong because Y." Full teaching signal preserved. |

If the next judge is fed *all* prior findings (accepted + rejected), it sees a mix of validated patterns (the accepted ones) and invalidated patterns (the rejected ones). Without the validation/invalidation labels visible, it pattern-matches across the union — and the accepted findings, which represent confirmed types of issue, look like *templates to apply* rather than completed work.

If the next judge is fed *only* rejections-with-rationale, it sees a curated negative-example set. The framing is unambiguous: these patterns were considered and refused. Pattern-matching now cuts the right way — toward suppression, not replication.

## When it shows up

Wherever the produce-judge cycle has these properties:

1. **Finding text is rich.** The finding is a paragraph of reasoning, not a label. Pattern-matchable shape exists at the language level.
2. **Rejections produce rationales.** When a finding is refused, the refusal is recorded with a written explanation, not just a flag.
3. **The cycle is bounded.** The producer can be invoked multiple times in a row — perfectionism cycling is observable as a sequence of progressively-smaller findings of the same shape.
4. **Convergence is gated by the producer's verdict.** As long as the producer keeps surfacing REVISE-class findings, the loop continues. Without an external bound, it runs to its iteration cap.

## Detection

The signature is a sequence of cycles where:

- Each cycle's findings have the same conceptual shape (e.g., "redundant prose about deps").
- Each cycle's edit is smaller than the last.
- All findings are accepted (resolution.edit, never resolution.reject).
- The artifact's correctness was not at issue in any cycle — only its style.
- Convergence eventually arrives by exhausting the iteration cap, not by the producer reporting clean.

When that pattern appears, the producer has fed itself into a perfectionism corner. The fix is contextual: tighten what the producer sees so the seed for the next variant is removed.

## Implementation

Substrate-derived implementation in this codebase:

```python
def _declined_findings_for_cone(store, cone_md_paths, max_rejects=5):
    rejects = store.find_links(type_set=["resolution.reject"])
    rejects.sort(key=lambda r: r.get("ts", ""), reverse=True)
    blocks = []
    for r in rejects:
        if len(blocks) >= max_rejects:
            break
        comment_id = r["to_set"][0]
        rationale_path = r["to_set"][1]
        comment = store.get(comment_id)
        if comment["to_set"][0] not in cone_md_paths:
            continue
        finding_body = read(comment["from_set"][0])
        rationale_text = read(rationale_path)
        blocks.append(format_block(finding_body, rationale_text))
    return "\n\n---\n\n".join(blocks)
```

The query is a substrate graph traversal — `resolution.reject` links scoped to the cone's claim paths, sorted by recency, capped at N. No state file, no curation. Past rejections accumulate passively in the substrate as the cycle runs, and each future invocation consumes them.

The prompt that wraps the result frames the section explicitly:

> The findings below were raised on prior reviews and **declined as invalid by the reviser**. Each is paired with the reviser's rationale explaining why it was refused. **Do not pattern-match on them** — surfacing variants of these findings will produce the same outcome.

## Where it applies

Any LLM-as-judge site in this codebase that produces both verdicts and rationales:

- Cone reviewer (claim-convergence) — implementation just landed
- Full-review reviewer (claim-convergence)
- Note-convergence reviewer
- Validate-revise per-rule reviser
- Contract producer in claim derivation

Each follows the same shape — emit findings, downstream judge accepts or rejects, loop until convergence. The pattern is reusable as a context-construction primitive at each site.

## Why "failure-side"

The naming choice contrasts with the obvious-but-wrong "feed history" approach. *Failure-side* names the asymmetry explicitly: the side of the produce-judge interaction that retains its teaching signal in language form is the failure side. The success side is mute by design — the artifact carries the lesson, not a separate record of it.

The principle generalizes: when an in-context learning loop has asymmetric signal preservation between outcomes, prime it with the side that preserves signal. Don't average over both sides; that flattens the curve.

## Origin

Surfaced during ASN-0034 cone-review work on T4 (HierarchicalParsing) on the Xanadu project. Four consecutive cone-review cycles produced REVISE findings, each accepted, each finding successively smaller variants of the same theme — "redundant narration about dependencies" — until the proof's prose was tightened past any reader benefit. The proof itself was correct in cycle 1 and stayed correct; only the surrounding prose was being shaved progressively thinner.

Investigation of `_extract_apex_history` found the loop: the function fed the reviewer up to 5 prior reviews' full finding text on every cycle. The reviewer was steeped in its own past REVISE findings and produced shape-similar variants. Replacing the function with `_declined_findings_for_cone` (this pattern's implementation) removes the seed without losing the legitimate "don't re-raise refused findings" behavior the original was trying to preserve.

## Related

- [Audit by Content](../design-notes/audit-by-content.md) — the rationale text is where the teaching signal lives, not in the resolution label. This pattern depends on rationales being read, not just counted.
- [Production Drive](../design-notes/production-drive.md) — perfectionism cycling is the production drive's failure mode at the LLM-as-judge boundary. Failure-side priming is a context-engineering corrective.
- [Convergence Protocol](../protocols/convergence-protocol.md) — defines the comment/resolution/rejection machinery whose substrate state this pattern queries.
