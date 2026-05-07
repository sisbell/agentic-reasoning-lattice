# Claim Extraction: New Workshop ASN

You are extracting specific claims from an origin ASN into a new
workshop ASN. The new ASN is a temporary home where these claims can
be refined independently before being absorbed into a destination ASN
that already covers their domain.

This is a **strict extraction** — copy the claims and their proofs
faithfully from the origin, with no improvements, additions, or
editorial changes.

## Operator's rationale

The operator chose to extract these specific claims because:

{{rationale}}

## Origin ASN (source of the claims)

{{origin_content}}

## Destination domain — foundation context

{{foundation_statements}}

## Destination domain — already-covered claims

{{absorb_into_statements}}

## Task

Extract the following claims from the origin ASN into a new workshop
ASN that will eventually be absorbed into the destination:

**Claims to extract:** {{claims}}
**New ASN:** {{new_label}}
**Will absorb into:** {{absorb_into_label}} ({{absorb_into_title}})
**Origin:** {{origin_label}}

For each listed claim label, find it in the origin ASN and extract:
1. The full formal statement with its label and type annotation
2. The complete proof
3. Any worked examples that follow the proof
4. Any supporting definitions needed that are NOT already covered by
   the destination ASN

## Output Format

Write a complete ASN reasoning document. Follow this structure exactly:

```
# {{new_label}}: {{new_title}}

*{{date}}*

[One paragraph: what this ASN extracts and why these claims belong in
the destination's domain. Do not reference the origin ASN.]

## [Section for each claim or group]

**LABEL** — *Name* (TYPE, construct). [Formal statement]

*Proof.* [Complete proof]  ∎

[Worked example if present in origin]

## Statement registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| ... | ... | ... | introduced |

## Open Questions

[Any open questions from the origin ASN that relate specifically to
the extracted claims. Omit if none are relevant.]
```

## Constraints

1. **Strict extraction.** Copy claim statements and proofs from the
   origin verbatim. Do not rephrase, simplify, or "improve" them.
2. **Self-contained.** The workshop ASN must be readable without the
   origin. Include any context needed to understand the extracted
   claims, referencing the destination ASN when appropriate.
3. **No new content.** Do not add claims, lemmas, or discussion that
   do not appear in the origin.
4. **No origin references.** Do not mention the origin ASN. The
   workshop ASN stands on its own as part of the destination's domain.
5. **Supporting material.** If a proof depends on a claim that is NOT
   being extracted and is NOT in the destination's coverage, note the
   dependency explicitly.
6. **Absorb-readiness.** The workshop ASN's framing should anticipate
   absorption into the destination — its claims should sit naturally
   alongside the destination's existing claims, using compatible
   vocabulary and assumptions.

Output ONLY the ASN document. No commentary before or after.
