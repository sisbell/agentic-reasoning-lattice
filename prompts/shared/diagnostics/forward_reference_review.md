# Forward-Reference Review (Diagnostic)

You are reading a specification note that has developed through many review/revise cycles. Your task is narrow: find prose that exists *because the document has to manage forward references and placement ordering*, rather than prose that advances the specification itself.

This is a diagnostic, not a full review. Do not check proof correctness, edge cases, or completeness. Do not propose new content. Look for one thing only: meta-prose accumulated to navigate the document's own structure.

## Patterns to flag

**Contract splits with deferral prose.** An entity (axiom, definition, transition, claim) is introduced in one section but its full content lives elsewhere. The introduction site carries deferral prose ("see section X below," "deferred to Y," "the full account is in Z"). Multiple paragraphs deferring to the same downstream section are particularly suspect — they likely accumulated across review cycles without earlier ones being removed.

**Non-circularity justification.** Paragraphs that exist to argue ordering — "placed here to avoid circular dependency on X," "the forward pointer is non-circular by Y argument," "we defer to section Z because P." This is meta-prose about document structure, not about the specification's content.

**Axiom-rationale accretion.** Multiple paragraphs around an axiom or claim that explain why it exists, what it does not assert, or how it differs from related concepts — separate from the axiom statement itself. Often appears as sub-paragraphs labeled "Scope," "Object-level content," "Protocol rationale," "Negative argument," "What is load-bearing," etc.

**Imagined-case prose.** Paragraphs exploring a case the precondition or carrier already excludes. "Were X to happen..." or "if Y were not the case..." prose where X / not-Y is structurally impossible at this point in the proof.

**Use-site inventories.** Prose enumerating downstream uses of a definition — "this is consumed by X, Y, Z" — that adds navigation rather than advancing the definition's meaning.

**Relocated-not-removed paragraphs.** Two or more paragraphs in different parts of the note that say essentially the same thing in different words. Likely a prior review's content was rephrased in a new location without removing the original.

## What NOT to flag

- Concrete examples, analogies, and motivating prose. These advance understanding even when placement seems awkward — flag placement (suggest moving), not existence.
- Proof prose, derivations, case analyses, invariant statements. These are content, not navigation.
- Section overviews and brief framing paragraphs at the start of major sections — these orient the reader.
- Open questions, gaps, and TODOs that mark unfinished work.

If you are uncertain whether something is content-advancing or navigation-only, do not flag it. False positives waste operator time; missing one finding is recoverable.

## Output format

For each finding:

```
### [short title naming the pattern instance]
**Section**: [section name, or "(multiple)" if the pattern spans sections]
**Pattern**: contract-split | non-circular | axiom-rationale | imagined-case | use-site | relocated | other
**Quote**: "[1-3 sentence verbatim snippet]"
**Why flagged**: [one sentence — what makes this navigation-only rather than content-advancing]
**Suggested resolution**: [restructure | remove | merge-with-downstream | other — one short phrase]
```

After all findings, emit a single VERDICT line:

```
VERDICT: CLEAN | LIGHT | HEAVY
```

- `CLEAN` — no findings; the note is structurally tight.
- `LIGHT` — 1-3 findings; minor cleanup opportunities.
- `HEAVY` — 4+ findings; substantive accretion present.

`### ` headers are reserved for findings. Use plain paragraphs for any narrative observations between findings.

## The note

ASN: {{asn_label}}

{{note_content}}
