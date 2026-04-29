# Consult Authority

## Pattern

During review/revise iteration, the reviser encounters a finding it questions — something that doesn't match its understanding, or a claim it can't verify from context alone. Rather than accepting the finding blindly or rejecting it based on reasoning alone, the reviser consults an external authority: the original source material that grounds the domain.

This opens the review/revise loop to external evidence. Without it, two agents refine each other's output in a closed system — potentially reinforcing errors or drifting from the source. The authority consultation is what keeps the cycle grounded.

In the scientific method, this is the experiment — you don't just theorize and review theories. You go back to the evidence. The hypothesis (the finding) is tested against reality (the authority), not just against other hypotheses.

## Forces

- **Reviewers are imperfect.** An LLM reviewer may hallucinate a finding. The reviser needs a way to check.
- **Revisers are imperfect.** A reviser may misunderstand a finding and produce a bad fix. Consulting the source prevents acting on misunderstanding.
- **Closed loops drift.** Two agents reasoning about each other's output can converge on something internally consistent but wrong. External evidence breaks the loop.
- **Not every finding needs consultation.** Most findings are straightforward — fix the contract, add the dependency. Consultation is selective: only when the reviser is uncertain or the finding challenges established understanding.
- **The authority is finite.** The source material doesn't change. Each consultation extracts more from the same base. Eventually the source is exhausted and the agents must reason from what they have.

## Structure

```
reviewer ──→ finding ──→ reviser
                           │
                    uncertain? ──→ consult authority ──→ grounded revision
                           │
                    clear? ──→ direct revision
```

The consultation is not a separate stage. It happens inside the revise phase, triggered by the reviser's judgment. The authority is accessed on demand, not loaded by default.

## When it applies

- The domain has external sources that can be queried (documents, code, data)
- The sources are more reliable than the agents' reasoning about them
- The review/revise cycle is producing findings that are plausible but unverifiable from context alone

## When it doesn't apply

- In claim convergence, agents work from the note itself. The "authority" is the proof and the foundation statements — already in context. There is no external source to consult.
- When the source has been exhausted — every relevant passage has been incorporated into the note. Further consultation returns nothing new.

## Leads to

[Review/revise iteration](review-revise-iteration.md) — consult authority is what happens inside the revise phase when the reviser needs grounding. It's not a separate cycle — it's a refinement of how revision works.

[Two data authorities](two-data-authorities.md) — the authorities consulted during revision are the same sources that the two channels draw from during initial discovery. The difference: during discovery, the channels systematically extract from the sources. During revision, the reviser selectively returns to them.

[Narrow → Refine → Verify](narrow-refine-verify.md) — consultation happens in the refine phase. It is what makes refinement empirical rather than purely deductive. The scientific method requires going back to evidence, not just reasoning from prior conclusions.

## Applications

### Discovery review/revise

During discovery, the reviewer flags an issue: "S7 claims document-level allocation but Nelson's text says owner-level allocation." The reviser is uncertain — does Nelson really say that? It consults the source (Nelson's *Literary Machines*, specific page) and finds the exact quote. The revision is grounded in the source, not in the reviser's interpretation of the reviewer's interpretation.

### Discovery refinement

A finding claims Gregory's implementation handles a specific edge case. The reviser consults the evidence channel's source (udanax-green code) to verify the claim before incorporating it. The consultation finds the implementation does handle it, but through a different mechanism than the finding described. The revision corrects both the finding and the note.

### When it prevents drift

Without consultation: reviewer says "S8 uses TumblerAdd." Reviser accepts this and adjusts S8 to cite TumblerAdd. Next review: "TumblerAdd is not in the foundation statements." Reviser removes TumblerAdd citation. The cycle oscillates between adding and removing a reference because neither agent checked the source.

With consultation: reviewer says "S8 uses TumblerAdd." Reviser checks the foundation — TumblerAdd doesn't exist, but OrdinalShift provides the same operation. Revision cites OrdinalShift. The issue is resolved in one cycle because the reviser consulted the authority.

## Origin

Present from the first discovery runs on the Xanadu formalization. The two-authority architecture separated theory and evidence channels, but during review/revise the agents would sometimes produce findings that contradicted the source material. Adding the ability for the reviser to consult the original sources during revision — selectively, when uncertain — eliminated a class of drift errors where agents refined each other's mistakes rather than the source material.