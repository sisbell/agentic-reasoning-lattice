# Failure-Side Priming

## Pattern

When an LLM produces and judges findings in a convergence loop, it gets smarter across cycles by reading what *prior* cycles raised and then refused. The teaching signal is not the finding alone — it's the finding *paired with the reviser's rationale for declining it*. Carrying that pair forward as in-context examples lets each cycle's reviewer learn from the shape of past invalid findings before producing its own.

This is in-context learning from failures, scoped to the running loop. The substrate already records every rejection-with-rationale; the pattern is to read them back as priming context for the next pass.

## Forces

- **LLM judgment improves with examples.** A reviewer cold-starting on an artifact applies general criteria. A reviewer primed with concrete prior examples applies *those* criteria, sharpened by what the running domain has already deliberated.
- **Successes self-document; failures don't.** When a finding is accepted, the artifact is edited to address it — the corrected state is what the next reviewer sees. The lesson lives in the result. When a finding is refused, the artifact is unchanged; without an explicit record, the next reviewer has no way to know the issue was already considered.
- **Rationale is the carrier.** A rejection without reasoning is just a label — "this was refused." A rejection with reasoning is a generalizable lesson: "this *kind* of finding was refused *because* Y." The next reviewer can apply the rationale's logic to candidate findings of similar shape.
- **Recency matters.** The artifact evolves; lessons from rejections decades ago may no longer apply. A bounded recent window keeps priming relevant.
- **Over-priming flattens.** If the reviewer is fed *every* prior finding (accepted and refused alike), pattern-matching cuts in both directions — the reviewer learns from the accepted shapes too, and produces variants of those. The teaching signal is asymmetric; the priming should be too.

## Mechanism

| Outcome | What persists in the running domain | What the next reviewer can learn from |
|---|---|---|
| Finding accepted | Edit to artifact | Current artifact (post-edit). The lesson is implicit in the corrected state. |
| Finding refused | Comment + written rationale | Both the finding text and the rationale that refused it. The lesson is explicit in language. |

The teaching signal lives on the failure side. Priming the next reviewer with the failure side passes that signal forward; priming with both sides flattens it; priming with neither leaves each cycle to relearn from scratch.

## Structure

```
cycle N:
  reviewer ──→ finding ──→ reviser
                              │
                       accept ──→ artifact edited
                              │
                       refuse ──→ comment + rationale recorded in substrate

cycle N+1:
  reviewer ←── recent (refused, rationale) pairs
  reviewer ──→ better-calibrated findings
```

Each cycle's reviewer reads the past few cycles' refusals before producing its findings. The substrate is the medium; recency is the cap.

## When it applies

- The judge produces findings in language form, not just classifications.
- Refusals carry written rationales, not just flags.
- The producer and judge are looped — the producer's next invocation can read the loop's running history.
- The domain is one where reasoning recurs — finding shapes repeat across cycles, so priming generalizes.

## When it doesn't apply

- The judge gives only thumbs-up/thumbs-down, no rationale text. There's nothing to prime with — the lesson didn't survive the rejection.
- The artifact is single-shot — no convergence loop, no later pass to prime.
- Findings are highly heterogeneous — each is unique enough that prior shapes don't generalize.

## Origin

Surfaced during ASN-0034 cone-review work on T4 (HierarchicalParsing). The reviewer was being primed with up to five prior reviews' full finding bodies regardless of outcome. Across four cycles the reviewer produced successively smaller variants of the same finding shape, each accepted, none affecting correctness — only prose density. Restricting the priming context to the failure side removed the seed for that recurrence while preserving the legitimate lesson the priming was meant to carry.

## Related

- [Audit by Content](../design-notes/audit-by-content.md) — the rationale text is where the teaching signal lives. This pattern depends on rationales being read in full, not just counted.
- [Consult Authority](consult-authority.md) — both patterns ground LLM judgment in something other than the LLM's own prior output. Consult Authority reaches outward to source material; Failure-Side Priming reaches backward to recorded rejections.
- [Convergence Protocol](../protocols/convergence-protocol.md) — defines the comment/resolution/rejection machinery whose rejection state this pattern reads.
